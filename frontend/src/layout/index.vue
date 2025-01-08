<script lang="ts" setup></script>

<template>
  <n-layout id="layout" class="layout">
    <Header></Header>
    <main>
      <RouterView />
    </main>
    <Footer></Footer>
  </n-layout>
</template>

<style lang="scss" scoped>
.layout {
  display: flex;
  flex-direction: column;
  margin: 0 auto;

  // max-width: 1920px;
  background: #000;

  main {
    flex: 1;
  }
}
</style>
