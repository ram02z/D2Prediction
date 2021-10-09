<template>
  <b-container fluid="lg" class="mt-4">
    <NestedNav :links="[{ name: 'League', tag: 'Play' }, { name: 'LeagueResults', tag: 'Results' }]"/>
  </b-container>
</template>

<script>
import NestedNav from '@/components/NestedNav.vue';

export default {
  name: 'LeagueResults',
  components: {
    NestedNav,
  },
};
</script>
