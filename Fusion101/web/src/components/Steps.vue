<template>
  <ol>
    <li v-for="step in chapter.steps" :key="step.order">{{ step.text }}
      <span v-on:mouseover="() => setHintToShow(step.hint)"
            v-on:mouseleave="() => setHintToShow('')">(i)</span>
    </li>
  </ol>
</template>

<script>
export default {
  name: 'ChapterSteps',
  props: {
    chapter: {},
    setHintToShow: {}
  }
}
</script>
