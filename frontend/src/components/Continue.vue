<template>
  <b-col lg="" id="continue" class="mx-lg-0 mx-1 mb-lg-2 mb-4">
    <div class="section-title">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M14 12l-14 9v-18l14 9zm-4-9v4l8.022 5-8.022 5v4l14-9-14-9z"/></svg>
      <span>continue</span>
    </div>
    <div class="section-body">
      <div v-if="sessions.length > 0">
        <b-row class="justify-content-center ml-lg-0" v-for="(session, IDX) in sessions" :key="IDX">
          {{ session.key }}
          </b-row>
      </div>
      <b-row class="justify-content-center ml-lg-0 my-1" v-else>
        No incomplete game sessions available.
      </b-row>
    </div>
  </b-col>
</template>

<script>
export default {
  name: 'Continue',
  data() {
    return {
      sessions: [],
    };
  },
  created() {
    this.nFSessionStore.iterate((val, key) => {
      const session = val;
      session.key = key;
      switch (val.preset) {
        case 0:
          session.preset = 'custom';
          break;
        case 1:
          session.preset = 'easy';
          break;
        case 2:
          session.preset = 'normal';
          break;
        case 3:
          session.preset = 'quickfire';
          break;
        default:
          session.preset = 'custom';
      }
      this.sessions.push(val);
    });
  },
};
</script>

<style lang="scss" scoped>
</style>
