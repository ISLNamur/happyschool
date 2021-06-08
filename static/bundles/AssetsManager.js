
var AssetsManager = function() {
    this.cacheName = '1623156147154'; 
    this.cacheEntries = ['/static/bundles/absence_prof-7cb33269b8b09e66b243.js','/static/bundles/admin-7cb33269b8b09e66b243.js','/static/bundles/annuaire-7cb33269b8b09e66b243.js','/static/bundles/answer-7cb33269b8b09e66b243.js','/static/bundles/appels-7cb33269b8b09e66b243.js','/static/bundles/ask_sanctions-7cb33269b8b09e66b243.js','/static/bundles/dossier_eleve-7cb33269b8b09e66b243.js','/static/bundles/grandset-7cb33269b8b09e66b243.js','/static/bundles/home-7cb33269b8b09e66b243.js','/static/bundles/infirmerie-7cb33269b8b09e66b243.js','/static/bundles/lateness-7cb33269b8b09e66b243.js','/static/bundles/mail_answer-7cb33269b8b09e66b243.js','/static/bundles/mail_notification-7cb33269b8b09e66b243.js','/static/bundles/mail_notification_list-7cb33269b8b09e66b243.js','/static/bundles/members-7cb33269b8b09e66b243.js','/static/bundles/menu-7cb33269b8b09e66b243.js','/static/bundles/pia-7cb33269b8b09e66b243.js','/static/bundles/schedule_change-7cb33269b8b09e66b243.js','/static/bundles/student_absence-7cb33269b8b09e66b243.js','/static/bundles/student_absence_teacher-7cb33269b8b09e66b243.js','/static/bundles/polyfill-7cb33269b8b09e66b243.js','/static/bundles/commons-7cb33269b8b09e66b243.js','/static/bundles/idb.js','/static/bundles/root_sw.js','/static/bundles/student_absence_sw.js','/static/bundles/bootstrap.min.css','/static/bundles/commons-7cb33269b8b09e66b243.js.LICENSE.txt','/static/bundles/student_absence-7cb33269b8b09e66b243.js.LICENSE.txt'];
    this.hashes = ['7cb33269b8b09e66b243','idb','root_sw','student_absence_sw'];
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

