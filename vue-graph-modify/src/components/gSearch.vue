<template>
	<div style="margin-top: 20px;width: 500px;">
		<el-autocomplete style="width: 500px" class="inline-input" v-model="input" :fetch-suggestions="querySearch"
		 placeholder="请输入内容" :trigger-on-focus="false" @select="handleSelect" clearable>
			<el-button slot="append" type="success" icon="el-icon-search" @click="query">搜索</el-button>
		</el-autocomplete>
	</div>
</template>
<!-- http://127.0.0.1:5000/star/attribute -->
<!-- http://127.0.0.1:5001/star/relationship -->

<script>
import axios from 'axios'
export default {
  name: 'gSearch',
  data () {
    return {
      input: '',
      mode: '1',
      // 后台请求到的json数据
      data: {},
      results: []
    }
  },
  methods: {
    // 搜索
    query () {
      const params = {
        keyword: this.input
      }
	  axios.post('http://127.0.0.1:5001/star/attribute', params).then(res => {
	    if (res.status === 200) {
	      this.data = res.data.respon
          this.$emit('getData', this.data)
          this.$store.commit('updateInput', this.input)
	    }
	  }).catch(err => {
	    console.log('err', err)

	  })
    },
    querySearch (queryString, cb) {
      var res = this.results
      var results = queryString ? res.filter(this.createFilter(queryString)) : res
      // 调用 callback 返回建议列表的数据
      cb(results)
    },
    createFilter (queryString) {
      return (res) => {
        return (res.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1)
      }
    },
    handleSelect (item) {
      console.log(item)
    }
  }
}
</script>

<style lang='scss' scoped>
	.el-select {
		width: 120px;
	}

	.input-with-select .el-input-group__prepend {
		background-color: #6ecbf3;
	}
</style>
