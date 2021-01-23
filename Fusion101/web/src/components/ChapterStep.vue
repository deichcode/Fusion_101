<template>
  <li class="chapter-step" :class="{'chapter-step--done': isDone }">
    <BaseTooltipText :text="step.text" :tooltips="step.tooltips"/>
    <!--      Set Hint when mouse if over hint icon and remove when mouse is no longer over icon-->
    <span v-if="step.hint"
          v-on:mouseover="setHintToShow(step.hint)"
          v-on:mouseleave="setHintToShow('')">
        <span
            v-on:mouseover="setStepHintHoverd(true)"
            v-on:mouseleave="setStepHintHoverd(false)"
        >
          <span v-if="hintIsDisplayed" class="hint-bulb">
            <font-awesome-icon :icon="['far', 'lightbulb']"/>
          </span>
          <span v-else class="hint-bulb">
            <font-awesome-icon :icon="['fas', 'lightbulb']"/>
          </span>
          <span v-if="isDone" class="checkmark">
            <font-awesome-icon :icon="['fas', 'check']"/>
        </span>
        </span>
    </span>
  </li>
</template>
<script>
import BaseTooltipText from "@/components/BaseTooltipText"

export default {
  name: 'ChapterStep',
  components: {BaseTooltipText},
  props: {
    step: {},
    setHintToShow: {},
  },
  data() {
    return {
      hintIsDisplayed: false,
      isDone: false
    }
  },
  methods: {
    handleFusionMessage: function (event) {
      const messageStatesStepCompletion = event.detail.data === this.step.event
      if (messageStatesStepCompletion) {
        this.isDone = true
      }
    },
    setStepHintHoverd: function (isShown) {
      this.hintIsDisplayed = isShown
    }
  },
  mounted() {
    window.addEventListener('Fusion360Message', this.handleFusionMessage);
  }
}
</script>
<style lang="scss" scoped>
@import "src/css/variables/colors";

.chapter-step {
  margin-bottom: 10px;

  .hint-bulb,
  .checkmark {
    margin-left: 10px
  }

  &--done {
    color: $green;

    .hint-bulb {
      display: none
    }
  }
}
</style>