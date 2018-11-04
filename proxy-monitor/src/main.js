// General high-level imports
import Vue from 'vue'
import VueResource from 'vue-resource'
import Element from 'element-ui'

// App specific
import App from './App.vue'
import router from './router'
import store from './store'

import 'element-ui/lib/theme-chalk/index.css';

Vue.use(Element)
Vue.use(VueResource);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
