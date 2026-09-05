/**
 * 📂 GENESIS Production Vault & Google Workspace Asset Manager (workspace_production_vault.js - v46)
 * - Google Sheets / Drive / JSON Schema Compatible
 * - Unlimited Dynamic Asset Scalability: Cast, Costumes, Locations, Vehicles, Props & Screenplay Cuts
 */

class WorkspaceProductionVault {
    constructor() {
        this.storageKey = "GENESIS_CINEMA_VAULT_DATA_V46";
        this.vault = this.loadVault();
    }

    getDefaultVault() {
        return {
            metadata: {
                studioName: "GENESIS Cinema Production Studio",
                version: "46.0",
                lastUpdated: new Date().toISOString(),
                exportFormat: "Google_Sheets_Compatible_V4"
            },
            characters: [
                {
                    id: "ren",
                    nameJa: "如月 蓮",
                    nameEn: "Ren Kisaragi",
                    heightM: 1.80,
                    role: "主人公 / 特殊捜査官",
                    voiceModel: "ja-JP-Chirp3-HD-Ren",
                    costumes: ["ノワールトレンチ", "レザージャケット", "タクティカルギア"],
                    status: "Active"
                },
                {
                    id: "kagerou",
                    nameJa: "緋村 影狼",
                    nameEn: "Kagerou Himura",
                    heightM: 1.85,
                    role: "元工作員 / ライバル",
                    voiceModel: "ja-JP-Chirp3-HD-Ren",
                    costumes: ["ライダース", "コンバットスーツ", "テーラードスーツ"],
                    status: "Active"
                },
                {
                    id: "yuki",
                    nameJa: "霧島 結衣",
                    nameEn: "Yui Kirishima",
                    heightM: 1.68,
                    role: "情報統括アナリスト",
                    voiceModel: "ja-JP-Chirp3-HD-Yui",
                    costumes: ["エージェントコート", "ウィンドブレーカー"],
                    status: "Active"
                }
            ],
            locations: [
                {
                    id: "harajuku_underground",
                    nameJa: "原宿・明治神宮前 地下コンコース (B1F)",
                    nameEn: "Harajuku / Meiji-jingumae Underground Concourse",
                    coords: "35.669921, 139.702518",
                    ceilingHeightM: 2.80,
                    depthM: -3.5,
                    category: "underground",
                    google3DTiles: "Available"
                },
                {
                    id: "shibuya_109_tele",
                    nameJa: "渋谷 109前 スクランブル交差点",
                    nameEn: "Shibuya 109 Crossing Tokyo",
                    coords: "35.6596286, 139.7005925",
                    ceilingHeightM: 50.0,
                    elevationM: 18.5,
                    category: "surface",
                    google3DTiles: "Available"
                },
                {
                    id: "nakano_sunmall",
                    nameJa: "中野サンモール商店街 アーケード",
                    nameEn: "Nakano Sun Mall Shopping Arcade",
                    coords: "35.7083894, 139.6656314",
                    ceilingHeightM: 9.20,
                    elevationM: 42.0,
                    category: "arcade",
                    google3DTiles: "Available"
                }
            ],
            vehicles: [
                { id: "jpn_taxi", nameJa: "ジャパンタクシー (JPN TAXI)", heightM: 1.75, widthM: 1.70, lengthM: 4.40 },
                { id: "city_bus", nameJa: "都営路線バス (Tokyo City Bus)", heightM: 3.20, widthM: 2.50, lengthM: 10.50 },
                { id: "black_sedan", nameJa: "黒塗り高級セダン (VIP Sedan)", heightM: 1.45, widthM: 1.88, lengthM: 4.95 },
                { id: "patrol_car", nameJa: "警視庁 パトカー (Police Cruiser)", heightM: 1.60, widthM: 1.80, lengthM: 4.90 }
            ],
            screenplayCuts: [
                {
                    cutId: "CUT_01",
                    sceneName: "原宿地下 ターンアウト急旋回",
                    charId: "ren",
                    locationId: "harajuku_underground",
                    cameraAction: "turn_out",
                    dialogueKey: "ren_harajuku_concourse"
                },
                {
                    cutId: "CUT_02",
                    sceneName: "渋谷109 超望遠ドリー追従",
                    charId: "ren",
                    locationId: "shibuya_109_tele",
                    cameraAction: "tracking_dolly",
                    dialogueKey: "kagerou_shibuya_standoff"
                }
            ]
        };
    }

    loadVault() {
        if (typeof localStorage !== 'undefined') {
            const raw = localStorage.getItem(this.storageKey);
            if (raw) {
                try {
                    return JSON.parse(raw);
                } catch(e) {
                    console.warn("Vault parse fallback:", e);
                }
            }
        }
        return this.getDefaultVault();
    }

    saveVault() {
        this.vault.metadata.lastUpdated = new Date().toISOString();
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem(this.storageKey, JSON.stringify(this.vault));
        }
        if (typeof window !== 'undefined' && window.MultiDisplayEngine) {
            window.MultiDisplayEngine.broadcast("VAULT_SYNC", this.vault);
        }
        return this.vault;
    }

    addCharacter(charData) {
        this.vault.characters.push(charData);
        this.saveVault();
        return this.vault.characters;
    }

    addLocation(locData) {
        this.vault.locations.push(locData);
        this.saveVault();
        return this.vault.locations;
    }

    exportToGoogleSheetsJson() {
        return JSON.stringify(this.vault, null, 2);
    }

    exportToCSV(category = "characters") {
        const items = this.vault[category] || [];
        if (items.length === 0) return "";
        const keys = Object.keys(items[0]);
        const header = keys.join(",");
        const rows = items.map(obj => keys.map(k => JSON.stringify(obj[k] || "")).join(","));
        return [header, ...rows].join("\n");
    }
}

if (typeof window !== 'undefined') {
    window.WorkspaceProductionVault = new WorkspaceProductionVault();
    console.log("📂 GENESIS Production Vault & Google Workspace Asset Manager v46 Loaded.");
}
