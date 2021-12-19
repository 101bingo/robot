import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

import Home from '@/views/home/home'
import Robot from '@/views/robot/robot'
import Tools from '@/views/tools/tools'
import Login from '@/views/login/Login'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path:'/home',
      name:'home',
      component: Home
    },
    {
      path:'/login',
      name:'login',
      component: Login
    }
  ]
})
