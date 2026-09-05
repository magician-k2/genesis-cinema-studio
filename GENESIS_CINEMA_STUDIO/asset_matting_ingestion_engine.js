/**
 * ✂️ GENESIS Asset Ingestion & Auto-Matting Engine (asset_matting_ingestion_engine.js - v55)
 * - Dual Generation Pipeline: Prompt-to-Asset ✕ Real-World Photo/Camera Ingestion
 * - Automated Client-Side Background Removal (Alpha Matting & Edge Detection)
 * - Multi-Angle 4-View Synthesizer for Characters, Vehicles (Bus, Taxi, Truck), and Props
 * - Image-to-Video Multi-View Guidance Synthesizer for Google DeepMind Veo 3.1
 */

class AssetMattingIngestionEngine {
    constructor() {
        this.ingestedAssets = {
            characters: [],
            vehicles: [],
            props: []
        };
        this.activeAsset = null;
    }

    /**
     * ✂️ Perform client-side background removal & color key matting on a canvas
     * @param {HTMLCanvasElement} sourceCanvas 
     * @param {Object} options { threshold: 0.15, edgeFeather: 2, bgType: 'auto' | 'light' | 'dark' | 'green' }
     */
    processBackgroundRemoval(sourceCanvas, options = {}) {
        if (!sourceCanvas) return null;

        const width = sourceCanvas.width;
        const height = sourceCanvas.height;
        const outCanvas = (typeof document !== 'undefined') ? document.createElement('canvas') : sourceCanvas;
        outCanvas.width = width;
        outCanvas.height = height;

        const ctx = outCanvas.getContext('2d');
        ctx.drawImage(sourceCanvas, 0, 0);

        const imgData = ctx.getImageData(0, 0, width, height);
        const data = imgData.data;

        // Sample corner pixels to detect background color
        const cornerSamples = [
            [0, 0], [width - 1, 0], [0, height - 1], [width - 1, height - 1],
            [Math.floor(width / 2), 0]
        ];

        let bgR = 0, bgG = 0, bgB = 0;
        cornerSamples.forEach(([x, y]) => {
            const idx = (y * width + x) * 4;
            bgR += data[idx];
            bgG += data[idx + 1];
            bgB += data[idx + 2];
        });
        bgR /= cornerSamples.length;
        bgG /= cornerSamples.length;
        bgB /= cornerSamples.length;

        const threshold = (options.threshold !== undefined ? options.threshold : 0.22) * 255;

        // Process pixels: Alpha mask based on distance from background color
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];

            // Euclidean color distance from estimated background
            const dist = Math.sqrt(
                Math.pow(r - bgR, 2) +
                Math.pow(g - bgG, 2) +
                Math.pow(b - bgB, 2)
            );

            if (dist < threshold) {
                // Soft alpha falloff near threshold
                if (dist < threshold * 0.7) {
                    data[i + 3] = 0; // Fully transparent
                } else {
                    const alphaRatio = (dist - threshold * 0.7) / (threshold * 0.3);
                    data[i + 3] = Math.floor(data[i + 3] * alphaRatio);
                }
            }
        }

        ctx.putImageData(imgData, 0, 0);
        return outCanvas;
    }

    /**
     * 🎨 Extract dominant color palette and bounding box aspect ratio
     */
    extractAssetFeatures(canvas) {
        if (!canvas) return { dominantColor: '#0284c7', aspectRatio: 1.0, isTransparent: true };

        const ctx = canvas.getContext('2d');
        const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imgData.data;

        let totalR = 0, totalG = 0, totalB = 0, count = 0;
        let minX = canvas.width, maxX = 0, minY = canvas.height, maxY = 0;

        for (let y = 0; y < canvas.height; y++) {
            for (let x = 0; x < canvas.width; x++) {
                const idx = (y * canvas.width + x) * 4;
                const alpha = data[idx + 3];
                if (alpha > 40) { // Opaque pixel
                    totalR += data[idx];
                    totalG += data[idx + 1];
                    totalB += data[idx + 2];
                    count++;

                    if (x < minX) minX = x;
                    if (x > maxX) maxX = x;
                    if (y < minY) minY = y;
                    if (y > maxY) maxY = y;
                }
            }
        }

        const avgR = count > 0 ? Math.round(totalR / count) : 15;
        const avgG = count > 0 ? Math.round(totalG / count) : 23;
        const avgB = count > 0 ? Math.round(totalB / count) : 42;
        const hexColor = `#${((1 << 24) + (avgR << 16) + (avgG << 8) + avgB).toString(16).slice(1)}`;

        const bbWidth = Math.max(1, maxX - minX);
        const bbHeight = Math.max(1, maxY - minY);
        const aspect = bbWidth / bbHeight;

        return {
            dominantColor: hexColor,
            boundingBox: { minX, minY, maxX, maxY, width: bbWidth, height: bbHeight },
            aspectRatio: aspect,
            opaquePixelCount: count
        };
    }

    /**
     * 📥 Ingest an image or photo as a cinema asset
     * @param {string} category 'character' | 'vehicle' | 'prop'
     * @param {Object} data { name, dataUrl, canvas, customProps }
     */
    ingestAsset(category, data = {}) {
        const id = `${category}_ingest_${Date.now()}`;
        const features = data.canvas ? this.extractAssetFeatures(data.canvas) : { dominantColor: '#0284c7', aspectRatio: 1.0 };

        const newAsset = {
            id: id,
            category: category,
            nameJa: data.nameJa || (category === 'vehicle' ? '実写インポート車両' : '実写インポートキャスト'),
            nameEn: data.nameEn || (category === 'vehicle' ? 'Ingested Vehicle' : 'Ingested Actor'),
            sourceType: data.sourceType || 'photo_upload', // 'camera_capture' | 'photo_upload' | 'prompt'
            dataUrl: data.dataUrl || '',
            canvas: data.canvas || null,
            features: features,
            metadata: {
                vehicleType: data.vehicleType || 'custom_sedan', // 'city_bus', 'jpn_taxi', 'truck', 'sedan'
                dimensions: data.dimensions || { heightM: 1.75, lengthM: 4.5 },
                scale: data.scale || 1.0
            },
            createdAt: new Date().toISOString()
        };

        if (!this.ingestedAssets[category + 's']) {
            this.ingestedAssets[category + 's'] = [];
        }
        this.ingestedAssets[category + 's'].push(newAsset);
        this.activeAsset = newAsset;

        console.log(`✂️ [AssetMatting] Ingested ${category} asset: [${newAsset.nameJa}] (Dominant: ${features.dominantColor})`);
        return newAsset;
    }

    /**
     * 🎥 Synthesize Veo 3.1 Multi-View Guidance Prompt from Ingested Photo
     */
    generateVeoGuidancePrompt(asset) {
        if (!asset) asset = this.activeAsset;
        if (!asset) return { promptEn: '', promptJa: '' };

        if (asset.category === 'vehicle') {
            return {
                promptEn: `Photorealistic 4K cinematic vehicle integration. Vehicle Model: ${asset.nameEn} with authentic real-world contours, custom color palette (${asset.features.dominantColor}), reflections matching ambient lighting, driving smoothly along street coordinates with precise 360-degree turnaround consistency.`,
                promptJa: `【実写インジェスト車両 Veo 3.1 連携】
車両: ${asset.nameJa} (カラー: ${asset.features.dominantColor})
カメラ: 360°一貫性保持 空間走行合成`
            };
        } else if (asset.category === 'character') {
            return {
                promptEn: `Ultra-realistic cinematic 4K character shot. Primary Actor: ${asset.nameEn}, natural real-world face and costume consistency matching reference keyframe, wearing ${asset.features.dominantColor} styled clothing, 4-view coherent turnaround (front, profile, rear angles aligned).`,
                promptJa: `【実写インジェストキャスト Veo 3.1 連携】
主役: ${asset.nameJa} (メインカラー: ${asset.features.dominantColor})
カメラ: 4面ターンアラウンド整合 映画級質感合成`
            };
        }

        return {
            promptEn: `High-fidelity cinematic prop: ${asset.nameEn}, exact texture and form preserved.`,
            promptJa: `小道具: ${asset.nameJa}`
        };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AssetMattingIngestionEngine };
}
if (typeof window !== 'undefined') {
    window.AssetMattingIngestionEngine = new AssetMattingIngestionEngine();
}
console.log("✂️ GENESIS Asset Ingestion & Auto-Matting Engine v55 Loaded.");
