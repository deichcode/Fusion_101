<template>
  <ol class="chapter-steps">
    <!--    Create a li element for each step in chapter-->
    <li v-for="step in chapter.steps" :key="step.order">
      <BaseTooltipText :text="step.text" :tooltips="step.tooltips"/>
      <!--      Set Hint when mouse if over hint icon and remove when mouse is no longer over icon-->
      <span v-if="step.hint"
            v-on:mouseover="() => setHintToShow(step.hint)"
            v-on:mouseleave="() => setHintToShow('')"> (i)</span>
    </li>
  </ol>
</template>

<script>
import BaseTooltipText from "@/components/BaseTooltipText";

export default {
  name: 'ChapterSteps',
  components: {BaseTooltipText},
  props: {
    chapter: {},
    setHintToShow: {}
  },
}
</script>

<style lang="scss" scoped>
.chapter-steps {
  padding-left: 30px;

  li {
    margin-bottom: 10px;
  }
}
</style>
