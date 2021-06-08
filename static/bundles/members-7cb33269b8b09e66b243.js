(()=>{"use strict";var e,t={"./assets/js/members.js":(e,t,r)=>{var a=r("./node_modules/vue/dist/vue.common.prod.js"),o=r.n(a),n=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("app-menu",{attrs:{"menu-info":e.menuInfo}}),e._v(" "),r("b-container",{},[r("h1",[e._v("Gestion du personnels")]),e._v(" "),r("b-row",[r("p",{staticClass:"card-text mb-2 ml-3"},[r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addGroupModal",modifiers:{addGroupModal:!0}}],attrs:{variant:"primary"}},[r("icon",{attrs:{name:"plus",scale:"1"}}),e._v("\n                    Ajouter un groupe\n                ")],1)],1)]),e._v(" "),r("b-row",[r("b-col",[r("b-card-group",{attrs:{columns:""}},[r("b-card",{attrs:{header:"<b>Secrétaires</b>"}},[r("b-list-group",e._l(e.secretary,(function(t){return r("b-list-group-item",{key:t.pk},[e._v("\n                                "+e._s(t.last_name)+" "+e._s(t.first_name)+"\n                            ")])})),1)],1),e._v(" "),r("b-card",[r("div",{attrs:{slot:"header"},slot:"header"},[r("b",[e._v("Autres personnels")]),e._v(" "),r("icon",{attrs:{id:"others-info",name:"info-circle",color:"blue",scale:"1"}}),e._v(" "),r("b-tooltip",{attrs:{target:"others-info",title:"Personnes responsables"}})],1),e._v(" "),r("b-list-group",e._l(e.others,(function(t){return r("b-list-group-item",{directives:[{name:"b-popover",rawName:"v-b-popover.hover",value:t.email,expression:"item.email",modifiers:{hover:!0}}],key:t.pk,staticClass:"d-flex justify-content-between align-items-center"},[e._v("\n                                "+e._s(t.last_name)+" "+e._s(t.first_name)+"\n                                "),r("div",[r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addModal",modifiers:{addModal:!0}}],attrs:{variant:"light"},on:{click:function(r){return e.fillModal(t)}}},[r("icon",{attrs:{name:"edit",scale:"1",color:"green"}})],1),e._v(" "),r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.deleteModal",modifiers:{deleteModal:!0}}],staticClass:"card-link",attrs:{variant:"light"},on:{click:function(r){e.currentItem=t}}},[r("icon",{attrs:{name:"remove",scale:"1",color:"red"}})],1)],1)])})),1),e._v(" "),r("p",{staticClass:"card-text mt-2"},[r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addModal",modifiers:{addModal:!0}}],attrs:{variant:"light"}},[r("icon",{attrs:{name:"plus",scale:"1",color:"green"}}),e._v("\n                                Ajouter\n                            ")],1)],1)],1),e._v(" "),e._l(e.groups,(function(t){return r("b-card",{key:t.id},[r("div",{attrs:{slot:"header"},slot:"header"},[r("b",[e._v(e._s(t.name))]),e._v(" "),r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.deleteGroupModal",modifiers:{deleteGroupModal:!0}}],staticClass:"card-link",attrs:{variant:"light"},on:{click:function(r){e.currentGroup=t}}},[r("icon",{attrs:{name:"remove",scale:"1",color:"red"}})],1)],1),e._v(" "),r("b-list-group",e._l(e.otherEmails[t.id],(function(t){return r("b-list-group-item",{directives:[{name:"b-popover",rawName:"v-b-popover.hover",value:t.email,expression:"p.email",modifiers:{hover:!0}}],key:t.id,staticClass:"d-flex justify-content-between align-items-center"},[e._v("\n                                "+e._s(t.last_name)+" "+e._s(t.first_name)+"\n                                "),r("div",[r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addModal",modifiers:{addModal:!0}}],attrs:{variant:"light"},on:{click:function(r){return e.fillModal(t)}}},[r("icon",{attrs:{name:"edit",scale:"1",color:"green"}})],1),e._v(" "),r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.deleteModal",modifiers:{deleteModal:!0}}],staticClass:"card-link",attrs:{variant:"light"},on:{click:function(r){e.currentItem=t}}},[r("icon",{attrs:{name:"remove",scale:"1",color:"red"}})],1)],1)])})),1),e._v(" "),r("p",{staticClass:"card-text mt-2"},[r("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addModal",modifiers:{addModal:!0}}],attrs:{variant:"light"},on:{click:function(r){e.group=t.id}}},[r("icon",{attrs:{name:"plus",scale:"1",color:"green"}}),e._v("\n                                Ajouter\n                            ")],1)],1)],1)}))],2)],1)],1)],1),e._v(" "),r("b-modal",{attrs:{id:"deleteModal","cancel-title":"Annuler","hide-header":"",centered:""},on:{ok:e.deleteCoreEntry}},[e._v("\n        Êtes-vous sûr de vouloir supprimer "+e._s(e.currentItem.last_name)+" "+e._s(e.currentItem.first_name)+" ?\n    ")]),e._v(" "),r("b-modal",{attrs:{id:"deleteGroupModal","cancel-title":"Annuler","hide-header":"",centered:""},on:{ok:e.deleteGroup}},[e._v("\n        Êtes-vous sûr de vouloir supprimer "+e._s(e.currentGroup.name)+" ?\n    ")]),e._v(" "),r("b-modal",{ref:"addGroupModal",attrs:{id:"addGroupModal","cancel-title":"Annuler",title:"Ajouter un groupe",centered:""},on:{ok:e.addGroup,hidden:e.resetGroupModal}},[r("b-form",[r("b-form-input",{attrs:{type:"text",placeholder:"Nom du groupe"},model:{value:e.groupName,callback:function(t){e.groupName=t},expression:"groupName"}})],1)],1),e._v(" "),r("b-modal",{ref:"addModal",attrs:{id:"addModal","cancel-title":"Annuler",title:"Ajouter une personne","ok-title":"Ajouter",centered:""},on:{ok:e.addEntry,hidden:e.resetModal}},[r("form",[r("b-form-input",{attrs:{type:"text",placeholder:"Nom",id:"last_name","aria-describedby":"lastNameFeedback",state:e.inputStates.last_name},model:{value:e.last_name,callback:function(t){e.last_name=t},expression:"last_name"}}),e._v(" "),r("b-form-invalid-feedback",{attrs:{id:"lastNameFeedback"}},[e._v("\n                "+e._s(e.errorMsg("last_name"))+"\n            ")]),e._v(" "),r("b-form-input",{attrs:{type:"text",placeholder:"Prénom",id:"first_name","aria-describedby":"firstNameFeedback",state:e.inputStates.first_name},model:{value:e.first_name,callback:function(t){e.first_name=t},expression:"first_name"}}),e._v(" "),r("b-form-invalid-feedback",{attrs:{id:"firstNameFeedback"}},[e._v("\n                "+e._s(e.errorMsg("first_name"))+"\n            ")]),e._v(" "),r("b-form-input",{attrs:{type:"email",placeholder:"Email",id:"email","aria-describedby":"emailFeedback",state:e.inputStates.email},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}}),e._v(" "),r("b-form-invalid-feedback",{attrs:{id:"emailFeedback"}},[e._v("\n                "+e._s(e.errorMsg("email"))+"\n            ")])],1)])],1)};n._withStripped=!0;var i=r("./node_modules/bootstrap-vue/esm/index.js"),s=(r("./node_modules/bootstrap-vue/dist/bootstrap-vue.css"),r("./node_modules/axios/index.js")),l=r.n(s),d=(r("./node_modules/vue-awesome/icons/index.js"),r("./node_modules/vue-awesome/components/Icon.vue")),m=r("./assets/common/menu.vue");o().use(i.ZPm),o().component("icon",d.Z);const u={data:function(){return{menuInfo:{},secretary:[],others:[],groups:[],otherEmails:{},currentItem:{},currentGroup:{},last_name:"",first_name:"",groupName:"",email:"",pk:null,group:null,errors:{},inputStates:{email:null,last_name:null,first_name:null},mail_notification:!0}},watch:{errors:function(e){var t=["email","last_name","first_name"];for(var r in t)this.inputStates[t[r]]=t[r]in e?0==e[t[r]].length:null}},methods:{errorMsg:function(e){return e in this.errors?this.errors[e][0]:""},fillModal:function(e){this.last_name=e.last_name,this.first_name=e.first_name,this.email=e.email,this.pk="group"in e?e.id:e.pk,"group"in e&&(this.group=e.group)},resetModal:function(){this.last_name="",this.first_name="",this.email="",this.pk=null,this.group=null},resetGroupModal:function(){this.groupName=""},loadCorePeople:function(e){var t=this,r={person_type:e};l().get("/core/api/members",{params:r}).then((function(r){t[e]=r.data.results}))},loadOtherPeople:function(){var e=this;l().get("/mail_notification/api/other_email/").then((function(t){var r=function(r){var a=e.groups[r].id,n=t.data.results.filter((function(e){return e.group===a}));o().set(e.otherEmails,a,n)};for(var a in e.groups)r(a)})).catch((function(e){console.log(e)}))},loadGroups:function(){var e=this;l().get("/mail_notification/api/other_email_group/").then((function(t){e.groups=t.data.results,e.loadOtherPeople()}))},deleteCoreEntry:function(){var e=this,t=!("group"in this.currentItem),r=t?"/core/api/members/":"/mail_notification/api/other_email/",a=t?this.currentItem.pk:this.currentItem.id;l().delete(r+a,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"}).then((function(){t?e.loadCorePeople("others"):e.loadOtherPeople()})).catch((function(e){console.log(e)}))},deleteGroup:function(){var e=this,t="/mail_notification/api/other_email_group/"+this.currentGroup.id+"/";l().delete(t,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"}).then((function(){e.loadGroups()})).catch((function(e){console.log(e)}))},addGroup:function(e){var t=this;e.preventDefault();var r={name:this.groupName};l().post("/mail_notification/api/other_email_group/",r,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"}).then((function(e){var r=e.data.id;t.groups.push({id:r,name:t.groupName}),t.resetGroupModal(),t.$refs.addGroupModal.hide()})).catch((function(e){console.log(e)}))},addEntry:function(e){var t=this;e.preventDefault();var r=this,a={last_name:this.last_name,first_name:this.first_name,email:this.email};this.group&&(a.group=this.group);var o=this.group?"/mail_notification/api/other_email/":"/core/api/members/";this.pk&&(o+=this.pk.toString()+"/");var n={xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"};(this.pk?l().put(o,a,n):l().post(o,a,n)).then((function(){"group"in a?t.loadOtherPeople():t.loadCorePeople("others"),t.errors={},t.$refs.addModal.hide()})).catch((function(e){r.errors=e.response.data}))}},mounted:function(){this.menuInfo=menu,this.loadCorePeople("secretary"),this.loadCorePeople("others"),this.mail_notification&&this.loadGroups()},components:{"app-menu":m.Z}};var c=(0,r("./node_modules/vue-loader/lib/runtime/componentNormalizer.js").Z)(u,n,[],!1,null,null,null);c.options.__file="assets/core/members.vue";const p=c.exports;new(o())({el:"#vue-app",template:"<members/>",components:{Members:p}})}},r={};function a(e){var o=r[e];if(void 0!==o)return o.exports;var n=r[e]={id:e,loaded:!1,exports:{}};return t[e].call(n.exports,n,n.exports,a),n.loaded=!0,n.exports}a.m=t,e=[],a.O=(t,r,o,n)=>{if(!r){var i=1/0;for(d=0;d<e.length;d++){for(var[r,o,n]=e[d],s=!0,l=0;l<r.length;l++)(!1&n||i>=n)&&Object.keys(a.O).every((e=>a.O[e](r[l])))?r.splice(l--,1):(s=!1,n<i&&(i=n));s&&(e.splice(d--,1),t=o())}return t}n=n||0;for(var d=e.length;d>0&&e[d-1][2]>n;d--)e[d]=e[d-1];e[d]=[r,o,n]},a.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return a.d(t,{a:t}),t},a.d=(e,t)=>{for(var r in t)a.o(t,r)&&!a.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},a.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),a.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),a.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),a.j=21,(()=>{var e={21:0};a.O.j=t=>0===e[t];var t=(t,r)=>{var o,n,[i,s,l]=r,d=0;for(o in s)a.o(s,o)&&(a.m[o]=s[o]);if(l)var m=l(a);for(t&&t(r);d<i.length;d++)n=i[d],a.o(e,n)&&e[n]&&e[n][0](),e[i[d]]=0;return a.O(m)},r=self.webpackChunkhappyschool=self.webpackChunkhappyschool||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();var o=a.O(void 0,[351],(()=>a("./assets/js/members.js")));o=a.O(o)})();