document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    let userMessage = document.getElementById("user-input").value.trim(); // Ensure userMessage is defined

    if (userMessage === "") return; // Prevent sending empty messages

    addMessage(userMessage, "user");

    fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage }), // Correct usage
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.reply) {
            addMessage(data.reply, "bot");
        } else {
            addMessage("Error: No response from server", "bot");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        addMessage("Error: Unable to reach server", "bot");
    });

    document.getElementById("user-input").value = ""; // Clear input box
}

function addMessage(text, sender) {
    let chatBox = document.getElementById("chat-box");
    let messageDiv = document.createElement("div");
    messageDiv.classList.add(sender);
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
}
