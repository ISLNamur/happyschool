<template>
    <div>
        <b-navbar toggleable type="light" variant="light">
            <b-nav-toggle target="nav_text_collapse"></b-nav-toggle>
            <b-navbar-brand href="/schedule_change">
                <img src="/static/img/logo_isln.png" class="d-inline-block align-top" alt="BV">
                Appyschool
            </b-navbar-brand>
            <b-collapse is-nav id="nav_text_collapse">
                <b-navbar-nav is-nav-bar v-for="(app, key) in apps" :key="key">
                    <b-nav-item :active="app.active" :href="app.url">{{ app.display}}</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
export default {
    props: ['apps'],
}
</script>

<style>
</style>
