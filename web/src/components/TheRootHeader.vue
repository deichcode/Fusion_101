<template>
  <div id="header">
    <Title :text="title"/>
  </div>
</template>

<script>
import Title from "./TheHeaderTitle.vue";

export default {
  name: "TheRootHeader",
  components: {
    Title,
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