importScripts('/static/bundles/AssetsManager.js');
importScripts('/static/bundles/idb.js');

let assetsManager = new AssetsManager();
let urlToCache = assetsManager.cacheEntries.filter(url => url.includes("commons") || url.includes("student_absence") || url.includes("polyfill"));
urlToCache.push("/student_absence/");
urlToCache.push("/student_absence/api/absence_count/");
urlToCache.push("/static/css/bootstrap4.min.css");
urlToCache.push("/static/img/logo_isln.png");

const hash = urlToCache[0].split("-")[1].split(".")[0];

// Create an Annuaire.
const dbPromise = idb.openDB("annuaire", 1, {
    upgrade(db, oldVersion, newVersion, transaction) {
        db.createObjectStore('students', {
            keyPath: 'matricule'
        });
        db.createObjectStore('classes');
    }
})

self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open(hash).then(function(cache) {
        return cache.addAll(urlToCache);
      })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
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
    if (event.request.url.includes("/annuaire/api/people/")) {
        event.respondWith(async function() {
            const response = await fetch(event.request)
            .catch(error => {
                return new Response({status: 200});
            });
            const data = await response.clone().json();
            dbPromise.then(db => {
                console.log("updating students");
                const students_tx = db.transaction('students', 'readwrite');
                const students_store = students_tx.objectStore('students');
                const classes_tx = db.transaction('classes', 'readwrite');
                const classes_store = classes_tx.objectStore('classes');
                classes = {};
                for (let s in data) {
                    // Put student.
                    students_store.put(data[s]);
                    // Get classe if any.
                    const classe_key = (data[s].classe.year + data[s].classe.letter).toUpperCase();
                    if (classe_key in classes) {
                        classes[classe_key].push(data[s].matricule);
                    } else {
                        classes[classe_key] = [data[s].matricule];
                    }
                }
                for (let classe in classes) {
                    if (classes.hasOwnProperty(classe)) {
                        classes_store.put(classes[classe], classe);
                    }
                }
                return classes_tx.complete;
            });
            return response;
          }());
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
                    return caches.match('/student_absence/');
                });
            })
        );
    }
});
