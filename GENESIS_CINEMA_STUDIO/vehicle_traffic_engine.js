/**
 * 🚕 GENESIS Vehicle & Traffic Simulation Engine (vehicle_traffic_engine.js - v45)
 * Photorealistic Tokyo Vehicles: JPN TAXI (1.75m), City Bus (3.2m), Black Sedan (1.45m), Patrol Car
 */

class VehicleTrafficEngine {
    constructor() {
        this.enabled = true;
        this.selectedVehicle = "jpn_taxi"; // jpn_taxi, city_bus, black_sedan, patrol_car
        this.vehicleCount = 1; // 0, 1, 2, 3
        this.lanePosition = "road_middle"; // road_foreground, road_middle, road_background
        this.motionState = "cruising"; // cruising, stopped, accelerating
        
        this.vehicles = {
            jpn_taxi: {
                id: "jpn_taxi",
                nameJa: "🚕 ジャパンタクシー (JPN TAXI)",
                nameEn: "iconic deep indigo-black Toyota JPN TAXI cab with glowing roof light",
                heightM: 1.75,
                widthM: 1.70,
                lengthM: 4.40,
                spriteUrl: "assets/extra_taxi.png",
                colorTag: "#fde047",
                descJa: "全高1.75mのトールワゴンタクシー。行灯の淡い点灯と滑らかな走行。"
            },
            city_bus: {
                id: "city_bus",
                nameJa: "🚌 都営路線バス (Tokyo City Bus)",
                nameEn: "large green and white Tokyo Metropolitan transit bus with illuminated route LED display",
                heightM: 3.20,
                widthM: 2.50,
                lengthM: 10.50,
                spriteUrl: "assets/extra_taxi.png", // Base vehicle texture fallback
                colorTag: "#10b981",
                descJa: "全高3.2mの大型ノンステップ路線バス。圧倒的な重量感とスケール対比。"
            },
            black_sedan: {
                id: "black_sedan",
                nameJa: "🚘 黒塗り高級セダン (VIP Sedan)",
                nameEn: "sleek glossy black executive luxury sedan with tinted privacy windows",
                heightM: 1.45,
                widthM: 1.88,
                lengthM: 4.95,
                spriteUrl: "assets/extra_taxi.png",
                colorTag: "#38bdf8",
                descJa: "漆黒の高級セダン。光沢ボディへの街灯反射とサスペンス感。"
            },
            patrol_car: {
                id: "patrol_car",
                nameJa: "🚓 警視庁 パトカー (Police Cruiser)",
                nameEn: "Tokyo Metropolitan Police black-and-white Crown patrol cruiser with flashing red LED lightbar",
                heightM: 1.60,
                widthM: 1.80,
                lengthM: 4.90,
                spriteUrl: "assets/extra_taxi.png",
                colorTag: "#ef4444",
                descJa: "白黒ツートンのパトカー。ルーフの赤色灯反射による緊迫した事件性。"
            }
        };
    }

    setVehicleType(typeKey) {
        if (this.vehicles[typeKey]) {
            this.selectedVehicle = typeKey;
        }
        return this.getVehicleStatus();
    }

    setVehicleCount(count) {
        this.vehicleCount = Math.max(0, Math.min(4, parseInt(count)));
        this.enabled = (this.vehicleCount > 0);
        return this.getVehicleStatus();
    }

    setMotionState(state) {
        this.motionState = state;
        return this.getVehicleStatus();
    }

    getVehicleStatus() {
        const veh = this.vehicles[this.selectedVehicle] || this.vehicles.jpn_taxi;
        return {
            enabled: this.enabled && (this.vehicleCount > 0),
            count: this.vehicleCount,
            vehicleKey: this.selectedVehicle,
            vehicle: veh,
            motionState: this.motionState,
            heightM: veh.heightM,
            widthM: veh.widthM,
            lengthM: veh.lengthM
        };
    }

    generatePromptDescription(environmentCategory = "surface") {
        if (!this.enabled || this.vehicleCount === 0 || environmentCategory === "underground") {
            if (environmentCategory === "underground") {
                return "Vehicular Traffic: None (Subterranean pedestrian concourse isolated from street vehicle traffic).";
            }
            return "Vehicular Traffic: Clear open street without distracting vehicles in immediate foreground.";
        }

        const veh = this.vehicles[this.selectedVehicle] || this.vehicles.jpn_taxi;
        let motionDesc = "cruising steadily along the asphalt avenue at 35km/h with warm headlight beams reflecting on the road surface";
        if (this.motionState === "stopped") motionDesc = "temporarily idling at the intersection crosswalk with red taillight reflections";
        else if (this.motionState === "accelerating") motionDesc = "accelerating past the camera creating realistic cinematic motion blur";

        let countDesc = `A single ${veh.nameEn} (height ${veh.heightM}m, length ${veh.lengthM}m)`;
        if (this.vehicleCount > 1) {
            countDesc = `${this.vehicleCount} vehicles including ${veh.nameEn} (height ${veh.heightM}m)`;
        }

        return `Vehicles & Urban Traffic: ${countDesc} ${motionDesc}, establishing sharp authentic scale contrast against the pedestrians and towering architecture.`;
    }
}

window.VehicleTrafficEngine = new VehicleTrafficEngine();
console.log("GENESIS Vehicle & Traffic Simulation Engine v45 Loaded.");
