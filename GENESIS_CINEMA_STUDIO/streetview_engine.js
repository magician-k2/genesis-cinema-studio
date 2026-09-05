/**
 * 🗺️ GENESIS Cinema Studio: 360-Degree Spherical & Elevation Physics Engine (Dynamic Slope Incline & Height)
 */
class StreetViewEngine {
    constructor() {
        this.cameraHeight = 0.2; // 0.1m - 5.0m
        this.cameraFov = 50;     // 24mm(84°), 35mm(63°), 50mm(47°), 85mm(28°)
        this.heading = 325.77;   // 0° - 360°
        this.pitch = 0;          // -30° to +30°
        this.slopeAngle = 0;     // -15° to +15° (Elevation incline)
        this.weatherMode = "raw";

        this.locations = {
            "ikebukuro_alley": {
                name: "池袋 東口繁華街の路地裏 (実写ストリートビュー)",
                coords: "35.72794, 139.7176752",
                heading: 325.77,
                pitch: 89.86,
                imageUrl: "assets/ikebukuro_real_clean.jpg",
                groundTexture: "舗装アスファルト道路 (高低差: 平坦)",
                elevationSlope: 0
            },
            "kyoto_gion": {
                name: "京都祇園 白川通り (実写・石畳セット)",
                coords: "35.0037, 135.7772",
                heading: 180.0,
                pitch: 88.0,
                imageUrl: "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1600&auto=format&fit=crop",
                groundTexture: "濡れた伝統石畳 (高低差: 緩やかな坂道 3°)",
                elevationSlope: 3
            },
            "tokyo_shibuya": {
                name: "東京 渋谷横丁 (ネオン路地)",
                coords: "35.6595, 139.7005",
                heading: 90.0,
                pitch: 90.0,
                imageUrl: "https://images.unsplash.com/photo-1542051841857-5f90071e7989?q=80&w=1600&auto=format&fit=crop",
                groundTexture: "湿ったアスファルト＆ネオン反射",
                elevationSlope: 0
            }
        };

        this.currentLocationKey = "ikebukuro_alley";
    }

    getLocation(key) {
        return this.locations[key] || this.locations["ikebukuro_alley"];
    }

    setCameraHeight(h) {
        const parsedH = parseFloat(h);
        this.cameraHeight = isNaN(parsedH) ? 1.6 : Math.max(0.1, Math.min(5.0, parsedH));
        return this.calculatePhysicsTransform();
    }

    setElevationSlope(slope) {
        const parsedSlope = parseFloat(slope);
        this.slopeAngle = isNaN(parsedSlope) ? 0 : Math.max(-15, Math.min(15, parsedSlope));
        return this.calculatePhysicsTransform();
    }

    setWeatherMode(mode) {
        this.weatherMode = mode;
        return this.weatherMode;
    }

    calculatePhysicsTransform() {
        const heightNorm = (this.cameraHeight - 1.6) / 2.4; 
        // Background shifts vertically with BOTH camera height and road slope incline!
        const bgTranslateY = (heightNorm * 55) - (this.slopeAngle * 3.2);
        const bgScale = 1.10 + Math.abs(heightNorm) * 0.12 + Math.abs(this.slopeAngle) * 0.01;
        const bgRotateZ = (this.slopeAngle * 0.35); // Subtle authentic incline tilt

        // Ground pitch + elevation slope incline
        const groundPitchDeg = Math.max(5, Math.min(85, 30 + (this.cameraHeight * 12) + (this.slopeAngle * 1.8)));
        const groundOpacity = Math.max(0.15, Math.min(0.95, 0.25 + (this.cameraHeight * 0.12) + (Math.abs(this.slopeAngle) * 0.02)));

        const actorTranslateY = ((1.6 - this.cameraHeight) * 38) + (this.slopeAngle * 1.5);
        const actorScale = (50 / (this.cameraFov || 50)) * (1 + (1.6 - this.cameraHeight) * 0.16);

        let shotType = "👀 目線ショット (1.6m)";
        if (this.cameraHeight <= 0.3) shotType = "🥾 超ローアングル・地面靴 (0.2m)";
        else if (this.cameraHeight <= 0.9) shotType = "📐 ローアングル・あおり (0.8m)";
        else if (this.cameraHeight >= 3.0) shotType = "🏗️ クレーン・俯瞰 (3.5m)";

        let lensType = "50mm 標準シネマ";
        if (this.cameraFov <= 35) lensType = "35mm 広角シネマ";
        else if (this.cameraFov >= 70) lensType = "85mm 望遠ポートレート";

        return {
            height: this.cameraHeight.toFixed(1),
            fov: this.cameraFov,
            heading: this.heading.toFixed(1),
            pitch: this.pitch.toFixed(1),
            slope: this.slopeAngle,
            shotType: shotType,
            lensType: lensType,
            bgTransformCss: `translateY(${bgTranslateY.toFixed(1)}px) scale(${bgScale.toFixed(2)}) rotate(${bgRotateZ.toFixed(2)}deg)`,
            actorTransformCss: `translateY(${actorTranslateY.toFixed(1)}px) scale(${actorScale.toFixed(2)})`,
            groundPitch: `${groundPitchDeg.toFixed(1)}deg`,
            groundOpacity: groundOpacity.toFixed(2)
        };
    }
}

window.StreetViewEngine = new StreetViewEngine();
