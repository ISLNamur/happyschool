<template>
    <b-list-group-item>
        <icon v-if="loading" name="spinner" scale="1" :pulse="loading"></icon>
        <b-btn v-else @click="deleteEntry" size="sm" variant="danger">Enlever</b-btn>
         <span v-if="file">{{ file.name }}</span>
         <span v-else>
             Voir <a target="_blank" rel="noopener noreferrer" :href="link">{{ filename.substring(removestr, 40) }}</a>
         </span>
    </b-list-group-item>
</template>

<script>
import axios from 'axios';
import Icon from 'vue-awesome/components/Icon.vue'

export default {
    props: ['id', 'file', 'path', 'removestr'],
    data: function () {
        return {
            loading: true,
            link: "",
            filename: "",
        }
    },
    methods: {
        deleteEntry: function() {
            axios.delete(this.path + this.id,
                {
                    xsrfCookieName: 'csrftoken',
                    xsrfHeaderName: 'X-CSRFToken',
                }
            ).then(response => {
                this.$emit('delete');
            });
        },
    },
    mounted: function() {
        if (this.id < 0) {
            var data = new FormData();
            data.append('file', this.file);
            axios.put(this.path, data,
                {
                    xsrfCookieName: 'csrftoken',
                    xsrfHeaderName: 'X-CSRFToken',
                    headers: {'Content-Disposition': 'form-data; name="file"; filename="' + this.file.name.normalize() + '"'},
                })
            .then(response => {
                this.link = response.data.attachment
                this.$emit('setdata', response.data);
                this.loading = false;
           })
           .catch(function (error) {
               alert("Une erreur est survenue lors de l'ajout du fichier, merci de réessayer.\n" + error);
               this.$emit('delete');
           });
       } else {
           axios.get("/dossier_eleve/upload_file/" + this.id + "/")
           .then(response => {
               this.link = response.data.attachment;
               this.filename = this.link.split("/")[this.link.split("/").length - 1];
               this.loading = false;
           });
       }
   },
   components: {Icon},
}
</script>

<style>
</style>
