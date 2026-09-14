# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import sys

def test_endpoints():
    print("========================================")
    print("=== GENESIS PHASE 4 E2E VERIFICATION ===")
    print("========================================")
    
    # 1. Test Static & HTML Organs
    endpoints = [
        ("/mobile_antigravity.html", 200),
        ("/parts/genesis_theme.css", 200),
        ("/parts/genesis_organ_nav.js", 200),
        ("/parts/genesis_audio_kit.js", 200),
        ("/cinema_lite.html", 200),
        ("/music_studio.html", 200),
    ]
    
    for ep, expected_status in endpoints:
        url = f"http://localhost:8080{ep}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as res:
            assert res.status == expected_status, f"Expected {expected_status} for {ep}, got {res.status}"
            print(f"  [PASS] Endpoint: {ep} (HTTP {res.status})")

    # 2. Test MaleCNS v1.0 SNN Telemetry
    url = "http://localhost:8080/api/malecns/telemetry"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200
        data = json.loads(res.read().decode("utf-8"))
        assert data.get("success") is True
        assert data.get("total_neurons") == 166000
        assert data.get("total_synapses") == 125000000
        assert data.get("heartbeat_hz") == 40.0
        assert data.get("status") == "COHERENT_40HZ_ENTRAINED"
        print(f"  [PASS] MaleCNS v1.0 Telemetry: {data.get('total_neurons')} neurons, {data.get('heading_compass_deg')} deg, 40Hz Entrained")

    # 3. Test Antigravity Plan API
    url = "http://localhost:8080/api/antigravity/plan"
    payload = json.dumps({"prompt": "Test E2E Plan Generation"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as res:
        assert res.status == 200
        plan_data = json.loads(res.read().decode("utf-8"))
        assert plan_data.get("success") is True
        steps = plan_data.get("plan", {}).get("steps", [])
        assert len(steps) > 0
        print(f"  [PASS] Antigravity Plan API: Generated {len(steps)} DAG steps successfully")

    # 4. Test Antigravity Terminal Sandbox Exec API
    url = "http://localhost:8080/api/antigravity/exec"
    payload = json.dumps({"command": "echo GENESIS_PHASE_4_SUCCESS"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as res:
        assert res.status == 200
        exec_data = json.loads(res.read().decode("utf-8"))
        assert exec_data.get("success") is True
        assert "GENESIS_PHASE_4_SUCCESS" in exec_data.get("output", "")
        print("  [PASS] Antigravity Sandbox Exec API: Echo command executed verified")

    print("----------------------------------------")
    print(">>> ALL API & STATIC VERIFICATION PASSED (100%) <<<")
    print("----------------------------------------")

if __name__ == "__main__":
    test_endpoints()
