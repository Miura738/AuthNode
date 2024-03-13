<script setup>

import {ref} from "vue";

const baseUrl = ref(window.location.protocol + "//" + window.location.host + "/api/yggdrasil");

function copy() {
  const oInput = document.createElement('input');
  oInput.value = baseUrl.value;
  oInput.style.display = "hidden"
  document.body.appendChild(oInput);
  oInput.select(); // 选择对象;
  document.execCommand("Copy"); // 执行浏览器复制命令
  oInput.remove();
}
</script>

<template>
<div @click="copy"  draggable="true" :data-clipboard-text="baseUrl" class="w-full shadow px-5 py-2 mb-8 shadow-gray-400 bg-white cursor-pointer hover:bg-emerald-100 hover:-translate-y-0.5
 transition-all active:translate-y-0">
  <div class="text-gray-500 text-xs">点击复制连接或将此模块拖入启动器</div>
  <div class="text-gray-300 text-xs mt-1">yggdrasil连接:</div>
  <div class="text-sm text-gray-900 w-full overflow-x-auto">{{baseUrl}}</div>
</div>
</template>

<style scoped>

</style>