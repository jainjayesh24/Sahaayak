const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        localStorage.setItem('username', username);
        window.location.href = 'chat.html';
    });
}

if (document.getElementById('userGreeting')) {
    const userGreeting = localStorage.getItem('username') || 'there';
    document.getElementById('userGreeting').innerText = userGreeting;
}

async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    const chatMessages = document.getElementById("chatMessages");

    if (userInput.trim() !== "") {
        chatMessages.innerHTML += `<div class="message user">${userInput}</div>`;

        // Send message to Flask backend
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        const data = await response.json();
        setTimeout(() => {
            chatMessages.innerHTML += `<div class="message bot">${data.response}</div>`;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
        
        document.getElementById("userInput").value = "";
    }
}

function showTypingEffect() {
    let botMessage = document.createElement("div");
    botMessage.classList.add("bot-message", "message");
    botMessage.innerHTML = '<span class="typing"></span>';
    document.querySelector(".chat-box").appendChild(botMessage);
}


function getBotResponse(input) {
    input = input.toLowerCase();

    const responses = {
        "hello": "Hey there! How are you feeling today?",
        "hi": "Hello! What’s on your mind?",
        "how are you": "I’m just a bot, but I’m here to listen. How are *you* feeling?",
        "help": "I’m here for you. You can talk to me about anything that’s bothering you.",
        "sad": "I'm sorry to hear that. Want to talk about what’s making you feel this way?",
        "happy": "That’s amazing to hear! What’s been making you feel so good?",
        "stressed": "Stress can be tough. Maybe taking a few deep breaths could help. Or talk to me about what’s causing it.",
        "bye": "Take care of yourself. I’m always here if you need to talk."
    };

    for (const keyword in responses) {
        if (input.includes(keyword)) {
            return responses[keyword];
        }
    }

    return "I'm here to listen. Can you tell me more about how you're feeling?";
}
