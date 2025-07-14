<template>
  <div class="gContainer">
    <div class="search-box">
        <gSearch @getData="update" />
    </div>
    <section class="personal-info">
      <h2 class="name" >{{searchResult.name}}</h2>
      <div class="basic-info">
        <div class="info-icon-box">
            <span class="info-icon"></span>
            <span class="basic-text">基本信息</span>
        </div>
        <div class="info-cont">
          <div class="all-generalization">{{searchResult.summary}}</div>
          <div class="detailed-desc"></div>
        </div>
        <div class="line-desc-box cmn-clearfix">
            <dl class="basicInfo-block basicInfo-left" v-for="(val, key) in searchResult.basicInfo" :key="key">
                <dt class="basicInfo-item name" >{{key}}</dt>
                <dd class="basicInfo-item value">{{val}}</dd>
            </dl>
        </div>
      </div>
    </section>
    <d3graph
      :data="data"
      :names="names"
      :labels="labels"
      :linkTypes="linkTypes"
    />
  </div>
</template>

<script>
import gSearch from '@/components/gSearch.vue'
import d3graph from '@/components/d3graph.vue'
export default {
  components: {
    gSearch,
    d3graph
  },
  data () {
    return {
      // d3jsonParser()处理 json 后返回的结果
      data: {
        nodes: [],
        links: []
      },
      names: ['企业', '贸易类型', '地区', '国家'],
      labels: ['Enterprise', 'Type', 'Region', 'Country'],
      linkTypes: ['', 'type', 'locate', 'export'],
      searchResult: {
        summary: '',
        basicInfo: {}
      }
    }
  },
  methods: {
    // 视图更新
    update (json) {
      this.searchResult = json
      console.log('searchResult', this.searchResult)
      // this.d3jsonParser(json)
    },
    /*eslint-disable*/
    // 解析json数据，主要负责数据的去重、标准化
    d3jsonParser (json) {
      const nodes =[]
      const links = [] // 存放节点和关系
      const nodeSet = [] // 存放去重后nodes的id

      // 使用vue直接通过require获取本地json，不再需要使用d3.json获取数据
      // d3.json('./../data/records.json', function (error, data) {
      //   if (error) throw error
      //   graph = data
      //   console.log(graph[0].p)
      // })

      for (let item of json) {
        for (let segment of item.p.segments) {
          // 重新更改data格式
          if (nodeSet.indexOf(segment.start.identity) == -1) {
            nodeSet.push(segment.start.identity)
            nodes.push({
              id: segment.start.identity,
              label: segment.start.labels[0],
              properties: segment.start.properties
            })
          }
          if (nodeSet.indexOf(segment.end.identity) == -1) {
            nodeSet.push(segment.end.identity)
            nodes.push({
              id: segment.end.identity,
              label: segment.end.labels[0],
              properties: segment.end.properties
            })
          }
          links.push({
            source: segment.relationship.start,
            target: segment.relationship.end,
            type: segment.relationship.type,
            properties: segment.relationship.properties
          })
        }
      }
      console.log(nodes)
      console.log(links)
      // this.links = links
      // this.nodes = nodes
      this.data = { nodes, links }
      // return { nodes, links }
    }
  }
}
</script>

<style lang="scss" scoped>
* {
    margin: 0;
    padding: 0;
}
.gContainer {
  position: relative;
  border: 2px #000 solid;
  background-color: #9dadc1;
  overflow: hidden;
  .search-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .personal-info {
    margin: 40px 0 0 20%;
    width: 60%;
    .basic-info {
        .info-icon-box {
            margin: 10px 0;
            .info-icon {
                display: inline-block;
                width: 8px;
                height: 16px;
                background-color: #609ce8;
            }
            .basic-text {
                font-size: 20px;
                margin-left: 10px;
            }
        }
    }
    .info-cont {
        text-indent: 2rem;
        font-size: 15px;
        .detailed-desc {
            margin-top: 10px;
            line-height: 25px;
        }
    }
    .line-desc-box {
        margin: 20px 0 35px;
        overflow: hidden;
        clear: both;
        background: url(https://bkssl.bdimg.com/static/wiki-lemma/widget/lemma_content/mainContent/basicInfo/img/basicInfo-bg_ccaff81.png);
        .basicInfo-block {
            width: 395px;
            float: left;
            .basicInfo-item {
                line-height: 26px;
                display: block;
                padding: 0;
                margin: 0;
                float: left;
            }
            .name {
                width: 90px;
                padding: 0 5px 0 12px;
                font-weight: 700;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                word-wrap: normal;
                color: #999;
            }
            .name:before {
                content: '';
                display: block;
            }
            .value {
                zoom: 1;
                color: #333;
                width: 285px;
                float: left;
                position: relative;
                word-break: break-all;
            }
            }
        }
    }
    .cmn-clearfix:after {
        content: '\0020';
        display: block;
        height: 0;
        font-size: 0;
        clear: both;
        overflow: hidden;
        visibility: hidden;
    }   
  }
</style>
