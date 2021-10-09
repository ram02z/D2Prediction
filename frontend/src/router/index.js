import Vue from 'vue';
import VueRouter from 'vue-router';

const HOME = () => import('@/views/Home.vue');
const LIVE = () => import('@/views/Live.vue');
const LIVERESULTS = () => import('@/views/LiveResults.vue');
const RANDPRO = () => import('@/views/RandPro.vue');
const RANDPRORESULTS = () => import('@/views/RandProResults.vue');
const LEAGUE = () => import('@/views/League.vue');
const LEAGUERESULTS = () => import('@/views/LeagueResults.vue');

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HOME,
    },
    {
      path: '/live',
      name: 'Live',
      component: LIVE,
    },
    {
      path: '/live/results',
      component: LIVERESULTS,
      children: [
        { path: '', name: 'LiveResults', meta: { scored: true } },
        { path: 'pending', name: 'LiveResultsPending', meta: { scored: false } },
      ],
    },
    {
      path: '/pro',
      name: 'RandPro',
      component: RANDPRO,
    },
    {
      path: '/pro/results',
      name: 'RandProResults',
      component: RANDPRORESULTS,
    },
    {
      path: '/league',
      component: LEAGUE,
      children: [
        { path: '', name: 'League' },
        { path: ':session', name: 'LeagueSession' },
      ],
    },
    {
      path: '/league/results',
      name: 'LeagueResults',
      component: LEAGUERESULTS,
    },
  ],
});

export default router;
