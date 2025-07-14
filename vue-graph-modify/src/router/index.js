import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/1dView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/2dView',
    name: '2dView',
    component: () => import('../views/2dView.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
