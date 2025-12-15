<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <div>
        <h4>Mise à jour</h4>
        <BRow>
            <BAlert
                show
                variant="warning"
            >
                Une fois la mise à jour terminée, veuillez redémarrer HappySchool.
                Attention, une fois la mise à jour enclenchée, elle continuera même si la page est rafraîchie.
            </BAlert>
        </BRow>
        <BRow>
            <BButton
                @click="runUpdate"
                :disabled="updating"
            >
                <BSpinner
                    v-if="updating"
                />
                Mettre à jour
            </BButton>
            <BButton
                variant="danger"
                @click="runRestart"
            >
                Redémarrer HappySchool
            </BButton>
        </BRow>
        <BRow class="mt-2">
            <BCol>
                <BCard
                    bg-variant="dark"
                    text-variant="white"
                >
                    <p class="card-text console">
                        {{ updateState }}
                    </p>
                </BCard>
            </BCol>
        </BRow>
    </div>
</template>

<script>
import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            updating: false,
            updateState: "",
            progressSocket: null,
        };
    },
    methods: {
        runUpdate: function () {
            let app = this;
            axios.get("/core/api/update/", token)
                .then((response) => {
                    app.updating = true;
                    app.updateState = "Connecting to server…\n";
                    const protocol = window.location.protocol === "http:" ? "ws" : "wss";
                    app.progressSocket = new WebSocket(protocol + "://" + window.location.host + "/ws/core/update/" + JSON.parse(response.data) + "/");
                    app.progressSocket.onmessage = function (event) {
                        app.updateState += JSON.parse(event.data)["status"];
                        if (JSON.parse(event.data)["status"].includes("Mise à jour terminé")) {
                            app.updating = false;
                            app.progressSocket.close();
                        }
                    };
                });
        },
        runRestart: function () {
            setTimeout(() => {
                document.location.reload(true);
            }, 10000);
            axios.get("/core/api/restart/", token);
            this.show({
                body: "La page sera automatiquement rafraîchie dans 10 secondes.",
                title: "Attention",
                variant: "danger",
                autoHideDelay: 10000,
            });
        },
    },
};
</script>

<style>
.console {
    font-family:monospace;
    white-space: pre-wrap;
}
</style>
