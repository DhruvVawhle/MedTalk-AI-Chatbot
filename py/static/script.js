document.querySelector("#send-btn").addEventListener("click", async () => {
    const input = document.querySelector("#user-input");
    const message = input.value.trim();

    if (message) {
        const chatWindow = document.querySelector(".chat-window");

        // Add user message to chat window
        const userMessage = document.createElement("div");
        userMessage.classList.add("message", "user-message");
        userMessage.innerHTML = `<span>${message}</span>`;
        chatWindow.appendChild(userMessage);

        input.value = ""; // Clear input field
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to latest message

        try {
            // Send user input to the server
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) {
                throw new Error(`Server error! Status code: ${response.status}`);
            }

            const data = await response.json();

            // Add bot response to chat window
            const botMessage = document.createElement("div");
            botMessage.classList.add("message", "bot-message");
            botMessage.innerHTML = `<span>${data.reply}</span>`;
            chatWindow.appendChild(botMessage);
            chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll

        } catch (error) {
            // Handle server errors or network issues
            const errorMessage = document.createElement("div");
            errorMessage.classList.add("message", "error-message");
            errorMessage.innerHTML = `<span>Unable to reach the server. Please try again later.</span>`;
            chatWindow.appendChild(errorMessage);
            chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll
        }
    }
});
///AIzaSyCdabqwmcBZzoWT_7JhRuPU40UA7FWRkeM