const CACHE_NAME = 'portal-cursos-v8';

self.addEventListener('install', (e) => {
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        console.log('Removendo cache antigo:', key);
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Network-First: sempre busca a versão mais recente na rede!
self.addEventListener('fetch', (e) => {
    // Para requisições de API (Gist, GitHub), não interceptar com cache do Service Worker
    if (e.request.url.includes('api.github.com') || e.request.url.includes('drive.google.com')) {
        return;
    }

    e.respondWith(
        fetch(e.request)
            .then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(e.request, responseClone);
                    });
                }
                return networkResponse;
            })
            .catch(() => caches.match(e.request))
    );
});