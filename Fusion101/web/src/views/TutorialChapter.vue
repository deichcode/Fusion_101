<template>
  <TheSubpageHeader
      :title="chapter.title"
      back-button-title="< Tutorial Overview"
      :back-button-action="navigateToOverview"
  />
  <main>
    <p class="description">{{ chapter.description }}</p>
    <ChapterStepHintVideo :hint="hintToShow"/>
    <ChapterSteps :chapter="chapter" :set-hint-to-show="setHintToShow"/>
    <ChapterNavigation :tutorial-id="tutorialId" :chapter-id="chapterId" :navigate-to-overview="navigateToOverview" />
  </main>
  <footer>
  </footer>
</template>

<script>
import router from "@/router";
import getTutorialChapter from "@/tools/tutorials/getTutorialChapter";
import TheSubpageHeader from "@/components/TheSubpageHeader";
import ChapterStepHintVideo from "@/components/ChapterStepHintVideo";
import ChapterSteps from "@/components/Steps";
import ChapterNavigation from "@/views/ChapterNavigation";

export default {
  name: "TutorialChapter",
  components: {ChapterNavigation, ChapterSteps, ChapterStepHintVideo, TheSubpageHeader},
  data() {
    return {
      tutorialId: this.$route.params.tutorialId,
      chapterId: this.$route.params.chapterId,
      chapter: {},
      hintToShow: ""
    }
  },
  mounted() {
    this.loadTutorialData();
  },
  watch: {
    $route() {
      this.tutorialId = this.$route.params.tutorialId
      this.chapterId = this.$route.params.chapterId
      this.loadTutorialData();
    }
  },
  methods: {
    loadTutorialData: function () {
      this.loadChapter()
    },
    loadChapter() {
      this.chapter = getTutorialChapter(this.tutorialId, this.chapterId)
    },
    navigateToOverview() {
      router.push({name: 'contents', params: {tutorialId: this.tutorialId}})
    },
    setHintToShow(hint) {
      this.hintToShow = hint
    },
  }
}
</script>

<style lang="scss" scoped>
.description {
  margin-top: 0;
}

</style>