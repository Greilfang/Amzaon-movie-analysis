<template>
  <div>
    <div class="title"><h2>搜索条件</h2></div>
    <div class="select_words">
      <el-form :inline="true" :label-position="left" style="padding: 20px" >
        <el-form-item label="电影名称">
          <el-input
            v-model="form.movie_name" placeholder="请输入电影名称,支持模糊搜索" clearable></el-input>
        </el-form-item>
        <br>
        <el-form-item label="导演姓名">
          <el-input
            type="textarea" v-model="form.director" placeholder="请输入导演名,支持模糊搜索" clearable
            autosize></el-input>
        </el-form-item>
        <br>
        <el-form-item label="演员姓名">
          <el-input
            type="textarea" v-model="form.actor" placeholder="请输入演员名,支持模糊搜索" autosize clearable></el-input>
        </el-form-item>
        <br>
        <el-form-item label="电影介绍">
          <el-input
            type="textarea" v-model="form.intro" placeholder="请输入电影介绍,支持模糊搜索" autosize clearable></el-input>
        </el-form-item>
        <br>
        <el-form-item label="年份筛选">
          <el-col :span="10">
            <el-date-picker type="year" placeholder="选择开始年份" v-model="form.start_from"
                            style="width: 80%;"></el-date-picker>
          </el-col>
          <el-col class="line" :span="2" style="text-align: center">-</el-col>
          <el-col :span="10">
            <el-date-picker type="year" placeholder="选择截止年份" v-model="form.end_until"
                            style="width: 80%;"></el-date-picker>
          </el-col>
        </el-form-item>
        <br>
        <el-form-item label="评分筛选" style="text-align: center;">
          <el-col :span="8" style="padding-top: 10px;margin-left: -20px">
            <el-rate v-model="form.score_from" allow-half style="width: 200px" show-score></el-rate>
          </el-col>
          <el-col class="line" :span="8" style="padding-left: 20px">-</el-col>
          <el-col :span="8" style="padding-top: 10px;margin-left: -20px">
            <el-rate v-model="form.score_to" allow-half style="width: 200px" show-score></el-rate>
          </el-col>
        </el-form-item>
        <br>
        <el-form-item label="电影类别">
          <template>
            <el-select v-model="form.genre" filterable placeholder="请选择电影类别">
              <el-option
                v-for="item in genre_list"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                <span style="float: left">{{ item.label }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.value }}</span>
              </el-option>
            </el-select>
          </template>
        </el-form-item>
        <br>
        <el-form-item label="情感倾向">
          <el-radio-group v-model="form.emotion" size="medium">
            <el-radio-button label="good" ></el-radio-button>
            <el-radio-button label="bad"></el-radio-button>
            <el-radio-button label="none"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <br>
        <el-switch
          v-model="brief"
          active-text="简略模式"
          inactive-text="详情模式">
        </el-switch>
        <el-button type="primary" icon="el-icon-search" style="margin-left: 5%" @click="getData">搜索</el-button>
        <el-button type="info" icon="el-icon-refresh" @click="resetInput">重置</el-button>
      </el-form>
    </div>
    <div class="title"><h2>查询结果</h2></div>
    <div class="results">
      <div style="padding:20px">
        <div v-text="result" class="italy"></div>
        <el-table :data="films.slice((curPage - 1) * curSize, curPage * curSize)" header-cell-style="background-color: rgb(245, 247, 249); text-align: center" stripe v-loading="loading">
          <el-table-column align="center" prop="ID" label="电影ID"></el-table-column>
          <el-table-column align="center" show-overflow-tooltip prop="Title" label="电影名"></el-table-column>
          <el-table-column v-if="brief === false" align="center" show-overflow-tooltip prop="Intro" label="电影介绍"></el-table-column>
          <el-table-column align="center" prop="Year" label="上映年份"></el-table-column>
          <el-table-column align="center" label="评分" key="1">
            <template slot-scope="scope">
              <el-rate
                v-model="scope.row.Score"
                disabled
                show-score
                text-color="#ff9900"
                score-template="{value}">
              </el-rate>
            </template>
          </el-table-column>
          <el-table-column v-if="brief === false" align="center" show-overflow-tooltip prop="Director" label="导演"></el-table-column>
          <el-table-column v-if="brief === false" align="center" show-overflow-tooltip prop="Actor" label="演员"></el-table-column>
        </el-table>
        <div class="block" style="margin-top: 10px;margin-left: 10px">
          <el-pagination
            layout="total, prev, pager, next"
            :total="films.length"
            @current-change="handleCurrentChange">
          </el-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import commonApi from "@/api/common";
    export default {
        name: "index",
        data() {
            return {
                genre_list: [
                    {
                    value:'Drama',
                    label:'戏剧'
                },{
                        value:'Suspense',
                        label:'悬疑'
                },{
                        value:'Comedy',
                        label:'喜剧'
                    },{
                        value:'Action',
                        label:'动作'
                    },{
                        value:'Adventure',
                        label:'冒险'
                    },{
                        value:'Science Fiction',
                        label:'科幻'
                    },{
                        value:'Fantasy',
                        label:'幻想'
                    },{
                        value:'Kids',
                        label:'儿童'
                    },{
                        value:'Sports',
                        label:'体育'
                    },{
                        value:'Special Interest',
                        label:'悬疑'
                    },{
                        value:'Documentary',
                        label:'纪录片'
                    },{
                        value:'Arts, Entertainment, and Culture',
                        label:'艺术,娱乐,文化'
                    },{
                        value:'Military and War',
                        label:'军事与战争'
                    },{
                        value:'Western',
                        label:'西部'
                    },{
                        value:'Horror',
                        label:'惊悚'
                    },{
                        value:'Animation',
                        label:'动画'
                    },{
                        value:'Music Videos and Concerts',
                        label:'音乐录影带与音乐会'
                    },{
                        value:'Arthouse',
                        label:'艺术屋'
                    },{
                        value:'International',
                        label:'国际'
                    },{
                        value:'Historical',
                        label:'历史'
                    },{
                        value:'Romance',
                        label:'爱情'
                    },{
                        value:'Young Adult Audience',
                        label:'校园青春'
                    },{
                        value:'LGBTQ',
                        label:'LGBTQ'
                    },{
                        value:'Anime',
                        label:'日本动漫'
                    },{
                        value:'Faith and Spirituality',
                        label:'宗教'
                    },{
                        value:'Fitness',
                        label:'健康'
                    },{
                        value:'Talk Show and Variety',
                        label:'脱口秀和综艺'
                    },{
                        value:'Erotic',
                        label:'情色片'
                    }],
                form: {
                    director: "",
                    actor: "",
                    intro: "",
                    movie_name: "",
                    start_from: null,
                    end_until: null,
                    score_from: 0,
                    score_to: 5,
                    genre: null,
                    emotion: null
                },
                brief:false,
                result:"查询信息",
                films:[],
                curPage:1,
                curSize:10,
                loading: false
            }
        },
        created(){
            this.resetInput();

        },
        methods:{
            resetInput(){
                this.form.director = "";
                this.form.actor = "";
                this.form.intro = "";
                this.form.movie_name = "";
                this.form.start_from = "";
                this.form.end_until = "";
                this.form.score_from=0;
                this.form.score_to=5;
                this.form.genre="";
                this.form.emotion="";

            },
            handleCurrentChange(val) {
                this.curPage = val;
            },
            getData(){
                this.loading = true;
                //pre format
                if (this.form.director !== ""){
                    let str = this.form.director
                    this.form.director = str.search("|") !== -1? str.split("|") : [str]
                }
                if (this.form.actor !== ""){
                    let str = this.form.actor
                    this.form.actor = str.search("|") !== -1? str.split("|") : [str]
                }
                if(this.form.start_from !== ""){
                    this.form.start_from = this.form.start_from.toString().split(" ")[3]
                }
                if(this.form.end_until !== ""){
                    this.form.end_until = this.form.end_until.toString().split(" ")[3]
                }
                if (this.brief){
                    commonApi.getBriefList(this.form).then(res=>{
                        this.films = res.data.data;
                        let str = "共查询到"+ res.data.meta.amount.toString()
                            + "条数据,共用时"+ (res.data.meta.duration * 1000).toFixed(2)
                            + "ms";
                        if(res.data.meta.mongotime){
                            str+=",其中mongodb用时" +  (res.data.meta.mongotime * 1000).toFixed(2) + "ms";
                        }
                        this.result = str;
                        if (res.data.flag){
                            this.$message({
                                type:"success",
                                message:"查询成功"
                            })
                        }
                        this.loading = false;
                    })
                }else {
                    commonApi.getDetailList(this.form).then(res=>{
                        this.films = res.data.data;
                        let str = "共查询到"+ res.data.meta.amount.toString()
                            + "条数据,共用时"+ (res.data.meta.duration * 1000).toFixed(2)
                            + "ms";
                        if(res.data.meta.mongotime){
                            str+=",其中mongodb用时" +  (res.data.meta.mongotime * 1000).toFixed(2) + "ms";
                        }
                        this.result = str;
                        if (res.data.flag){
                            this.$message({
                                type:"success",
                                message:"查询成功"
                            })
                        }
                        this.loading = false;
                    })
                }
            }
        }
    }
</script>

<style scoped>
  .select_words{
    margin-left: -20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }
  .select_words .el-input, .el-textarea {
    width: 400px;
  }
.results{
  margin-left: -20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
  .title {
    margin-top: 40px;
    margin-bottom: 20px;
    margin-left: -20px;
  }

  .line {
    text-align: center;
  }
  .italy {font-family: "PingFang SC",cursive;margin-bottom: 40px;margin-top: 5px;margin-left: 5px}
</style>
