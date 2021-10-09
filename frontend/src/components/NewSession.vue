<template>
  <b-col lg="" id="new-session" class="mx-lg-0 mx-1 mb-lg-2 mb-5">
    <div class="section-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21 12l-18 12v-24z"/></svg>
        <span>new</span>
    </div>
    <div class="section-body">
      <div v-if="Object.keys(res).length === 0 && res.constructor === Object">
        <CLoader :type="'NG'"/>
      </div>
      <div v-else-if="this.parentPage === 'League'">
          <b-tabs
            v-if="patchNames !== null"
            pills
            nav-class="gilded-nav"
            active-nav-item-class="selected-tab"
            content-class="mt-2"
            align="center"
            v-model="selectedValues.patch"
          >
            <b-tab v-for="(patch, idx) in patchNames" :key="idx" :title="patch">
            </b-tab>
          </b-tabs>
          <p
          role="button"
          v-for="(league, idx) in filteredRes" :key="idx"
          v-on:click="selectedValues.leagues = league"
          :class="league.id === selectedValues.leagues.id && 'underline'"
          >
            <span v-if="patchNames === null">{{ league.version }}</span>
            {{ league.name }}
          </p>
          <p v-if="filteredRes.length === 0">
            ...
          </p>
        <b-row v-if="selectedValues.leagues">
          <b-col align-self="center">
            <b-img-lazy
            thumbnail
            :alt="selectedValues.leagues.name"
            :src="require('@/assets/league_banners/'+ selectedValues.leagues.banner)"
            :blank-src="require('@/assets/league_banners/default.png')"
            >
            </b-img-lazy>
          </b-col>
          <b-col class="lead">
            <b-row>
              <span><b>{{ selectedValues.lengths.easy }}/{{ selectedValues.leagues.ids.easy.length }}</b> easy matches</span>
              <b-form-input number type="range" min="0" :max="easyMax" v-model="selectedValues.lengths.easy">
              </b-form-input>
            </b-row>
            <b-row>
              <span><b>{{ selectedValues.lengths.med }}/{{ selectedValues.leagues.ids.medium.length }}</b> medium matches</span>
              <b-form-input number type="range" min="0" :max="medMax" v-model="selectedValues.lengths.med">
              </b-form-input>
            </b-row>
            <b-row>
              <span><b>{{ selectedValues.lengths.hard }}/{{ selectedValues.leagues.ids.hard.length }}</b> hard matches</span>
              <b-form-input number type="range" min="0" :max="hardMax" v-model="selectedValues.lengths.hard">
              </b-form-input>
            </b-row>
          </b-col>
          <b-col lg="" align-self="center">
            <b-row class="justify-content-center lead">
              <span><b>{{params.noIds}}</b> matches selected in total</span>
            </b-row>
            <b-row v-if="params.noIds < 10" class="justify-content-center small">
              <span>Select at-least 10 matches to continue</span>
            </b-row>
            <b-row v-else class="justify-content-center small mt-2">
              <b-button class="selected-tab" size="sm" :pressed.sync="toggleSettings">
                <span v-if="toggleSettings">Hide game settings</span>
                <span v-else>Show game settings</span>
              </b-button>
            </b-row>
          </b-col>
        </b-row>
      </div>
      <div v-else-if="this.parentPage === 'RandPro'">
        params form for randpro
      </div>
      <transition name="slide">
        <div v-show="toggleSettings" class="mt-2">
          <b-form-group
          :label="gameMode.label"
          :id="gameMode.model"
          class="mb-2"
          >
            <b-form-radio-group
            v-model="params[gameMode.model]"
            :options="gameMode.options"
            >
            </b-form-radio-group>
          </b-form-group>
          <div id="optionSelect">
            <b-form-group
            v-for="(obj, idx) in optionSchema" :key="idx"
            :label="obj.label"
            :id="obj.model"
            class="mb-2"
            >
            <b-form-radio-group
              v-model="params[obj.model]"
              :options="obj.options"
              :disabled="params.preset !== 0"
            >
            </b-form-radio-group>
            </b-form-group>
            </div>
          <b-button class="selected-tab my-2" size="md" @click="createGame()">
            <span>Start game</span>
          </b-button>
        </div>
      </transition>
    </div>
  </b-col>
</template>

<script>
import CLoader from '@/components/CLoader.vue';

export default {
  name: 'NewSession',
  components: {
    CLoader,
  },
  data() {
    return {
      parentPage: this.$route.name,
      patchNames: null,
      toggleSettings: false,
      gameMode: {
        label: 'Mode?',
        model: 'preset',
        options: [{ text: 'Easy', value: 1 }, { text: 'Normal', value: 2 }, { text: 'Quickfire', value: 3 }, { text: 'Custom', value: 0 }],
      },
      optionSchema: [
        {
          label: 'Time/match?',
          model: 'timePerQ',
          options: [{ text: '60s', value: 60 }, { text: '30s', value: 30 }, { text: '15s', value: 15 }, { text: '10s', value: 10 }],
        },
        {
          label: 'Time bonus?',
          model: 'timeBonus',
          options: [{ text: 'Yes', value: true }, { text: 'No', value: false }],
        },
        {
          label: 'Include hints?',
          model: 'hints',
          options: [{ text: 'Yes', value: true }, { text: 'No', value: false }],
        },
        {
          label: 'Score penalty on hints?',
          model: 'hintsPenalty',
          options: [{ text: 'Yes', value: true }, { text: 'No', value: false }],
        },
        {
          label: 'Include team and league info as hints?',
          model: 'incMeta',
          options: [{ text: 'Yes', value: true }, { text: 'No', value: false }],
        },
        {
          label: 'Amount of lives?',
          model: 'lives',
          options: [{ text: 'Zero', value: 0 }, { text: 'One', value: 1 }, { text: 'Two', value: 2 }, { text: 'Unlimited', value: -1 }],
        },
      ],
      params: {
        ids: {
          easy: [],
          medium: [],
          hard: [],
        },
        cached: [],
        results: {
          correct_ids: [],
          incorrect_ids: [],
          time_taken: 0,
          lives_used: 0,
          hints_used: 0,
        },
        score: 0,
        streak: 0,
        noIds: 0,
        preset: 0,
        timePerQ: 10,
        currentTime: 10,
        timeBonus: false,
        hints: false,
        hintsPenalty: false, // dependant on value of hints
        incMeta: false, // dependant on value of hints
        lives: -1,
        break: 5,
      },
      res: {},
      selectedValues: {
        patch: 0,
        leagues: 0,
        lengths: {
          easy: 0,
          med: 0,
          hard: 0,
        },
      },
    };
  },
  computed: {
    filteredRes() {
      if (this.patchNames === null) {
        return this.res;
      }
      return this.res.filter((league) => league.version === this.patchNames[this.selectedValues.patch]);
    },
    easyMax() {
      return this.selectedValues.leagues.ids.easy.length;
    },
    medMax() {
      return this.selectedValues.leagues.ids.medium.length;
    },
    hardMax() {
      return this.selectedValues.leagues.ids.hard.length;
    },
  },
  watch: {
    'selectedValues.leagues': {
      handler(league) {
        if (league !== 0) {
          this.selectedValues.lengths.easy = 0;
          this.selectedValues.lengths.med = 0;
          this.selectedValues.lengths.hard = 0;
        }
      },
    },
    'selectedValues.lengths': {
      deep: true,
      handler() {
        this.params.ids.easy = this.getSample(this.selectedValues.leagues.ids.easy, this.selectedValues.lengths.easy);
        this.params.ids.medium = this.getSample(this.selectedValues.leagues.ids.medium, this.selectedValues.lengths.med);
        this.params.ids.hard = this.getSample(this.selectedValues.leagues.ids.hard, this.selectedValues.lengths.hard);
        this.params.noIds = this.selectedValues.lengths.easy + this.selectedValues.lengths.med + this.selectedValues.lengths.hard;
      },
    },
    'params.preset': {
      handler(val) {
        switch (val) {
          case 1:
            this.params.timePerQ = 60;
            this.params.currentTime = 60;
            this.params.timeBonus = true;
            this.params.hints = true;
            this.params.hintsPenalty = false;
            this.params.incMeta = false;
            this.params.lives = 2;
            break;
          case 2:
            this.params.timePerQ = 30;
            this.params.currentTime = 30;
            this.params.timeBonus = true;
            this.params.hints = true;
            this.params.hintsPenalty = true;
            this.params.incMeta = true;
            this.params.lives = 2;
            break;
          case 3:
            this.params.timePerQ = 10;
            this.params.currentTime = 10;
            this.params.timeBonus = true;
            this.params.hints = false;
            this.params.hintsPenalty = true;
            this.params.incMeta = true;
            this.params.lives = 1;
            break;
          default:
            break;
        }
      },
    },
    'params.noIds': {
      // ensures that menu is hidden if matches slider is changed again
      handler(val) {
        if (val < 10) {
          this.toggleSettings = false;
        }
      },
    },
  },
  methods: {
    getLeagues() {
      return this.$api.get('/getLeagues')
        .then((res) => res.data.data.leagues)
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSample(arr, count) {
      const a = arr.slice();
      for (let i = a.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a.slice(0, count);
    },
    createGame() {
      const randomKey = [...Array(7)].map(() => Math.random().toString(36)[2]).join('');
      this.nFSessionStore.setItem(randomKey, this.params)
        .finally(() => {
          this.$router.push({ name: 'LeagueSession', params: { session: randomKey } });
        }).catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.cachedStore.getItem('patchContent')
      .then((obj) => {
        this.patchNames = obj.names;
      });
    if (this.parentPage === 'League') {
      this.getLeagues()
        .then((res) => {
          // eslint-disable-next-line
          const SORTEDRES = res.sort((a, b) => (a.version > b.version) ? 1 : -1);
          this.res = SORTEDRES;
        });
    }
  },
  mounted() {
    // find a different way, today was too hot to think
    this.$watch('params.hints', (val) => {
      const hintsPenalty = document.getElementById('hintsPenalty');
      const incMeta = document.getElementById('incMeta');
      if (val === false) {
        hintsPenalty.style.display = 'none';
        incMeta.style.display = 'none';
      } else {
        hintsPenalty.style.display = 'block';
        incMeta.style.display = 'block';
      }
    }, { immediate: true });
  },
};
</script>

<style lang="scss">
.selected-tab{
  color: $bg-color !important;
  background-color: $gold !important;
  text-shadow: none !important;
  border: none;
}
.gilded-nav{
  a{
    color: $gold-text;
    &:hover{
      color: $gold;
    }
  }
  .nav-link{
    &:focus{
      outline: none;
    }
  }
}
.underline{
  text-decoration: underline;
}
@mixin track() {
  background-color: $bg-color;
}
@mixin progress() {
  background-color: $gold;
}
@mixin thumb() {
  background-color: $gold;
  cursor: pointer;
}
.custom-range{
  width: 95%;
  &:active {
    &::-webkit-slider-thumb {
      background-color: $gold;
    }
    &::-moz-range-thumb {
      background-color: $gold;
    }
    &::-ms-thumb {
      background-color: $gold;
    }
  }
  &::-webkit-slider-runnable-track { @include track }
  &::-moz-range-track { @include track }
  &::-ms-track { @include track }
  &::-moz-range-thumb { @include thumb }
  &::-ms-thumb { @include thumb }
  &::-webkit-slider-thumb { @include thumb }
  &::-moz-range-progress { @include progress }
  &::-ms-fill-lower { @include progress }
  &::-ms-fill-upper { @include progress }
}
.img-thumbnail {
  border: none ;
  background-color: $gold-text;
}
.custom-control-label::before{
  background-color: $bg-color;
  border-color: $bg-color;
}
.custom-control-input:not(:disabled):active ~ .custom-control-label::before {
  background-color: $bg-color;
  border-color: $bg-color;
}
.custom-control-input:checked ~ .custom-control-label::before {
  border-color: $gold;
  background-color: $bg-color;
  box-shadow: none !important;
}
.custom-radio .custom-control-input:checked ~ .custom-control-label::after{
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23A5813F'/%3e%3c/svg%3e")
}
.custom-control-input[disabled] ~ .custom-control-label, .custom-control-input:disabled ~ .custom-control-label {
  color: rgba($color: $gold-text, $alpha: 0.5);
  &::before{
    background-color: rgba($color: $grayed-out, $alpha: 0.5);
  }
}
.custom-radio .custom-control-input:disabled:checked ~ .custom-control-label::before{
  background-color: rgba($color: $grayed-out, $alpha: 0.5);
}
.slide-enter-active {
   -moz-transition-duration: 0.5s;
   -webkit-transition-duration: 0.5s;
   -o-transition-duration: 0.5s;
   transition-duration: 0.5s;
   -moz-transition-timing-function: ease-in;
   -webkit-transition-timing-function: ease-in;
   -o-transition-timing-function: ease-in;
   transition-timing-function: ease-in;
}

.slide-leave-active {
   -moz-transition-duration: 0.5s;
   -webkit-transition-duration: 0.5s;
   -o-transition-duration: 0.5s;
   transition-duration: 0.5s;
   -moz-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
   -webkit-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
   -o-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
   transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
}

.slide-enter-to, .slide-leave {
   max-height: 50vh;
   overflow: hidden;
}

.slide-enter, .slide-leave-to {
   overflow: hidden;
   max-height: 0;
}
</style>
