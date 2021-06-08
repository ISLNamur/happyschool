
var AssetsManager = function() {
    this.cacheName = '1623159213745'; 
    this.cacheEntries = ['/static/bundles/absence_prof-d8fe37bee6a15eecbaa7.js','/static/bundles/admin-d8fe37bee6a15eecbaa7.js','/static/bundles/annuaire-d8fe37bee6a15eecbaa7.js','/static/bundles/answer-d8fe37bee6a15eecbaa7.js','/static/bundles/appels-d8fe37bee6a15eecbaa7.js','/static/bundles/ask_sanctions-d8fe37bee6a15eecbaa7.js','/static/bundles/dossier_eleve-d8fe37bee6a15eecbaa7.js','/static/bundles/grandset-d8fe37bee6a15eecbaa7.js','/static/bundles/home-d8fe37bee6a15eecbaa7.js','/static/bundles/infirmerie-d8fe37bee6a15eecbaa7.js','/static/bundles/lateness-d8fe37bee6a15eecbaa7.js','/static/bundles/mail_answer-d8fe37bee6a15eecbaa7.js','/static/bundles/mail_notification-d8fe37bee6a15eecbaa7.js','/static/bundles/mail_notification_list-d8fe37bee6a15eecbaa7.js','/static/bundles/members-d8fe37bee6a15eecbaa7.js','/static/bundles/menu-d8fe37bee6a15eecbaa7.js','/static/bundles/pia-d8fe37bee6a15eecbaa7.js','/static/bundles/schedule_change-d8fe37bee6a15eecbaa7.js','/static/bundles/student_absence-d8fe37bee6a15eecbaa7.js','/static/bundles/student_absence_teacher-d8fe37bee6a15eecbaa7.js','/static/bundles/polyfill-d8fe37bee6a15eecbaa7.js','/static/bundles/commons-d8fe37bee6a15eecbaa7.js','/static/bundles/idb.js','/static/bundles/root_sw.js','/static/bundles/student_absence_sw.js','/static/bundles/bootstrap.min.css','/static/bundles/commons-d8fe37bee6a15eecbaa7.js.LICENSE.txt','/static/bundles/student_absence-d8fe37bee6a15eecbaa7.js.LICENSE.txt'];
    this.hashes = ['d8fe37bee6a15eecbaa7','idb','root_sw','student_absence_sw'];
};

AssetsManager.prototype.addAllToCache = function() {
    if(!this.cacheName)
        throw new Error('Please provide cacheName in plugin options');
    const ctx = this;

    return caches.open(ctx.cacheName).then(function(cache) {
      Promise.all(
        ctx.cacheEntries.map(function(asset){cache.add(asset)})
      );
    });            
};

AssetsManager.prototype.removeNotInAssets = function() {
    var ctx = this;   
    
     return caches.open(ctx.cacheName).then(function(cache) {
          cache.keys().then(function(keys) {
              return Promise.all(
                keys.filter(function(request){
                  var erase = true;
                  var noErase = false;          
                  return ctx.cacheEntries.indexOf(request.url) >= 0 ? noErase:erase;
                }).map(function(entryToErase){          
                  cache.delete(entryToErase);                                
                })      
              );
          });
      }); 
};

