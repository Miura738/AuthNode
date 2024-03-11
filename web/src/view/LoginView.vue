<script setup>

const LoginSubmit = (event) => {
  event.preventDefault();
  console.log(1);
}

</script>

<template>
<div class="w-full h-full flex justify-center items-center text-black">

  <div class="w-[35rem] p-8 h-80 bg-emerald-50 shadow-xl flex items-center justify-between">
    <div class="flex-grow">

    </div>
    <form @submit="LoginSubmit" class="w-56">
      <div class="mb-10 text-2xl font-mono">AuthNode OpenID</div>

      <div class="flex flex-col items-start mb-8">
        <label class="text-xs text-gray-500 transition-all mb-0.5">Email / Username</label>
        <input class="w-full border-b border-stone-500 focus:outline-0 p-1 text-sm h-7">
      </div>

      <div class="flex flex-col items-start  mb-8">
        <label class="text-xs text-gray-500 transition-all mb-0.5">Password</label>
        <input class="w-full border-b border-stone-500 focus:outline-0 p-1 text-sm h-7 " type="password">
      </div>

      <button class="w-full h-7 bg-emerald-500 text-white text-xs uppercase transition-all
        shadow-2xl relative overflow-hidden btn">Submit</button>

    </form>
  </div>

</div>
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