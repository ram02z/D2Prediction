<template>
  <b-container fluid="lg" class="mt-4">
    <NestedNav :links="[{ name: 'RandPro', tag: 'Play' }, { name: 'RandProResults', tag: 'Results' }]"/>
    <p v-if="error">Error: {{ error }} - {{ errorMsg }}</p>
  </b-container>
</template>
<script>
import axios from 'axios';
import NestedNav from '@/components/NestedNav.vue';

export default {
  name: 'RandPro',
  components: {
    NestedNav,
  },
  data() {
    return {
      error: null,
      errorMsg: '',
    };
  },
  methods: {
    pingExplorer() {
      const path = 'http://localhost:5000/api/pingexplorer';
      axios.get(path)
        .then((res) => {
          this.error = res.data.error;
          this.errorMsg = res.data.data.message;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.error = true;
          this.errorMsg = String(error.message);
          console.error(error);
        });
    },
  },
  created() {
    // this.pingExplorer();
  },
};
</script>
