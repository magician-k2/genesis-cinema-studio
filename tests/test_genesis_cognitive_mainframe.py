# -*- coding: utf-8 -*-
"""
Tests for GenesisCognitiveMainframeEngine & Organ Wave Multiplexing
Enhanced with Zero-Mock 2D Raw Pixel EMD, 1000Hz Medulla Daemon Thread,
and Alley Micro-Cartographer Raw Frame Difference Inspection.
"""
import time
import unittest
import numpy as np
from core.genesis_cognitive_mainframe_engine import (
    GenesisCognitiveMainframeEngine,
    VisualCortexNN,
    AuditoryCortexNN,
    VestibularCortexNN,
    SomatoMotorCortexNN,
    AssociationExecutiveCortex,
    FlyBrainOpticLobeEMD,
    FlyBrainCentralComplex,
    MedullaTechnoCPG,
    AlleyMicroCartographer
)

class TestGenesisCognitiveMainframe(unittest.TestCase):
    def setUp(self):
        self.engine = GenesisCognitiveMainframeEngine()

    def test_visual_cortex(self):
        vc = VisualCortexNN()
        res = vc.process_visual_input(0.8)
        self.assertIn("visual_saliency", res)
        self.assertTrue(0.0 <= res["visual_saliency"] <= 2.0)
        self.assertEqual(len(res["dominant_feature_vector"]), 4)

    def test_auditory_cortex(self):
        ac = AuditoryCortexNN()
        res = ac.process_auditory_input(0.9)
        self.assertIn("acoustic_arousal", res)
        self.assertTrue(0.0 <= res["acoustic_arousal"] <= 1.0)
        self.assertEqual(res["auditory_event"], "ALERT_TRANSIENT")

    def test_vestibular_cortex(self):
        vst = VestibularCortexNN()
        res = vst.process_vestibular_input(0.8, dt=0.01)
        self.assertIn("postural_equilibrium", res)
        self.assertTrue(0.0 <= res["postural_equilibrium"] <= 1.0)

    def test_active_inference(self):
        exec_cortex = AssociationExecutiveCortex()
        res = exec_cortex.compute_active_inference(predicted_sensory=0.5, actual_sensory=0.7)
        self.assertAlmostEqual(res["prediction_error"], 0.2, places=3)
        self.assertTrue(res["variational_free_energy"] > 0)
        self.assertTrue(0.0 <= res["updated_belief"] <= 1.0)

    def test_fly_brain_biomimetics_and_cpg(self):
        # 1D EMD
        emd = FlyBrainOpticLobeEMD()
        res_emd = emd.compute_motion_correlation(0.3, 0.7)
        self.assertIn("optical_flow_vector_x", res_emd)
        self.assertIn("collision_tau_sec", res_emd)

        # Central Complex Ring Attractor
        cx = FlyBrainCentralComplex()
        res_cx = cx.step_angular_velocity(45.0, dt=0.1)
        self.assertIn("compass_heading_deg", res_cx)
        self.assertIn("ring_attractor_peak_wedge", res_cx)

        # Medulla Techno CPG tick
        cpg = MedullaTechnoCPG()
        res_cpg = cpg.tick(dt=0.01)
        self.assertEqual(res_cpg["cpg_bpm"], 128.0)
        self.assertIn("baseline_carrier_amplitude", res_cpg)

    def test_fly_brain_2d_raw_pixel_emd(self):
        emd = FlyBrainOpticLobeEMD(grid_size=16)
        # Create synthetic moving frames (a bright vertical bar moving rightward)
        frame1 = np.zeros((64, 64), dtype=np.float32)
        frame1[:, 20:28] = 1.0

        frame2 = np.zeros((64, 64), dtype=np.float32)
        frame2[:, 28:36] = 1.0  # shifted right

        # First frame initializes memory
        res1 = emd.compute_2d_raw_pixel_emd(frame1)
        self.assertFalse(res1["collision_imminent"])

        # Second frame calculates true motion correlation
        res2 = emd.compute_2d_raw_pixel_emd(frame2)
        self.assertIn("optical_flow_x", res2)
        self.assertIn("collision_tau_sec", res2)
        self.assertEqual(res2["flow_grid_shape"], [16, 16])

    def test_medulla_1000hz_daemon_thread(self):
        cpg = MedullaTechnoCPG()
        cpg.start_cpg_daemon(target_hz=1000.0)
        time.sleep(0.05)  # allow background thread to generate ~50 samples

        pulse = cpg.get_realtime_pulse()
        self.assertTrue(pulse["daemon_running"])
        self.assertEqual(pulse["cpg_bpm"], 128.0)
        self.assertGreater(len(pulse["recent_pulse_samples"]), 0)

        cpg.stop_cpg_daemon()
        time.sleep(0.01)
        pulse_stopped = cpg.get_realtime_pulse()
        self.assertFalse(pulse_stopped["daemon_running"])

    def test_alley_micro_cartographer_raw_frame_diff(self):
        carto = AlleyMicroCartographer()
        coords = (35.6812, 139.7671)

        # Frame 1: Empty street
        frame1 = np.ones((64, 64, 3), dtype=np.uint8) * 100
        res1 = carto.inspect_and_extract_delta_from_raw_frames(frame1, coords)
        self.assertFalse(res1["has_delta"])

        # Frame 2: Sudden new landmark / obstacle in right alley
        frame2 = frame1.copy()
        frame2[10:40, 40:60, :] = 255  # bright sign
        res2 = carto.inspect_and_extract_delta_from_raw_frames(frame2, coords)

        self.assertTrue(res2["has_delta"])
        self.assertIsNotNone(res2["delta_payload"])
        payload = res2["delta_payload"]
        self.assertEqual(payload["delta_type"], "STRUCTURAL_STREET_FEATURE_CHANGE")
        self.assertGreater(payload["payload_size_kb"], 0.1)
        self.assertIn("affected_pixels_ratio", payload["difference_metrics"])

    def test_full_cognitive_closed_loop(self):
        result = self.engine.run_full_cognitive_closed_loop(
            external_tilt_perturbation=0.1,
            external_sound_flash=0.5
        )
        self.assertEqual(result["status"], "COGNITIVE_CLOSED_LOOP_SUCCESS")
        
        # Verify telemetry
        telemetry = result["wave_transmission_telemetry"]
        self.assertEqual(telemetry["sensory_channels_multiplexed"], 7)
        self.assertTrue(telemetry["composite_sensory_wave_rms"] > 0)
        self.assertTrue(telemetry["composite_motor_wave_rms"] > 0)

        # Verify cognitive analysis
        cortex = result["cognitive_mainframe_analysis"]
        self.assertIn("visual_cortex", cortex)
        self.assertIn("auditory_cortex", cortex)
        self.assertIn("vestibular_cortex", cortex)
        self.assertIn("active_inference_executive", cortex)
        self.assertIn("motor_synergy_planned", cortex)

        # Verify fly brain & cartographer
        fly = result["fly_brain_biomimetics"]
        self.assertIn("emd_optical_flow", fly)
        self.assertIn("central_complex_heading", fly)
        self.assertIn("minimal_techno_cpg", fly)

    def test_full_cognitive_closed_loop_with_raw_frame(self):
        synthetic_camera_frame = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
        result = self.engine.run_full_cognitive_closed_loop(
            external_tilt_perturbation=0.05,
            external_sound_flash=0.3,
            raw_frame=synthetic_camera_frame
        )
        self.assertEqual(result["status"], "COGNITIVE_CLOSED_LOOP_SUCCESS")
        fly = result["fly_brain_biomimetics"]
        self.assertIsNotNone(fly["raw_pixel_emd_2d"])
        self.assertIn("flow_grid_shape", fly["raw_pixel_emd_2d"])
        self.assertIn("dynamic_hazard_telemetry", result)

    def test_dynamic_road_network_router_and_reroute(self):
        from core.genesis_cognitive_mainframe_engine import DynamicRoadNetworkRouter
        router = DynamicRoadNetworkRouter()

        # 1. Normal state: TRUCK takes Underpass route (1100m)
        r_init = router.compute_optimal_route("N_DEPOT", "N_DEST_SHELTER", vehicle_type="TRUCK")
        self.assertTrue(r_init["route_found"])
        self.assertIn("L_UNDERPASS", r_init["path_links"])
        self.assertEqual(r_init["total_distance_m"], 1100)

        # 2. Hazard occurs: Underpass is submerged (sever link)
        sever_res = router.sever_link("L_UNDERPASS", reason="CRITICAL_INUNDATION")
        self.assertEqual(sever_res["status"], "SEVERED")

        # 3. TRUCK automatically diverts to High Bypass route (1250m)
        r_truck_reroute = router.compute_optimal_route("N_DEPOT", "N_DEST_SHELTER", vehicle_type="TRUCK")
        self.assertTrue(r_truck_reroute["route_found"])
        self.assertIn("L_HIGH_BYPASS", r_truck_reroute["path_links"])
        self.assertNotIn("L_UNDERPASS", r_truck_reroute["path_links"])

        # 4. BICYCLE uses Narrow 1.4m Alley route (920m)
        r_bike = router.compute_optimal_route("N_DEPOT", "N_DEST_SHELTER", vehicle_type="BICYCLE")
        self.assertTrue(r_bike["route_found"])
        self.assertIn("L_NARROW_ALLEY", r_bike["path_links"])
        self.assertEqual(r_bike["total_distance_m"], 920)

    def test_hazard_cartographer_inundation_detection(self):
        from core.genesis_cognitive_mainframe_engine import GenesisDynamicHazardCartographer
        hz_carto = GenesisDynamicHazardCartographer()

        # Synthesize Inundated Road Frame (Smooth specular highlight with zero high-frequency texture)
        flood_frame = np.ones((80, 80, 3), dtype=np.uint8) * 40
        # Water specular highlight pool at bottom ROI
        flood_frame[55:75, 20:60, :] = 240

        res = hz_carto.inspect_frame_for_hazards(
            frame_rgb=flood_frame,
            current_coordinates=(35.6610, 139.7040),
            target_link_id="L_UNDERPASS"
        )

        self.assertTrue(res["hazard_detected"])
        self.assertEqual(res["hazard_type"], "CRITICAL_INUNDATION")
        self.assertIsNotNone(res["hazard_delta_payload"])
        p = res["hazard_delta_payload"]
        self.assertGreater(p["estimated_depth_cm"], 15.0)
        self.assertIn("event_triggered_compression", p)
        self.assertIn("truck_reroute", res["reroute_navigation"])
        self.assertTrue(res["reroute_navigation"]["truck_reroute"]["route_found"])

    def test_spinal_reflex_arc(self):
        from core.genesis_cognitive_mainframe_engine import GenesisSpinalReflexArc
        spinal = GenesisSpinalReflexArc()

        # 1. Normal Proprioceptive Tonus
        res_norm = spinal.evaluate_reflex(collision_tau_sec=5.0, optical_flow_divergence=0.01, surface_depth_cm=0.0, accel_g=1.0)
        self.assertFalse(res_norm["reflex_triggered"])
        self.assertEqual(res_norm["reflex_action"], "NORMAL_PROPRIOCEPTIVE_TONUS")

        # 2. Critical Inundation Flood Reflex
        res_flood = spinal.evaluate_reflex(collision_tau_sec=5.0, optical_flow_divergence=0.01, surface_depth_cm=28.5, accel_g=1.0)
        self.assertTrue(res_flood["reflex_triggered"])
        self.assertEqual(res_flood["reflex_action"], "FLOOD_SEVER_AND_LATCH")
        self.assertEqual(res_flood["emergency_keyframe_size_kb"], 3.2)
        self.assertIn("insurtech_telematics", res_flood)
        ins = res_flood["insurtech_telematics"]
        self.assertEqual(ins["fault_ratio_objective_grade"], "CLASS_A_DEFINITIVE_TELEMATICS")

        # 3. Collision Imminent Reflex (tau < 0.8s)
        res_crash = spinal.evaluate_reflex(collision_tau_sec=0.45, optical_flow_divergence=0.12, surface_depth_cm=0.0, accel_g=1.0)
        self.assertTrue(res_crash["reflex_triggered"])
        self.assertEqual(res_crash["reflex_action"], "EMERGENCY_BRAKE_AND_LATCH")

        # 4. Impact Shock (accel_g >= 1.8G)
        res_impact = spinal.evaluate_reflex(collision_tau_sec=9.0, optical_flow_divergence=0.0, surface_depth_cm=0.0, accel_g=2.4)
        self.assertTrue(res_impact["reflex_triggered"])
        self.assertEqual(res_impact["reflex_action"], "IMPACT_EVIDENCE_LATCH")

    def test_autonomic_medulla(self):
        from core.genesis_cognitive_mainframe_engine import GenesisAutonomicMedulla, MedullaTechnoCPG
        cpg = MedullaTechnoCPG()
        medulla = GenesisAutonomicMedulla(master_cpg=cpg)

        # 1. Parked in garage (Hibernation Sleep)
        res_sleep = medulla.update_autonomic_state(engine_on=False, driver_present=False, vibration_g=0.1)
        self.assertEqual(res_sleep["autonomic_state"], "HIBERNATION_SLEEP")
        self.assertEqual(res_sleep["power_mode"], "ULTRA_LOW_POWER_120uW")

        # 2. Door punch / vandalism shock (Instant Arousal Wakeup)
        res_arousal = medulla.update_autonomic_state(engine_on=False, driver_present=False, vibration_g=1.65)
        self.assertEqual(res_arousal["autonomic_state"], "AROUSAL_WAKEUP")
        self.assertEqual(res_arousal["power_mode"], "HIGH_PERF_NPU_AWAKE")
        self.assertEqual(res_arousal["absence_incident_count"], 1)

        # 3. Driver enters car (Bluetooth Handshake & Incident Report)
        res_sync = medulla.update_autonomic_state(engine_on=False, driver_present=True, vibration_g=0.2)
        self.assertEqual(res_sync["autonomic_state"], "BLUETOOTH_SYNC")
        self.assertEqual(res_sync["bluetooth_tether_status"], "PAIRED_WITH_ACTIVE_PHONE")

        report = medulla.sync_to_driver_smartphone()
        self.assertEqual(report["sync_status"], "SUCCESSFUL_BLUETOOTH_HANDSHAKE")
        self.assertEqual(report["driver_notified_incidents"], 1)

    def test_drive_parallel_fanout_router(self):
        from core.genesis_cognitive_mainframe_engine import GenesisDriveParallelFanoutRouter
        router = GenesisDriveParallelFanoutRouter(
            owner_gmail="magician.k2@gmail.com",
            institutional_email="251zs04264@student.zen.ac.jp"
        )
        
        # Dispatch parallel fan-out for flood incident
        res = router.dispatch_parallel_fanout(
            event_type="CRITICAL_INUNDATION",
            coordinates=(35.6610, 139.7040),
            telematics_payload={"depth_cm": 28.5, "severity": "BLOCKED"},
            keyframe_size_kb=3.2
        )
        
        self.assertIn("dispatch_id", res)
        self.assertIn("dedicated_drive_vault", res)
        self.assertEqual(res["dedicated_drive_vault"]["owner"], "magician.k2@gmail.com")
        self.assertEqual(res["dedicated_drive_vault"]["authorized_auditor"], "251zs04264@student.zen.ac.jp")
        self.assertTrue(res["dedicated_drive_vault"]["sandbox_isolated_from_personal_data"])
        
        # Verify 4 parallel fan-out destinations
        dests = res["parallel_fanout_destinations"]
        self.assertIn("1_INSURER_GRID", dests)
        self.assertIn("2_JARTIC_AND_POLICE", dests)
        self.assertIn("3_GOOGLE_MAPS_AND_STREETVIEW", dests)
        self.assertIn("4_MUNICIPALITY_DISASTER_BCP", dests)
        self.assertTrue(res["bystander_witness_matched"])
        self.assertEqual(dests["1_INSURER_GRID"]["fault_ratio_grade"], "OBJECTIVE_10_0_DETERMINED")

    def test_closed_loop_with_spinal_and_medulla(self):
        res = self.engine.run_full_cognitive_closed_loop(
            external_tilt_perturbation=0.2,
            external_sound_flash=0.5
        )
        self.assertEqual(res["status"], "COGNITIVE_CLOSED_LOOP_SUCCESS")
        self.assertIn("spinal_reflex_telemetry", res)
        self.assertIn("autonomic_medulla_telemetry", res)
        self.assertIn("google_drive_fanout_telemetry", res)
        self.assertIn("insurtech_telematics", res["spinal_reflex_telemetry"])
        self.assertEqual(res["autonomic_medulla_telemetry"]["autonomic_state"], "ACTIVE_CRUISE")

if __name__ == "__main__":
    unittest.main()
