document.addEventListener("DOMContentLoaded", function() {
    const STORAGE_KEY = "jini_memory";
    let memory = [];
    const micBtn = document.getElementById('micBtn');
    const backBtn = document.getElementById('backBtn');
    const status = document.getElementById('status');
    const wave = document.getElementById('wave');
    let listening = false;
    let audioCtx = null;
    let analyser = null;
    let source = null;
    let dataArray = null;

    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        memory = JSON.parse(saved);
    }

    function saveMemory() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(memory));
    }

    async function initMic() {
        if (audioCtx) return;
        try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        source = audioCtx.createMediaStreamSource(stream);
        source.connect(analyser);
        analyser.fftSize = 512;
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        animate();
        status.textContent = "🎧 Listening — speak to see the core react!";
        } catch (err) {
        status.textContent = "Microphone access denied or not available.";
        console.error(err);
        }
    }

    function stopMic() {
        if (audioCtx) {
            audioCtx.close();
            audioCtx = null;
            analyser = null;
            source = null;
            dataArray = null;
        }
    }

    function animate() {
        if (!listening || !analyser) return;

        requestAnimationFrame(animate);
        analyser.getByteTimeDomainData(dataArray);

        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
            let val = (dataArray[i] - 128) / 128;
            sum += val * val;
        }

        let volume = Math.sqrt(sum / dataArray.length);
        let scale = 1 + Math.min(volume * 8, 0.8);
        wave.style.transform = `scale(${scale})`;
        wave.style.opacity = 0.7 + Math.min(volume * 3, 0.3);
    }

    // Expose showResponse so Python can call it
    eel.expose(showResponse);
    function showResponse(reply) {
        console.log("🤖 AI:", reply);
        status.innerHTML = "JINI: " + reply;

        memory.push({ role: "assistant", text: reply });
        saveMemory();
    }

    micBtn.addEventListener("click", async () => {
        if (!listening) {
        status.textContent = "🎙️ Listening...";
        micBtn.textContent = "🛑 Stop Listening";
        micBtn.style.background = "linear-gradient(90deg, #ef4444, #b91c1c)";
        initMic();
        listening = true;

        // Start backend mic input
        try {
            await eel.mic_input()();
        } catch (error) {
            console.error(error);
            status.textContent = "⚠️ Couldn't access mic or backend error.";
        }

        stopMic();

        // Reset after speaking
        listening = false;
        micBtn.textContent = "🎧 Start Listening";
        micBtn.style.background = "linear-gradient(90deg, #06b6d4, #7c3aed)";
        }
    });

    backBtn.addEventListener("click", () => {
        window.close();
    });

    function goTo(page) {
        if (typeof eel !== "undefined") {
        eel.navigate_to(page)();
        } else {
        window.location.href = page;
        }
    }
});