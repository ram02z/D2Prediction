<template>
  <b-container fluid="lg" class="mt-4">
    <NestedNav :links="[{ name: 'League', tag: 'Play' }, { name: 'LeagueResults', tag: 'Results' }]"/>
    <div v-if="showingSession">
      <div v-if="Object.keys(session).length !== 0 && session.constructor === Object">
        <div v-if="game.length === 0 || emptyCache === true" class="content-loader mx-auto">
          <CLoader :type="'GC'"/>
        </div>
        <div v-else class="game-card mx-auto">
                    <b-row v-if="radiantVote === null">
            <span class="radiant-title d-flex align-items-end mr-5">THE RADIANT</span>
      </b-row>
          <GameCard :game="game" :class="{ 'rad-won' : game.radiant_vote === true, 'dire-won' : game.radiant_vote === false}"/>
          <b-row v-if="radiantVote === null">
            <span class="dire-title d-flex align-items-end mr-5">THE DIRE</span>
      </b-row>
        <b-row class="justify-content-center" v-if="radiantVote === null && timeCount !== 0">
          <button v-on:click="radiantVote = true" class="mr-1 radiant-button"><span>VOTE RADIANT</span></button>
          <button v-on:click="radiantVote = false" class="ml-1 dire-button"><span>VOTE DIRE</span></button>
        </b-row>
        <b-row v-if="timeCount === 0" class="justify-content-center mt-3" id="vote-title">
          YOU RAN OUT OF TIME
        </b-row>
      <b-row class="justify-content-between mt-3 ml-1">
        <div class="time-badge">
          <span class="float-left">{{fmtMSS(timeCount)}}</span>
        </div>
        <svg :id="'tooltip-target-info'" fill="#e4c269" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
        <path d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm-.001 5.75c.69 0 1.251.56 1.251 1.25s-.561 1.25-1.251 1.25-1.249-.56-1.249-1.25.559-1.25 1.249-1.25zm2.001 12.25h-4v-1c.484-.179 1-.201 1-.735v-4.467c0-.534-.516-.618-1-.797v-1h3v6.265c0 .535.517.558 1 .735v.999z"/>
        </svg>
        </b-row>
        <b-row v-if="radiantVote !== null || timeCount === 0" class="my-4 justify-content-center">
          <button class="reload-button" v-on:click="forceRerender()"><span>NEXT MATCH</span></button>
        </b-row>
        </div>
      </div>
      <div v-else>
        <Continue/>
        <div class="gold-text lead mt-4">
          <p>Game session not found. Any incomplete game sessions are shown above.</p>
          <b-button class="selected-tab" size="sm" :to="{ name: 'League'}">
            <span>Back to league page</span>
          </b-button>
        </div>
      </div>
    </div>
    <div v-else id="league-forms">
      <Continue/>
      <NewSession/>
    </div>
  </b-container>
</template>

<script>
import NestedNav from '@/components/NestedNav.vue';
import Continue from '@/components/Continue.vue';
import NewSession from '@/components/NewSession.vue';
import GameCard from '@/components/GameCard.vue';
import CLoader from '@/components/CLoader.vue';

export default {
  name: 'League',
  components: {
    NestedNav,
    Continue,
    NewSession,
    GameCard,
    CLoader,
  },
  data() {
    return {
      showingSession: false,
      emptyCache: true,
      session: {},
      session_id: this.$route.params.session,
      game: [],
      radiantVote: null,
      timeCount: NaN,
    };
  },
  watch: {
    '$route.params.session': {
      handler(session) {
        if (session) {
          this.showingSession = true;
          this.nFSessionStore.iterate((value, key) => {
            if (key === session) {
              this.session = value;
              const CACHENO = 3 - value.cached.length; // max number of cached games
              if (CACHENO > 0) {
                if (CACHENO !== 3) {
                  this.emptyCache = false;
                }
                this.cacheMatches(CACHENO);
              } else {
                this.emptyCache = false;
              }
            }
          });
        } else {
          this.showingSession = false;
          this.session = {};
        }
      },
      deep: true,
      immediate: true,
    },
    emptyCache: {
      handler(val) {
        if (val === false) {
          this.game = this.session.cached.find((e) => e !== undefined);
          if (this.game === undefined) {
            this.emptyCache = true;
            this.cacheMatches(3);
          } else {
            this.timeCount = this.session.timePerQ * 100;
          }
        } else if (val === true) {
          console.log('cache is empty');
        }
      },
    },
    timeCount: {
      handler(value) {
        if (value > 0) {
          if (this.radiantVote === null) {
            setTimeout(() => {
              this.timeCount -= 1;
            }, 1000);
          }
        }
      },
      immediate: true,
    },
    radiantVote: {
      handler(value) {
        if (value === true || value === false) {
          this.game.radiant_vote = value;
          this.session.cached.shift();
          if (value === this.game.radiant_outcome) {
            this.session.results.correct_ids.push(this.game);
          } else {
            this.session.results.incorrect_ids.push(this.game);
          }
        }
      },
    },
  },
  methods: {
    cacheMatches(cacheNo) {
      for (let i = 0; i < cacheNo; i += 1) {
        const currentIdTotal = this.session.ids.easy.length + this.session.ids.medium.length + this.session.ids.hard.length;
        const easyWeight = (this.session.ids.easy.length / currentIdTotal);
        const mediumWeight = (this.session.ids.medium.length / currentIdTotal);
        const hardWeight = (this.session.ids.hard.length / currentIdTotal);
        const fromList = this.nextGame(easyWeight, mediumWeight, hardWeight);
        const MATCHID = (() => {
          switch (fromList) {
            case 0:
              return this.session.ids.easy.shift();
            case 1:
              return this.session.ids.medium.shift();
            case 2:
              return this.session.ids.hard.shift();
            default:
              break;
          }
        })();
        this.$api.get(`/match/${MATCHID}`, {
          params: {
            full: this.session.hints,
          },
        })
          .catch(() => {
            console.log(`error on ${MATCHID}`);
            this.session.noIds -= 1;
          })
          .then((res) => {
            if (res.data.error === true) {
              console.log(`error on ${MATCHID}`);
              this.session.noIds -= 1;
            } else {
              this.session.cached.push(res.data.data);
              if (this.session_id !== undefined) {
                this.nFSessionStore.setItem(this.session_id, this.session).catch((err) => { console.log(err); });
              }
              this.emptyCache = false;
            }
          });
      }
    },
    nextGame(easyWeight, mediumWeight, hardWeight) {
      const PMF = [easyWeight, mediumWeight, hardWeight];
      const CDF = PMF.map(((sum) => (value) => sum += value)(0)); // eslint-disable-line
      const R = Math.random();
      return CDF.filter((el) => R >= el).length;
    },
    fmtMSS(s) {
      let sec = s;
      const MSS = (sec - (sec %= 60)) / 60 + (sec > 9 ? 'm ' : 'm ') + sec;
      return `${MSS}s`;
    },
    forceRerender() {
      this.$parent.componentKey += 1;
    },
  },
  beforeDestroy() {
    this.nFSessionStore.keys().then((keys) => {
      if (keys.includes(this.session_id) && this.session_id !== undefined) {
        this.nFSessionStore.setItem(this.session_id, this.session).catch((err) => { console.log(err); });
      }
    });
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/styles/gamecard.scss";
</style>
