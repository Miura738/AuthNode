<script setup>

import {ref} from "vue";

const Loading = ref(false);


import AnButton from "../../components/AnButton.vue";
import LoadingComponent from "../../components/LoadingComponent.vue";
import AnInput from "../../components/AnInput.vue";
import CryptoJS from "crypto-js"
import axios from "axios";
import {useRouter} from "vue-router";

const router = useRouter();

const LoginSubmit = (event) => {
  Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target)
  const username = formData.get("username")
  const email = formData.get("email")
  const password = (CryptoJS.SHA1(formData.get("password"))).toString()


  axios.post("/api/join?useSHA1=false",
      {
        "username": username,
        "email": email,
        "password": password,
        "requestUser": true,
      }).then(r => {
    const ApiData = r.data
      localStorage.setItem("accessToken", ApiData["accessToken"])
      localStorage.setItem("uuid",ApiData["user"]["id"])
      localStorage.setItem("name",ApiData["user"]["name"])
      localStorage.setItem("email",email)
      localStorage.setItem("textures",ApiData["user"]["properties"][0]["value"])

      Loading.value = false;
      router.push("/")

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
  <form @submit="LoginSubmit" class="flex-grow mb-1">
    <div class="mb-10 text-2xl font-mono">Join AuthNode</div>

    <div class="p-1">
      <AnInput type="email" name="email" required>Email</AnInput>
      <AnInput name="username" required>Username(ProfileName)</AnInput>

      <AnInput type="password" name="password" required>Password</AnInput>
    </div>

    <AnButton>Submit</AnButton>

  </form>

  <LoadingComponent v-if="Loading"/>
</template>