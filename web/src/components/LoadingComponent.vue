<script setup>

</script>

<template>
  <div class="absolute top-0 left-0 bg-white w-full h-full bg-opacity-75 flex justify-center items-center">
    <div class="loading"></div>
  </div>
</template>

<style scoped>
.loading {
  position: relative;
  width: 140px;
  height: 140px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-left-color: #26574a;
  border-radius: 100%;

  animation: circle infinite 0.75s linear;
}

@keyframes circle {
  0% {
    transform: rotate(0);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>