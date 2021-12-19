<template>
  <div id="app">
    <!-- <img src="./assets/logo.png"> -->
    <router-view/>
  </div>
  <!-- <div id="app">
    <div class="login-div">
      <el-form
        class="login-form"
        ref="form"
        style="text-align: center"
        label-width="70px"
        @submit.prevent="login"
      >
        <h1 style="text-align: center">自动化测试平台</h1>
        <br />
        <el-row>
          <el-form-item
            label="用户名："
            style="display: inline-block; font-weight: bold"
          >
            <el-input
              v-model="username"
              style="width: 200px"
              placeholder="admin"
            ></el-input>
          </el-form-item>
        </el-row>

        <el-form-item
          label="密码："
          style="display: inline-block; font-weight: bold"
        >
          <el-input v-model="password" style="width: 200px"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="login" type="primary">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div> -->
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      form: {
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: "",
      },
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      if (this.username === "admin" && this.password === "123456") {
        this.$router.push("/");
      } else {
        alert("用户名或密码错误");
      }
    },
  },
};
</script>

<style>
#app {
  /* font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px; */
}
</style>
