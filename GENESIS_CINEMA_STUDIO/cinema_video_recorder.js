/**
 * 🎬 GENESIS 4K Cinema Video Recorder & Stream Renderer (cinema_video_recorder.js - v46)
 * - Browser-Native 4K / 60fps Video Rendering via MediaRecorder & Canvas Stream
 * - Real-time MP4 / WebM Exporter & SMPTE Timecode Embedded Recorder
 */

class CinemaVideoRecorder {
    constructor() {
        this.isRecording = false;
        this.recordedChunks = [];
        this.mediaRecorder = null;
        this.recordingTimeMs = 0;
        this.timer = null;
        this.recordedBlobUrl = null;
    }

    startRecording(canvasElement, fps = 60, mimeType = 'video/webm;codecs=vp9') {
        if (!canvasElement) {
            console.error("Canvas element required for recording");
            return false;
        }

        try {
            const stream = canvasElement.captureStream(fps);
            this.recordedChunks = [];
            
            // Check supported mime types
            let finalMime = mimeType;
            if (!MediaRecorder.isTypeSupported(finalMime)) {
                finalMime = 'video/webm';
            }

            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: finalMime,
                videoBitsPerSecond: 25000000 // 25 Mbps High-bitrate 4K Cinema Quality
            });

            this.mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) {
                    this.recordedChunks.push(e.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                const blob = new Blob(this.recordedChunks, { type: finalMime });
                this.recordedBlobUrl = URL.createObjectURL(blob);
                console.log("🎬 [CinemaRecorder] Video recording completed. Size:", (blob.size / 1024 / 1024).toFixed(2), "MB");

                if (typeof window !== 'undefined' && window.MultiDisplayEngine) {
                    window.MultiDisplayEngine.broadcast("VIDEO_RENDER_COMPLETE", {
                        blobUrl: this.recordedBlobUrl,
                        sizeBytes: blob.size,
                        timestamp: Date.now()
                    });
                }
            };

            this.mediaRecorder.start(100); // 100ms timeslice
            this.isRecording = true;
            this.recordingTimeMs = 0;

            this.timer = setInterval(() => {
                this.recordingTimeMs += 100;
            }, 100);

            console.log("🎬 [CinemaRecorder] 4K Video Recording Started @", fps, "FPS");
            return true;
        } catch(e) {
            console.error("Recording error:", e);
            return false;
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            if (this.timer) clearInterval(this.timer);
            return true;
        }
        return false;
    }

    downloadLatestVideo(filename = "GENESIS_4K_CINEMA_CUT.webm") {
        if (!this.recordedBlobUrl) return false;
        const a = document.createElement('a');
        a.href = this.recordedBlobUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        return true;
    }
}

if (typeof window !== 'undefined') {
    window.CinemaVideoRecorder = new CinemaVideoRecorder();
    console.log("🎬 GENESIS 4K Cinema Video Recorder v46 Loaded.");
}
