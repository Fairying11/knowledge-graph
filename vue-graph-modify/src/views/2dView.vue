<template>
  <div>
    <div style="height:calc(100vh - 50px);">
       <RelationGraph ref="seeksRelationGraph" :options="graphOptions" :on-node-click="onNodeClick" :on-line-click="onLineClick" />
    </div>
  </div>
</template>

<script>
// relation-graph也支持在main.js文件中使用Vue.use(RelationGraph);这样，你就不需要下面这一行代码来引入了。
import RelationGraph from 'relation-graph'
import axios from 'axios'
export default {
  name: 'Demo',
  components: { RelationGraph },
  data () {
    return {
      graphOptions: {
        allowSwitchLineShape: true,
        allowSwitchJunctionPoint: true,
        defaultJunctionPoint: 'border',
        graphJsonData: {}
        // 这里可以参考"Graph 图谱"中的参数进行设置
      }
    }
  },
  computed: {
    getInput () {
      return this.$store.state.input
    }
  },
  mounted () {
    this.showSeeksGraph()
  },
  methods: {
    showSeeksGraph () {
      const params = {
        keyword: this.getInput
      }
      axios.post('http://127.0.0.1:5001/relationship', params).then(res => {
        if (res.status === 200) {
          this.graphJsonData = res.data.respon
          this.$refs.seeksRelationGraph.setJsonData(this.graphJsonData, (seeksRGGraph) => {
            // Called when the relation-graph is completed
          })
        }
      }).catch(err => {
        console.log('err', err)

      })
    },
    onNodeClick (nodeObject, $event) {
      console.log('onNodeClick:', nodeObject)
    },
    onLineClick (lineObject, $event) {
      console.log('onLineClick:', lineObject)
    }
  }
}
</script>
