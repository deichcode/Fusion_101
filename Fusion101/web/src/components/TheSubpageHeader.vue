<template>
  <header ref="header">
    <div class="button-row">
      <BaseButton :text="backButtonTitle"
                  v-on:click="backButtonAction"></BaseButton>
    </div>
    <Title class="title" :text="title"/>
  </header>
</template>

<script>
import Title from "@/components/TheHeaderTitle";
import BaseButton from "@/components/BaseButton";

export default {
  name: "TheSubpageHeader",
  components: {BaseButton, Title},
  props: {
    backButtonTitle: String,
    backButtonAction: Function,
    title: String,
    storeRef: Function
  },
  mounted() {
    //pass Reference to dom element to using component
    this.storeRef(this.$refs.header)
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";

header {
  padding: 10px;
  position: sticky;
  top: 0;
  background-color: $menu-background;

  > .button-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: .8rem;

    button {
      margin-left: 0;
    }
  }
}
</style>