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
    lastStepGroup: function () {
      return this.steps[this.steps?.length - 1].stepGroup
    },
    chapterCompleted: function () {
      return this.currentStepGroup > this.lastStepGroup
    },
    chapterDoesNotWorkRightNow: function () {
      return this.lastStepGroup === 0
    }
  },
  watch: {
    //when steps are changed (i.e. route change) the array of current steps and the current step group umber need to be refreshed
    'steps':
        function () {
          this.updateCurrentStepGroupSteps()
          this.resetCurrentStepGroup()
          //set not finished chapters automatically to done
          if (this.chapterDoesNotWorkRightNow) {
            this.sendChapterCompletedNotification()
          }
        },
    //when current step group number is updated the steps of this step gorup need to be loaded into the current step group steps array
    'currentStepGroup':
        function () {
          this.updateCurrentStepGroupSteps()
        }
  },
  methods: {
    updateCurrentStepGroupSteps() {
      this.currentStepGroupSteps = this.getStepsOfCurrentStepGroup()
    },
    getStepsOfCurrentStepGroup() {
      return this.steps?.filter((step) => step.stepGroup === this.currentStepGroup)
    },
    resetCurrentStepGroup() {
      this.currentStepGroup = 0
    },
    setStepDone(completedStep) {
      completedStep.done = true
      this.validateStepGroup()
      if (this.chapterCompleted) {
        this.sendChapterCompletedNotification()
      }
    },
    validateStepGroup() {
      let stepGroupCompleted = this.allStepsOfGroupCompleted();
      if (stepGroupCompleted) {
        this.activateNextStepGroup()
      }
    },
    allStepsOfGroupCompleted() {
      let stepGroupCompleted = true
      this.currentStepGroupSteps.forEach(step => {
        stepGroupCompleted = stepGroupCompleted && step.done
      })
      return stepGroupCompleted;
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
