import Vue from 'vue'
import Router from 'vue-router'

import Login from "@/components/Login";
import HomePage from "@/components/HomePage";
import DetailPost from "@/components/DetailPost";

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/blog/:blog_id',
      name: 'blog',
      component: HomePage
    },
    {
      path: '/post/:post_id',
      name: 'post',
      component: DetailPost
    }
  ]
})

export default router