<script setup>
import {Input} from "postcss";

const Loading = ref(false);

import AnInput from "../../components/AnInput.vue";
import AnButton from "../../components/AnButton.vue";
import {ref} from "vue";
import axios from "axios";
import {useRouter} from "vue-router";
import LoadingComponent from "../../components/LoadingComponent.vue";


const UserTextures = ref(JSON.parse(atob(localStorage.getItem("textures"))));
const UserSkin = ref(UserTextures.value["textures"]["SKIN"]["url"]);
const UserSkinType = ref(UserTextures.value["textures"]["SKIN"]["metadata"]["model"]);

const router = useRouter();
function Submit(event) {
      // Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target);


  axios.put(`/api/user/profile/${localStorage.getItem("uuid")}/SKIN?backTextures=true`,formData,{
    headers: {
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      "Content-Type": 'multipart/form-data'
    }
  }).then(r => {
    const ApiData = r.data
      localStorage.setItem("textures",ApiData["properties"][0]["value"])
    location.reload()
  }).catch(
      error => {
        try {
          alert(error.response.data["cause"])

        } catch (e) {
          alert("Unknown error!")
        }

        Loading.value = false;
      }
  )
  Loading.value = false;

}
</script>

<template>
<form @submit="Submit" class="w-full shadow px-5 py-6 shadow-gray-400 bg-white">


   <div class="flex flex-col items-start  mb-4">
        <label class="text-xs text-gray-500 transition-all mb-2">You skin Now:</label>
        <input class="w-full border border-stone-500 focus:outline-0 p-1 text-sm h-9"
               required
               type="file"
               name="file">

        <div class="flex w-full mt-3">
          <div class="flex items-center">
            <input required type="radio" id="classic" name="model" value="classic">
            <label for="classic" class="text-sm uppercase ml-1">Classic</label>
          </div>
          <div class="flex items-center ml-5">
            <input required type="radio" id="slim" name="model" value="slim">
            <label for="slim" class="text-sm uppercase ml-1">Slim</label>
          </div>
        </div>
      </div>

  <an-button>Submit</an-button>

     <div class="flex flex-col items-start  mt-8">
        <label class="text-xs text-gray-500 transition-all mb-1">You skin Now:</label>
        <div class="w-full p-1 text-sm flex items-start justify-start">
          <img :src="UserSkin" class="w-full h-full shadow-xl">
        </div>
      </div>

</form>
  <LoadingComponent v-if="Loading"/>
</template>

<style scoped>

</style>