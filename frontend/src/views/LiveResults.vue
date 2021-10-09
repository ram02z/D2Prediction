<template>
 <b-container fluid="lg" class="mt-4">
  <NestedNav :links="[{ name: 'Live', tag: 'Live' }, { name: 'LiveResults', tag: 'Results' }]"/>
  <b-form-checkbox size="lg" v-model="checked" @click.native="checked ? $router.push({ name: 'LiveResultsPending' }, () => {}) : $router.push({ name: 'LiveResults' }, () => {})" name="check-button" switch>
      <span v-if="!checked">Showing pending games</span>
      <span v-if="checked">Showing scored games</span>
  </b-form-checkbox>
  <div class="px-1">
    <div v-if="checked" id="scored-accordion" role="tablist">
      <b-card no-body class="mb-1" v-for="(game, idx) in scoredGames" :key="idx">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <span v-on:click="$event.target.classList.contains('collapsed') ? locHash = `#${game.match_id}` : locHash = ''" block v-b-toggle="'scoredacc-'+idx" class="accordion-heading pl-3">{{ game.match_id }}</span>
          <button type="button" class="remove mr-1" aria-label="Remove" v-on:click="removedScored(game.match_id);">
            <span aria-hidden="true">&times;</span>
          </button>
        </b-card-header>
        <b-collapse :visible="parsedHash === game.match_id" :id="'scoredacc-'+ idx" accordion="scored-accordion" role="tabpanel">
          <b-card-body class="mt-1">
            <GameCard :game="game" :class="{ 'rad-won' : game.radiant_outcome === true, 'dire-won' : game.radiant_outcome === false}"/>
          </b-card-body>
        </b-collapse>
      </b-card>
      <b-row v-if="scoredGames.length > 0 && checked === true" class="row justify-content-center mt-2">
          <abbr title="Correct predictions" class="lead no-select gold-color text-decoration-none">{{ compScore }}</abbr>
      </b-row>
    </div>
    <div v-if="!checked" id="nscored-accordion" role="tablist">
      <b-card no-body class="mb-1" v-for="(game, idx) in nscoredGames" :key="idx">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <span v-on:click="$event.target.classList.contains('collapsed') ? locHash = `#${game.match_id}` : locHash = ''" block v-b-toggle="'nscoredacc-'+ idx" class="accordion-heading">{{ game.match_id }}</span>
        </b-card-header>
        <b-collapse :visible="parsedHash === game.match_id" :id="'nscoredacc-'+ idx" accordion="nscored-accordion" role="tabpanel">
          <b-card-body class="mt-1">
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
            <GameCard :game="game" :class="{ 'rad-voted' : game.radiant_vote === true, 'dire-voted' : game.radiant_vote === false}"/>
            <b-row>
              <span class="dire-title d-flex align-items-end mr-5">THE DIRE</span>
            </b-row>
            <b-row class="justify-content-center">
              <span id="vote-title">YOU VOTED <span class="radiant-color" v-if="game.radiant_vote">RADIANT</span><span class="dire-color" v-else>DIRE</span></span>
            </b-row>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
  </div>
</b-container>
</template>

<script>
import GameCard from '@/components/GameCard.vue';
import NestedNav from '@/components/NestedNav.vue';

export default {
  name: 'LiveResults',
  components: {
    GameCard,
    NestedNav,
  },
  data() {
    return {
      checked: this.$route.meta.scored,
      scoredGames: [],
      nscoredGames: [],
      locHash: this.$route.hash,
    };
  },
  watch: {
    $route(to, from) {
      if ((to.hash !== '' && from.name !== 'LiveResults') || from.hash === '') {
        this.forceRerender();
        this.locHash = to.hash;
      }
    },
    locHash: {
      handler(val) {
        this.$router.push(`${val}`);
      },
    },
  },
  computed: {
    parsedHash() {
      return parseInt(this.locHash.substring(1), 10);
    },
    compScore() {
      let score = 0;
      for (let i = 0; i < this.scoredGames.length; i += 1) {
        if (this.scoredGames[i].radiant_outcome === this.scoredGames[i].radiant_vote) {
          score += 1;
        }
      }
      return score;
    },
  },
  methods: {
    removedScored(matchId) {
      if (window.confirm('This will remove the match. Continue?')) {
        this.scoredLiveStore.removeItem(String(matchId))
          .then(() => {
            this.forceRerender();
            this.$router.push({ name: 'LiveResults' }, () => {});
          }).catch((err) => {
            console.log(err);
          });
      }
    },
    forceRerender() {
      this.$parent.componentKey += 1;
    },
  },
  created() {
    this.votedLiveStore.iterate((value) => {
      this.nscoredGames.push(value);
    });
    this.scoredLiveStore.iterate((value) => {
      this.scoredGames.push(value);
    });
  },
};
</script>

<style scoped lang="scss">
#scored-accordion, #nscored-accordion {
  max-width: $app-width;
  margin: 0 auto;
}
.collapsing {
  transition: none !important;
}
.accordion-heading{
  opacity: 1;
  color: $gold;
  font-weight: 600;
  width: fit-content;
  font-size: 1.5em!important;
  letter-spacing: 2px;
  transition: 200ms ease;
  filter: grayscale(70%) opacity(0.7);
  &:hover{
    filter: grayscale(0%) opacity(1);
  }
  &:focus{
    filter: grayscale(0%) opacity(1);
    text-decoration: underline;
    outline: none!important;
  }
}
.card{
  background-color: transparent !important;
  border: 0;
}
.card-body{
  padding: 0;
  border-radius: 10px;
  background-color: rgba($color: $bg-color, $alpha: 0.4) !important;
}
.card-header{
  background-color: rgba($color: $bg-color, $alpha: 0.8) !important;
  border-radius: 10px;
}
.remove{
  float: right;
  font-size: 1.5rem;
  opacity: 1;
  color: $gold;
  font-weight: 700;
  transition: 200ms ease;
  filter: grayscale(70%) opacity(0.7);
  &:hover{
    filter: grayscale(0%) opacity(1);
  }
  &:focus{
    filter: grayscale(0%) opacity(1);
    outline: none!important;
  }
}
button.remove{
  padding: 0;
  border: 0;
  background-color: transparent;
}
</style>
