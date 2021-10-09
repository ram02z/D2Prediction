<template>
    <b-col lg="" id="settings" class="mx-lg-0 mx-1 mb-lg-2 mb-4 no-select">
        <div class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 13.616v-3.232l-2.869-1.02c-.198-.687-.472-1.342-.811-1.955l1.308-2.751-2.285-2.285-2.751 1.307c-.613-.339-1.269-.613-1.955-.811l-1.021-2.869h-3.232l-1.021 2.869c-.686.198-1.342.471-1.955.811l-2.751-1.308-2.285 2.285 1.308 2.752c-.339.613-.614 1.268-.811 1.955l-2.869 1.02v3.232l2.869 1.02c.197.687.472 1.342.811 1.955l-1.308 2.751 2.285 2.286 2.751-1.308c.613.339 1.269.613 1.955.811l1.021 2.869h3.232l1.021-2.869c.687-.198 1.342-.472 1.955-.811l2.751 1.308 2.285-2.286-1.308-2.751c.339-.613.613-1.268.811-1.955l2.869-1.02zm-12 2.384c-2.209 0-4-1.791-4-4s1.791-4 4-4 4 1.791 4 4-1.791 4-4 4z"/></svg>
            <span>preferences</span>
        </div>
        <div class="section-body">
            <b-list-group>
                <b-list-group-item v-for="(setting, sIDX) in settings" :key="sIDX">
                    <div v-show="!setting.focus">
                      <span class="float-left">{{ setting.title }}</span>
                      <span role="button" class="float-right" v-on:click="setting.focus = true">&plus;</span>
                    </div>
                    <div v-show="setting.focus">
                        <span
                        class="mr-1 float-left"
                        role="button"
                        v-on:click="handleSetting(setting.key, sIDX, oIDX)"
                        v-for="(option, oIDX) in setting.options"
                        :key="oIDX"
                        :class="setting.chosen_index === oIDX && 'underline'">
                        {{ option }}
                        </span>
                        <span role="button" class="float-right" v-on:click="setting.focus = false">&minus;</span>
                    </div>
                </b-list-group-item>
            </b-list-group>
        </div>
    </b-col>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      settings: [{
        key: 'webService',
        title: 'Web service used to view match details',
        options: ['Dotabuff', 'Stratz', 'Opendota'],
        chosen_index: 0,
        focus: false,
      },
      {
        key: 'toastHide',
        title: 'Auto hide push notifications',
        options: ['Off', 'On'],
        chosen_index: 0,
        focus: false,
      }],
    };
  },
  methods: {
    handleSetting(key, sIDX, oIDX) {
      this.settingsStore.setItem(key, oIDX)
        .then(() => {
          this.settings[sIDX].chosen_index = oIDX;
        }).catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    for (let i = 0; i < this.settings.length; i += 1) {
      this.settingsStore.getItem(this.settings[i].key)
        .then((val) => {
          if (val !== null) {
            this.settings[i].chosen_index = val;
          }
        });
    }
  },
};
</script>
<style lang="scss" scoped>
.underline{
  text-decoration: underline;
}

</style>
