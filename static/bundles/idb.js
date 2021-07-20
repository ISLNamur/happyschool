var idb=function(e){"use strict";const t=(e,t)=>t.some((t=>e instanceof t));let n,r;const o=new WeakMap,s=new WeakMap,a=new WeakMap,i=new WeakMap,c=new WeakMap;let u={get(e,t,n){if(e instanceof IDBTransaction){if("done"===t)return s.get(e);if("objectStoreNames"===t)return e.objectStoreNames||a.get(e);if("store"===t)return n.objectStoreNames[1]?void 0:n.objectStore(n.objectStoreNames[0])}return p(e[t])},set:(e,t,n)=>(e[t]=n,!0),has:(e,t)=>e instanceof IDBTransaction&&("done"===t||"store"===t)||t in e};function d(e){u=e(u)}function f(e){return"function"==typeof e?function(e){return e!==IDBDatabase.prototype.transaction||"objectStoreNames"in IDBTransaction.prototype?(r||(r=[IDBCursor.prototype.advance,IDBCursor.prototype.continue,IDBCursor.prototype.continuePrimaryKey])).includes(e)?function(...t){return e.apply(l(this),t),p(o.get(this))}:function(...t){return p(e.apply(l(this),t))}:function(t,...n){const r=e.call(l(this),t,...n);return a.set(r,t.sort?t.sort():[t]),p(r)}}(e):(e instanceof IDBTransaction&&function(e){if(s.has(e))return;const t=new Promise(((t,n)=>{const r=()=>{e.removeEventListener("complete",o),e.removeEventListener("error",s),e.removeEventListener("abort",s)},o=()=>{t(),r()},s=()=>{n(e.error||new DOMException("AbortError","AbortError")),r()};e.addEventListener("complete",o),e.addEventListener("error",s),e.addEventListener("abort",s)}));s.set(e,t)}(e),t(e,n||(n=[IDBDatabase,IDBObjectStore,IDBIndex,IDBCursor,IDBTransaction]))?new Proxy(e,u):e)}function p(e){if(e instanceof IDBRequest)return function(e){const t=new Promise(((t,n)=>{const r=()=>{e.removeEventListener("success",o),e.removeEventListener("error",s)},o=()=>{t(p(e.result)),r()},s=()=>{n(e.error),r()};e.addEventListener("success",o),e.addEventListener("error",s)}));return t.then((t=>{t instanceof IDBCursor&&o.set(t,e)})).catch((()=>{})),c.set(t,e),t}(e);if(i.has(e))return i.get(e);const t=f(e);return t!==e&&(i.set(e,t),c.set(t,e)),t}const l=e=>c.get(e),D=["get","getKey","getAll","getAllKeys","count"],I=["put","add","delete","clear"],B=new Map;function b(e,t){if(!(e instanceof IDBDatabase)||t in e||"string"!=typeof t)return;if(B.get(t))return B.get(t);const n=t.replace(/FromIndex$/,""),r=t!==n,o=I.includes(n);if(!(n in(r?IDBIndex:IDBObjectStore).prototype)||!o&&!D.includes(n))return;const s=async function(e,...t){const s=this.transaction(e,o?"readwrite":"readonly");let a=s.store;r&&(a=a.index(t.shift()));const i=await a[n](...t);return o&&await s.done,i};return B.set(t,s),s}d((e=>({...e,get:(t,n,r)=>b(t,n)||e.get(t,n,r),has:(t,n)=>!!b(t,n)||e.has(t,n)})));const v=["continue","continuePrimaryKey","advance"],g={},y=new WeakMap,h=new WeakMap,w={get(e,t){if(!v.includes(t))return e[t];let n=g[t];return n||(n=g[t]=function(...e){y.set(this,h.get(this)[t](...e))}),n}};async function*m(...e){let t=this;if(t instanceof IDBCursor||(t=await t.openCursor(...e)),!t)return;t=t;const n=new Proxy(t,w);for(h.set(n,t),c.set(n,l(t));t;)yield n,t=await(y.get(n)||t.continue()),y.delete(n)}function E(e,n){return n===Symbol.asyncIterator&&t(e,[IDBIndex,IDBObjectStore,IDBCursor])||"iterate"===n&&t(e,[IDBIndex,IDBObjectStore])}return d((e=>({...e,get:(t,n,r)=>E(t,n)?m:e.get(t,n,r),has:(t,n)=>E(t,n)||e.has(t,n)}))),e.deleteDB=function(e,{blocked:t}={}){const n=indexedDB.deleteDatabase(e);return t&&n.addEventListener("blocked",(()=>t())),p(n).then((()=>{}))},e.openDB=function(e,t,{blocked:n,upgrade:r,blocking:o,terminated:s}={}){const a=indexedDB.open(e,t),i=p(a);return r&&a.addEventListener("upgradeneeded",(e=>{r(p(a.result),e.oldVersion,e.newVersion,p(a.transaction))})),n&&a.addEventListener("blocked",(()=>n())),i.then((e=>{s&&e.addEventListener("close",(()=>s())),o&&e.addEventListener("versionchange",(()=>o()))})).catch((()=>{})),i},e.unwrap=l,e.wrap=p,e}({});