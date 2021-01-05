<template>
  <TheSubpageHeader :title="chapter.title"
                    back-button-title="< Tutorial Overview"
                    :back-button-action="navigateToOverview"/>
</template>

<script>
import router from "@/router";


import getTutorialChapter from "@/tools/getTutorialChapter";
import TheSubpageHeader from "@/components/TheSubpageHeader";

export default {
  name: "TutorialChapter",
  components: {TheSubpageHeader},
  data() {
    return {
      tutorialId: this.$route.params.tutorialId,
      chapterId: this.$route.params.chapterId,
      chapter: {}
    }
  },
  mounted() {
    this.loadChapter()
  },
  methods: {
    loadChapter() {
      this.chapter = getTutorialChapter(this.tutorialId, this.chapterId)
    },
    navigateToOverview() {
      router.push({name: 'contents', params: {tutorialId: this.tutorialId}})
    }
  }
}
</script>

<style lang="scss" scoped>

</style>