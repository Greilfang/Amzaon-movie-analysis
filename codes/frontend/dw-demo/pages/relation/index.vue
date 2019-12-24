<template>
  <div>
    <div class="title"><h2>搜索条件</h2></div>
    <div class="select_words">
      <div style="padding: 20px">
        <el-form :inline="true">
          <el-form-item label="查询条件1:">
            <el-input placeholder="请输入名字,支持模糊查询" v-model="name" class="input-with-select" style="width: 300px">
              <el-select v-model="role1" slot="prepend" style="width: 80px">
                <el-option label="导演" value="director"></el-option>
                <el-option label="演员" value="actor"></el-option>
              </el-select>
            </el-input>
          </el-form-item>
          <br>
          <el-form-item label="查询条件2:">
            <el-select v-model="role2" style="width: 150px">
              <el-option v-if="role1 !== 'director'" label="导演" value="director"></el-option>
              <el-option label="演员" value="actor"></el-option>
            </el-select>
          </el-form-item>
          <br>
          <el-form-item label="查询范围:">
            <el-input-number v-model="num" :min="1" style="width: 150px; margin-left: 10px"></el-input-number>
          </el-form-item>
          <el-button icon="el-icon-search" circle style="margin-left: 100px" @click="loadData"></el-button>
        </el-form>
      </div>
    </div>
    <div class="title"><h2>查询结果</h2></div>
    <div class="results">
      <div style="padding: 20px">
        <div v-text="result" class="italy"></div>
        <div id="myChart" :style="{width: '1200px', height: '600px'}"></div>
      </div>
    </div>
  </div>
</template>

<script>
    import echarts from 'echarts'
    import relationApi from "@/api/relation";

    export default {
        name: "index",
        data() {
            return {
                chart: null,
                role1: "director",
                role2: "actor",
                name: null,
                num: 10,
                result: "查询结果",
            }
        },
        mounted() {
            this.drawChart();
        },
        methods: {
            drawChart() {
                // 基于准备好的dom，初始化echarts实例
                this.chart = echarts.init(document.getElementById('myChart'))
                let option = {
                    title: {
                        text: '关系图',
                        top: 'bottom',
                        left: 'right'
                    },
                    tooltip: {
                        formatter: function (param) {
                            if (param.dataType === 'edge') {
                                return param.data.desc;
                            }
                            return param.data.name;
                        }
                    },
                    animationDuration: 1500,
                    animationEasingUpdate: 'quinticInOut',
                };
                this.chart.setOption(option);
            },
            loadData() {
                this.chart.showLoading();
                let _this = this;
                relationApi.getRelations({"role":this.role1,"name":this.name,"target":this.role2,"top_nums":this.num}).then(res=>{
                    _this.result = "共查询到" + res.data.meta.amount +"名演员/导演,共用时" + (res.data.meta.duration * 1000).toFixed(2) + "ms";
                    let categories = res.data.data.category;
                    let links = res.data.data.links;
                    let nodes = res.data.data.nodes;
                    nodes.forEach(function (node) {
                        // node.id = index;
                        // index ++;
                        if (node.category === "key_2") {
                            node.symbolSize = 40
                        } else {
                            node.symbolSize = 60
                        }
                    });

                    links.forEach(function (edge) {
                        // edge.id = index;
                        // index ++;
                       edge.desc = edge.description.join(" | ")
                    });
                    let m_legend = [{
                        // selectedMode: 'single',
                        data: ["key_2"]
                    }];
                    if(categories.length < 15){
                        m_legend = [{
                            // selectedMode: 'single',
                            data: categories.map(function (a) {
                                return a.name;
                            })
                        }]
                    }
                    let option = {
                        legend: m_legend,
                        series: [
                            {
                                type: 'graph',
                                layout: 'force',
                                data: nodes,
                                links: links,
                                categories: categories,
                                roam: true,
                                draggable: true,
                                focusNodeAdjacency: true,
                                itemStyle: {
                                    normal: {
                                        borderColor: '#fff',
                                        borderWidth: 1,
                                        shadowBlur: 10,
                                        shadowColor: 'rgba(0, 0, 0, 0.3)',

                                    }
                                },
                                label: {
                                    normal: {
                                        show: true,                 // 是否显示标签
                                        position: "inside",         // 标签位置:'top''left''right''bottom''inside''insideLeft''insideRight''insideTop''insideBottom''insideTopLeft''insideBottomLeft''insideTopRight''insideBottomRight'
                                        textStyle: {                // 文本样式
                                            fontSize: 10
                                        }
                                    }

                                },
                                lineStyle: {
                                    color: 'source',
                                    width: 5,
                                    curveness: 0.3
                                },
                                force: {
                                    repulsion: 2500,
                                    edgeLength: [10, 50]
                                },
                                emphasis: {
                                    lineStyle: {
                                        width: 10
                                    }
                                },
                            }
                        ]
                    };
                    _this.chart.setOption(option);
                    _this.chart.hideLoading();

                });
            },
        }
    }
</script>

<style scoped>
  .title {
    margin-top: 40px;
    margin-bottom: 20px;
    margin-left: -20px;
  }

  .select_words {
    margin-left: -20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }

  .select_words .el-input, .el-textarea {

  }

  .results {
    margin-left: -20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }

  .italy {
    font-family: "PingFang SC", cursive;
    margin-bottom: 40px;
    margin-top: 5px;
    margin-left: 5px
  }
</style>
