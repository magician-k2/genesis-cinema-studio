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
PROPS_VAULT_FILE = os.path.join(DIRECTORY, 'props_vault.json')
SCENES_VAULT_FILE = os.path.join(DIRECTORY, 'scenes_vault.json')

# Initialize Character Matting & 4-View Engine
ROOT_DIR = os.path.dirname(DIRECTORY)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from core.character_matting_engine import CharacterMattingEngine
from core.mocap_pose_transfer_engine import MocapPoseTransferEngine
from core.aerial_flight_swarm_engine import AerialFlightSwarmEngine
matting_engine = CharacterMattingEngine(vault_dir=os.path.join(DIRECTORY, 'characters'))
mocap_engine = MocapPoseTransferEngine(root_dir=ROOT_DIR)
aerial_engine = AerialFlightSwarmEngine()

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

        # 2.5. 🏮 Global Cinematic Alleyway & Backstreet Scout Endpoint
        elif parsed.path == '/api/scout/alleyway':
            qs = urllib.parse.parse_qs(parsed.query)
            query = qs.get('query', [''])[0].strip()
            lat_str = qs.get('lat', [''])[0].strip()
            lng_str = qs.get('lng', [''])[0].strip()

            # Worldwide Cinematic Alleyways Database (Curated authentic narrow lanes & cobblestones)
            global_alleyways = {
                "パリ": (48.8878, 2.3385, 240.0, "パリ モンマルトルの石畳裏階段 (Rue de l'Abreuvoir, Paris)", ""),
                "paris": (48.8878, 2.3385, 240.0, "Rue de l'Abreuvoir, Montmartre (Paris, France)", ""),
                "ロンドン": (51.5108, -0.1275, 85.0, "ロンドン コヴェントガーデン裏小路 (St Martin's Ct, London)", ""),
                "london": (51.5108, -0.1275, 85.0, "Historic Gaslit Alley (London, UK)", ""),
                "ローマ": (41.8893, 12.4721, 110.0, "ローマ トラステヴェレ地区の細道 (Via della Lungaretta, Rome)", ""),
                "rome": (41.8893, 12.4721, 110.0, "Vicolo del Cinque, Trastevere (Rome, Italy)", ""),
                "バルセロナ": (41.3837, 2.1764, 310.0, "バルセロナ ゴシック地区 ビスベ小路 (Carrer del Bisbe, Barcelona)", ""),
                "barcelona": (41.3837, 2.1764, 310.0, "Carrer del Bisbe, Gothic Quarter (Barcelona, Spain)", ""),
                "ヴェネツィア": (45.4371, 12.3412, 190.0, "ヴェネツィア 運河沿い狭小迷宮路地 (Calle del Paradiso, Venice)", ""),
                "venice": (45.4371, 12.3412, 190.0, "Calle del Paradiso Narrow Canal Passage (Venice, Italy)", ""),
                "香港": (22.2827, 114.1543, 200.0, "香港 中環 砵典乍街・石板街 (Pottinger St Stair Alley, HK)", ""),
                "hong kong": (22.2827, 114.1543, 200.0, "Pottinger Street Historic Stepped Alley (Hong Kong)", ""),
                "プラハ": (50.0919, 14.4038, 270.0, "プラハ城 黄金の小路 (Golden Lane, Prague)", ""),
                "prague": (50.0919, 14.4038, 270.0, "Zlata Ulicka / Golden Lane (Prague, Czechia)", ""),
                "ニューヨーク": (40.7033, -73.9896, 15.0, "NY ダンボ・ワシントン街のレンガ小路 (Washington St, DUMBO, NYC)", ""),
                "new york": (40.7033, -73.9896, 15.0, "Washington St Cobblestone Alley (DUMBO, NYC)", ""),
                "京都": (35.0037, 135.7772, 180.0, "京都 祇園白川・先斗町 (石畳と格子戸の細道)", ""),
                "kyoto": (35.0037, 135.7772, 180.0, "Pontocho & Gion Shirakawa Historic Narrow Corridor (Kyoto)", ""),
                "浅草": (35.7118, 139.7963, 260.0, "浅草 仲見世裏道・西参道小路 (東京)", ""),
                "新宿": (35.6930, 139.6998, 340.0, "新宿 西口 思い出横丁 (やきとり小路)", ""),
                "池袋": (35.7279, 139.7176, 325.8, "池袋 東口繁華街・美久仁小路 (昭和横丁)", ""),
                "神楽坂": (35.7018, 139.7408, 60.0, "東京 神楽坂・兵庫横丁 (石畳と黒板塀の隠れ路地)", ""),
                "モナコ": (43.7311, 7.4239, 120.0, "モナコ公国 旧市街ル・ロシェ迷宮小路 (Rue Basse, Monaco)", ""),
                "鈴鹿": (34.8872, 136.5056, 220.0, "三重 鈴鹿・東海道 庄野宿 歴史街道小路", ""),
                "エディンバラ": (55.9501, -3.1912, 350.0, "エディンバラ 旧市街の急勾配路地 (Advocate's Close, Edinburgh)", ""),
                "アムステルダム": (52.3738, 4.9004, 160.0, "アムステルダム 運河沿い歴史的レンガ小路 (Zeedijk, Amsterdam)", "")
            }

            matched = None
            if query:
                for k, v in global_alleyways.items():
                    if k in query.lower():
                        matched = v
                        break

            if matched:
                res_data = {
                    'success': True,
                    'isAlleyway': True,
                    'lat': matched[0],
                    'lng': matched[1],
                    'heading': matched[2],
                    'locationName': f"🏮 {matched[3]}",
                    'panoId': matched[4],
                    'cinemaTag': 'atmospheric narrow cobblestone historic back-alley, moody shadows, authentic cinematic side-lighting, intimate scale'
                }
            else:
                # Dynamic Geo + Street View Exploration for ANY city or coordinate
                target_lat = float(lat_str) if lat_str else 35.7018
                target_lng = float(lng_str) if lng_str else 139.7408
                target_name = f"{query} 周辺の裏道・細道" if query else "探索された路地裏"

                if query:
                    # Append alley search terms to find authentic small lanes
                    alley_query = f"{query} alley OR lane OR passage OR 狭小路地 OR 横丁"
                    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(alley_query)}&key={API_KEY}"
                    try:
                        req = urllib.request.Request(geo_url, headers={'User-Agent': 'GenesisCinemaStudio/1.0'})
                        with urllib.request.urlopen(req, timeout=8) as response:
                            data = json.loads(response.read().decode('utf-8'))
                            if data.get('status') == 'OK' and len(data.get('results', [])) > 0:
                                loc = data['results'][0]['geometry']['location']
                                target_lat = loc['lat']
                                target_lng = loc['lng']
                                target_name = f"🏮 {data['results'][0].get('formatted_address', query)} (細道・小路)"
                    except Exception:
                        pass

                # Query Street View Metadata with small radius=25 to isolate back-alleys and avoid main roads
                meta_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={target_lat},{target_lng}&radius=25&source=default&key={API_KEY}"
                pano_id = ""
                try:
                    req = urllib.request.Request(meta_url, headers={'User-Agent': 'GenesisCinemaStudio/1.0'})
                    with urllib.request.urlopen(req, timeout=5) as response:
                        mdata = json.loads(response.read().decode('utf-8'))
                        if mdata.get('status') == 'OK':
                            pano_id = mdata.get('pano_id', '')
                            if 'location' in mdata:
                                target_lat = mdata['location']['lat']
                                target_lng = mdata['location']['lng']
                except Exception:
                    pass

                res_data = {
                    'success': True,
                    'isAlleyway': True,
                    'lat': target_lat,
                    'lng': target_lng,
                    'heading': 0.0,
                    'locationName': target_name,
                    'panoId': pano_id,
                    'cinemaTag': 'atmospheric narrow cobblestone historic back-alley, moody shadows, authentic cinematic side-lighting, intimate scale'
                }

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

        # 7. 🎭 Scene Assets Vault (Costumes, Props, Vehicles/Liveries) Endpoint
        elif parsed.path == '/api/scene/assets':
            assets = {"costumes": [], "props": [], "vehicles": []}
            if os.path.exists(PROPS_VAULT_FILE):
                try:
                    with open(PROPS_VAULT_FILE, 'r', encoding='utf-8') as f:
                        assets = json.load(f)
                except Exception:
                    pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(assets, ensure_ascii=False).encode('utf-8'))
            return

        # 8. 🎬 Generated Scenes List Endpoint
        elif parsed.path == '/api/scenes':
            scenes_data = []
            if os.path.exists(SCENES_VAULT_FILE):
                try:
                    with open(SCENES_VAULT_FILE, 'r', encoding='utf-8') as f:
                        scenes_data = json.load(f)
                except Exception:
                    pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(scenes_data, ensure_ascii=False).encode('utf-8'))
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
        # 🎬 Generate Cinema Scene (Actor + Costume + Prop + Vehicle + Street View)
        elif parsed.path == '/api/scene/generate':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', '')
                costume_id = payload.get('costume_id', '')
                prop_id = payload.get('prop_id', '')
                vehicle_id = payload.get('vehicle_id', '')
                loc = payload.get('location', {})
                custom_prompt = payload.get('custom_prompt', '').strip()

                # 1. Load Props Vault
                assets = {"costumes": [], "props": [], "vehicles": []}
                if os.path.exists(PROPS_VAULT_FILE):
                    with open(PROPS_VAULT_FILE, 'r', encoding='utf-8') as f:
                        assets = json.load(f)

                # 2. Match Assets
                costume_item = next((c for c in assets.get('costumes', []) if c['id'] == costume_id), None)
                prop_item = next((p for p in assets.get('props', []) if p['id'] == prop_id), None)
                vehicle_item = next((v for v in assets.get('vehicles', []) if v['id'] == vehicle_id), None)

                # 3. Match Character
                char_info = {}
                char_img_url = ""
                if char_id:
                    char_meta_path = os.path.join(matting_engine.vault_dir, char_id, 'character_meta.json')
                    if os.path.exists(char_meta_path):
                        with open(char_meta_path, 'r', encoding='utf-8') as f:
                            char_info = json.load(f)
                    char_img_url = f"/characters/{char_id}/front.png"

                # 4. Construct Photorealistic Veo 3.1 Scene Prompt
                loc_name = loc.get('locationName', 'Urban Street')
                lat = loc.get('lat', 35.7111)
                lng = loc.get('lng', 139.7963)
                heading = loc.get('heading', 180)
                is_alley = loc.get('isAlleyway', False)

                char_name = char_info.get('name', 'The protagonist')
                char_features = char_info.get('features', {})
                hair = char_features.get('hair', 'natural styling')
                build = char_features.get('build', 'slender build')

                prompt_parts = []
                prompt_parts.append(f"Cinematic 35mm motion picture master shot, ultra-photorealistic 8k, filmed on location at {loc_name} (Coordinates: {lat:.4f}, {lng:.4f}, facing heading {int(heading)}°).")

                # Character description
                char_desc = f"Main character {char_name} ({hair}, {build})"
                if costume_item:
                    char_desc += f", {costume_item['prompt_tag']}"
                if prop_item:
                    char_desc += f", authentically {prop_item['prompt_tag']}"
                prompt_parts.append(char_desc + ".")

                # Vehicle / Big prop description
                if vehicle_item:
                    prompt_parts.append(f"Set dressing: {vehicle_item['prompt_tag']} parked realistically along the street edge with accurate corporate livery.")

                # Lighting & Atmospheric tone
                if is_alley:
                    prompt_parts.append("Atmosphere: narrow historic cobblestone back-alley, dramatic rim lighting casting long shadows across textured walls, subtle atmospheric haze, wet ground reflections.")
                else:
                    prompt_parts.append("Atmosphere: authentic street ambiance, shallow depth of field, anamorphic bokeh, balanced cinematic grading, documentary realism.")

                if custom_prompt:
                    prompt_parts.append(f"Director cue: {custom_prompt}.")

                final_veo_prompt = " ".join(prompt_parts)

                # 5. Composite Scene Metadata for Immediate Stage Preview
                scene_id = f"scene_{int(time.time()*1000)}"
                scene_result = {
                    "success": True,
                    "scene_id": scene_id,
                    "timestamp": int(time.time() * 1000),
                    "title": f"🎬 {char_name} in {loc_name}",
                    "location": loc,
                    "character": {
                        "id": char_id,
                        "name": char_name,
                        "front_image": char_img_url,
                        "gender": char_info.get("gender", "")
                    },
                    "costume": costume_item,
                    "prop": prop_item,
                    "vehicle": vehicle_item,
                    "veo_prompt": final_veo_prompt,
                    "preview_layers": {
                        "streetview_url": f"/api/streetview?lat={lat}&lng={lng}&heading={heading}",
                        "character_overlay": char_img_url,
                        "prop_badge": prop_item['icon'] + ' ' + prop_item['name'] if prop_item else None,
                        "costume_badge": costume_item['icon'] + ' ' + costume_item['name'] if costume_item else None,
                        "vehicle_badge": vehicle_item['icon'] + ' ' + vehicle_item['name'] if vehicle_item else None
                    }
                }

                # 6. Save to Scenes Vault
                scenes_list = []
                if os.path.exists(SCENES_VAULT_FILE):
                    try:
                        with open(SCENES_VAULT_FILE, 'r', encoding='utf-8') as f:
                            scenes_list = json.load(f)
                    except Exception:
                        pass
                scenes_list.insert(0, scene_result)
                # Keep up to 50 scenes
                scenes_list = scenes_list[:50]
                with open(SCENES_VAULT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(scenes_list, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(scene_result, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ➕ Add New Costume/Prop/Vehicle into Props Vault
        elif parsed.path == '/api/props_vault/add':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                category = payload.get('category_type', 'props') # 'costumes' | 'props' | 'vehicles'
                item = payload.get('item', {})
                if not item.get('id'):
                    item['id'] = f"{category}_{int(time.time()*1000)}"

                assets = {"costumes": [], "props": [], "vehicles": []}
                if os.path.exists(PROPS_VAULT_FILE):
                    with open(PROPS_VAULT_FILE, 'r', encoding='utf-8') as f:
                        assets = json.load(f)

                if category not in assets:
                    assets[category] = []
                assets[category].append(item)

                with open(PROPS_VAULT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(assets, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "item": item}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🛩️ Parse Google Earth Web URL Endpoint
        elif parsed.path == '/api/aerial/parse_earth_url':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                url = payload.get('url', '')
                waypoint = aerial_engine.parse_earth_url(url)
                if waypoint:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True, "waypoint": waypoint}, ensure_ascii=False).encode('utf-8'))
                    return
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Invalid Google Earth URL"}, ensure_ascii=False).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🚀 Synthesize Aerial Dive-in Flight Scene via Gemma 4 Swarm Endpoint
        elif parsed.path == '/api/aerial/generate_flight':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                waypoints = payload.get('waypoints', [])
                traffic_level = payload.get('traffic_level', 'medium')
                crowd_level = payload.get('crowd_level', 'medium')
                location_name = payload.get('location_name', '大阪 中之島・市役所周辺')
                landing_gimmick = payload.get('landing_gimmick', 'hero_face_close_up')
                hero_name = payload.get('hero_name', '如月 蓮')

                flight_path = aerial_engine.compute_flight_path(waypoints)
                swarm_result = aerial_engine.execute_swarm_synthesis(
                    flight_info=flight_path,
                    traffic_level=traffic_level,
                    crowd_level=crowd_level,
                    location_name=location_name,
                    landing_gimmick=landing_gimmick,
                    hero_name=hero_name
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(swarm_result, ensure_ascii=False).encode('utf-8'))
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
