/**
 * 📱 GENESIS Small & Handheld Props Engine (small_prop_engine.js - v52)
 * - Tech & Communication (AR Smart Glasses, Encrypted Phone, Military Tablet)
 * - Handheld Gear & Luggage (Secret Attache Case, Leather Dossier, Coffee, Backpack)
 * - Weapons & Tactical (Silenced Handgun, Combat Knife, Ballistic Shield, Flashlight)
 * - Life & Celebration (BBQ Tongs, Vintage Camera, Champagne Glass)
 */

class SmallPropEngine {
    constructor() {
        this.selectedPropKey = "none";
        this.holdStyle = "right_hand"; // right_hand, two_handed, equipped_body, shoulder_slung

        this.props = {
            none: {
                id: "none",
                nameJa: "なし (素手)",
                nameEn: "bare hands",
                category: "none",
                promptEn: "hands free and unencumbered",
                descJa: "手持ちアイテムを持たず、自然な歩行・身振り手振りを表現。"
            },
            // --- Tech & Communication ---
            smart_glasses: {
                id: "smart_glasses",
                nameJa: "🕶️ ARスマートグラス (HUD透過ディスプレイ)",
                nameEn: "sleek cyberpunk AR smart glasses with subtle glowing cyan micro-HUD reflections on the lenses",
                category: "tech",
                promptEn: "wearing high-tech AR smart glasses with subtle cyan digital HUD data flickering across the ultra-thin polarized lenses",
                descJa: "レンズ内側にサイバーパンクHUDデータが淡く反射するスマートグラス。"
            },
            encrypted_phone: {
                id: "encrypted_phone",
                nameJa: "📱 暗号化スマートフォン (生体スキャン)",
                nameEn: "matte black bezel-less encrypted smartphone with glowing green biometric verification interface on screen",
                category: "tech",
                promptEn: "holding a matte black encrypted smartphone displaying glowing tactical interface waveforms",
                descJa: "マットブラックの防諜スマホ。画面の波形が演者の表情を照らす。"
            },
            tactical_tablet: {
                id: "tactical_tablet",
                nameJa: "💻 ミリタリーグレード堅牢タブレット",
                nameEn: "ruggedized carbon-fiber military field tablet displaying active 3D radar maps and satellite overlays",
                category: "tech",
                promptEn: "operating a ruggedized military-grade field tablet with an active 3D wireframe tactical map casting blue screen light onto the character",
                descJa: "頑丈なカーボンファイバー作戦端末。3Dワイヤーフレーム地図が光る。"
            },

            // --- Luggage & Narrative Items ---
            attache_case: {
                id: "attache_case",
                nameJa: "💼 極秘ジュラルミン・アタッシュケース",
                nameEn: "brushed silver duralumin security attache briefcase with reinforced titanium corners and dual digital biometric locks",
                category: "luggage",
                promptEn: "carrying a brushed silver duralumin security attache briefcase with reinforced titanium latches and dual digital biometric locks",
                descJa: "銀色に輝くジュラルミン製アタッシュケース。映画のサスペンスストーリーの核。"
            },
            leather_dossier: {
                id: "leather_dossier",
                nameJa: "📁 黒革調書ファイル (極秘機密文書)",
                nameEn: "weathered black leather classified dossier folder stamped with confidential intelligence seals",
                category: "luggage",
                promptEn: "clutching a thick black leather classified intelligence dossier stamped with red 'TOP SECRET' embossing",
                descJa: "極秘スタンプが押された黒革の機密ファイル。"
            },
            takeaway_coffee: {
                id: "takeaway_coffee",
                nameJa: "☕ テイクアウト紙コップ (立ち上る蒸気)",
                nameEn: "black artisanal takeaway coffee cup with cardboard sleeve and delicate wisp of hot steam rising into the cold air",
                category: "lifestyle",
                promptEn: "holding a black takeaway coffee cup with a delicate wisp of hot steam swirling into the atmospheric lighting",
                descJa: "湯気が立ち上るブラックのカフェカップ。日常感と映画的リラックス。"
            },

            // --- Weapons & Tactical Gear ---
            silenced_handgun: {
                id: "silenced_handgun",
                nameJa: "🔫 サイレンサー付きタクティカルハンドガン",
                nameEn: "matte-black 9mm tactical semi-automatic pistol fitted with a cylindrical carbon-fiber sound suppressor",
                category: "tactical",
                promptEn: "gripping a matte-black 9mm tactical handgun equipped with a sleek cylindrical carbon-fiber silencer in a disciplined low-ready stance",
                descJa: "消音器付きタクティカルピストル。マットブラックの重厚な質感。"
            },
            combat_knife: {
                id: "combat_knife",
                nameJa: "🗡️ タクティカル・コンバットナイフ",
                nameEn: "tactical black-coated tungsten combat knife with textured G10 grip handle",
                category: "tactical",
                promptEn: "holding a non-reflective black tungsten combat knife with a razor-sharp bevel edge catching subtle rim highlights",
                descJa: "反射防止加工されたタングステンナイフ。刃先の鋭いハイライト。"
            },
            tactical_flashlight: {
                id: "tactical_flashlight",
                nameJa: "🔦 高輝度LEDタクティカルライト (強力光条)",
                nameEn: "heavy anodized aluminum tactical LED torch projecting a sharp brilliant 1,500-lumen white volumetric beam cutting through the atmosphere",
                category: "tactical",
                promptEn: "pointing a heavy tactical LED flashlight that casts a brilliant, razor-sharp volumetric cone of light slicing through the atmospheric dust",
                descJa: "1500ルーメンの強力な光条が夜間・暗闇の大気を切り裂く。"
            },

            // --- Life & Celebration ---
            bbq_tongs: {
                id: "bbq_tongs",
                nameJa: "🍖 BBQグリル用ステンレス角トング",
                nameEn: "heavy-duty stainless steel BBQ grill tongs holding a sizzling skewer with rising charcoal smoke",
                category: "lifestyle",
                promptEn: "holding long stainless steel BBQ cooking tongs with sizzling embers and gentle rising charcoal smoke adding organic atmosphere",
                descJa: "炭火の煙と肉汁が香るBBQトング。アウトドアや野外祝祭シーンに最適。"
            },
            vintage_camera: {
                id: "vintage_camera",
                nameJa: "📸 ヴィンテージ一眼レフカメラ (35mmレンズ)",
                nameEn: "classic chrome-and-black 35mm mechanical rangefinder camera with worn brown leather neck strap",
                category: "lifestyle",
                promptEn: "carrying a classic chrome-and-black vintage 35mm rangefinder camera on a weathered brown leather strap",
                descJa: "クラシックな銀黒レンジファインダーカメラ。本革ストラップ。"
            },
            champagne_glass: {
                id: "champagne_glass",
                nameJa: "🍾 クリスタル・シャンパングラス (黄金発泡)",
                nameEn: "elegant crystal champagne flute filled with effervescent sparkling golden wine capturing delicate refraction highlights",
                category: "lifestyle",
                promptEn: "holding a fine crystal champagne flute with effervescent golden bubbles catching glittering ambient lens flare",
                descJa: "黄金色にきらめくシャンパングラス。優雅なパーティー・祝杯シーン。"
            }
        };
    }

    selectProp(propKey) {
        if (this.props[propKey]) {
            this.selectedPropKey = propKey;
        }
        return this.getSelectedProp();
    }

    setHoldStyle(style) {
        if (["right_hand", "two_handed", "equipped_body", "shoulder_slung"].includes(style)) {
            this.holdStyle = style;
        }
        return this.getSelectedProp();
    }

    getSelectedProp() {
        const prop = this.props[this.selectedPropKey] || this.props.none;
        return {
            key: this.selectedPropKey,
            prop: prop,
            holdStyle: this.holdStyle,
            category: prop.category
        };
    }

    generatePromptDescription() {
        if (this.selectedPropKey === "none") return "";
        const p = this.getSelectedProp();
        const styleMap = {
            right_hand: "held firmly in the character's right hand with natural grip dynamics",
            two_handed: "held and operated with both hands with focused tactile precision",
            equipped_body: "worn directly on the character's body as specialized personal equipment",
            shoulder_slung: "slung comfortably over the character's shoulder with authentic drape and weight"
        };

        return `Handheld Prop & Equipment: ${p.prop.promptEn}, ${styleMap[p.holdStyle]}.`;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SmallPropEngine };
}
if (typeof window !== 'undefined') {
    window.SmallPropEngine = new SmallPropEngine();
}
console.log("📱 GENESIS Small & Handheld Props Engine v52 Loaded.");
