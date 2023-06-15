document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
  
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const message = userInput.value;
      userInput.value = '';
  
      // Display user message in chat log with typing motion
      const userMessage = document.createElement('div');
      userMessage.classList.add('message');
      chatLog.appendChild(userMessage);
  
      typeMessage(userMessage, message, () => {
        // Display loading message in chat log with typing motion
        const loadingMessage = document.createElement('div');
        loadingMessage.classList.add('message', 'loading-message');
        chatLog.appendChild(loadingMessage);
  
        typeMessage(loadingMessage, 'Loading...', () => {
          // Make API request to process the message
          fetch('/process_request/', {
            method: 'POST',
            body: new URLSearchParams({
              request: message
            })
          })
            .then(response => response.json())
            .then(data => {
              // Remove loading message from chat log
              chatLog.removeChild(loadingMessage);
  
              // Display processed message in chat log with typing motion
              const processedMessage = document.createElement('div');
              processedMessage.classList.add('message');
              chatLog.appendChild(processedMessage);
  
              typeMessage(processedMessage, data.processed_request);
            })
            .catch(error => {
              // Remove loading message from chat log
              chatLog.removeChild(loadingMessage);
  
              // Display error message in chat log with typing motion
              const errorMessage = document.createElement('div');
              errorMessage.classList.add('message', 'error-message');
              chatLog.appendChild(errorMessage);
  
              typeMessage(errorMessage, 'Error occurred. Please try again later.');
            });
        });
      });
    });
  
    function typeMessage(element, message, callback) {
      let index = 0;
      const typingSpeed = 50; // Adjust typing speed (milliseconds)
  
      function type() {
        if (index < message.length) {
          element.innerHTML += message.charAt(index);
          index++;
          setTimeout(type, typingSpeed);
        } else {
          callback();
        }
      }
  
      type();
    }
  });