<script setup>

import {ref} from "vue";
const Loading = ref(false);


import AnButton from "../../components/AnButton.vue";
import LoadingComponent from "../../components/LoadingComponent.vue";
import AnInput from "../../components/AnInput.vue";
import CryptoJS from "crypto-js"

const LoginSubmit = (event) => {
  Loading.value = true;
  event.preventDefault();

  const formData = new FormData(event.target)
  const user = formData.get("user")
  const password = (CryptoJS.SHA1(formData.get("pwd"))).toString()

  console.log(user)
  console.log(password)

}

</script>
<template>
<form @submit="LoginSubmit" class="flex-grow mb-1">
      <div class="mb-10 text-2xl font-mono">AuthNode OpenID</div>

      <div class="p-1">
        <AnInput name="user" required>Email / Username</AnInput>

        <AnInput type="password" name="pwd" required>Password</AnInput>
      </div>

  <AnButton>Submit</AnButton>

    </form>

  <LoadingComponent v-if="Loading" />
</template>