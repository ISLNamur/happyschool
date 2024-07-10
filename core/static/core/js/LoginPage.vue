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
    <b-container
        class="text-center"
        style="max-width: 400px;"
    >
        <b-row>
            <b-col>
                <h1>Se connecter</h1>
            </b-col>
        </b-row>
        <b-row v-if="microsoftLogin || googleLogin">
            <b-col>
                <b-card>
                    <strong>
                        <a :href="microsoftLogin || googleLogin">
                            Se connecter avec un compte mail de l'école ({{ microsoftLogin ? "Microsoft" : "Google" }})
                        </a>
                    </strong>
                </b-card>
            </b-col>
        </b-row>
        <b-row
            class="mb-2 mt-2"
            v-if="modelLogin && (microsoftLogin || googleLogin)"
        >
            <b-col>
                <b-btn
                    v-b-toggle.model-form
                    variant="outline-primary"
                    size="sm"
                >
                    Autre compte
                </b-btn> 
            </b-col>
        </b-row>
        <b-collapse
            id="model-form"
            :visible="modelLogin && !microsoftLogin && !googleLogin"
        >
            <b-row>
                <b-col>
                    <b-card>
                        <b-form method="post">
                            <input
                                type="hidden"
                                name="csrfmiddlewaretoken"
                                :value="csrfToken"
                            >
                            <b-form-group
                                label="Nom d'utilisateur :"
                                label-for="username"
                            >
                                <b-form-input
                                    id="username"
                                    name="username"
                                    required
                                />
                            </b-form-group>
                            <b-form-group
                                label="Mot de passe :"
                                label-for="password"
                            >
                                <b-form-input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                />
                            </b-form-group>
                            <b-btn
                                type="submit"
                                variant="primary"
                                size="lg"
                            >
                                Se connecter
                            </b-btn>
                        </b-form>
                    </b-card>
                </b-col>
            </b-row>
        </b-collapse>
    </b-container>
</template>

<script>
export default {
    data: function () {
        return {
            modelLogin: false,
            showModelLogin: false,
            csrfToken: "",
            googleLogin: "",
            microsoftLogin: "",
        };
    },
    mounted: function () {
        this.modelLogin = typeof hasModelLogin !== "undefined";
        // eslint-disable-next-line no-undef
        this.microsoftLogin = typeof microsoftURL !== "undefined" ? microsoftURL : "";
        // eslint-disable-next-line no-undef
        this.googleLogin = typeof googleURL !== "undefined" ? googleURL : "";

        if (this.modelLogin) {
            // eslint-disable-next-line no-undef
            this.csrfToken = csrfToken;

            this.showModelLogin = this.microsoftLogin.length > 0 || this.googleLogin.length > 0;
        }
    }
};
</script>
