<template>
  <div id="header">
    <div class="button-row">
      <BaseButton :text="backButtonTitle"
                  v-on:click="backButtonAction"></BaseButton>
      <ThePaletteCloseButton/>
    </div>
    <Title class="title" :text="title"/>
  </div>
</template>

<script>
import Title from "@/components/TheHeaderTitle";
import ThePaletteCloseButton from "@/components/ThePaletteCloseButton";
import BaseButton from "@/components/BaseButton";

export default {
  name: "TheSubpageHeader",
  components: {BaseButton, Title, ThePaletteCloseButton},
  props: {
    backButtonTitle: String,
    backButtonAction: Function,
    title: String
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";

#header {
  padding: 8px;
  position: sticky;
  top: 0;
  background-color: $menu-background;

  > .button-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }
}
</style>