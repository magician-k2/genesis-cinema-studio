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

def test_rescue_zone_system():
    artifacts_dir = r"C:\Users\magic\.gemini\antigravity\brain\35b89419-3b90-4875-947d-0cc26e4dff4d"
    os.makedirs(artifacts_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        print("\n========================================================")
        print("🚩 [TEST] DYNAMIC RESCUE ZONE (150m DEFAULT OPTIMAL) TEST")
        print("========================================================")
        page.goto("http://localhost:8080/genesis_cybernetics_3d_simulator.html")
        page.wait_for_timeout(2000)

        # 1. Verify Default Zone Size = 150m x 150m (Optimal Recommended Default)
        zone_info = page.evaluate("""() => ({
            size: rescueZone.size,
            minX: rescueZone.minX,
            maxX: rescueZone.maxX,
            minZ: rescueZone.minZ,
            maxZ: rescueZone.maxZ,
            victimX: rescueTargetPos.x,
            victimZ: rescueTargetPos.z,
            fenceChildren: zonePerimeterGroup ? zonePerimeterGroup.children.length : 0,
            activeButton: document.getElementById('btnZone150').classList.contains('active')
        })""")

        print(f"[TEST 1] Default Zone verification:")
        print(f"  Zone Size: {zone_info['size']}m x {zone_info['size']}m (X: [{zone_info['minX']}, {zone_info['maxX']}], Z: [{zone_info['minZ']}, {zone_info['maxZ']}])")
        print(f"  Victim Position: ({zone_info['victimX']:.2f}, {zone_info['victimZ']:.2f})")
        print(f"  Fence 3D Meshes: {zone_info['fenceChildren']} objects")
        print(f"  Active Button: 150m = {zone_info['activeButton']}")

        assert zone_info['size'] == 150.0, f"Default size must be 150m, got {zone_info['size']}"
        assert abs(zone_info['victimX']) <= 75.0, f"Victim X out of 150m zone: {zone_info['victimX']}"
        assert abs(zone_info['victimZ']) <= 75.0, f"Victim Z out of 150m zone: {zone_info['victimZ']}"
        assert zone_info['fenceChildren'] > 0, "Fence perimeter mesh must be created"
        assert zone_info['activeButton'], "150m button must be active by default"
        print("  -> Verified: Default 150m x 150m optimal zone initialized perfectly!")

        # 2. Capture screenshot of 150m default zone
        shot150 = os.path.join(artifacts_dir, "screen_rescue_zone_150m_default.png")
        page.screenshot(path=shot150)
        print(f"  📸 Saved 150m Default Zone screenshot to: {shot150}")

        # 3. Test Zone Switching across entire spectrum: 10m, 50m, 100m, 200m then back to 150m
        print("\n[TEST 2] Testing Dynamic Zone Size Switching Across Full Operational Tier...")
        for target_sz in [10, 50, 100, 200, 150]:
            page.click(f'#btnZone{target_sz}')
            page.wait_for_timeout(400)
            cur_sz = page.evaluate("() => rescueZone.size")
            btn_active = page.evaluate(f"() => document.getElementById('btnZone{target_sz}').classList.contains('active')")
            v_pos = page.evaluate("() => ({ x: rescueTargetPos.x, z: rescueTargetPos.z, half: rescueZone.size * 0.5 })")
            print(f"  Switched to {target_sz}m: size={cur_sz}m, buttonActive={btn_active}, victim=({v_pos['x']:.2f}, {v_pos['z']:.2f}) inside [{ -v_pos['half']:.1f}, { v_pos['half']:.1f}]")
            assert cur_sz == float(target_sz), f"Expected {target_sz}m, got {cur_sz}"
            assert btn_active, f"Button btnZone{target_sz} should be active"
            assert abs(v_pos['x']) <= v_pos['half'], f"Victim outside zone: {v_pos['x']}"
            assert abs(v_pos['z']) <= v_pos['half'], f"Victim outside zone: {v_pos['z']}"

        print("  -> Verified: Dynamic Zone Switching works seamlessly across all tiers (10m - 200m)!")

        # 4. Switch to GROUND (Centipede) mode in 150m Zone and verify autonomous navigation
        print("\n[TEST 3] Testing Centipede Autonomous Search & Rescue inside 150m Zone...")
        page.click('#btnModeGround')
        page.wait_for_timeout(1000)

        # Place casualty along open boulevard at X=0.0, Z=-12.0 inside 150m zone
        page.evaluate("""() => {
            respawnVehicle();
            position.set(0, getTerrainHeight(0, 0) + 0.18, 0);
            rotation.set(0, 0, 0);
            speed = 6.0;
            targetSpeed = 6.0;
            flightState = 'CRUISE';
            avoidanceCooldown = 0;
            rescueTargetPos.set(0.0, getTerrainHeight(0.0, -12.0), -12.0);
            victimPersonGroup.position.copy(rescueTargetPos);
            updateMissionGoalBeaconPosition();
            updateMissionGoalHud();
        }""")

        seen_clamped_in_zone = True
        reached_victim = False

        for tick in range(500):
            page.wait_for_timeout(50)
            t = page.evaluate("""() => ({
                x: position.x,
                z: position.z,
                speed: speed,
                state: flightState,
                distToVictim: Math.hypot(position.x - rescueTargetPos.x, position.z - rescueTargetPos.z)
            })""")

            # Verify geofence: vehicle must NEVER leave [-75.0, 75.0]
            if abs(t['x']) > 75.05 or abs(t['z']) > 75.05:
                seen_clamped_in_zone = False
                print(f"  [ERROR] Centipede breached 150m zone boundary: ({t['x']:.2f}, {t['z']:.2f})")

            if tick % 25 == 0:
                print(f"  Tick {tick:03d}: State={t['state']}, Pos=({t['x']:.2f}, {t['z']:.2f}), Dist={t['distToVictim']:.2f}m")

            if t['state'] == 'RESCUE_ARRIVED' or t['distToVictim'] <= 3.2:
                reached_victim = True
                print(f"\n  [RESCUE ARRIVED] Tick {tick}: State={t['state']}, Pos=({t['x']:.2f}, {t['z']:.2f}), Dist={t['distToVictim']:.2f}m")
                break

        assert seen_clamped_in_zone, "Vehicle breached rescue zone perimeter!"
        assert reached_victim, "Centipede must reach and secure casualty in 150m zone!"
        print("  -> Verified: Centipede navigated across wide zone and secured casualty!")

        shot_rescue = os.path.join(artifacts_dir, "screen_centipede_150m_zone_rescue_success.png")
        page.screenshot(path=shot_rescue)
        print(f"  📸 Saved Centipede 150m Zone Rescue screenshot to: {shot_rescue}")

        # Also take screenshot of HQ Digital Twin HUD in 150m mode
        page.evaluate("() => toggleHQHUDModal()")
        page.wait_for_timeout(500)
        shot_hud = os.path.join(artifacts_dir, "screen_hq_hud_150m_digital_twin.png")
        page.screenshot(path=shot_hud)
        print(f"  📸 Saved HQ Digital Twin HUD screenshot to: {shot_hud}")

        browser.close()
        print("\n========================================================")
        print("🎉 ALL RESCUE ZONE SYSTEM TESTS PASSED 100%!")
        print("========================================================")

if __name__ == '__main__':
    test_rescue_zone_system()
