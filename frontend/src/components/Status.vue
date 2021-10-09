<template>
    <b-col lg="" id="status" class="mx-lg-0 mx-1 mb-lg-2 mb-4 no-select">
        <div class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 7.244c3.071-3.24 7.314-5.244 12-5.244 4.687 0 8.929 2.004 12 5.244l-2.039 2.15c-2.549-2.688-6.071-4.352-9.961-4.352s-7.412 1.664-9.961 4.352l-2.039-2.15zm5.72 6.034c1.607-1.696 3.827-2.744 6.28-2.744s4.673 1.048 6.28 2.744l2.093-2.208c-2.143-2.261-5.103-3.659-8.373-3.659s-6.23 1.398-8.373 3.659l2.093 2.208zm3.658 3.859c.671-.708 1.598-1.145 2.622-1.145 1.023 0 1.951.437 2.622 1.145l2.057-2.17c-1.197-1.263-2.851-2.044-4.678-2.044s-3.481.782-4.678 2.044l2.055 2.17zm2.622 1.017c-1.062 0-1.923.861-1.923 1.923s.861 1.923 1.923 1.923 1.923-.861 1.923-1.923-.861-1.923-1.923-1.923z"/></svg>
            <span>status</span>
        </div>
        <div class="section-body">
            <b-row class="justify-content-around ml-lg-0">
                <b-col
                v-for="(service, IDX) in content.services"
                :key="IDX"
                :id="'service_' + IDX"
                :class="serviceObj(service.response)">
                    <b-img-lazy
                    :id="'service_img_' + IDX" width="48" height="48"
                    :alt="service.name"
                    :src="require('@/' + service.img_path)"
                    blank-color='#2f2f2f'
                    >
                    </b-img-lazy>
                    <b-tooltip delay="0" variant="dark" :target="'service_img_' + IDX" triggers="hover">
                        <strong>{{service.name}}</strong>
                        <br>
                        <small>{{service.use}}</small>
                    </b-tooltip>
                    <br>
                    <div v-if="service.response.time">
                      <span v-if="service.response.error === false" class="mt-2">
                        Responded in {{ service.response.time }}ms
                      </span>
                      <span v-else>Response error</span>
                    </div>
                </b-col>
            </b-row>
            <b-row class="justify-content-center ml-lg-0 mt-2 mb-1">
              <button v-if="checking === false" @click="checking = true" class="check-btn">CHECK</button>
              <span class="small text-muted" v-if="showingCached === true && (checking === null || checking === true)">You can check status of the services again at {{ tillCheck }}</span>
            </b-row>
        </div>
    </b-col>
</template>

<script>
export default {
  name: 'Status',
  data() {
    return {
      checking: null,
      showingCached: false,
      content: {
        timestamp: Date.now(),
        services: [{
          name: 'Dota 2 Live API',
          img_path: 'assets/icons/dota2.png',
          use: 'To get top live MMR games',
          endpoint: '/filteredLive',
          response: {
            error: null,
            time: NaN,
          },
        },
        {
          name: 'Stratz API',
          img_path: 'assets/icons/stratz.png',
          use: 'For parsing individual games',
          endpoint: 'match/5464296449', // random match
          response: {
            error: null,
            time: NaN,
          },
        },
        {
          name: 'Opendota API',
          img_path: 'assets/icons/opendota.png',
          use: 'For collecting random league match ids',
          endpoint: '/randomMatches',
          response: {
            error: null,
            time: NaN,
          },
        },
        ],
      },
    };
  },
  computed: {
    tillCheck() {
      const ts = new Date(this.content.timestamp);
      ts.setMinutes(ts.getMinutes() + 5);
      return ts.toLocaleTimeString('en-GB');
    },
  },
  methods: {
    // res.time is half of most timeouts which is usually 5s
    serviceObj(res) {
      return {
        'success-res': res.error === false && res.time < 4000,
        'failed-res': res.error === true,
        'slow-res': res.error === false && res.time >= 4000,
        'active-ani': Number.isNaN(res.time) && res.error === null && this.checking === true,
      };
    },
    getResDur(path) {
      return this.$api.get(path)
        .then((res) => [res.headers.requestDuration, res.data.error])
        .catch((err) => err.headers.requestDuration);
    },
  },
  watch: {
    checking: {
      handler(val) {
        if (val === true) {
          for (let i = 0; i < this.content.services.length; i += 1) {
            this.getResDur(this.content.services[i].endpoint)
              .then(([dur, err]) => {
                if (err) {
                  this.content.services[i].response.error = true;
                } else {
                  this.content.services[i].response.error = false;
                }
                this.content.services[i].response.time = dur;
              })
              .catch(() => {
                this.content.services[i].response.error = true;
                this.content.services[i].response.time = -1;
              })
              .finally(() => {
                this.cachedStore.setItem('statusContent', this.content).catch((err) => { console.log(err); });
                this.showingCached = true;
              });
          }
        }
      },
    },
  },
  created() {
    this.cachedStore.getItem('statusContent').then((cachedContent) => {
      if (cachedContent) {
        const diffInStamps = Math.floor((this.content.timestamp - cachedContent.timestamp) / 1000);
        if (diffInStamps >= 300) {
          this.checking = false;
          this.cachedStore.removeItem('statusContent').catch((err) => { console.log(err); });
        } else {
          this.content = cachedContent;
          this.showingCached = true;
        }
      } else {
        this.checking = false;
      }
    }).catch((err) => {
      console.log(err);
    });
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/styles/_classes.scss";

.check-btn{
  @extend %button;
  background-color: rgba($color: $bg-color, $alpha: 0.8);
  width: 4.5em;
  height: 50%;
  border-radius: 5px;
  border-bottom: .125em inset $bg-color;
  color: $gold-text;
  &:hover{
    background-color: $bg-color;
  }
  &:focus{
    outline: none;
  }
}
.success-res{
    img{
        border: .125em solid $muted-green !important;
    }
    span{
        color: $muted-green ;
    }
}
.failed-res{
    img{
        border: .125em solid $muted_red !important;
    }
    span{
        color: $muted_red;
    }
}
.slow-res{
    img{
        border: .125em solid $muted_amber !important;
    }
    span{
        color: $muted_amber;
    }
}
img{
  padding: .25em;
  border-radius: 5px;
  border: .125em solid $bg-color;
}
.active-ani img{
  background-image:
  linear-gradient(90deg, #604E2D 50%, transparent 50%),
  linear-gradient(90deg, #604E2D 50%, transparent 50%),
  linear-gradient(0deg, #604E2D 50%, transparent 50%),
  linear-gradient(0deg, #604E2D 50%, transparent 50%);
  background-repeat: repeat-x, repeat-x, repeat-y, repeat-y;
  background-size: 15px 2px, 15px 2px, 2px 15px, 2px 15px;
  background-position: left top, right bottom, left bottom, right top;
  -webkit-animation: border-infinite 1s infinite linear;
  -moz-animation: border-infinite 1s infinite linear;
  -o-animation: border-infinite 1s infinite linear;
  animation: border-infinite 1s infinite linear;
  &:hover{
    -webkit-animation-play-state: paused;
    -moz-animation-play-state: paused;
    -o-animation-play-state: paused;
     animation-play-state: paused;
  }
}
@keyframes border-infinite {
  0% {
    background-position: left top, right bottom, left bottom, right top;
  }
  100% {
    background-position: left 15px top, right 15px bottom , left bottom 15px , right top 15px;
  }
}
</style>
