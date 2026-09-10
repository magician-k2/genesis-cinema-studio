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
MEDIA_VAULT_FILE = os.path.join(DIRECTORY, 'media_vault.json')
MEDIA_UPLOAD_DIR = os.path.join(DIRECTORY, 'media_vault_uploads')
if not os.path.exists(MEDIA_UPLOAD_DIR):
    os.makedirs(MEDIA_UPLOAD_DIR, exist_ok=True)

# Initialize Character Matting & 4-View Engine
ROOT_DIR = os.path.dirname(DIRECTORY)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from core.character_matting_engine import CharacterMattingEngine
from core.mocap_pose_transfer_engine import MocapPoseTransferEngine
from core.aerial_flight_swarm_engine import AerialFlightSwarmEngine
from core.quantum_gemma4_engine import quantum_gemma_engine
from core.genesis_4view_to_3d_mesh_engine import mesh_3d_engine
from core.genesis_hybrid_3d_dispatcher import hybrid_3d_dispatcher
from core.genesis_humanoid_figure_basemesh_engine import figure_basemesh_engine
from core.face_synthesis_docking_engine import face_docking_engine
from core.quantum_nervous_orchestrator import QuantumNervousOrchestrator
qno = QuantumNervousOrchestrator()
matting_engine = CharacterMattingEngine(vault_dir=os.path.join(DIRECTORY, 'characters'))
mocap_engine = MocapPoseTransferEngine(root_dir=ROOT_DIR)
aerial_engine = AerialFlightSwarmEngine()


# 🎙️ Google DeepMind Gemini Native Audio TTS Engine (gemini-2.5-flash-preview-tts)
import hashlib
import struct

VOICES_CACHE_DIR = os.path.join(DIRECTORY, 'characters', 'voices')
os.makedirs(VOICES_CACHE_DIR, exist_ok=True)

def pcm24k_to_wav(pcm_bytes, rate=24000):
    datalen = len(pcm_bytes)
    header = struct.pack('<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + datalen, b'WAVE', b'fmt ', 16, 1, 1, rate, rate * 2, 2, 16, b'data', datalen
    )
    return header + pcm_bytes

def synthesize_gemini_tts(text: str, voice_name: str = 'Fenrir', persona: dict = None) -> dict:
    if not text:
        return {"success": False, "error": "Empty text"}
        
    text_clean = text.replace('『', '').replace('』', '').replace('「', '').replace('」', '').strip()
    persona = persona or {}
    birthplace = persona.get('birthplace', '').strip()
    raised = persona.get('raised', '').strip()
    residence = persona.get('residence', '').strip()
    story = persona.get('story', '').strip()
    accent = persona.get('accent', '').strip()
    char_name = persona.get('name', '').strip()
    
    acting_context = []
    if char_name: acting_context.append(f"【キャラクター名】{char_name}")
    if birthplace: acting_context.append(f"【出身地】{birthplace}")
    if raised: acting_context.append(f"【育った場所・環境】{raised}")
    if residence: acting_context.append(f"【現在の居住地】{residence}")
    if story: acting_context.append(f"【生い立ちと声の個性】{story}")
    if accent: acting_context.append(f"【方言・口調】{accent}")

    # 1. Primary cache key by spoken text and voice name for instantaneous 0ms cache hits
    cache_key = hashlib.md5(f"{text_clean}_{voice_name}".encode('utf-8')).hexdigest()
    cache_filename = f"{voice_name}_{cache_key}.wav"
    cache_path = os.path.join(VOICES_CACHE_DIR, cache_filename)
    audio_url = f"/characters/voices/{cache_filename}"

    # Also check actor-named preset clips (e.g. ren_normal_Aoede.wav or ren_test_Aoede.wav)
    actor_key = persona.get('actor', '')
    if actor_key:
        named_candidates = [
            f"{actor_key}_normal_{voice_name}.wav",
            f"{actor_key}_awaken_{voice_name}.wav",
            f"{actor_key}_test_{voice_name}.wav",
            f"{actor_key}_{voice_name}.wav"
        ]
        for nc in named_candidates:
            np = os.path.join(VOICES_CACHE_DIR, nc)
            if os.path.exists(np) and os.path.getsize(np) > 1000:
                if not os.path.exists(cache_path):
                    try:
                        with open(np, 'rb') as sf, open(cache_path, 'wb') as df:
                            df.write(sf.read())
                    except Exception:
                        pass
                return {
                    "success": True,
                    "cached": True,
                    "voice": voice_name,
                    "audioUrl": f"/characters/voices/{nc}",
                    "text": text_clean,
                    "persona": persona
                }

    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        return {
            "success": True,
            "cached": True,
            "voice": voice_name,
            "audioUrl": audio_url,
            "text": text_clean,
            "persona": persona
        }

    # Google Gemini Native Audio TTS generates pristine audio when contents is the clean dialogue transcript
    prompt_content = text_clean

    try:
        from google import genai
        from google.genai import types
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT_DIR, '.env'))
        api_key = os.environ.get('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)

        resp = client.models.generate_content(
            model='gemini-2.5-flash-preview-tts',
            contents=prompt_content,
            config=types.GenerateContentConfig(
                response_modalities=['AUDIO'],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                    )
                )
            )
        )

        if resp.candidates and resp.candidates[0].content and resp.candidates[0].content.parts:
            part = resp.candidates[0].content.parts[0]
            if part.inline_data and part.inline_data.data:
                wav_bytes = pcm24k_to_wav(part.inline_data.data, 24000)
                with open(cache_path, 'wb') as f:
                    f.write(wav_bytes)
                return {
                    "success": True,
                    "cached": False,
                    "voice": voice_name,
                    "audioUrl": audio_url,
                    "text": text_clean,
                    "persona": persona,
                    "fileSize": len(wav_bytes)
                }
    except Exception as e:
        print(f"[Gemini TTS] API Error: {e}", file=sys.stderr)

    # Fallback to Edge Neural TTS if Gemini API was unavailable
    try:
        import asyncio, edge_tts
        edge_voice_map = {
            'Fenrir': 'ja-JP-KeitaNeural',
            'Charon': 'ja-JP-KeitaNeural',
            'Aoede': 'ja-JP-NanamiNeural',
            'Kore': 'ja-JP-MayuNeural',
            'Puck': 'ja-JP-AoiNeural'
        }
        edge_voice = edge_voice_map.get(voice_name, 'ja-JP-NanamiNeural' if voice_name in ['Aoede', 'Kore'] else 'ja-JP-KeitaNeural')
        asyncio.run(edge_tts.Communicate(text_clean, edge_voice).save(cache_path))
        return {
            "success": True,
            "cached": False,
            "fallback": f"Edge Neural TTS ({edge_voice})",
            "voice": voice_name,
            "audioUrl": audio_url,
            "text": text_clean
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_ai_character_turnaround(prompt_text: str, metadata: dict):
    """
    Generate photorealistic 4-view turnaround sheet using Google GenAI (gemini-3.1-flash-image / gemini-2.5-flash-image).
    """
    from PIL import Image
    import io
    from google import genai

    api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyBycrf1yVVcARNepmrblZJYtAxtKEUN92s')
    client = genai.Client(api_key=api_key)

    char_name = metadata.get('name', '')
    char_name_en = metadata.get('name_en', '')
    age = metadata.get('age', 26)
    gender = metadata.get('gender', 'male')
    height_m = metadata.get('height_m', 1.80)
    build = metadata.get('build', 'athletic')
    costume_tags = metadata.get('costume_tags', [])
    costume = ', '.join(costume_tags) if isinstance(costume_tags, list) else str(costume_tags)
    neon_accent = metadata.get('neon_accent')
    has_neon = bool(neon_accent and str(neon_accent).lower() not in ['none', '#000000', ''])

    wardrobe_desc = (
        f"{costume} style with subtle luminous neon trim ({neon_accent})."
        if has_neon else
        f"{costume}. Authentic premium textile textures, natural fabric folds, NO glowing neon lines, NO cybernetic seams, pure realistic clothing."
    )

    turnaround_instruction = (
        f"Master photorealistic 4-view character turnaround sheet showing 4 angles side-by-side: "
        f"1. Front View, 2. Right Side Profile, 3. Back View, 4. Left Side Profile. "
        f"Subject: {char_name_en} ({char_name}), {age}-year-old Japanese {gender} detective/actor, {height_m}m tall, {build} build. "
        f"Face & Hair: Defined facial features, sharp intense cinematic gaze, natural textured hair strands. "
        f"Wardrobe: {wardrobe_desc} "
        f"Pose: Strict neutral standing A-pose. Both arms hanging naturally down along the sides of the body. Both hands completely empty, open relaxed fingers, natural wrists, NO held objects, NO tablets, NO weapons, NO hands in pockets, NO raised arms. "
        f"Framing & Consistency: Full body visible from head to boots. All 4 views are evenly spaced side-by-side on an infinite solid pure white background (#FFFFFF). Perfectly identical character and clothing across all 4 views. "
        f"Quality: Hyper-realistic 8K cinema still photography, ARRI Alexa LF, 35mm anamorphic prime lens, natural human skin pores and texture, studio lighting, photorealistic live-action movie actor. "
        f"Negative constraints: anime, cartoon, 3D CGI render, illustration, drawing, painting, "
        f"{'' if has_neon else 'glowing neon lines, cybernetic glow, '}held items, handheld tablets, guns, swords, cut off hands, severed wrists, floor grid, ground text, shadows on floor, pedestals."
    )

    models_to_try = ["gemini-3.1-flash-image", "gemini-2.5-flash-image"]
    last_err = None
    for model_name in models_to_try:
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=turnaround_instruction
            )
            for part in resp.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    return Image.open(io.BytesIO(part.inline_data.data))
        except Exception as e:
            last_err = e
            print(f"[AI Turnaround] Model {model_name} failed: {e}, trying fallback...", file=sys.stderr)
            continue

    raise RuntimeError(f"All Google AI image models failed: {last_err}")

class GenesisCinemaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # ⚛️ Quantum Nervous Orchestrator (Q-NO) Status Endpoint
        if parsed.path == '/api/qno/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            status_data = qno.get_topology_status()
            self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode('utf-8'))
            return
        
        # 1. 🌐 Cloud Street View Gateway Endpoint
        elif parsed.path == '/api/streetview':
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
                # 🏛️ Digital Asset Management: Media Vault Master Aggregator
        elif parsed.path == '/api/media_vault':
            all_assets = []

            # 1. Cast & Characters (from characters/characters_vault.json)
            char_vault_path = os.path.join(DIRECTORY, 'characters', 'characters_vault.json')
            if os.path.exists(char_vault_path):
                try:
                    with open(char_vault_path, 'r', encoding='utf-8') as f:
                        chars = json.load(f)
                    for c in chars:
                        views = c.get('views', {})
                        all_assets.append({
                            'id': f"char_{c.get('id', '')}",
                            'category': 'cast',
                            'category_name': '👤 キャスト・人物',
                            'title': c.get('name', '未登録キャスト'),
                            'subtitle': f"{c.get('name_en', '')} ({c.get('age', 20)}歳 / {c.get('height_m', 1.7)}m)",
                            'thumbnail': views.get('front', '/characters/test_ren_e2e/front.png'),
                            'views': views,
                            'tags': c.get('costume_tags', []) + [c.get('gender', '')],
                            'created_at': c.get('created_at', ''),
                            'source_studio': 'asset_studio.html',
                            'metadata': {
                                'voice': c.get('voice_profile', ''),
                                'build': c.get('build', '')
                            }
                        })
                except Exception as e:
                    print("Error reading char vault:", e)

            # 2. Costumes & Props & Vehicles (from props_vault.json)
            if os.path.exists(PROPS_VAULT_FILE):
                try:
                    with open(PROPS_VAULT_FILE, 'r', encoding='utf-8') as f:
                        pv = json.load(f)
                    # Costumes
                    for item in pv.get('costumes', []):
                        all_assets.append({
                            'id': f"costume_{item.get('id', '')}",
                            'category': 'costume',
                            'category_name': '👘 衣装・クローゼット',
                            'title': item.get('name', '衣装'),
                            'subtitle': item.get('category', 'コスチューム'),
                            'thumbnail': item.get('texture_url', item.get('image_url', 'https://images.unsplash.com/photo-1544441893-675973e31985?w=500&q=80')),
                            'tags': item.get('tags', []) + ['衣装', 'ECテクスチャ'],
                            'created_at': item.get('created_at', '2026-09-06'),
                            'source_studio': 'asset_studio.html',
                            'metadata': item
                        })
                    # Props
                    for item in pv.get('props', []):
                        all_assets.append({
                            'id': f"prop_{item.get('id', '')}",
                            'category': 'prop',
                            'category_name': '🗡️ 小道具 (Props)',
                            'title': item.get('name', '小道具'),
                            'subtitle': item.get('category', 'プロップアイテム'),
                            'thumbnail': item.get('image_url', 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&q=80'),
                            'tags': item.get('tags', []) + ['小道具', '透過PNG'],
                            'created_at': item.get('created_at', '2026-09-06'),
                            'source_studio': 'asset_studio.html',
                            'metadata': item
                        })
                    # Vehicles
                    for item in pv.get('vehicles', []):
                        all_assets.append({
                            'id': f"veh_{item.get('id', '')}",
                            'category': 'vehicle',
                            'category_name': '🚌 大道具・車両',
                            'title': item.get('name', '車両'),
                            'subtitle': item.get('pattern_type', '大道具'),
                            'thumbnail': item.get('image_url', 'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=500&q=80'),
                            'tags': item.get('tags', []) + ['車両', 'ラッピング'],
                            'created_at': item.get('created_at', '2026-09-06'),
                            'source_studio': 'asset_studio.html',
                            'metadata': item
                        })
                except Exception as e:
                    print("Error reading props vault:", e)

            # 3. Locations & Scouting Snaps (from locations_vault.json)
            if os.path.exists(VAULT_FILE):
                try:
                    with open(VAULT_FILE, 'r', encoding='utf-8') as f:
                        locs = json.load(f)
                    for loc in locs:
                        all_assets.append({
                            'id': f"loc_{loc.get('id', '')}",
                            'category': 'location',
                            'category_name': '🌐 ロケハンスナップ',
                            'title': loc.get('name', '登録ロケ地'),
                            'subtitle': f"GPS: {loc.get('lat', 0):.4f}, {loc.get('lng', 0):.4f} (方位: {loc.get('heading', 0)}°)",
                            'thumbnail': f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={loc.get('lat', 35.7111)},{loc.get('lng', 139.7963)}&heading={loc.get('heading', 180)}&pitch=0&fov=80&key={API_KEY}",
                            'tags': loc.get('tags', []) + ['360°実写', 'ストリートビュー'],
                            'created_at': loc.get('created_at', '2026-09-06'),
                            'source_studio': 'index.html',
                            'metadata': loc
                        })
                except Exception as e:
                    print("Error reading locations vault:", e)

            # 4. Aerial Dive-in Keyframes & Flight Snaps
            aerial_presets = [
                {
                    'id': 'aerial_osaka_dive',
                    'category': 'aerial',
                    'category_name': '🛸 空撮キーフレーム',
                    'title': '大阪中之島 355m➔48m 超高空ダイブイン',
                    'subtitle': 'Google Earth 3D 空撮軌道 (急降下速度 55.8m/s / 200km/h)',
                    'thumbnail': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&q=80',
                    'tags': ['GoogleEarth', 'ダイブイン', '大阪中之島', '355m高空'],
                    'created_at': '2026-09-06',
                    'source_studio': 'aerial_studio.html',
                    'metadata': {'start_alt': 355, 'end_alt': 48, 'descent_rate': 55.8}
                },
                {
                    'id': 'aerial_shinjuku_glide',
                    'category': 'aerial',
                    'category_name': '🛸 空撮キーフレーム',
                    'title': '新宿副都心 420m➔50m 超高層滑空ショット',
                    'subtitle': 'Google Earth 3D 空撮軌道 (都庁ビル群すり抜け)',
                    'thumbnail': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600&q=80',
                    'tags': ['GoogleEarth', '新宿副都心', '滑空', 'ビル群'],
                    'created_at': '2026-09-06',
                    'source_studio': 'aerial_studio.html',
                    'metadata': {'start_alt': 420, 'end_alt': 50, 'descent_rate': 45.0}
                }
            ]
            all_assets.extend(aerial_presets)

            # 5. Video Footages (Shot Bin)
            footage_presets = [
                {
                    'id': 'footage_shot1_omotesando',
                    'category': 'footage',
                    'category_name': '🎬 生成動画フッテージ',
                    'title': 'Shot 1: 表参道並木道・正面シネマドリー',
                    'subtitle': 'Veo 3.1 4K 60fps / 5.0秒 / 40m前進トラッキング',
                    'thumbnail': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&q=80',
                    'tags': ['Veo3.1', '4K', 'ドリー', '表参道'],
                    'created_at': '2026-09-06',
                    'source_studio': 'cast_footage_studio.html',
                    'metadata': {'duration': 5.0, 'fps': 60, 'resolution': '4K'}
                },
                {
                    'id': 'footage_shot2_sensoji',
                    'category': 'footage',
                    'category_name': '🎬 生成動画フッテージ',
                    'title': 'Shot 2: 浅草寺雷門・夕焼けクレーン降下',
                    'subtitle': 'Veo 3.1 4K 60fps / 4.5秒 / 夕焼け3000Kライティング',
                    'thumbnail': 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=600&q=80',
                    'tags': ['Veo3.1', '4K', '浅草寺', '夕焼け'],
                    'created_at': '2026-09-06',
                    'source_studio': 'cast_footage_studio.html',
                    'metadata': {'duration': 4.5, 'fps': 60, 'resolution': '4K'}
                }
            ]
            all_assets.extend(footage_presets)

            # 6. Custom Uploaded Assets in media_vault.json
            if os.path.exists(MEDIA_VAULT_FILE):
                try:
                    with open(MEDIA_VAULT_FILE, 'r', encoding='utf-8') as f:
                        custom_items = json.load(f)
                    if isinstance(custom_items, list):
                        all_assets.extend(custom_items)
                except Exception as e:
                    print("Error reading custom media vault:", e)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'count': len(all_assets), 'assets': all_assets}, ensure_ascii=False).encode('utf-8'))
            return

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

        # 🥋 DessinPose 100-Pose Master Library Endpoint
        elif parsed.path == '/api/dessinpose/manifest':
            vault_index = os.path.join(DIRECTORY, 'assets', 'dessinpose_vault', 'poses_master_index.json')
            if os.path.exists(vault_index):
                with open(vault_index, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(manifest_data, ensure_ascii=False).encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "DessinPose manifest not found"}, ensure_ascii=False).encode('utf-8'))
                return

        # 💈 MEN'S NON-NO 360° Hair Catalog Master Library Endpoint
        elif parsed.path == '/api/haircatalog/manifest':
            hair_index = os.path.join(DIRECTORY, 'assets', 'haircatalog_vault', 'hair_master_index.json')
            if os.path.exists(hair_index):
                with open(hair_index, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(manifest_data, ensure_ascii=False).encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Hair catalog manifest not found"}, ensure_ascii=False).encode('utf-8'))
                return

        # 🎭 Fictional Golden-Ratio Faces Master Library Endpoint
        elif parsed.path == '/api/face/manifest':
            try:
                manifest_data = face_docking_engine.get_manifest()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(manifest_data, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))
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
        
        # 🏛️ Save New Asset Item to Media Vault
        if parsed.path == '/api/media_vault':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                new_item = json.loads(body)
                if 'id' not in new_item:
                    new_item['id'] = f"custom_asset_{int(time.time() * 1000)}"
                if 'created_at' not in new_item:
                    new_item['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S')

                custom_items = []
                if os.path.exists(MEDIA_VAULT_FILE):
                    try:
                        with open(MEDIA_VAULT_FILE, 'r', encoding='utf-8') as f:
                            custom_items = json.load(f)
                    except Exception:
                        custom_items = []
                
                custom_items.insert(0, new_item)
                with open(MEDIA_VAULT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(custom_items, f, ensure_ascii=False, indent=2)

                res = {'success': True, 'item': new_item, 'message': 'アセットを保管庫に保存しました'}
            except Exception as e:
                res = {'success': False, 'error': str(e)}

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            return

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

        # 🚀 Google AI Photorealistic 4-View Turnaround Generator Endpoint
                # 🎙️ Google Gemini Native Audio TTS Endpoint
        elif parsed.path == '/api/tts/gemini':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                text = payload.get('text', '').strip()
                voice_name = payload.get('voice', 'Fenrir')
                actor = payload.get('actor', 'ren')

                voice_map = {
                    'ren': 'Fenrir',
                    'mayu': 'Aoede',
                    'rin': 'Kore',
                    'aoi': 'Puck'
                }
                if voice_name in ['ja-JP-Chirp3-HD-Ren', 'Ren', 'ren']:
                    voice_name = 'Fenrir'
                elif voice_name in ['ja-JP-Chirp3-HD-Yui', 'Yui', 'mayu']:
                    voice_name = 'Aoede'
                elif voice_name in ['ja-JP-Chirp3-HD-Aoi-Kids', 'Aoi', 'aoi']:
                    voice_name = 'Puck'
                elif voice_name not in ['Fenrir', 'Aoede', 'Kore', 'Puck', 'Charon']:
                    voice_name = voice_map.get(actor, 'Fenrir')

                persona = payload.get('persona', {})
                if isinstance(persona, dict):
                    persona['actor'] = actor
                else:
                    persona = {'actor': actor}
                result = synthesize_gemini_tts(text, voice_name, persona)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

        elif parsed.path == '/api/character/generate_ai_turnaround':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                prompt_text = payload.get('prompt', '')
                char_id = payload.get('char_id') or f"char_{int(time.time()*1000)}"
                metadata = payload.get('metadata', {})

                # 1. Generate 4-view turnaround sheet with Google AI
                ai_sheet_img = generate_ai_character_turnaround(prompt_text, metadata)

                # 2. Save raw sheet in character folder
                char_dir = os.path.join(matting_engine.vault_dir, char_id)
                os.makedirs(char_dir, exist_ok=True)
                raw_sheet_path = os.path.join(char_dir, 'raw_sheet.png')
                ai_sheet_img.save(raw_sheet_path, 'PNG')

                # 3. Process with SOTA matting, slicing, defringe & ground alignment
                result = matting_engine.process_turnaround_sheet(ai_sheet_img, char_id, metadata)
                result['raw_sheet'] = f"/characters/{char_id}/raw_sheet.png"

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "character": result}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
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

        # ✈️ Analyze Flight Recording Video (Google Earth Ctrl+Alt+A Flight Sim)
        elif parsed.path == '/api/aerial/analyze_flight_video':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                video_name = payload.get('video_name', 'flight_recording.mp4')
                duration_s = float(payload.get('duration_s', 6.0))
                start_alt = float(payload.get('start_altitude_m', 650.0))
                end_alt = float(payload.get('end_altitude_m', 48.0))

                analysis = aerial_engine.analyze_flight_video(
                    video_name=video_name,
                    duration_s=duration_s,
                    estimated_start_alt=start_alt,
                    estimated_end_alt=end_alt
                )
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(analysis, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ⚛️ Quantum-Type Gemma 4 SQA Timeline Cut Optimizer Endpoint
        elif parsed.path == '/api/quantum/optimize_timeline':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                clips = payload.get('clips', [])
                target_sec = float(payload.get('target_duration_sec', 30.0))
                bpm = float(payload.get('bpm', 120.0))

                res = quantum_gemma_engine.optimize_timeline_cuts(
                    candidate_clips=clips,
                    target_duration_sec=target_sec,
                    bpm=bpm
                )
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ⚛️ Quantum-Type Gemma 4 3D Pose & Rigging Optimizer Endpoint
        elif parsed.path == '/api/quantum/optimize_3d_pose':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                joint_angles = payload.get('joint_angles', [])
                collision_pairs = [tuple(p) for p in payload.get('collision_pairs', [])]
                weights = payload.get('desired_pose_weights', [])

                res = quantum_gemma_engine.optimize_3d_pose_rigging(
                    joint_angles=joint_angles,
                    collision_pairs=collision_pairs,
                    desired_pose_weights=weights
                )
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ⚛️ Dual-AI Code AST Verification Endpoint (Antigravity 2.0 Telepathy Bridge)
        elif parsed.path == '/api/quantum/code_assist':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                symbols = payload.get('symbols', [])
                required_calls = payload.get('required_calls', [])

                res = quantum_gemma_engine.verify_code_dependencies(
                    symbol_definitions=symbols,
                    required_calls=required_calls
                )
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ⚛️ Quantum Nervous Orchestrator (Q-NO) - Pulse Emission Endpoint
        elif parsed.path == '/api/qno/pulse':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                pulse = QuantumOrganPulse(
                    source_organ=payload.get('source_organ', 'UNKNOWN_ORGAN'),
                    target_organ=payload.get('target_organ', 'ALL'),
                    action=payload.get('action', 'NOOP'),
                    payload=payload.get('payload', {}),
                    priority=float(payload.get('priority', 1.0)),
                    qubo_affinity=float(payload.get('qubo_affinity', 0.5))
                )
                res = qno.emit_pulse(pulse)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ⚛️ Quantum Nervous Orchestrator (Q-NO) - Workload Arbitration Endpoint
        elif parsed.path == '/api/qno/arbitrate':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                tasks = payload.get('tasks', [])
                res = qno.arbitrate_workload(tasks)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # ⚛️ Quantum Nervous Orchestrator (Q-NO) - Edge SEED Node Registration / Heartbeat Endpoint
        elif parsed.path == '/api/qno/register_seed':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                node_id = payload.get('node_id', f"seed_{int(time.time()*1000)}")
                res = qno.register_edge_seed(
                    node_id=node_id,
                    device_type=payload.get('device_type', 'BROWSER_WEBGPU'),
                    gpu_vendor=payload.get('gpu_vendor', 'GENERIC_GPU'),
                    latency_ms=float(payload.get('latency_ms', 10.0)),
                    battery_level=payload.get('battery_level')
                )
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "seed": res}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🧊 GENESIS AI 3D Mesh Generator (TripoSR-Equivalent Engine)
        elif parsed.path == '/api/character/generate_3d_mesh':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                char_dir = os.path.join(DIRECTORY, 'characters', char_id)
                front_p = os.path.join(char_dir, 'front.png')
                right_p = os.path.join(char_dir, 'right.png')
                back_p  = os.path.join(char_dir, 'back.png')
                left_p  = os.path.join(char_dir, 'left.png')
                out_obj = os.path.join(char_dir, 'actor_model.obj')

                res = hybrid_3d_dispatcher.dispatch_3d_generation(
                    character_id=char_id,
                    height_m=float(payload.get('height_m', 1.82)),
                    mode=payload.get('mode', 'hybrid_optimal')
                )
                res["model_url"] = f"/characters/{char_id}/actor_model.obj?t={int(time.time())}"

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🥋 GENESIS Anatomical Figure Basemesh Generator (Amazon Body-kun/chan Standard)
        elif parsed.path == '/api/character/generate_basemesh':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                char_dir = os.path.join(DIRECTORY, 'characters', char_id)
                os.makedirs(char_dir, exist_ok=True)

                gender = payload.get('gender', 'male')
                height_m = float(payload.get('height_m', 1.80))
                body_type = payload.get('body_type', 'standard')
                bust_cm = float(payload.get('bust_cm')) if payload.get('bust_cm') is not None else None
                waist_cm = float(payload.get('waist_cm')) if payload.get('waist_cm') is not None else None
                hip_cm = float(payload.get('hip_cm')) if payload.get('hip_cm') is not None else None
                skin_tone = payload.get('skin_tone', 'natural')

                # 保存先: actor_model.obj を素体ベースで更新
                out_obj = os.path.join(char_dir, 'actor_model.obj')
                basemesh_obj = os.path.join(char_dir, 'basemesh_model.obj')

                res = figure_basemesh_engine.generate_figure_basemesh(
                    output_obj_path=out_obj,
                    gender=gender,
                    height_m=height_m,
                    body_type=body_type,
                    bust_cm=bust_cm,
                    waist_cm=waist_cm,
                    hip_cm=hip_cm,
                    skin_tone=skin_tone
                )

                # basemesh_model.obj にも複製コピー
                import shutil
                shutil.copyfile(out_obj, basemesh_obj)
                mtl_src = os.path.join(char_dir, 'figure_basemesh.mtl')
                if os.path.exists(mtl_src):
                    shutil.copyfile(mtl_src, os.path.join(char_dir, 'actor_model.mtl'))

                res["model_url"] = f"/characters/{char_id}/actor_model.obj?t={int(time.time() * 1000)}"
                res["basemesh_url"] = f"/characters/{char_id}/basemesh_model.obj?t={int(time.time() * 1000)}"

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🥋 DessinPose Apply to Character Endpoint
        elif parsed.path == '/api/dessinpose/apply':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                gender = payload.get('gender', 'female')
                category = payload.get('category', 'standing')
                pose_id = payload.get('pose_id', '0000')

                pose_src_dir = os.path.join(DIRECTORY, 'assets', 'dessinpose_vault', gender, category, f"pose_{pose_id}")
                char_dir = os.path.join(DIRECTORY, 'characters', char_id)
                os.makedirs(char_dir, exist_ok=True)

                import shutil
                copied_files = []
                for fname in ['front.jpg', 'right.jpg', 'back.jpg', 'left.jpg', 'top.jpg']:
                    src_f = os.path.join(pose_src_dir, fname)
                    if os.path.exists(src_f):
                        dst_f = os.path.join(char_dir, f"pose_{fname}")
                        shutil.copyfile(src_f, dst_f)
                        shutil.copyfile(src_f, os.path.join(char_dir, fname))
                        copied_files.append(fname)

                angles_urls = [
                    f"/assets/dessinpose_vault/{gender}/{category}/pose_{pose_id}/angle_h{h:02d}.jpg"
                    for h in range(24)
                ]

                res = {
                    "success": True,
                    "character_id": char_id,
                    "pose_id": pose_id,
                    "gender": gender,
                    "category": category,
                    "copied_views": copied_files,
                    "angles_24": angles_urls,
                    "top_url": f"/assets/dessinpose_vault/{gender}/{category}/pose_{pose_id}/top.jpg",
                    "thumbnail_url": f"/assets/dessinpose_vault/{gender}/{category}/pose_{pose_id}/thumbnail.jpg"
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 💈 Apply Hair Style to Character Endpoint
        elif parsed.path == '/api/haircatalog/apply':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                category = payload.get('category', 'short')
                style_id = payload.get('style_id', '')

                # Execute natural hair docking onto 4-view character images
                dock_res = face_docking_engine.dock_hair_onto_character(char_id, category, style_id)

                style_src_dir = os.path.join(DIRECTORY, 'assets', 'haircatalog_vault', category, f"style_{style_id}")
                char_dir = os.path.join(DIRECTORY, 'characters', char_id)
                os.makedirs(char_dir, exist_ok=True)

                import shutil
                copied_files = []
                for fname in ['front.jpg', 'right.jpg', 'back.jpg', 'left.jpg']:
                    src_f = os.path.join(style_src_dir, fname)
                    if os.path.exists(src_f):
                        dst_f = os.path.join(char_dir, f"hair_{fname}")
                        shutil.copyfile(src_f, dst_f)
                        copied_files.append(fname)

                angles_urls = [
                    f"/assets/haircatalog_vault/{category}/style_{style_id}/angle_{deg:03d}.jpg"
                    for deg in range(0, 360, 30)
                ]

                # Update character_meta.json if present
                char_meta_file = os.path.join(char_dir, 'character_meta.json')
                if os.path.exists(char_meta_file):
                    try:
                        with open(char_meta_file, 'r', encoding='utf-8') as cmf:
                            char_meta_data = json.load(cmf)
                        char_meta_data['hair_style_ref'] = {
                            "style_id": style_id,
                            "category": category,
                            "angles_12": angles_urls,
                            "thumbnail_url": f"/assets/haircatalog_vault/{category}/style_{style_id}/thumbnail.jpg"
                        }
                        with open(char_meta_file, 'w', encoding='utf-8') as cmf:
                            json.dump(char_meta_data, cmf, ensure_ascii=False, indent=2)
                    except Exception as meta_e:
                        print("Error updating character meta hair ref:", meta_e)

                res = {
                    "success": True,
                    "character_id": char_id,
                    "style_id": style_id,
                    "category": category,
                    "copied_views": copied_files,
                    "angles_12": angles_urls,
                    "views": dock_res.get('views', {}),
                    "timestamp": dock_res.get('timestamp', int(time.time())),
                    "thumbnail_url": f"/assets/haircatalog_vault/{category}/style_{style_id}/thumbnail.jpg"
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 💈 Revert Hair Style to Original Endpoint
        elif parsed.path == '/api/haircatalog/revert':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                revert_res = face_docking_engine.restore_character_backup(char_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(revert_res, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🎭 Generate AI Fictional Face Endpoint
        elif parsed.path == '/api/face/generate':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                prompt = payload.get('prompt', '20代の知性派映画主役俳優')
                gender = payload.get('gender', 'male')
                category = payload.get('category', 'cool_sharp')
                result_face = face_docking_engine.generate_ai_face(prompt=prompt, gender=gender, category=category)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "face": result_face}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 🧬 Trinity Face Fusion & Docking Endpoint (Dessin + Hair + Fictional Face)
        elif parsed.path == '/api/face/dock':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                face_id = payload.get('face_id', 'male_cool_01')
                hair_category = payload.get('hair_category', 'short')
                hair_style_id = payload.get('hair_style_id', '000')
                dessin_gender = payload.get('dessin_gender', 'male')
                dessin_category = payload.get('dessin_category', 'standing')
                dessin_pose_id = payload.get('dessin_pose_id', '0000')

                dock_result = face_docking_engine.dock_trinity(
                    character_id=char_id,
                    face_id=face_id,
                    hair_category=hair_category,
                    hair_style_id=hair_style_id,
                    dessin_gender=dessin_gender,
                    dessin_category=dessin_category,
                    dessin_pose_id=dessin_pose_id
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(dock_result, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        # 👤 Apply Fictional Face Metadata Endpoint
        elif parsed.path == '/api/face/apply':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                char_id = payload.get('character_id', 'ren')
                face_id = payload.get('face_id', 'male_cool_01')
                char_dir = os.path.join(DIRECTORY, 'characters', char_id)
                char_meta_file = os.path.join(char_dir, 'character_meta.json')
                
                meta_data = {}
                if os.path.exists(char_meta_file):
                    with open(char_meta_file, 'r', encoding='utf-8') as cmf:
                        meta_data = json.load(cmf)
                
                meta_data['fictional_face_ref'] = {
                    "face_id": face_id,
                    "thumbnail_url": f"/assets/face_vault/{face_id}/thumbnail.jpg",
                    "front_url": f"/assets/face_vault/{face_id}/front.png"
                }

                with open(char_meta_file, 'w', encoding='utf-8') as cmf:
                    json.dump(meta_data, cmf, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "character_id": char_id, "face_id": face_id}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8'))
                return

        elif parsed.path == '/api/ytmusic/analyze':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
            try:
                payload = json.loads(body) if body else {}
                url_or_query = payload.get('url', '').strip()
                scene_context = payload.get('context', 'Cyberpunk & Cinema Blockbuster')
                if not url_or_query:
                    url_or_query = "Hans Zimmer Interstellar Style"

                from core.genesis_youtube_music_analyzer import analyze_and_produce_prompt
                result = analyze_and_produce_prompt(url_or_query, scene_context)

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

        elif parsed.path == '/api/music/separate_stems':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
            try:
                payload = json.loads(body) if body else {}
                url_or_query = payload.get('url', '').strip()
                scene_context = payload.get('context', 'Cyberpunk & Cinema Blockbuster')
                raw_duration = payload.get('duration_sec', 0)
                duration_sec = None if (raw_duration is None or float(raw_duration) <= 0 or float(raw_duration) >= 9999) else float(raw_duration)
                if not url_or_query:
                    url_or_query = "Hans Zimmer Interstellar Style"

                from core.genesis_youtube_music_analyzer import analyze_and_separate_stems
                result = analyze_and_separate_stems(url_or_query, scene_context, max_duration_sec=duration_sec)

                resp_bytes = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_bytes)
                return
            except (ConnectionAbortedError, BrokenPipeError):
                return
            except Exception as e:
                err_bytes = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8')
                try:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Content-Length', str(len(err_bytes)))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(err_bytes)
                except Exception:
                    pass
                return

        elif parsed.path == '/api/music/upload_and_analyze':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
            try:
                payload = json.loads(body) if body else {}
                b64_data = payload.get('audio_base64', '')
                filename = payload.get('filename', 'upload.wav')
                scene_context = payload.get('context', 'Cyberpunk & Cinema Blockbuster')
                raw_duration = payload.get('duration_sec', 0)
                duration_sec = None if (raw_duration is None or float(raw_duration) <= 0 or float(raw_duration) >= 9999) else float(raw_duration)

                if ',' in b64_data:
                    b64_data = b64_data.split(',', 1)[1]

                import base64, tempfile
                raw_bytes = base64.b64decode(b64_data)
                ext = os.path.splitext(filename)[1] or '.wav'
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tf:
                    tf.write(raw_bytes)
                    temp_file_path = tf.name

                from core.genesis_youtube_music_analyzer import analyze_and_separate_stems
                try:
                    result = analyze_and_separate_stems(temp_file_path, scene_context, max_duration_sec=duration_sec)
                    result["track_title"] = os.path.splitext(filename)[0]
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                resp_bytes = json.dumps(result, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_bytes)
                return
            except Exception as e:
                err_bytes = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(err_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(err_bytes)
                return

        elif parsed.path == '/api/music/generate_lyria':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
            try:
                payload = json.loads(body) if body else {}
                prompt = payload.get('prompt', 'Cinematic Cyberpunk Track')
                features = payload.get('features', {"bpm": 123.0, "key": "G Major", "energy": "Cinematic"})
                duration = int(payload.get('duration_sec', 30))

                from core.genesis_youtube_music_analyzer import generate_music_with_lyria
                result = generate_music_with_lyria(prompt, features, duration)
                resp_bytes = json.dumps(result, ensure_ascii=False).encode('utf-8')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_bytes)
                return
            except Exception as e:
                err_bytes = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(err_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(err_bytes)
                return

        elif parsed.path == '/api/music/publish_ytmusic':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
            try:
                payload = json.loads(body) if body else {}
                track_title = payload.get('track_title', 'GENESIS Sovereign Track')
                artist_name = payload.get('artist', 'GENESIS Cinema AI Ensemble')
                features = payload.get('features', {})
                prompt = payload.get('prompt', '')

                from core.genesis_youtube_music_analyzer import package_for_youtube_music
                result = package_for_youtube_music(track_title, artist_name, features, prompt)
                resp_bytes = json.dumps(result, ensure_ascii=False).encode('utf-8')

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(resp_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp_bytes)
                return
            except Exception as e:
                err_bytes = json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(err_bytes)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(err_bytes)
                return




        self.send_response(404)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": f"Endpoint not found: {parsed.path}"}).encode('utf-8'))
        return

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    with ThreadedHTTPServer(("", PORT), GenesisCinemaHandler) as httpd:
        print(f"🎬 GENESIS Global Cinema Studio Server running on http://localhost:{PORT}")
        httpd.serve_forever()

