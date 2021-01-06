<template>
  <BaseButton v-on:click="closeApp" text="X"></BaseButton>
</template>

<script>
import BaseButton from './BaseButton'
export default {
  name: "ThePaletteCloseButton",
  components: {
    BaseButton
  },
  methods: {
    closeApp() {
      const args = {
        command: "close",
      };
      window.adsk.fusionSendData("send", JSON.stringify(args));
    }
  }
}
</script>

<style scoped>
button {
  min-width: 1.6rem;
}
</style>