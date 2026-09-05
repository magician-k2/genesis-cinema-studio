/**
 * 🎭 GENESIS Cinema Studio: Character Kinematics & Acting Profile Engine
 */
class CharacterMasterEngine {
    constructor() {
        this.currentAngle = "front";
        this.currentCostume = "noir_suit";
        this.strideLength = 75; // cm (歩幅)
        this.walkSpeed = 4.2;   // km/h (歩行速度)
        this.walkStyle = "confident"; // "confident", "sneaking", "running", "casual"
        this.emotionIntensity = 85;   // 0 - 100%
        this.actingTone = "tense";    // "tense", "whisper", "angry", "calm"

        this.costumes = {
            "noir_suit": {
                name: "ノワールスーツ",
                angles: {
                    "front": { icon: "fa-user-tie", label: "正面", pose: "直立・鋭い眼光" },
                    "back": { icon: "fa-user-secret", label: "背面", pose: "背中・襟立て" },
                    "left": { icon: "fa-person", label: "左側面", pose: "左プロファイル" },
                    "right": { icon: "fa-person", label: "右側面", pose: "右プロファイル" }
                }
            },
            "casual_jacket": {
                name: "レザージャケット",
                angles: {
                    "front": { icon: "fa-user", label: "正面", pose: "私服・リラックス" },
                    "back": { icon: "fa-user-secret", label: "背面", pose: "ジャケット背面" },
                    "left": { icon: "fa-person-walking", label: "左側面", pose: "歩行姿勢" },
                    "right": { icon: "fa-person-walking", label: "右側面", pose: "歩行姿勢" }
                }
            },
            "tactical_gear": {
                name: "タクティカルギア",
                angles: {
                    "front": { icon: "fa-user-shield", label: "正面", pose: "戦闘準備" },
                    "back": { icon: "fa-shield-halved", label: "背面", pose: "ホルスター背面" },
                    "left": { icon: "fa-gun", label: "左側面", pose: "警戒構え" },
                    "right": { icon: "fa-gun", label: "右側面", pose: "警戒構え" }
                }
            }
        };
    }

    setKinematics(stride, speed, style) {
        this.strideLength = parseInt(stride);
        this.walkSpeed = parseFloat(speed);
        this.walkStyle = style;
        return { stride: this.strideLength, speed: this.walkSpeed, style: this.walkStyle };
    }

    setActing(emotion, tone) {
        this.emotionIntensity = parseInt(emotion);
        this.actingTone = tone;
        return { emotion: this.emotionIntensity, tone: this.actingTone };
    }

    setAngle(angle) {
        this.currentAngle = angle;
        return this.costumes[this.currentCostume].angles[angle];
    }

    setCostume(costumeKey) {
        if (this.costumes[costumeKey]) {
            this.currentCostume = costumeKey;
        }
        return {
            costumeName: this.costumes[this.currentCostume].name,
            angleData: this.costumes[this.currentCostume].angles[this.currentAngle]
        };
    }
}

window.CharacterMasterEngine = new CharacterMasterEngine();
