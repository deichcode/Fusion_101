<template>
  <button>{{ text }}</button>
</template>

<script>
export default {
  name: "BaseButton",
  props: {
    text: String
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";
@import "src/css/mixins/clickable";

button {
  @include clickable;
  border: 1px solid $active;
  border-radius: 2px;
  height: 1.6rem;
}

</style>