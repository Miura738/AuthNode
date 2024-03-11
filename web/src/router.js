import { createRouter,createWebHashHistory } from 'vue-router'
import HelloWorld from "./components/HelloWorld.vue";
import LoginView from "./view/LoginView.vue";

const routes = [
  {
    path: '/',
    name: 'root',
    component: HelloWorld
  },
  {
    path: "/login",
    component: LoginView
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})
//
//
// router.beforeEach((to, from, next) => {
//   // 每次切换页面时，调用进度条
//   // 这个一定要加，没有next()页面不会跳转的。这部分还不清楚的去翻一下官网就明白了
//   next();
// });
// router.afterEach((to) => {
//       // document.title = "Web | UIM";
//       if (to.meta.title) {
//         document.title = to.meta.title + " | " + "白澪";
//       }
//
//     }
// )


export default router;