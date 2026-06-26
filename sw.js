const CACHE_NAME = 'dangmok-cache-v15';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './bg_waves.png',
  './logo_circle.png',
  './css/style.css',
  './js/db.js',
  './js/audio.js',
  './js/firebase-config.js',
  './js/app.js'
];

// 서비스 워커 설치 및 리소스 캐싱
self.addEventListener('install', (event) => {
  self.skipWaiting(); // Force activate new service worker
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// 오프라인 시 캐시 우선 전략 (Cache-First)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// 오래된 캐시 삭제
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
    })
  );
});
