<template>
  <li class="chapter-step" :class="{'chapter-step--done': step.done, 'chapter-step--active': isCurrentStep }">
    <BaseTooltipText :text="step.text" :tooltips="step.tooltips"/>
    <!--      Set Hint when mouse if over hint icon and remove when mouse is no longer over icon-->
    <span v-if="showHint()"
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
          <span v-if="step.done" class="checkmark">
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
    isCurrentStep: Boolean,
    completeStepCallback: Function
  },
  data() {
    return {
      hintIsDisplayed: false
    }
  },
  methods: {
    handleFusionMessage: function (event) {
      if (!this.isCurrentStep) {
        return
      }
      const messageStatesStepCompletion = event.detail.data === this.step.event
      if (messageStatesStepCompletion) {
        this.completeStepCallback(this.step)
      }
    },
    showHint: function () {
      const stepHasHint = this.step.hint
      const hintShouldBeVisible = this.isCurrentStep || this.step.done
      return stepHasHint && hintShouldBeVisible
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
  color: $midGray;
  margin-bottom: 10px;

  .hint-bulb,
  .checkmark {
    margin-left: 10px
  }

  &--active {
    color: $font
  }

  &--done {
    color: $green;

    .hint-bulb {
      display: none
    }
  }
}
</style>