/* ---------- UI elements ---------- */
document.addEventListener("DOMContentLoaded", function () {
    const historyEl = document.getElementById("history");
    const promptEl = document.getElementById("prompt");
    const sendBtn = document.getElementById("sendBtn");
    const micBtn = document.getElementById("micBtn");
    const statusEl = document.getElementById("status");
    const robotCore = document.getElementById("robotCore");
    const mouth = document.getElementById("mouth");
    const eyeL = document.getElementById("eyeL");
    const eyeR = document.getElementById("eyeR");
    const chestLight = document.getElementById("chestLight");

    const wakeSound = document.getElementById("wakeSound");
    const processingSound = document.getElementById("processingSound");
    const endSound = document.getElementById("endSound");

    /* ---------- conversation memory (client) ---------- */
    const memory = []; // list of {role:'user'|'assistant', text}

    // ----- Conversation Persistence -----
    const STORAGE_KEY = "jini_memory";

    // Load conversation history from localStorage on page load
    window.addEventListener("DOMContentLoaded", () => {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            const messages = JSON.parse(saved);
            messages.forEach(msg => appendBubble(msg.text, msg.role));
            memory.push(...messages);
        }
    });

    // Save new messages to localStorage
    function saveMemory() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(memory));
    }


    /* ---------- helpers ---------- */
    function appendBubble(text, role) {
        const d = document.createElement("div");
        d.className = "bubble " + (role === "user" ? "user" : "ai");
        d.innerHTML = `<strong>${role === "user" ? "You" : "Jini"}:</strong> ${escapeHtml(text)}`;
        historyEl.appendChild(d);
        historyEl.scrollTop = historyEl.scrollHeight;
    }

    function escapeHtml(s) {
        return s.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    }

    /* ---------- robot animations ---------- */
    function startTalking() {
        mouth.style.animation = "mouthTalk 0.26s infinite";
        robotCore.classList.add("glow");
        chestLight.style.opacity = "1";
    }
    function stopTalking() {
        mouth.style.animation = "none";
        robotCore.classList.remove("glow");
        chestLight.style.opacity = "0.9";
        endSound.play();
    }
    function blink() {
        eyeL.style.transform = "scaleY(0.15)";
        eyeR.style.transform = "scaleY(0.15)";
        setTimeout(() => { eyeL.style.transform = "scaleY(1)"; eyeR.style.transform = "scaleY(1)"; }, 160);
    }
    setInterval(blink, 5000);

    /* ---------- OpenAI call (server proxy) ---------- */
    async function askServer(prompt) {
        try {
        const reply = await eel.get_ai_response(prompt)();  // Call Python via Eel
        return reply;
        } catch (err) {
        console.error("Eel communication error:", err);
        return "Sorry — I couldn’t reach the AI backend.";
        }
    }

    /* ---------- Speak using browser TTS (robust) ---------- */
    function speakAndAnimate(text) {
        if (!("speechSynthesis" in window)) {
        // fallback: no tts
        return;
        }
        const u = new SpeechSynthesisUtterance(text);
        u.lang = "en-US";
        u.rate = 1;
        u.onstart = () => { startTalking(); processingSound.pause(); processingSound.currentTime = 0; };
        u.onend = () => { stopTalking(); };
        speechSynthesis.speak(u);
    }

    /* ---------- send typed prompt ---------- */
    async function sendPrompt() {
        const t = promptEl.value.trim();
        if (!t) return;
        appendBubble(t, "user");
        memory.push({ role: "user", text: t });
        saveMemory();
        promptEl.value = "";
        statusEl.textContent = "Thinking...";
        processingSound.play();

        try {
        const reply = await askServer(t);
        appendBubble(reply, "assistant");
        memory.push({ role: "assistant", text: reply });
        saveMemory();
        processingSound.pause();
        processingSound.currentTime = 0;
        speakAndAnimate(reply);
        statusEl.textContent = "Ready";
        } catch (err) {
        processingSound.pause();
        processingSound.currentTime = 0;
        appendBubble("Sorry, server error.", "assistant");
        statusEl.textContent = "Error";
        }
    }

    /* ---------- manual microphone (button) ---------- */
    let micRecognition;
    if ("webkitSpeechRecognition" in window) {
        micRecognition = new webkitSpeechRecognition();
        micRecognition.continuous = false;
        micRecognition.interimResults = false;
        micRecognition.lang = "en-US";

        micRecognition.onstart = () => {
        micBtn.textContent = "🎧";
        statusEl.textContent = "Listening...";
        robotCore.classList.add("glow");
        };
        micRecognition.onend = () => {
        micBtn.textContent = "🎙️";
        statusEl.textContent = "Ready";
        robotCore.classList.remove("glow");
        };
        micRecognition.onresult = (e) => {
        const spoken = e.results[0][0].transcript;
        appendBubble(spoken, "user");
        memory.push({ role: "user", text: spoken });
        // send to server
        statusEl.textContent = "Thinking...";
        processingSound.play();
        askServer(spoken).then(reply => {
            appendBubble(reply, "assistant");
            memory.push({ role: "assistant", text: reply });
            processingSound.pause();
            processingSound.currentTime = 0;
            speakAndAnimate(reply);
            statusEl.textContent = "Ready";
        }).catch(err => {
            appendBubble("Sorry, server error.", "assistant");
            statusEl.textContent = "Error";
        });
        };

        micBtn.addEventListener("click", () => {
        goTo("pages/mic.html");
        });


    } else {
        micBtn.disabled = true;
        micBtn.textContent = "No mic";
    }

    /* ---------- wake-word listener (Jini) ---------- */
    let listeningWake = true;
    function startWakeListener() {
        if (!("webkitSpeechRecognition" in window)) return;
        const r = new webkitSpeechRecognition();
        r.continuous = false;
        r.interimResults = false;
        r.lang = "en-US";

        r.onresult = (e) => {
        const t = e.results[0][0].transcript.toLowerCase();
        blink();
        if (listeningWake && t.includes("jini")) {
            wakeSound.play();
            // short confirmation and then listen for command
            speakAndAnimate("Yes?");
            setTimeout(listenForCommand, 800);
        } else {
            // keep listening
            r.start();
        }
        };

        r.onend = () => {
        if (listeningWake) r.start();
        };
        r.start();
    }

    function listenForCommand() {
        if (!("webkitSpeechRecognition" in window)) return;
        const cr = new webkitSpeechRecognition();
        cr.continuous = false;
        cr.interimResults = false;
        cr.lang = "en-US";
        statusEl.textContent = "Listening for command...";
        cr.onresult = async (e) => {
        const cmd = e.results[0][0].transcript;
        appendBubble(cmd, "user");
        memory.push({ role: "user", text: cmd });
        statusEl.textContent = "Thinking...";
        processingSound.play();
        const reply = await askServer(cmd);
        appendBubble(reply, "assistant");
        memory.push({ role: "assistant", text: reply });
        processingSound.pause();
        processingSound.currentTime = 0;
        speakAndAnimate(reply);
        statusEl.textContent = "Ready";
        };
        cr.onend = () => { /* if user silent, resume wake listening */ };
        cr.start();
    }

    /* ---------- events ---------- */
    sendBtn.addEventListener("click", sendPrompt);
    promptEl.addEventListener("keydown", (e) => { if (e.key === "Enter") sendPrompt(); });

    startWakeListener();

    // Function to show messages from Python in your UI
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        const status = document.getElementById("status");
        if (status) {
        status.textContent = message;
        } else {
        console.log("Status:", message);
        }
    }

    // Function to show user's spoken/sent text
    eel.expose(senderText);
    function senderText(text) {
        const h1 = document.querySelector("h1");
        if (h1) {
        h1.textContent = text;
        }
    }

    // Optional — show when AI (JINI) is responding
    eel.expose(ShowHood);
    function ShowHood() {
        const h1 = document.querySelector("h1");
        if (h1) {
        h1.textContent = "🤖 JINI is processing...";
        }
    }

    // Reusable navigation helper for Eel or direct browser
    function goTo(page) {
      if (typeof eel !== "undefined") {
        eel.navigate_to(page)();
      } else {
        window.location.href = page;
      }
    }
    const clearBtn = document.getElementById("clearMemory");
    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            localStorage.removeItem(STORAGE_KEY);
            memory.length = 0;
            historyEl.innerHTML = "";
        });
    }
});