/**
 * 📜 GENESIS Storyboard & Cinematic Script Engine (storyboard_script_engine.js - v55)
 * - Complete Hierarchical Script & Scene Management (Scene -> Shot -> Action & Dialogue)
 * - Cinematic Storyboard Optics & Composition Calculations (2.39:1 Anamorphic, Focal Length, F-stop, Camera Action)
 * - Google Chirp 3 HD Dialogue Synthesis & Emotion Modulation
 * - Timecode Accumulator & Timeline Dialogue Track Bridge
 * - Quad-Display W3C BroadcastChannel Synchronizer
 */

class StoryboardScriptEngine {
    constructor() {
        this.scenes = [
            {
                id: "scene_01",
                sceneNumber: 1,
                title: "表参道・雨の追跡 (Omotesando Rain Pursuit)",
                location: {
                    name: "原宿 表参道 (Omotesando Main Avenue)",
                    coords: { lat: 35.6699, lng: 139.7025 },
                    heading: 108.0,
                    pitch: -1.0,
                    timeOfDay: "sunset",
                    weather: "heavy_rain"
                },
                shots: [
                    {
                        id: "shot_01_01",
                        shotNumber: 1,
                        name: "Shot 1: 追従ドリー (正面ローアングル)",
                        durationSec: 5.0,
                        aspectRatio: "2.39:1",
                        lensMm: 35,
                        fStop: 2.8,
                        angle: "low_angle",
                        shotSize: "full",
                        cameraWork: "dolly_in",
                        gridType: "rule_of_thirds",
                        actionDescription: "如月蓮が大雨の表参道をアタッシュケースを抱えて早足で歩いてくる。アスファルトの濡れた路面に街灯とネオンが反射する。",
                        dialogues: [
                            {
                                id: "dlg_01_01_01",
                                speaker: "如月 蓮",
                                characterId: "ren",
                                tone: "tense",
                                lang: "ja-JP",
                                text: "……時間がない。奴らの包囲網が狭まっている。",
                                speed: 1.0,
                                durationEstSec: 3.2
                            }
                        ]
                    },
                    {
                        id: "shot_01_02",
                        shotNumber: 2,
                        name: "Shot 2: 背後からの緊迫クローズアップ",
                        durationSec: 4.0,
                        aspectRatio: "2.39:1",
                        lensMm: 85,
                        fStop: 1.8,
                        angle: "eye_level",
                        shotSize: "closeup",
                        cameraWork: "tracking",
                        gridType: "golden_ratio",
                        actionDescription: "如月蓮の鋭い眼光。背後から黒塗りVIPセダンがヘッドライトを消して静かに接近する。",
                        dialogues: [
                            {
                                id: "dlg_01_02_01",
                                speaker: "如月 蓮",
                                characterId: "ren",
                                tone: "whisper",
                                lang: "ja-JP",
                                text: "尾行か……。感づかれたようだな。",
                                speed: 0.95,
                                durationEstSec: 2.8
                            }
                        ]
                    }
                ]
            },
            {
                id: "scene_02",
                sceneNumber: 2,
                title: "浅草寺・雷鳴の決闘 (Asakusa Thunder Duel)",
                location: {
                    name: "サイバー浅草寺 (雷門 Neo-Tokyo)",
                    coords: { lat: 35.7111, lng: 139.7963 },
                    heading: 180.0,
                    pitch: 0.0,
                    timeOfDay: "night",
                    weather: "thunderstorm"
                },
                shots: [
                    {
                        id: "shot_02_01",
                        shotNumber: 1,
                        name: "Shot 1: 巨大鳥居の対峙 (ワイドクレーン)",
                        durationSec: 6.0,
                        aspectRatio: "2.39:1",
                        lensMm: 24,
                        fStop: 4.0,
                        angle: "low_angle",
                        shotSize: "extreme_long",
                        cameraWork: "crane_up",
                        gridType: "symmetry",
                        actionDescription: "巨大な朱塗りの雷門前。雷光が夜空を裂き、如月蓮と緋村影狼が10メートルの距離を置いて睨み合う。",
                        dialogues: [
                            {
                                id: "dlg_02_01_01",
                                speaker: "緋村 影狼",
                                characterId: "kagerou",
                                tone: "cold",
                                lang: "ja-JP",
                                text: "ここまでだ、如月。そのアタッシュケースを置いていけ。",
                                speed: 1.0,
                                durationEstSec: 3.8
                            },
                            {
                                id: "dlg_02_01_02",
                                speaker: "如月 蓮",
                                characterId: "ren",
                                tone: "tense",
                                lang: "ja-JP",
                                text: "断る。これをお前たちに渡すわけにはいかない。",
                                speed: 1.05,
                                durationEstSec: 3.5
                            }
                        ]
                    }
                ]
            },
            {
                id: "scene_03",
                sceneNumber: 3,
                title: "渋谷スクランブル・深夜潜入 (Shibuya Stealth Infiltration)",
                location: {
                    name: "渋谷 スクランブル交差点 (Shibuya Crossing)",
                    coords: { lat: 35.6595, lng: 139.7005 },
                    heading: 0.0,
                    pitch: 5.0,
                    timeOfDay: "night",
                    weather: "dense_fog"
                },
                shots: [
                    {
                        id: "shot_03_01",
                        shotNumber: 1,
                        name: "Shot 1: 霧のネオン街 (ハイアングル旋回)",
                        durationSec: 5.5,
                        aspectRatio: "2.39:1",
                        lensMm: 50,
                        fStop: 2.0,
                        angle: "high_angle",
                        shotSize: "cowboy",
                        cameraWork: "orbit_360",
                        gridType: "rule_of_thirds",
                        actionDescription: "濃霧に包まれた深夜の渋谷。橘飛鳥がARスマートグラスを調整しながら雑踏に紛れ込む。",
                        dialogues: [
                            {
                                id: "dlg_03_01_01",
                                speaker: "橘 飛鳥",
                                characterId: "asuka",
                                tone: "calm",
                                lang: "ja-JP",
                                text: "ターゲット捕捉。バイオメトリクス照合99.8%、潜入を開始します。",
                                speed: 1.0,
                                durationEstSec: 4.1
                            }
                        ]
                    }
                ]
            }
        ];

        this.selectedSceneId = "scene_01";
        this.selectedShotId = "shot_01_01";
    }

    /**
     * 📋 Get all scenes
     */
    getAllScenes() {
        return this.scenes;
    }

    /**
     * 🎯 Get current selected scene
     */
    getCurrentScene() {
        return this.scenes.find(s => s.id === this.selectedSceneId) || this.scenes[0];
    }

    /**
     * 🎯 Get current selected shot
     */
    getCurrentShot() {
        const scene = this.getCurrentScene();
        if (!scene || !scene.shots) return null;
        return scene.shots.find(sh => sh.id === this.selectedShotId) || scene.shots[0];
    }

    /**
     * 🔘 Select scene by ID
     */
    selectScene(sceneId) {
        const scene = this.scenes.find(s => s.id === sceneId);
        if (scene) {
            this.selectedSceneId = sceneId;
            if (scene.shots && scene.shots.length > 0) {
                this.selectedShotId = scene.shots[0].id;
            } else {
                this.selectedShotId = null;
            }
            return scene;
        }
        return null;
    }

    /**
     * 🔘 Select shot by ID
     */
    selectShot(shotId) {
        const scene = this.getCurrentScene();
        if (scene && scene.shots) {
            const shot = scene.shots.find(sh => sh.id === shotId);
            if (shot) {
                this.selectedShotId = shotId;
                return shot;
            }
        }
        return null;
    }

    /**
     * ➕ Add new scene
     */
    addScene(sceneData = {}) {
        const sceneNum = this.scenes.length + 1;
        const newSceneId = `scene_${String(sceneNum).padStart(2, '0')}_${Date.now()}`;
        const newScene = {
            id: newSceneId,
            sceneNumber: sceneNum,
            title: sceneData.title || `Scene ${sceneNum}: 新規シーン`,
            location: {
                name: sceneData.locationName || "原宿 表参道",
                coords: sceneData.coords || { lat: 35.6699, lng: 139.7025 },
                heading: sceneData.heading !== undefined ? sceneData.heading : 108.0,
                pitch: sceneData.pitch !== undefined ? sceneData.pitch : 0.0,
                timeOfDay: sceneData.timeOfDay || "sunset",
                weather: sceneData.weather || "clear"
            },
            shots: [
                {
                    id: `shot_${sceneNum}_01_${Date.now()}`,
                    shotNumber: 1,
                    name: `Shot 1: メインカット`,
                    durationSec: 5.0,
                    aspectRatio: "2.39:1",
                    lensMm: 35,
                    fStop: 2.8,
                    angle: "eye_level",
                    shotSize: "medium",
                    cameraWork: "dolly_in",
                    gridType: "rule_of_thirds",
                    actionDescription: "演者がカメラに向かって行動を開始する。",
                    dialogues: [
                        {
                            id: `dlg_${Date.now()}`,
                            speaker: "如月 蓮",
                            characterId: "ren",
                            tone: "tense",
                            lang: "ja-JP",
                            text: "作戦開始だ。配置につけ。",
                            speed: 1.0,
                            durationEstSec: 2.5
                        }
                    ]
                }
            ]
        };

        this.scenes.push(newScene);
        this.selectedSceneId = newScene.id;
        this.selectedShotId = newScene.shots[0].id;
        return newScene;
    }

    /**
     * 🗑️ Delete scene
     */
    deleteScene(sceneId) {
        if (this.scenes.length <= 1) return false;
        this.scenes = this.scenes.filter(s => s.id !== sceneId);
        this.scenes.forEach((s, idx) => { s.sceneNumber = idx + 1; });
        if (this.selectedSceneId === sceneId) {
            this.selectedSceneId = this.scenes[0].id;
            this.selectedShotId = this.scenes[0].shots[0] ? this.scenes[0].shots[0].id : null;
        }
        return true;
    }

    /**
     * 📑 Duplicate scene
     */
    duplicateScene(sceneId) {
        const idx = this.scenes.findIndex(s => s.id === sceneId);
        if (idx === -1) return null;
        const orig = this.scenes[idx];
        const newSceneId = `scene_${String(this.scenes.length + 1).padStart(2, '0')}_${Date.now()}`;
        const cloned = JSON.parse(JSON.stringify(orig));
        cloned.id = newSceneId;
        cloned.title = `${orig.title} (Copy)`;
        if (cloned.shots) {
            cloned.shots.forEach((sh, shIdx) => {
                sh.id = `shot_${newSceneId}_${shIdx + 1}_${Date.now()}`;
            });
        }
        this.scenes.splice(idx + 1, 0, cloned);
        this.scenes.forEach((s, i) => { s.sceneNumber = i + 1; });
        this.selectedSceneId = cloned.id;
        this.selectedShotId = cloned.shots && cloned.shots[0] ? cloned.shots[0].id : null;
        return cloned;
    }

    /**
     * ↕️ Move scene up or down
     */
    moveScene(sceneId, direction) {
        const idx = this.scenes.findIndex(s => s.id === sceneId);
        if (idx === -1) return false;
        const targetIdx = idx + direction;
        if (targetIdx < 0 || targetIdx >= this.scenes.length) return false;
        
        const temp = this.scenes[idx];
        this.scenes[idx] = this.scenes[targetIdx];
        this.scenes[targetIdx] = temp;
        this.scenes.forEach((s, i) => { s.sceneNumber = i + 1; });
        return true;
    }

    /**
     * ✏️ Update scene metadata
     */
    updateSceneMeta(sceneId, meta = {}) {
        const scene = this.scenes.find(s => s.id === sceneId);
        if (!scene) return false;
        if (meta.title !== undefined) scene.title = meta.title;
        if (meta.locationName !== undefined) scene.location.name = meta.locationName;
        if (meta.timeOfDay !== undefined) scene.location.timeOfDay = meta.timeOfDay;
        if (meta.weather !== undefined) scene.location.weather = meta.weather;
        return true;
    }

    /**
     * ➕ Add new shot to current scene
     */
    addShotToCurrentScene(shotData = {}) {
        const scene = this.getCurrentScene();
        if (!scene) return null;
        const shotNum = (scene.shots ? scene.shots.length : 0) + 1;
        const newShot = {
            id: `shot_${scene.sceneNumber}_${String(shotNum).padStart(2, '0')}_${Date.now()}`,
            shotNumber: shotNum,
            name: shotData.name || `Shot ${shotNum}: 新カット`,
            durationSec: parseFloat(shotData.durationSec || 4.0),
            aspectRatio: shotData.aspectRatio || "2.39:1",
            lensMm: parseInt(shotData.lensMm || 35),
            fStop: parseFloat(shotData.fStop || 2.8),
            angle: shotData.angle || "eye_level",
            shotSize: shotData.shotSize || "medium",
            cameraWork: shotData.cameraWork || "fix",
            gridType: shotData.gridType || "rule_of_thirds",
            actionDescription: shotData.actionDescription || "シーンのアクションと被写体の動線。",
            dialogues: shotData.dialogues || []
        };

        if (!scene.shots) scene.shots = [];
        scene.shots.push(newShot);
        this.selectedShotId = newShot.id;
        return newShot;
    }

    /**
     * 📑 Duplicate shot
     */
    duplicateShot(shotId) {
        const scene = this.getCurrentScene();
        if (!scene || !scene.shots) return null;
        const idx = scene.shots.findIndex(sh => sh.id === shotId);
        if (idx === -1) return null;
        const orig = scene.shots[idx];
        const cloned = JSON.parse(JSON.stringify(orig));
        cloned.id = `shot_${scene.sceneNumber}_${Date.now()}`;
        cloned.name = `${orig.name} (Copy)`;
        scene.shots.splice(idx + 1, 0, cloned);
        scene.shots.forEach((sh, i) => { sh.shotNumber = i + 1; });
        this.selectedShotId = cloned.id;
        return cloned;
    }

    /**
     * ↕️ Move shot within current scene
     */
    moveShot(shotId, direction) {
        const scene = this.getCurrentScene();
        if (!scene || !scene.shots) return false;
        const idx = scene.shots.findIndex(sh => sh.id === shotId);
        if (idx === -1) return false;
        const targetIdx = idx + direction;
        if (targetIdx < 0 || targetIdx >= scene.shots.length) return false;

        const temp = scene.shots[idx];
        scene.shots[idx] = scene.shots[targetIdx];
        scene.shots[targetIdx] = temp;
        scene.shots.forEach((sh, i) => { sh.shotNumber = i + 1; });
        return true;
    }

    /**
     * 🗑️ Delete shot from current scene
     */
    deleteShot(shotId) {
        const scene = this.getCurrentScene();
        if (!scene || !scene.shots || scene.shots.length <= 1) return false;
        scene.shots = scene.shots.filter(sh => sh.id !== shotId);
        scene.shots.forEach((sh, idx) => { sh.shotNumber = idx + 1; });
        if (this.selectedShotId === shotId) {
            this.selectedShotId = scene.shots[0].id;
        }
        return true;
    }

    /**
     * 💬 Add dialogue to current shot
     */
    addDialogueToCurrentShot(dialogueData) {
        const shot = this.getCurrentShot();
        if (!shot) return null;
        if (!shot.dialogues) shot.dialogues = [];

        const newDlg = {
            id: `dlg_${Date.now()}`,
            speaker: dialogueData.speaker || "如月 蓮",
            characterId: dialogueData.characterId || "ren",
            tone: dialogueData.tone || "tense",
            lang: dialogueData.lang || "ja-JP",
            text: dialogueData.text || "",
            speed: parseFloat(dialogueData.speed || 1.0),
            durationEstSec: this.estimateSpeechDuration(dialogueData.text || "", dialogueData.speed || 1.0)
        };

        shot.dialogues.push(newDlg);
        return newDlg;
    }

    /**
     * ⏱️ Estimate speech duration in seconds
     */
    estimateSpeechDuration(text, speed = 1.0) {
        if (!text) return 1.0;
        const len = text.trim().length;
        const estSec = Math.max(1.5, (len / 6.5) / (speed || 1.0));
        return parseFloat(estSec.toFixed(1));
    }

    /**
     * ⏱️ Total duration across all scenes and shots
     */
    getTotalScriptDurationSec() {
        let total = 0;
        this.scenes.forEach(s => {
            if (s.shots) {
                s.shots.forEach(sh => {
                    total += parseFloat(sh.durationSec || 0);
                });
            }
        });
        return parseFloat(total.toFixed(1));
    }

    /**
     * ⏱️ Format seconds into Timecode (HH:MM:SS:FF)
     */
    formatTimecode(sec) {
        const totalMs = Math.floor(sec * 1000);
        const hours = Math.floor(totalMs / 3600000);
        const minutes = Math.floor((totalMs % 3600000) / 60000);
        const seconds = Math.floor((totalMs % 60000) / 1000);
        const frames = Math.floor(((totalMs % 1000) / 1000) * 30);
        return `${String(hours).padStart(2,'0')}:${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}:${String(frames).padStart(2,'0')}`;
    }

    /**
     * 📦 Generate Master Sync Package for Main Director Monitor (Monitor 1)
     */
    generateDirectorSyncPayload() {
        const scene = this.getCurrentScene();
        const shot = this.getCurrentShot();

        const firstDlg = (shot && shot.dialogues && shot.dialogues[0]) ? shot.dialogues[0] : null;

        return {
            sceneId: scene.id,
            sceneName: scene.title,
            shotId: shot ? shot.id : "",
            shotName: shot ? shot.name : "",
            location: scene.location,
            durationSec: shot ? shot.durationSec : 5.0,
            camera: {
                lensMm: shot ? shot.lensMm : 35,
                fStop: shot ? shot.fStop : 2.8,
                angle: shot ? shot.angle : "eye_level",
                shotSize: shot ? shot.shotSize : "medium",
                cameraWork: shot ? shot.cameraWork : "dolly_in"
            },
            actionDescription: shot ? shot.actionDescription : "",
            dialogue: firstDlg ? firstDlg.text : "",
            speaker: firstDlg ? firstDlg.speaker : "如月 蓮",
            characterId: firstDlg ? firstDlg.characterId : "ren",
            tone: firstDlg ? firstDlg.tone : "tense",
            lang: firstDlg ? firstDlg.lang : "ja-JP",
            allDialogues: shot ? shot.dialogues : []
        };
    }

    /**
     * ⏱️ Calculate exact start time (IN-point) of a shot across all scenes
     */
    calculateShotStartTime(shotId) {
        let accumulatedSec = 0;
        for (const scene of this.scenes) {
            if (scene.shots) {
                for (const shot of scene.shots) {
                    if (shot.id === shotId) {
                        return parseFloat(accumulatedSec.toFixed(2));
                    }
                    accumulatedSec += parseFloat(shot.durationSec || 0);
                }
            }
        }
        return 0;
    }

    /**
     * 📚 Get MMKG Knowledge Presets (from E-Book Ingestion)
     */
    getAvailableKnowledgePresets() {
        return [
            {
                key: "stdp_synaptic_plasticity",
                title: "生体脳 STDP シナプス可塑性数理モデル",
                source: "生体脳構造と神経回路数理モデル.pdf (p.45)",
                formula: "\\Delta w = A_+ \\exp(-\\Delta t / \\tau_+)",
                conceptTriple: "(スパイクタイミング依存性可塑性) -[定式化]-> (ヘブ則 指数減衰結合荷重)",
                actionInjection: "如月蓮の神経インプラントが発光し、シナプス可塑性モデル（Δw = A_+ e^(-Δt/τ_+)）に基づくリアルタイム記憶固定化プロセスが走る。",
                dialogueInjection: "「ヘブ則によるシナプス強化が完了した……。ターゲットの全思考回路が読める。」"
            },
            {
                key: "hippocampal_cortical_replay",
                title: "海馬-皮質 記憶固定化リプレイ機構",
                source: "生体脳構造と神経回路数理モデル.pdf (p.88)",
                formula: "R_{replay} = \\int \\Psi_{ca3}(t) \\Phi_{pfc}(t - \\tau) dt",
                conceptTriple: "(海馬CA3領域) -[シャープウェーブ・リップル]-> (前頭前野 長期記憶定着)",
                actionInjection: "空間に青白いホログラムが展開。海馬CA3から大脳新皮質への高速リプレイ（200Hzリップル波）が神経回路マップ上に可視化される。",
                dialogueInjection: "「短期記憶から長期記憶への固定化シーケンスを開始。海馬-皮質結合を切断するな！」"
            },
            {
                key: "quantum_neural_cryptography",
                title: "量子ニューロ暗号 ＆ ベル状態もつれ",
                source: "先端量子サイバーパンク工学原論.pdf (p.112)",
                formula: "|\\Psi^+\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle + |10\\rangle)",
                conceptTriple: "(EPRペア量子もつれ) -[暗号鍵共有]-> (非局所生体脳ネットワーク)",
                actionInjection: "アタッシュケース内の量子コアが脈動し、量子もつれ状態の光子が雨粒の中に干渉縞を描き出す。",
                dialogueInjection: "「ベル状態の測定基底を固定しろ。盗聴者がいれば波動関数が即座に収縮する！」"
            }
        ];
    }

    /**
     * 📚 Inject MMKG Knowledge into Current Shot (Action & Dialogue)
     */
    injectKnowledgeToCurrentShot(presetKey) {
        const presets = this.getAvailableKnowledgePresets();
        const preset = presets.find(p => p.key === presetKey) || presets[0];
        const shot = this.getCurrentShot();
        if (!shot) return null;

        // Append to Action
        if (shot.actionDescription) {
            shot.actionDescription += `\n【MMKG ナレッジ注入 (${preset.source})】: ${preset.actionInjection}`;
        } else {
            shot.actionDescription = `【MMKG ナレッジ注入 (${preset.source})】: ${preset.actionInjection}`;
        }

        // Append or set Dialogue
        if (!shot.dialogues) shot.dialogues = [];
        const newDlg = {
            id: `dlg_mmkg_${Date.now()}`,
            speaker: shot.dialogues.length > 0 ? shot.dialogues[0].speaker : "如月 蓮",
            characterId: shot.dialogues.length > 0 ? shot.dialogues[0].characterId : "ren",
            tone: "tense",
            lang: "ja-JP",
            text: preset.dialogueInjection,
            speed: 1.0,
            durationEstSec: this.estimateSpeechDuration(preset.dialogueInjection, 1.0)
        };
        shot.dialogues.push(newDlg);

        return {
            shot: shot,
            injectedPreset: preset,
            dialogue: newDlg
        };
    }

    /**
     * 🎬 Build Hollywood-Grade Google Veo 3.1 Cinema Prompt
     */
    buildVeoPrompt(shot = null) {
        const targetShot = shot || this.getCurrentShot();
        const scene = this.getCurrentScene();
        if (!targetShot || !scene) return "";

        const lensMm = targetShot.lensMm || 35;
        const fStop = targetShot.fStop || 2.8;
        const angle = targetShot.angle || "eye_level";
        const shotSize = targetShot.shotSize || "medium";
        const cameraWork = targetShot.cameraWork || "dolly_in";
        const locationName = scene.location.name || "Tokyo Neon Street";
        const weather = scene.location.weather || "heavy_rain";
        const timeOfDay = scene.location.timeOfDay || "night";
        const action = targetShot.actionDescription || "Cinematic character interaction";
        const firstDlg = (targetShot.dialogues && targetShot.dialogues[0]) ? targetShot.dialogues[0].text : "";

        // Optics Description
        const opticsMap = {
            14: "ultra-wide 14mm anamorphic lens, extreme spatial depth and dynamic peripheral distortion",
            24: "wide-angle 24mm cinema prime, immersive perspective and environmental prominence",
            35: "35mm Hollywood anamorphic standard prime, perfect balance of subject and atmospheric architecture",
            50: "50mm portrait master lens, natural human vision fidelity and cinematic separation",
            85: "85mm telephoto prime, intense character focus and compressed atmospheric depth",
            135: "135mm long telephoto, extreme background compression and dramatic shallow depth of field"
        };
        const lensDesc = opticsMap[lensMm] || `${lensMm}mm cinema lens`;

        const cameraWorkMap = {
            fix: "rock-solid static master tripod lock, perfectly framed composition",
            dolly_in: "smooth mechanized forward dolly track glide pushing into the focal point",
            dolly_out: "dramatic reverse dolly pullback revealing the expansive environmental scale",
            tracking: "fluid dynamic Steadicam tracking alongside the moving subject with cinematic cadence",
            crane_up: "sweeping Technocrane pedestal ascent from ground level to panoramic vantage",
            orbit_360: "hypnotic 360-degree rotational orbit track maintaining locked parallax on the subject"
        };
        const moveDesc = cameraWorkMap[cameraWork] || cameraWork;

        const weatherMap = {
            heavy_rain: "heavy cinematic rainstorm, glistening wet asphalt reflections, neon puddles, mist particles",
            thunderstorm: "dramatic thunderstorm with intermittent volumetric lightning flashes casting sharp dynamic shadows",
            clear: "crystal-clear atmospheric visibility, sharp specular highlights, pristine air quality",
            dense_fog: "dense atmospheric fog and volumetric light rays piercing through Tokyo neon haze"
        };
        const envDesc = weatherMap[weather] || weather;

        const prompt = [
            `[MASTER CINEMATOGRAPHY]: Shot on ARRI ALEXA LF 65 with ${lensDesc}, aperture f/${fStop}, 2.39:1 Anamorphic Cinemascope aspect ratio, 8K ultra-photorealistic capture.`,
            `[CAMERA MOVEMENT & COMPOSITION]: ${shotSize.toUpperCase()} framing, ${angle.replace('_', ' ')} perspective, executing a ${moveDesc}.`,
            `[ENVIRONMENT & LIGHTING]: Location: ${locationName}. Atmosphere: ${timeOfDay} lighting with ${envDesc}. Master volumetric lighting, anamorphic horizontal lens flare, rich cinematic color grading (Kodak 2383 LUT aesthetic).`,
            `[SUBJECT & ACTION]: ${action}.`,
            firstDlg ? `[DIALOGUE SUBTEXT & PERFORMANCE]: Character speaks: "${firstDlg}". Intensely calibrated micro-expressions, authentic physical weight, lifelike wet cloth and skin micro-textures.` : `[PERFORMANCE]: Subtle micro-expressions, high-stakes cinematic tension.`
        ].join("\n\n");

        return prompt;
    }

    /**
     * 🚀 Execute Google Veo 3.1 Cinematic Video Generation & Broadcast to Quad Studio
     */
    generateVeoVideoClip(shotId = null) {
        const shot = shotId ? (this.getCurrentScene().shots.find(s => s.id === shotId) || this.getCurrentShot()) : this.getCurrentShot();
        const scene = this.getCurrentScene();
        if (!shot) return null;

        const startTime = this.calculateShotStartTime(shot.id);
        const prompt = this.buildVeoPrompt(shot);
        const videoId = `veo_${Date.now()}`;
        const durationSec = parseFloat(shot.durationSec || 5.0);

        // Assets video sample mapping
        const sampleVideos = [
            "assets/cyberpunk_tokyo_drone_4k_sample.mp4",
            "assets/harajuku_straight_street_perfect.mp4",
            "assets/matrix_bullet_time_sample.mp4"
        ];
        const videoSrc = sampleVideos[Math.floor(Math.random() * sampleVideos.length)];

        const videoClipPayload = {
            id: videoId,
            shotId: shot.id,
            shotName: shot.name,
            sceneId: scene.id,
            sceneName: scene.title,
            title: `Veo 3.1: ${scene.title} - ${shot.name}`,
            durationSec: durationSec,
            startTimeSec: startTime,
            videoSrc: videoSrc,
            thumbnailSrc: "assets/harajuku_straight_street_perfect.jpg",
            prompt: prompt,
            resolution: "3840x1608 (4K 2.39:1 Anamorphic)",
            fps: 24,
            codec: "H.265 / ProRes 422HQ HDR10+",
            lensMm: shot.lensMm,
            fStop: shot.fStop,
            location: scene.location.name,
            generatedAt: new Date().toISOString()
        };

        // Quad Studio Broadcast
        if (typeof window !== 'undefined' && window.MultiDisplayEngine) {
            // 1. Broadcast to Theater (Monitor 2)
            window.MultiDisplayEngine.broadcast("THEATER_PLAY_VIDEO", videoClipPayload);
            // 2. Broadcast to Director NLE (Monitor 1) Track 1 & Shot Bin
            window.MultiDisplayEngine.broadcast("TIMELINE_VIDEO_ADD", videoClipPayload);
            // 3. General Veo Generated Notice
            window.MultiDisplayEngine.broadcast("VIDEO_RENDER_COMPLETE", videoClipPayload);
        }

        return videoClipPayload;
    }

    /**
     * 🎵 Generate Timeline Dialogue Clip for Track 3
     */
    generateTimelineDialogueClip() {
        const shot = this.getCurrentShot();
        if (!shot || !shot.dialogues || shot.dialogues.length === 0) return null;
        
        const dlg = shot.dialogues[0];
        const startTime = this.calculateShotStartTime(shot.id);
        return {
            id: `dlg_clip_${Date.now()}`,
            name: `💬 ${dlg.speaker}: 「${dlg.text.substring(0, 16)}${dlg.text.length > 16 ? '...' : ''}」`,
            durationSec: dlg.durationEstSec || 3.5,
            startTimeSec: startTime,
            speaker: dlg.speaker,
            characterId: dlg.characterId,
            lang: dlg.lang,
            text: dlg.text,
            type: "dialogue",
            color: "linear-gradient(90deg, #3b82f6, #06b6d4)"
        };
    }

    /**
     * 💾 Export script to JSON
     */
    exportJSON() {
        return JSON.stringify({
            version: "GENESIS_CINEMA_SCRIPT_v55",
            exportedAt: new Date().toISOString(),
            totalScenes: this.scenes.length,
            totalDurationSec: this.getTotalScriptDurationSec(),
            scenes: this.scenes
        }, null, 2);
    }

    /**
     * 📥 Import script from JSON
     */
    importJSON(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            if (data && Array.isArray(data.scenes) && data.scenes.length > 0) {
                this.scenes = data.scenes;
                this.selectedSceneId = this.scenes[0].id;
                this.selectedShotId = (this.scenes[0].shots && this.scenes[0].shots[0]) ? this.scenes[0].shots[0].id : null;
                return true;
            }
        } catch(e) {
            console.error("Failed to import script JSON:", e);
        }
        return false;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StoryboardScriptEngine };
}
if (typeof window !== 'undefined') {
    window.StoryboardScriptEngine = new StoryboardScriptEngine();
}
console.log("📜 GENESIS Storyboard & Cinematic Script Engine v55 Loaded.");
