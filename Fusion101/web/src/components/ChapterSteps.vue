<template>
  <ol class="chapter-steps">
    <!--    Create a ChapterStep element for each step in chapter-->
    <ChapterStep v-for="step in steps" :key="step" :step="step"
                 :set-hint-to-show="setHintToShow"
                 :isCurrentStep="step.stepGroup === currentStepGroup"
                 :completeStepCallback="setStepDone"
    />
  </ol>
</template>

<script>
import ChapterStep from "@/components/ChapterStep";

export default {
  name: 'ChapterSteps',
  components: {ChapterStep},
  props: {
    steps: {},
    setHintToShow: {}
  },
  data() {
    return {
      currentStepGroup: 0,
      currentStepGroupSteps: []
    }
  },
  computed: {
    lastStepGroup: function() {
      return this.steps[this.steps.length - 1].stepGroup
    },
    chapterCompleted: function() {
      console.log("chapter Completed: ", this.currentStepGroup > this.lastStepGroup)
      return this.currentStepGroup > this.lastStepGroup
    }
  },
  watch: {
    'steps': function () {
      this.updateCurrentStepGroupSteps()
      this.resetCurrentStepGroup()
    },
    'currentStepGroup': function () {
      this.updateCurrentStepGroupSteps()
    }
  },
  methods: {
    updateCurrentStepGroupSteps() {
      this.currentStepGroupSteps = this.steps?.filter((step) => step.stepGroup === this.currentStepGroup)
    },
    resetCurrentStepGroup() {
      this.currentStepGroup = 0
    },
    setStepDone(completedStep) {
      completedStep.done = true
      this.validateStepGroup()
      if(this.chapterCompleted){
        this.sendChapterCompletedNotification()
      }
    },
    validateStepGroup() {
      let stepGroupCompleted = true
      this.currentStepGroupSteps.forEach(step => {
        stepGroupCompleted = stepGroupCompleted && step.done
      })
      if (stepGroupCompleted) {
        this.activateNextStepGroup()
      }
    },
    activateNextStepGroup() {
      this.currentStepGroup += 1
    },
    sendChapterCompletedNotification() {
      this.$emit('chapterCompleted')
    }
  }
}
</script>

<style lang="scss" scoped>
.chapter-steps {
  padding-left: 30px;
}
</style>
