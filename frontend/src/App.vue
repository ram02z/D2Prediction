<template>
  <div v-if="webStorage">
    <div id="app">
      <router-view class="pb-0 pb-lg-5" id="router-view" :key="componentKey"/>
      <Navigation v-if="!mobileView"/>
      <NavigationMobile v-if="mobileView"/>
      <Toasts/>
    </div>
    <div class="rotate-prompt">
      <div class="device"></div>
      <div class="message mt-2">Please rotate your device to landscape mode.</div>
      <div class="warning mt-2">Your device is too small to use this web-app!</div>
    </div>
  </div>
  <div v-else class="d-flex min-vh-100 justify-content-center align-items-center">
    Web storage not available on this browser.
  </div>
</template>

<script>
import Navigation from './components/Navigation.vue';
import NavigationMobile from './components/NavigationMobile.vue';
import Toasts from './components/Toasts.vue';

export default {
  name: 'App',
  data() {
    return {
      componentKey: 0,
      mobileView: false,
      webStorage: this.storageAvi() || false,
    };
  },
  components: {
    Navigation,
    NavigationMobile,
    Toasts,
  },
  methods: {
    handleView() {
      this.mobileView = window.innerWidth <= 991;
    },
    storageAvi() {
      try {
        const x = '__storage_test__';
        window.localStorage.setItem(x, x);
        window.localStorage.removeItem(x);
        return true;
      } catch (e) {
        return e instanceof DOMException && (
          // everything except Firefox
          e.code === 22
          // Firefox
          || e.code === 1014
          // test name field too, because code might not be present
          // everything except Firefox
          || e.name === 'QuotaExceededError'
          // Firefox
          || e.name === 'NS_ERROR_DOM_QUOTA_REACHED')
          // acknowledge QuotaExceededError only if there's something already stored
          && window.localStorage && window.localStorage.length !== 0;
      }
    },
    getPatch() {
      this.$api.get('/patchNames', {
        params: {
          last: 10,
        },
      })
        .then((res) => {
          this.cachedStore.setItem('patchContent', { timestamp: Date.now(), names: res.data.data })
            .catch((err) => { console.log(err); });
        });
    },
    handlePatch() {
      this.cachedStore.getItem('patchContent')
        .then((cached) => {
          if (cached === null) {
            this.getPatch();
          } else {
            const diffInStamps = Math.floor((Date.now() - cached.timestamp) / 1000);
            if (diffInStamps > 3600) {
              this.getPatch();
            }
          }
        });
    },
  },
  created() {
    this.handleView();
    this.handlePatch();
    window.addEventListener('resize', this.handleView);
  },
};
</script>
<style lang="scss">
@import "@/assets/styles/_classes.scss";

.hidden{
  visibility: hidden;
}
.dnone{
  display: none;
}
.gold-color{
  color: $gold !important;
}
.gold-text{
  color: $gold-text !important;
}
.no-select{
  -webkit-user-select: none;  /* Chrome all / Safari all */
  -moz-user-select: none;     /* Firefox all */
  -ms-user-select: none;      /* IE 10+ */
  user-select: none;
}
html, body{
  background: $bg-color;
  color: $primary-color;
  font-family: 'Source Sans Pro', sans-serif;
  font-weight: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // cursor: url('assets/dota_cursor.png'), auto;
}
#app{
  position: fixed;
  top: 10px;
  right: 10px;
  left: 10px;
  bottom: 10px;
  background-color: $app-color;
  border-radius: 10px;
  text-align: center;
  overflow-y:auto;
  scrollbar-width: thin;
  scrollbar-color: $bg-color $app-color;
}
/* highlight color */
::selection {
  background: $gold;
}
::-moz-selection {
  background: $gold;
}

/* scrollbar for app */
::-webkit-scrollbar-track {
  background: $app-color;
  width: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
}
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
::-webkit-scrollbar-thumb {
  background: $bg-color;
  border-radius: 6px;
  border: 3px solid $app-color;
}
/* *:hover, a:hover, button:hover{
  cursor: url('assets/dota_cursor.png'), auto;
} */
/* Error display styling*/
.error-display{
  display: flex;
  justify-content: center;
  .error-message{
    @extend %title;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
}
/* tooltip size, alignment and background color  */
.tooltip.b-tooltip-dark{
  .tooltip-inner {
    max-width: 100% !important;
    background-color: $bg-color !important;
    color: $primary-color !important;
    border: 1px solid $nav-bg!important;
  }
}
.bs-tooltip-top, .bs-tooltip-bottom{
  .arrow{
    &::before{
      border-top-color: $bg-color!important;
      border-bottom-color: $bg-color!important;
    }
  }
}
.bs-tooltip-right, .bs-tooltip-left{
  .tooltip-inner{
    text-align: left !important;
  }
  .arrow{
    &::before{
      border-left-color: $bg-color!important;
      border-right-color: $bg-color!important;
    }
  }
}
/* Toggle switch buttons */
input[type="checkbox"] {
  ~ .custom-control-label{
    &::before{
      box-shadow: none!important;
      border-color:$nav-bg!important;
      background-color: $bg-color!important;
    }
    &::after{
      background-color: $gold!important;
      filter: grayscale(80%);
    }
  }
  &:checked{
      ~ .custom-control-label{
        &::before{
            border-color:$nav-bg!important;
            background-color: $bg-color!important;
        }
        &::after{
          background-color: $gold!important;
          filter: none;
        }
    }
  }
}
/* Medal and team titles*/
.medal{
  filter: drop-shadow(0 0 1px #99532a);
}
.radiant-title, .hidden-title{
  @extend %team-title;
  text-shadow: 0px 0px 5px $radiant-color, 0px 0px 5px $radiant-color, 0px 0px 5px $radiant-color, 0px 0px 5px $radiant-color;
}
.dire-title{
  @extend %team-title;
  text-shadow: 0px 0px 5px $dire-color,0px 0px 5px $dire-color,0px 0px 5px $dire-color,0px 0px 5px $dire-color;
}
#vote-title{
  letter-spacing: 1.5px;
  font-size: 1.4em;
  color: $grayed-out;
  font-weight: 600;
  transform: scale(1, 0.9);
}
.dire-color{
  color: $dire-color;
}
.radiant-color{
  color: $radiant-color;
}
/* Toast theming */
.b-toaster.b-toaster-top-right{
  right: 10px!important;
  top: 10px!important;
}
.b-toaster.b-toaster-top-right .b-toaster-slot{
  top: 0px;
}
.b-toast{
  float: right;
  padding: 5px;
}
.toast{
  border-radius: 10px;
  z-index: 1;
  outline: none;
  a{
    text-align: center;
    opacity: 1;
    color: $primary-color;
    font-weight: 600;
    transition: 200ms ease;
    filter: grayscale(70%) opacity(0.7);
    &:hover{
      filter: grayscale(0%) opacity(1);
      text-decoration: none;
    }
    &:focus{
      filter: grayscale(0%) opacity(1);
      outline: none!important;
    }
  }
}
.toast-header{
  color: $primary-color;
  background-color: $gold;
  .close{
    color: $primary-color;
    font-weight: 700;
    text-shadow: none;
    transition: 200ms ease;
    outline: none;
    filter: grayscale(70%) opacity(0.7);
    &:hover{
      filter: grayscale(0%) opacity(1);
    }
  }
}
.b-toast .toast {
  background-color: rgba($color: $gold, $alpha: 0.75);
}
// Modaular Sections
.section-body{
  color: $gold-text;
  font-weight: 600;
  text-shadow:
    -1px -1px 0 $bg-color,
    1px -1px 0 $bg-color,
    -1px  1px 0 $bg-color,
    1px  1px 0 $bg-color;
  background-color: rgba($color: $bg-color, $alpha: 0.4) ;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
  padding: 0.5em;
  .list-group-item{
    background-color: transparent;
    border: none;
  }
}
.section-title{
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.125em 0;
  background-color: rgba($color: $bg-color, $alpha: 0.8);
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  color: $gold;
  text-transform:uppercase;
  svg{
    height: 1.1275em;
    width: 1.1275em;
    fill: $gold;
  }
  span{
    padding-left: 0.25em;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-size: 18px;
    font-weight: 600;
  }
}
@media only screen and (max-width: $app-width) {
  #app{
    display: none;
  }
  .rotate-prompt{
    z-index: 9999;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .warning{
     display: none;
   }
  .device {
    height: 100px;
    width: 50px;
    border: 3px solid $primary-color;
    border-radius: 10px;
    animation: rotate 1.5s ease-in-out infinite alternate;
  }
  @keyframes rotate {
    0%{
      transform: rotate(0deg);
    }
    50%{
      transform: rotate(-90deg);
    }
    100%{
      transform: rotate(-90deg);
    }
  }
}
@media only screen and (min-width: $app-width) {
  #app{
    display: block;
  }
  .rotate-prompt{
    display: none;
  }
  .device{
    animation: none;
  }
}
 @media screen and (orientation:landscape) and (max-width: $app-width) {
   .message{
     display:none;
   }
   .warning{
     display: block;
   }
  .device{
     animation: none;
     display: none;
   }
  }
</style>
