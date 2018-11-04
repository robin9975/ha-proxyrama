<template>
  <div class="home">
	  	<template :span="12" v-for="c in config">
	  	<el-row :gutter="15" style="margin-bottom: 45px;">
	  		<h2>
		  		{{c.name}}
		  		<status-badge :server_key='c.server'></status-badge>
		  	</h2>
	  		<el-col :span="24 / c.metrics.length" v-for="m in c.metrics">
			  	<div style="width: 100%; margin: 0; display: inline-block;">
			  		<metric-chart :server_key='c.server' :metric_key="m.keys" :unit="m.unit"></metric-chart>
			  	</div>
		  	</el-col>
	  	</el-row>
	  </template>
  </div>
</template>

<script>
// @ is an alias to /src
import {EventBus, DataCollector} from '@/services/DataCollector.js'

import MetricChart from '@/components/MetricChart'
import StatusBadge from '@/components/StatusBadge'

import Chart from 'chart.js'

export default {
  name: 'home',

  mounted: function() {
  	EventBus.$on('data', (data) => {
  		this.$store.commit('storeStatsUpdate', JSON.parse(data));
  	})
  	EventBus.$on('config', (config) => {
  		this.$store.commit('storeConfig', JSON.parse(config));
  	})
  	let collector = new DataCollector();
  	collector.init();
  },

  computed: {
  	'config': function() {
  		return this.$store.getters['config'];
  	}
  },

  components: {
  	MetricChart,
  	StatusBadge
  }
}
</script>
