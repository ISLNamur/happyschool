(()=>{"use strict";var e,t={"./assets/js/annuaire.js":(e,t,s)=>{var n=s("./node_modules/vue/dist/vue.common.prod.js"),r=s.n(n),a=s("./node_modules/vuex/dist/vuex.esm.js"),o=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[e.loaded?e._e():s("div",{staticClass:"loading"}),e._v(" "),e.loaded?s("app-menu",{attrs:{"menu-info":e.menuInfo}}):e._e(),e._v(" "),e.loaded?s("b-container",[s("h1",[e._v("Annuaire")]),e._v(" "),s("b-row",[e.teachingsOptions.length>1?s("b-col",{attrs:{md:"2",sm:"12"}},[s("b-form-group",{attrs:{label:"Établissement(s) :"}},[s("b-form-select",{attrs:{multiple:"","select-size":3,options:e.teachingsOptions,"value-field":"id","text-field":"display_name"},model:{value:e.teachings,callback:function(t){e.teachings=t},expression:"teachings"}})],1)],1):e._e(),e._v(" "),s("b-col",[s("b-form-group",{staticClass:"ml-4",attrs:{label:"Recherche :"}},[s("multiselect",{ref:"input",attrs:{"show-no-options":!1,"internal-search":!1,options:e.searchOptions,loading:e.searchLoading,placeholder:"Rechercher un étudiant, une classe, un professeur, …","select-label":"","selected-label":"Sélectionné","deselect-label":"",label:"display","track-by":"id"},on:{"search-change":e.getSearchOptions,select:e.selected},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}},[s("span",{attrs:{slot:"noResult"},slot:"noResult"},[e._v("Aucune personne trouvée.")]),e._v(" "),s("span",{attrs:{slot:"noOptions"},slot:"noOptions"})])],1)],1)],1),e._v(" "),s("transition",{attrs:{name:"slide-right",mode:"out-in"}},[s("router-view")],1)],1):e._e()],1)};o._withStripped=!0;var i=s("./node_modules/bootstrap-vue/esm/index.js"),l=s("./node_modules/vue-multiselect/dist/vue-multiselect.min.js"),u=s.n(l),c=(s("./node_modules/vue-multiselect/dist/vue-multiselect.min.css"),s("./node_modules/vue-awesome/icons/index.js"),s("./node_modules/vue-awesome/components/Icon.vue")),d=s("./node_modules/axios/index.js"),p=s.n(d),h=s("./assets/common/menu.vue");r().use(i.ZPm),r().component("icon",c.Z);const m={data:function(){return{menuInfo:{},loaded:!1,searchId:0,teachings:[],teachingsOptions:[],search:null,searchOptions:[],searchLoading:!1}},methods:{selected:function(e){"classe"!=e.type?this.$router.push("/person/".concat(e.type,"/").concat(e.id,"/")):this.$router.push("/classe/".concat(e.id,"/"))},getSearchOptions:function(e){var t=this;this.searchId+=1;var s=this.searchId,n={query:e,teachings:this.teachings.length>0?this.teachings:this.teachingsOptions.map((function(e){return e.id})),people:"all",check_access:!1};p().post("/annuaire/api/people_or_classes/",n,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"}).then((function(n){if(t.searchId===s){var r=n.data.map((function(t){if(Number.isNaN(Number.parseInt(e[0]))){if("is_secretary"in t){var s=" —";for(var n in t.teaching)s+=" "+t.teaching[n].display_name;return{display:t.last_name+" "+t.first_name+s,id:t.matricule,type:"responsible"}}return{display:t.display,id:t.matricule,type:"student"}}var r=t;return r.type="classe",r}));t.searchOptions=r}}))},overloadInput:function(){var e=this;setTimeout((function(){var t=e.$refs.input;if(t){var s=t.$refs.search;return s.focus(),s.addEventListener("keypress",(function(s){"Enter"==s.key&&t.search&&t.search.length>1&&!isNaN(t.search)&&p().get("/annuaire/api/student/"+t.search+"/").then((function(s){s.data&&(e.$router.push("/person/student/".concat(t.search,"/")),t.search="")})).catch((function(){console.log("Aucun étudiant trouvé")}))})),s}e.overloadInput()}),300)}},mounted:function(){var e=this;p().get("/core/api/teaching/").then((function(t){e.teachingsOptions=t.data.results,e.loaded=!0})),this.menuInfo=menu,this.overloadInput()},components:{multiselect:u(),"app-menu":h.Z}};var v=s("./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js"),f=s.n(v),g=s("./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/annuaire/annuaire.vue?vue&type=style&index=0&lang=css&");f()(g.Z,{insert:"head",singleton:!1}),g.Z.locals;var b=s("./node_modules/vue-loader/lib/runtime/componentNormalizer.js"),_=(0,b.Z)(m,o,[],!1,null,null,null);_.options.__file="assets/annuaire/annuaire.vue";const y=_.exports;var j=s("./assets/annuaire/info.vue"),O=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("b-row",[s("b-col",[e.students.length>0?s("div",{staticClass:"mb-2"},[e._v("\n            Téléchargements :\n            "),s("b-button",{attrs:{target:"_blank",rel:"noopener noreferrer",href:e.getClassePhoto}},[e._v("\n                Photos de classe\n            ")]),e._v(" "),e.$store.state.settings.show_credentials?s("span",[s("b-button",{attrs:{target:"_blank",rel:"noopener noreferrer",href:e.getClasseListExcel}},[e._v("\n                    Liste des étudiants avec identifiants (excel)\n                ")]),e._v(" "),s("b-button",{attrs:{target:"_blank",rel:"noopener noreferrer",href:e.getClasseListPDF}},[e._v("\n                    Liste des étudiants avec identifiants (PDF)\n                ")])],1):e._e()],1):s("p",[e._v("\n            Il n'y a pas d'élèves dans cette classe.\n        ")]),e._v(" "),s("b-list-group",{staticClass:"text-center"},e._l(e.students,(function(t){return s("b-list-group-item",{key:t.matricule,attrs:{button:""},on:{click:function(s){return e.selectStudent(t.matricule)}}},[e._v("\n                "+e._s(t.display)+"\n            ")])})),1)],1)],1)};O._withStripped=!0;const w={props:{classe:{type:String,default:""}},data:function(){return{students:[]}},watch:{$route:function(){this.loadClasse()}},computed:{getClassePhoto:function(){return this.classe?"/annuaire/get_class_photo_pdf/"+this.classe+"/":""},getClasseListExcel:function(){return this.classe?"/annuaire/get_class_list_excel/"+this.classe+"/":""},getClasseListPDF:function(){return this.classe?"/annuaire/get_class_list_pdf/"+this.classe+"/":""}},methods:{selectStudent:function(e){this.$router.push("/person/student/".concat(e,"/"))},loadClasse:function(){var e=this,t={params:{classe:this.classe}};p().get("/annuaire/api/studentclasse/",t).then((function(t){e.students=t.data}))}},mounted:function(){this.loadClasse()}};var x=(0,b.Z)(w,O,[],!1,null,null,null);x.options.__file="assets/annuaire/classe.vue";const k=x.exports;function P(e,t){var s=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),s.push.apply(s,n)}return s}function C(e,t,s){return t in e?Object.defineProperty(e,t,{value:s,enumerable:!0,configurable:!0,writable:!0}):e[t]=s,e}const I=[{path:"/",component:y,children:[{path:"/person/:type/:matricule/",component:j.Z,props:function(e){var t=function(e){for(var t=1;t<arguments.length;t++){var s=null!=arguments[t]?arguments[t]:{};t%2?P(Object(s),!0).forEach((function(t){C(e,t,s[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(s)):P(Object(s)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(s,t))}))}return e}({},e.params);return t.matricule=Number(t.matricule),t}},{path:"/classe/:classe/",component:k,props:!0}]}];var S=s("./node_modules/vue-router/dist/vue-router.esm.js");r().use(a.ZP),r().use(S.Z);var Z=new S.Z({routes:I}),L=new a.ZP.Store({state:{settings}});new(r())({el:"#vue-app",data:{},router:Z,store:L,template:"<router-view></router-view>"})},"./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/annuaire/annuaire.vue?vue&type=style&index=0&lang=css&":(e,t,s)=>{s.d(t,{Z:()=>c});var n=s("./node_modules/css-loader/dist/runtime/api.js"),r=s.n(n),a=s("./node_modules/css-loader/dist/runtime/getUrl.js"),o=s.n(a),i=s("./static/img/spin.svg"),l=r()((function(e){return e[1]})),u=o()(i.Z);l.push([e.id,'\n.loading {\n  content: " ";\n  display: block;\n  position: absolute;\n  width: 80px;\n  height: 80px;\n  background-image: url('+u+");\n  background-size: cover;\n  left: 50%;\n  top: 50%;\n}\n",""]);const c=l}},s={};function n(e){var r=s[e];if(void 0!==r)return r.exports;var a=s[e]={id:e,loaded:!1,exports:{}};return t[e].call(a.exports,a,a.exports,n),a.loaded=!0,a.exports}n.m=t,e=[],n.O=(t,s,r,a)=>{if(!s){var o=1/0;for(u=0;u<e.length;u++){for(var[s,r,a]=e[u],i=!0,l=0;l<s.length;l++)(!1&a||o>=a)&&Object.keys(n.O).every((e=>n.O[e](s[l])))?s.splice(l--,1):(i=!1,a<o&&(o=a));i&&(e.splice(u--,1),t=r())}return t}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[s,r,a]},n.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return n.d(t,{a:t}),t},n.d=(e,t)=>{for(var s in t)n.o(t,s)&&!n.o(e,s)&&Object.defineProperty(e,s,{enumerable:!0,get:t[s]})},n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),n.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),n.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),n.j=997,(()=>{var e={997:0};n.O.j=t=>0===e[t];var t=(t,s)=>{var r,a,[o,i,l]=s,u=0;for(r in i)n.o(i,r)&&(n.m[r]=i[r]);if(l)var c=l(n);for(t&&t(s);u<o.length;u++)a=o[u],n.o(e,a)&&e[a]&&e[a][0](),e[o[u]]=0;return n.O(c)},s=self.webpackChunkhappyschool=self.webpackChunkhappyschool||[];s.forEach(t.bind(null,0)),s.push=t.bind(null,s.push.bind(s))})();var r=n.O(void 0,[351],(()=>n("./assets/js/annuaire.js")));r=n.O(r)})();