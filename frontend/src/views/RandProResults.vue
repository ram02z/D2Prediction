<template>
  <b-container fluid="lg" class="mt-4">
    <NestedNav :links="[{ name: 'RandPro', tag: 'Play' }, { name: 'RandProResults', tag: 'Results' }]"/>
  </b-container>
</template>

<script>
import NestedNav from '@/components/NestedNav.vue';

export default {
  name: 'RandProResults',
  components: {
    NestedNav,
  },
};
</script>
