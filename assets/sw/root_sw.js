importScripts('/static/bundles/AssetsManager.js');

let assetsManager = new AssetsManager();
let urlToCache = assetsManager.cacheEntries.filter(url => url.includes("commons") || url.includes("polyfill"));

urlToCache.push("/static/css/bootstrap4.min.css");
urlToCache.push("/static/img/logo_isln.png");
urlToCache.push("/static/img/favicon.ico");
const hash = urlToCache[0].split("-")[1].split(".")[0];

self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open(hash).then(function(cache) {
        return cache.addAll(urlToCache);
      })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        self.clients.claim(),
        caches.keys().then(function(keyList) {
            return Promise.all(keyList.map(function(key) {
                if (!key.includes(hash)) {
                    return caches.delete(key);
                }
            }));
        })
    );
  });

  self.addEventListener('fetch', function(event) {
    if (event.request.url.includes("/core/ping")) {
        return fetch(event.request);
    } else {
        event.respondWith(
            fetch(event.request)
            .then(response => {
                caches.open(hash).then(function(cache) {
                    cache.put(event.request, response)
                    .catch(err => {
                        
                    });
                });
                return response.clone();
            })
            .catch(function () {
                return caches.match(event.request)
                .catch(error => {
                    return caches.match('/annuaire/');
                });
            })
        );
    }
    }
);