<template>
  <div :key="tutorialId + chapterId">
    <TheSubpageHeader
        :title="chapter.title"
        back-button-title="^ Tutorial Overview"
        :back-button-action="navigateToOverview"
    />
    <main>
      <p class="description">{{ chapter.description }}</p>
      <!--      Hint Videos can have a size of 380x163@2 (double resolution)-->
      <!--      Hint Videos can have a size of 570x245@2 (double resolution)-->
      <!--      Hint Videos can have a size of 760x328@2 (double resolution)-->
      <ChapterStepHintVideo :hint="hintToShow"/>
      <ChapterSteps :chapter="chapter" :set-hint-to-show="setHintToShow"/>
    </main>
    <footer>
      <ChapterNavigation :tutorial-id="tutorialId" :chapter-id="chapterId" :navigate-to-overview="navigateToOverview"/>
    </footer>
  </div>
</template>

<script>
import router from "@/router";
import getTutorialChapter from "@/tools/tutorials/getTutorialChapter";
import TheSubpageHeader from "@/components/TheSubpageHeader";
import ChapterStepHintVideo from "@/components/ChapterStepHintVideo";
import ChapterSteps from "@/components/ChapterSteps";
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
    this.loadChapter();
  },
  watch: {
    $route() { //Watch on changes in route and load chapter data if chapter and/or tutorial have changed
      this.tutorialId = this.$route.params.tutorialId
      this.chapterId = this.$route.params.chapterId
      this.loadChapter();
    }
  },
  methods: {
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
@import "src/css/variables/colors";

$footerHeight: 30px;

.description {
  margin-top: 0;
}

main {
  margin-bottom: $footerHeight;
}

footer {
  position: fixed;
  bottom: 0;
  /* Permalink - use to edit and share this gradient: https://colorzilla.com/gradient-editor/#ffffff+0,ffffff+100&0+0,1+28 */
  background: -moz-linear-gradient(top, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 1) 100%); /* FF3.6-15 */
  background: -webkit-linear-gradient(top, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 1) 100%); /* Chrome10-25,Safari5.1-6 */
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 1) 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#00ffffff', endColorstr='#ffffff', GradientType=0); /* IE6-9 */
  padding-top: 15px;
  height: $footerHeight;
  width: 100%;
}

</style>