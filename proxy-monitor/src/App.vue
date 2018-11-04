<template>
  <div id="app">

    <el-container>
      <el-container>
      <el-aside width="200px">
        <h1>HAProxy Monitor</h1>
        <h3>Views</h3>
      </el-aside>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </el-container>
  </div>
</template>

<style lang="scss">
#app {
  font-family: 'Raleway';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  overflow-y: scroll;
}
</style>
