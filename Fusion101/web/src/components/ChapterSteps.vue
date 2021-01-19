<template>
  <ol class="chapter-steps">
    <!--    Create a ChapterStep element for each step in chapter-->
    <ChapterStep v-for="step in chapter.steps" :key="step" :step="step"
                 :set-hint-to-show="setHintToShow"/>
  </ol>
</template>

<script>
import ChapterStep from "@/components/ChapterStep";

export default {
  name: 'ChapterSteps',
  components: {ChapterStep},
  props: {
    chapter: {},
    setHintToShow: {}
  },
}
</script>

<style lang="scss" scoped>
.chapter-steps {
  padding-left: 30px;
}
</style>
