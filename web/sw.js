// GENESIS Sovereign Mesh: Mobile Edge Server & DNS Shield (Service Worker)
// Runs autonomously on the smartphone device

const CACHE_NAME = 'genesis-mobile-antigravity-v2.3';
const OFFLINE_URLS = [
    '/mobile',
    '/mobile_antigravity_pwa.html',
    '/manifest.webmanifest'
];

// In-memory blacklist synced from Sovereign DNS Authority
const LOCAL_SINKHOLE_BLACKLIST = [
    'malicious-phishing-branch.xyz',
    'fake-branch-login-phishing.com'
];

self.addEventListener('install', (event) => {
    console.log('📱 [Mobile Server SW] Sovereign Mesh Edge Node Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(OFFLINE_URLS);
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    console.log('🛡️ [Mobile Server SW] Sovereign Mesh Active on Smartphone (10.0.1.20)');
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // 1. Threat Defense: Check if domain is malicious
    if (LOCAL_SINKHOLE_BLACKLIST.some(bad => url.hostname.includes(bad))) {
        console.warn(`🚨 [Mobile Server SW] Malicious domain blocked by Sovereign Shield: ${url.hostname}`);
        event.respondWith(new Response(JSON.stringify({
            status: "BLOCKED",
            reason: "SINKHOLED_TO_0.0.0.0",
            quarantine: true
        }), {
            status: 403,
            headers: { 'Content-Type': 'application/json' }
        }));
        return;
    }

    // 2. Sovereign Mesh Internal Domain Proxy (*.genesis.internal)
    if (url.hostname.endsWith('.genesis.internal')) {
        // Forward to PC Mothership or handle locally
        event.respondWith(
            fetch(event.request).catch(() => {
                return new Response(JSON.stringify({
                    node: "mobile.genesis.internal",
                    ip: "10.0.1.20",
                    status: "EDGE_OFFLINE_AUTONOMOUS",
                    message: "スマホ内蔵エッジサーバーが自律応答中"
                }), {
                    headers: { 'Content-Type': 'application/json' }
                });
            })
        );
        return;
    }

    // 3. Cache-first with network fallback for offline mobile development
    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.match(event.request).then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }
                if (event.request.mode === 'navigate') {
                    return caches.match('/mobile_antigravity_pwa.html');
                }
                return new Response('Offline: Service Worker Edge Node Active', { status: 503 });
            });
        })
    );
});
