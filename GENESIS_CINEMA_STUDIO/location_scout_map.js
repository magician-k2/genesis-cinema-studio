/**
 * GENESIS Location Scout Map Engine (location_scout_map.js - v43)
 * Google Maps / Earth 連動 原宿・神宮前・地下街 実写ロケハンエンジン
 */

class LocationScoutMapEngine {
    constructor() {
        this.locations = {
            harajuku_underground: {
                id: "harajuku_underground",
                name: "原宿・明治神宮前 地下コンコース (B1F)",
                coordsDisplay: "35.669921, 139.702518",
                category: "underground",
                depthM: -3.5,
                ceilingHeightM: 2.80,
                mapX: 0.52,
                mapY: 0.70,
                color: "#c084fc",
                badge: "🚇 地下深度 -3.5m / 天井高 2.8m",
                description: "東京メトロ明治神宮前〈原宿〉駅 地下通路。光沢タイル床面反射と円柱群。"
            },
            harajuku_station_front: {
                id: "harajuku_station_front",
                name: "JR原宿駅 表参道口 (地上交差点)",
                coordsDisplay: "35.670215, 139.702840",
                category: "surface",
                depthM: 0.0,
                elevationM: 38.0,
                mapX: 0.55,
                mapY: 0.46,
                color: "#38bdf8",
                badge: "🌳 地上標高 38.0m / 表参道口",
                description: "JR原宿駅前。銀杏並木と明治神宮前交差点への地上接続ポイント。"
            },
            shibuya_109_tele: {
                id: "shibuya_109_tele",
                name: "渋谷 109前 (Google Maps 15y 望遠)",
                coordsDisplay: "35.6596286, 139.7005925",
                category: "surface",
                elevationM: 18.5,
                buildingHeightM: 50.0,
                mapX: 0.82,
                mapY: 0.58,
                color: "#fde047",
                badge: "🏢 109高 50m / 望遠 FOV 15°",
                description: "SHIBUYA 109前。超望遠圧縮効果によるタクシーと主役の緊迫感。"
            },
            nakano_sunmall: {
                id: "nakano_sunmall",
                name: "中野サンモール商店街 (アーケード)",
                coordsDisplay: "35.7083894, 139.6656314",
                category: "arcade",
                ceilingHeightM: 9.20,
                elevationM: 42.0,
                mapX: 0.22,
                mapY: 0.35,
                color: "#34d399",
                badge: "🏛️ アーケード天井 9.2m",
                description: "採光ガラスアーケード。全長224mの奥行きある商店街パースペクティブ。"
            }
        };

        this.selectedId = "harajuku_underground";
        this.mapImage = new Image();
        this.mapImage.src = "assets/google_maps_harajuku_scout.png";
        this.imageLoaded = false;
        this.mapImage.onload = () => {
            this.imageLoaded = true;
        };

        // Pulse Animation Counter
        this.animTick = 0;
        this.startPulseLoop();
    }

    startPulseLoop() {
        setInterval(() => {
            this.animTick = (this.animTick + 0.08) % (Math.PI * 2);
        }, 50);
    }

    selectPoint(id) {
        if (this.locations[id]) {
            this.selectedId = id;
        }
    }

    getSelectedPoint() {
        return this.locations[this.selectedId] || this.locations.harajuku_underground;
    }

    renderMapCanvas(ctx, width, height) {
        ctx.save();
        ctx.clearRect(0, 0, width, height);

        // 1. Draw Map Background Image or Stylized Grid Map
        if (this.imageLoaded && this.mapImage.width > 0) {
            ctx.drawImage(this.mapImage, 0, 0, width, height);
            
            // Subtle Dark Vignette & Tech Overlay
            const grad = ctx.createRadialGradient(width * 0.5, height * 0.5, width * 0.2, width * 0.5, height * 0.5, width * 0.7);
            grad.addColorStop(0, "rgba(4, 6, 12, 0.25)");
            grad.addColorStop(1, "rgba(4, 6, 12, 0.75)");
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, width, height);
        } else {
            // Fallback Vector Tech Map
            ctx.fillStyle = "#090e1a";
            ctx.fillRect(0, 0, width, height);

            // Grid Lines
            ctx.strokeStyle = "rgba(0, 242, 254, 0.08)";
            ctx.lineWidth = 1;
            for (let x = 0; x < width; x += 40) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();
            }
            for (let y = 0; y < height; y += 40) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }
        }

        // 2. Draw Subway / Scout Trajectory Route (青・紫の軌跡)
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        
        const ptUnderground = { x: width * 0.52, y: height * 0.70 };
        const ptStation = { x: width * 0.55, y: height * 0.46 };
        const ptShibuya = { x: width * 0.82, y: height * 0.58 };
        const ptNakano = { x: width * 0.22, y: height * 0.35 };

        // Underground Metro Concourse Path (Purple Glow)
        ctx.shadowColor = "#a855f7";
        ctx.shadowBlur = 15;
        ctx.strokeStyle = "rgba(168, 85, 247, 0.85)";
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(ptUnderground.x - 70, ptUnderground.y + 40);
        ctx.lineTo(ptUnderground.x, ptUnderground.y);
        ctx.lineTo(ptUnderground.x + 60, ptUnderground.y - 30);
        ctx.stroke();

        // Surface Connection Line (Cyan Glow)
        ctx.shadowColor = "#00f2fe";
        ctx.shadowBlur = 12;
        ctx.strokeStyle = "rgba(0, 242, 254, 0.75)";
        ctx.lineWidth = 4;
        ctx.setLineDash([8, 6]);
        ctx.beginPath();
        ctx.moveTo(ptUnderground.x, ptUnderground.y);
        ctx.lineTo(ptStation.x, ptStation.y);
        ctx.lineTo(ptShibuya.x, ptShibuya.y);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.shadowBlur = 0;

        // 3. Render Location Pins & Radar Waves
        Object.values(this.locations).forEach(loc => {
            const px = loc.mapX * width;
            const py = loc.mapY * height;
            const isSelected = (loc.id === this.selectedId);

            // Radar Pulse for Selected
            if (isSelected) {
                const pulseR = 14 + Math.sin(this.animTick) * 8;
                ctx.strokeStyle = loc.color;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(px, py, pulseR, 0, Math.PI * 2);
                ctx.stroke();

                ctx.fillStyle = loc.color + "33";
                ctx.fill();
            }

            // Pin Outer Ring
            ctx.fillStyle = isSelected ? loc.color : "rgba(15, 23, 42, 0.9)";
            ctx.strokeStyle = loc.color;
            ctx.lineWidth = isSelected ? 3 : 2;
            ctx.beginPath();
            ctx.arc(px, py, isSelected ? 9 : 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();

            // Inner Dot
            ctx.fillStyle = isSelected ? "#05070e" : loc.color;
            ctx.beginPath();
            ctx.arc(px, py, 3.5, 0, Math.PI * 2);
            ctx.fill();

            // Location Label Card
            const cardW = 190;
            const cardH = 34;
            const cardX = Math.min(width - cardW - 15, Math.max(15, px - cardW * 0.5));
            const cardY = (py < height * 0.5) ? py + 16 : py - cardH - 16;

            ctx.fillStyle = isSelected ? "rgba(10, 14, 26, 0.95)" : "rgba(15, 23, 42, 0.85)";
            ctx.strokeStyle = isSelected ? loc.color : "rgba(255, 255, 255, 0.15)";
            ctx.lineWidth = isSelected ? 1.5 : 1;
            ctx.fillRect(cardX, cardY, cardW, cardH);
            ctx.strokeRect(cardX, cardY, cardW, cardH);

            // Text
            ctx.fillStyle = isSelected ? loc.color : "#f8fafc";
            ctx.font = `bold ${isSelected ? "11px" : "10px"} 'Noto Sans JP', sans-serif`;
            ctx.fillText(loc.name, cardX + 8, cardY + 14);

            ctx.fillStyle = isSelected ? "#fde047" : "#94a3b8";
            ctx.font = "bold 9px 'Fira Code', monospace";
            ctx.fillText(loc.badge, cardX + 8, cardY + 28);
        });

        // 4. HUD Header & Scale Meter
        ctx.fillStyle = "rgba(4, 6, 12, 0.85)";
        ctx.fillRect(12, 12, 280, 52);
        ctx.strokeStyle = "rgba(0, 242, 254, 0.3)";
        ctx.strokeRect(12, 12, 280, 52);

        ctx.fillStyle = "#00f2fe";
        ctx.font = "bold 11px 'Outfit', sans-serif";
        ctx.fillText("GENESIS MAPS SCOUT ✕ HARAJUKU", 20, 28);

        const selLoc = this.getSelectedPoint();
        ctx.fillStyle = "#f8fafc";
        ctx.font = "10px 'Noto Sans JP', sans-serif";
        ctx.fillText(`選択中: ${selLoc.name}`, 20, 44);
        ctx.fillStyle = "#a855f7";
        ctx.font = "9px 'Fira Code', monospace";
        ctx.fillText(`座標: ${selLoc.coordsDisplay}`, 20, 57);

        ctx.restore();
    }
}

window.LocationScoutMapEngine = new LocationScoutMapEngine();
console.log("GENESIS Location Scout Map Engine v43 Loaded.");
