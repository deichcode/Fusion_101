<template>
  <div class="chapter" role="button" tabindex="0"
       :class="{'with-image': thumbnailSrc}"
       v-on:click="openChapter(id)"
       v-on:keyup.enter="openChapter(id)"
       v-on:keydown.space.prevent
       v-on:keyup.space="openChapter(id)">
    <h2>{{ number }}&emsp;{{ title }}</h2>
    <img v-if="thumbnailSrc" :src="thumbnailSrc" :alt="thumbnailAlt">
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  name: "BaseChapterOverview",
  props: {
    id: String,
    number: String,
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
@import "src/css/mixins/clickable";

.chapter {
  @include clickable;

  padding: 15px;
  margin-bottom: 32px;

  border: 1px solid $active;
  border-radius: 4px;

  &.with-image {
    display: grid;
    grid-template-columns: 33% auto;
    grid-template-rows: auto auto;

    p {
      margin-left: 20px;
    }
  }

  h2 {
    grid-column-start: 1;
    grid-column-end: 3;

    margin-top: 0;
    margin-bottom: 10px;
  }

  img {
    width: 100%;
    max-width: 230px;
    grid-row-start: 2;
  }

  p {
    margin-top: 0;
    grid-row-start: 2;
    font-size: .8rem
  }
}
</style>