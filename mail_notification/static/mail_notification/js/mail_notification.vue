<template>
    <div v-cloak>
        <BContainer v-cloak>
            <BRow>
                <BCol>
                    <BNav tabs>
                        <BNavItem
                            active
                            href="/mail_notification/"
                        >
                            Envoyer un email
                        </BNavItem>
                        <BNavItem to="/list/">
                            Liste des emails envoyés
                        </BNavItem>
                        <BNavItem href="/mail_answer/">
                            Gestion des modèles
                        </BNavItem>
                        <BNavItem href="/core/members/">
                            Gestion des personnes
                        </BNavItem>
                    </BNav>
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <BForm @submit="onSubmit">
                        <div>
                            <BFormGroup label="Choisissez d'abord l'enseignement : ">
                                <BFormRadioGroup
                                    v-model="teaching"
                                    name="teaching"
                                >
                                    <BFormRadio value="secondaire">
                                        Secondaire
                                    </BFormRadio>
                                    <BFormRadio value="primaire">
                                        Primaire
                                    </BFormRadio>
                                </BFormRadioGroup>
                            </BFormGroup>
                        </div>
                        <div v-if="teaching">
                            <h3>Enseignement : {{ teaching.toUpperCase() }}</h3>
                            <BFormGroup label="Le type de destinataires : ">
                                <BFormRadioGroup
                                    v-model="toType"
                                    name="toType"
                                    @update:model-value="warnChoice"
                                >
                                    <BFormRadio value="teachers">
                                        Professeurs
                                    </BFormRadio>
                                    <BFormRadio value="parents">
                                        Parents
                                    </BFormRadio>
                                </BFormRadioGroup>
                            </BFormGroup>
                            <BFormGroup
                                v-if="toType == 'parents'"
                                description="Si «Par parent» est choisi, un parent ayant plusieurs enfants ne recevra qu'un seul email. À contrario, si «Par élève» est choisi, un parent ayant plusieurs élèves recevra un email par élève."
                                label="Type d'envoi : "
                            >
                                <BFormRadioGroup
                                    v-model="sendType"
                                    name="sendType"
                                >
                                    <BFormRadio value="parents">
                                        Par parent
                                    </BFormRadio>
                                    <BFormRadio value="students">
                                        Par élève
                                    </BFormRadio>
                                </BFormRadioGroup>
                            </BFormGroup>
                            <BFormGroup
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
                                    <template #noResult>
                                        Aucun expéditeur trouvé.
                                    </template>
                                    <template #noOptions />
                                </multiselect>
                                <BAlert
                                    variant="danger"
                                    :model-value="!emailFromState"
                                >
                                    Merci de choisir un expéditeur.
                                </BAlert>
                            </BFormGroup>

                            <BFormGroup
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
                                    <template #noResult>
                                        Aucun destinataire trouvé.
                                    </template>
                                    <template #noOptions />
                                </multiselect>
                                <BAlert
                                    variant="danger"
                                    :model-value="!emailToState"
                                >
                                    Merci de choisir au moins un destinataire.
                                </BAlert>
                            </BFormGroup>
                            <BFormGroup>
                                <BFormCheckbox v-model="responsibles">
                                    Également envoyer aux educateurs et coordonnateurs correspondants.
                                </BFormCheckbox>
                            </BFormGroup>
                            <BListGroup horizontal>
                                <BListGroupItem
                                    v-for="group in pinnedGroups"
                                    :key="group.id"
                                >
                                    <BButton
                                        size="sm"
                                        @click="addRecipient(group)"
                                    >
                                        <IBiPlus />
                                        {{ group.name }}
                                    </BButton>
                                </BListGroupItem>
                            </BListGroup>
                            <BFormGroup v-if="sendType == 'students'">
                                <multiselect
                                    v-model="template"
                                    :options="templateOptions"
                                    track-by="id"
                                    label="name"
                                    placeholder="Ajouter un formulaire à remplir"
                                >
                                    <template #noOptions />
                                </multiselect>
                            </BFormGroup>
                            <BFormGroup
                                label="Tag(s) : "
                                description="Permet de facilement identifier l'email (CPE, CGQ,…)"
                            >
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
                                    <template #noResult>
                                        Aucun tag trouvé.
                                    </template>
                                    <template #noOptions />
                                </multiselect>
                            </BFormGroup>

                            <BFormGroup label="Sujet* : ">
                                <BFormInput
                                    v-model="subject"
                                    type="text"
                                    placeholder="Sujet de l'email"
                                />
                            </BFormGroup>

                            <BFormGroup
                                description="Ajouter une ou des pièces jointes à l'email. Accepte uniquement des fichiers pdf."
                                label="Pièce(s) jointe(s) : "
                            >
                                <BFormFile
                                    multiple
                                    accept=".pdf"
                                    v-model="attachments"
                                    ref="attachments"
                                    placeholder="Attacher un ou des fichiers."
                                    choose-label="Attacher un ou des fichiers"
                                    drop-label="Déposer des fichiers ici"
                                    plain
                                    @update:model-value="addFiles"
                                />
                                <BListGroup
                                    v-for="(item, index) in uploadedFiles"
                                    :key="index"
                                >
                                    <file-upload
                                        :id="item.id"
                                        :file="item.file"
                                        path="/mail_notification/upload_file/"
                                        @delete="deleteFile(index)"
                                        @setdata="setFileData(index, $event)"
                                    />
                                </BListGroup>
                            </BFormGroup>
                            <BFormGroup
                                :description="explanation_mail"
                                label="Email : "
                            >
                                <text-editor
                                    v-model="emailContent"
                                    advanced
                                    div-block
                                    placeholder="Écrire le mail ici."
                                />
                                <div
                                    class="html ql-editor"
                                    v-html="replaceContent"
                                />
                            </BFormGroup>
                            <BButton
                                type="submit"
                                variant="primary"
                            >
                                Envoyer
                            </BButton>
                        </div>
                    </BForm>
                </BCol>
            </BRow>
        </BContainer>
        <b-modal
            v-model="showModal"
            centered
            ok-only
        >
            <p v-if="sending">
                <BSpinner small />
                Envoi des emails en cours…
            </p>
            <p v-if="!sending && !hasError">
                La demande d'envoi des emails a été soumise !
            </p>
            <p />
            <p v-if="!sending && hasError">
                Désolé, une erreur est survenue lors de l'envoi du mail. Merci de réessayer plus tard ou de contacter un
                administrateur.
            </p>
            <p />
            <template #modal-footer>
                <BButton
                    size="sm"
                    class="float-right"
                    variant="primary"
                    @click="showModal = false"
                >
                    OK
                </BButton>
            </template>
        </b-modal>
    </div>
</template>

<script>
import TextEditor from "@s:core/js/common/text_editor.vue";

import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";
import Multiselect from "vue-multiselect";

import FileUpload from "@s:core/js/common/file_upload.vue";

export default {
    data: function () {
        return {
            menuInfo: {},
            explanation_mail: "",
            /*`Dans le cas d'un message «Par élève»,
            les variables {{ nom }} et {{ classe }} seront automatiquement converties en nom et classe de l'élève.
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
            preshow: "",
            pinnedGroups: [],
        };
    },
    watch: {
        teaching: function () {
            if (!this.teaching) return;

            // Reset fields.
            this.emailFrom = "";
            this.responsibles = false;
            //TODO reset all other fields.
            axios.get("/mail_notification/get_senders/" + this.teaching + "/")
                .then(response => {
                    this.emailFromOptions = response.data.map(m => m.sender_email_name + " <" + m.sender_email + ">");
                });
        }
    },
    computed: {
        replaceContent: function () {
            let attachmentsHtml = "<ul>";
            for (let a in this.uploadedFiles) {
                attachmentsHtml += `<li><a href="#" >${this.attachments[a].name}</a></li>\n`;
            }
            attachmentsHtml += "</ul>";

            return this.emailContent
                .replace(/\{\{ nom \}\}/g, "Toto Tutu")
                .replace(/\{\{ classe \}\}/g, "3B")
                .replace(/\{\{ fichiers \}\}/g, attachmentsHtml);
        },
    },
    methods: {
        warnChoice: function () {
            if (this.toType === "teachers") alert("Vous avez choisi d'envoyer aux parents.");
        },
        reset: function () {
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
        addFiles: function (files) {
            for (let a in files) {
                this.uploadedFiles.push({ file: files[a], id: -1 });
            }
        },
        setFileData: function (index, data) {
            this.uploadedFiles[index].id = data.id;
            this.uploadedFiles[index].link = data.attachment;
        },
        deleteFile: function (index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
        getEmailToOptions: function (search) {
            this.emailToLoading = true;
            axios.get("/mail_notification/get_email_to_options/" + this.teaching + "/" + this.toType + "/?query=" + search)
                .then(response => {
                    this.emailToOptions = response.data;
                    this.emailToLoading = false;
                });
        },
        getTagsOptions: function (search) {
            this.tagsLoading = true;
            axios.get("/mail_notification/get_tags_options/?query=" + search)
                .then(response => {
                    this.tagsOptions = response.data;
                    this.tagsLoading = false;
                });
        },
        addRecipient: function (group) {
            this.emailTo.push(group.name);
        },
        onEditorChange(event) {
            this.emailContent = event.html;
        },
        onSubmit(evt) {
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
            formData.append("to_type", this.toType);
            formData.append("email_to", this.emailTo);
            formData.append("responsibles", this.responsibles);
            formData.append("email_from", this.emailFrom);
            formData.append("send_type", this.sendType);
            formData.append("email_content", this.emailContent);
            formData.append("subject", this.subject);
            formData.append("teaching", this.teaching);
            if (this.template) formData.append("template", this.template.id);
            var attachments = [];
            for (let u in this.uploadedFiles) {
                attachments.push(this.uploadedFiles[u].id);
            }
            formData.append("attachments", attachments);

            const thisApp = this;
            axios.post(
                "send_emails/",
                formData,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                }
            ).then(() => {
                thisApp.sending = false;
                thisApp.reset();
            }).catch(() => {
                thisApp.sending = false;
                thisApp.hasError = true;
            });
        }
    },
    components: { Multiselect, TextEditor, FileUpload },
    mounted: function () {
        this.getTagsOptions("");

        axios.get("/mail_notification/api/other_email_group/?pinned=true")
            .then((resp) => {
                this.pinnedGroups = resp.data.results;
            });

        // Get templates.
        axios.get("/mail_answer/api/mail_template/?is_used=0")
            .then(response => {
                this.templateOptions = response.data.results;
            })
            .catch(function (error) {
                alert(error);
            });
    }
};
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
