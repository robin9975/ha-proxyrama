import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	'stats': {},
  	'config': {},
  	'last_update_key': null
  },
  getters: {
  	getLatest: (state) =>  {
  		return state.stats[state.last_update_key];
  	},

  	config: (state) => {
  		return state.config;
  	}
  },
  mutations: {
  	storeStatsUpdate: (state, data_response) => {
  		for (let time_key of Object.keys(data_response).sort()) {
	  		let data = data_response[time_key];
	  		state.stats[time_key] = {}
	  		for (let x of data) {
	  			console.log(`${x['pxname']}_${x['svname']}`)
	  			state.stats[time_key][`${x['pxname']}_${x['svname']}`] = x;
	  		}
	  		state.last_update_key = time_key
  		}
  	},

  	storeConfig: (state, config) => {
  		// TODO: Validate configuration??
  		state.config = config;
  	}
  },
  actions: {

  }
})
