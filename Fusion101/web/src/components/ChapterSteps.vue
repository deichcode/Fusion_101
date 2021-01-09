<template>
  <ol>
    <li v-for="step in chapter.steps" :key="step.order">
      <BaseTooltipText :text="step.text" :tooltips="step.tooltips"/>
      <span v-on:mouseover="() => setHintToShow(step.hint)"
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
