<template>
  <div id="login-page">
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
          <el-input v-model="password" style="width: 200px" show-password></el-input>
        </el-form-item>
        <!-- <el-button type="primary">登录</el-button> -->
        <el-form-item>
          <el-button @click="login" type="primary">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
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
      username: "admin",
      password: "123456",
    };
  },
  methods: {
    login() {
      if (this.username === "admin" && this.password === "123456") {
        this.$router.push("/home");
      } else {
        alert("用户名或密码错误");
      }
    },
  },
};
</script>

<style>
#login-page {
  /* font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px; */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgb(63, 160, 216);
}
.login-div {
  margin: auto;
  position: relative;
  top: 30%;
  /* display: flex; */

  /* padding: 100%; */
}

.login-form {
  /* margin: auto; */

  /* padding: 70px 0;

  text-align: center; */
}
</style>

