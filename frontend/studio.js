// ===============================
// Timeline play simulation
// ===============================
const playBtn = document.querySelector(".timeline-controls button:nth-child(2)");

let playing = false;

playBtn.addEventListener("click", () => {
  playing = !playing;
  playBtn.textContent = playing ? "⏸" : "▶";
});

// ===============================
// Tool click feedback
// ===============================
document.querySelectorAll(".tool-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    alert("Tool action will go here");
  });
});

// ===============================
// AI CHAT LOGIC
// ===============================
const chatInput = document.getElementById("chatInput");
const sendChatBtn = document.getElementById("sendChatBtn");
const chatHistory = document.getElementById("chatHistory");

// TEMP: replace later with selected video
const CURRENT_VIDEO = "video1.mp4";

sendChatBtn.addEventListener("click", sendChatMessage);

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendChatMessage();
  }
});

async function sendChatMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  // Show user message
  const userMsg = document.createElement("div");
  userMsg.style.marginBottom = "8px";
  userMsg.textContent = "You: " + message;
  chatHistory.appendChild(userMsg);

  chatInput.value = "";
  chatHistory.scrollTop = chatHistory.scrollHeight;

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        video_name: CURRENT_VIDEO,
        message: message
      })
    });

    if (!res.ok) throw new Error("Chat failed");

    const data = await res.json();

    const aiMsg = document.createElement("div");
    aiMsg.style.color = "#7dd3fc";
    aiMsg.style.marginBottom = "8px";
    aiMsg.textContent = "AI: Edit applied";
    chatHistory.appendChild(aiMsg);

    chatHistory.scrollTop = chatHistory.scrollHeight;

  } catch (err) {
    console.error(err);

    const errMsg = document.createElement("div");
    errMsg.style.color = "#f87171";
    errMsg.textContent = "AI: Error applying edit";
    chatHistory.appendChild(errMsg);
  }
}
