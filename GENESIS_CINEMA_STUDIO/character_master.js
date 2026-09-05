/**
 * 🎭 GENESIS Character Kinematics & Advanced Cast Generator Engine (character_master.js - v55)
 * - Complete Human Anatomy Customizer: Height (1.40~2.05m), Build, Skin, Hair Styles & Meshes, 6 Costume Styles
 * - Ingested Real-World Photo / Camera Asset Integration
 * - Cast Vault Roster Storage & JSON Serializer
 * - Acting Dynamics & Veo 3.1 360-Degree Master Prompt Synthesis
 */

class CharacterMasterEngine {
    constructor() {
        this.characters = {
            ren: {
                id: "ren",
                nameJa: "如月 蓮",
                nameEn: "Ren Kisaragi",
                age: 28,
                gender: "male",
                heightM: 1.80,
                build: "athletic",
                skinTone: "natural",
                hairStyle: "short_crop",
                hairColor: "#0f172a",
                hairMeshColor: "#00f2fe",
                defaultCostume: "noir_suit",
                neonAccent: "#00f2fe",
                costumes: {
                    noir_suit: {
                        nameJa: "ノワール・ロングトレンチコート",
                        nameEn: "charcoal-black tailored long trench coat, dark turtleneck, matte black trousers",
                        tag: "🧥 ノワールトレンチ",
                        color: "#0f172a",
                        accentColor: "#00f2fe"
                    },
                    tactical_gear: {
                        nameJa: "タクティカル・オペレーションギア",
                        nameEn: "tactical stealth vest with concealed holsters, dark urban combat fatigues",
                        tag: "🛡️ タクティカルギア",
                        color: "#1e293b",
                        accentColor: "#10b981"
                    },
                    bespoke_suit: {
                        nameJa: "漆黒テーラードスーツ",
                        nameEn: "sharp bespoke all-black three-piece suit with slim tie",
                        tag: "👔 テーラードスーツ",
                        color: "#020617",
                        accentColor: "#f59e0b"
                    }
                }
            },
            kagerou: {
                id: "kagerou",
                nameJa: "緋村 影狼",
                nameEn: "Kagerou Himura",
                age: 32,
                gender: "male",
                heightM: 1.85,
                build: "heavy",
                skinTone: "tan",
                hairStyle: "swept_back",
                hairColor: "#1e293b",
                hairMeshColor: "#94a3b8",
                defaultCostume: "cyber_riders",
                neonAccent: "#f59e0b",
                costumes: {
                    cyber_riders: {
                        nameJa: "ブラック・ライダースジャケット",
                        nameEn: "heavy black leather riders jacket with silver zips, dark combat boots",
                        tag: "🧥 ライダース",
                        color: "#18181b",
                        accentColor: "#f59e0b"
                    },
                    tactical_gear: {
                        nameJa: "特殊工作員コンバットスーツ",
                        nameEn: "high-tech tactical ballistic suit, combat harness, tactical gauntlets",
                        tag: "🛡️ コンバットスーツ",
                        color: "#09090b",
                        accentColor: "#ef4444"
                    }
                }
            },
            yuki: {
                id: "yuki",
                nameJa: "霧島 結衣",
                nameEn: "Yui Kirishima",
                age: 25,
                gender: "female",
                heightM: 1.68,
                build: "slender",
                skinTone: "fair",
                hairStyle: "ponytail",
                hairColor: "#090d16",
                hairMeshColor: "#a855f7",
                defaultCostume: "noir_suit",
                neonAccent: "#00f2fe",
                costumes: {
                    noir_suit: {
                        nameJa: "スマート・エージェントスーツ",
                        nameEn: "sleek charcoal slim-fit intelligence agent coat, tactical gloves",
                        tag: "🧥 エージェントコート",
                        color: "#334155",
                        accentColor: "#00f2fe"
                    },
                    neo_kimono: {
                        nameJa: "現代サイバー羽織・和装",
                        nameEn: "modern cyberpunk tailored haori jacket with luminescent cyan geometric embroidery",
                        tag: "🥋 サイバー羽織",
                        color: "#0f172a",
                        accentColor: "#a855f7"
                    }
                }
            },
            asuka: {
                id: "asuka",
                nameJa: "橘 飛鳥",
                nameEn: "Asuka Tachibana",
                age: 24,
                gender: "female",
                heightM: 1.72,
                build: "athletic",
                skinTone: "cyber_pale",
                hairStyle: "wolf_cut",
                hairColor: "#0a0a0c",
                hairMeshColor: "#00f2fe",
                defaultCostume: "urban_techwear",
                neonAccent: "#00f2fe",
                costumes: {
                    urban_techwear: {
                        nameJa: "サイバーパンク・ロングライダース",
                        nameEn: "cyberpunk matte-black tailored leather coat with luminescent cyan seams",
                        tag: "✨ サイバーテック",
                        color: "#0284c7",
                        accentColor: "#00f2fe"
                    }
                }
            }
        };

        this.selectedCharId = "ren";
        this.selectedCostumeKey = "noir_suit";
        this.currentAngle = "front";
        this.actingTone = "tense";
        this.emotionIntensity = 85;
        this.walkSpeedKmh = 4.2;
        this.motionType = "walking_forward";
        this.castVault = [];
    }

    /**
     * 👥 Create or update custom actor dynamically (with deep customization & photo ingestion)
     */
    createCustomActor(params = {}) {
        const id = params.id || "custom_" + Date.now();
        const customActor = {
            id: id,
            nameJa: params.nameJa || "カスタム主人公",
            nameEn: params.nameEn || "Custom Protagonist",
            age: parseInt(params.age || 26),
            gender: params.gender || "male",
            heightM: parseFloat(params.heightM || 1.78),
            build: params.build || "athletic", // slender, athletic, heavy, tactical
            skinTone: params.skinTone || "natural", // fair, natural, tan, dark, cyber_pale
            hairStyle: params.hairStyle || "short_crop", // short_crop, side_part, ponytail, long_straight, wolf_cut, swept_back, cyber_undercut
            hairColor: params.hairColor || "#0f172a",
            hairMeshColor: params.hairMeshColor || "#00f2fe",
            neonAccent: params.neonAccent || "#00f2fe",
            isIngestedPhoto: !!params.isIngestedPhoto,
            photoDataUrl: params.photoDataUrl || "",
            defaultCostume: "custom_style",
            costumes: {
                custom_style: {
                    nameJa: params.costumeNameJa || "カスタムシネマ衣装",
                    nameEn: params.costumeNameEn || "tailored stylish cinematic jacket, dark modern trousers, clean sneakers",
                    tag: "✨ カスタム衣装",
                    color: params.costumeColor || "#1e293b",
                    accentColor: params.neonAccent || "#00f2fe"
                }
            }
        };

        this.characters[id] = customActor;
        this.selectedCharId = id;
        this.selectedCostumeKey = "custom_style";

        // Sync with Turnaround Engine
        if (typeof window !== 'undefined' && window.CharacterTurnaroundEngine) {
            window.CharacterTurnaroundEngine.createCharacter({
                id: id,
                nameJa: customActor.nameJa,
                nameEn: customActor.nameEn,
                age: customActor.age,
                gender: customActor.gender,
                heightM: customActor.heightM,
                build: customActor.build,
                skinTone: customActor.skinTone,
                hairStyle: customActor.hairStyle,
                hairColor: customActor.hairColor,
                hairMeshColor: customActor.hairMeshColor,
                neonAccent: customActor.neonAccent,
                costumeColor: customActor.costumes.custom_style.color,
                photoDataUrl: customActor.photoDataUrl,
                styleDescription: `${customActor.age}yo ${customActor.gender}, ${customActor.build} build, wearing ${customActor.costumes.custom_style.nameEn}`,
                actionDescription: "walking forward with steady cinematic pace"
            });
        }

        return this.getCharacterProfile();
    }

    selectCharacter(charId) {
        if (this.characters[charId]) {
            this.selectedCharId = charId;
            if (!this.characters[charId].costumes[this.selectedCostumeKey]) {
                this.selectedCostumeKey = Object.keys(this.characters[charId].costumes)[0];
            }
            if (typeof window !== 'undefined' && window.CharacterTurnaroundEngine) {
                const char = this.characters[charId];
                const costume = char.costumes[this.selectedCostumeKey] || Object.values(char.costumes)[0];
                window.CharacterTurnaroundEngine.createCharacter({
                    id: char.id,
                    nameJa: char.nameJa,
                    nameEn: char.nameEn,
                    age: char.age,
                    gender: char.gender,
                    heightM: char.heightM,
                    build: char.build,
                    skinTone: char.skinTone,
                    hairStyle: char.hairStyle,
                    hairColor: char.hairColor,
                    hairMeshColor: char.hairMeshColor,
                    neonAccent: char.neonAccent,
                    costumeColor: costume.color,
                    photoDataUrl: char.photoDataUrl || ""
                });
            }
        }
        return this.getCharacterProfile();
    }

    setCostume(costumeKey) {
        const char = this.characters[this.selectedCharId];
        if (char && char.costumes[costumeKey]) {
            this.selectedCostumeKey = costumeKey;
        }
        return this.getCharacterProfile();
    }

    setActingTone(tone, intensity = 85) {
        this.actingTone = tone;
        this.emotionIntensity = parseInt(intensity);
        return this.getCharacterProfile();
    }

    getCharacterProfile() {
        const char = this.characters[this.selectedCharId] || this.characters.ren;
        const costume = char.costumes[this.selectedCostumeKey] || Object.values(char.costumes)[0];
        
        return {
            charId: char.id,
            nameJa: char.nameJa,
            nameEn: char.nameEn,
            age: char.age || 28,
            gender: char.gender || "male",
            heightM: char.heightM,
            build: char.build || "athletic",
            skinTone: char.skinTone || "natural",
            hairStyle: char.hairStyle || "short_crop",
            hairColor: char.hairColor || "#0f172a",
            hairMeshColor: char.hairMeshColor || "#00f2fe",
            neonAccent: char.neonAccent || "#00f2fe",
            costumeKey: this.selectedCostumeKey,
            costumeNameJa: costume.nameJa,
            costumeNameEn: costume.nameEn,
            costumeTag: costume.tag,
            costumeColor: costume.color || "#0f172a",
            angle: this.currentAngle,
            actingTone: this.actingTone,
            emotionIntensity: this.emotionIntensity,
            walkSpeedKmh: this.walkSpeedKmh,
            motionType: this.motionType,
            photoDataUrl: char.photoDataUrl || ""
        };
    }

    /**
     * 🗃️ Cast Vault Management
     */
    saveToVault() {
        const prof = this.getCharacterProfile();
        const existingIdx = this.castVault.findIndex(c => c.charId === prof.charId);
        if (existingIdx >= 0) {
            this.castVault[existingIdx] = prof;
        } else {
            this.castVault.push(prof);
        }
        return this.castVault;
    }

    getVaultList() {
        return this.castVault;
    }

    exportVaultJSON() {
        return JSON.stringify({
            version: "GENESIS_CAST_VAULT_v55",
            exportedAt: new Date().toISOString(),
            castCount: this.castVault.length,
            roster: this.castVault
        }, null, 2);
    }

    generatePromptDescription() {
        const prof = this.getCharacterProfile();
        let toneDesc = "tense focused expression with intense piercing eyes";
        if (this.actingTone === "confident") toneDesc = "commanding confident expression, unwavering calm posture";
        else if (this.actingTone === "angry") toneDesc = "intense furious expression with clenched jaw and sharp predatory gaze";
        else if (this.actingTone === "calm") toneDesc = "stoic emotionless analytical gaze, silent operative presence";
        else if (this.actingTone === "fear") toneDesc = "haunted vigilant gaze, rapid breathing with hyper-alert awareness";
        else if (this.actingTone === "joy") toneDesc = "exhilarated triumphant smile, vibrant charismatic energy";

        return `${prof.nameEn} (${prof.age}yo, ${prof.gender === 'female' ? 'female' : 'male'}, ${prof.heightM}m tall, ${prof.build} build, ${prof.hairStyle} hair in ${prof.hairColor}), wearing ${prof.costumeNameEn}, walking forward steadily along the road, displaying ${toneDesc}`;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CharacterMasterEngine };
}
if (typeof window !== 'undefined') {
    window.CharacterMasterEngine = new CharacterMasterEngine();
}
console.log("🎭 GENESIS Advanced Character Master Engine v55 Loaded.");
