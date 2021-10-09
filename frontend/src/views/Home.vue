<template>
  <b-container fluid="lg" class="mt-4">
    <header>
      <b-row align-h="center" class="no-select">
        <span class="display-2 gold-color">D2Predictions</span>
      </b-row>
      <b-row align-h="center" class="mb-1">
        <span class="gold-text small">chnage this</span>
      </b-row>
    </header>
    <main>
      <b-row>
        <Status/>
        <Continue/>
      </b-row>
      <b-row>
        <b-col lg="" id="changelog" class="mx-lg-0 mx-1 mb-lg-2 mb-4">
          <div class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M5.485 3.567l6.488-3.279c.448-.199.904-.288 1.344-.288 1.863 0 3.477 1.629 3.287 3.616l-7.881 4.496c.118-2.088-1.173-4.035-3.238-4.545zm15.857 8.996c-.928-1.137-4.549-4.567-5.762-6.045l-8.855 5.069-1.083-1.354c1.16-.757 1.431-2.619.632-3.799-1.383-2.042-4.274-1.037-4.274 1.129 0 .653.263 1.412.909 2.225.018.023 7.109 8.25 8.531 9.873.768.874 1.081 1.8 1.061 2.71 8.836-5.572 7.833-4.958 7.996-5.065.98-.643 1.503-1.747 1.503-2.827 0-.691-.214-1.372-.658-1.916zm-13.562 5.937c-2.148 1.09-2.38 3.252-1.222 4.598.545.632 1.265.902 1.943.902 1.476 0 2.821-1.337 1.567-2.877-1.3-1.599-2.288-2.623-2.288-2.623z"/></svg>
            <span>changelog</span>
          </div>
          <div class="section-body">
            markdown render
          </div>
        </b-col>
        <Settings/>
      </b-row>
    </main>
  </b-container>
</template>

<script>
import Settings from '@/components/Settings.vue';
import Status from '@/components/Status.vue';
import Continue from '@/components/Continue.vue';

export default {
  name: 'Home',
  components: {
    Settings,
    Status,
    Continue,
  },
};
</script>

<style lang="scss">
@media (min-width: 992px) {
  main{
    display: grid;
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    height: calc(100vh - 105px - 24px - 40px - 38px - 14px );// title - padding - navbar - idek forgot
    .row{
      align-self: center;
      justify-self: center;
      width: 100%;
    }
  }
}
</style>
