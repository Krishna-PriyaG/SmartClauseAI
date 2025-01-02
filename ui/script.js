const messagesDiv = document.getElementById("messages");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

// Rasa server endpoint
const rasaEndpoint = "http://localhost:5005/webhooks/rest/webhook";

// Function to append a message to the chat
function appendMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Function to send a message to the Rasa bot
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message
    appendMessage("user", message);
    userInput.value = "";

    // Send message to Rasa server
    try {
        const response = await fetch(rasaEndpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ sender: "user", message: message }),
        });

        if (response.ok) {
            const data = await response.json();
            data.forEach((reply) => {
                appendMessage("bot", reply.text);
            });
        } else {
            appendMessage("bot", "Error: Could not connect to the server.");
        }
    } catch (error) {
        appendMessage("bot", "Error: Something went wrong.");
    }
}

// Event listeners
sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});
