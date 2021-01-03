<template>
  <Button v-on:click="closeApp" text="X"></Button>
</template>

<script>
import Button from './BaseButton'
export default {
  name: "CloseButton",
  components: {
    Button
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
</style>