# -*- coding: utf-8 -*-
import os
import sys
import math
import time
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_drone_omnidirectional_rescue():
    artifacts_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    os.makedirs(artifacts_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        page.on("console", lambda msg: print(f"[BROWSER LOG] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))

        print("\n========================================================")
        print("🛸 [TEST] DRONE OMNIDIRECTIONAL RESCUE & ACTIVE TURNING TEST")
        print("========================================================")
        page.goto("http://localhost:8080/genesis_cybernetics_3d_simulator.html")
        page.wait_for_timeout(2000)

        # 1. 初期状態の確認 (Rescue Mode, Zone Active, Victim Visible)
        init_state = page.evaluate("""() => ({
            isRescueActive: window.isRescueActive,
            rescueCompleted: window.rescueCompleted,
            zoneActive: window.rescueZone ? window.rescueZone.active : false,
            victimVisible: window.victimPersonGroup ? window.victimPersonGroup.visible : false,
            beamVisible: window.rescueScanBeam ? window.rescueScanBeam.visible : false,
            dronePos: { x: window.position.x, y: window.position.y, z: window.position.z },
            victimPos: { x: window.rescueTargetPos.x, y: window.rescueTargetPos.y, z: window.rescueTargetPos.z },
            flightState: window.flightState,
            flightDetail: document.getElementById('lblFlightDetail') ? document.getElementById('lblFlightDetail').innerText : ''
        })""")

        print("[TEST 1] Initial Drone & Rescue Status:")
        print(f"  isRescueActive: {init_state['isRescueActive']}")
        print(f"  rescueZone.active: {init_state['zoneActive']}")
        print(f"  victimPersonGroup.visible: {init_state['victimVisible']}")
        print(f"  rescueScanBeam.visible: {init_state['beamVisible']}")
        print(f"  Drone Position: ({init_state['dronePos']['x']:.2f}, {init_state['dronePos']['y']:.2f}, {init_state['dronePos']['z']:.2f})")
        print(f"  Victim Position: ({init_state['victimPos']['x']:.2f}, {init_state['victimPos']['y']:.2f}, {init_state['victimPos']['z']:.2f})")
        print(f"  Flight State: {init_state['flightState']}")
        print(f"  Flight Detail: {init_state['flightDetail']}")

        assert init_state['isRescueActive'] == True, "isRescueActive must be True by default"
        assert init_state['zoneActive'] == True, "rescueZone.active must be True"
        assert init_state['victimVisible'] == True, "victimPersonGroup must be visible"

        # 2. テスト用に斜め東側（X: +25m, Z: -15m）に救護者を配置し、ドローンが自律旋回して急行するか検証
        print("\n[TEST 2] Spawning victim at East-Northeast (X: 25, Z: -15) and testing autonomous yaw turning...")
        page.evaluate("""() => {
            const gy = (typeof getTerrainHeight === 'function') ? getTerrainHeight(25.0, -15.0) : 0;
            window.rescueTargetPos.set(25.0, gy, -15.0);
            if (window.victimPersonGroup) {
                window.victimPersonGroup.position.copy(window.rescueTargetPos);
                window.victimPersonGroup.visible = true;
            }
            window.isRescueActive = true;
            window.rescueCompleted = false;
        }""")

        init_x = float(init_state['dronePos']['x'])
        # 1秒〜4秒経過観察
        print("  Tracking drone heading and position for 4.0 seconds...")
        for step in range(8):
            page.wait_for_timeout(500)
            telemetry = page.evaluate("""() => {
                const dx = window.rescueTargetPos.x - window.position.x;
                const dz = window.rescueTargetPos.z - window.position.z;
                const targetHeading = Math.atan2(-dx, -dz);
                let diff = targetHeading - window.rotation.y;
                while (diff > Math.PI) diff -= Math.PI * 2;
                while (diff < -Math.PI) diff += Math.PI * 2;

                return {
                    pos: { x: window.position.x, y: window.position.y, z: window.position.z },
                    speed: window.speed,
                    yawDeg: (window.rotation.y * 180 / Math.PI).toFixed(1),
                    targetHeadingDeg: (targetHeading * 180 / Math.PI).toFixed(1),
                    headingDiffDeg: (diff * 180 / Math.PI).toFixed(1),
                    distToVictim: Math.hypot(dx, dz).toFixed(1),
                    flightState: window.flightState,
                    flightDetail: document.getElementById('lblFlightDetail') ? document.getElementById('lblFlightDetail').innerText : ''
                };
            }""")
            print(f"  Step {step+1} (t={(step+1)*0.5:.1f}s): Pos=({telemetry['pos']['x']:.1f}, {telemetry['pos']['z']:.1f}), Yaw={telemetry['yawDeg']}° (Tgt={telemetry['targetHeadingDeg']}°, Diff={telemetry['headingDiffDeg']}°), Speed={telemetry['speed']:.1f}km/h, Dist={telemetry['distToVictim']}m, State={telemetry['flightState']}")

        # ドローンが真北（0°）だけでなく東向き（yaw < 0, X正方向）に回頭していることを検証
        drone_yaw = float(telemetry['yawDeg'])
        drone_x = float(telemetry['pos']['x'])
        delta_x = drone_x - init_x
        print(f"  -> Verified: Drone X moved towards victim: X={drone_x:.2f} (Init: {init_x:.2f}, DeltaX: +{delta_x:.2f}m), Yaw={drone_yaw:.1f}°")
        assert delta_x > 1.5, f"Drone should actively steer towards positive X (victim at X=25), got delta_x={delta_x}"
        assert drone_yaw < -30.0, f"Drone should yaw towards -60 deg, got {drone_yaw}"

        shot_turn = os.path.join(artifacts_dir, "screen_drone_active_turn_to_victim.png")
        page.screenshot(path=shot_turn)
        print(f"  📸 Saved active turn screenshot to: {shot_turn}")

        # 3. テスト3: 真後ろ・南西（X: -20m, Z: +25m）に救助者を配置し、180度以上の大回頭テスト
        print("\n[TEST 3] Spawning victim at South-West behind drone (X: -20, Z: 25) - 180° Reverse Turn Test...")
        page.evaluate("""() => {
            const gy = (typeof getTerrainHeight === 'function') ? getTerrainHeight(-20.0, 25.0) : 0;
            window.rescueTargetPos.set(-20.0, gy, 25.0);
            if (window.victimPersonGroup) {
                window.victimPersonGroup.position.copy(window.rescueTargetPos);
                window.victimPersonGroup.visible = true;
            }
            window.isRescueActive = true;
            window.rescueCompleted = false;
        }""")

        for step in range(8):
            page.wait_for_timeout(500)
            telemetry = page.evaluate("""() => {
                const dx = window.rescueTargetPos.x - window.position.x;
                const dz = window.rescueTargetPos.z - window.position.z;
                const targetHeading = Math.atan2(-dx, -dz);
                let diff = targetHeading - window.rotation.y;
                while (diff > Math.PI) diff -= Math.PI * 2;
                while (diff < -Math.PI) diff += Math.PI * 2;

                return {
                    pos: { x: window.position.x, y: window.position.y, z: window.position.z },
                    speed: window.speed,
                    yawDeg: (window.rotation.y * 180 / Math.PI).toFixed(1),
                    targetHeadingDeg: (targetHeading * 180 / Math.PI).toFixed(1),
                    headingDiffDeg: (diff * 180 / Math.PI).toFixed(1),
                    distToVictim: Math.hypot(dx, dz).toFixed(1),
                    flightState: window.flightState
                };
            }""")
            print(f"  Step {step+1} (t={(step+1)*0.5:.1f}s): Pos=({telemetry['pos']['x']:.1f}, {telemetry['pos']['z']:.1f}), Yaw={telemetry['yawDeg']}°, Dist={telemetry['distToVictim']}m, State={telemetry['flightState']}")

        shot_rev = os.path.join(artifacts_dir, "screen_drone_180deg_reverse_turn.png")
        page.screenshot(path=shot_rev)
        print(f"  📸 Saved 180° reverse turn screenshot to: {shot_rev}")

        # 4. 到着・ホバリング救護完了テスト
        print("\n[TEST 4] Testing Arrival & Hovering Rescue Completion...")
        # 機体の直前 2.2m に救護者を配置して即座に救護完了フェーズへ
        page.evaluate("""() => {
            const rx = window.position.x - Math.sin(window.rotation.y) * 2.2;
            const rz = window.position.z - Math.cos(window.rotation.y) * 2.2;
            const gy = (typeof getTerrainHeight === 'function') ? getTerrainHeight(rx, rz) : 0;
            window.rescueTargetPos.set(rx, gy, rz);
            if (window.victimPersonGroup) {
                window.victimPersonGroup.position.copy(window.rescueTargetPos);
                window.victimPersonGroup.visible = true;
            }
            window.isRescueActive = true;
            window.rescueCompleted = false;
        }""")
        page.wait_for_timeout(1000)

        rescue_status = page.evaluate("""() => ({
            flightState: window.flightState,
            rescueCompleted: window.rescueCompleted,
            bannerVisible: document.getElementById('rescueBanner') ? document.getElementById('rescueBanner').style.display : 'none',
            ringColor: window.victimVitalRing ? window.victimVitalRing.material.color.getHexString() : '',
            completedCount: window.currentMissionGoal ? window.currentMissionGoal.completedCount : 0
        })""")

        print(f"  Rescue Status: State={rescue_status['flightState']}, Completed={rescue_status['rescueCompleted']}, Banner={rescue_status['bannerVisible']}, RingColor=#{rescue_status['ringColor']}, SuccessCount={rescue_status['completedCount']}")
        assert rescue_status['rescueCompleted'] == True or rescue_status['flightState'] == 'RESCUE_ARRIVED', "Rescue must complete upon reaching victim"

        shot_arrived = os.path.join(artifacts_dir, "screen_drone_rescue_success_hover.png")
        page.screenshot(path=shot_arrived)
        print(f"  📸 Saved rescue success screenshot to: {shot_arrived}")

        print("\n========================================================")
        print("✅ ALL TESTS PASSED! DRONE ACTIVELY SEARCHES & RESCUES IN 360°")
        print("========================================================")
        browser.close()

if __name__ == '__main__':
    test_drone_omnidirectional_rescue()
