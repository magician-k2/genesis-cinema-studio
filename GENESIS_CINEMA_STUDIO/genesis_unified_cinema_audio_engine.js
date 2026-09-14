/**
 * 🎬🎵 GENESIS Unified Cinema & Audio Engine | 映画・音響共通統合エンジン
 * 
 * 映画スタジオ (cinema_lite.html / cinema_studio.html) と
 * 音楽スタジオ (music_studio.html / audio_mixer.html) で共通利用される
 * 中核エンジン。
 * 
 * 主な責務:
 * 1. Web Audio API Singleton 管理 ＆ FFT音響解析 (スペクトル重心/エネルギー/ダイナミクス)
 * 2. 映画コンテ全自動生成 API (/api/music/to_cinema_storyboard) との連携＆キャッシュ
 * 3. 神脈バス (genesis_nervous_bus) による双方向リアルタイム同期 (コンテ・カット・再生ヘッド)
 * 4. Google Veo 3.1 / Gemini Omni 1.1 Flash / Agentic Video プロンプト整形
 * 5. 手続き型効果音 (Procedural SFX) ＆ MPCトーン合成
 */

class GenesisCinemaAudioEngine {
  constructor() {
    this.busName = 'genesis_nervous_bus';
    this.storageKey = 'genesis_active_storyboard';
    this.audioCtx = null;
    this.analyser = null;
    this.masterCompressor = null;
    this.bgmGain = null;
    this.sfxGain = null;
    this.bus = null;
    this.listeners = new Map();
    this.activeStoryboard = null;
    this.activeCutIndex = 0;
    this.isPlaying = false;
    this.currentTime = 0;

    this.initBus();
    this.loadCachedStoryboard();
  }

  // ==============================================================
  // 1. 神脈バス (Synaptic Nervous Bus: BroadcastChannel)
  // ==============================================================
  initBus() {
    try {
      if (typeof window !== 'undefined' && 'BroadcastChannel' in window) {
        this.bus = new BroadcastChannel(this.busName);
        this.bus.onmessage = (event) => {
          if (!event.data || !event.data.type) return;
          this.handleBusMessage(event.data);
        };
      }
    } catch (e) {
      console.warn('[GenesisCinemaAudio] BroadcastChannel not supported or failed:', e);
    }
  }

  on(type, callback) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, new Set());
    }
    this.listeners.get(type).add(callback);
    return () => this.listeners.get(type).delete(callback);
  }

  emitLocal(type, payload) {
    if (this.listeners.has(type)) {
      this.listeners.get(type).forEach((cb) => {
        try { cb(payload); } catch (err) { console.error('[GenesisCinemaAudio] listener error (' + type + '):', err); }
      });
    }
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('genesis:' + type.toLowerCase(), { detail: payload }));
    }
  }

  broadcast(type, payload = {}) {
    const message = Object.assign({ type: type, timestamp: Date.now() }, payload);
    this.emitLocal(type, message);
    if (this.bus) {
      try {
        this.bus.postMessage(message);
      } catch (e) {
        console.warn('[GenesisCinemaAudio] postMessage error:', e);
      }
    }
  }

  handleBusMessage(msg) {
    switch (msg.type) {
      case 'CINEMA_STORYBOARD_SYNC':
        if (msg.storyboard) {
          this.activeStoryboard = msg.storyboard;
          this.emitLocal('storyboard', msg.storyboard);
        }
        break;
      case 'CUT_SELECT_SYNC':
        if (typeof msg.cutIndex === 'number') {
          this.activeCutIndex = msg.cutIndex;
          this.emitLocal('cutselect', { cutIndex: msg.cutIndex, cut: msg.cut, origin: msg.origin });
        }
        break;
      case 'PLAYHEAD_SYNC':
        if (typeof msg.currentTime === 'number') {
          this.currentTime = msg.currentTime;
          this.isPlaying = !!msg.isPlaying;
          this.emitLocal('playhead', { currentTime: msg.currentTime, isPlaying: msg.isPlaying });
        }
        break;
      case 'AUDIO_STEM_SYNC':
        this.emitLocal('stems', msg.stems || {});
        break;
      default:
        this.emitLocal(msg.type, msg);
        break;
    }
  }

  // ==============================================================
  // 2. Web Audio API Singleton & 音響解析
  // ==============================================================
  initAudioContext() {
    if (typeof window === 'undefined') return null;
    if (!this.audioCtx) {
      const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtxClass) return null;
      this.audioCtx = new AudioCtxClass();

      // Master Compressor
      this.masterCompressor = this.audioCtx.createDynamicsCompressor();
      this.masterCompressor.threshold.setValueAtTime(-16, this.audioCtx.currentTime);
      this.masterCompressor.knee.setValueAtTime(20, this.audioCtx.currentTime);
      this.masterCompressor.ratio.setValueAtTime(3.5, this.audioCtx.currentTime);
      this.masterCompressor.connect(this.audioCtx.destination);

      // Master BGM Gain
      this.bgmGain = this.audioCtx.createGain();
      this.bgmGain.gain.setValueAtTime(0.3, this.audioCtx.currentTime);
      this.bgmGain.connect(this.masterCompressor);

      // SFX Gain
      this.sfxGain = this.audioCtx.createGain();
      this.sfxGain.gain.setValueAtTime(0.4, this.audioCtx.currentTime);
      this.sfxGain.connect(this.masterCompressor);

      // FFT Analyser
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 512;
      this.bgmGain.connect(this.analyser);
    }

    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume().catch(() => {});
    }
    return this.audioCtx;
  }

  getAudioContext() {
    return this.initAudioContext();
  }

  analyzeAudioBuffer(buffer) {
    if (!buffer) return null;
    const channelData = buffer.getChannelData(0);
    const length = channelData.length;
    const sampleRate = buffer.sampleRate;

    let sumSquares = 0;
    let maxAmp = 0;
    for (let i = 0; i < length; i++) {
      const val = channelData[i];
      sumSquares += val * val;
      const absVal = Math.abs(val);
      if (absVal > maxAmp) maxAmp = absVal;
    }
    const rms = Math.sqrt(sumSquares / length);

    // Simple spectral centroid approximation
    const fftSize = 1024;
    let centroid = 2200;
    if (length >= fftSize) {
      let weightedSum = 0;
      let ampSum = 0;
      for (let i = 0; i < fftSize / 2; i++) {
        const amp = Math.abs(channelData[i]);
        const freq = (i * sampleRate) / fftSize;
        weightedSum += freq * amp;
        ampSum += amp;
      }
      if (ampSum > 0.001) {
        centroid = Math.round(weightedSum / ampSum);
      }
    }

    return {
      duration: buffer.duration,
      sampleRate: sampleRate,
      rms: parseFloat(rms.toFixed(4)),
      peak_amplitude: parseFloat(maxAmp.toFixed(4)),
      estimated_centroid: Math.max(400, Math.min(6000, centroid)),
      sub_bass_ratio: centroid < 1200 ? 0.45 : 0.25,
      percussive_ratio: rms > 0.15 ? 0.5 : 0.3
    };
  }

  // ==============================================================
  // 3. 手続き型効果音・トーン再生 (Procedural SFX & Tone)
  // ==============================================================
  playTone(freq = 440, type = 'sine', duration = 0.3) {
    this.initAudioContext();
    if (!this.audioCtx) return;
    const now = this.audioCtx.currentTime;

    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, now);

    gain.gain.setValueAtTime(0.35, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

    osc.connect(gain);
    gain.connect(this.sfxGain);

    osc.start(now);
    osc.stop(now + duration);
  }

  playSFX(sfxType) {
    this.initAudioContext();
    if (!this.audioCtx) return;
    const now = this.audioCtx.currentTime;

    if (sfxType === 'click') {
      this.playTone(1200, 'triangle', 0.05);
    } else if (sfxType === 'drop' || sfxType === 'impact') {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, now);
      osc.frequency.exponentialRampToValueAtTime(35, now + 0.5);

      gain.gain.setValueAtTime(0.5, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

      osc.connect(gain);
      gain.connect(this.sfxGain);
      osc.start(now);
      osc.stop(now + 0.6);
    } else if (sfxType === 'whoosh') {
      const bufferSize = Math.floor(this.audioCtx.sampleRate * 0.4);
      const buffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;

      const noise = this.audioCtx.createBufferSource();
      noise.buffer = buffer;
      const filter = this.audioCtx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(400, now);
      filter.frequency.exponentialRampToValueAtTime(1600, now + 0.2);
      filter.frequency.exponentialRampToValueAtTime(300, now + 0.4);

      const gain = this.audioCtx.createGain();
      gain.gain.setValueAtTime(0.3, now);
      gain.gain.linearRampToValueAtTime(0.001, now + 0.4);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.sfxGain);
      noise.start(now);
      noise.stop(now + 0.4);
    }
  }

  // ==============================================================
  // 4. 映画コンテ全自動生成 ＆ ストーリーボード管理
  // ==============================================================
  loadCachedStoryboard() {
    if (typeof window === 'undefined' || !window.localStorage) return null;
    try {
      const cached = localStorage.getItem(this.storageKey);
      if (cached) {
        this.activeStoryboard = JSON.parse(cached);
      }
    } catch (e) {
      console.warn('[GenesisCinemaAudio] Failed to load cached storyboard:', e);
    }
    return this.activeStoryboard;
  }

  getActiveStoryboard() {
    if (!this.activeStoryboard) {
      this.loadCachedStoryboard();
    }
    return this.activeStoryboard;
  }

  async generateStoryboard(options = {}) {
    const features = options.features || {};
    const trackTitle = options.trackTitle || 'Hans Zimmer Interstellar Style';
    const sceneContext = options.sceneContext || '雨のサイバーパンク新宿 首都高チェイス';
    const durationSec = options.durationSec || 60;

    const payload = {
      features: features,
      track_title: trackTitle,
      scene_context: sceneContext,
      total_duration_sec: durationSec
    };

    const res = await fetch('/api/music/to_cinema_storyboard', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!data || !data.success) {
      throw new Error(data && data.error ? data.error : 'Failed to generate cinema storyboard');
    }

    this.activeStoryboard = data;
    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        localStorage.setItem(this.storageKey, JSON.stringify(data));
      } catch (e) {}
    }

    // Broadcast to cinema studio and other connected windows
    this.broadcast('CINEMA_STORYBOARD_SYNC', { storyboard: data });
    return data;
  }

  selectCut(cutIndex, origin = 'unknown', broadcast = true) {
    this.activeCutIndex = cutIndex;
    const cut = (this.activeStoryboard && this.activeStoryboard.storyboard_cuts) ? this.activeStoryboard.storyboard_cuts[cutIndex] : null;
    if (broadcast) {
      this.broadcast('CUT_SELECT_SYNC', { cutIndex: cutIndex, cut: cut, origin: origin });
    } else {
      this.emitLocal('cutselect', { cutIndex: cutIndex, cut: cut, origin: origin });
    }
  }

  syncPlayhead(currentTime, isPlaying = false, broadcast = true) {
    this.currentTime = currentTime;
    this.isPlaying = isPlaying;
    if (broadcast) {
      this.broadcast('PLAYHEAD_SYNC', { currentTime: currentTime, isPlaying: isPlaying });
    } else {
      this.emitLocal('playhead', { currentTime: currentTime, isPlaying: isPlaying });
    }
  }

  // ==============================================================
  // 5. プロンプト生成・整形 (Veo 3.1 & Gemini Omni 1.1 Flash)
  // ==============================================================
  formatPrompts(storyboard = this.activeStoryboard) {
    if (!storyboard || !storyboard.storyboard_cuts) {
      return { veo: '', agentic: '', cuts: [] };
    }

    const cuts = storyboard.storyboard_cuts;

    const veoText = cuts.map(c =>
      '[' + c.cut_id + ': ' + c.section + ' (' + c.timecode + ')]\n' +
      'Shot: ' + c.shot_type + ' | Motion: ' + c.camera_motion + '\n' +
      'Prompt: ' + c.video_generation_prompt + '\n'
    ).join('\n');

    const agenticText = storyboard.gemini_omni_script || cuts.map(c => {
      const agentRole = (c.agentic_video_spec && c.agentic_video_spec.agent_role) ? c.agentic_video_spec.agent_role : 'Cinematography Agent';
      const anchor = (c.agentic_video_spec && c.agentic_video_spec.perceptual_anchor) ? c.agentic_video_spec.perceptual_anchor : 'Protagonist Expression';
      const omniPrompt = c.gemini_omni_prompt || c.video_generation_prompt;
      return '[' + c.cut_id + ': ' + c.section + ' (' + c.timecode + ')]\n' +
             'Omni Prompt: ' + omniPrompt + '\n' +
             'Agentic Role: ' + agentRole + ' | Anchor: ' + anchor + '\n';
    }).join('\n\n');

    return {
      veo: veoText,
      agentic: agenticText,
      cuts: cuts,
      look: storyboard.cinematic_look || {}
    };
  }
}

// Global Singleton Export
if (typeof window !== 'undefined') {
  window.GenesisCinemaAudioEngine = GenesisCinemaAudioEngine;
  if (!window.genesisCinemaAudio) {
    window.genesisCinemaAudio = new GenesisCinemaAudioEngine();
  }
}

// Module export for Node.js / tests
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GenesisCinemaAudioEngine };
}
