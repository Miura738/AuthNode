<script setup>


import {Input} from "postcss";

const props = defineProps({
  type: Input.types,
  name: String,
  required: Boolean
});

</script>

<template>
      <div class="flex flex-col items-start  mb-8">
        <label class="text-xs text-gray-500 transition-all mb-0.5"><slot /></label>
        <input class="w-full border-b border-stone-500 focus:outline-0 p-1 text-sm h-7"
               :required="props.required"
               :type="props.type"
               :name="props.name">
      </div>
</template>

<style scoped>

</style>