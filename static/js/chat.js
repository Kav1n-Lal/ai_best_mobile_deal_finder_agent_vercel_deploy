const params = new URLSearchParams(window.location.search);

let threadId = params.get("thread_id");


// ---------------------------------------------------------
// Generate thread ID if missing
// ---------------------------------------------------------

if (!threadId) {

    threadId = crypto.randomUUID();

    const url = new URL(window.location.href);

    url.searchParams.set("thread_id", threadId);

    window.history.replaceState(
        {},
        "",
        url
    );
}


// ---------------------------------------------------------
// DOM
// ---------------------------------------------------------

const chatMessages =
    document.getElementById("chatMessages");

const messageInput =
    document.getElementById("messageInput");

const chatForm =
    document.getElementById("chatForm");

const sendButton =
    document.getElementById("sendButton");

const typingIndicator =
    document.getElementById("typingIndicator");

const sidebar =
    document.getElementById("sidebar");

const historyMessages =
    document.getElementById("historyMessages");

const historyThreadId =
    document.getElementById("historyThreadId");

const clearModal =
    document.getElementById("clearModal");


// ---------------------------------------------------------
// Thread ID
// ---------------------------------------------------------

historyThreadId.textContent = threadId;


// ---------------------------------------------------------
// Sidebar
// ---------------------------------------------------------

document
    .getElementById("historyButton")
    .addEventListener("click", async () => {

        sidebar.classList.add("open");

        await loadHistory();
    });


document
    .getElementById("closeSidebarButton")
    .addEventListener("click", () => {

        sidebar.classList.remove("open");
    });


// ---------------------------------------------------------
// New Chat
// ---------------------------------------------------------

document
    .getElementById("newChatButton")
    .addEventListener("click", () => {

        const newThreadId =
            crypto.randomUUID();

        window.location.href =
            `/chat?thread_id=${encodeURIComponent(newThreadId)}`;
    });


// ---------------------------------------------------------
// Suggestions
// ---------------------------------------------------------

document
    .querySelectorAll(".suggestion")
    .forEach(button => {

        button.addEventListener("click", () => {

            messageInput.value =
                button.dataset.query;

            messageInput.focus();

            chatForm.requestSubmit();
        });
    });


// ---------------------------------------------------------
// Enter / Shift+Enter
// ---------------------------------------------------------

messageInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            chatForm.requestSubmit();
        }
    }
);


// ---------------------------------------------------------
// Send message
// ---------------------------------------------------------

chatForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        const query =
            messageInput.value.trim();

        if (!query) {
            return;
        }

        messageInput.value = "";

        hideWelcome();

        addMessage(
            "user",
            query
        );

        setLoading(true);

        try {

            const response =
                await fetch("/deals", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        query: query,
                        thread_id: threadId
                    })
                });


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Something went wrong."
                );
            }


            addMessage(
                "assistant",
                data.response || "No response received."
            );


        } catch (error) {

            addMessage(
                "assistant",
                `Error: ${error.message}`
            );

        } finally {

            setLoading(false);

            messageInput.focus();
        }
    }
);


// ---------------------------------------------------------
// Add message
// ---------------------------------------------------------

function addMessage(
    role,
    content
) {

    const row =
        document.createElement("div");

    row.className =
        `message-row ${role}`;


    const message =
        document.createElement("div");

    message.className =
        `message ${role}`;


    message.textContent = content;


    row.appendChild(message);

    chatMessages.appendChild(row);


    scrollToBottom();
}


// ---------------------------------------------------------
// Loading
// ---------------------------------------------------------

function setLoading(isLoading) {

    if (isLoading) {

        typingIndicator.classList.remove(
            "hidden"
        );

        sendButton.disabled = true;

    } else {

        typingIndicator.classList.add(
            "hidden"
        );

        sendButton.disabled = false;
    }

    scrollToBottom();
}


// ---------------------------------------------------------
// Scroll
// ---------------------------------------------------------

function scrollToBottom() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ---------------------------------------------------------
// Welcome
// ---------------------------------------------------------

function hideWelcome() {

    const welcome =
        document.getElementById(
            "welcomeMessage"
        );

    if (welcome) {

        welcome.remove();
    }
}


// ---------------------------------------------------------
// Load conversation history
// ---------------------------------------------------------

async function loadHistory() {

    historyMessages.innerHTML =
        `
        <div class="history-loading">
            Loading...
        </div>
        `;


    try {

        const response =
            await fetch(
                `/history/${encodeURIComponent(threadId)}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to load history."
            );
        }


        renderHistory(
            data.messages
        );


    } catch (error) {

        historyMessages.innerHTML =
            `
            <div class="history-item">
                <div class="history-content">
                    ${escapeHtml(error.message)}
                </div>
            </div>
            `;
    }
}


// ---------------------------------------------------------
// Render history
// ---------------------------------------------------------

function renderHistory(messages) {

    historyMessages.innerHTML = "";


    if (!messages || messages.length === 0) {

        historyMessages.innerHTML =
            `
            <div class="history-item">
                <div class="history-content">
                    No messages yet.
                </div>
            </div>
            `;

        return;
    }


    messages.forEach(message => {

        const item =
            document.createElement("div");

        item.className =
            "history-item";


        const role =
            document.createElement("div");

        role.className =
            "history-role";


        role.textContent =
            message.type === "human"
                ? "You"
                : "Assistant";


        const content =
            document.createElement("div");

        content.className =
            "history-content";


        content.textContent =
            message.content;


        item.appendChild(role);

        item.appendChild(content);

        historyMessages.appendChild(item);
    });
}


// ---------------------------------------------------------
// Clear chat
// ---------------------------------------------------------

document
    .getElementById("clearChatButton")
    .addEventListener("click", () => {

        clearModal.classList.remove(
            "hidden"
        );
    });


document
    .getElementById("cancelClearButton")
    .addEventListener("click", () => {

        clearModal.classList.add(
            "hidden"
        );
    });


document
    .getElementById("confirmClearButton")
    .addEventListener(
        "click",
        clearCurrentChat
    );


async function clearCurrentChat() {

    const button =
        document.getElementById(
            "confirmClearButton"
        );


    button.disabled = true;

    button.textContent =
        "Clearing...";


    try {

        const response =
            await fetch(
                `/history/${encodeURIComponent(threadId)}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to clear chat."
            );
        }


        // Clear visible chat

        chatMessages.innerHTML = "";


        // Restore welcome screen

        chatMessages.innerHTML =
            `
            <div
                id="welcomeMessage"
                class="welcome-message"
            >

                <div class="welcome-icon">
                    📱
                </div>

                <h2>
                    How can I help?
                </h2>

                <p>
                    Ask me for the best mobile deal
                    or ask a question about mobile phones.
                </p>

            </div>
            `;


        // Clear history panel

        historyMessages.innerHTML =
            `
            <div class="history-item">
                <div class="history-content">
                    No messages yet.
                </div>
            </div>
            `;


        clearModal.classList.add(
            "hidden"
        );


        sidebar.classList.remove(
            "open"
        );


    } catch (error) {

        alert(
            `Failed to clear chat: ${error.message}`
        );

    } finally {

        button.disabled = false;

        button.textContent =
            "Clear Chat";
    }
}


// ---------------------------------------------------------
// HTML escaping
// ---------------------------------------------------------

function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}