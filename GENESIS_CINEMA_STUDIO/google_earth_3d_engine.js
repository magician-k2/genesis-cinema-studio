/**
 * GENESIS Google Earth 3D & Street View Concourse Engine (google_earth_3d_engine.js - v45)
 * Comprehensive Metric Scaling: Human (1.68m-1.85m) ✕ Vehicle (1.75m-3.2m) ✕ Underground (2.8m) ✕ Towers (50m)
 */

class GoogleEarth3DEngine {
    constructor() {
        this.coords = { lat: 35.669921, lng: 139.702518 };
        this.fovDeg = 35.0;
        this.yawDeg = 180.0;
        this.tiltDeg = 90.0;
        this.cameraHeightM = 1.60;

        // Actor Dimensions & Framing
        this.actorHeightM = 1.80;
        this.actorZDistM = 3.50;
        this.currentFraming = "full"; // full, knee, bust, closeup

        this.showMetricBoxes = true;
        this.showHorizonLine = true;

        // Environments Setup
        this.environments = {
            harajuku_underground: {
                id: "harajuku_underground",
                name: "原宿・明治神宮前 地下コンコース (B1F)",
                coordsDisplay: "35.669921, 139.702518",
                category: "underground",
                depthM: -3.5,
                ceilingHeightM: 2.80,
                baseFov: 35.0,
                baseYaw: 180.0,
                baseTilt: 90.0,
                imageUrl: "assets/harajuku_underground.jpg",
                metricObjects: [
                    { name: "地下天井梁 (2.80m)", type: "ceiling", heightM: 2.80, widthM: 10.0, x: 400, y: 35, w: 200, h: 40, color: "#c084fc" },
                    { name: "耐震コンクリート柱 (2.80m)", type: "pillar", heightM: 2.80, widthM: 0.90, x: 210, y: 75, w: 85, h: 330, color: "#38bdf8" },
                    { name: "光沢タイル床面 (反射層)", type: "floor", heightM: 0.0, widthM: 12.0, x: 400, y: 405, w: 220, h: 45, color: "#10b981" }
                ]
            },
            shibuya_109_tele: {
                id: "shibuya_109_tele",
                name: "渋谷 109前 (Google Maps 15y 望遠 351.9h)",
                coordsDisplay: "35.6596286, 139.7005925",
                category: "surface",
                elevationM: 18.5,
                ceilingHeightM: 50.0,
                baseFov: 15.0,
                baseYaw: 351.9,
                baseTilt: 87.09,
                imageUrl: "assets/shibuya_109_telephoto.jpg",
                metricObjects: [
                    { name: "SHIBUYA 109 (円筒タワー)", type: "building", heightM: 50.0, widthM: 42.0, x: 400, y: 30, w: 180, h: 280, color: "#fde047" },
                    { name: "ジャパンタクシー (JPN TAXI)", type: "vehicle", heightM: 1.75, widthM: 1.70, lengthM: 4.40, x: 475, y: 325, w: 260, h: 140, color: "#38bdf8" },
                    { name: "横断歩道 通行人 (平均1.70m)", type: "pedestrian", heightM: 1.70, x: 865, y: 345, w: 75, h: 145, color: "#a855f7" }
                ]
            },
            nakano_sunmall: {
                id: "nakano_sunmall",
                name: "中野サンモール商店街 (アーケード 3D)",
                coordsDisplay: "35.7083894, 139.6656314",
                category: "arcade",
                ceilingHeightM: 9.20,
                elevationM: 42.0,
                baseFov: 45.0,
                baseYaw: 0.0,
                baseTilt: 88.8,
                imageUrl: "assets/nakano_sunmall.jpg",
                metricObjects: [
                    { name: "店舗1F入口 (SUIT SELECT)", type: "building", heightM: 3.5, widthM: 6.0, x: 260, y: 130, w: 180, h: 220, color: "#38bdf8" },
                    { name: "アーケード採光ガラス天井", type: "roof", heightM: 9.2, widthM: 12.0, x: 440, y: 25, w: 120, h: 80, color: "#fde047" }
                ]
            }
        };

        this.currentEnv = this.environments.harajuku_underground;
    }

    setEnvironment(envKey) {
        if (this.environments[envKey]) {
            this.currentEnv = this.environments[envKey];
            this.fovDeg = this.currentEnv.baseFov;
            this.yawDeg = this.currentEnv.baseYaw;
            this.tiltDeg = this.currentEnv.baseTilt;
        }
        return this.calculateTransform();
    }

    setShotFraming(framing) {
        this.currentFraming = framing;
        if (framing === "full") {
            this.actorZDistM = 4.0;
        } else if (framing === "knee") {
            this.actorZDistM = 3.2;
        } else if (framing === "bust") {
            this.actorZDistM = 2.4;
        } else if (framing === "closeup") {
            this.actorZDistM = 1.8;
        }
        return this.calculateTransform();
    }

    setActorHeight(h) {
        this.actorHeightM = parseFloat(h) || 1.80;
        return this.calculateTransform();
    }

    setFov(fov) {
        this.fovDeg = Math.max(10.0, Math.min(100.0, parseFloat(fov)));
        return this.calculateTransform();
    }

    setYaw(yaw) {
        this.yawDeg = (parseFloat(yaw) + 360) % 360;
        return this.calculateTransform();
    }

    setTilt(tilt) {
        this.tiltDeg = Math.max(45.0, Math.min(135.0, parseFloat(tilt)));
        return this.calculateTransform();
    }

    setActorZDistance(distM) {
        this.actorZDistM = Math.max(1.2, Math.min(25.0, parseFloat(distM)));
        return this.calculateTransform();
    }

    toggleMetricBoxes() {
        this.showMetricBoxes = !this.showMetricBoxes;
        return this.showMetricBoxes;
    }

    toggleHorizonLine() {
        this.showHorizonLine = !this.showHorizonLine;
        return this.showHorizonLine;
    }

    calculateTransform() {
        const zoomMultiplier = (60.0 / this.fovDeg);
        const yawShiftPercent = ((this.yawDeg % 360) / 360) * 100;
        const pitchDeltaDeg = (this.tiltDeg - 90.0);
        const pitchShiftPx = pitchDeltaDeg * 8.0;

        const distanceFactor = (3.5 / this.actorZDistM);
        const actorScale = Math.max(0.45, Math.min(2.2, distanceFactor * 0.95 * (this.actorHeightM / 1.80) * (zoomMultiplier * 0.65)));
        const actorBottomY = Math.max(15, Math.min(180, 30 + (distanceFactor - 1.0) * 20 - pitchShiftPx));

        return {
            actorZ: this.actorZDistM,
            fov: this.fovDeg.toFixed(1),
            yaw: this.yawDeg.toFixed(1),
            tilt: this.tiltDeg.toFixed(2),
            zoomMultiplier: zoomMultiplier.toFixed(1) + "x",
            lensEquivalentMm: (24.0 * zoomMultiplier).toFixed(0) + "mm",
            bgTransformCss: `scale(${Math.max(1.0, zoomMultiplier * 0.55)}) translate(0px, ${pitchShiftPx}px)`,
            bgPositionPercent: yawShiftPercent.toFixed(2),
            actorScaleCss: actorScale.toFixed(3),
            actorBottomY: actorBottomY.toFixed(0),
            ratioCeilingToActor: (this.currentEnv.ceilingHeightM / this.actorHeightM).toFixed(2)
        };
    }

    renderMetricOverlay(ctx, width, height) {
        ctx.save();
        ctx.clearRect(0, 0, width, height);

        // 1. Camera Eye-Level Horizon (1.60m)
        const horizonY = height * 0.50 + (90.0 - this.tiltDeg) * 8.0;

        if (this.showHorizonLine) {
            ctx.strokeStyle = "rgba(16, 185, 129, 0.85)";
            ctx.lineWidth = 1.5;
            ctx.setLineDash([8, 4]);
            ctx.beginPath();
            ctx.moveTo(0, horizonY);
            ctx.lineTo(width, horizonY);
            ctx.stroke();
            ctx.setLineDash([]);

            ctx.fillStyle = "#10b981";
            ctx.font = "bold 9px 'Fira Code', monospace";
            ctx.fillText(`── 🟢 カメラ水平線 (Eye-Level 1.60m / Tilt ${this.tiltDeg.toFixed(1)}°) ──`, 15, horizonY - 6);
        }

        // 2. Metric Bounding Boxes & Height Guides
        if (this.showMetricBoxes && this.currentEnv.metricObjects) {
            this.currentEnv.metricObjects.forEach(obj => {
                const ox = (obj.x / 800) * width;
                const oy = (obj.y / 450) * height;
                const ow = (obj.w / 800) * width;
                const oh = (obj.h / 450) * height;

                ctx.strokeStyle = obj.color;
                ctx.lineWidth = 1.5;
                ctx.strokeRect(ox, oy, ow, oh);

                // Dimension Tag
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(ox, oy - 16, 190, 15);
                ctx.fillStyle = obj.color;
                ctx.font = "bold 9px 'Noto Sans JP', sans-serif";
                ctx.fillText(`📐 ${obj.name}: ${obj.heightM}m`, ox + 4, oy - 4);
            });
        }

        ctx.restore();
    }
}

window.GoogleEarth3DEngine = new GoogleEarth3DEngine();
console.log("GENESIS Google Earth 3D Engine v45 Loaded.");
