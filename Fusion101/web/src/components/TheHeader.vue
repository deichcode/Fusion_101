<template>
  <div id="header">
    <Title :text="title"/>
    <CloseButton/>
  </div>
</template>

<script>
import Title from "./TheHeaderTitle.vue";
import CloseButton from "./ThePaletteCloseButton.vue";

export default {
  name: "Header",
  components: {
    Title,
    CloseButton
  },
  props: {
    title: String
  }
}
</script>
2
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