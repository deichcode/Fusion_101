<template>
  <TheRootHeader :title="tutorial.title"/>
  <main>
    <div id="tutorial-description">{{ tutorial.description }}</div>
<!--Show each chapter of the tutorial-->
    <BaseChapterOverview v-for="(chapter, index) in tutorial.chapters" :key="chapter.id"
                         :id="chapter.id"
                         :number="getChapterNumber(chapter, index)"
                         :title="chapter.title"
                         :description="chapter.extendedDescription ?? chapter.description"
                         :thumbnail-src="getThumbnailPath(chapter.thumbnail)"
                         :thumbnail-alt="chapter.thumbnailAlt"
                         :openChapter="navigateToChapter"
    />
  </main>
</template>

<script>
import TheRootHeader from "../components/TheRootHeader.vue";
import getTutorial from "@/tools/tutorials/getTutorial";
import BaseChapterOverview from "@/components/BaseChapterOverview";
import router from "@/router";
import getTutorialMedia from "@/tools/tutorials/getTutorialMedia";

export default {
  name: "TutorialContents",
  components: {
    BaseChapterOverview,
    TheRootHeader
  },
  data() {
    return {
      tutorial: {}
    }
  },
  mounted() {
    this.loadTutorial()
  },
  methods: {
    loadTutorial() {
      this.tutorial = getTutorial(this.$route.params.tutorialId)
    },
    getThumbnailPath(thumbnailFileName) {
      //try/catch prevents crash on missing media file
      try {
        return getTutorialMedia(this.tutorial.id, thumbnailFileName)
      } catch (e) {
        return ""
      }
    },
    navigateToChapter(chapterId) {
      router.push({name: 'chapter', params: {tutorialId: this.tutorial.id, chapterId}})
    },
    getChapterNumber(chapter, index) {
      //If chapter 'number' is given by file use it otherwise calculate by chapter's index
      const chapterNumber = chapter.number ? chapter.number : this.calculatedChapterNumber(index)
      return chapterNumber.toString()
    },
    calculatedChapterNumber(index){
      return this.tutorial.startChapterNumbersWith + index
    }
  }
}
</script>

<style scoped>
#tutorial-description {
  margin-bottom: 20px;
}
</style>