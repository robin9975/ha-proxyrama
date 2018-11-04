<template>
	<div>
		<canvas :id="canvas_id">
		</canvas>
	</div>
</template>


<script>

let colors = [
	'#99af5d',
	'#62a1a9',
	'#c83d32',
	'#e6b740',
	'#2b595a'
];

export default {
	'name': 'metric-chart',

	props: [
		'unit',
		'metric_key',
		'server_key' // TODO: Support multiple
	],

	data: () => {
		return {
			'max_elements': 30
		}
	},

	methods: {
	  	drawChart: function() {
	  		let ctx = document.getElementById(this.canvas_id).getContext('2d');

	  		let datasets = [];
	  		for (let index in this.metric_key_array) {
	  			let m = this.metric_key_array[index];
	  			datasets.push({
	  				data: [],
	  				borderColor: colors[index],
	  				label: m,
	  				fill: false
	  			})
	  		}

	  		this.chart = new Chart(ctx, {
			    type: 'line',
			    data: {
			    	datasets: datasets 
				},	
			    options: {
			    	scales: {
				    	xAxes: [{
		                type: 'time',
			                time: {
			                    displayFormats: {
			                        quarter: 'h:mm:ss'
			                    }
			                }
			            }],
			            yAxes: [{
			            	'scaleLabel': {
				            	'display': true,
				            	'labelString': this.unit
			            	}
			            }]
			    	}
			    }
			}); 
	  	},

	  	setInitialData: function() {
			let stats_data = this.$store.state.stats;

			this.chart.data.datasets.forEach((dataset) => {
				let values = [];
				let key_list = Object.keys(stats_data);
				for (let t = (key_list.length - this.max_elements); t < key_list.length; t++) {
					let key = key_list[t]
					if (key == undefined) {
						break;
					}

					console.log(stats_data[key][this.server_key])
					console.log(key);
					console.log(this.server_key);
					values.push({
						't': new Date(key),
						'y': stats_data[key][this.server_key][dataset.label]
					})
				}

				dataset.data = values;
			})
	  	}
	},

	mounted: function() {
		this.drawChart();
	},

	watch: {
		'$store.state.last_update_key': function() {
			if (this.chart == undefined) return;
			if (this.chart.data.datasets[0].data.length < this.max_elements) {
				this.setInitialData();
			}

			this.chart.data.datasets.forEach((dataset) => {
				let last_values = this.$store.getters['getLatest']
				dataset.data.push({
					't': new Date(this.$store.state.last_update_key),
					'y': last_values[this.server_key][dataset.label]
				});

				if (dataset.data.length > this.max_elements) {
					dataset.data.shift();
				}
		    });
		    this.chart.update();
		}
	},

	computed: {
		canvas_id: function() {
			return `${this.server_key}_${this.metric_key}`
		},

		metric_key_array: function() {
			let target_array = this.metric_key;
			if (!Array.isArray(target_array)) {
				target_array = [target_array]
			}
			return target_array;
		}
	}
}
</script>