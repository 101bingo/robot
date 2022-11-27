"use strict";(self["webpackChunkmonitor_vue_h5"]=self["webpackChunkmonitor_vue_h5"]||[]).push([[447],{3447:function(t,e,a){a.r(e),a.d(e,{default:function(){return b}});var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"login-container"},[e("van-nav-bar",{attrs:{title:"历史数据"}}),e("van-tabs",{attrs:{type:"line"},on:{click:t.onClickHoursData},model:{value:t.active,callback:function(e){t.active=e},expression:"active"}},[e("van-tab",{attrs:{title:"1小时"}}),e("van-tab",{attrs:{title:"6小时"}}),e("van-tab",{attrs:{title:"12小时"}}),e("van-tab",{attrs:{title:"自定义"}},[e("van-cell",{attrs:{title:"选择日期区间",value:t.canlendarData},on:{click:function(e){t.isShowCalendar=!0}}}),e("van-calendar",{attrs:{type:"range","allow-same-day":"","min-date":t.startMin,"max-date":new Date},on:{confirm:t.onConfirm},model:{value:t.isShowCalendar,callback:function(e){t.isShowCalendar=e},expression:"isShowCalendar"}})],1)],1),e("LineChart",{attrs:{testData11:t.testresponse,temperData:t.tempratureData,height:t.calculateHeight},on:{temperChange:t.updateTemp}})],1)},n=[],r=function(){var t=this,e=t._self._c;return e("div",{class:t.className,style:{height:t.height,width:t.width}})},s=[],o=(a(7658),a(3139)),d=a(2325),l={data(){return{$_sidebarElm:null,$_resizeHandler:null}},mounted(){this.$_resizeHandler=(0,d.Ds)((()=>{this.chart&&this.chart.resize()}),100),this.$_initResizeEvent(),this.$_initSidebarResizeEvent()},beforeDestroy(){this.$_destroyResizeEvent(),this.$_destroySidebarResizeEvent()},activated(){this.$_initResizeEvent(),this.$_initSidebarResizeEvent()},deactivated(){this.$_destroyResizeEvent(),this.$_destroySidebarResizeEvent()},methods:{$_initResizeEvent(){window.addEventListener("resize",this.$_resizeHandler)},$_destroyResizeEvent(){window.removeEventListener("resize",this.$_resizeHandler)},$_sidebarResizeHandler(t){"width"===t.propertyName&&this.$_resizeHandler()},$_initSidebarResizeEvent(){this.$_sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.$_sidebarElm&&this.$_sidebarElm.addEventListener("transitionend",this.$_sidebarResizeHandler)},$_destroySidebarResizeEvent(){this.$_sidebarElm&&this.$_sidebarElm.removeEventListener("transitionend",this.$_sidebarResizeHandler)}}};a(3630);let h=new Date(1997,9,3),m=1e3*Math.random();var u={mixins:[l],props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"600px"},autoResize:{type:Boolean,default:!0},testData11:{type:Array,default:[["2022-11-09 17:54:43",11],["2022-11-09 17:56:43",13]]},temperData:{type:Array,default:[["2022-11-09 17:54:43",11],["2022-11-09 17:56:43",13]]}},data(){return{chart:null,testData:[]}},computed:{livedOxygenLimit(){return this.$store.state.oxygenLimit}},watch:{testData11:{handler(t){this.chart.setOption({series:[{name:"溶氧",data:t}]})}},temperData:{handler(t){this.chart.setOption({series:[{name:"温度",data:t}]})}},livedOxygenLimit:{handler(t){console.log("oxygenLimit:",t),this.setOptions()}}},mounted(){this.$nextTick((()=>{this.initChart()}))},beforeDestroy(){this.chart&&(this.chart.dispose(),this.chart=null,clearInterval(this.dataTimer))},methods:{initChart(){this.chart=o.init(this.$el,"macarons"),this.setOptions()},setOptions(){this.chart.setOption({xAxis:[{type:"time",boundaryGap:!1,axisLabel:{align:"center",formatter:function(t,e){let a=new Date(t),i=(a.getMinutes().toString().padStart(2,"0"),a.getHours().toString().padStart(2,"0")),n=a.getMinutes().toString().padStart(2,"0");a.getSeconds().toString().padStart(2,"0");var r=[i,n];return r.join(":")}},splitLine:{show:!1}},{gridIndex:1,type:"time",boundaryGap:!1,axisLine:{onZero:!0},position:"bottom"}],grid:[{left:30,right:20,height:"50%"},{left:30,right:20,top:"65%",bottom:20,height:"35%"}],axisPointer:{link:[{xAxisIndex:"all"}]},dataZoom:[{show:!1,realtime:!0,xAxisIndex:[0,1]},{type:"inside",realtime:!0,xAxisIndex:[0,1]}],toolbox:{feature:{dataZoom:{yAxisIndex:"none"},restore:{},saveAsImage:{}}},tooltip:{trigger:"axis",backgroundColor:"#D38359",formatter:function(t){let e=0===t[0].axisIndex?t[0]:t[1],a=1===t[0].axisIndex?t[0]:t[1];return e.data[0]+"<br>"+e.marker+e.seriesName+"&emsp;&emsp;"+e.data[1]+"<br>"+a.marker+a.seriesName+"&emsp;&emsp;"+a.data[1]},axisPointer:{animation:!1},padding:[5,10]},yAxis:[{name:"溶氧",type:"value",boundaryGap:!1,axisTick:{show:!1}},{name:"温度",type:"value",gridIndex:1}],legend:{data:["溶氧","温度"]},series:[{name:"溶氧",markLine:{data:[{name:"阈值",yAxis:this.livedOxygenLimit,label:{show:"true",position:"middle",formatter:`溶氧红线${this.livedOxygenLimit}`,fontSize:20},lineStyle:{normal:{width:2,color:"#FF5D1D"}}}]},itemStyle:{normal:{color:"#64EDE0",lineStyle:{color:"#FF005A",width:2}}},smooth:!0,areaStyle:{},type:"line",data:this.testData11,animationEasing:"cubicInOut"},{name:"温度",type:"line",xAxisIndex:1,yAxisIndex:1,data:this.temperData,itemStyle:{normal:{color:"#8ACF62"}}}]})},createData(){let t=this;t.dataTimer=setInterval((()=>{t.testData.shift(),t.testData.push(t.randomData()),t.chart.setOption({series:[{data:t.testData}]})}),1e3)},randomData(){return h=new Date,m=m+21*Math.random()-10,this.$emit("temperChange",Math.round(m)),console.log("name:",h.toString()),{name:h.toString(),value:[[h.getFullYear(),h.getMonth(),h.getDate()].join("/")+" "+h.getHours()+":"+h.getMinutes().toString().padStart(2,"0")+":"+h.getSeconds().toString().padStart(2,"0"),Math.round(m)]}}}},c=u,p=a(1001),g=(0,p.Z)(c,r,s,!1,null,null,null),v=g.exports,y=a(586),x={name:"HomePage",components:{LineChart:v},data(){return{ischecked:!1,active:0,oxygenData:0,temprature:0,isShowCalendar:!1,canlendarData:"",testresponse:[],tempratureData:[],startMin:this.setStartMin(),loadFlag:!1}},computed:{calculateHeight:function(){let t=window.screen.height-46-48-50-40;return`${t}px`}},watch:{$route:{handler:function(t){this.redirect=t.query&&t.query.redirect},immediate:!0}},methods:{showPwd(){"password"===this.passwordType?this.passwordType="":this.passwordType="password",this.$nextTick((()=>{this.$refs.password.focus()}))},setStartMin(){var t=new Date;return new Date(t.getFullYear(),t.getMonth()-6,t.getDate())},endMax(){var t=new Date;return new Date(t.getFullYear(),t.getMonth()+6,t.getDate())},updateTemp(t){this.temprature=t},updateOxygen(t){this.oxygenData=t},formatDate(t){return`${t.getMonth()+1}/${t.getDate()}`},onConfirm(t){const[e,a]=t;let i=new Date(a.getFullYear(),a.getMonth(),a.getDate()+1);this.isShowCalendar=!1,this.canlendarData=`${this.formatDate(e)} - ${this.formatDate(a)}`,new Promise(((t,a)=>{(0,y.Vb)(e.valueOf()/1e3,i.valueOf()/1e3).then((t=>{const{data:e}=t;this.testresponse=e[0],this.tempratureData=e[1]}))}))},onClickHoursData(t,e){let a=1;switch(e){case"1小时":a=1;break;case"6小时":a=6;break;case"12小时":a=12;break;default:a=24;break}new Promise(((t,e)=>{(0,y._R)(a).then((t=>{const{data:e}=t;this.testresponse=e[0],this.tempratureData=e[1]}))}))}}},D=x,w=(0,p.Z)(D,i,n,!1,null,"495cd424",null),b=w.exports}}]);
//# sourceMappingURL=447.92c9b1b7.js.map