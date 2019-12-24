<template>
  <div id="app">
    <el-container>
            <el-header>
              <template>
                <div class="m_title">
                <i class="el-icon-data-analysis" style="color: black"></i>
                  <i style="color: black">数据仓库</i>
                </div>
              </template>
              <hr style="color:black;box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)">
            </el-header>
            <el-container>
              <el-aside width="200px" >
                <el-menu  active-text-color="#ffd04b" default-active="1">
                  <el-submenu index="1">
                    <template slot="title"><nuxt-link to="/common"><i class="el-icon-search"></i>普通查询</nuxt-link></template>
                  </el-submenu>
                  <el-submenu index="2">
                    <template slot="title"><nuxt-link to="/relation"><i class="el-icon-user"></i>关系查询</nuxt-link></template>
                  </el-submenu>
                  <el-submenu index="3">
                    <template slot="title"><nuxt-link to="about"><i class="el-icon-message"></i>团队介绍</nuxt-link></template>
                  </el-submenu>
                </el-menu>
              </el-aside>
              <div class="main" style="width: 100%"><nuxt /></div>

            </el-container>
    </el-container>
  </div>
</template>

<style>
html {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}
#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 90%;
  height: 100%;
  margin-left: 5%;
  margin-right: 5%;

}
.el-container>.el-aside {
  height:100vh;
}

  .m_title{
    font-size: 40px
  }

.el-header{
  /*background-color: #B3C0D1;*/
  /*color: #333;*/
  /*text-align: center;*/
  /*line-height: 60px;*/
    line-height: 60px;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 10px;
}
.main{
  margin-left: 40px;
  margin-bottom: 40px;
}
.el-aside {
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
  .el-submenu{
    margin-top: 20px;
  }
.nuxt-link-exact-active,.nuxt-link-active{
  color: #409EFF;
}
a{
  color:black ;
}
  a:link{
    color: #409EFF;
  }
a:active{
  color: #409EFF;
}
</style>
