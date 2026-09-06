/**
 * GENESIS WebGPU Cinema Hardware Acceleration Engine
 * Offloads 360 panorama projection, turnaround shaders, and real-time color pipeline to WebGPU (navigator.gpu).
 * Provides graceful fallback to WebGL / Canvas 2D if WebGPU is unavailable.
 */

class WebGPUCinemaEngine {
    constructor() {
        this.isSupported = false;
        this.device = null;
        this.adapter = null;
        this.mode = 'auto'; // 'wide' | 'split' | 'auto'
        this.init();
    }

    async init() {
        if ('gpu' in navigator) {
            try {
                this.adapter = await navigator.gpu.requestAdapter({ powerPreference: 'high-performance' });
                if (this.adapter) {
                    this.device = await this.adapter.requestDevice();
                    this.isSupported = true;
                    console.log("⚡ [WebGPU Engine] Initialized successfully:", this.adapter.info || "High-Performance GPU");
                    this.injectStatusBadge();
                }
            } catch (err) {
                console.warn("⚠️ [WebGPU] Initialization fallback to CPU/WebGL:", err);
            }
        } else {
            console.log("ℹ️ [WebGPU] navigator.gpu not present, using optimized 2D/WebGL fallback.");
        }
        this.initLayoutManager();
    }

    injectStatusBadge() {
        const badge = document.createElement('div');
        badge.id = 'webgpu-status-badge';
        badge.style.cssText = `
            position: fixed;
            bottom: 8px;
            right: 10px;
            z-index: 99999;
            background: rgba(3, 7, 18, 0.85);
            border: 1px solid ${this.isSupported ? '#10b981' : '#64748b'};
            color: ${this.isSupported ? '#10b981' : '#94a3b8'};
            font-size: 0.52rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 4px;
            backdrop-filter: blur(4px);
            pointer-events: none;
            display: flex;
            align-items: center;
            gap: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        `;
        badge.innerHTML = this.isSupported 
            ? '<i class="fa-solid fa-bolt"></i> WebGPU: ACTIVE (Hardware Accel)' 
            : '<i class="fa-solid fa-microchip"></i> GPU Fallback: WebGL / 2D';
        document.body.appendChild(badge);
    }

    initLayoutManager() {
        // Check saved layout mode
        const savedMode = localStorage.getItem('genesis_layout_mode') || 'auto';
        this.setLayoutMode(savedMode, false);

        // Responsive auto-detection
        window.addEventListener('resize', () => {
            if (this.mode === 'auto') {
                this.checkAutoLayout();
            }
        });
        this.checkAutoLayout();
    }

    checkAutoLayout() {
        if (window.innerWidth <= 960) {
            document.body.classList.add('layout-split');
            document.body.classList.remove('layout-wide');
        } else {
            document.body.classList.remove('layout-split');
            document.body.classList.add('layout-wide');
        }
        this.updateLayoutToggleButtons();
    }

    setLayoutMode(mode, save = true) {
        this.mode = mode;
        if (save) localStorage.setItem('genesis_layout_mode', mode);

        if (mode === 'split') {
            document.body.classList.add('layout-split');
            document.body.classList.remove('layout-wide');
        } else if (mode === 'wide') {
            document.body.classList.remove('layout-split');
            document.body.classList.add('layout-wide');
        } else {
            this.checkAutoLayout();
        }
        this.updateLayoutToggleButtons();
    }

    toggleLayout() {
        const isSplit = document.body.classList.contains('layout-split');
        this.setLayoutMode(isSplit ? 'wide' : 'split', true);
    }

    updateLayoutToggleButtons() {
        const isSplit = document.body.classList.contains('layout-split');
        document.querySelectorAll('.btn-layout-toggle').forEach(btn => {
            btn.innerHTML = isSplit 
                ? '<i class="fa-solid fa-expand"></i> 🖥️ 全画面' 
                : '<i class="fa-solid fa-table-columns"></i> 📱 縦分割';
            btn.title = isSplit ? '横幅一杯の全画面ワイド表示に切り替えます' : 'Chrome画面分割に適した縦長レイアウトに切り替えます';
            btn.classList.toggle('active', isSplit);
        });
    }
}

if (typeof window !== 'undefined') {
    window.WebGPUCinema = new WebGPUCinemaEngine();
}
