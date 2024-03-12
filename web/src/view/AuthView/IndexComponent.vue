<script setup>


import {useRouter} from "vue-router";
import AnButton from "../../components/AnButton.vue";
const router = useRouter();
function push(uri) {
  setTimeout(()=>{router.push(uri)},500)
}

</script>

<template>
<div class="flex-grow mb-1 flex flex-col items-center">

  <div class="text-3xl font-mono mb-20">Welcome to AuthNode Login Gateway</div>
  <div class="flex flex-col gap-5 w-full">
    <AnButton @click="push('/login')">Sign In</AnButton>
    <AnButton @click="push('/join')">Sign Up</AnButton>
  </div>
</div>

</template>
