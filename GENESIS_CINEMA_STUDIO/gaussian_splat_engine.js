/**
 * GENESIS Gaussian Splatting & 3D Camera Engine (gaussian_splat_engine.js - v34)
 */

class GaussianSplatEngine {
    constructor() {
        this.cameraMode = "orbit_360"; // orbit_360, tracking_dolly, crane_descent
        this.cameraPos = { x: 0, y: 1.6, z: 0 };
        this.orbitAngleDeg = 0;
        this.orbitRadius = 6.0;
        this.orbitSpeed = 1.0;
        
        // 3DGS Environments using exact verified local assets
        this.environments = {
            shibuya_scramble: {
                id: "shibuya_scramble",
                name: "渋谷スクランブル交差点 (完全無人 3DGS)",
                buildingHeightMax: 230,
                pointColor: "#00f2fe",
                ambientLight: "#38bdf8",
                imageUrl: "assets/shibuya_3dgs.jpg"
            },
            death_star_hangar: {
                id: "death_star_hangar",
                name: "超巨大格納庫 (スターウォーズ級 3DGS)",
                buildingHeightMax: 60,
                pointColor: "#ef4444",
                ambientLight: "#f8fafc",
                imageUrl: "assets/deathstar_3dgs.jpg"
            },
            ikebukuro_alley_3dgs: {
                id: "ikebukuro_alley_3dgs",
                name: "池袋東口 路地裏 (3DGSボリューメトリック)",
                buildingHeightMax: 35,
                pointColor: "#f59e0b",
                ambientLight: "#fbbf24",
                imageUrl: "assets/ren_walk_master.jpg"
            }
        };

        this.currentEnv = this.environments.shibuya_scramble;
    }

    setEnvironment(envKey) {
        if (this.environments[envKey]) {
            this.currentEnv = this.environments[envKey];
        }
        return this.currentEnv;
    }

    setCameraMode(mode) {
        this.cameraMode = mode;
        if (mode === "orbit_360") {
            this.orbitAngleDeg = 0;
            this.cameraPos.y = 1.6;
        } else if (mode === "crane_descent") {
            this.cameraPos.y = 50.0;
        } else if (mode === "tracking_dolly") {
            this.cameraPos.y = 1.6;
        }
        return this.getCameraTransform();
    }

    updateCameraPath(stepDelta = 1.0) {
        if (this.cameraMode === "orbit_360") {
            this.orbitAngleDeg = (this.orbitAngleDeg + stepDelta * this.orbitSpeed) % 360;
            const rad = (this.orbitAngleDeg * Math.PI) / 180;
            this.cameraPos.x = Math.sin(rad) * this.orbitRadius;
            this.cameraPos.z = Math.cos(rad) * this.orbitRadius;
            this.cameraPos.y = 1.6 + Math.sin(rad * 2) * 0.3;
        } else if (this.cameraMode === "crane_descent") {
            this.cameraPos.y = Math.max(0.2, this.cameraPos.y - stepDelta * 0.8);
        } else if (this.cameraMode === "tracking_dolly") {
            this.cameraPos.z += stepDelta * 0.05;
        }

        return this.getCameraTransform();
    }

    getCameraTransform() {
        const rad = (this.orbitAngleDeg * Math.PI) / 180;
        // Continuous horizontal panoramic scrolling
        const bgShiftX = (this.orbitAngleDeg / 360) * 100;
        
        const pitchDeg = (this.cameraPos.y > 10) ? -20 : (this.cameraPos.y <= 0.4 ? 12 : 0);
        const parallaxFactor = (this.cameraPos.y / 50.0);

        return {
            mode: this.cameraMode,
            angleDeg: this.orbitAngleDeg.toFixed(1),
            cameraHeight: this.cameraPos.y.toFixed(2),
            bgPositionPercent: bgShiftX.toFixed(2),
            bgTransformCss: `scale(${1.15 + parallaxFactor * 0.15}) translateY(${(this.cameraPos.y - 1.6) * 2.0}px)`,
            actorScale: Math.max(0.4, Math.min(1.4, 1.0 - (this.cameraPos.y - 1.6) * 0.015)),
            pitchDeg: pitchDeg,
            buildingCastShadowOffset: {
                x: Math.cos(rad) * 30,
                y: Math.sin(rad) * 15
            }
        };
    }
}

window.GaussianSplatEngine = new GaussianSplatEngine();
console.log("GENESIS Gaussian Splat Engine v34 Loaded.");
