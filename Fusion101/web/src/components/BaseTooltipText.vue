<template>
  <span v-html="textWithTooltips" class="text-with-tooltips"></span>
</template>
<script>
import parseTooltips from "@/tools/parseTooltips";

export default {
  name: 'BaseTooltipText',
  props: {
    text: {},
    tooltips: {},
  },
  data() {
    return {
      textWithTooltips: ""
    }
  },
  beforeMount() {
    this.textWithTooltips = parseTooltips(this.text, this.tooltips)
  },
  mounted() {
    this.addListenerToEnsureTooltipsAreVisible();
  },
  methods: {
    addListenerToEnsureTooltipsAreVisible: function () {
      const tooltips = document.getElementsByClassName('tooltip__trigger')
      tooltips.forEach(tooltip => {
        tooltip.addEventListener("mouseenter", this.ensureTooltipIsVisible)
      })
    },
    ensureTooltipIsVisible: function (event) {
      event.stopImmediatePropagation(); // Necessary to prevent multiple invocations of this function
      const tooltipContent = event.target.children[0]
      const tooltipTriangle = tooltipContent.children[0]
      const tooltipContentBoundingBox = tooltipContent.getBoundingClientRect()
      const marginFromWindowBorder = 5
      if (this.tooltipIsOutOfWindowLeft(tooltipContentBoundingBox)) {
        const offsetFromLeft = this.getDistanceFromLeftWindowBorderToLeftTooltipBorder(tooltipContentBoundingBox)
        const amountToMoveToTheRight = offsetFromLeft + marginFromWindowBorder
        this.moveTooltipHorizontal(tooltipContent, tooltipTriangle, amountToMoveToTheRight)
      }
      const upperRightCornerX = tooltipContentBoundingBox.x + tooltipContentBoundingBox.width
      if (this.tooltipIsOutOfWindowRight(upperRightCornerX)) {
        const offsetFromRight = Math.ceil(upperRightCornerX - window.innerWidth)
        const amountToMoveToTheLeft = offsetFromRight + marginFromWindowBorder
        this.moveTooltipHorizontal(tooltipContent, tooltipTriangle, -amountToMoveToTheLeft)
      }
    },
    tooltipIsOutOfWindowLeft: function (tooltipContentBoundingBox) {
      return tooltipContentBoundingBox.x < 0
    },
    getDistanceFromLeftWindowBorderToLeftTooltipBorder: function (tooltipBoundingBox) {
      return Math.ceil(-tooltipBoundingBox.x)
    },
    tooltipIsOutOfWindowRight: function (upperRightCornerX) {
      return upperRightCornerX > window.innerWidth
    },
    moveTooltipHorizontal: function (tooltipContent, tooltipTriangle, amountInPixel) {
      tooltipContent.style.left = `calc(50% + ${amountInPixel}px)`
      tooltipTriangle.style.left = `calc(50% - ${amountInPixel}px)` //Keep triangle at original position
    }
  }
}

</script>

<!--//https://www.w3schools.com/css/css_tooltip.asp-->
<style lang="scss" scoped>
@import "src/css/variables/colors";

$tooltipWidth: 200px;
.text-with-tooltips {
  ::v-deep(.tooltip__trigger) {
    position: relative;
    display: inline-block;
    //border-bottom: 1px dotted $link; /* If you want dots under the hoverable text */
    text-decoration: underline dotted $link;
    text-underline-offset: 3px;
    cursor: help;
  }

  /* Tooltip text */
  ::v-deep(.tooltip__trigger .tooltip__content) {
    visibility: hidden;
    width: $tooltipWidth;
    background-color: $active;
    color: #fff;
    text-align: center;
    padding: 5px;
    border-radius: 6px;

    /* Position the tooltip text - see examples below! */
    position: absolute;
    z-index: 1;
    top: calc(100% + 4px);
    left: 50%;
    margin-left: -$tooltipWidth/2; /* Use half of the width (120/2 = 60), to center the tooltip */

    opacity: 0;
    transition: opacity 200ms;
  }

  /* Show the tooltip text when you mouse over the tooltip container */
  ::v-deep(.tooltip__trigger:hover .tooltip__content) {
    visibility: visible;
    opacity: 1;
  }

  ::v-deep(.tooltip__trigger .tooltip__triangle) {
    position: absolute;
    bottom: 100%; /* At the top of the tooltip */
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent transparent $active transparent;
  }
}
</style>