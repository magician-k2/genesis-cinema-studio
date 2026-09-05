/**
 * 🎙️ GENESIS Cinema Studio: Multi-Track Audio & On-Demand SE/BGM Engine
 */
class AudioStudioEngine {
    constructor() {
        this.audioCtx = null;
        this.isPlaying = false;
        this.currentAudio = null;
        this.bgmOscillators = [];
        this.bgmGain = null;
        this.sfxGain = null;
        this.voicevoxSpeakerId = 13; // 青山龍星 (渋い映画主人公イケボ)
    }

    init() {
        if (!this.audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioCtx = new AudioContext();

            const comp = this.audioCtx.createDynamicsCompressor();
            comp.threshold.setValueAtTime(-16, this.audioCtx.currentTime);
            comp.knee.setValueAtTime(20, this.audioCtx.currentTime);
            comp.ratio.setValueAtTime(3.5, this.audioCtx.currentTime);
            comp.connect(this.audioCtx.destination);

            this.bgmGain = this.audioCtx.createGain();
            this.bgmGain.gain.setValueAtTime(0.18, this.audioCtx.currentTime);
            this.bgmGain.connect(comp);

            this.sfxGain = this.audioCtx.createGain();
            this.sfxGain.gain.setValueAtTime(0.35, this.audioCtx.currentTime);
            this.sfxGain.connect(comp);
        }
        if (this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }
    }

    // On-Demand Procedural Siren / Rain / Footstep Generator
    playSFX(type) {
        this.init();
        const now = this.audioCtx.currentTime;

        if (type === "siren") {
            // Distant Police Siren
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(650, now);
            osc.frequency.linearRampToValueAtTime(900, now + 0.6);
            osc.frequency.linearRampToValueAtTime(650, now + 1.2);

            gain.gain.setValueAtTime(0.15, now);
            gain.gain.linearRampToValueAtTime(0.01, now + 1.8);

            osc.connect(gain);
            gain.connect(this.sfxGain);

            osc.start(now);
            osc.stop(now + 1.8);
        } else if (type === "rain") {
            // White noise rain drop
            const bufferSize = this.audioCtx.sampleRate * 2;
            const buffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            const noise = this.audioCtx.createBufferSource();
            noise.buffer = buffer;
            const filter = this.audioCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(1000, now);

            const gain = this.audioCtx.createGain();
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.linearRampToValueAtTime(0.01, now + 2.0);

            noise.connect(filter);
            filter.connect(gain);
            gain.connect(this.sfxGain);

            noise.start(now);
            noise.stop(now + 2.0);
        } else {
            this.playFootstep();
        }
    }

    async playDialogue(text) {
        this.init();
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }

        try {
            const encodedText = encodeURIComponent(text);
            const apiUrl = `https://api.tts.quest/v3/voicevox/synthesis?text=${encodedText}&speaker=${this.voicevoxSpeakerId}`;
            const res = await fetch(apiUrl);
            if (res.ok) {
                const data = await res.json();
                if (data.mp3DownloadUrl || data.wavDownloadUrl) {
                    const audioUrl = data.mp3DownloadUrl || data.wavDownloadUrl;
                    const audio = new Audio(audioUrl);
                    this.currentAudio = audio;
                    audio.volume = 1.0;
                    audio.play();
                    return;
                }
            }
        } catch (e) {}

        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            const voices = window.speechSynthesis.getVoices();
            const naturalVoice = voices.find(v => v.lang.includes('ja') && (v.name.includes('Natural') || v.name.includes('Neural') || v.name.includes('Google'))) || voices.find(v => v.lang.startsWith('ja'));
            if (naturalVoice) utter.voice = naturalVoice;
            utter.lang = 'ja-JP';
            utter.rate = 0.95;
            utter.pitch = 0.90;
            window.speechSynthesis.speak(utter);
        }
    }

    playFootstep() {
        this.init();
        if (!this.audioCtx) return;
        const now = this.audioCtx.currentTime;

        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(110, now);
        osc.frequency.exponentialRampToValueAtTime(25, now + 0.08);

        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

        osc.connect(gain);
        gain.connect(this.sfxGain);

        osc.start(now);
        osc.stop(now + 0.08);
    }

    startCinematicBGM() {
        this.init();
        this.stopCinematicBGM();

        const chordFreqs = [65.41, 98.00, 155.56, 196.00, 261.63];
        const now = this.audioCtx.currentTime;

        chordFreqs.forEach((freq, idx) => {
            const osc = this.audioCtx.createOscillator();
            const filter = this.audioCtx.createBiquadFilter();
            const gain = this.audioCtx.createGain();

            osc.type = idx % 2 === 0 ? 'sawtooth' : 'sine';
            osc.frequency.setValueAtTime(freq, now);

            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(360 + (idx * 40), now);
            filter.Q.setValueAtTime(1.8, now);

            gain.gain.setValueAtTime(0.001, now);
            gain.gain.exponentialRampToValueAtTime(0.11, now + 1.0);

            osc.connect(filter);
            filter.connect(gain);
            gain.connect(this.bgmGain);

            osc.start(now);
            this.bgmOscillators.push(osc);
        });

        this.isPlaying = true;
    }

    stopCinematicBGM() {
        this.bgmOscillators.forEach(osc => {
            try { osc.stop(); } catch (e) {}
        });
        this.bgmOscillators = [];
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        this.isPlaying = false;
    }

    togglePlayback() {
        this.init();
        if (this.isPlaying) {
            this.stopCinematicBGM();
            return false;
        } else {
            this.startCinematicBGM();
            setTimeout(() => {
                this.playDialogue("池袋東口、目標ポイントに到達。周囲の通行人・車両はすべて消去完了。これよりメインショットの収録を開始する。");
            }, 500);

            let count = 0;
            const interval = setInterval(() => {
                if (!this.isPlaying || count > 8) {
                    clearInterval(interval);
                    return;
                }
                this.playFootstep();
                count++;
            }, 580);

            return true;
        }
    }
}

window.AudioStudioEngine = new AudioStudioEngine();
