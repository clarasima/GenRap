import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/auth/LoginView.vue';
import UserProfile from '../views/UserProfile.vue';
import Signup from '../views/auth/SignupView.vue';
import CreateReport from '../views/CreateReport.vue';
import MyPublications from '../views/PublicationsView.vue';
import MyPublCitations from '@/views/PubCitationsView.vue';
import CitationsView from '../views/CitationsView.vue';
import { getToken } from '@/composables/tokenManagement';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/signup',
    name: 'signup',
    component: Signup
  },
  {
    path: '/createReport',
    name: 'createReport',
    component: CreateReport
  },
  {
    path: '/myPublications',
    name: 'myPublications',
    component: MyPublications
  },
  {
    path: '/pubCitations',
    name: 'pubCitations',
    component: MyPublCitations
  },
  {
    path: '/profile',
    name: 'userProfile',
    component: UserProfile
  },
  {
    path: '/citations/:id',
    name: 'citations',
    component: CitationsView,
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = getToken();
  const publicPages = ['login', 'signup', 'home'];
  if (token || publicPages.includes(to.name)) {
    next(); 
  } else {
    next({ name: 'login' });
  }
});

export default router
