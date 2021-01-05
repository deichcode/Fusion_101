<template>
  <TheRootHeader :title="tutorial.title"/>
  <main>
    <div id="tutorial-description">{{ tutorial.description }}</div>
    <BaseChapter v-for="chapter in tutorial.chapters" :key="chapter.id"
                 :id="chapter.id"
                 :title="chapter.title"
                 :description="chapter.description"
                 :thumbnail-src="getThumbnailPath(chapter.thumbnail)"
                 :openChapter="navigateToChapter"
    />
  </main>
</template>

<script>
import TheRootHeader from "../components/TheRootHeader.vue";
import getTutorial from "@/tools/getTutorial";
import BaseChapter from "@/components/BaseChapterOverview";
import router from "@/router";

export default {
  name: "TutorialContents",
  components: {
    BaseChapter,
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
      return require(`@/assets/tutorials/${this.tutorial.id}/${thumbnailFileName}`) //https://github.com/vuejs/vue-loader/issues/896
    },
    navigateToChapter(chapterId) {
      router.push({name: 'chapter', params: {tutorialId: this.tutorial.id, chapterId }})
    }
  }
}
</script>

<style scoped>
main {
  padding: 10px;
}

#tutorial-description {
  margin-bottom: 20px;
}
</style>