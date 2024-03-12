<script setup>
const Loading = ref(false);

import AnInput from "../../components/AnInput.vue";
import AnButton from "../../components/AnButton.vue";
import {ref} from "vue";
import axios from "axios";
import {useRouter} from "vue-router";
import LoadingComponent from "../../components/LoadingComponent.vue";

const UserName = ref(localStorage.getItem("name"));
const router = useRouter();
function Submit(event) {
      Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target);
  axios.post(`/api/user/profile/${localStorage.getItem("uuid")}/name`,
      {
        accessToken: localStorage.getItem("accessToken"),
        profileName: formData.get("profileName")
      }).then(() => {
      localStorage.setItem("name",formData.get("profileName"))
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

}
</script>

<template>
<form @submit="Submit" class="w-full shadow px-5 py-6 shadow-gray-400 bg-white">
   <div class="flex flex-col items-start  mb-2">
        <label class="text-xs text-gray-500 transition-all mb-1">You profile name Now:</label>
        <div class="w-full p-1 text-sm flex items-start justify-start">
          <div>
            {{UserName}}
          </div>
        </div>
      </div>
  <an-input name="profileName" required class="flex-grow">New profile name!</an-input>
  <an-button>Submit</an-button>
</form>
  <LoadingComponent v-if="Loading"/>
</template>

<style scoped>

</style>