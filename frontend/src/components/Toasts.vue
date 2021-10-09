<template>
    <div>
    </div>
</template>

<script>
export default {
  name: 'Toasts',
  methods: {
    makeToast(matchId, append = false) {
      this.settingsStore.getItem('toastHide')
        .then((val) => {
          this.$bvToast.toast('View outcome', {
            title: `Match #${matchId}`,
            noAutoHide: !val && true,
            appendToast: append,
            to: { name: 'LiveResults', hash: `#${matchId}` },
          });
        });
    },
    checkOutcome(matchId) {
      const PATH = `/matchDetail/${matchId}`;
      return this.$api.get(PATH, {
        params: {
          winner: true,
        },
      })
        .catch((error) => {
          console.log(error);
        })
        .then((res) => {
          if (res.data.error === false) {
            return res.data.data.radiant_win;
          }
        });
    },
    filterGames() {
      this.votedLiveStore.iterate((value, key) => {
        this.checkOutcome(key)
          .then((scored) => {
            if (scored !== undefined) {
              const {
                medal, ...game
              } = value; // Removes redundant key
              game.radiant_outcome = scored;
              this.scoredLiveStore.setItem(key, game)
                .then(() => {
                  this.makeToast(key);
                }).catch((err) => {
                  console.log(err);
                });
              this.votedLiveStore.removeItem(key).catch((err) => { console.log(err); });
            }
          });
      }).catch((err) => { console.log(err); });
    },
  },
  mounted() {
    window.setInterval(() => this.filterGames(), 30000);
  },
};
</script>

<style lang="scss" scoped>

</style>
