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
      <ChapterNavigation :tutorial-id="tutorialId" :chapter-id="chapterId" :navigate-to-overview="navigateToOverview"/>
    </main>
    <footer>
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
.description {
  margin-top: 0;
}

</style>

ffmpeg -i click-create-sketch.mov -vcodec h264 -acodec mp2 click-create-sketch.mp4
ffmpeg -i click-create-sketch.mp4 -c:v libvpx-vp9 -lossless 1 click-create-sketch.webm
for f in *.*;do ffmpeg -i "$f" -vcodec h264 -acodec mp2 "${f%mov}mp4";done
for f in *.mp4;do ffmpeg -i "$f" -c:v libvpx-vp9 -lossless 1 "${f%mp4}webm";done