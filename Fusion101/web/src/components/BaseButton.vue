<template>
  <button>{{ text }}</button>
</template>

<script>
export default {
  name: "Button",
  props: {
    text: String
  }
}
</script>

<style lang="scss" scoped>
@import "src/css/variables/colors";
button {
  background: none;
  border: none;
  cursor: pointer;
}

button:hover{
  background-color: $highlight;
}

button:active {
  background-color: $active;
}

</style>