<template>
  <!-- <span>test</span> -->
  <el-table :data="tableData" border :row-class-name="tableRowClassName">
    <el-table-column type="expand">
      <template slot-scope="props">
        <el-form>
          <el-form-item
            v-for="(kwd, index) in props.row.address"
            :key="index"
            inline
          >
            <el-button type="primary">{{ index }}</el-button>
            <el-button>{{ kwd }}</el-button>
            <!-- <span> {{ kwd }}</span> -->
          </el-form-item>
        </el-form>
      </template>
    </el-table-column>
    <el-table-column
      prop="date"
      label="时间"
      width="180"
      header-align="center"
    ></el-table-column>
    <el-table-column
      prop="id"
      label="事件ID"
      width="180"
      header-align="center"
      align="center"
    ></el-table-column>
    <el-table-column
      prop="name"
      label="事件名称"
      width="180"
      header-align="center"
      align="center"
    ></el-table-column>
    <el-table-column
      prop="expendWords"
      label="扩展字段"
      header-align="center"
      align="center"
    ></el-table-column>
  </el-table>
</template>

<script>
// import { validUsername } from "@/utils/validate";

export default {
  name: "LiveTableDataa",
  data() {
    return {
      tableData: [],
      eventDict: [
        {
          id: "P1026012",
          desc: "我的页面",
          address: {
            pageId: 12345,
            sessionId: "heisidfhiezoqb584671235",
            souceId: 9527,
          },
          expendWords:
            "pageId: 12345,sessionId: heisidfhiezoqb584671235,souceId:9527",
        },
        {
          id: "C102601",
          desc: "点击我的按钮",
          address: {
            pageId: 676436,
            sessionId: "jueqidkeiadsdf584671235",
            souceId: 9528,
          },
          expendWords:
            "pageId: 676436,sessionId: jueqidkeiadsdf584671235,souceId:9528",
        },
        {
          id: "CE1026012",
          desc: "我的页面曝光",
          address: {
            pageId: 12345,
            sessionId: "heisidfhiezoqb584671235",
            souceId: 9527,
            position: 1,
            type: "page01",
          },
          expendWords:
            "pageId: 12345,sessionId: 87912,souceId:9527,position:1,type:page01",
        },
        {
          id: "C102603",
          desc: "小视频播放按钮点击",
          address: {
            pageId: 58458,
            sessionId: "sdjfwoejfoasdsdf584671235",
            souceId: 8527,
            position: 9,
            type: "video",
          },
          expendWords:
            "pageId: 58458,sessionId: sdjfwoejfoasdsdf584671235,souceId:8527,position:9,type:video",
        },
        {
          id: "P102603",
          desc: "小视频播放页面",
          address: {
            pageId: 38465,
            sessionId: "weasdfwjijiowe584671235",
            souceId: 7527,
            position: 5,
            type: "video",
          },
          expendWords:
            "pageId: 38465,sessionId: weasdfwjijiowe584671235,souceId:7527,position:5,type:video",
        },
        {
          id: "CE102604",
          desc: "视频列表曝光",
          address: {
            pageId: 58465,
            sessionId: "weasdfwjijiowe584671235",
            souceId: 9527,
            position: 5,
            type: "video",
          },
          expendWords:
            "pageId: 58465,sessionId: weasdfwjijiowe584671235,souceId:9522,position:5,type:video",
        },
        {
          id: "C201201",
          desc: "收藏按钮点击",
          address: {
            pageId: 827382,
            sessionId: "dfasewefasdiijiw584671235",
            souceId: 5846,
            type: "btn",
          },
          expendWords:
            "pageId: 827382,sessionId: dfasewefasdiijiw584671235,souceId:5846,type:btn",
        },
      ],
    };
  },
  // watch: {
  //   $route: {
  //     handler: function (route) {
  //       this.redirect = route.query && route.query.redirect;
  //     },
  //     immediate: true,
  //   },
  // },
  mounted() {
    //在mounted 声明周期中创建定时器
    const timer = setInterval(() => {
      // 这里调用调用需要执行的方法，由于特殊的需求它将用来区分，定时器调用和手工调用，然后执行不同的业务逻辑
      this.createTableData();
    }, 2000); // 每两秒执行1次
    // 通过$once来监听定时器，在beforeDestroy钩子可以被清除
    this.$once("hook:beforeDestroy", () => {
      // 在页面销毁时，销毁定时器
      clearInterval(timer);
    });
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (row.id === "undefined") {
        return;
      }
      if (row.id.startsWith("CE")) {
        return "expose-row";
      } else if (row.id.startsWith("C")) {
        return "click-row";
      } else if (row.id.startsWith("P")) {
        return "page-row";
      } else {
        return "";
      }
    },

    createTableData() {
      if (this.tableData === "undefined") {
        return;
      }
      while (this.tableData.length > 15) {
        this.tableData.shift();
      }
      let localDate = new Date();
      let nowTime = localDate.toLocaleString().replace("/", "-");
      let evnetId =
        this.eventDict[Math.floor(Math.random() * this.eventDict.length)];
      let temp = {
        id: evnetId.id,
        date: nowTime,
        name: evnetId.desc,
        address: evnetId.address,
        expendWords: evnetId.expendWords,
      };
      this.tableData.push(temp);
    },
  },
};
</script>

<style>
.el-table .expose-row {
  background: coral;
}
.el-table .click-row {
  background-color: cyan;
}
.el-table .page-row {
  background-color: chartreuse;
}
</style>
