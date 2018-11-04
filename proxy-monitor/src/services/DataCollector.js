
import Vue from 'vue'

let EventBus = new Vue();

class DataCollector {

	constructor() {
		this.url =  'http://localhost:9000/stats;csv';
		this.username = 'Admin';
		this.password = 'Admin';
		this.timeout = null;
	}

	init() {
		this.config_socket = new WebSocket('ws://localhost:9001')
		this.config_socket.onopen = () => {
			this.config_socket.send(JSON.stringify({
				'command': 'config'
			}))
		}
		this.config_socket.onmessage = (event) => {
			EventBus.$emit('config', event.data);
			this.conig_socket.close();
		}

		this.socket = new WebSocket('ws://localhost:9001')
		this.socket.onopen = () => {
			this.socket.send(JSON.stringify(
				{
					'command': 'update',
					'max_elements': 100,
					'send_rate': 1
				}));
		}
		this.socket.onmessage = (event) => {
			console.log(event.data);
			EventBus.$emit('data', event.data);
		}
	}
} 



export {EventBus, DataCollector};
