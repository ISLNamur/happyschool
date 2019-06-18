importScripts('/static/bundles/AssetsManager.js');
importScripts('/static/bundles/idb.js');

let assetsManager = new AssetsManager();
let urlToCache = assetsManager.cacheEntries.filter(url => url.includes("commons") || url.includes("student_absence") || url.includes("polyfill"));
urlToCache.push("/student_absence/");
urlToCache.push("/student_absence/api/absence_count/");
const hash = urlToCache[0].split("-")[1].split(".")[0];


// Create an Annuaire.
const dbPromise = idb.openDB("annuaire", 1, {
    upgrade(db, oldVersion, newVersion, transaction) {
        console.log("upgrading db");
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
    if (event.request.url.includes("/student_absence/api/students_classes/")) {
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
                        classes[classe_key].students.push(data[s].matricule);
                    } else {
                        classes[classe_key] = {students: [data[s].matricule], id: data[s].classe.id};
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
    } else if (event.request.url.includes("/core/ping/")) {
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
                    return caches.match('/student_absence/');
                });
            })
        );
    }
    }
);
