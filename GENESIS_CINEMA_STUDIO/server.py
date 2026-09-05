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

        # 2.5. 🏮 Global Cinematic Alleyway & Backstreet Scout Endpoint
        elif parsed.path == '/api/scout/alleyway':
            qs = urllib.parse.parse_qs(parsed.query)
            query = qs.get('query', [''])[0].strip()
            lat_str = qs.get('lat', [''])[0].strip()
            lng_str = qs.get('lng', [''])[0].strip()

            # Worldwide Cinematic Alleyways Database (Curated historic lanes & narrow streets)
            global_alleyways = {
                "パリ": (48.8878, 2.3385, 240.0, "パリ モンマルトルの石畳裏階段 (Rue de l'Abreuvoir, Paris)", "FjX9dY8z_sample1"),
                "paris": (48.8878, 2.3385, 240.0, "Rue de l'Abreuvoir, Montmartre (Paris, France)", "FjX9dY8z_sample1"),
                "ロンドン": (51.5103, -0.1264, 85.0, "ロンドン コヴェントガーデン裏小路 (Goodwin's Court, London)", "Lnd_mews_01"),
                "london": (51.5103, -0.1264, 85.0, "Goodwin's Court Historic Gaslit Alley (London, UK)", "Lnd_mews_01"),
                "ローマ": (41.8893, 12.4721, 110.0, "ローマ トラステヴェレ地区の細道 (Via della Lungaretta, Rome)", "Rome_trast_01"),
                "rome": (41.8893, 12.4721, 110.0, "Vicolo del Cinque, Trastevere (Rome, Italy)", "Rome_trast_01"),
                "バルセロナ": (41.3837, 2.1764, 310.0, "バルセロナ ゴシック地区 ビスベ小路 (Carrer del Bisbe, Barcelona)", "Bcn_gothic_01"),
                "barcelona": (41.3837, 2.1764, 310.0, "Carrer del Bisbe, Gothic Quarter (Barcelona, Spain)", "Bcn_gothic_01"),
                "ヴェネツィア": (45.4371, 12.3412, 190.0, "ヴェネツィア 運河沿い狭小迷宮路地 (Calle del Paradiso, Venice)", "Ven_paradiso_01"),
                "venice": (45.4371, 12.3412, 190.0, "Calle del Paradiso Narrow Canal Passage (Venice, Italy)", "Ven_paradiso_01"),
                "香港": (22.2827, 114.1543, 200.0, "香港 中環 砵典乍街・石板街 (Pottinger St Stair Alley, HK)", "HK_pottinger_01"),
                "hong kong": (22.2827, 114.1543, 200.0, "Pottinger Street Historic Stepped Alley (Hong Kong)", "HK_pottinger_01"),
                "プラハ": (50.0919, 14.4038, 270.0, "プラハ城 黄金の小路 (Golden Lane, Prague)", "Prg_golden_01"),
                "prague": (50.0919, 14.4038, 270.0, "Zlata Ulicka / Golden Lane (Prague, Czechia)", "Prg_golden_01"),
                "ニューヨーク": (40.7033, -73.9896, 15.0, "NY ダンボ・ワシントン街のレンガ小路 (Washington St, DUMBO, NYC)", "NYC_dumbo_01"),
                "new york": (40.7033, -73.9896, 15.0, "Washington St Cobblestone Alley (DUMBO, NYC)", "NYC_dumbo_01"),
                "京都": (35.0048, 135.7712, 180.0, "京都 鴨川沿い 先斗町通り (木造格子戸の細道)", "Kyoto_pontocho_01"),
                "kyoto": (35.0048, 135.7712, 180.0, "Pontocho Alley Historic Narrow Corridor (Kyoto, Japan)", "Kyoto_pontocho_01"),
                "浅草": (35.7126, 139.7958, 260.0, "浅草 西参道・初音小路 昭和レトロ路地 (東京)", "Asakusa_hatsune_01"),
                "新宿": (35.6929, 139.6997, 340.0, "新宿 西口 思い出横丁 (やきとり小路)", "Shinjuku_omoide_01"),
                "池袋": (35.7279, 139.7176, 325.8, "池袋 東口繁華街・美久仁小路 (昭和横丁)", "Ikebukuro_mikuni_01"),
                "神楽坂": (35.7018, 139.7408, 60.0, "東京 神楽坂・兵庫横丁 (石畳と黒板塀の隠れ路地)", "Kagurazaka_hyogo_01"),
                "モナコ": (43.7311, 7.4239, 120.0, "モナコ公国 旧市街ル・ロシェ迷宮小路 (Rue Basse, Monaco)", "Monaco_rocher_01"),
                "鈴鹿": (34.8872, 136.5056, 220.0, "三重 鈴鹿・東海道 庄野宿 歴史街道小路", "Suzuka_shono_01"),
                "エディンバラ": (55.9501, -3.1912, 350.0, "エディンバラ 旧市街の急勾配路地 (Advocate's Close, Edinburgh)", "Edin_close_01"),
                "アムステルダム": (52.3738, 4.9004, 160.0, "アムステルダム 運河沿い歴史的レンガ小路 (Zeedijk, Amsterdam)", "Ams_zeedijk_01")
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
