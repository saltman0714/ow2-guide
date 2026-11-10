const CACHE = 'ow2-guide-v4';
const CORE = ['./', './index.html', './manifest.webmanifest', './icon.svg'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(CORE)));
  self.skipWaiting();
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))));
  self.clients.claim();
});
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.endsWith('.json') || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/ow2-guide/')) {
    event.respondWith(fetch(event.request).then(response => {
      if (response.ok) {
        const clone = response.clone();
        event.waitUntil(caches.open(CACHE).then(cache => cache.put(event.request, clone)));
      }
      return response;
    }).catch(() => caches.match(event.request)));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
    if (response.ok) {
      const clone = response.clone();
      event.waitUntil(caches.open(CACHE).then(cache => cache.put(event.request, clone)));
    }
    return response;
  })));
});
