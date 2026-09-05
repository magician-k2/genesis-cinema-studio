/**
 * 👥 GENESIS Crowd Army & Extra Pedestrian Engine (crowd_army_engine.js - v45)
 * Dynamic Extra Generation: Pedestrian Density, Z-Depth Scattering, Type & Motion Blur
 */

class CrowdArmyEngine {
    constructor() {
        this.crowdCount = 0; // 0, 3, 10, 25, etc.
        this.crowdType = "subway_commuter"; // subway_commuter, urban_youth, business_rush, mixed
        this.depthScattering = "natural"; // natural, foreground_only, background_dense
        this.spriteUrl = "assets/extra_pedestrian.png";
        
        this.crowdTypes = {
            subway_commuter: {
                nameJa: "🚇 地下鉄利用客・通勤者",
                nameEn: "Tokyo subway commuters in dark overcoats and tailored business attire, walking with purposeful pace",
                descJa: "暗色コートやスーツの通勤者。奥の通路を整然と歩行。"
            },
            urban_youth: {
                nameJa: "🛍️ 原宿・渋谷 若者＆観光客",
                nameEn: "stylish urban pedestrians and shoppers wearing contemporary streetwear and casual jackets, carrying shopping bags",
                descJa: "ストリートウェアを着た若者やショッピング客。自然な会話と歩行。"
            },
            business_rush: {
                nameJa: "🏢 ビジネス街 ラッシュ群衆",
                nameEn: "dense crowd of rushing office workers with briefcases, creating authentic urban hustle motion blur",
                descJa: "ブリーフケースを持ったビジネスマンの群衆。速足のモーションブラー。"
            },
            mixed: {
                nameJa: "👥 ミックス都市群衆",
                nameEn: "diverse mix of Tokyo city pedestrians, evening commuters, and passersby blurred in the background",
                descJa: "多様な通行人や帰宅客の自然な群衆。"
            }
        };

        // Pre-computed Scatter Positions for Consistent Viewport Rendering
        this.cachedPedestrians = this.generateScatterList(30);
    }

    generateScatterList(maxCount) {
        const list = [];
        for (let i = 0; i < maxCount; i++) {
            // Z depth between 3.8m and 18.0m
            const z = 3.8 + Math.pow((i / maxCount), 1.4) * 14.0;
            // X position spread across the screen (-35% to +35% from center, avoiding exact center actor spot)
            const side = (i % 2 === 0) ? 1 : -1;
            const xPercent = 50 + side * (12 + (i * 7) % 36);
            const scale = Math.max(0.18, Math.min(0.85, 3.5 / z));
            const opacity = Math.max(0.35, Math.min(0.95, 1.0 - (z - 4.0) * 0.04));
            const blurPx = (z > 7.0) ? Math.min(4.0, (z - 7.0) * 0.4) : 0;
            const walkDir = (i % 3 === 0) ? "away" : "towards";

            list.push({
                id: i,
                xPercent: xPercent,
                zDistM: z,
                scale: scale,
                opacity: opacity,
                blurPx: blurPx,
                walkDir: walkDir
            });
        }
        return list;
    }

    setCrowdCount(count) {
        this.crowdCount = Math.max(0, Math.min(50, parseInt(count)));
        return this.getCrowdStatus();
    }

    setCrowdType(typeKey) {
        if (this.crowdTypes[typeKey]) {
            this.crowdType = typeKey;
        }
        return this.getCrowdStatus();
    }

    getCrowdStatus() {
        return {
            count: this.crowdCount,
            typeKey: this.crowdType,
            type: this.crowdTypes[this.crowdType],
            visiblePedestrians: this.cachedPedestrians.slice(0, this.crowdCount)
        };
    }

    generatePromptDescription() {
        if (this.crowdCount === 0) {
            return "Environment Atmosphere: Eerily vacant and deserted atmosphere with zero bystanders, creating hyper-isolated suspense tension.";
        }

        const typeInfo = this.crowdTypes[this.crowdType] || this.crowdTypes.subway_commuter;
        let densityDesc = "a sparse scattering of 2-3 distant pedestrians";
        if (this.crowdCount >= 20) densityDesc = `a dense atmospheric crowd of ${this.crowdCount} pedestrians with natural cinematic motion blur in the depth of field`;
        else if (this.crowdCount >= 8) densityDesc = `a moderate group of ${this.crowdCount} authentic background pedestrians walking at varied depths`;
        else if (this.crowdCount >= 3) densityDesc = `a few (${this.crowdCount}) subtle background commuters moving along the perimeter`;

        return `Crowd & Extras: ${densityDesc} (${typeInfo.nameEn}), maintaining clear visual hierarchy with the primary subject sharply isolated in the focal plane.`;
    }
}

window.CrowdArmyEngine = new CrowdArmyEngine();
console.log("GENESIS Crowd Army Engine v45 Loaded.");
