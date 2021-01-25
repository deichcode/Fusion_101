<template>
  <div class="chapter-navigation">
    <BaseButton v-if="nextChapter" text="Next Chapter >" v-on:click="navigateToNextChapter"/>
    <BaseButton v-if="!nextChapter" text="Finish Tutorial" v-on:click="navigateToOverview"/>
    <BaseButton v-if="previousChapter" text="< Previous Chapter" v-on:click="navigateToPreviousChapter"/>
  </div>
</template>
<script>
import BaseButton from "@/components/BaseButton"
import router from "@/router";
import getNextChapter from "@/tools/tutorials/getNextChapter";
import getPreviousChapter from "@/tools/tutorials/getPreviousChapter";

export default {
  name: 'ChapterNavigation',
  components: {BaseButton},
  props: {
    tutorialId: String,
    chapterId: String,
    navigateToOverview: Function
  },
  data() {
    return {
      previousChapter: undefined,
      nextChapter: undefined,
    }
  },
  mounted() {
    this.loadTutorialData();
  },
  watch: {
    chapterId() {
      console.log("props changed")
      this.loadTutorialData();
    }
  },
  methods: {
    loadTutorialData() {
      this.loadNextChapter()
      this.loadPreviousChapter()
    },
    loadNextChapter() {
      this.nextChapter = getNextChapter(this.tutorialId, this.chapterId)
    },
    loadPreviousChapter() {
      this.previousChapter = getPreviousChapter(this.tutorialId, this.chapterId)
    },
    navigateToNextChapter() {
      router.push({name: 'chapter', params: {tutorialId: this.tutorialId, chapterId: this.nextChapter.id}})
    },
    navigateToPreviousChapter() {
      router.push({name: 'chapter', params: {tutorialId: this.tutorialId, chapterId: this.previousChapter.id}})
    },
  }
}
</script>
<style lang="scss" scoped>

.chapter-navigation {
  pointer-events: auto;
  display: flex;
  flex-direction: row-reverse;
  justify-content: space-between;
}
</style>