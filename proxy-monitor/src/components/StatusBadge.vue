<template>
	<el-tag :type="status_type">
		{{current_status}}
	</el-tag>
</template>

<script>

export default {
	name: 'status-badge', 

	props: ['server_key'],

	
	computed: {
		current_status: function() {
			let last_data = this.$store.getters['getLatest'];
			if (last_data == undefined) return "UNKNOWN";
			return last_data[this.server_key]['status'];
		},

		status_type: function() {
			if (this.current_status == 'DOWN') return 'danger';
			if (this.current_status == 'UNKNOWN') return 'warning';
			if (this.current_status == 'OPEN') return 'success' ;
			if (this.current_status == 'UP') return 'success' ;
		}
	}
}
</script>