(()=>{"use strict";var e,t={"./assets/js/admin.js":(e,t,n)=>{var o=n("./node_modules/vue/dist/vue.common.prod.js"),s=n.n(o),a=n("./node_modules/vuex/dist/vuex.esm.js"),r=n("./node_modules/vue-router/dist/vue-router.esm.js"),i=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("b-container",[n("h3",[e._v("Page d'administration d'HappySchool")]),e._v(" "),n("b-row",[n("b-col",{attrs:{sm:"3"}},[n("b-list-group",[n("b-list-group-item",{attrs:{to:"general"}},[n("strong",[e._v("Général")])]),e._v(" "),n("b-list-group-item",{attrs:{to:"import"}},[n("strong",[e._v("Import")])]),e._v(" "),n("b-list-group-item",{attrs:{to:"photos"}},[n("strong",[e._v("Photos")])]),e._v(" "),n("b-list-group-item",{attrs:{to:"update"}},[n("strong",[e._v("Mise à jour")])]),e._v(" "),n("b-list-group-item",{attrs:{to:"annuaire"}},[n("strong",[e._v("Annuaire")])])],1)],1),e._v(" "),n("b-col",[n("router-view")],1)],1)],1)],1)};i._withStripped=!0;var l=n("./node_modules/bootstrap-vue/esm/index.js"),u=(n("./node_modules/bootstrap-vue/dist/bootstrap-vue.css"),n("./node_modules/vue-awesome/icons/index.js"),n("./node_modules/vue-awesome/components/Icon.vue"));s().use(l.ZPm),s().component("icon",u.Z);var c=n("./node_modules/vue-loader/lib/runtime/componentNormalizer.js"),d=(0,c.Z)({data:function(){return{}},mounted:function(){},components:{}},i,[],!1,null,null,null);d.options.__file="assets/core/admin.vue";const p=d.exports;var m=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("b-tabs",{attrs:{"content-class":"mt-3"}},[n("b-tab",{attrs:{title:"Étudiants"}},[n("b-row",[n("b-col",[n("h5",[e._v("Format des champs")]),e._v(" "),n("ul",[n("li",[n("strong",[e._v("Année : ")]),e._v(" L'année d'étude doit être un chiffre, seuls les deux premiers caractères sont considérés.\n                            Par exemple, 2C ou P2 seront considérés comme la deuxième année.\n                        ")]),e._v(" "),n("li",[n("strong",[e._v("Classe : ")]),e._v(" La classe peut être un ou plusieurs caractères. La classe sera automatiquement mis en minuscule dans la base de donnée,\n                            mais sera affichée en majustcule dans HappySchool.\n                        ")]),e._v(" "),n("li",[n("strong",[e._v("Date de naissance :")]),e._v(" La date de naissance doit être sous la forme yyyymmdd. Par exemple, 20020322 donnera le 22 mars 2002.")]),e._v(" "),n("li",[n("strong",[e._v("Cours :")]),e._v(" Seul le nom du cours court est nécessaire. Pour prendre entre compte plusieurs cours, il suffit que la ligne de l'étudiant soit répétée (seul le matricule est nécessaire).")])]),e._v(" "),n("b-alert",{attrs:{show:"",variant:"warning"}},[e._v("\n                        Le fichier csv soumit doit contenir l'entièreté des étudiants de l'établissement. Ceux qui ne sont pas présent (identifié\n                        par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.\n                    ")])],1)],1),e._v(" "),n("b-row",[n("b-col",[n("b-form",[n("b-form-row",[n("b-form-group",{attrs:{label:"Établissement où importer les étudiants :"}},[n("b-select",{attrs:{options:e.teachingOptions,"value-field":"id","text-field":"display_name"},model:{value:e.teaching,callback:function(t){e.teaching=t},expression:"teaching"}})],1)],1),e._v(" "),n("b-form-row",[n("b-form-checkbox",{model:{value:e.ignoreFirstLine,callback:function(t){e.ignoreFirstLine=t},expression:"ignoreFirstLine"}},[e._v("\n                                Ignorer la première ligne\n                            ")])],1),e._v(" "),n("b-form-row",[n("b-form-group",{attrs:{description:"Le fichier doit être encodé en UTF-8."}},[n("b-form-file",{attrs:{accept:".csv",placeholder:"Importer un fichier csv..."},on:{input:e.testFile},model:{value:e.file,callback:function(t){e.file=t},expression:"file"}})],1)],1)],1)],1)],1),e._v(" "),n("b-row",[n("b-col",[n("b-table",{attrs:{items:e.content,fields:e.studentColumnRawNames.slice(0,e.fields_number)},scopedSlots:e._u([e._l(e.studentColumnHeads.slice(0,e.fields_number),(function(t,o){return{key:t,fn:function(t){return[n("b-select",{key:o,attrs:{options:e.student_column_names},model:{value:e.student_columns[o],callback:function(t){e.$set(e.student_columns,o,t)},expression:"student_columns[i]"}},[n("template",{slot:"first"},[n("option",{attrs:{disabled:""},domProps:{value:null}},[e._v("\n                                        Choississez le type de colonne\n                                    ")])])],2)]}}}))],null,!0)})],1)],1),e._v(" "),e.file?n("div",[n("b-row",[n("b-btn",{on:{click:e.importStudents}},[e._v("\n                        Importer\n                    ")])],1),e._v(" "),n("b-row",{staticClass:"mt-2"},[n("b-col",[n("b-card",{attrs:{"bg-variant":"dark","text-variant":"white"}},[n("p",{staticClass:"card-text console"},[e._v("\n                                "+e._s(e.importState)+"\n                            ")])])],1)],1)],1):e._e()],1),e._v(" "),n("b-tab",{attrs:{title:"Enseignants"}},[n("b-row",[n("b-col",[n("h5",[e._v("Format des champs")]),e._v(" "),n("ul",[n("li",[n("strong",[e._v("Classe : ")]),e._v(" Le premier caractères définit l'année de la classe tandis que le reste la ou les lettres de la classe.\n                        ")]),e._v(" "),n("li",[n("strong",[e._v("Cours :")]),e._v(" Seul le nom du cours court est nécessaire. Pour prendre entre compte plusieurs cours, il suffit que la ligne de l'étudiant soit répétée (seul le matricule est nécessaire).")])]),e._v(" "),n("b-alert",{attrs:{show:"",variant:"warning"}},[e._v("\n                        Le fichier csv soumit doit contenir l'entièreté des enseignants de l'établissement. Ceux qui ne sont pas présent (identifié\n                        par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.\n                    ")])],1)],1),e._v(" "),n("b-row",[n("b-col",[n("b-form",[n("b-form-row",[n("b-form-group",{attrs:{label:"Établissement où importer les étudiants :"}},[n("b-select",{attrs:{options:e.teachingOptions,"value-field":"id","text-field":"display_name"},model:{value:e.teaching,callback:function(t){e.teaching=t},expression:"teaching"}})],1)],1),e._v(" "),n("b-form-row",[n("b-form-checkbox",{model:{value:e.ignoreFirstLine,callback:function(t){e.ignoreFirstLine=t},expression:"ignoreFirstLine"}},[e._v("\n                                Ignorer la première ligne\n                            ")])],1),e._v(" "),n("b-form-row",[n("b-form-group",{attrs:{description:"Le fichier doit être encodé en UTF-8."}},[n("b-form-file",{attrs:{accept:".csv",placeholder:"Importer un fichier csv..."},on:{input:e.testFile},model:{value:e.file,callback:function(t){e.file=t},expression:"file"}})],1)],1)],1)],1)],1),e._v(" "),n("b-row",[n("b-col",[n("b-table",{attrs:{items:e.content,fields:e.teacherColumnRawNames.slice(0,e.fields_number)},scopedSlots:e._u([e._l(e.teacherColumnHeads.slice(0,e.fields_number),(function(t,o){return{key:t,fn:function(t){return[n("b-select",{key:o,attrs:{options:e.teacher_column_names},model:{value:e.teacher_columns[o],callback:function(t){e.$set(e.teacher_columns,o,t)},expression:"teacher_columns[i]"}},[n("template",{slot:"first"},[n("option",{attrs:{disabled:""},domProps:{value:null}},[e._v("\n                                        Choississez le type de colonne\n                                    ")])])],2)]}}}))],null,!0)})],1)],1),e._v(" "),e.file?n("div",[n("b-row",[n("b-btn",{on:{click:e.importTeachers}},[e._v("\n                        Importer\n                    ")])],1),e._v(" "),n("b-row",{staticClass:"mt-2"},[n("b-col",[n("b-card",{attrs:{"bg-variant":"dark","text-variant":"white"}},[n("p",{staticClass:"card-text console"},[e._v("\n                                "+e._s(e.importState)+"\n                            ")])])],1)],1)],1):e._e()],1)],1)],1)};m._withStripped=!0;var v=n("./node_modules/axios/index.js"),h=n.n(v);s().use(l.ZPm),s().component("icon",u.Z);var f=[{value:"matricule",text:"Matricule"},{value:"last_name",text:"Nom"},{value:"first_name",text:"Prénom"},{value:"year",text:"Année"},{value:"classe_letter",text:"Classe"},{value:"course_name_short",text:"Cours (court)"},{value:"course_name_long",text:"Cours (long)"},{value:"group",text:"Groupe"},{value:"gender",text:"Genre"},{value:"scholar_year",text:"Année scolaire"},{value:"previous_class",text:"Classe précédente"},{value:"orientation",text:"Orientation"},{value:"street",text:"Rue"},{value:"postal_code",text:"Code postal"},{value:"locality",text:"Ville"},{value:"birth_date",text:"Date de naissance"},{value:"student_phone",text:"Tél. étudiant"},{value:"student_mobile",text:"GSM étudiant"},{value:"student_email",text:"Courriel étudiant"},{value:"resp_last_name",text:"Nom responsable"},{value:"resp_first_name",text:"Prénom responsable"},{value:"resp_phone",text:"Tél. responsable"},{value:"resp_mobile",text:"GSM responsable"},{value:"resp_email",text:"Courriel responsable"},{value:"father_last_name",text:"Nom pére"},{value:"father_first_name",text:"Prénom pére"},{value:"father_job",text:"Job pére"},{value:"father_phone",text:"Tél. pére"},{value:"father_mobile",text:"GSM pére"},{value:"father_email",text:"Courriel pére"},{value:"mother_last_name",text:"Nom mère"},{value:"mother_first_name",text:"Prénom mère"},{value:"mother_job",text:"Job mère"},{value:"mother_phone",text:"Tél. mère"},{value:"mother_mobile",text:"GSM mère"},{value:"mother_email",text:"Courriel mère"},{value:"doctor",text:"Médecin"},{value:"doctor_phone",text:"Tél. médecin"},{value:"mutual",text:"Mutuelle"},{value:"mutual_number",text:"Numéro mutuelle"},{value:"medical_information",text:"Info médicale"},{value:"username",text:"Nom d'utilisateur"},{value:"password",text:"Mot de passe"}],_=[{value:"matricule",text:"Matricule"},{value:"last_name",text:"Nom"},{value:"first_name",text:"Prénom"},{value:"email",text:"Courriel"},{value:"email_school",text:"Courriel de l'école"},{value:"tenure",text:"Titulariat"},{value:"classe",text:"Classe"},{value:"birth_date",text:"Date de naissance"},{value:"course_name_short",text:"Cours (court)"},{value:"course_name_long",text:"Cours (long)"},{value:"group",text:"Groupe"}];const b={data:function(){return{ignoreFirstLine:!1,teaching:null,teachingOptions:[],file:null,fields_number:0,content:[],student_columns:new Array(f.length),student_column_names:f,teacher_columns:new Array(_.length),teacher_column_names:_,studentColumnRawNames:f.map((function(e,t){return t.toString()})),studentColumnHeads:f.map((function(e,t){return"head("+t+")"})),teacherColumnRawNames:_.map((function(e,t){return t.toString()})),teacherColumnHeads:_.map((function(e,t){return"head("+t+")"})),progressSocket:null,importState:""}},methods:{testFile:function(){var e=this;this.progressSocket&&(this.progressSocket.close(),this.importState="");var t=new FormData;t.append("file",this.file),t.append("ignore_first_line",this.ignoreFirstLine),h().post("/core/api/testfile/",t,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken",headers:{"Content-Disposition":'form-data; name="file"; filename="'+this.file.name.normalize()+'"'}}).then((function(t){e.content=JSON.parse(t.data),e.content.length>0&&(e.fields_number=Object.keys(e.content[0]).length)})).catch((function(e){alert("Une erreur est survenue lors de l'analyse du fichier.\n"+e)}))},importStudents:function(){var e=new FormData,t=this;e.append("file",this.file),e.append("ignore_first_line",JSON.stringify(this.ignoreFirstLine)),e.append("teaching",this.teaching),e.append("columns",JSON.stringify(this.student_columns.slice(0,this.fields_number))),h().post("/core/api/import_students/",e,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken",headers:{"Content-Disposition":'form-data; name="file"; filename="'+this.file.name.normalize()+'"'}}).then((function(e){t.importState="Connecting to server…\n";var n="http:"===window.location.protocol?"ws":"wss";t.progressSocket=new WebSocket("".concat(n,"://").concat(window.location.host,"/ws/core/import_state/student/").concat(JSON.parse(e.data),"/")),t.progressSocket.onmessage=function(e){t.importState+=JSON.parse(e.data).status+"\n"}}))},importTeachers:function(){var e=new FormData,t=this;e.append("file",this.file),e.append("ignore_first_line",JSON.stringify(this.ignoreFirstLine)),e.append("teaching",this.teaching),e.append("columns",JSON.stringify(this.teacher_columns.slice(0,this.fields_number))),h().post("/core/api/import_teachers/",e,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken",headers:{"Content-Disposition":'form-data; name="file"; filename="'+this.file.name.normalize()+'"'}}).then((function(e){t.importState="Connecting to server…\n";var n="http:"===window.location.protocol?"ws":"wss";t.progressSocket=new WebSocket("".concat(n,"://").concat(window.location.host,"/ws/core/import_state/teacher/").concat(JSON.parse(e.data),"/")),t.progressSocket.onmessage=function(e){t.importState+=JSON.parse(e.data).status+"\n"}}))}},mounted:function(){var e=this;h().get("/core/api/teaching/").then((function(t){e.teachingOptions=t.data.results})).catch((function(e){alert(e)}))},components:{}};var g=n("./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js"),x=n.n(g),w=n("./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/core/import.vue?vue&type=style&index=0&lang=css&");x()(w.Z,{insert:"head",singleton:!1}),w.Z.locals;var S=(0,c.Z)(b,m,[],!1,null,null,null);S.options.__file="assets/core/import.vue";const k=S.exports;var y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("h4",[e._v("Paramètres généraux")]),e._v(" "),n("b-row",[n("p",[e._v("Pour le moment, HappySchool utilise principalement les pages d'administrations fournies par django.")]),e._v(" "),n("p",[n("b-button",{attrs:{href:"/admin"}},[e._v("\n                Accèder à l'interface d'administration de django\n            ")])],1)]),e._v(" "),n("b-row",[n("h5",[e._v("Établissement(s)")])]),e._v(" "),n("b-row",[n("b-col",[n("b-list-group",e._l(e.teachings,(function(t){return n("b-list-group-item",{key:t.pk},[e._v("\n                    "+e._s(t.display_name)+" ("+e._s(t.name)+")\n                    "),n("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addModal",modifiers:{addModal:!0}}],staticClass:"float-right",attrs:{variant:"light"},on:{click:function(n){e.currentTeaching=t}}},[n("icon",{attrs:{name:"edit",scale:"1",color:"green"}})],1),e._v(" "),n("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.deleteModal",modifiers:{deleteModal:!0}}],staticClass:"float-right",attrs:{variant:"light"},on:{click:function(n){e.currentTeaching=t}}},[n("icon",{attrs:{name:"remove",scale:"1",color:"red"}})],1)],1)})),1),e._v(" "),n("p",{staticClass:"card-text mt-2"},[n("b-btn",{directives:[{name:"b-modal",rawName:"v-b-modal.addModal",modifiers:{addModal:!0}}],attrs:{variant:"light"}},[n("icon",{attrs:{name:"plus",scale:"1",color:"green"}}),e._v("\n                    Ajouter\n                ")],1)],1)],1)],1),e._v(" "),n("b-row",[n("h5",[e._v("Logo")])]),e._v(" "),n("b-row",[n("b-col",[n("b-form",[n("b-form-row",[n("b-form-group",{attrs:{description:"Le logo doit être au format png."}},[n("b-form-file",{attrs:{accept:".png",placeholder:"Sélectionner le logo"},model:{value:e.logo,callback:function(t){e.logo=t},expression:"logo"}})],1)],1)],1),e._v(" "),n("p",{staticClass:"card-text mt-2"},[n("b-btn",{attrs:{variant:"light",disabled:!e.logo},on:{click:e.sendLogo}},[n("icon",{attrs:{name:"plus",scale:"1",color:"green"}}),e._v("\n                    Envoyer\n                ")],1)],1)],1)],1),e._v(" "),n("b-modal",{attrs:{id:"deleteModal","cancel-title":"Annuler","hide-header":"",centered:""},on:{ok:e.deleteTeaching,hidden:e.resetTeachings}},[e._v("\n        Êtes-vous sûr de vouloir supprimer "+e._s(e.currentTeaching.display_name)+" ("+e._s(e.currentTeaching.name)+")\n        ainsi que toutes les classes cet établissement définitivement ?\n    ")]),e._v(" "),n("b-modal",{ref:"addModal",attrs:{id:"addModal","cancel-title":"Annuler",title:"Ajouter un établissement","ok-title":"Ajouter",centered:""},on:{ok:e.setTeaching,hidden:e.resetTeachings}},[n("form",[n("b-form-input",{attrs:{type:"text",placeholder:"Nom d'affichage","aria-describedby":"displayNameFeedback",state:e.inputStates.display_name},model:{value:e.currentTeaching.display_name,callback:function(t){e.$set(e.currentTeaching,"display_name",t)},expression:"currentTeaching.display_name"}}),e._v(" "),n("b-form-invalid-feedback",{attrs:{id:"displayNameFeedback"}},[e._v("\n                "+e._s(e.errorMsg("display_name"))+"\n            ")]),e._v(" "),n("b-form-input",{attrs:{type:"text",placeholder:"Nom simple","aria-describedby":"nameFeedback",state:e.inputStates.name},model:{value:e.currentTeaching.name,callback:function(t){e.$set(e.currentTeaching,"name",t)},expression:"currentTeaching.name"}}),e._v(" "),n("b-form-invalid-feedback",{attrs:{id:"nameFeedback"}},[e._v("\n                "+e._s(e.errorMsg("name"))+"\n            ")])],1)])],1)};y._withStripped=!0,s().use(l.ZPm);var C={xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"};const j={data:function(){return{teachings:[],currentTeaching:{display_name:null,name:null},inputStates:{display_name:null,name:null},errors:{},logo:null}},watch:{errors:function(e){var t=Object.keys(this.inputStates);for(var n in t)t[n]in e?this.inputStates[t[n]]=0==e[t[n]].length:this.inputStates[t[n]]=null}},methods:{sendLogo:function(){var e=this,t=new FormData;t.append("file",this.logo),h().post("/core/api/logo/",t,C).then((function(){e.logo=null,e.$bvToast.toast("Le logo a été envoyé, actualisez la page pour voir le nouveau logo.",{variant:"success",noCloseButton:!0})})).catch((function(e){alert(e)}))},deleteTeaching:function(){h().delete("/core/api/teaching/"+this.currentTeaching.id+"/",C)},resetTeachings:function(){var e=this;this.currentTeaching={display_name:null,name:null},h().get("/core/api/teaching/").then((function(t){e.teachings=t.data.results}))},setTeaching:function(){var e=this,t="/core/api/teaching/",n="id"in this.currentTeaching;n&&(t+=this.currentTeaching.id+"/"),(n?h().put(t,this.currentTeaching,C):h().post(t,this.currentTeaching,C)).then((function(){})).catch((function(t){e.errors=t.response.data}))},errorMsg:function(e){return e in this.errors?this.errors[e][0]:""}},mounted:function(){this.resetTeachings()},components:{}};var N=(0,c.Z)(j,y,[],!1,null,null,null);N.options.__file="assets/core/general_settings.vue";const T=N.exports;var P=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("h4",[e._v("Importer des photos")]),e._v(" "),n("b-row",[n("p",[e._v('Les photos des étudiants doivent être sous la forme "numéro_de_matricule.jpg", par exemple 6143.'),n("strong",[e._v("jpg")]),e._v(".")])]),e._v(" "),n("b-row",[n("b-form",[n("b-form-row",[n("b-form-group",{attrs:{label:"Type de personne"}},[n("b-form-select",{attrs:{options:e.peopleOptions},model:{value:e.people,callback:function(t){e.people=t},expression:"people"}})],1)],1),e._v(" "),e.people?n("b-form-row",[n("b-form-group",{attrs:{label:"Photos"}},[n("b-form-file",{attrs:{accept:".jpg",placeholder:"Choisir les photos...",multiple:"","file-name-formatter":e.formatNames},model:{value:e.photos,callback:function(t){e.photos=t},expression:"photos"}})],1)],1):e._e(),e._v(" "),e.people&&e.photos.length>0?n("b-form-row",[n("b-form-group",[n("b-btn",{attrs:{disabled:e.sending},on:{click:e.uploadPhotos}},[e.sending?n("b-spinner",{attrs:{small:"",label:"Sending...",variant:"light"}}):e._e(),e._v("\n                        "+e._s(e.sendingButton)+"\n                    ")],1)],1)],1):e._e()],1)],1)],1)};P._withStripped=!0;const F={data:function(){return{people:null,peopleOptions:[{text:"Étudiants",value:"student"},{text:"Responsables (enseignants, éducateurs,…)",value:"responsible"}],photos:[],sending:!1,currentPhoto:0}},computed:{sendingButton:function(){return this.sending?"En cours d'envoi (".concat(this.currentPhoto,"/").concat(this.photos.length,")"):"Envoyer"}},methods:{formatNames:function(e){return 1===e.length?e[0].name:"".concat(e.length," photos sélectionnées")},uploadPhotos:function(){this.sending=!0,this.uploadPhoto()},uploadPhoto:function(){var e=this,t=this,n={xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken",headers:{"Content-Disposition":'form-data; name="file"; filename="'+this.photos[this.currentPhoto].name.normalize()+'"'}},o=new FormData;o.append("file",this.photos[this.currentPhoto]),o.append("people",this.people),h().post("/core/api/photo/",o,n).then((function(){e.currentPhoto+=1,e.currentPhoto==e.photos.length?(e.currentPhoto=0,e.sending=!1):e.uploadPhoto()})).catch((function(){(o=new FormData).append("file",t.photos[t.currentPhoto]),o.append("people",t.people),h().post("/core/api/photo/",o,n).then((function(){t.currentPhoto+=1,t.currentPhoto==t.photos.length?(t.currentPhoto=0,t.sending=!1):t.uploadPhoto()})).catch((function(){alert("Unable to send photo: "+t.photos[t.currentPhoto].name)}))}))}}};var O=(0,c.Z)(F,P,[],!1,null,null,null);O.options.__file="assets/core/photos.vue";const L=O.exports;var G=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("h4",[e._v("Mise à jour")]),e._v(" "),n("b-row",[n("b-alert",{attrs:{show:"",variant:"warning"}},[e._v("\n            Une fois la mise à jour terminée, veuillez redémarrer HappySchool.\n            Attention, une fois la mise à jour enclenchée, elle continuera même si la page est rafraîchie.\n        ")])],1),e._v(" "),n("b-row",[n("b-btn",{attrs:{disabled:e.updating},on:{click:e.runUpdate}},[e.updating?n("icon",{staticClass:"align-baseline",attrs:{name:"spinner",scale:"1",spin:""}}):e._e(),e._v("\n            Mettre à jour\n        ")],1),e._v(" "),n("b-btn",{attrs:{variant:"danger"},on:{click:e.runRestart}},[e._v("\n            Redémarrer HappySchool\n        ")])],1),e._v(" "),n("b-row",{staticClass:"mt-2"},[n("b-col",[n("b-card",{attrs:{"bg-variant":"dark","text-variant":"white"}},[n("p",{staticClass:"card-text console"},[e._v("\n                    "+e._s(e.updateState)+"\n                ")])])],1)],1)],1)};G._withStripped=!0,s().component("icon",u.Z);var M={xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"};const Z={data:function(){return{updating:!1,updateState:"",progressSocket:null}},methods:{runUpdate:function(){var e=this;h().get("/core/api/update/",M).then((function(t){e.updating=!0,e.updateState="Connecting to server…\n";var n="http:"===window.location.protocol?"ws":"wss";e.progressSocket=new WebSocket(n+"://"+window.location.host+"/ws/core/update/"+JSON.parse(t.data)+"/"),e.progressSocket.onmessage=function(t){e.updateState+=JSON.parse(t.data).status,JSON.parse(t.data).status.includes("Mise à jour terminé")&&(e.updating=!1,e.progressSocket.close())}}))},runRestart:function(){setTimeout((function(){document.location.reload(!0)}),1e4),h().get("/core/api/restart/",M),this.$bvToast.toast("La page sera automatiquement rafraîchie dans 10 secondes.",{title:"Attention",variant:"danger",autoHideDelay:1e4})}}};var A=n("./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/core/update.vue?vue&type=style&index=0&lang=css&");x()(A.Z,{insert:"head",singleton:!1}),A.Z.locals;var H=(0,c.Z)(Z,G,[],!1,null,null,null);H.options.__file="assets/core/update.vue";const R=H.exports;var $=n("./assets/common/menu.vue"),D=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("h4",[e._v("Annuaire")]),e._v(" "),n("br"),e._v(" "),n("b-row",[n("b-col",[n("h5",[e._v("Gestion des accès aux données")])])],1),e._v(" "),e._l(e.permissions,(function(t){return n("div",{key:t.title},[n("b-row",[n("b-col",[n("b-card",{staticClass:"mb-2",attrs:{"no-body":""}},[n("b-card-header",[e._v("\n                        "+e._s(t.title)+"\n                    ")]),e._v(" "),n("b-list-group",{attrs:{flush:""}},e._l(t.canSee,(function(o){return n("b-list-group-item",{key:o.id},[e._v("\n                            "+e._s(o.name)+"\n                            "),n("b-btn",{staticClass:"float-right",attrs:{variant:"light",size:"sm"},on:{click:function(n){return e.deleteGroup(t.permissionName,o)}}},[n("icon",{attrs:{name:"remove",scale:"1",color:"red"}})],1)],1)})),1),e._v(" "),n("b-card-body",{attrs:{"body-bg-variant":"light"}},[n("b-form-group",{attrs:{label:"Sélectionner un groupe dans la liste et cliquer sur 'Ajouter'"}},[n("b-input-group",[n("b-form-select",{attrs:{options:t.availableGroups,"value-field":"id","text-field":"name"},model:{value:t.selected,callback:function(n){e.$set(t,"selected",n)},expression:"permission.selected"}}),e._v(" "),n("b-input-group-append",[n("b-button",{attrs:{size:"sm",text:"Button",variant:"success"},on:{click:function(n){return e.sendPermission(t.permissionName)}}},[e._v("\n                                        Ajouter\n                                    ")])],1)],1)],1)],1)],1)],1)],1)],1)})),e._v(" "),n("b-row",[n("b-col",[n("h5",[e._v("Afficher les identifiants")])])],1),e._v(" "),n("b-row",[n("b-col",[n("b-form-group",{attrs:{description:" Afficher les champs utilisateur/mot de passe dans la fiche info et ainsi que la liste des mots de passe des élèves par classe"}},[n("b-form-checkbox",{on:{change:e.sendCredentials},model:{value:e.credentials,callback:function(t){e.credentials=t},expression:"credentials"}},[e._v("\n                    Afficher les champs utilisateur/mot de passe\n                ")])],1)],1)],1)],2)};function I(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}D._withStripped=!0;var J={xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"};const E={data:function(){return{permissions:[{title:"Groupes pouvants voir les responsables (professeurs, éducateurs,… )",permissionName:"responsibles",canSee:[],selected:null,availableGroups:[]},{title:"Groupes pouvants voir les données sensibles des responsables (professeurs, éducateurs,… )",permissionName:"responsibles_sensitive",canSee:[],selected:null,availableGroups:[]},{title:"Groupes pouvants voir les données sensibles des élèves (adresses, professions des parents,… )",permissionName:"student_sensitive",canSee:[],selected:null,availableGroups:[]},{title:"Groupes pouvants voir les données de contact des élèves",permissionName:"student_contact",canSee:[],selected:null,availableGroups:[]},{title:"Groupes pouvants voir les données médiacles des élèves",permissionName:"student_medical",canSee:[],selected:null,availableGroups:[]}],credentials:null,groups:[]}},methods:{sendCredentials:function(){var e=this;this.credentials=!this.credentials,h().put("/annuaire/api/settings/1/",{show_credentials:this.credentials},J).then((function(){e.$bvToast.toast("Sauvegardé.",{variant:"success",noCloseButton:!0})}))},sendPermission:function(e){var t=this,n=this.permissions.find((function(t){return t.permissionName==e})),o=n.canSee.map((function(e){return e.id})).concat([n.selected]);h().put("/annuaire/api/settings/1/",I({},"can_see_"+e,o),J).then((function(){n.canSee=o.map((function(e){return t.groups.find((function(t){return t.id==e}))})),n.availableGroups=n.availableGroups.filter((function(e){return e.id!=n.selected})),n.selected=null,t.$bvToast.toast("Sauvegardé.",{variant:"success",noCloseButton:!0})})).catch((function(e){alert(e)}))},deleteGroup:function(e,t){var n=this;this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer "+t.name+" ?").then((function(o){if(o){var s=n.permissions.find((function(t){return t.permissionName==e})),a=s.canSee.map((function(e){return e.id})).filter((function(e){return e!=t.id}));h().put("/annuaire/api/settings/1/",I({},"can_see_"+e,a),J).then((function(){s.canSee=a.map((function(e){return n.groups.find((function(t){return t.id==e}))})),s.availableGroups=s.availableGroups.concat([t])})).catch((function(e){alert(e)}))}}))},getGroups:function(){var e=this;h().get("/core/api/group/").then((function(t){e.groups=t.data.results.filter((function(e){if(isNaN(e.name[e.name.length-1]))return!0}))}))}},mounted:function(){var e=this;this.getGroups(),h().get("/annuaire/api/settings/1/").then((function(t){e.credentials=t.data.show_credentials,e.permissions.forEach((function(n){n.canSee=t.data["can_see_"+n.permissionName].map((function(t){return e.groups.find((function(e){return e.id==t}))})),n.availableGroups=e.groups.filter((function(e){return!n.canSee.find((function(t){return t.name==e.name}))}))}))})).catch((function(e){alert(e)}))}};var z=(0,c.Z)(E,D,[],!1,null,null,null);z.options.__file="assets/core/annuaire_settings.vue";const q=z.exports;s().use(a.ZP),s().use(r.Z);var B=new r.Z({routes:[{path:"",component:p,children:[{path:"",component:T},{path:"general",component:T},{path:"import",component:k},{path:"photos",component:L},{path:"update",component:R},{path:"annuaire",component:q}]}]});new(s())({el:"#vue-app",data:{menuInfo:{}},router:B,template:'<div><app-menu :menu-info="menuInfo"></app-menu><router-view></router-view></div>',mounted:function(){this.menuInfo=menu},components:{"app-menu":$.Z}})},"./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/core/import.vue?vue&type=style&index=0&lang=css&":(e,t,n)=>{n.d(t,{Z:()=>a});var o=n("./node_modules/css-loader/dist/runtime/api.js"),s=n.n(o)()((function(e){return e[1]}));s.push([e.id,"\n.console {\n    font-family:monospace;\n    white-space: pre-wrap;\n}\n",""]);const a=s},"./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/core/update.vue?vue&type=style&index=0&lang=css&":(e,t,n)=>{n.d(t,{Z:()=>a});var o=n("./node_modules/css-loader/dist/runtime/api.js"),s=n.n(o)()((function(e){return e[1]}));s.push([e.id,"\n.console {\n    font-family:monospace;\n    white-space: pre-wrap;\n}\n",""]);const a=s}},n={};function o(e){var s=n[e];if(void 0!==s)return s.exports;var a=n[e]={id:e,loaded:!1,exports:{}};return t[e].call(a.exports,a,a.exports,o),a.loaded=!0,a.exports}o.m=t,e=[],o.O=(t,n,s,a)=>{if(!n){var r=1/0;for(u=0;u<e.length;u++){for(var[n,s,a]=e[u],i=!0,l=0;l<n.length;l++)(!1&a||r>=a)&&Object.keys(o.O).every((e=>o.O[e](n[l])))?n.splice(l--,1):(i=!1,a<r&&(r=a));i&&(e.splice(u--,1),t=s())}return t}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[n,s,a]},o.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return o.d(t,{a:t}),t},o.d=(e,t)=>{for(var n in t)o.o(t,n)&&!o.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},o.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),o.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),o.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),o.j=328,(()=>{var e={328:0};o.O.j=t=>0===e[t];var t=(t,n)=>{var s,a,[r,i,l]=n,u=0;for(s in i)o.o(i,s)&&(o.m[s]=i[s]);if(l)var c=l(o);for(t&&t(n);u<r.length;u++)a=r[u],o.o(e,a)&&e[a]&&e[a][0](),e[r[u]]=0;return o.O(c)},n=self.webpackChunkhappyschool=self.webpackChunkhappyschool||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))})();var s=o.O(void 0,[351],(()=>o("./assets/js/admin.js")));s=o.O(s)})();