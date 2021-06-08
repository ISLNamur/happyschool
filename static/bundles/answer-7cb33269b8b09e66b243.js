(()=>{"use strict";var e,t={"./assets/js/answer.js":(e,t,o)=>{var s=o("./node_modules/vue/dist/vue.common.prod.js"),n=o.n(s),a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[e.loaded?e._e():o("div",{staticClass:"loading"}),e._v(" "),e.loaded?o("b-container",[o("h1",[e._v(e._s(e.template.name))]),e._v(" "),o("b-row",[o("b-col",[o("p",[e._v("\n                    En tant que responsable de "),o("strong",[e._v(e._s(e.student.full_name))]),e._v(" en "+e._s(e.student.classe)+", veuillez remplir le formulaire suivant. Si vous n'êtes pas responsable de "+e._s(e.student.full_name)+",\n                    merci de contacter au plus vite le service informatique de l'école.\n                ")])])],1),e._v(" "),o("b-row",[o("b-col",[o("p",[e._v("\n                    "+e._s(e.template.text)+"\n                ")])])],1),e._v(" "),o("b-row",[o("b-col",[o("b-form",[e.template.choices.length>0?o("b-form-row",[o("b-form-group",{attrs:{label:"Merci de choisir une des options ci-dessous :","invalid-feedback":"Choisissez au moins une option.",state:e.choiceState}},[o("b-form-radio-group",{attrs:{stacked:""},model:{value:e.form.choices,callback:function(t){e.$set(e.form,"choices",t)},expression:"form.choices"}},e._l(e.template.choices,(function(t,s){return o("b-form-radio",{key:t.id,staticClass:"mb-3",attrs:{value:t.id}},[o("b-form",{attrs:{inline:""}},[e._v("\n                                        "+e._s(t.text)+"\n                                        "),t.input&&e.form.choices==t.id?o("b-form-input",{staticClass:"ml-2",attrs:{type:"text"},model:{value:e.form.choiceText[s].text,callback:function(t){e.$set(e.form.choiceText[s],"text",t)},expression:"form.choiceText[index].text"}}):e._e()],1)],1)})),1)],1)],1):e._e(),e._v(" "),e.template.options.length>0?o("b-form-row",[o("b-form-group",{attrs:{label:"Merci de choisir une ou plusieurs des options ci-dessous :"}},[o("b-form-checkbox-group",{attrs:{stacked:""},model:{value:e.form.options,callback:function(t){e.$set(e.form,"options",t)},expression:"form.options"}},e._l(e.template.options,(function(t,s){return o("b-form-checkbox",{key:t.id,staticClass:"mb-3",attrs:{value:t.id}},[o("b-form",{attrs:{inline:""}},[e._v("\n                                        "+e._s(t.text)+"\n                                        "),t.input?o("b-form-input",{staticClass:"ml-2",attrs:{type:"text"},model:{value:e.form.optionText[s].text,callback:function(t){e.$set(e.form.optionText[s],"text",t)},expression:"form.optionText[index].text"}}):e._e()],1)],1)})),1)],1)],1):e._e()],1)],1)],1),e._v(" "),e.template.acknowledge?o("b-row",[o("b-col",[o("b-card",{staticClass:"mb-2"},[e.template.acknowledge?o("b-form-group",[o("b-form-checkbox",{model:{value:e.form.acknowledge,callback:function(t){e.$set(e.form,"acknowledge",t)},expression:"form.acknowledge"}},[e._v("\n                            "+e._s(e.template.acknowledge_text)+"\n                        ")])],1):e._e()],1)],1)],1):e._e(),e._v(" "),o("b-row",[o("p",[o("b-btn",{attrs:{disabled:e.saving||e.template.acknowledge&&!e.form.acknowledge,variant:"primary"},on:{click:e.sendData}},[e._v("\n                    "+e._s(e.sent?"Mettre à jour":"Envoyer")+"\n                    "),e.saving?o("icon",{attrs:{name:"spinner",scale:"1",spin:e.saving}}):e._e()],1)],1)]),e._v(" "),o("b-row",[o("p",[o("b-alert",{attrs:{variant:"success",show:e.countDownSuccess}},[e._v("\n                    Les données ont été envoyées !\n                ")])],1)])],1):e._e()],1)};a._withStripped=!0;var i=o("./node_modules/bootstrap-vue/esm/index.js"),r=(o("./node_modules/vue-awesome/icons/index.js"),o("./node_modules/vue-awesome/components/Icon.vue")),l=o("./node_modules/axios/index.js"),c=o.n(l);n().use(i.ZPm),n().component("icon",r.Z);const d={props:{uuid:{type:String,default:""}},data:function(){return{loaded:!1,student:{full_name:"",classe:""},template:{},form:{acknowledge:!1,options:[],optionText:[],choices:"",choiceText:[]},sent:!1,saving:!1,countDownSuccess:0,choiceState:null}},methods:{sendData:function(){var e=this;if(this.template.choices.length>0&&0==this.form.choices)this.choiceState=!1;else{this.choiceState||(this.choiceState=!0),this.saving=!0;var t="/mail_answer/api/public/mail_answer/"+this.uuid+"/";c().put(t,{answers:JSON.stringify(this.form)},{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"}).then((function(){e.sent=!0,e.saving=!1,e.countDownSuccess=4})).catch((function(){alert("Un problème est survenu.\nMerci de réessayer ou de contacter le service informatique."),this.saving=!1}))}}},mounted:function(){var e=this,t="/mail_answer/api/public/mail_answer/"+this.uuid+"/";c().get(t,{xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken"}).then((function(t){e.student.full_name=t.data.student.last_name+" "+t.data.student.first_name,e.student.classe=t.data.student.classe.year+t.data.student.classe.letter.toUpperCase(),e.template=t.data.template;var o=JSON.parse(t.data.answers),s=Object.keys(o).length>2;for(var n in s&&(e.form.acknowledge=o.acknowledge,e.form.choices=o.choices,e.form.options=o.options,e.sent=!0),e.template.choices){var a=s?o.choiceText[n].text:"";e.form.choiceText.push({id:e.template.choices[n].id,text:a})}for(var i in e.template.options){var r=s?o.optionText[i].text:"";e.form.optionText.push({id:e.template.options[i].id,text:r})}e.loaded=!0}))}};var u=o("./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js"),m=o.n(u),p=o("./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/mail_answer/answer.vue?vue&type=style&index=0&lang=css&");m()(p.Z,{insert:"head",singleton:!1}),p.Z.locals;var f=(0,o("./node_modules/vue-loader/lib/runtime/componentNormalizer.js").Z)(d,a,[],!1,null,null,null);f.options.__file="assets/mail_answer/answer.vue";const v=f.exports;new(n())({el:"#vue-app",data:{uuid:null,component:""},template:'<component :is="component" :uuid="uuid"/>',components:{answer:v},mounted:function(){this.uuid=uuid,this.component="answer"}})},"./node_modules/css-loader/dist/cjs.js!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./assets/mail_answer/answer.vue?vue&type=style&index=0&lang=css&":(e,t,o)=>{o.d(t,{Z:()=>d});var s=o("./node_modules/css-loader/dist/runtime/api.js"),n=o.n(s),a=o("./node_modules/css-loader/dist/runtime/getUrl.js"),i=o.n(a),r=o("./static/img/spin.svg"),l=n()((function(e){return e[1]})),c=i()(r.Z);l.push([e.id,'\n.loading {\n  content: " ";\n  display: block;\n  position: absolute;\n  width: 80px;\n  height: 80px;\n  background-image: url('+c+");\n  background-size: cover;\n  left: 50%;\n  top: 50%;\n}\n",""]);const d=l}},o={};function s(e){var n=o[e];if(void 0!==n)return n.exports;var a=o[e]={id:e,loaded:!1,exports:{}};return t[e].call(a.exports,a,a.exports,s),a.loaded=!0,a.exports}s.m=t,e=[],s.O=(t,o,n,a)=>{if(!o){var i=1/0;for(c=0;c<e.length;c++){for(var[o,n,a]=e[c],r=!0,l=0;l<o.length;l++)(!1&a||i>=a)&&Object.keys(s.O).every((e=>s.O[e](o[l])))?o.splice(l--,1):(r=!1,a<i&&(i=a));r&&(e.splice(c--,1),t=n())}return t}a=a||0;for(var c=e.length;c>0&&e[c-1][2]>a;c--)e[c]=e[c-1];e[c]=[o,n,a]},s.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return s.d(t,{a:t}),t},s.d=(e,t)=>{for(var o in t)s.o(t,o)&&!s.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})},s.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),s.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),s.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),s.j=986,(()=>{var e={986:0};s.O.j=t=>0===e[t];var t=(t,o)=>{var n,a,[i,r,l]=o,c=0;for(n in r)s.o(r,n)&&(s.m[n]=r[n]);if(l)var d=l(s);for(t&&t(o);c<i.length;c++)a=i[c],s.o(e,a)&&e[a]&&e[a][0](),e[i[c]]=0;return s.O(d)},o=self.webpackChunkhappyschool=self.webpackChunkhappyschool||[];o.forEach(t.bind(null,0)),o.push=t.bind(null,o.push.bind(o))})();var n=s.O(void 0,[351],(()=>s("./assets/js/answer.js")));n=s.O(n)})();