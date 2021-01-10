<template>
  <ol class="chapter-steps">
    <li v-for="step in chapter.steps" :key="step.order">
      <BaseTooltipText :text="step.text" :tooltips="step.tooltips"/>
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
