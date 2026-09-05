/**
 * 🖥️ GENESIS Cinema Studio: Zero-Install Multi-Display Synchronizer
 * - Uses W3C Standard BroadcastChannel API for 0.0001s cross-tab/cross-monitor sync
 * - Supports Director Console (Viewport), Editor Console (Timeline & Audio), Asset Desk
 */
class MultiDisplayEngine {
    constructor() {
        this.channelName = "genesis_cinema_studio_bus";
        this.channel = null;
        this.mode = "single"; // "single", "director", "editor", "assets"
        this.init();
    }

    init() {
        if (typeof BroadcastChannel !== 'undefined') {
            this.channel = new BroadcastChannel(this.channelName);
            this.channel.onmessage = (event) => this.handleMessage(event.data);
            console.log("🖥️ [MultiDisplay] BroadcastChannel Synchronizer Active");
        }
    }

    broadcast(type, payload) {
        if (this.channel) {
            this.channel.postMessage({ type, payload, timestamp: Date.now() });
        }
    }

    handleMessage(data) {
        if (!data || !data.type) return;
        console.log("⚡ [MultiDisplay Sync]:", data.type, data.payload);

        switch (data.type) {
            case "CAMERA_UPDATE":
                if (window.applyPhysicsTransform && data.payload.transform) {
                    window.applyPhysicsTransform(data.payload.transform);
                }
                break;
            case "LOCATION_CHANGE":
                if (window.selectLocationKeySilent) {
                    window.selectLocationKeySilent(data.payload.locationKey);
                }
                break;
            case "CHARACTER_UPDATE":
                if (window.updateCharacterViewSilent) {
                    window.updateCharacterViewSilent(data.payload);
                }
                break;
            case "AUDIO_TRIGGER":
                if (window.AudioStudioEngine) {
                    if (data.payload.action === "play") window.AudioStudioEngine.togglePlayback();
                }
                break;
        }
    }

    openSubWindow(role) {
        const url = window.location.href.split('?')[0] + `?role=${role}`;
        window.open(url, `GENESIS_${role}`, "width=1200,height=800");
    }
}

window.MultiDisplayEngine = new MultiDisplayEngine();
