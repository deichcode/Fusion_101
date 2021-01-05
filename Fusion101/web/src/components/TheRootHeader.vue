<template>
  <div id="header">
    <Title :text="title"/>
    <ThePaletteCloseButton/>
  </div>
</template>

<script>
import Title from "./TheHeaderTitle.vue";
import ThePaletteCloseButton from "./ThePaletteCloseButton.vue";

export default {
  name: "TheRootHeader",
  components: {
    Title,
    ThePaletteCloseButton
  },
  props: {
    title: String
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";

#header{
  display: flex;
  align-items: flex-start;
  background-color: $menu-background;
  padding: 8px;
  position: sticky;
  top: 0;
}

</style>