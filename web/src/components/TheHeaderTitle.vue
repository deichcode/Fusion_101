<template>
  <h1>{{text}}</h1>
</template>

<script>
export default {
  name: 'Title',
  props: {
    text: String
  }
}
</script>


<style scoped>
h1 {
  flex-grow: 1;
  text-align: left;
  margin: 0;
}

</style>