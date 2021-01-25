<template>
  <div :key="tutorialId + chapterId">
    <div id="header-wrapper">
      <TheSubpageHeader
          :title="chapter.title"
          back-button-title="^ Tutorial Overview"
          :back-button-action="navigateToOverview"
          :storeRef="storeRef('header')"
      />
      <ChapterStepHintVideo id="fixed-hint" :class="{'hidden': !scrollingHintIsCovered }" :hint="hintToShow"/>
    </div>
    <main>
      <p class="description">{{ chapter.description }}</p>
      <!--      Hint Videos can have a size of 380x163@2 (double resolution)-->
      <!--      Hint Videos can have a size of 570x245@2 (double resolution)-->
      <!--      Hint Videos can have a size of 760x328@2 (double resolution)-->
      <ChapterStepHintVideo :class="{'hidden': scrollingHintIsCovered }" :storeRef="storeRef('scrollingHint')"
                            :hint="hintToShow"/>
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
import ChapterNavigation from "@/components/ChapterNavigation";
import {executeOnScroll} from "@/tools/eventListener/scrollEvent";

export default {
  name: "TutorialChapter",
  components: {ChapterNavigation, ChapterSteps, ChapterStepHintVideo, TheSubpageHeader},
  data() {
    return {
      tutorialId: this.$route.params.tutorialId,
      chapterId: this.$route.params.chapterId,
      chapter: {},
      hintToShow: "",
      hintIsInViewport: true,
      refs: [],
      scrollingHintIsCovered: false,
    }
  },
  mounted() {
    this.loadChapter();
    executeOnScroll(this.updateScrollingHintIsCovered)
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
    updateScrollingHintIsCovered() {
      const hintBorderSize = 2
      const header = this.refs['header']
      const scrollingHint = this.refs['scrollingHint']
      const headerBottomBorder = header.getBoundingClientRect().bottom
      const scrollingVideoTopBorder = scrollingHint.getBoundingClientRect().top
      this.scrollingHintIsCovered = headerBottomBorder + hintBorderSize > scrollingVideoTopBorder;
    },
    navigateToOverview() {
      router.push({name: 'contents', params: {tutorialId: this.tutorialId}})
    },
    setHintToShow(hint) {
      this.hintToShow = hint
    },
    storeRef(name) {
      return (ref) => {
        this.refs[name] = ref
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";

$footerHeight: 30px;

#header-wrapper {
  position: sticky;
  top: 0;
  z-index: 1;
}

#fixed-hint {
  position: absolute;

  &.hidden {
    visibility: hidden;
  }
}

.description {
  margin-top: 0;
}

main {
  margin-bottom: $footerHeight;

  .hint {
    margin-left: -10px;
    margin-right: -10px;
    width: calc(100% + 20px);
    background: $white;

    &.hidden {
      visibility: hidden;
    }
  }
}

footer {
  pointer-events: none;
  position: fixed;
  bottom: 0;
  padding: 20px 10px 10px;
  width: calc(100% - 20px);


  /* Permalink - use to edit and share this gradient: https://colorzilla.com/gradient-editor/#ffffff+0,ffffff+100&0+0,1+28 */
  background: -moz-linear-gradient(top, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 1) 100%); /* FF3.6-15 */
  background: -webkit-linear-gradient(top, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 1) 100%); /* Chrome10-25,Safari5.1-6 */
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 28%, rgba(255, 255, 255, 1) 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#00ffffff', endColorstr='#ffffff', GradientType=0); /* IE6-9 */
}

</style>