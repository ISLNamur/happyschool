importScripts("/static/bundles/AssetsManager.js"),importScripts("/static/bundles/idb.js");let assetsManager=new AssetsManager,urlToCache=assetsManager.cacheEntries.filter((e=>e.includes("commons")||e.includes("student_absence")||e.includes("polyfill")));urlToCache.push("/student_absence/");const hash=urlToCache[0].split("-")[1].split(".")[0],dbPromise=idb.openDB("annuaire",1,{upgrade(e){console.log("upgrading db"),e.createObjectStore("students",{keyPath:"matricule"}),e.createObjectStore("classes")}});self.addEventListener("install",(function(e){e.waitUntil(caches.open(hash).then((function(e){return e.addAll(urlToCache)})))})),self.addEventListener("activate",(function(e){e.waitUntil(self.clients.claim(),caches.keys().then((function(e){return Promise.all(e.map((function(e){if(!e.includes(hash))return caches.delete(e)})))})))})),self.addEventListener("fetch",(function(e){if(e.request.url.includes("/student_absence/api/students_classes/"))e.respondWith(async function(){const t=await fetch(e.request).catch((()=>new Response({status:200}))),s=await t.clone().json();return dbPromise.then((e=>{console.log("updating students");const t=e.transaction("students","readwrite").objectStore("students"),n=e.transaction("classes","readwrite"),c=n.objectStore("classes");c.clear(),t.clear();let a={};for(let e in s){t.put(s[e]);const n=(s[e].classe.year+s[e].classe.letter).toUpperCase();n in a?a[n].students.push(s[e].matricule):a[n]={students:[s[e].matricule],id:s[e].classe.id}}for(let e in a)Object.prototype.hasOwnProperty.call(a,e)&&c.put(a[e],e);return n.complete})),t}());else{if(e.request.url.includes("/core/ping/"))return fetch(e.request);e.respondWith(fetch(e.request).then((t=>(caches.open(hash).then((function(s){s.put(e.request,t).catch((()=>{}))})),t.clone()))).catch((function(){return caches.match(e.request).catch((()=>caches.match("/student_absence/")))})))}}));