<template>
<div>
    <b-row v-if="(game.radiant_outcome === true || game.radiant_outcome === false )&& game.radiant_vote !== null" class="mx-auto justify-content-center">
      <div v-if="game.radiant_outcome === true" class="big-radiant-title">RADIANT WON</div>
      <div v-if="game.radiant_outcome === false" class="big-dire-title">DIRE WON</div>
    </b-row>
    <b-row id="radiant-row" class="mx-auto justify-content-center">
      <div class="radiant-wrapper" v-for="(hero, idx) in game.radiant_team.heroes" :key="idx">
          <b-img-lazy
          width="120px"
          height="68px"
          :src="hero[1]"
          :alt="hero[0]"
          blank-color="#2f2f2f"
          >
          </b-img-lazy>
      </div>
    </b-row>
    <b-row class="mx-auto role-text">
      <span class="pl-4 pr-4">Safe lane</span>
      <span class="pl-5 pr-4">Mid Lane</span>
      <span class="pl-5 pr-2">Off Lane</span>
      <span class="pl-5 pr-2">Soft Support</span>
      <span class="pl-4">Hard Support</span>
    </b-row>
    <b-row id="dire-row" class="mx-auto justify-content-center">
        <div class="dire-wrapper" v-for="(hero, idx) in game.dire_team.heroes" :key="idx">
          <b-img-lazy
          width="120px"
          height="68px"
          :src="hero[1]"
          :alt="hero[0]"
          blank-color="#2f2f2f"
          >
          </b-img-lazy>
        </div>
    </b-row>
    <b-row v-if="(game.radiant_outcome === true || game.radiant_outcome === false) && game.radiant_vote !== null" class="justify-content-center">
      <div class="details-btn">
        <button v-on:click="statsSite(game.match_id)">VIEW MATCH DETAILS</button>
      </div>
    </b-row>
    <b-row v-if="(game.radiant_outcome === true || game.radiant_outcome === false) && game.radiant_vote !== null" class="justify-content-center">
      <span id="vote-title">YOU VOTED <span class="radiant-color" v-if="game.radiant_vote === true">RADIANT</span><span class="dire-color" v-else-if="game.radiant_vote === false">DIRE</span></span>
    </b-row>
</div>
</template>

<script>
export default {
  name: 'GameCard',
  props: ['game'],
  methods: {
    statsSite(id) {
      this.settingsStore.getItem('webService')
        .then((SITEIDX) => {
          switch (SITEIDX) {
            case 1:
              window.open(`https://stratz.com/matches/${id}`, '_blank');
              break;
            case 2:
              window.open(`https://www.opendota.com/matches/${id}`, '_blank');
              break;
            default:
              window.open(`https://www.dotabuff.com/matches/${id}`, '_blank');
              break;
          }
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/styles/_classes.scss";

.rad-voted{
    #radiant-row{
        background: transparent!important;
        filter: drop-shadow(2px -6px 6px rgba(19, 37, 9, 1))drop-shadow(2px -6px 6px rgba(19, 37, 9, 1)) !important;
    }
    #dire-row{
        filter: grayscale(100%) brightness(35%) sepia(100%) hue-rotate(-50deg) saturate(400%) contrast(1)!important;
    }
}
.dire-voted{
    #radiant-row{
        filter: grayscale(100%) brightness(35%) sepia(100%) hue-rotate(50deg) saturate(400%) contrast(1)!important;
    }
    #dire-row{
        background: transparent!important;
        filter: drop-shadow(2px 6px 6px #220908)drop-shadow(2px 6px 6px #220908)!important;
    }
}
.noteam-voted{
    #radiant-row{
        filter: grayscale(100%) brightness(35%) sepia(100%) hue-rotate(50deg) saturate(400%) contrast(1)!important;
    }
    #dire-row{
        filter: grayscale(100%) brightness(35%) sepia(100%) hue-rotate(-50deg) saturate(400%) contrast(1)!important;
    }
}
.dire-won{
  #dire-row{
    background: transparent!important;
    filter: drop-shadow(0px 0px 10px $dire-shadow) drop-shadow(0px 0px 10px $dire-shadow) drop-shadow(0px 0px 10px $dire-shadow)!important;
  }
  #radiant-row{
    display:none;
  }
  .role-text{
    display:none;
  }
}
.rad-won{
  #dire-row{
    display:none;
  }
  .role-text{
    display:none;
  }
  #radiant-row{
    background: transparent !important;
    filter: drop-shadow(0px 0px 10px $rad-shadow) drop-shadow(0px 0px 10px $rad-shadow) drop-shadow(0px 0px 10px $rad-shadow)!important;
  }
}
#radiant-row{
  background: linear-gradient(to top, #132509 0,rgba(19, 37, 9, 0.8)10px, rgba(19, 37, 9, 0.05) 100%);
  filter: drop-shadow(0 -6px 10px rgba(19, 37, 9, 0.8));
}
#dire-row{
  background: linear-gradient(to bottom, #220908 0,rgba(34, 9, 8, 0.8)10px, rgba(34, 9, 8, 0.05) 100%);
  filter: drop-shadow(0 6px 10px rgba(34, 9, 8, 0.8))  ;
}
.dire-wrapper, .radiant-wrapper{
  max-width: 120px;
  max-height: 68px;
}
.dire-wrapper{
  clip-path: polygon(5% 0, 100% 0, 95% 100%, 0% 100%);
}
.radiant-wrapper{
  clip-path: polygon(0 0, 95% 0, 100% 100%, 5% 100%);
}
.big-radiant-title{
  @extend %big-team-title;
  text-shadow: 0px 0px 10px $radiant-color, 0px 0px 10px $radiant-color, 0px 0px 10px $radiant-color, 0px 0px 10px $radiant-color;
}
.big-dire-title{
  @extend %big-team-title;
  text-shadow: 0px 0px 10px $dire-shadow,0px 0px 10px $dire-shadow,0px 0px 10px $dire-color,0px 0px 10px $dire-color;
}
.role-text{
  font-weight: 300;
  text-shadow: 0px 0px 25px white, 0px 0px 25px white, 0px 0px 25px gray;
}
.details-btn{
  position: relative;
  z-index: 1;
  bottom: 20px;
  button{
    padding-right: 10px;
    padding-left: 10px;
    letter-spacing: 1.5px;
    font-size: 1.4em;
    background-color: black;
    color: $grayed-out;
    border: 2px solid #292929;
    border-radius: 5px;
    outline: none;
    &:hover{
      color: $primary-color;
    }
  }
}
@media only screen and (max-width: $app-width + 33px) {
  #radiant-row, #dire-row{
    max-width: max-content;
  }
}
</style>
