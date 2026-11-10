// Compatibility cleanup for older cached versions of OW2 HERO GUIDE.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => {
  event.waitUntil(Promise.all([
    caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('ow2-guide-')).map(k => caches.delete(k)))),
    self.clients.claim()
  ]));
});
// All requests use browser networking; no offline HTML cache.
