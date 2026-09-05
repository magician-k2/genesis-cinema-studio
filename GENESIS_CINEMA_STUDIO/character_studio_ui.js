/**
 * 🎭 GENESIS Cinema Studio: Character & Wardrobe Studio UI Engine (character_studio_ui.js)
 * ----------------------------------------------------------------------------------------
 * - [🅰️ プロンプト生成] ⇄ [🅱️ 実在人物4枚写真ドラッグ] 切替
 * - EC商品画像ドラッグ＆ドロップ着せ替えクローゼット
 * - 4面32bit完全透過PNGプレビュー ＆ Defringe（フチ消し）スライダー
 * - ストリートビュー実写空間へのワンクリック召喚＆路面接地影（Contact Drop Shadow）
 * - ドラッグ移動＆マウスホイールによる奥行きパース調整
 */

class CharacterStudioUI {
    constructor() {
        this.activeMode = 'prompt'; // 'prompt' or 'photos'
        this.activeCharacterId = 'ren';
        this.activeCharacterData = null;
        this.uploadedPhotos = { front: null, right: null, back: null, left: null };
        this.defringeStrength = 80; // 0 - 100%
        this.stageActorActive = false;
        this.stageActorAspect = 'front';
        this.stageActorScale = 1.0;
        this.stageActorPos = { x: 50, y: 14 }; // percentage from bottom

        this.init();
    }

    init() {
        // Fetch character catalog on startup
        this.refreshCharacterVault();
        this.setupStageActorDragging();
    }

    /**
     * 📂 1. Open / Close Character Studio Modal
     */
    openModal() {
        const modal = document.getElementById('modal-character-studio');
        if (modal) {
            modal.style.display = 'flex';
            this.syncFormWithActiveCharacter();
        }
    }

    closeModal() {
        const modal = document.getElementById('modal-character-studio');
        if (modal) modal.style.display = 'none';
    }

    /**
     * 🔀 2. Mode Switching: [🅰️ Prompt] ⇄ [🅱️ 4-Photos] ⇄ [🎬 Mocap]
     */
    switchMode(mode) {
        this.activeMode = mode;
        const tabPrompt = document.getElementById('tab-char-prompt');
        const tabPhotos = document.getElementById('tab-char-photos');
        const tabMocap = document.getElementById('tab-char-mocap');
        const secPrompt = document.getElementById('section-char-prompt');
        const secPhotos = document.getElementById('section-char-photos');
        const secMocap = document.getElementById('section-char-mocap');
        const btnExec = document.getElementById('btn-exec-char-gen');

        [tabPrompt, tabPhotos, tabMocap].forEach(t => t && t.classList.remove('active'));
        if (secPrompt) secPrompt.style.display = 'none';
        if (secPhotos) secPhotos.style.display = 'none';
        if (secMocap) secMocap.style.display = 'none';

        if (mode === 'prompt') {
            if (tabPrompt) tabPrompt.classList.add('active');
            if (secPrompt) secPrompt.style.display = 'block';
            if (btnExec) btnExec.innerHTML = '<i class="fa-solid fa-bolt"></i> ⚡ 4面高精度切り抜き ＆ 透過アセット生成';
        } else if (mode === 'photos') {
            if (tabPhotos) tabPhotos.classList.add('active');
            if (secPhotos) secPhotos.style.display = 'block';
            if (btnExec) btnExec.innerHTML = '<i class="fa-solid fa-bolt"></i> ⚡ 実在4枚写真から正規化・透過生成';
        } else if (mode === 'mocap') {
            if (tabMocap) tabMocap.classList.add('active');
            if (secMocap) secMocap.style.display = 'flex';
            if (btnExec) btnExec.innerHTML = '<i class="fa-solid fa-person-running"></i> 🎬 骨格抽出 ＆ Gemma 4 演技トランスファー実行';
        }
    }

    /**
     * 📥 3. Mode B: Handling 4-Photo Drag & Drop
     */
    handlePhotoDrop(e, viewName) {
        e.preventDefault();
        e.stopPropagation();
        const dropzone = document.getElementById(`dropzone-${viewName}`);
        if (dropzone) dropzone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            this.readAndSetPhoto(files[0], viewName);
        }
    }

    handlePhotoSelect(input, viewName) {
        if (input.files && input.files.length > 0) {
            this.readAndSetPhoto(input.files[0], viewName);
        }
    }

    readAndSetPhoto(file, viewName) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const dataUri = event.target.result;
            this.uploadedPhotos[viewName] = dataUri;

            // Update preview inside dropzone
            const dropzone = document.getElementById(`dropzone-${viewName}`);
            if (dropzone) {
                dropzone.innerHTML = `
                    <div style="position:relative; width:100%; height:100%;">
                        <img src="${dataUri}" style="width:100%; height:120px; object-fit:contain; border-radius:3px;">
                        <span style="position:absolute; bottom:2px; right:2px; background:rgba(0,0,0,0.8); color:var(--accent-cyan); font-size:0.48rem; padding:1px 3px; border-radius:2px;">✅ 読込済</span>
                    </div>
                `;
            }
            this.updatePreviewCanvases();
        };
        reader.readAsDataURL(file);
    }

    /**
     * 👔 4. Virtual Wardrobe & EC Product Image Ingestion
     */
    handleCostumeDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        const dropzone = document.getElementById('dropzone-costume-ec');
        if (dropzone) dropzone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            const file = files[0];
            const reader = new FileReader();
            reader.onload = (evt) => {
                this.addCostumeItem("EC取り込みアイテム", evt.target.result, ["#EC衣装", "#新着アウター"]);
            };
            reader.readAsDataURL(file);
        } else {
            // Check text/URI
            const text = e.dataTransfer.getData('text');
            if (text && text.startsWith('http')) {
                this.addCostumeItem("ECリンク衣装", text, ["#EC商品", "#Webカタログ"]);
            }
        }
    }

    addCostumeItem(title, imgUrl, tags) {
        const tray = document.getElementById('wardrobe-items-tray');
        if (!tray) return;

        const card = document.createElement('div');
        card.className = 'wardrobe-item-card active';
        card.onclick = () => this.selectCostumeCard(card, title);
        card.innerHTML = `
            <img src="${imgUrl}" style="width:40px; height:40px; object-fit:cover; border-radius:3px; background:#070a14;">
            <div style="font-size:0.52rem; font-weight:700; color:#fff; text-overflow:ellipsis; overflow:hidden; white-space:nowrap; max-width:60px;">${title}</div>
            <div style="font-size:0.45rem; color:var(--accent-cyan);">${tags.join(' ')}</div>
        `;
        tray.insertBefore(card, tray.firstChild);

        // Notify user
        const statusMsg = document.getElementById('char-studio-status');
        if (statusMsg) statusMsg.textContent = `✨ EC衣装「${title}」を取り込み、キャラクターへ装着可能にしました！`;
    }

    selectCostumeCard(el, title) {
        document.querySelectorAll('.wardrobe-item-card').forEach(c => c.classList.remove('active'));
        el.classList.add('active');
        const tagInput = document.getElementById('char-costume-tag');
        if (tagInput) tagInput.value = title;
    }

    /**
     * 🚀 5. Execute Backend Generation & Cutout
     */
    async executeCharacterGeneration() {
        const statusMsg = document.getElementById('char-studio-status');
        const btn = document.getElementById('btn-exec-char-gen');
        if (btn) btn.disabled = true;
        if (statusMsg) statusMsg.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> 高精度エッジ切り抜き ＆ Defringe処理を実行中...`;

        try {
            const nameJa = document.getElementById('char-input-name').value || "新規キャスト";
            const nameEn = document.getElementById('char-input-name-en').value || "New Actor";
            const age = parseInt(document.getElementById('char-input-age').value || "25");
            const gender = document.getElementById('char-select-gender').value || "male";
            const heightM = parseFloat(document.getElementById('char-input-height').value || "1.78");
            const build = document.getElementById('char-select-build').value || "athletic";
            const costumeTag = document.getElementById('char-costume-tag').value || "カスタム衣装";
            const charId = "char_" + Date.now();

            const metadata = {
                name: nameJa,
                name_en: nameEn,
                age: age,
                gender: gender,
                height_m: heightM,
                build: build,
                costume_tags: [costumeTag],
                voice_profile: "Aoede"
            };

            let result = null;

            if (this.activeMode === 'mocap') {
                await this.executeMocapExtraction();
                if (btn) btn.disabled = false;
                return;
            } else if (this.activeMode === 'photos') {
                // Mode B: Process 4 separate photos
                if (!this.uploadedPhotos.front) {
                    alert("⚠️ 少なくとも正面（Front）の写真をアップロードしてください。");
                    if (btn) btn.disabled = false;
                    return;
                }
                const res = await fetch('/api/character/process_photos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        char_id: charId,
                        photos: this.uploadedPhotos,
                        metadata: metadata
                    })
                });
                const data = await res.json();
                if (!data.success) throw new Error(data.error);
                result = data.character;
            } else {
                // Mode A: Render high-res procedural 4-view turnaround sheet
                const sheetCanvas = document.createElement('canvas');
                sheetCanvas.width = 1600;
                sheetCanvas.height = 800;
                const ctx = sheetCanvas.getContext('2d');
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, sheetCanvas.width, sheetCanvas.height);

                // Draw procedural 4 views
                const colW = 400;
                ['front', 'right', 'back', 'left'].forEach((v, idx) => {
                    ctx.save();
                    ctx.translate(idx * colW, 0);
                    if (window.CharacterTurnaroundEngine) {
                        window.CharacterTurnaroundEngine.renderCleanProceduralActor(ctx, colW, 800, v);
                    }
                    ctx.restore();
                });

                const sheetDataUri = sheetCanvas.toDataURL('image/png');
                const res = await fetch('/api/character/process_sheet', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        char_id: charId,
                        sheet_image: sheetDataUri,
                        metadata: metadata
                    })
                });
                const data = await res.json();
                if (!data.success) throw new Error(data.error);
                result = data.character;
            }

            this.activeCharacterData = result;
            this.activeCharacterId = result.id;

            // Refresh UI Preview
            this.displayTransparentResults(result);
            await this.refreshCharacterVault();

            if (statusMsg) {
                statusMsg.innerHTML = `✅ 32bit完全透過アセット生成完了！白フチ消去済み。キャスト台帳に保存されました。`;
            }
        } catch (err) {
            console.error("Character generation failed:", err);
            if (statusMsg) statusMsg.innerHTML = `❌ エラー: ${err.message}`;
        } finally {
            if (btn) btn.disabled = false;
        }
    }

    /**
     * 🔍 6. Display 32bit Transparent PNGs in 4-View Preview
     */
    displayTransparentResults(charData) {
        if (!charData || !charData.views) return;
        ['front', 'right', 'back', 'left'].forEach(view => {
            const imgEl = document.getElementById(`preview-matte-${view}`);
            if (imgEl && charData.views[view]) {
                imgEl.src = `${charData.views[view]}?t=${Date.now()}`;
            }
        });

        // Update Defringe visual filter
        this.updateDefringeFilter();
    }

    /**
     * 🎛️ 7. Defringe Slider Update
     */
    updateDefringeFilter() {
        const slider = document.getElementById('slider-defringe-strength');
        if (slider) this.defringeStrength = parseInt(slider.value);
        const valLabel = document.getElementById('label-defringe-val');
        if (valLabel) valLabel.textContent = `${this.defringeStrength}%`;

        // Apply clean edge contrast filter to preview elements
        const sharpness = 1.0 + (this.defringeStrength / 200.0);
        ['front', 'right', 'back', 'left'].forEach(view => {
            const imgEl = document.getElementById(`preview-matte-${view}`);
            if (imgEl) {
                imgEl.style.filter = `contrast(${sharpness}) drop-shadow(0 0 1px rgba(0,0,0,0.8))`;
            }
        });

        // Also update stage actor if visible
        const stageImg = document.getElementById('stage-actor-img');
        if (stageImg) {
            stageImg.style.filter = `contrast(${sharpness}) drop-shadow(0 0 1px rgba(0,0,0,0.8))`;
        }
    }

    /**
     * 📂 8. Refresh Characters in Vault & Cockpit Buttons
     */
    async refreshCharacterVault() {
        try {
            const res = await fetch('/api/characters');
            const characters = await res.json();
            const container = document.getElementById('vault-character-grid');
            const cockpitBin = document.getElementById('cockpit-cast-buttons');

            if (container) container.innerHTML = '';
            if (cockpitBin) cockpitBin.innerHTML = '';

            characters.forEach(char => {
                // Modal Vault Card
                if (container) {
                    const card = document.createElement('div');
                    card.className = `vault-char-card ${char.id === this.activeCharacterId ? 'active' : ''}`;
                    card.onclick = () => this.selectVaultCharacter(char);
                    card.innerHTML = `
                        <div style="width:100%; height:75px; background:repeating-conic-gradient(#1e293b 0% 25%, #0f172a 0% 50%) 50% / 12px 12px; border-radius:3px; display:flex; justify-content:center; align-items:center; overflow:hidden;">
                            <img src="${char.views?.front || ''}" style="max-height:100%; object-fit:contain;">
                        </div>
                        <div style="font-size:0.56rem; font-weight:800; color:var(--accent-cyan); text-align:center; margin-top:2px;">${char.name}</div>
                        <div style="font-size:0.48rem; color:#94a3b8; text-align:center;">${char.height_m}m / ${char.build}</div>
                    `;
                    container.appendChild(card);
                }

                // Cockpit Left Panel Button
                if (cockpitBin) {
                    const btn = document.createElement('button');
                    btn.className = `btn-opt ${char.id === this.activeCharacterId ? 'active' : ''}`;
                    btn.id = `btn-cockpit-char-${char.id}`;
                    btn.onclick = () => this.selectCockpitCharacter(char);
                    btn.innerHTML = `<i class="fa-solid fa-user"></i> ${char.name}`;
                    cockpitBin.appendChild(btn);
                }
            });
        } catch (e) {
            console.warn("Failed to refresh character vault:", e);
        }
    }

    selectVaultCharacter(char) {
        this.activeCharacterId = char.id;
        this.activeCharacterData = char;
        this.displayTransparentResults(char);
        this.syncFormWithActiveCharacter();
        document.querySelectorAll('.vault-char-card').forEach(c => c.classList.remove('active'));
    }

    selectCockpitCharacter(char) {
        this.activeCharacterId = char.id;
        this.activeCharacterData = char;
        document.querySelectorAll('#cockpit-cast-buttons .btn-opt').forEach(b => b.classList.remove('active'));
        const activeBtn = document.getElementById(`btn-cockpit-char-${char.id}`);
        if (activeBtn) activeBtn.classList.add('active');

        // Update Mini turnaround canvases in cockpit
        ['front', 'right', 'back', 'left'].forEach(v => {
            const canvas = document.getElementById(`canvas-aspect-${v}`);
            if (canvas && char.views && char.views[v]) {
                const ctx = canvas.getContext('2d');
                const img = new Image();
                img.onload = () => {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                };
                img.src = char.views[v];
            }
        });

        // Update HUD
        const hudActor = document.getElementById('hud-actor-val');
        if (hudActor) hudActor.textContent = `${char.name} (${char.height_m}m / ${this.stageActorAspect})`;

        // Update stage actor if active
        if (this.stageActorActive) {
            this.updateStageActorDisplay();
        }
    }

    syncFormWithActiveCharacter() {
        if (!this.activeCharacterData) return;
        const c = this.activeCharacterData;
        const nameEl = document.getElementById('char-input-name');
        const heightEl = document.getElementById('char-input-height');
        const heightVal = document.getElementById('char-height-val');
        if (nameEl) nameEl.value = c.name || '';
        if (heightEl && c.height_m) {
            heightEl.value = c.height_m;
            if (heightVal) heightVal.textContent = `${c.height_m}m`;
        }
    }

    /**
     * 🌐 9. Main Stage Street View Summon Integration
     */
    toggleStageActor() {
        this.stageActorActive = !this.stageActorActive;
        const layer = document.getElementById('stage-actor-layer');
        const btn = document.getElementById('btn-summon-stage-actor');

        if (this.stageActorActive) {
            if (layer) layer.style.display = 'block';
            if (btn) {
                btn.classList.add('active');
                btn.innerHTML = `<i class="fa-solid fa-person-circle-check"></i> 📍 街角セットから退場`;
            }
            this.updateStageActorDisplay();
        } else {
            if (layer) layer.style.display = 'none';
            if (btn) {
                btn.classList.remove('active');
                btn.innerHTML = `<i class="fa-solid fa-person-walking-arrow-right"></i> 📍 街角セットに召喚`;
            }
        }
    }

    dismissStageActor(e) {
        if (e) e.stopPropagation();
        this.stageActorActive = false;
        const layer = document.getElementById('stage-actor-layer');
        const btn = document.getElementById('btn-summon-stage-actor');
        if (layer) layer.style.display = 'none';
        if (btn) {
            btn.classList.remove('active');
            btn.innerHTML = `<i class="fa-solid fa-person-walking-arrow-right"></i> 📍 街角セットに召喚`;
        }
    }

    cycleStageActorAspect(e) {
        if (e) e.stopPropagation();
        const cycle = { front: 'right', right: 'back', back: 'left', left: 'front' };
        this.stageActorAspect = cycle[this.stageActorAspect] || 'front';
        this.updateStageActorDisplay();
    }

    updateStageActorDisplay() {
        const imgEl = document.getElementById('stage-actor-img');
        const nameBadge = document.getElementById('stage-actor-name-badge');
        const aspectBadge = document.getElementById('stage-actor-aspect-badge');

        const aspectJa = { front: '正面', right: '右側面', back: '背面', left: '左側面' };
        if (aspectBadge) aspectBadge.textContent = aspectJa[this.stageActorAspect];

        if (this.activeCharacterData && this.activeCharacterData.views) {
            const viewUrl = this.activeCharacterData.views[this.stageActorAspect];
            if (imgEl && viewUrl) {
                imgEl.src = `${viewUrl}?t=${Date.now()}`;
            }
            if (nameBadge) {
                nameBadge.textContent = `${this.activeCharacterData.name} (${this.activeCharacterData.height_m}m)`;
            }
        } else {
            // Default placeholder
            if (imgEl) imgEl.src = `/characters/test_ren_e2e/${this.stageActorAspect}.png`;
            if (nameBadge) nameBadge.textContent = `如月 蓮 (1.80m)`;
        }

        // Apply perspective height
        const heightM = this.activeCharacterData?.height_m || 1.80;
        const pixelHeight = Math.round(heightM * 240 * this.stageActorScale);
        if (imgEl) imgEl.style.height = `${pixelHeight}px`;

        // Update ground shadow width proportional to actor scale
        const shadow = document.getElementById('stage-actor-shadow');
        if (shadow) shadow.style.width = `${Math.round(140 * this.stageActorScale)}px`;
    }

    /**
     * 🖱️ 10. Drag & Drop & Depth Wheel on Street View Stage
     */
    setupStageActorDragging() {
        const entity = document.getElementById('stage-actor-entity');
        const container = document.getElementById('stage-viewport-container');
        if (!entity || !container) return;

        let isDragging = false;
        let startX, startY;

        entity.addEventListener('mousedown', (e) => {
            if (e.target.tagName === 'BUTTON') return;
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            entity.style.cursor = 'grabbing';
            e.preventDefault();
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const rect = container.getBoundingClientRect();
            const deltaX = (e.clientX - startX) / rect.width * 100;
            const deltaY = (startY - e.clientY) / rect.height * 100;

            this.stageActorPos.x = Math.max(10, Math.min(90, this.stageActorPos.x + deltaX));
            this.stageActorPos.y = Math.max(5, Math.min(60, this.stageActorPos.y + deltaY));

            entity.style.left = `${this.stageActorPos.x}%`;
            entity.style.bottom = `${this.stageActorPos.y}%`;

            startX = e.clientX;
            startY = e.clientY;
        });

        window.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                entity.style.cursor = 'grab';
            }
        });

        // Mouse wheel over actor to adjust depth scale (Near/Far perspective)
        entity.addEventListener('wheel', (e) => {
            e.preventDefault();
            const zoomDelta = e.deltaY < 0 ? 0.05 : -0.05;
            this.stageActorScale = Math.max(0.4, Math.min(2.2, this.stageActorScale + zoomDelta));
            this.updateStageActorDisplay();
        });
    }

    /**
     * 🎬 9. Mocap & Pose-Acting Transfer Handlers
     */
    handleMocapDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        const dropzone = document.getElementById('dropzone-mocap-video');
        if (dropzone) dropzone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            this.readAndSetMocapVideo(files[0]);
        }
    }

    handleMocapSelect(input) {
        if (input.files && input.files.length > 0) {
            this.readAndSetMocapVideo(input.files[0]);
        }
    }

    readAndSetMocapVideo(file) {
        const label = document.getElementById('mocap-file-label');
        if (label) label.textContent = `🎥 読込中: ${file.name} (${(file.size / 1024 / 1024).toFixed(1)}MB)`;

        const reader = new FileReader();
        reader.onload = (event) => {
            this.uploadedMocapVideo = event.target.result;
            if (label) label.innerHTML = `<span style="color:var(--accent-cyan);">✅ 読込完了: ${file.name}</span>`;
            const statusMsg = document.getElementById('char-studio-status');
            if (statusMsg) statusMsg.innerHTML = `💡 動画を読み込みました。下の「骨格抽出＆演技トランスファー実行」ボタンを押してください。`;
        };
        reader.readAsDataURL(file);
    }

    async executeMocapExtraction() {
        const statusMsg = document.getElementById('char-studio-status');
        const startSec = parseFloat(document.getElementById('mocap-input-start').value || '0.0');
        const endSec = parseFloat(document.getElementById('mocap-input-end').value || '3.0');

        if (statusMsg) statusMsg.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Google MediaPipe Pose骨格抽出 ＆ Gemma 4演技解析を実行中...`;

        const payload = {
            start_sec: startSec,
            end_sec: endSec,
            sample_fps: 10
        };

        if (this.uploadedMocapVideo) {
            payload.video_base64 = this.uploadedMocapVideo;
        }

        const res = await fetch('/api/mocap/extract_motion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!data.success) throw new Error(data.error || 'Mocap extraction failed');

        // Display results in UI
        const resultCard = document.getElementById('mocap-result-card');
        const dirEl = document.getElementById('mocap-acting-direction');
        const veoEl = document.getElementById('mocap-veo-prompt');
        const latencyEl = document.getElementById('mocap-latency-badge');

        if (resultCard) resultCard.style.display = 'flex';
        if (dirEl) dirEl.textContent = `🎭 ト書き: ${data.acting_direction?.stage_direction || '演技解析完了'}`;
        if (veoEl) veoEl.textContent = `🎥 Veo 3.1: ${data.acting_direction?.veo_prompt || ''}`;
        if (latencyEl) latencyEl.textContent = `${data.acting_direction?.latencyMs || 8.5}ms ($0) | ${data.motion_summary?.motion_type || 'Active'}`;

        if (statusMsg) statusMsg.innerHTML = `<span style="color:var(--accent-cyan); font-weight:800;">✅ 演技解析完了！</span> Gemma 4が演技ト書きとVeoプロンプトを自律生成しました。`;

        // Apply motion to current active actor
        await fetch('/api/mocap/apply_to_actor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                character_id: this.activeCharacterId || 'test_idol_e2e',
                motion_data: data
            })
        });
    }
}

// Global instance attached to window
window.CharacterStudioUI = new CharacterStudioUI();
