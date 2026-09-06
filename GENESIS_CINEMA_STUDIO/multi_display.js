/**
 * 🖥️ GENESIS Cinema Studio: Zero-Install Multi-Display Synchronizer (multi_display.js - v55)
 * - W3C Standard BroadcastChannel API for 0.001s ultra-low latency sync across Quad Displays
 *   1. 🎬 Monitor 1: Main Director Cockpit & 5-Track Timeline NLE (index.html)
 *   2. 🍿 Monitor 2: 4K Screening Theater & Video Library (video_player.html)
 *   3. 👤 Monitor 3: Asset & Prop Studio (asset_studio.html)
 *   4. 📜 Monitor 4: Script & Storyboard Studio (storyboard_studio.html)
 */

class MultiDisplayEngine {
    constructor() {
        this.channelName = "genesis_cinema_studio_bus";
        this.channel = null;
        this.init();
    }

    init() {
        if (typeof BroadcastChannel !== 'undefined') {
            this.channel = new BroadcastChannel(this.channelName);
            this.channel.onmessage = (event) => this.handleMessage(event.data);
            console.log("🖥️ [MultiDisplay] BroadcastChannel Synchronizer Active v55");
        }
    }

    broadcast(type, payload) {
        if (this.channel) {
            this.channel.postMessage({ type, payload, timestamp: Date.now() });
        }
    }

    handleMessage(data) {
        if (!data || !data.type) return;

        switch (data.type) {
            case "ACTOR_SYNC":
                if (window.onMultiDisplayActorUpdate) window.onMultiDisplayActorUpdate(data.payload);
                break;
            case "CAST_ROSTER_SYNC":
                if (window.onMultiDisplayCastRosterUpdate) window.onMultiDisplayCastRosterUpdate(data.payload);
                break;
            case "VEHICLE_SYNC":
                if (window.onMultiDisplayVehicleUpdate) window.onMultiDisplayVehicleUpdate(data.payload);
                break;
            case "PROP_SYNC":
                if (window.onMultiDisplayPropUpdate) window.onMultiDisplayPropUpdate(data.payload);
                break;
            case "SCRIPT_SYNC":
                if (window.onMultiDisplayScriptUpdate) window.onMultiDisplayScriptUpdate(data.payload);
                break;
            case "TIMELINE_DLG_ADD":
                if (window.onMultiDisplayDialogueAdd) window.onMultiDisplayDialogueAdd(data.payload);
                break;
            case "SUBTITLE_SYNC":
                if (window.onMultiDisplaySubtitleUpdate) window.onMultiDisplaySubtitleUpdate(data.payload);
                break;
            case "VIDEO_RENDER_COMPLETE":
                if (window.onMultiDisplayVideoRendered) window.onMultiDisplayVideoRendered(data.payload);
                break;
            case "THEATER_PLAY_VIDEO":
                if (window.onMultiDisplayTheaterPlay) window.onMultiDisplayTheaterPlay(data.payload);
                break;
            case "TIMELINE_VIDEO_ADD":
                if (window.onMultiDisplayTimelineVideoAdd) window.onMultiDisplayTimelineVideoAdd(data.payload);
                break;
            case "AERIAL_FLIGHT_ADD":
                if (window.onMultiDisplayAerialFlightAdd) window.onMultiDisplayAerialFlightAdd(data.payload);
                break;
        }
    }

    async launchTripleMonitorCockpit() {
        return this.launchQuadMonitorCockpit();
    }

    async launchQuadMonitorCockpit() {
        console.log("🚀 [MultiDisplay] Launching Quad Display Cinema Cockpit (4 Screens)...");

        if ('getScreenDetails' in window) {
            try {
                const screenDetails = await window.getScreenDetails();
                const screens = screenDetails.screens;
                console.log(`🖥️ [Window Management API] Detected ${screens.length} physical displays.`);

                const s2 = screens[1] || screens[0];
                const s3 = screens[2] || screens[0];
                const s4 = screens[3] || screens[0];

                window.open('video_player.html', 'GENESIS_THEATER_WING', 
                    `left=${s2.availLeft},top=${s2.availTop},width=${s2.availWidth},height=${s2.availHeight}`);
                window.open('asset_studio.html', 'GENESIS_ASSET_WING', 
                    `left=${s3.availLeft},top=${s3.availTop},width=${s3.availWidth},height=${s3.availHeight}`);
                window.open('storyboard_studio.html', 'GENESIS_STORYBOARD_WING', 
                    `left=${s4.availLeft},top=${s4.availTop},width=${s4.availWidth},height=${s4.availHeight}`);
                
                return true;
            } catch(e) {
                console.warn("Screen Details fallback:", e);
            }
        }

        window.open('video_player.html', 'GENESIS_THEATER_WING', 'width=1100,height=720,left=100,top=50');
        window.open('asset_studio.html', 'GENESIS_ASSET_WING', 'width=1100,height=720,left=300,top=100');
        window.open('storyboard_studio.html', 'GENESIS_STORYBOARD_WING', 'width=1100,height=720,left=500,top=150');
        return true;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MultiDisplayEngine };
}
if (typeof window !== 'undefined') {
    window.MultiDisplayEngine = new MultiDisplayEngine();
}
console.log("🖥️ GENESIS Multi-Display Synchronizer v55 Loaded.");
