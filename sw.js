// Service Worker desativado e limpador de caches para liberar visual imediatamente
self.addEventListener('install', (e) => {
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(keys.map((k) => caches.delete(k)));
        })
    );
    self.clients.claim();
});

// Pass-through direto na rede sem interceptação
self.addEventListener('fetch', (e) => {
    return;
});
