<template>
  <div class="chapter" role="button" tabindex="0"
       v-on:click="openChapter(id)"
       v-on:keyup.enter="openChapter(id)"
       v-on:keydown.space.prevent
       v-on:keyup.space="openChapter(id)">
    <h2>{{ title }}</h2>
    <img :src="thumbnailSrc" :alt="thumbnailAlt">
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: "BaseChapter",
  props: {
    id: String,
    title: String,
    thumbnailSrc: String,
    thumbnailAlt: String,
    description: String,
    openChapter: Function
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";

.chapter {
  display: grid;
  grid-template-columns: 33% auto;
  grid-template-rows: auto auto;

  //background-color: $menu-background;
  padding: .8rem;
  margin-bottom: 2rem;

  border: 1px solid $active;
  border-radius: .4rem;
  cursor: pointer;

  &:hover {
    background-color: $highlight;
  }

  &:active {
    background-color: $active;
    color: white;
  }
}

h2 {
  grid-column-start: 1;
  grid-column-end: 3;

  margin-top: 0;
  margin-bottom: .6rem;
}

img {
  width: 100%;
  max-width: 230px;
  grid-row-start: 2;
}

p {
  margin-top: 0;
  margin-left: .8rem;
  grid-row-start: 2;
}
</style>