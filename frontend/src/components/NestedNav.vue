<template>
    <div id="nested-nav" class="row mx-auto">
        <b-col v-for="(link, idx) in links" :key="idx" class="live-nav"><router-link :to="{ name: link.name }" v-slot="{ route, href, navigate }">
            <a
            @click="navigate"
            :class="route.path.split('/')[2] === $route.path.split('/')[2] ? 'router-link-active' : ''"
            :aria-current="route.path.split('/')[2] === $route.path.split('/')[2] && 'page'"
            :href="href"
            ><slot></slot
            >{{ link.tag }}</a></router-link>
        </b-col>
    </div>
</template>
<script>
export default {
  name: 'NestedNav',
  props: ['links'],
};
</script>

<style lang="scss" scoped>
@import "@/assets/styles/_classes.scss";

#nested-nav{
    max-width: $app-width;
    .live-nav > a{
        @extend %title;
        text-transform: uppercase;
        position: relative;
        display: inline-block;
        &:before{
            content: "";
            position: absolute;
            width: 100%;
            height: 2px;
            bottom: 2px;
            background-color: $gold;
            visibility: hidden;
            transform: scaleX(0);
            transition: all 0.3s ease-in-out;
        }
        &:hover:before{
            visibility: visible;
            transform: scaleX(1);
        }
    }
    .live-nav > .router-link-active{
        opacity: 0.5!important;
        cursor: not-allowed;
        // cursor: url('assets/dota_cursor_illegal.png'), auto;
        &:before{
            visibility: hidden!important;
            transition: none !important;
        }
    }
}

</style>
