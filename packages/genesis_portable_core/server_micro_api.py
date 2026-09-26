# -*- coding: utf-8 -*-
"""
GENESIS Portable Core: Zero-Dependency Micro-Server
Built entirely on Python standard library (http.server).
Requires NO pip packages! Runs out-of-the-box on ANY machine with Python 3.
Serves:
1. Static Application Assets (HTML / JS / CSS)
2. REST JSON APIs for SNN, Connectome, Merkle Proof & Triple-Shield Orchestration
"""

import os
import sys
import json
import time
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Import sibling modules
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine_snn import PortableActiveInferenceCortex
from engine_connectome import PortableConnectomeNavigator
from engine_merkle import PortableMerkleAuditor
from engine_orchestrator import PortableTripleShieldOrchestrator

cortex = PortableActiveInferenceCortex(num_neurons=100)
connectome = PortableConnectomeNavigator()
merkle = PortableMerkleAuditor()
orchestrator = PortableTripleShieldOrchestrator()

APP_ROOT = Path(__file__).resolve().parent.parent.parent  # default fallback

class GenesisMicroHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = str(APP_ROOT)
        super().__init__(*args, directory=directory, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # 1. API: Status & Heartbeat
        if parsed.path == "/api/status":
            self.send_json_response({
                "genesis_portable_core": "ONLINE",
                "version": "2.0.0-PORTABLE",
                "triple_shield": orchestrator.state,
                "snn_neurons": len(cortex.neurons),
                "flywire_grounding": "Princeton FlyWire Connectome",
                "eu_compliance": "EU AI Act Art. 13 Auditable",
                "uptime_sec": round(time.time() - START_TIME, 1)
            })
            return

        # 2. API: SNN Step
        elif parsed.path == "/api/snn_step":
            sim = cortex.step_simulation(current_time=time.time() * 1000)
            self.send_json_response(sim)
            return

        # 3. Static Files Fallback
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            req_data = json.loads(post_body) if post_body else {}
        except Exception:
            req_data = {}

        # 1. API: Full Causal Reverse-Mindmap Reasoning
        if parsed.path == "/api/reason":
            query = req_data.get("query", "生体脳と同じ機能を持つ機械脳を作るには？")
            
            # Step 1: Triple-Shield Dispatch
            tso = orchestrator.dispatch_intent(query)
            
            # Step 2: Connectome Causal Convergence
            path_result = connectome.resolve_reverse_causal_path(query)
            
            # Step 3: SNN Simulation Step
            snn_result = cortex.step_simulation(current_time=time.time() * 1000)
            
            # Step 4: Cryptographic Merkle Receipt
            evidence = [n["name"] for n in path_result["evidence_periphery_nodes"]]
            receipt = merkle.generate_cognitive_receipt(
                query=query,
                decision=path_result["root_cause"]["name"],
                evidence=evidence
            )

            response_payload = {
                "status": "SUCCESS",
                "query": query,
                "orchestration": tso,
                "reverse_causal_graph": path_result,
                "snn_telemetry": snn_result,
                "cognitive_receipt": receipt
            }
            self.send_json_response(response_payload)
            return

        self.send_error(404, "Endpoint not found")

    def send_json_response(self, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

START_TIME = time.time()

def run_server(port: int = 8080, serve_dir: str = None):
    global APP_ROOT
    if serve_dir:
        APP_ROOT = Path(serve_dir).resolve()
    
    server_address = ('', port)
    handler = lambda *args, **kwargs: GenesisMicroHandler(*args, directory=str(APP_ROOT), **kwargs)
    httpd = HTTPServer(server_address, handler)
    print(f"🏛️ GENESIS Portable Core Micro-Server running on http://localhost:{port}/")
    print(f"📁 Serving assets from: {APP_ROOT}")
    print("⚡ Endpoints: /api/status, /api/reason, /api/snn_step")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Micro-Server stopped.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    serve_path = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).resolve().parent.parent.parent)
    run_server(port, serve_path)
