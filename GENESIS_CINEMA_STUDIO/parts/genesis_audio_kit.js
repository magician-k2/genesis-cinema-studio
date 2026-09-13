/**
 * 🎵 GENESIS Audio & MPC Kit | 共通音響・MPCパーツ
 * Web Audio APIの初期化、16-Pad MPCグリッドの構築、サンプル再生、波形ビジュアライザー描画を
 * 1つのクラスにカプセル化し、Cinema StudioやMusic Studioから共通利用できるように部品化。
 */
class GenesisAudioKit {
  constructor(options = {}) {
    this.containerId = options.containerId || 'genesis-mpc-container';
    this.canvasId = options.canvasId || 'genesis-visualizer-canvas';
    this.onPadTrigger = options.onPadTrigger || null;
    this.audioCtx = null;
    this.analyser = null;
    this.samples = new Map();
    this.isInitialized = false;

    this.defaultPadConfig = [
      { key: '1', name: 'Kick 1', type: 'drums', freq: 65, color: '#ef4444' },
      { key: '2', name: 'Snare 1', type: 'drums', freq: 220, color: '#ef4444' },
      { key: '3', name: 'HiHat Cl', type: 'drums', freq: 800, color: '#ef4444' },
      { key: '4', name: 'HiHat Op', type: 'drums', freq: 1200, color: '#ef4444' },
      { key: 'Q', name: 'Sub 808', type: 'bass', freq: 45, color: '#eab308' },
      { key: 'W', name: 'Acid Bass', type: 'bass', freq: 110, color: '#eab308' },
      { key: 'E', name: 'Synth Lead', type: 'melody', freq: 440, color: '#a855f7' },
      { key: 'R', name: 'Pluck Arp', type: 'melody', freq: 660, color: '#a855f7' },
      { key: 'A', name: 'Vocal Chop', type: 'vocals', freq: 520, color: '#06b6d4' },
      { key: 'S', name: 'Vocal Breath', type: 'vocals', freq: 780, color: '#06b6d4' },
      { key: 'D', name: 'Atmosphere', type: 'melody', freq: 330, color: '#a855f7' },
      { key: 'F', name: 'Crash Cym', type: 'drums', freq: 1500, color: '#ef4444' },
      { key: 'Z', name: 'Perc Click', type: 'drums', freq: 950, color: '#ef4444' },
      { key: 'X', name: 'FM Bass', type: 'bass', freq: 85, color: '#eab308' },
      { key: 'C', name: 'Bell Chime', type: 'melody', freq: 880, color: '#a855f7' },
      { key: 'V', name: 'Riser FX', type: 'melody', freq: 600, color: '#a855f7' }
    ];
  }

  initAudioContext() {
    if (this.audioCtx) return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    this.audioCtx = new AudioContextClass();
    this.analyser = this.audioCtx.createAnalyser();
    this.analyser.fftSize = 256;
    this.analyser.connect(this.audioCtx.destination);
    this.isInitialized = true;
    this.startVisualizer();
  }

  playSyntheticTone(freq, type = 'sine', duration = 0.3) {
    this.initAudioContext();
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);

    gain.gain.setValueAtTime(0.4, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + duration);

    osc.connect(gain);
    gain.connect(this.analyser);

    osc.start();
    osc.stop(this.audioCtx.currentTime + duration);
  }

  triggerPad(index) {
    const pad = this.defaultPadConfig[index];
    if (!pad) return;

    // Visual feedback
    const padElem = document.querySelector(`[data-genesis-pad="${index}"]`);
    if (padElem) {
      padElem.classList.add('genesis-pad-active');
      setTimeout(() => padElem.classList.remove('genesis-pad-active'), 150);
    }

    // Play sound (synthetic or loaded sample)
    if (this.samples.has(index)) {
      const audio = new Audio(this.samples.get(index));
      audio.play().catch(() => {});
    } else {
      const type = pad.type === 'bass' ? 'sawtooth' : (pad.type === 'drums' ? 'triangle' : 'sine');
      this.playSyntheticTone(pad.freq, type, 0.25);
    }

    if (this.onPadTrigger) {
      this.onPadTrigger(pad, index);
    }
  }

  renderMPC(targetElementId = this.containerId) {
    const container = document.getElementById(targetElementId);
    if (!container) return;

    container.innerHTML = `
      <style>
        .genesis-mpc-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 10px;
          background: rgba(15, 23, 42, 0.6);
          padding: 14px;
          border-radius: 12px;
          border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .genesis-mpc-pad {
          background: rgba(30, 41, 59, 0.7);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          padding: 12px 6px;
          text-align: center;
          cursor: pointer;
          user-select: none;
          transition: all 0.1s ease;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 4px;
        }
        .genesis-mpc-pad:hover {
          background: rgba(51, 65, 85, 0.9);
          transform: translateY(-2px);
          border-color: var(--pad-color, #8b5cf6);
        }
        .genesis-mpc-pad.genesis-pad-active {
          transform: scale(0.95);
          background: var(--pad-color, #8b5cf6) !important;
          color: #ffffff !important;
          box-shadow: 0 0 16px var(--pad-color, #8b5cf6);
        }
        .genesis-pad-key {
          font-family: 'JetBrains Mono', monospace;
          font-weight: 800;
          font-size: 0.85rem;
          color: #f8fafc;
        }
        .genesis-pad-name {
          font-size: 0.7rem;
          color: #94a3b8;
          font-family: 'Outfit', sans-serif;
        }
      </style>
      <div class="genesis-mpc-grid">
        ${this.defaultPadConfig.map((pad, idx) => `
          <div class="genesis-mpc-pad" data-genesis-pad="${idx}" style="--pad-color: ${pad.color};" onclick="window.__genesis_audio_kit.triggerPad(${idx})">
            <span class="genesis-pad-key">${pad.key}</span>
            <span class="genesis-pad-name">${pad.name}</span>
          </div>
        `).join('')}
      </div>
    `;

    window.__genesis_audio_kit = this;
    this.bindKeyboard();
  }

  bindKeyboard() {
    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
      const key = e.key.toUpperCase();
      const idx = this.defaultPadConfig.findIndex(p => p.key === key);
      if (idx !== -1) {
        e.preventDefault();
        this.triggerPad(idx);
      }
    });
  }

  startVisualizer(canvasId = this.canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !this.analyser) return;
    const ctx = canvas.getContext('2d');
    const bufferLength = this.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      requestAnimationFrame(draw);
      this.analyser.getByteFrequencyData(dataArray);

      ctx.fillStyle = 'rgba(7, 9, 14, 0.3)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const barWidth = (canvas.width / bufferLength) * 2.5;
      let barHeight;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        barHeight = (dataArray[i] / 255) * canvas.height;
        const grad = ctx.createLinearGradient(0, canvas.height, 0, 0);
        grad.addColorStop(0, '#06b6d4');
        grad.addColorStop(0.5, '#8b5cf6');
        grad.addColorStop(1, '#ec4899');

        ctx.fillStyle = grad;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        x += barWidth + 1;
      }
    };
    draw();
  }
}

window.GenesisAudioKit = GenesisAudioKit;
