import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

import Home from '@/views/home/home'
import Robot from '@/views/robot/robot'
import Tools from '@/views/tools/tools'
import Login from '@/views/login/Login'

Vue.use(Router)

// export default new Router({
//   mode:'history',
//   routes: [
//     {
//       path: '/',
//       name: 'login',
//       component: Login
//     },
//     {
//       path:'/home',
//       name:'home',
//       component: Home
//     },
//     {
//       path:'/login',
//       name:'login',
//       component: Login
//     }
//   ]
// })


export const constantRoutes = [
  {
    path:'/',
    component: ()=>import(Login)
  },
  {
    path:'/home',
    component: Layout,
    meta:{title:'home',icon:'icon'}
  },
  {
    path:'/login',
    component: ()=>import(Login)
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router