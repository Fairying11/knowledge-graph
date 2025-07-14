import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 输入内容
    input: ''
  },
  mutations: {
    // 更新输入内容
    updateInput (state, input) {
      state.input = input
    }
  },
  actions: {
  },
  modules: {
  }
})
