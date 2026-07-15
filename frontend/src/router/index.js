import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import MapView from '../views/MapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // 게시판 목록
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    // 게시글 작성
    {
      path: '/posts/create',
      name: 'post-create',
      component: () => import('../views/PostCreateView.vue'),
    },

    // 게시글 수정
    {
      path: '/posts/:id/edit',
      name: 'post-edit',
      component: () => import('../views/PostEditView.vue'),
    },

    // 게시글 상세
    {
      path: '/posts/:id',
      name: 'post-detail',
      component: () => import('../views/PostDetailView.vue'),
    },

    {
      path: '/map',
      name: 'map',
      component: MapView,
    },
  ],
})

export default router
