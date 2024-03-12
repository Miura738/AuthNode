<template>
  <div class="w-screen h-screen bg-[url(./assets/touhou-1710238054191-1816.jpg)]
  bg-no-repeat bg-cover bg-center text-white">
    <div class="bg-white bg-opacity-60 backdrop-blur-[1px] w-full h-full absolute top-0">
      <div class="w-full h-full flex justify-center items-center text-black">
        <div class="w-[40rem] p-8 h-96 bg-emerald-50 shadow-xl flex items-center justify-between relative">
    <div class="w-[20rem] min-w-[20rem] h-full   pr-16">
      <img src="./assets/d81scz2-17e584aa-f1fc-4f79-9e3e-5a00c944c52c.png" class="w-full h-full hue-rotate-180 " style="transform: rotateY(180deg)" alt="">
    </div>
            <router-view />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
</script>