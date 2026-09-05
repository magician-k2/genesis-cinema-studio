/**
 * 🎬 GENESIS AI Video Prompt & Spatial Guidance Engine (prompt_director_engine.js - v52)
 * - Google DeepMind Veo 3.1 & 2 4K Native Geometry-Constrained Master Synthesizer
 * - Multi-Node Dolly Sequence & Continuous Road Navigation Synthesis
 * - 7 Time-of-Day Lighting Profiles ✕ 6 Cinematic Weather Atmospheres
 * - Full Integration: Character Details ✕ Large Stage Props ✕ Small Handheld Props
 */

class PromptDirectorEngine {
    constructor() {
        this.currentTech = "tracking_dolly";
        this.currentTimeOfDay = "sunset"; // sunrise, morning, noon, late_afternoon, sunset, night, twilight
        this.currentWeather = "clear";   // clear, overcast, heavy_rain, wind_storm, thunderstorm, dense_fog

        this.timeOfDayPresets = {
            sunrise: {
                nameJa: "🌅 朝焼け (Sunrise / Early Dawn)",
                kelvin: 3800,
                promptEn: "early morning sunrise golden-rose light rays casting long dramatic soft shadows, horizontal sun angle, soft ambient dawn mist",
                descJa: "水平線からのオレンジ・ピンクの朝焼け光。長い斜光影と朝の澄んだ空気感。"
            },
            morning: {
                nameJa: "☀️ 朝 (Crisp Morning)",
                kelvin: 5200,
                promptEn: "crisp bright morning directional sunlight, clean high-contrast shadows, fresh daylight atmosphere",
                descJa: "爽やかな朝のクリアな自然光。シャープなコントラストと街並みの鮮明なディテール。"
            },
            noon: {
                nameJa: "🌤️ 昼 (Direct Midday Sun)",
                kelvin: 6000,
                promptEn: "bright midday sunlight directly overhead, neutral color temperature, short grounded shadows, vivid natural saturation",
                descJa: "真上の太陽光による均一な昼間光。最短の地面影と高解像度リアリズム。"
            },
            late_afternoon: {
                nameJa: "🌇 夕方 (Late Afternoon Golden Light)",
                kelvin: 4500,
                promptEn: "late afternoon warm amber sunlight glancing across buildings, lengthening shadows, warm cinematic rim glow",
                descJa: "傾いた琥珀色の夕方斜光。建物の立体感を引き立てる美しいサイドリムライト。"
            },
            sunset: {
                nameJa: "🌆 夕焼け (Dramatic Golden Sunset)",
                kelvin: 3000,
                promptEn: "dramatic golden sunset with fiery orange and magenta sky gradient, intense golden hour lens flare, rich silhouette rim illumination",
                descJa: "燃えるような夕焼け空。ドラマティックなゴールデンアワーの逆光リムライトとシネマレンズフレア。"
            },
            night: {
                nameJa: "🌙 夜 (Cinematic Neo-Tokyo Night)",
                kelvin: 3200,
                promptEn: "cinematic dark night atmosphere, high-contrast urban practical lighting, glowing streetlamps, vibrant neon reflections in shadows",
                descJa: "漆黒の夜景に浮かぶ街灯とネオンの反射光。映画的な深い陰影とハイコントラスト。"
            },
            twilight: {
                nameJa: "🌌 夜明け / 薄明 (Blue Hour Twilight)",
                kelvin: 7500,
                promptEn: "blue hour twilight, deep sapphire blue sky, soft ethereal diffused ambient illumination, subtle pre-dawn serenity",
                descJa: "日没直後・日の出前のブルーアワー。サファイアブルーの天空光による神秘的で静謐な空気感。"
            }
        };

        this.weatherPresets = {
            clear: {
                nameJa: "☀️ 快晴 (Crystal Clear Sky)",
                promptEn: "crystal clear optical atmosphere, pristine air clarity with razor-sharp architectural horizons",
                descJa: "澄み渡る大気とクッキリとした視界。"
            },
            overcast: {
                nameJa: "☁️ 曇天・薄曇り (Overcast Diffused)",
                promptEn: "soft overcast cloudy sky, diffused shadowless ambient lighting, cinematic muted color palette",
                descJa: "雲に覆われた均一な拡散光。やわらかな陰影と映画的なトーン。"
            },
            heavy_rain: {
                nameJa: "🌧️ 大雨・路面反射 (Heavy Rain Storm)",
                promptEn: "heavy torrential rain streaks slicing through the air, glistening wet reflective asphalt road mirroring street illumination, splashing water droplets on ground",
                descJa: "雨粒の軌跡と濡れたアスファルトの鏡面反射。水たまりに映り込む光彩。"
            },
            wind_storm: {
                nameJa: "💨 強風・砂塵 (Dynamic Wind Storm)",
                promptEn: "strong gusting wind atmosphere, character trench coat and hair fluttering dynamically, airborne atmospheric micro-particles, dynamic motion turbulence",
                descJa: "風になびくコートと髪。大気を舞う微粒子が生み出す臨場感と躍動感。"
            },
            thunderstorm: {
                nameJa: "⚡ 雷雨・稲光 (Thunderstorm & Lightning)",
                promptEn: "dark ominous storm clouds, heavy deluge with sudden intense lightning flashes dramatically illuminating the entire scene with stark electric blue highlights",
                descJa: "暗雲を割る強烈な稲光。青白い閃光が一瞬で周囲を劇的に照らし出す緊迫シーン。"
            },
            dense_fog: {
                nameJa: "🌫️ 濃霧・朝靄 (Dense Volumetric Fog)",
                promptEn: "dense cinematic volumetric fog and atmospheric mist, dramatic volumetric light rays filtering through moisture, deep atmospheric z-depth falloff",
                descJa: "立ち込める濃霧と光条（ゴッドレイ）。奥行きを強調する幻想的な大気表現。"
            }
        };

        this.techSpecs = {
            turn_out: {
                nameJa: "🔄 ターンアウト (180° 急旋回・人物対比リビール)",
                promptEn: "fast-paced cinematic 180-degree turn-out camera rotation, whipping smoothly around the character to reveal the surrounding environment and background perspective",
                descJa: "カメラが演者正面から背後へ180度急旋回。主役の表情から周囲の空間・エキストラ・背景へとダイナミックに展開。"
            },
            close_up: {
                nameJa: "🎥 アップ (顔・目線・緊迫表情クローズ)",
                promptEn: "intense cinematic close-up shot focused on character sharp intense eyes and facial nuances, atmospheric rim lighting with shallow depth of field",
                descJa: "演者の鋭い目線と決意の表情にフォーカス。背景の群衆や車両を美しくボケさせて主役を際立たせる。"
            },
            crane_boom: {
                nameJa: "🏗️ クレーン降下 (高所スラブから演者目線へ下降)",
                promptEn: "smooth vertical crane boom down from the high architectural ceiling overhead down to 1.60m eye-level subject framing",
                descJa: "天井高や構造物の高所からカメラが垂直下降し、演者の目線（1.6m）へ滑らかに着地。"
            },
            tracking_dolly: {
                nameJa: "🎥 追従ドリー (ステディカム前方ウォーキング)",
                promptEn: "low-angle smooth tracking dolly moving steadily in front of the walking subject, maintaining grounded proportions and cinematic pacing along the road vector",
                descJa: "前進する演者を正面から一定距離で捉え続ける追従ドリー。足元の床面反射と堂々たる歩行。"
            }
        };
    }

    setTimeOfDay(timeKey) {
        if (this.timeOfDayPresets[timeKey]) {
            this.currentTimeOfDay = timeKey;
        }
        return this.timeOfDayPresets[this.currentTimeOfDay];
    }

    setWeather(weatherKey) {
        if (this.weatherPresets[weatherKey]) {
            this.currentWeather = weatherKey;
        }
        return this.weatherPresets[this.currentWeather];
    }

    setCameraTechnique(tech) {
        if (this.techSpecs[tech]) {
            this.currentTech = tech;
        }
        return this.techSpecs[this.currentTech];
    }

    generatePrompt(params = {}) {
        const tech = this.techSpecs[this.currentTech] || this.techSpecs.tracking_dolly;
        const tod = this.timeOfDayPresets[this.currentTimeOfDay] || this.timeOfDayPresets.sunset;
        const weather = this.weatherPresets[this.currentWeather] || this.weatherPresets.clear;

        const locName = params.locationName || "Harajuku Street";
        const coords = params.coords || "35.71110, 139.79630";
        const mapsUrl = params.mapsUrl || `https://www.google.com/maps/@${coords},3a,75y,180h,90t`;
        const yaw = parseFloat(params.yaw || 180).toFixed(0);

        // 1. Character Kinematics & Turnaround
        let charDesc = "Ren Kisaragi (1.80m tall, commanding athletic build, dark trench coat)";
        let charNameJa = "如月 蓮";
        let charHeightM = "1.80";
        let actingTone = "tense";
        if (typeof window !== 'undefined' && window.CharacterMasterEngine) {
            const prof = window.CharacterMasterEngine.getCharacterProfile();
            charNameJa = prof.nameJa;
            charHeightM = prof.heightM.toFixed(2);
            actingTone = prof.actingTone;
            charDesc = window.CharacterMasterEngine.generatePromptDescription();
        }

        // 2. Large Stage Props & Vehicles
        let largePropEn = "";
        let largePropJa = "なし";
        if (typeof window !== 'undefined' && window.StagePropEngine) {
            const lpStatus = window.StagePropEngine.getSelectedProp();
            if (lpStatus && lpStatus.key !== "none") {
                largePropJa = `${lpStatus.prop.nameJa} [${lpStatus.layer}]`;
                largePropEn = window.StagePropEngine.generatePromptDescription();
            }
        }

        // 3. Small Handheld Props & Gear
        let smallPropEn = "";
        let smallPropJa = "なし (素手)";
        if (typeof window !== 'undefined' && window.SmallPropEngine) {
            const spStatus = window.SmallPropEngine.getSelectedProp();
            if (spStatus && spStatus.key !== "none") {
                smallPropJa = `${spStatus.prop.nameJa} [${spStatus.holdStyle}]`;
                smallPropEn = window.SmallPropEngine.generatePromptDescription();
            }
        }

        // 4. Multi-Node Dolly Sequence
        let sequenceContextEn = "";
        let sequenceContextJa = "";
        if (params.dollyNodes && params.dollyNodes.length > 1) {
            sequenceContextEn = `Contiguous Multi-Node Dolly Sequence: ${params.dollyNodes.length} connected camera waypoints spanning ${(params.totalDistanceM || 40)}m total tracking path along the exact road vector. `;
            sequenceContextJa = `■ 連続撮影パス: 全${params.dollyNodes.length}ノード (${params.totalDistanceM || 40}m連続ドリー追従)\n`;
        }

        // 5. Synthesis Master English Prompt (Veo 3.1 4K Optimized)
        const promptEn = `Cinematic 4K 60fps movie scene, ultra-realistic visual consistency. ` +
            `Real-World Spatial Location: ${locName} (Exact GPS Coordinates: ${coords}, Camera Heading: ${yaw} deg). Google Maps Ground Truth: ${mapsUrl}. ` +
            `${sequenceContextEn}` +
            `Primary Actor & 4-View Turnaround Coherence: ${charDesc}, maintaining anatomical coherence from all angles. ` +
            `${smallPropEn ? smallPropEn + ' ' : ''}` +
            `${largePropEn ? largePropEn + ' ' : ''}` +
            `Atmosphere & Time of Day: ${tod.promptEn}. ` +
            `Weather & Environmental Lighting: ${weather.promptEn}. ` +
            `Camera Optics & Kinematics: ${tech.promptEn}, ARRI Alexa LF 35mm anamorphic lens, shallow depth of field, photorealistic lighting matched with local geographical sun angle (${tod.kelvin}K), 8K spatial resolution.`;

        // 6. Japanese Director Instruction Sheet
        const promptJa = `【実写座標 ✕ 連続ドリー ✕ キャラクター ✕ 大道具 ✕ 小道具 4K映画シーン】\n` +
            `■ 実写ロケ地: ${locName}\n` +
            `■ 緯度経度: ${coords} (カメラ方位: ${yaw}°)\n` +
            `■ Google Maps: ${mapsUrl}\n` +
            `${sequenceContextJa}` +
            `■ 主役キャスト: ${charNameJa} (${charHeightM}m) ✕ 演技トーン: ${actingTone}\n` +
            `■ 小道具・装備: ${smallPropJa}\n` +
            `■ 大道具・車両: ${largePropJa}\n` +
            `■ 時間帯・光線: ${tod.nameJa} (${tod.kelvin}K)\n` +
            `■ 天候・大気: ${weather.nameJa}\n` +
            `■ カメラワーク: ${tech.nameJa} (ARRI Alexa LF 35mm)`;

        return {
            promptEn: promptEn,
            promptJa: promptJa,
            timeOfDay: tod,
            weather: weather,
            tech: tech
        };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PromptDirectorEngine };
}
if (typeof window !== 'undefined') {
    window.PromptDirectorEngine = new PromptDirectorEngine();
}
console.log("🎬 GENESIS Prompt Director & Lighting Engine v52 Loaded.");
