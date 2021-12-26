<template>
  <!-- <h1>home page</h1> -->
  <el-container>
    <el-aside width="200px" style="background-color: blue">
      <el-menu :default-openeds="['1']">
        <!-- <el-submenu index="1">
          <template>
            <i class="el-icon-s-home"></i>
            Home
          </template>
          <el-menu-item-group>
            <el-menu-item>test1</el-menu-item>
          </el-menu-item-group>
        </el-submenu> -->
        <el-menu-item-group v-for="(item, i) in menuList" v-bind:key="i">
          <el-menu-item><i :class="item.icon"></i>{{ item.name }}</el-menu-item>
        </el-menu-item-group>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background-color: grey">
          
      </el-header>
      <el-main class="el-main-zone">
        <div>
          <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrump-item :to="{ path: '/' }">home</el-breadcrump-item>
            <el-breadcrumb-item>活动管理</el-breadcrumb-item>
            <el-breadcrumb-item>活动列表</el-breadcrumb-item>
            <el-breadcrumb-item>活动详情</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      menuList: [
        {
          name: "Home",
          icon: "el-icon-s-home",
        },
        {
          name: "UI_TEST",
          icon: "el-icon-table-lamp",
        },
        {
          name: "Interface",
          icon: "el-icon-s-shop",
        },
        {
          name: "Performance",
          icon: "el-icon-cpu",
        },
      ],
    };
  },
};
</script>

<style scoped>
.el-main-zone{
    background-color: rgb(64, 155, 197);
}
</style>