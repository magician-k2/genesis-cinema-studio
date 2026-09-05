/**
 * 🏛️ GENESIS Stage & Set Large Props Engine (stage_prop_engine.js - v52)
 * - Vehicles (Taxi, Bus, VIP Sedan, Patrol Car, Cyber Hover)
 * - Architecture & Large Set Structures (Torii Gate, Neon Stalls, Barricades, Hologram Towers, Search Drones)
 * - Z-Depth Layering (Foreground, Midground, Background)
 */

class StagePropEngine {
    constructor() {
        this.selectedPropKey = "none";
        this.placementLayer = "midground"; // foreground, midground, background
        this.lightingInteraction = "reflective"; // reflective, casting_shadows, glowing

        this.props = {
            none: {
                id: "none",
                nameJa: "なし (オープン空間)",
                nameEn: "none",
                category: "none",
                heightM: 0,
                promptEn: "",
                descJa: "特設の大道具を配置せず、実写ロケ地の背景をそのまま活かします。"
            },
            // --- Vehicles ---
            jpn_taxi: {
                id: "jpn_taxi",
                nameJa: "🚕 トヨタ JPN TAXI (行灯点灯)",
                nameEn: "iconic deep indigo-black Toyota JPN TAXI cab with glowing amber roof lamp",
                category: "vehicle",
                heightM: 1.75,
                widthM: 1.70,
                lengthM: 4.40,
                promptEn: "a deep indigo-black Toyota JPN TAXI cab (1.75m height) with illuminated roof lamp, glossy body reflecting city lights",
                descJa: "日本の街並みを象徴する全高1.75mのトールワゴンタクシー。"
            },
            city_bus: {
                id: "city_bus",
                nameJa: "🚌 都営路線バス (大型ノンステップ)",
                nameEn: "large green-and-white Tokyo Metropolitan transit bus with illuminated LED destination sign",
                category: "vehicle",
                heightM: 3.20,
                widthM: 2.50,
                lengthM: 10.50,
                promptEn: "a massive green-and-white Tokyo City transit bus (3.2m height, 10.5m length) idling with illuminated route LED signage, providing immense architectural scale contrast",
                descJa: "全高3.2mの大型ノンステップバス。圧倒的な重量感とスケール対比。"
            },
            black_sedan: {
                id: "black_sedan",
                nameJa: "🚘 黒塗りVIPセダン (スモークガラス)",
                nameEn: "sleek glossy black executive luxury sedan with dark tinted privacy windows",
                category: "vehicle",
                heightM: 1.45,
                widthM: 1.88,
                lengthM: 4.95,
                promptEn: "a sleek executive black luxury sedan (1.45m height) with tinted privacy glass and mirror-polished bodywork reflecting ambient headlights",
                descJa: "漆黒の高級セダン。光沢ボディへの街灯反射とサスペンス感。"
            },
            patrol_car: {
                id: "patrol_car",
                nameJa: "🚓 警視庁 パトカー (赤色灯点滅)",
                nameEn: "Tokyo Metropolitan Police black-and-white Crown patrol car with flashing red aerodynamic LED lightbar",
                category: "vehicle",
                heightM: 1.60,
                widthM: 1.80,
                lengthM: 4.90,
                promptEn: "a Japanese police patrol cruiser (1.6m height) with synchronized flashing red emergency lightbars casting pulsating crimson reflections on the pavement",
                descJa: "白黒パトカー。ルーフの赤色灯が周囲を緊迫感ある赤色光で照らし出す。"
            },
            cyber_hover: {
                id: "cyber_hover",
                nameJa: "🏎️ 近未来ホバービークル (反重力グロー)",
                nameEn: "futuristic matte-black anti-gravity hover vehicle floating 0.4m above the ground with cyan neon underglow",
                category: "vehicle",
                heightM: 1.30,
                widthM: 2.00,
                lengthM: 4.80,
                promptEn: "a futuristic aerodynamic hover speeder (1.3m height) floating smoothly above the road with glowing cyan anti-gravity emitter underglow",
                descJa: "地上40cmを浮遊する近未来ビークル。サイアンのネオングロー。"
            },

            // --- Large Set Structures & Architecture ---
            torii_gate: {
                id: "torii_gate",
                nameJa: "⛩️ 巨大朱塗り鳥居 ＆ 提灯ゲート",
                nameEn: "monumental vermilion Japanese Torii gate flanked by glowing paper lanterns",
                category: "structure",
                heightM: 8.50,
                promptEn: "a towering 8.5m-tall vermilion red traditional Torii gate flanked by hanging glowing paper lanterns, casting a warm majestic crimson illumination over the street",
                descJa: "全高8.5mの壮大な朱塗り鳥居。温かい提灯の光が厳かな映画の空気感を創出。"
            },
            festival_stall: {
                id: "festival_stall",
                nameJa: "🎪 ネオン屋台 ＆ 露店テント (祝祭セット)",
                nameEn: "vibrant traditional festival food stalls with glowing neon lanterns, canvas awnings, and gentle rising food steam",
                category: "structure",
                heightM: 2.80,
                promptEn: "lively festival street stalls (2.8m height) with glowing Japanese red-and-white lanterns, striped canvas awnings, and faint rising steam mingling with the lighting",
                descJa: "提灯が灯るお祭り屋台セット。立ち上る湯気と映画的な祝祭の活気。"
            },
            police_barricade: {
                id: "police_barricade",
                nameJa: "🚧 警戒バリケード ＆ 発光コーン (封鎖セット)",
                nameEn: "yellow-and-black emergency perimeter barricades with blinking LED traffic beacons and reflective hazard tape",
                category: "structure",
                heightM: 1.20,
                promptEn: "high-contrast black-and-yellow hazard barricades (1.2m height) wrapped in reflective police tape with pulsating strobe beacons sealing off the roadway",
                descJa: "立ち入り禁止の警戒バリケード。ストロボライトによるサスペンス緊迫空間。"
            },
            hologram_tower: {
                id: "hologram_tower",
                nameJa: "🏢 巨大立体ホログラム広告塔 (サイバー都市)",
                nameEn: "towering 15m volumetric cyberpunk 3D hologram billboard projector casting flickering multi-colored light",
                category: "structure",
                heightM: 15.0,
                promptEn: "a massive 15m-tall cyberpunk holographic advertising monolith projecting flickering 3D neon visuals that cast volumetric magenta and cyan light beams across the scene",
                descJa: "15mの巨大3D立体ホログラム広告。大気中に揺らめくマゼンタとサイアンの光線。"
            },
            police_drone: {
                id: "police_drone",
                nameJa: "🚁 上空ホバリング・サーチライトドローン",
                nameEn: "tactical heavy-lift surveillance drone hovering 6m overhead with a brilliant high-intensity spotlight beam",
                category: "structure",
                heightM: 2.50,
                promptEn: "a heavy tactical quad-rotor police drone hovering 6m overhead, directing a brilliant 10,000-lumen conical searchlight beam down onto the street, illuminating atmospheric dust particles",
                descJa: "上空6mから強力なサーチライトを照射する大型ドローン。光条が空間の立体感を強調。"
            }
        };
    }

    selectProp(propKey) {
        if (this.props[propKey]) {
            this.selectedPropKey = propKey;
        }
        return this.getSelectedProp();
    }

    setLayer(layer) {
        if (["foreground", "midground", "background"].includes(layer)) {
            this.placementLayer = layer;
        }
        return this.getSelectedProp();
    }

    getSelectedProp() {
        const prop = this.props[this.selectedPropKey] || this.props.none;
        return {
            key: this.selectedPropKey,
            prop: prop,
            layer: this.placementLayer,
            heightM: prop.heightM,
            category: prop.category
        };
    }

    generatePromptDescription() {
        if (this.selectedPropKey === "none") return "";
        const p = this.getSelectedProp();
        const layerMap = {
            foreground: "in the immediate cinematic foreground, framing the bottom and side of the shot with sharp depth-of-field separation",
            midground: "positioned in the midground adjacent to the main subject, establishing direct physical scale and spatial presence",
            background: "anchored in the atmospheric background along the road vanishing axis"
        };

        return `Large Set Piece & Environmental Prop: ${p.prop.promptEn}, placed ${layerMap[p.layer]}.`;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StagePropEngine };
}
if (typeof window !== 'undefined') {
    window.StagePropEngine = new StagePropEngine();
}
console.log("🏛️ GENESIS Stage & Set Large Props Engine v52 Loaded.");
