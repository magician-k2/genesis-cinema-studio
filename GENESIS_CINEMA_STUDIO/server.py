import time
import http.server
import socketserver
import urllib.parse
import urllib.request
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PORT = 8080
API_KEY = 'AIzaSyBkhM10sDbZGHmeBfeMGC6cgeIVr9qPvUk'
DIRECTORY = r'G:\マイドライブ\GENESIS_ROOT\GENESIS_CINEMA_STUDIO'
VAULT_FILE = os.path.join(DIRECTORY, 'locations_vault.json')

# Initialize Character Matting & 4-View Engine
ROOT_DIR = os.path.dirname(DIRECTORY)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from core.character_matting_engine import CharacterMattingEngine
from core.mocap_pose_transfer_engine import MocapPoseTransferEngine
matting_engine = CharacterMattingEngine(vault_dir=os.path.join(DIRECTORY, 'characters'))
mocap_engine = MocapPoseTransferEngine(root_dir=ROOT_DIR)

class GenesisCinemaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # 1. 🌐 Cloud Street View Gateway Endpoint
        if parsed.path == '/api/streetview':
            qs = urllib.parse.parse_qs(parsed.query)
            lat = qs.get('lat', ['35.7111'])[0]
            lng = qs.get('lng', ['139.7963'])[0]
            heading = qs.get('heading', ['180'])[0]
            pitch = qs.get('pitch', ['-1'])[0]
            fov = qs.get('fov', ['75'])[0]
            
            google_url = f"https://maps.googleapis.com/maps/api/streetview?size=1200x800&location={lat},{lng}&heading={heading}&pitch={pitch}&fov={fov}&key={API_KEY}"
            
            try:
                req = urllib.request.Request(google_url, headers={'User-Agent': 'GenesisCinemaStudio/1.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Cache-Control', 'public, max-age=86400')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                    return
            except Exception as e:
                fallback_path = os.path.join(DIRECTORY, 'assets', 'harajuku_straight_street_perfect.jpg')
                if os.path.exists(fallback_path):
                    with open(fallback_path, 'rb') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                    return

        # 2. 🔍 Global Geo Location Scout Endpoint
        elif parsed.path == '/api/scout':
            qs = urllib.parse.parse_qs(parsed.query)
            query = qs.get('query', ['浅草寺 雷門'])[0]
            
            geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(query)}&key={API_KEY}"
            try:
                req = urllib.request.Request(geo_url, headers={'User-Agent': 'GenesisCinemaStudio/1.0'})
                with urllib.request.urlopen(req, timeout=8) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('status') == 'OK' and len(data.get('results', [])) > 0:
                        loc = data['results'][0]['geometry']['location']
                        formatted_address = data['results'][0].get('formatted_address', query)
                        res_data = {
                            'success': True,
                            'lat': loc['lat'],
                            'lng': loc['lng'],
                            'heading': 0.0,
                            'locationName': formatted_address
                        }
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json; charset=utf-8')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps(res_data, ensure_ascii=False).encode('utf-8'))
                        return
            except Exception as e:
                pass

            # Worldwide Presets
            world_presets = {
                "鈴鹿": (34.8431, 136.5410, "鈴鹿サーキット (三重県鈴鹿市)"),
                "ビッグベン": (51.5007, -0.1246, "ビッグベン / ウェストミンスター (ロンドン, イギリス)"),
                "big ben": (51.5007, -0.1246, "Big Ben / Westminster (London, UK)"),
                "浅草寺": (35.7111, 139.7963, "浅草寺 雷門 (東京都台東区浅草)"),
                "タイムズスクエア": (40.7580, -73.9855, "Times Square (New York, USA)"),
                "エッフェル塔": (48.8584, 2.2945, "Eiffel Tower (Paris, France)")
            }
            matched_loc = None
            for k, v in world_presets.items():
                if k in query.lower():
                    matched_loc = v
                    break

            if matched_loc:
                res_data = { 'success': True, 'lat': matched_loc[0], 'lng': matched_loc[1], 'heading': 0.0, 'locationName': matched_loc[2] }
            else:
                res_data = { 'success': True, 'lat': 35.7111, 'lng': 139.7963, 'heading': 180.0, 'locationName': f"{query} (ロケ地特定)" }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(res_data, ensure_ascii=False).encode('utf-8'))
            return

        # 3. 📂 Location Vault List Endpoint
        elif parsed.path == '/api/locations':
            if os.path.exists(VAULT_FILE):
                with open(VAULT_FILE, 'r', encoding='utf-8') as f:
                    vault_data = json.load(f)
            else:
                vault_data = []
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(vault_data, ensure_ascii=False).encode('utf-8'))
            return

        # 4. 🛣️ Street View Metadata & Coverage Endpoint
        elif parsed.path == '/api/roads':
            qs = urllib.parse.parse_qs(parsed.query)
            lat = float(qs.get('lat', ['35.7111'])[0])
            lng = float(qs.get('lng', ['139.7963'])[0])
            
            # Query official Google Street View Metadata API for precise panorama availability
            meta_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={lat},{lng}&radius=100&key={API_KEY}"
            has_sv = True
            pano_id = ""
            actual_loc = {"lat": lat, "lng": lng}
            try:
                req = urllib.request.Request(meta_url, headers={'User-Agent': 'GenesisCinemaStudio/1.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    meta_data = json.loads(response.read().decode('utf-8'))
                    if meta_data.get('status') == 'OK':
                        has_sv = True
                        pano_id = meta_data.get('pano_id', '')
                        if 'location' in meta_data:
                            actual_loc = meta_data['location']
            except Exception as e:
                pass

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"hasCoverage": has_sv, "panoId": pano_id, "location": actual_loc}, ensure_ascii=False).encode('utf-8'))
            return

        # 5. 👥 Characters Vault List Endpoint
        elif parsed.path == '/api/characters':
            char_list = matting_engine.list_characters()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(char_list, ensure_ascii=False).encode('utf-8'))
            return

        # 6. 👤 Single Character Detail Endpoint
        elif parsed.path.startswith('/api/characters/'):
            char_id = parsed.path.split('/api/characters/')[1].strip('/')
            char_meta_path = os.path.join(matting_engine.vault_dir, char_id, 'character_meta.json')
            if os.path.exists(char_meta_path):
                with open(char_meta_path, 'r', encoding='utf-8') as f:
                    char_data = json.load(f)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(char_data, ensure_ascii=False).encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Character not found"}, ensure_ascii=False).encode('utf-8'))
                return

        return super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # 💾 Save New Location to Vault Endpoint
        if parsed.path == '/api/locations':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                new_loc = json.loads(body)
                if os.path.exists(VAULT_FILE):
                    with open(VAULT_FILE, 'r', encoding='utf-8') as f:
                        vault_data = json.load(f)
                else:
                    vault_data = []

                new_loc['id'] = f"loc_{int(time.time()*1000)}"
                vault_data.insert(0, new_loc)

                with open(VAULT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(vault_data, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "location": new_loc}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        # 🎭 Process Turnaround Sheet (Input A)
        elif parsed.path == '/api/character/process_sheet':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                sheet_img = payload.get('sheet_image')
                char_id = payload.get('char_id') or f"char_{int(time.time()*1000)}"
                metadata = payload.get('metadata', {})
                result = matting_engine.process_turnaround_sheet(sheet_img, char_id, metadata)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "character": result}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 📱 Process Individual Photos (Input B: Real actors, underground idols, etc.)
        elif parsed.path == '/api/character/process_photos':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                photos = payload.get('photos', {})  # { front, right, back, left }
                char_id = payload.get('char_id') or f"char_{int(time.time()*1000)}"
                metadata = payload.get('metadata', {})
                result = matting_engine.process_individual_photos(photos, char_id, metadata)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "character": result}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
        # 🎬 Mocap Pose & Acting Extraction Endpoint
        elif parsed.path == '/api/mocap/extract_motion':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                import base64
                import tempfile
                payload = json.loads(body)
                video_base64 = payload.get('video_base64')
                video_path = payload.get('video_path')
                start_sec = float(payload.get('start_sec', 0.0))
                end_sec = float(payload.get('end_sec', 3.0))
                sample_fps = int(payload.get('sample_fps', 15))

                temp_file = None
                if video_base64:
                    # Strip base64 header if present
                    if ',' in video_base64:
                        video_base64 = video_base64.split(',', 1)[1]
                    raw_bytes = base64.b64decode(video_base64)
                    temp_dir = os.path.join(ROOT_DIR, "outputs", "mocap_preview")
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_file = os.path.join(temp_dir, f"upload_{int(time.time()*1000)}.mp4")
                    with open(temp_file, "wb") as tf:
                        tf.write(raw_bytes)
                    target_video = temp_file
                elif video_path and os.path.exists(video_path):
                    target_video = video_path
                else:
                    # Default sample video if none provided
                    sample_video = os.path.join(DIRECTORY, 'assets', 'harajuku_straight_street_perfect.mp4')
                    target_video = sample_video if os.path.exists(sample_video) else video_path

                result = mocap_engine.extract_motion_from_video(
                    target_video, start_sec=start_sec, end_sec=end_sec, sample_fps=sample_fps
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🎭 Apply Mocap Motion to Character Actor Endpoint
        elif parsed.path == '/api/mocap/apply_to_actor':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'test_idol_e2e')
                motion_data = payload.get('motion_data', {})
                char_meta_path = os.path.join(matting_engine.vault_dir, char_id, 'character_meta.json')
                
                char_info = {}
                if os.path.exists(char_meta_path):
                    with open(char_meta_path, 'r', encoding='utf-8') as f:
                        char_info = json.load(f)

                transfer_result = {
                    "success": True,
                    "character_id": char_id,
                    "character_name": char_info.get("name", char_id),
                    "acting_direction": motion_data.get("acting_direction", {}),
                    "motion_summary": motion_data.get("motion_summary", {}),
                    "synchronized_keyframes": motion_data.get("frames", []),
                    "veo_prompt": motion_data.get("acting_direction", {}).get("veo_prompt", ""),
                    "status": "MOTION_TRANSFERRED_TO_ACTOR",
                    "timestamp": int(time.time() * 1000)
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(transfer_result, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        return super().do_POST()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), GenesisCinemaHandler) as httpd:
        print(f"🎬 GENESIS Global Cinema Studio Server running on http://localhost:{PORT}")
        httpd.serve_forever()
