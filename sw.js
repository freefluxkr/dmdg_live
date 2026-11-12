const CACHE_NAME = 'dangmok-cache-v19-20261112';
const urlsToCache = [
  './manifest.json',
  './bg_waves.png',
  './logo_circle.png'
];

// 서비스 워커 설치 및 핵심 정적 리소스 선캐싱
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(
        urlsToCache.map((url) => cache.add(url))
      );
    })
  );
});

// HTML/CSS/JS는 Network-First, 기타 정적 에셋은 Stale-While-Revalidate
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const reqUrl = new URL(event.request.url);
  if (reqUrl.origin !== self.location.origin) return;

  const isDynamicDocumentOrAsset =
    event.request.mode === 'navigate' ||
    reqUrl.pathname === '/' ||
    reqUrl.pathname.endsWith('.html') ||
    reqUrl.pathname.endsWith('.css') ||
    reqUrl.pathname.endsWith('.js');

  if (isDynamicDocumentOrAsset) {
    event.respondWith(
      fetch(event.request)
        .then((networkRes) => {
          if (networkRes && networkRes.ok) {
            const resClone = networkRes.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, resClone));
          }
          return networkRes;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedRes) => {
      const fetchPromise = fetch(event.request).then((networkRes) => {
        if (networkRes && networkRes.ok) {
          const resClone = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, resClone));
        }
        return networkRes;
      }).catch(() => cachedRes);
      return cachedRes || fetchPromise;
    })
  );
});

// 오래된 캐시(v15 등) 즉시 삭제 및 활성 클라이언트 제어권 획득
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});
