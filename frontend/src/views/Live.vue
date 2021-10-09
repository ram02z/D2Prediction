<template>
<b-container fluid="lg" class="mt-4">
  <NestedNav :links="[{ name: 'Live', tag: 'Live' }, { name: 'LiveResults', tag: 'Results' }]"/>
  <b-container class="error-display" v-if="error === true">
    <div class="error-message">
      <h1>Something went wrong. Please try again later.</h1>
      <h4><b>Reason: </b>{{ errorMsg }}</h4>
    </div>
  </b-container>
  <div v-else-if="game.length === 0" class="content-loader mx-auto">
    <CLoader :type="'GC'"/>
  </div>
  <div v-else-if="error === false">
    <div class="game-card mx-auto">
      <b-row class="justify-content-around">
          <span class="radiant-title d-flex align-items-end mr-5">THE RADIANT</span>
          <b-img-lazy
          class="mx-5 medal mb-2" height="76px" width="76px"
          rounded="circle"
          :src="require('@/assets/medals/'+ game.medal + '_full.png')"
          blank-color='#2f2f2f'
          :alt="game.average_mmr + ' MMR'">
          </b-img-lazy>
          <span class="hidden-title d-flex align-items-end ml-5 hidden">THE RADIANT</span>
        </b-row>
      <GameCard :game="game" :class="{ 'rad-voted' : radiantVote === true, 'dire-voted' : radiantVote === false, 'noteam-voted' : radiantVote === null && timeCount === 0 }"/>
      <b-row>
        <span class="dire-title d-flex align-items-end mr-5">THE DIRE</span>
      </b-row>
        <b-row class="justify-content-center" v-if="radiantVote === null && timeCount !== 0">
          <button v-on:click="radiantVote = true" class="mr-1 radiant-button"><span>VOTE RADIANT</span></button>
          <button v-on:click="radiantVote = false" class="ml-1 dire-button"><span>VOTE DIRE</span></button>
        </b-row>
        <b-row v-if="timeCount !== 0 && radiantVote !== null" class="justify-content-center mt-3" id="vote-title">
          <span v-if="radiantVote">YOU VOTED <span class="radiant-color">RADIANT</span></span>
          <span v-else>YOU VOTED <span class="dire-color">DIRE</span></span>
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
          <b-tooltip delay="0" variant="dark" placement="right" :target="'tooltip-target-info'" triggers="hover">
            <b>Radiant lineup likelihood: </b><abbr title="Help section explains how 'likelihood' is determined">{{likelihoodText(game.radiant_likelihood)}}</abbr> <br>
            <b>Dire lineup likelihood: </b>{{likelihoodText(game.dire_likelihood)}} <br>
            <b>Average MMR: </b>{{game.average_mmr}} <br>
            <b>Server ID: </b>{{game.server_id}}
          </b-tooltip>
        </b-row>
        <b-row v-if="radiantVote !== null || timeCount === 0" class="my-4 justify-content-center">
          <button class="reload-button" v-on:click="forceRerender()"><span>NEW MATCH</span></button>
        </b-row>
        <b-row class="justify-content-center">
          <span class="matchq-title mt-2">NO. OF MATCHES LEFT: <span class="text-light">{{noMatches - 1}}</span></span>
        </b-row>
    </div>
    </div>
  </b-container>
</template>

<script>
import NestedNav from '@/components/NestedNav.vue';
import CLoader from '@/components/CLoader.vue';
import GameCard from '@/components/GameCard.vue';

export default {
  name: 'Live',
  components: {
    CLoader,
    GameCard,
    NestedNav,
  },
  data() {
    return {
      game: [],
      timeCount: NaN,
      error: null,
      errorMsg: '',
      radiantVote: null,
      noMatches: 0,
    };
  },
  methods: {
    filteredLive() {
      this.$api.get('/filteredLive?ux&test')
        .then((res) => {
          this.error = res.data.error;
          if (this.error === false) {
            this.filterResponse(res.data.data)
              .then((RESPONSE) => {
                this.noMatches = RESPONSE.length;
                if (RESPONSE.length === 0) {
                  this.error = true;
                  this.errorMsg = 'You have voted on all the current live games';
                  return;
                }
                const INDEX = Math.floor(Math.random() * RESPONSE.length);
                this.game = RESPONSE[INDEX];
                this.timeCount = RESPONSE[INDEX].time_remaining;
              });
          } else {
            this.errorMsg = 'Steams live match api is down';
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.error = true;
          this.errorMsg = String(error.message);
        });
    },
    filterResponse(response) {
      // Combines the two key promises containing the match ids to filter the axios response
      const FILTEREDRESPONSE = [];
      const votedIDs = this.votedLiveStore.keys();
      const scoredIDs = this.scoredLiveStore.keys();
      return Promise.all([votedIDs, scoredIDs])
        .then((ids) => {
          const combinedIDs = ids.reduce((arr1, arr2) => arr1.concat(arr2), []).map(Number);
          for (let i = 0; i < response.length; i += 1) {
            if (combinedIDs.includes(response[i].match_id) === false) {
              FILTEREDRESPONSE.push(response[i]);
            }
          }
          return FILTEREDRESPONSE;
        });
    },
    fmtMSS(s) {
      let sec = s;
      const MSS = (sec - (sec %= 60)) / 60 + (sec > 9 ? 'm ' : 'm ') + sec;
      return `${MSS}s`;
    },
    forceRerender() {
      this.$parent.componentKey += 1;
    },
    likelihoodText(x) {
      if (x === -1) {
        return 'Unlikely';
      }
      if (x === 0) {
        return 'Likely';
      }
      return 'Highly Likely';
    },
  },
  mounted() {
    this.filteredLive();
  },
  watch: {
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
          /* eslint-disable camelcase */
          const {
            average_mmr, dire_likelihood, radiant_likelihood, server_id, time_remaining, ...clean_game
          } = this.game; // Removes redundant keys
          /* eslint-enable camelcase */
          clean_game.radiant_vote = value;
          this.votedLiveStore.setItem(String(clean_game.match_id), clean_game)
            .catch((err) => {
              console.log(err);
            });
        }
      },
    },
  },
};
</script>
<style lang="scss">
@import "@/assets/styles/gamecard.scss";
</style>
