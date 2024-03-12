<script setup>

import {onMounted, ref} from "vue";
import {useRouter} from "vue-router";
import AnButton from "../components/AnButton.vue";
import axios from "axios";
import LoadingComponent from "../components/LoadingComponent.vue";
import ProfileComponent from "./IndexView/ProfileComponent.vue";

const router = useRouter();

const UserId = ref(null);
const UserTextures = ref(null);
const UserName = ref(null);
const UserEmail = ref(null);
const UserSkin = ref("./assets/6ea6a47358157ac85c050760d26f9cbae058b370811ef1927bc55009d5b81f4f.png");
const Loading = ref(true);

onMounted(()=> {
  const accessToken = localStorage.getItem("accessToken");
  if (accessToken) {
    axios.post("/api/yggdrasil/authserver/validate", {
      accessToken: accessToken
    }).then(()=>{
     UserId.value = localStorage.getItem("uuid");
     UserTextures.value = JSON.parse(atob(localStorage.getItem("textures")));
     UserName.value = localStorage.getItem("name");
     UserEmail.value = localStorage.getItem("email");
     UserSkin.value = `/api/parse/skin?url=${UserTextures.value["textures"]["SKIN"]["url"]}`;
      Loading.value = false;
    }).catch(()=>{
    router.replace("/auth")
    })
  }else {
    router.replace("/auth")
  }

})

function Logout() {
  Loading.value = true;
  localStorage.clear();
  setTimeout(()=>{router.replace("/auth")},500)
}
function push(uri) {
  setTimeout(()=>{router.push(uri)},500)
}
</script>

<template>
  <div class="w-full h-full flex flex-col p-1 overflow-auto">
    <div class="w-full shadow px-5 py-6 shadow-gray-400 bg-white mb-8">
      <div class="flex">
        <img class="w-12 h-12 mr-4" :src='UserSkin'/>
        <div class="flex flex-col flex-grow justify-center">
          <div class="font-medium text-lg">{{UserName}}</div>
          <div class="font-thin text-xs text-gray-600">{{UserEmail}}</div>
        </div>
      </div>

      <div class="mt-3 text-xs text-gray-400 overflow-x-auto">{{UserId}}</div>

    </div>
    <div class="w-full flex flex-col gap-3">
      <ProfileComponent />

      <div class="w-full shadow px-5 py-6 shadow-gray-400 bg-white">
      </div>
    </div>

    <an-button @click="Logout" class="mt-8 w-full">Logout</an-button>

  </div>
  <LoadingComponent v-if="Loading"/>
</template>

<style scoped>

</style>