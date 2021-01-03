<template>
  <router-view/>
</template>

<style lang="scss">
@import "src/css/variables/colors";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $font;
}

body {
  margin: 0;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: $font;
}

#nav a.router-link-exact-active {
  color: $link;
}
</style>
