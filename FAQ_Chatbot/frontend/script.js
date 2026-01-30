document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const chatWindow = document.getElementById('chatWindow');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const typingIndicator = document.getElementById('typingIndicator');
    const clearChatBtn = document.getElementById('clearChatBtn');
    
    // API endpoint
    const API_ENDPOINT = 'http://localhost:5000/chat';
    
    // Initial welcome message already in HTML
    
    // Event listener for send button
    sendBtn.addEventListener('click', sendMessage);
    
    // Event listener for Enter key in input field
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Event listener for clear chat button
    clearChatBtn.addEventListener('click', clearChat);
    
    // Function to send a message
    function sendMessage() {
        const message = userInput.value.trim();
        
        // Don't send empty messages
        if (message === '') {
            return;
        }
        
        // Add user message to chat
        addMessageToChat(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator(true);
        
        // Send message to backend API
        sendToBackend(message);
    }
    
    // Function to add a message to the chat window
    function addMessageToChat(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-bubble');
        
        if (sender === 'user') {
            messageElement.classList.add('user-message');
            messageElement.innerHTML = `
                <p>${escapeHtml(message)}</p>
                <span class="message-time">${getCurrentTime()}</span>
            `;
        } else {
            messageElement.classList.add('bot-message');
            messageElement.innerHTML = `
                <p>${formatBotMessage(message)}</p>
                <span class="message-time">${getCurrentTime()}</span>
            `;
        }
        
        chatWindow.appendChild(messageElement);
        
        // Scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
    
    // Function to send message to backend
    async function sendToBackend(message) {
        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Hide typing indicator
            showTypingIndicator(false);
            
            // Add bot's response to chat
            if (data.response) {
                addMessageToChat(data.response, 'bot');
            } else {
                addMessageToChat("I received your message but didn't get a proper response from the server.", 'bot');
            }
            
        } catch (error) {
            console.error('Error sending message to backend:', error);
            
            // Hide typing indicator
            showTypingIndicator(false);
            
            // Show error message in chat
            addMessageToChat(
                "I'm having trouble connecting to the server. Please make sure the backend is running on localhost:5000.", 
                'bot'
            );
        }
    }
    
    // Function to show/hide typing indicator
    function showTypingIndicator(show) {
        if (show) {
            typingIndicator.classList.add('visible');
        } else {
            typingIndicator.classList.remove('visible');
        }
        
        // Scroll to bottom to show typing indicator
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
    
    // Function to clear chat
    function clearChat() {
        // Remove all messages except the welcome message
        const messages = chatWindow.querySelectorAll('.chat-bubble, .welcome-message');
        
        messages.forEach(message => {
            if (message.classList.contains('welcome-message')) {
                // Keep the welcome message but reset its visibility
                message.style.display = 'flex';
            } else {
                message.remove();
            }
        });
        
        // Make sure welcome message is visible
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'flex';
        }
    }
    
    // Helper function to get current time in HH:MM format
    function getCurrentTime() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    }
    
    // Helper function to escape HTML (security)
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Helper function to format bot messages (simple line breaks)
    function formatBotMessage(text) {
        return escapeHtml(text).replace(/\n/g, '<br>');
    }
    
    // Add click event to suggested questions in welcome message
    const suggestedQuestions = document.querySelectorAll('.suggested-questions li');
    suggestedQuestions.forEach(question => {
        question.style.cursor = 'pointer';
        question.addEventListener('click', function() {
            userInput.value = this.textContent;
            userInput.focus();
        });
    });
    
    // Focus on input field when page loads
    userInput.focus();
});