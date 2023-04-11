<template>
    <div>
        <b-container>
            <b-row>
                <h3>{{ this.state=="1" ? "Traiter" : "Ajout/Modifier" }} un appel</h3>
            </b-row>
            <b-row>
                <b-col sm="4">
                    <b-btn
                        class="mb-2"
                        to="/"
                    >
                        Retour à la liste des appels
                    </b-btn>
                    <div>
                        <b-img
                            rounded
                            :src="'/static/photos' + photo + '.jpg'"
                            fluid
                            alt="Photo de la personne"
                        />
                    </div>
                </b-col>
                <b-col>
                    <b-form
                        @submit="addAppel"
                    >
                        <b-form-row>
                            <b-col sm="8">
                                <b-form-group
                                    label="Nom"
                                    label-for="input-name"
                                    :state="inputStates.name"
                                >
                                    <multiselect
                                        id="input-name"
                                        :internal-search="false"
                                        :options="nameOptions"
                                        @search-change="getNameOptions"
                                        :loading="nameLoading"
                                        placeholder="Rechercher une personne…"
                                        select-label=""
                                        selected-label="Sélectionné"
                                        deselect-label=""
                                        label="display"
                                        track-by="matricule"
                                        v-model="name"
                                    >
                                        <template #noResult>
                                            Aucune personne trouvée.
                                        </template>
                                        <template #noOptions />
                                    </multiselect>
                                    <template #invalid-feedback>
                                        {{ errorMsg('name') }}
                                    </template>
                                </b-form-group>
                            </b-col>
                            <b-col sm="4">
                                <b-form-group
                                    label="Matricule"
                                    label-for="input-matricule"
                                >
                                    <b-form-input
                                        id="input-matricule"
                                        type="text"
                                        v-model="form.matricule_id"
                                        readonly
                                    />
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                        <b-form-row>
                            <b-col>
                                <b-form-group
                                    label="Objet"
                                    label-for="input-object"
                                    :state="inputStates.object_id"
                                >
                                    <b-form-select
                                        id="input-object"
                                        v-model="form.object_id"
                                        :options="objectOptions"
                                    >
                                        <template #first>
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez un objet
                                            </option>
                                        </template>
                                    </b-form-select>
                                    <template #invalid-feedback>
                                        {{ errorMsg('object_id') }}
                                    </template>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    label="Motif"
                                    label-for="input-motif"
                                    :state="inputStates.motive_id"
                                >
                                    <b-form-select
                                        v-model="form.motive_id"
                                        :options="motiveOptions"
                                    >
                                        <template #first>
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez un motif
                                            </option>
                                        </template>
                                    </b-form-select>
                                    <template #invalid-feedback>
                                        {{ errorMsg('motive_id') }}
                                    </template>
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                        <div v-if="this.state==0 || form.is_traiter">
                            <b-form-row>
                                <b-col>
                                    <b-form-group
                                        label="Début du motif"
                                        label-for="input-date-motif-start"
                                        :state="inputStates.date_motif_start"
                                    >
                                        <b-form-input
                                            id="input-date-motif-start"
                                            type="date"
                                            v-model="form.date_motif_start"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('date_motif_start') }}
                                        </template>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group
                                        label="(heure)"
                                        label-for="input-time-motif-start"
                                    >
                                        <b-form-input
                                            id="input-time-motif-start"
                                            type="time"
                                            v-model="form.time_motif_start"
                                        />
                                    </b-form-group>
                                </b-col>
                            </b-form-row>
                            <b-form-row>
                                <b-col>
                                    <b-form-group
                                        label="Fin du motif"
                                        label-for="input-date-motif-end"
                                        :state="inputStates.date_motif_end"
                                    >
                                        <b-form-input
                                            id="input-date-motif-end"
                                            type="date"
                                            v-model="form.date_motif_end"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('date_motif_end') }}
                                        </template>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group
                                        label="(heure)"
                                        label-for="input-time-motif-end"
                                    >
                                        <b-form-input
                                            id="input-time-motif-end"
                                            type="time"
                                            v-model="form.time_motif_end"
                                        />
                                    </b-form-group>
                                </b-col>
                            </b-form-row>
                            <b-form-row>
                                <b-col>
                                    <b-form-group
                                        label="Date de l'appel"
                                        label-for="input-date-appel"
                                        :state="inputStates.datetime_appel"
                                    >
                                        <b-form-input
                                            id="input-date-appel"
                                            type="date"
                                            v-model="form.datetime_appel"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('datetime_appel') }}
                                        </template>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group
                                        label="Heure de l'appel"
                                        label-for="input-time-appel"
                                    >
                                        <b-form-input
                                            id="input-time-appel"
                                            type="time"
                                            :step="60"
                                            v-model="timeAppel"
                                        />
                                    </b-form-group>
                                </b-col>
                            </b-form-row>
                        </div>
                        <div v-if="this.state==1 || form.is_traiter">
                            <b-form-row>
                                <b-form-group label="Destinataire(s) : ">
                                    <b-form-checkbox-group
                                        id="emails"
                                        stacked
                                        v-model="form.emails"
                                        :options="$store.state.emails"
                                        value-field="id"
                                        text-field="display"
                                    />
                                </b-form-group>
                            </b-form-row>
                            <b-form-row>
                                <b-form-group
                                    label="Autre email :"
                                    label-for="input-custom-email"
                                    :state="inputStates.custom_email"
                                >
                                    <b-form-input
                                        v-model="form.custom_email"
                                        type="text"
                                        id="input-custom-email"
                                        placeholder="Courriel personnalisé"
                                    />
                                    <template #invalid-feedback>
                                        {{ errorMsg('custom_email') }}
                                    </template>
                                </b-form-group>
                            </b-form-row>
                        </div>

                        <b-form-row>
                            <b-col>
                                <b-form-group
                                    label="Commentaires"
                                    label-for="input-comment"
                                >
                                    <b-form-textarea
                                        id="input-comment"
                                        :rows="3"
                                        v-model="form.commentaire"
                                    />
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                        <b-button
                            type="submit"
                            variant="primary"
                            :disabled="loading"
                        >
                            {{ this.state==1 ? 'Traiter' : 'Soumettre' }}
                        </b-button>
                    </b-form>
                </b-col>
            </b-row>
            <template #modal-ok>
                <b-spinner
                    v-if="loading"
                    small
                />
                {{ this.state==1 ? 'Traiter' : 'Soumettre' }}
            </template>
        </b-container>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import Moment from "moment";
Moment.locale("fr");

import axios from "axios";
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

export default {
    props: { entry: {
        type: Object,
        default: null
    }, 
    state:{
        type: String,
        default: "0",
    },
    processing:{
        type: Boolean,
        default: false
    },
    id: {
        type: String,
        default: null,
    }},
    data: function () {
        return {
            form: {
                name: null,
                matricule_id: null,
                responsible_pk: null,
                object_id: null,
                motive_id: null,
                date_motif_start: null,
                time_motif_start: null,
                date_motif_end: null,
                time_motif_end: null,
                datetime_appel: null,
                commentaire: "",
                emails: [],
                custom_email: null,
                is_student: false,
                is_traiter: false,
            },
            timeAppel: null,
            objectOptions: [],
            motiveOptions: [],
            name: null,
            nameOptions: [],
            nameLoading: false,
            searchId: 0,
            errors: {},
            inputStates: {
                name: null,
                object_id: null,
                motive_id: null,
                date_motif_start: null,
                date_motif_end: null,
                datetime_appel: null,
                custom_email: null,
            },
            loading: false,
        };
    },
    computed: {
        photo: function () {
            if (this.form.name) {
                if (this.name.is_student) {
                    return "/" + this.name.matricule;
                } else {
                    let url = "_prof/";
                    url += this.entry ? this.form.matricule_id : this.name.id;
                    return url;
                }
            } else {
                return "/unknown";
            }
        }
    },
    watch: {
        id: function (newVal) {
            if (newVal) {
                this.setEntry(newVal);
            } else {
                this.reset();
            }
        },
        name: function () {
            //Update form data.
            if (this.name && this.name.matricule) {
                // First update form name data.
                this.form.name = this.name.display;
                if (!("is_teacher" in this.name)) {
                    // Student.
                    this.form.matricule_id = this.name.matricule;
                } else {
                    this.form.responsible_pk = this.name.id;
                }
            }
        },
        errors: function (newErrors) {
            const inputs = Object.keys(this.inputStates);
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
    },
    methods: {
        setEntry: function (entry) {
            const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.get(`/appels/api/appel/${this.id}/`, token)
                .then(resp => {
                    if (resp.data) {
                        entry=resp.data,
                        this.form = {
                            id: entry.id,
                            name: entry.name,
                            matricule_id: entry.matricule_id,
                            responsible_pk: entry.responsible_pk,
                            object_id: entry.object.id,
                            motive_id: entry.motive.id,
                            date_motif_start: Moment(entry.date_motif_start).format("YYYY-MM-DD"),
                            time_motif_start: entry.time_motif_start ? Moment(entry.time_motif_start, "hh:mm:ss").format("hh:mm") : null,
                            date_motif_end: Moment(entry.date_motif_end).format("YYYY-MM-DD"),
                            time_motif_end: entry.time_motif_end ? Moment(entry.time_motif_end, "hh:mm:ss").format("hh:mm") : null,
                            datetime_appel: Moment(entry.datetime_appel).format("YYYY-MM-DD"),
                            commentaire: entry.commentaire,
                            emails: entry.emails,
                            custom_email: entry.custom_email,
                            is_student: entry.is_student,
                            is_traiter: entry.is_traiter,
                        };
                        this.name = resp.data.matricule;
                        if (entry.matricule) {
                            this.name = entry.matricule;
                            this.name.is_student = true;
                        } else {
                            this.name = entry.responsible;
                            this.name.is_student = false;
                        }
                        this.timeAppel = Moment(entry.datetime_appel).format("HH:mm");
                        if (entry) {
                        // Precheck emails.
                            if (!this.processing && this.form.is_student) {
                                
                                this.form.emails = this.$store.state.emails.filter(email => {
                                    if (this.name.teaching.id == email.teaching
                                    && email.years.includes(this.name.classe.year)) {
                                        return true;
                                    }
                                    return false;
                                }).map(email => email.id);
                            }
                        }
                    }
                });
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        addAppel: function (evt) {
            evt.preventDefault();
            this.loading = true;
            // Copy form data.
            let data = Object.assign({}, this.form);
            // Add times if any.
            const time = this.timeAppel ? " " + this.timeAppel : Moment().format("HH:mm");
            data.datetime_appel += time;

            // Set is_student field and responsible's matricule.
            if (this.name){
                data.is_student = this.name.is_student;
            }
            if (!data.is_student) {
                if (!this.form.id) {
                    data.responsible_pk = data.matricule_id;
                }
                data.matricule_id = null;
            }

            let modal = this;
            // Send data.
            const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let path = "/appels/api/appel/";
            if (this.form.id) path += this.form.id + "/";
            
            const send = this.form.id ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(() => {
                this.errors = {};
                this.$emit("update");
                this.loading = false;
                if(this.form.id){
                    this.$router.push("/",() => {
                        this.$root.$bvToast.toast("L'appel a été envoyé.", {
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                } else {this.$router.push("/",() => {
                    this.$root.$bvToast.toast("L'appel a été créé. Traiter l'appel pour envoyé l'information par courriel.", {
                        variant: "success",
                        noCloseButton: true,
                    });
                });
                }            
            })
                .catch(function (error) {
                    modal.loading = false;
                    modal.errors = error.response.data;
                });
        },
        getNameOptions(query) {
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.nameLoading = true;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: "all",
                check_access: false,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch) {
                        return;
                    }
                    const options = response.data.map(p => {
                    // Format entries.
                        let entry = {display: p.last_name + " " + p.first_name};
                        if ("is_secretary" in p) {
                        // It's a responsible.
                            let teachings = " —";
                            for (let t in p.teaching) {
                                teachings += " " + p.teaching[t].display_name;
                            }
                            entry.display += teachings;
                            entry.is_student = false;
                            entry.matricule = p.pk;
                            entry.id = p.matricule;
                        } else {
                        // It's a student.
                            entry.display = p.display;
                            entry.is_student = true;
                            entry.matricule = p.matricule;
                        }
                        return entry;
                    });
                    this.nameLoading = false;
                    this.nameOptions = options;
                })
                .catch(function (error) {
                    alert(error);
                    app.nameLoading = false;
                });
        },
    },
    components: {Multiselect},
    mounted: function () {
        if (!this.entry) {
            const nowDate = Moment().format("YYYY-MM-DD");
            const nowTime = Moment().format("HH:mm");
            this.form.datetime_appel = nowDate;
            this.form.time_motif_end = nowTime;
            this.form.time_motif_start = nowTime;
            this.timeAppel = nowTime;
            this.form.date_motif_start = nowDate;
            this.form.date_motif_end = nowDate;
        }
        // Set motive options.
        axios.get("/appels/api/motive/")
            .then(response => {
                this.motiveOptions = response.data.results.map(m => {
                    return {value: m.id, text: m.display};
                });
            });
        // Set object options.
        axios.get("/appels/api/object/")
            .then(response => {
                this.objectOptions = response.data.results.map(m => {
                    return {value: m.id, text: m.display};
                });
            });
        if (this.id) this.setEntry();
    }
};
</script>

<style>
</style>
