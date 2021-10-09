<template>
  <div id="navigation-mobile" class="no-select">
    <div class="sticky">
      <div v-on:click="expandedMenu = !expandedMenu" class="float-left">
        <svg v-if="expandedMenu === false" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M24 6h-24v-4h24v4zm0 4h-24v4h24v-4zm0 8h-24v4h24v-4z"/>
        </svg>
        <svg v-if="expandedMenu === true" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M24 20.188l-8.315-8.209 8.2-8.282-3.697-3.697-8.212 8.318-8.31-8.203-3.666 3.666 8.321 8.24-8.206 8.313 3.666 3.666 8.237-8.318 8.285 8.203z"/>
        </svg>
      </div>
    </div>
    <transition name="fade">
      <div v-if="expandedMenu === true" class="fullscreen-menu">
        <div class="container">
            <router-link v-on:click.native="expandedMenu = false" tag="b-row" :to="{ name: 'Home' }">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21 13v10h-6v-6h-6v6h-6v-10h-3l12-12 12 12h-3zm-1-5.907v-5.093h-3v2.093l3 3z"/></svg>
                <span >Home</span>
            </router-link>
            <router-link v-on:click.native="expandedMenu = false" tag="b-row" :to="{ name: 'Live' }">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M6.043 19.496l-1.482 1.505c-2.791-2.201-4.561-5.413-4.561-9.001s1.77-6.8 4.561-9l1.482 1.504c-2.326 1.835-3.804 4.512-3.804 7.496s1.478 5.661 3.804 7.496zm.675-7.496c0-1.791.887-3.397 2.282-4.498l-1.481-1.502c-1.86 1.467-3.04 3.608-3.04 6s1.18 4.533 3.04 6l1.481-1.502c-1.396-1.101-2.282-2.707-2.282-4.498zm15.043 0c0-2.984-1.478-5.661-3.804-7.496l1.482-1.504c2.791 2.2 4.561 5.412 4.561 9s-1.77 6.8-4.561 9.001l-1.482-1.505c2.326-1.835 3.804-4.512 3.804-7.496zm-6.761 4.498l1.481 1.502c1.86-1.467 3.04-3.608 3.04-6s-1.18-4.533-3.04-6l-1.481 1.502c1.396 1.101 2.282 2.707 2.282 4.498s-.886 3.397-2.282 4.498zm-3-7.498c-1.656 0-3 1.343-3 3s1.344 3 3 3 3-1.343 3-3-1.344-3-3-3z"/>
                    </svg>
                    <span >Live </span>
            </router-link>
            <router-link v-on:click.native="expandedMenu = false" tag="b-row" :to="{ name: 'RandPro' }">
                <svg  xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M18 9v-3c-1 0-3.308-.188-4.506 2.216l-4.218 8.461c-1.015 2.036-3.094 3.323-5.37 3.323h-3.906v-2h3.906c1.517 0 2.903-.858 3.58-2.216l4.218-8.461c1.356-2.721 3.674-3.323 6.296-3.323v-3l6 4-6 4zm-9.463 1.324l1.117-2.242c-1.235-2.479-2.899-4.082-5.748-4.082h-3.906v2h3.906c2.872 0 3.644 2.343 4.631 4.324zm15.463 8.676l-6-4v3c-3.78 0-4.019-1.238-5.556-4.322l-1.118 2.241c1.021 2.049 2.1 4.081 6.674 4.081v3l6-4z"/>
                </svg>
                <span >random</span>
            </router-link>
            <router-link v-on:click.native="expandedMenu = false" tag="b-row" :to="{ name: 'League' }">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M15.655 16.639c-.757.739-.736 1.936.04 2.604-.92 1.8-2.16 3.41-3.643 4.757-5.812.038-10.804-4.137-11.852-9.806 1.059-1.779 2.441-3.344 4.064-4.614.729.493 1.732.353 2.334-.328 3.835 1.292 7.046 3.947 9.057 7.387zm-15.108-8.233c-.396 1.265-.58 2.586-.542 3.941 1.001-1.398 2.195-2.646 3.575-3.722l-.02-.083c-1.033-.141-2.019-.181-3.013-.136zm23.012.365c-1.469-.964-3.099-1.702-4.841-2.162-.14.257-.354.467-.618.611.784 3.021.761 6.233-.072 9.248.859.659.901 1.94.078 2.701.305.881.539 1.788.702 2.713 4.323-2.984 6.095-8.288 4.751-13.111zm-8.333-2.696c-2.851-.128-5.655.471-8.186 1.745.019.135.019.242.013.348 4.208 1.432 7.593 4.373 9.662 7.955l.199-.015c.78-2.834.791-5.845.028-8.689-.802-.11-1.469-.662-1.716-1.344zm1.671-2.122c.917.044 1.708.679 1.936 1.476 1.426.358 2.796.892 4.086 1.59-1.559-3.412-4.668-5.965-8.428-6.76.962 1.138 1.767 2.378 2.406 3.694zm-15.91 3.274c.901-.016 1.787.032 2.713.156.523-1.073 1.92-1.375 2.788-.602 2.766-1.396 5.784-2 8.752-1.872.107-.254.282-.47.506-.632-.794-1.58-1.833-3.016-3.067-4.259-5.189-.289-9.752 2.738-11.692 7.209zm15.812 12.438c-.76 1.514-1.742 2.925-2.929 4.19 1.38-.216 2.682-.667 3.863-1.311-.148-.994-.384-1.96-.7-2.889l-.234.01z"/>
                    </svg>
                    <span >league</span>
            </router-link>
            <div class="row">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M5.495 2h16.505v-2h-17c-1.657 0-3 1.343-3 3v18c0 1.657 1.343 3 3 3h17v-20h-16.505c-1.375 0-1.375-2 0-2zm6.681 17c-.573 0-1.04-.467-1.04-1.042 0-.576.467-1.042 1.04-1.042.576 0 1.042.466 1.042 1.042 0 .575-.466 1.042-1.042 1.042zm.034-10c1.644 0 2.81 1.015 2.79 2.666-.015 1.134-.705 1.878-1.259 2.477-.832.896-.766 1.336-.766 1.941h-1.644c0-1.311-.045-1.84 1.174-2.999.469-.446.839-.799.788-1.493-.048-.66-.599-1.004-1.118-1.004-.883 0-1.26.785-1.26 1.746h-1.647c0-2.212 1.262-3.334 2.942-3.334z"/>
              </svg>
              <span >help</span>
            </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'NavigationMobile',
  data() {
    return {
      expandedMenu: false,
    };
  },
};
</script>

<style scoped lang="scss">

.sticky{
    z-index: 4;
    position: fixed;
    top: 10px;
    bottom: 0;
    left: 10px;
    padding: 0 2px 0 2px;
    width: calc((100vw - 10px) / 45);
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    height: calc(100vh - 20px);
    line-height: calc(100vh - 20px);
    background: rgba($nav-bg, 0.9);
    svg{
        fill: $gold;
        width: calc((100vw - 10px) / 55);
        height: calc((100vw - 10px) / 55);
    }
}
.fullscreen-menu{
    color: $gold;
    z-index: 4;
    background: rgba($nav-bg, 0.9);
    position: fixed;
    top: 10px;
    right: 10px;
    left: calc(((100vw - 10px) / 45) + 10px);
    max-height: calc(100vh - 20px);
    bottom: 10px;
    display: grid;
    svg{
        fill: $gold;
        display: inline-block;
        vertical-align: middle;
    }
    span{
        display: inline-block;
        padding-left: 15px;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        font-size: 16px;
        font-weight: 600;
    }
    .row{
        padding: 10px 0 10px 0;
        filter: grayscale(50%) opacity(0.75);
    }
    .container{
        margin: auto;
        width: fit-content;
    }
    .router-link-exact-active, .router-link-active:nth-child(n+2){ // ignores home router-link-active
      text-shadow: 0 0 3px rgba($gold, 0.75);
      filter: grayscale(0%) opacity(1);
      svg{
          filter: drop-shadow(0 0 2px rgba($gold, 0.75));
      }
    }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease-out;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
@supports (-webkit-backdrop-filter: none) or (backdrop-filter: none) {
    .fullscreen-menu{
        -webkit-backdrop-filter: blur(5px);
        backdrop-filter: blur(5px);
    }
}
</style>
