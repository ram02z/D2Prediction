import Vlf from 'vlf';
import localforage from 'localforage';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import api from './plugins/api';

Vue.use(Vlf, localforage);
// Install BootstrapVue
Vue.use(BootstrapVue);

Vue.config.productionTip = false;

// Global axios and interceptors
Vue.prototype.$api = api;
/* eslint-disable no-param-reassign */
api.interceptors.request.use((config) => {
  config.headers.requestStartTime = Date.now();
  return config;
}, (error) => Promise.reject(error));

api.interceptors.response.use((response) => {
  const requestStart = response.config.headers.requestStartTime;
  response.headers.requestDuration = Date.now() - requestStart;
  return response;
}, (error) => Promise.reject(error));
/* eslint-enable no-param-reassign */

Vue.mixin({
  data() {
    return {
      settingsStore: this.settingsInstance(),
      votedLiveStore: this.votedLiveInstance(),
      scoredLiveStore: this.scoredLiveInstance(),
      cachedStore: this.cachedInstance(),
      nFSessionStore: this.nFSessionInstance(),
      fSessionStore: this.fSessionInstance(),
    };
  },
  methods: {
    settingsInstance() {
      try {
        return this.$vlf.instance('settings');
      } catch (err) {
        return this.$vlf.createInstance({
          name: 'settings',
          description: 'Stores the user preferences.',
        });
      }
    },
    votedLiveInstance() {
      try {
        return this.$vlf.instance('votedLive');
      } catch (err) {
        return this.$vlf.createInstance({
          name: 'votedLive',
          description: 'Stores live games the user has voted for awaiting completion.',
        });
      }
    },
    scoredLiveInstance() {
      try {
        return this.$vlf.instance('scoredLive');
      } catch (err) {
        return this.$vlf.createInstance({
          name: 'scoredLive',
          description: 'Stores live games the user has voted that have been scored.',
        });
      }
    },
    nFSessionInstance() {
      try {
        return this.$vlf.instance('nFSession');
      } catch (err) {
        return this.$vlf.createInstance({
          name: 'nFSession',
          description: 'Stores game sessions that have not been completed.',
        });
      }
    },
    fSessionInstance() {
      try {
        return this.$vlf.instance('fSession');
      } catch (err) {
        return this.$vlf.createInstance({
          name: 'fSession',
          description: 'Stores completed game sessions.',
        });
      }
    },
    cachedInstance() {
      try {
        return this.$vlf.instance('cached');
      } catch (err) {
        return this.$vlf.createInstance({
          name: 'cached',
          description: 'Stores cached responses to save on loaded times.',
        });
      }
    },
  },
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
