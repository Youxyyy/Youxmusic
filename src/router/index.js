import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Rankinglist from '../views/Rankinglist.vue'
import Whitenoise from '../views/Whitenoise.vue'
import Contact from '../views/Contact.vue'
import Mine from '../views/Mine.vue'
import Singer from '../views/Singer.vue'
import SingerDetail from '../views/SingerDetail.vue'
import Login from '../views/Login.vue'
import Songs from '../views/Songs.vue'
import PlaylistDetail from '../views/PlaylistDetail.vue'
import Favorite from '../views/Favorite.vue'
import Admin from '../views/Admin.vue'
import History from '../views/History.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/songs',
    name: 'Songs',
    component: Songs
  },
  {
    path: '/rankinglist',
    name: 'Rankinglist',
    component: Rankinglist
  },
  {
    path: '/whitenoise',
    name: 'Whitenoise',
    component: Whitenoise
  },
  {
    path: '/singer',
    name: 'Singer',
    component: Singer
  },
  {
    path: '/singer/:id',
    name: 'SingerDetail',
    component: SingerDetail
  },
  {
    path: '/mine',
    name: 'Mine',
    component: Mine
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { hideLayout: true }
  },
  {
    path: '/playlist/:id',
    name: 'PlaylistDetail',
    component: PlaylistDetail
  },
  {
    path: '/favorite',
    name: 'Favorite',
    component: Favorite
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/history',
    name: 'History',
    component: History
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router