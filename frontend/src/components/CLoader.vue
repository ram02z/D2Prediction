<template>
    <content-loader v-if="type === 'GC'" :width="650" :height="360" :speed="1" primaryColor="#272727" secondaryColor="#2f2f2f">
        <rect x="287" y="0" rx="50" ry="50" width="76" height="76" />
        <rect transform="skewX(5)" x="15" y="85" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(5)" x="132" y="85" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(5)" x="249" y="85" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(5)" x="366" y="85" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(5)" x="484" y="85" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(-5)" x="43" y="175" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(-5)" x="160" y="175" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(-5)" x="277" y="175" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(-5)" x="393" y="175" rx="0" ry="0" width="110" height="68" />
        <rect transform="skewX(-5)" x="509" y="175" rx="0" ry="0" width="110" height="68" />
        <rect x="140" y="275" rx="0" ry="0" width="198" height="36" />
        <rect x="347" y="275" rx="0" ry="0" width="150" height="36" />
        <rect x="-80" y="330" rx="10" ry="10" width="150" height="100" />
        <rect x="626" y="330" rx="100" ry="100" width="24" height="24" />
        <rect x="30" y="55" rx="10" ry="10" width="133" height="23" />
        <rect x="26" y="250" rx="10" ry="10" width="98" height="23" />
        <!-- <rect x="25" y="156" rx="0" ry="0" width="580" height="16" /> -->
    </content-loader>
    <content-loader v-else-if="type === 'NG'" :width="650" :height="150" :speed="1" primaryColor="#272727" secondaryColor="#2f2f2f">
        <rect x="0" y="0" rx="0" ry="0" width="650" height="150" />
    </content-loader>
</template>

<script>
import { ContentLoader } from 'vue-content-loader';

export default {
  name: 'CLoader',
  components: { ContentLoader },
  props: ['type'],
};
</script>

<style lang="scss" scoped>

</style>
