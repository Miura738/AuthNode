<script setup>

</script>

<template>
<button class="w-full min-h-7 bg-emerald-500 text-white text-xs uppercase transition-all
        relative overflow-hidden btn focus:outline-0 focus:shadow-2xl focus:shadow-black shadow-black"><slot /></button>
</template>


<style scoped>
.btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: radial-gradient(circle, #ccc 10%, transparent 10.1%);
  transform: scale(10);
  opacity: 0;
  transition: all .6s;
}
.btn:active::after {
  transform: scale(0);
  opacity: .5;
  transition: 0s;
}
</style>