let ws;
let audioContext;
let sourceNode;
let workletNode;

const transcript = document.getElementById('transcript');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');

const CHARS_PER_SEC = 15; // typing effect speed

// ---------------- order management ----------------
let lastSeq = 0;
const pending = {};
let queueProcessing = false;
let typingAbort = false;

// ---------------- type a full line slowly ----------------
async function typeLine(text) {
  text = text.trim();
  typingAbort = false;

  for (let i = 0; i < text.length; i++) {
    if (typingAbort) {
      transcript.textContent += text.slice(i);
      transcript.scrollTop = transcript.scrollHeight;
      break;
    }
    transcript.textContent += text[i];
    transcript.scrollTop = transcript.scrollHeight;
    await new Promise(r => setTimeout(r, 1000 / CHARS_PER_SEC));
  }
  transcript.textContent += "\n";
}

// ---------------- process queue in order ----------------
async function processQueue() {
  if (queueProcessing) {
    typingAbort = true; // abort current typing
    return;
  }

  queueProcessing = true;
  try {
    while (pending[lastSeq + 1]) {
      const line = pending[lastSeq + 1];
      delete pending[lastSeq + 1];
      lastSeq++;
      await typeLine(line);
    }
  } finally {
    queueProcessing = false;
  }
}

// ---------------- start recording and WS ----------------
startBtn.onclick = async () => {
  // Reset sequence for fresh session
  lastSeq = 0;
  for (let key in pending) delete pending[key];

  // Open WebSocket
  ws = new WebSocket("ws://46.224.122.101:8181");
  ws.binaryType = "arraybuffer";

  ws.onopen = () => console.log("[INFO] WebSocket connected");

  ws.onmessage = (msg) => {
    const data = msg.data.trim();
    if (!data) return;

    const colonIndex = data.indexOf(":");
    if (colonIndex === -1) return;

    const seq = parseInt(data.slice(3, colonIndex), 10); // skip "SEQ"
    const text = data.slice(colonIndex + 1);

    pending[seq] = text;
    processQueue();
  };

  ws.onclose = () => console.log("[INFO] WebSocket closed");
  ws.onerror = (err) => console.error("[ERROR] WebSocket", err);

  // ---------------- Audio setup ----------------
  audioContext = new AudioContext();
  await audioContext.audioWorklet.addModule(URL.createObjectURL(new Blob([`
    class PCMProcessor extends AudioWorkletProcessor {
      process(inputs, outputs) {
        const input = inputs[0][0];
        if (!input) return true;
        this.port.postMessage(input);
        return true;
      }
    }
    registerProcessor('pcm-processor', PCMProcessor);
  `], { type: 'application/javascript' })));

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  sourceNode = audioContext.createMediaStreamSource(stream);

  workletNode = new AudioWorkletNode(audioContext, 'pcm-processor');
  workletNode.port.onmessage = (event) => {
    const float32Array = event.data;

    // Resample to 16kHz
    const targetRate = 16000;
    const ratio = audioContext.sampleRate / targetRate;
    const length = Math.floor(float32Array.length / ratio);
    const resampled = new Float32Array(length);
    for (let i = 0; i < length; i++) {
      resampled[i] = float32Array[Math.floor(i * ratio)];
    }

    // Convert float32 -> 16-bit PCM
    const buffer = new ArrayBuffer(resampled.length * 2);
    const view = new DataView(buffer);
    for (let i = 0; i < resampled.length; i++) {
      let s = Math.max(-1, Math.min(1, resampled[i]));
      view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    }

    if (ws.readyState === WebSocket.OPEN) ws.send(buffer);
  };

  sourceNode.connect(workletNode);
  workletNode.connect(audioContext.destination);

  console.log("[INFO] Recording started (AudioWorklet, 16kHz PCM)");
};

// ---------------- stop recording ----------------
stopBtn.onclick = () => {
  if (workletNode) workletNode.disconnect();
  if (sourceNode) sourceNode.disconnect();
  if (audioContext) audioContext.close();
  if (ws) ws.close();
  console.log("[INFO] Recording stopped");
};