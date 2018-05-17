<template>
    <div v-cloak>
        <b-container v-cloak>
            <b-row>
                <b-nav tabs>
                    <b-nav-item active href="/mail_notification/">Envoyer un email</b-nav-item>
                    <b-nav-item href="/mail_notification/list/">Liste des emails envoyés</b-nav-item>
                    <b-nav-item href="/core/members/">Gestion des personnes</b-nav-item>
                </b-nav>
            </b-row>
            <b-row>
                <b-form @submit="onSubmit">
                    <div>
                        <b-form-group
                            label="Choisissez d'abord l'enseignement : "
                            >
                            <b-form-radio-group v-model="teaching" name="teaching">
                                <b-form-radio value="secondaire">Secondaire</b-form-radio>
                                <b-form-radio value="primaire">Primaire</b-form-radio>
                            </b-form-radio-group>
                        </b-form-group>
                    </div>
                    <div v-if="teaching">
                        <h3>Enseignement : {{ teaching.toUpperCase() }}</h3>
                        <b-form-group
                            label="Le type de destinataires : "
                            >
                            <b-form-radio-group v-model="toType" name="toType" @change="warnChoice">
                                <b-form-radio value="teachers">Professeurs</b-form-radio>
                                <b-form-radio value="parents">Parents</b-form-radio>
                            </b-form-radio-group>
                        </b-form-group>
                        <b-form-group
                            v-if="toType == 'parents'"
                            description="Si «Par parent» est choisi, un parent aillant plusieurs enfants ne recevra qu'un seul email. À contrario, si «Par élève» est choisi, un parent aillant plusières élèves recevra un email par élève."
                            label="Type d'envoi : "
                            >
                            <b-form-radio-group v-model="sendType" name="sendType">
                                <b-form-radio value="parents">Par parent</b-form-radio>
                                <b-form-radio value="students">Par élève</b-form-radio>
                            </b-form-radio-group>
                        </b-form-group>
                        <b-form-group
                            description="Sélectionner à partir de quelle adresse l'email sera envoyé."
                            label="Expéditeur* : "
                            :state="emailFromState"
                            >
                            <multiselect
                                :options="emailFromOptions"
                                placeholder="Sélectionner un expéditeur"
                                select-label="Cliquer dessus pour sélectionner"
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="emailFrom"
                                >
                                <span slot="noResult">Aucun destinataire trouvé.</span>
                            </multiselect>
                            <b-alert variant="danger" :show="!emailFromState">
                                Merci de choisir un expéditeur.
                            </b-alert>
                        </b-form-group>

                        <b-form-group
                            description="Ajouter un cycle et/ou un degré, une année, une classe…"
                            label="Destinataires* : "
                            :state="emailToState"
                            >
                            <multiselect
                                :internal-search="false"
                                :options="emailToOptions"
                                @search-change="getEmailToOptions"
                                :multiple="true"
                                :loading="emailToLoading"
                                placeholder="Ajouter un destinataire"
                                select-label="Cliquer dessus pour sélectionner"
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="emailTo"
                                >
                                <span slot="noResult">Aucun destinataire trouvé.</span>
                            </multiselect>
                            <b-alert variant="danger" :show="!emailToState">
                                Merci de choisir au moins un destinataire.
                            </b-alert>
                        </b-form-group>
                        <b-form-group v-if="toType == 'teachers'">
                            <b-form-checkbox v-model="responsibles">
                                Également envoyer aux educateurs et coordonnateurs correspondants.
                            </b-form-checkbox>
                        </b-form-group>
                        <b-form-group v-if="sendType == 'students'">
                            <multiselect
                                v-model="template"
                                :options="templateOptions"
                                trackBy="id"
                                label="name"
                                placeholder="Ajouter un formulaire à remplir"
                                >
                            </multiselect>
                        </b-form-group>
                        <b-form-group label="Tag(s) : " description="Permet de facilement identifier l'email (CPE, CGQ,…)">
                            <multiselect
                                :internal-search="false"
                                :options="tagsOptions"
                                @search-change="getTagsOptions"
                                :multiple="true"
                                :loading="tagsLoading"
                                placeholder="Ajouter un tag si besoin."
                                select-label="Cliquer dessus pour sélectionner"
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="tags"
                                >
                                <span slot="noResult">Aucun tag trouvé.</span>
                            </multiselect>
                        </b-form-group>

                        <b-form-group
                            label="Sujet* : "
                            >
                            <b-form-input v-model="subject" type="text" placeholder="Sujet de l'email"></b-form-input>
                        </b-form-group>

                        <b-form-group
                            description="Ajouter une ou des pièces jointes à l'email. Accepte uniquement des fichiers pdf."
                            label="Pièce(s) jointe(s) : "
                            >
                            <b-form-file
                                multiple
                                accept=".pdf"
                                v-model="attachments"
                                ref="attachments"
                                placeholder="Attacher un ou des fichiers."
                                choose-label="Attacher un ou des fichiers"
                                drop-label="Déposer des fichiers ici"
                                plain
                                @input="addFiles"
                                >
                            </b-form-file>
                            <b-list-group v-for="(item, index) in uploadedFiles" :key="index">
                                <file-upload :file="item.file" @delete="deleteFile(index)" @setid="setFileId(index, $event)"></file-upload>
                            </b-list-group>
                        </b-form-group>
                        <b-form-group
                            :description="explanation_mail"
                            label="Email : "
                            >
                            <quill-editor :content="emailContent"
                                :options="editorOptions"
                                @change="onEditorChange($event)"
                                >
                            </quill-editor>
                            <div class="html ql-editor" v-html='replaceContent()'></div>
                        </b-form-group>
                        <b-button type="submit" variant="primary">Envoyer</b-button>
                    </div>
                </b-form>
            </b-row>
        </b-container>
        <b-modal v-model="showModal" centered>
            <p v-if="sending"><icon name="refresh" scale="1" spin></icon> Envoi des emails en cours…</p>
            <p v-if="!sending && !hasError">La demande d'envoi des emails a été soumise !<p>
            <p v-if="!sending && hasError">Désolé, une erreur est survenue lors de l'envoi du mail. Merci de réessayer plus tard ou de contacter un administrateur.<p>
            <div slot="modal-footer" class="w-100">
                <b-btn size="sm" class="float-right" variant="primary" @click="showModal=false">
                    OK
                </b-btn>
           </div>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import {quillEditor} from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'

import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'vue-multiselect/dist/vue-multiselect.min.css'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
import axios from 'axios';
import Multiselect from 'vue-multiselect';

import FileUpload from './file_upload.vue';

Vue.use(BootstrapVue);
Vue.component('icon', Icon);

export default {
    data: function () {
        return {
            menu: {},
            explanation_mail:"",
            /*`Dans le cas d'un message «Par élève»,
            les variables {{ nom }} et {{ classe }} seront automatiquement converties en nom et classe de l'élève.
            Vous pouvez voir le résultat directement dans la prévisualisation.`,*/
            toType: "teachers",
            subject: "",
            emailTo: [],
            emailToOptions: [],
            emailToLoading: false,
            emailToState: true,
            emailFrom: "",
            emailFromOptions: [],
            emailFromState: true,
            emailContent: "",
            sendType: "parents",
            template: null,
            templateOptions: [],
            tags: [],
            tagsOptions: [],
            tagsLoading: false,
            teaching: null,
            responsibles: false,
            attachments: [],
            uploadedFiles: [],
            showModal: false,
            sending: false,
            hasError: false,
            editorOptions: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                        ['blockquote', 'code-block'],

                        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
                        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
                        [{ 'direction': 'rtl' }],                         // text direction

                        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
                        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

                        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
                        [{ 'font': [] }],
                        [{ 'align': [] }],

                        ['clean']
                    ]
                },
                placeholder: 'Ecrivez le mail ici.'
            },
            preshow: ""
        }
    },
    watch: {
        teaching: function() {
            if (!this.teaching) return;

            // Reset fields.
            this.emailFrom = "";
            this.responsibles = false;
            //TODO reset all other fields.
            axios.get('/mail_notification/get_senders/' + this.teaching + '/')
            .then(response => {
                this.emailFromOptions = response.data.map(m => m.sender_email_name + " <" + m.sender_email + ">");
           });
        }
    },
    methods: {
        warnChoice: function() {
            if (this.toType === "teachers") alert('Vous avez choisi d\'envoyer aux parents.');
        },
        reset: function() {
                this.toType = "teachers";
                this.subject = "";
                this.emailFrom = "";
                this.emailTo = [];
                this.tags = [];
                this.emailContent = "";
                this.preshow = "";
                this.$refs.attachments.reset();
                this.uploadedFiles.splice(0, this.uploadedFiles.length);
                this.teaching = null;
                this.hasError = false;
                this.responsibles = true;
        },
        addFiles: function(evt) {
            for (let a in this.attachments) {
                this.uploadedFiles.push({file: this.attachments[a], id: -1});
            }
            this.attachments.splice(0, this.attachments.length);
        },
        setFileId: function(index, id) {
            this.uploadedFiles[index].id = id;
        },
        deleteFile: function(index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
        replaceContent: function() {
            let attachmentsHtml ="<ul>";
            for (let a in this.attachments) {
                attachmentsHtml += `<li><a href="#" >${this.attachments[a].name}</a></li>\n`;
            }
            attachmentsHtml += "</ul>";

            return this.emailContent
                .replace(/\{\{ nom \}\}/g, "Toto Tutu")
                .replace(/\{\{ classe \}\}/g, "3B")
                .replace(/\{\{ fichiers \}\}/g, attachmentsHtml);
        },
        getEmailToOptions: function (search) {
            this.emailToLoading = true;
            axios.get('/mail_notification/get_email_to_options/' + this.teaching + '/' + this.toType + '/?query='+search)
            .then(response => {
                this.emailToOptions = response.data;
                this.emailToLoading = false;
           });
       },
       getTagsOptions: function (search) {
           this.tagsLoading = true;
           axios.get('/mail_notification/get_tags_options/?query='+search)
           .then(response => {
               this.tagsOptions = response.data;
               this.tagsLoading = false;
          });
       },
       onEditorChange({editor, html, text}) {
           this.emailContent = html;
       },
       onSubmit (evt) {
           evt.preventDefault();
           if (!this.emailFrom) {
               this.emailFromState = false;
           } else {
               this.emailFromState = true;
           }
           if (this.emailTo.length == 0) {
               this.emailToState = false;
           } else {
               this.emailToState = true;
           }
           if (this.emailTo.length === 0 || !this.emailFrom) return;

           // Ready to send emails.
           this.sending = true;
           this.showModal = true;
           var formData = new FormData();
           formData.append('to_type', this.toType);
           formData.append('email_to', this.emailTo);
           formData.append('responsibles', this.responsibles);
           formData.append('email_from', this.emailFrom);
           formData.append('send_type', this.sendType);
           formData.append('email_content', this.emailContent);
           formData.append('subject', this.subject);
           formData.append('teaching', this.teaching);
           formData.append('template', this.template.id);
           var attachments = [];
           for (let u in this.uploadedFiles) {
               attachments.push(this.uploadedFiles[u].id);
           }
           formData.append('attachments', attachments);

           const thisApp = this;
           axios.post(
               'send_emails/',
               formData,
               {
                   xsrfCookieName: 'csrftoken',
                   xsrfHeaderName: 'X-CSRFToken',
               }
           ).then(function (response) {
               thisApp.sending = false;
               thisApp.reset();
           }).catch(function (error) {
               thisApp.sending = false;
               thisApp.hasError = true;
           });
        }
    },
    components: {Multiselect, quillEditor, FileUpload},
    mounted: function () {
        this.getTagsOptions("");

        // Get templates.
        axios.get('/mail_answer/api/mail_template/?is_used=0')
        .then(response => {
            this.templateOptions = response.data.results;
        })
        .catch(function (error) {
            alert(error);
        });
    }
}
</script>

<style>
    .html {
      height: 9em;
      overflow-y: auto;
      border: 1px solid #ccc;
      border-top: none;
      resize: vertical;
    }
    .custom-file-label::after {
        content: "Parcourir";
    }
    [v-cloak] {
      display: none;
    }
</style>
