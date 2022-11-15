(function(){"use strict";var e={5033:function(e,t,n){n.r(t),n.d(t,{default:function(){return w}});var r=function(){var e=this,t=e._self._c;return t("div",{staticClass:"login-container"},[t("van-nav-bar",{attrs:{title:"首页--实时数据","left-text":"返回","left-arrow":""},scopedSlots:e._u([{key:"right",fn:function(){return[t("van-icon",{attrs:{name:"search",size:"18"}})]},proxy:!0}])}),t("van-cell-group",{attrs:{inset:""}},[t("van-field",{attrs:{label:"溶氧：",placeholder:"0","label-align":"right","input-align":"center"},model:{value:e.oxygenData,callback:function(t){e.oxygenData=t},expression:"oxygenData"}}),t("van-field",{attrs:{label:"温度：",placeholder:"0","label-align":"right","input-align":"center"},model:{value:e.temprature,callback:function(t){e.temprature=t},expression:"temprature"}})],1),t("LineChart",{attrs:{testData11:e.testresponse},on:{temperChange:e.updateTemp}})],1)},o=[],i=(n(7658),function(){var e=this,t=e._self._c;return t("div",{class:e.className,style:{height:e.height,width:e.width}})}),a=[],s=n(3139),l=n(2325),u={data(){return{$_sidebarElm:null,$_resizeHandler:null}},mounted(){this.$_resizeHandler=(0,l.Ds)((()=>{this.chart&&this.chart.resize()}),100),this.$_initResizeEvent(),this.$_initSidebarResizeEvent()},beforeDestroy(){this.$_destroyResizeEvent(),this.$_destroySidebarResizeEvent()},activated(){this.$_initResizeEvent(),this.$_initSidebarResizeEvent()},deactivated(){this.$_destroyResizeEvent(),this.$_destroySidebarResizeEvent()},methods:{$_initResizeEvent(){window.addEventListener("resize",this.$_resizeHandler)},$_destroyResizeEvent(){window.removeEventListener("resize",this.$_resizeHandler)},$_sidebarResizeHandler(e){"width"===e.propertyName&&this.$_resizeHandler()},$_initSidebarResizeEvent(){this.$_sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.$_sidebarElm&&this.$_sidebarElm.addEventListener("transitionend",this.$_sidebarResizeHandler)},$_destroySidebarResizeEvent(){this.$_sidebarElm&&this.$_sidebarElm.removeEventListener("transitionend",this.$_sidebarResizeHandler)}}};n(3630);let c=new Date(1997,9,3),d=1e3*Math.random();var h={mixins:[u],props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"550px"},autoResize:{type:Boolean,default:!0},testData11:{type:Array,default:[["2022-11-09 17:54:43",11],["2022-11-09 17:56:43",13]]}},data(){return{chart:null,testData:[]}},watch:{testData11:{handler(e){this.chart.setOption({series:[{data:e}]})}}},mounted(){this.height=window.screen.height/2+"px",this.$nextTick((()=>{this.initChart()}))},beforeDestroy(){this.chart&&(this.chart.dispose(),this.chart=null,clearInterval(this.dataTimer))},methods:{initChart(){this.chart=s.init(this.$el,"macarons"),this.setOptions()},setOptions(){this.chart.setOption({xAxis:{type:"time",boundaryGap:!1,axisLabel:{align:"center",formatter:function(e,t){let n=new Date(e),r=n.getMinutes().toString().padStart(2,"0"),o=n.getSeconds().toString().padStart(2,"0");var i=[r,o];return i.join(":")}},splitLine:{show:!1}},grid:{left:10,right:10,bottom:20,top:30,containLabel:!0},tooltip:{trigger:"axis",backgroundColor:"#00A1F1",formatter:function(e){return console.log("params:",e),console.log("params.value[0]->:",e.value[0]),date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+" "+date.getHours()+":"+date.getMinutes().toString().padStart(2,"0")+":"+date.getSeconds().toString().padStart(2,"0")+" -> "+e.value[1]},axisPointer:{animation:!1},padding:[5,10]},yAxis:{type:"value",axisTick:{show:!1}},legend:{data:["expected"]},dataZoom:{type:"inside"},series:[{name:"expected",markLine:{data:[{name:"阈值",yAxis:3,label:{show:"true",position:"middle",formatter:"溶氧红线：3",color:"inherit",fontSize:20,fontWeight:"bold"},lineStyle:{normal:{width:2,color:"#FF5D1D"}}}]},itemStyle:{normal:{color:"#FF005A",lineStyle:{color:"#FF005A",width:2}}},smooth:!0,type:"line",data:this.testData11,animationDuration:2800,animationEasing:"cubicInOut"}]})},createData(){let e=this;e.dataTimer=setInterval((()=>{e.testData.shift(),e.testData.push(e.randomData()),e.chart.setOption({series:[{data:e.testData}]})}),1e3)},randomData(){return c=new Date,d=d+21*Math.random()-10,this.$emit("temperChange",`${Math.round(d)} mg/L`),{name:c.toString(),value:[[c.getFullYear(),c.getMonth(),c.getDate()].join("/")+" "+c.getHours()+":"+c.getMinutes().toString().padStart(2,"0")+":"+c.getSeconds().toString().padStart(2,"0"),Math.round(d)]}}}},p=h,f=n(1001),m=(0,f.Z)(p,i,a,!1,null,null,null),g=m.exports,v={name:"HomePage",components:{LineChart:g},data(){return{ischecked:!1,active:0,oxygenData:"",temprature:"",testresponse:[]}},watch:{$route:{handler:function(e){this.redirect=e.query&&e.query.redirect},immediate:!0}},mounted(){this.openWebSocket()},methods:{showPwd(){"password"===this.passwordType?this.passwordType="":this.passwordType="password",this.$nextTick((()=>{this.$refs.password.focus()}))},updateTemp(e){this.temprature=e},updateOxygen(e){this.oxygenData=e},openWebSocket(){let e=this,t=location.host,n=`ws://${t}/ws`;console.log("websocketUrl:",n),"WebSocket"in window?console.log("您的浏览器支持WebSocket"):console.log("您的浏览器不支持WebSocket");const r=new WebSocket(n);r.onopen=function(e){console.log(new Date),console.log("websocket 已连接"),console.log(n)},r.onerror=function(e){console.log(e)},r.onclose=function(e){console.log(new Date),console.log("websocket 断开连接！")},r.onmessage=function(t){console.log(t.data);let n=t.data,r=JSON.parse(n);e.oxygenData=`${r.oxygen} mg/L`,e.temprature=`${r.temper} ℃`,e.testresponse.push([r.date_time,r.oxygen])},window.onbeforeunload=function(){r.close()}}}},b=v,y=(0,f.Z)(b,r,o,!1,null,"39ae5466",null),w=y.exports},5679:function(e,t,n){var r=n(6369),o=function(){var e=this,t=e._self._c;return t("div",{attrs:{id:"app"}},[t("router-view"),t("van-tabbar",{model:{value:e.active,callback:function(t){e.active=t},expression:"active"}},[t("van-tabbar-item",{attrs:{icon:"home-o"},on:{click:e.onClickHome}},[e._v("首页")]),t("van-tabbar-item",{attrs:{icon:"chart-trending-o"},on:{click:e.onClickHistory}},[e._v("历史数据")]),t("van-tabbar-item",{attrs:{icon:"setting-o"}},[e._v("控制")]),t("van-tabbar-item",{attrs:{icon:"manager-o"}},[e._v("我的")])],1)],1)},i=[],a=(n(7658),n(5033)),s={name:"App",components:{HomePage:a["default"]},data(){return{active:0}},methods:{onClickHome(){this.$router.push({path:"/home"})},onClickHistory(){this.$router.push({path:"/history"})},onClickControl(){this.$router.push({path:"/history"})},onClickMy(){this.$router.push({path:"/history"})}}},l=s,u=n(1001),c=(0,u.Z)(l,o,i,!1,null,null,null),d=c.exports,h=n(2631);r.ZP.use(h.ZP);const p=[{path:"/",name:"Home",component:()=>Promise.resolve().then(n.bind(n,5033))},{path:"/home",name:"Home",component:()=>Promise.resolve().then(n.bind(n,5033))},{path:"/history",name:"History",component:()=>n.e(289).then(n.bind(n,289))}],f=()=>new h.ZP({mode:"history",scrollBehavior:()=>({y:0}),routes:p}),m=f(),g=h.ZP.prototype.push;h.ZP.prototype.push=function(e){return g.call(this,e).catch((e=>e))};var v=m,b=n(3713),y=(n(5110),n(9821)),w=n.n(y);r.ZP.config.productionTip=!1,r.ZP.use(b.ZP);const _=new(w());r.ZP.use(_),new r.ZP({router:v,render:e=>e(d)}).$mount("#app")},2325:function(e,t,n){n.d(t,{Ds:function(){return r}});n(7658);function r(e,t,n){let r,o,i,a,s;const l=function(){const u=+new Date-a;u<t&&u>0?r=setTimeout(l,t-u):(r=null,n||(s=e.apply(i,o),r||(i=o=null)))};return function(...o){i=this,a=+new Date;const u=n&&!r;return r||(r=setTimeout(l,t)),u&&(s=e.apply(i,o),i=o=null),s}}}},t={};function n(r){var o=t[r];if(void 0!==o)return o.exports;var i=t[r]={exports:{}};return e[r].call(i.exports,i,i.exports,n),i.exports}n.m=e,function(){var e=[];n.O=function(t,r,o,i){if(!r){var a=1/0;for(c=0;c<e.length;c++){r=e[c][0],o=e[c][1],i=e[c][2];for(var s=!0,l=0;l<r.length;l++)(!1&i||a>=i)&&Object.keys(n.O).every((function(e){return n.O[e](r[l])}))?r.splice(l--,1):(s=!1,i<a&&(a=i));if(s){e.splice(c--,1);var u=o();void 0!==u&&(t=u)}}return t}i=i||0;for(var c=e.length;c>0&&e[c-1][2]>i;c--)e[c]=e[c-1];e[c]=[r,o,i]}}(),function(){n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,{a:t}),t}}(),function(){n.d=function(e,t){for(var r in t)n.o(t,r)&&!n.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}}(),function(){n.f={},n.e=function(e){return Promise.all(Object.keys(n.f).reduce((function(t,r){return n.f[r](e,t),t}),[]))}}(),function(){n.u=function(e){return"static/js/"+e+".1f94a14c.js"}}(),function(){n.miniCssF=function(e){return"static/css/"+e+".424a8ba7.css"}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={},t="monitor-vue-h5:";n.l=function(r,o,i,a){if(e[r])e[r].push(o);else{var s,l;if(void 0!==i)for(var u=document.getElementsByTagName("script"),c=0;c<u.length;c++){var d=u[c];if(d.getAttribute("src")==r||d.getAttribute("data-webpack")==t+i){s=d;break}}s||(l=!0,s=document.createElement("script"),s.charset="utf-8",s.timeout=120,n.nc&&s.setAttribute("nonce",n.nc),s.setAttribute("data-webpack",t+i),s.src=r),e[r]=[o];var h=function(t,n){s.onerror=s.onload=null,clearTimeout(p);var o=e[r];if(delete e[r],s.parentNode&&s.parentNode.removeChild(s),o&&o.forEach((function(e){return e(n)})),t)return t(n)},p=setTimeout(h.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=h.bind(null,s.onerror),s.onload=h.bind(null,s.onload),l&&document.head.appendChild(s)}}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.p="/"}(),function(){var e=function(e,t,n,r){var o=document.createElement("link");o.rel="stylesheet",o.type="text/css";var i=function(i){if(o.onerror=o.onload=null,"load"===i.type)n();else{var a=i&&("load"===i.type?"missing":i.type),s=i&&i.target&&i.target.href||t,l=new Error("Loading CSS chunk "+e+" failed.\n("+s+")");l.code="CSS_CHUNK_LOAD_FAILED",l.type=a,l.request=s,o.parentNode.removeChild(o),r(l)}};return o.onerror=o.onload=i,o.href=t,document.head.appendChild(o),o},t=function(e,t){for(var n=document.getElementsByTagName("link"),r=0;r<n.length;r++){var o=n[r],i=o.getAttribute("data-href")||o.getAttribute("href");if("stylesheet"===o.rel&&(i===e||i===t))return o}var a=document.getElementsByTagName("style");for(r=0;r<a.length;r++){o=a[r],i=o.getAttribute("data-href");if(i===e||i===t)return o}},r=function(r){return new Promise((function(o,i){var a=n.miniCssF(r),s=n.p+a;if(t(a,s))return o();e(r,s,o,i)}))},o={143:0};n.f.miniCss=function(e,t){var n={289:1};o[e]?t.push(o[e]):0!==o[e]&&n[e]&&t.push(o[e]=r(e).then((function(){o[e]=0}),(function(t){throw delete o[e],t})))}}(),function(){var e={143:0};n.f.j=function(t,r){var o=n.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else{var i=new Promise((function(n,r){o=e[t]=[n,r]}));r.push(o[2]=i);var a=n.p+n.u(t),s=new Error,l=function(r){if(n.o(e,t)&&(o=e[t],0!==o&&(e[t]=void 0),o)){var i=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;s.message="Loading chunk "+t+" failed.\n("+i+": "+a+")",s.name="ChunkLoadError",s.type=i,s.request=a,o[1](s)}};n.l(a,l,"chunk-"+t,t)}},n.O.j=function(t){return 0===e[t]};var t=function(t,r){var o,i,a=r[0],s=r[1],l=r[2],u=0;if(a.some((function(t){return 0!==e[t]}))){for(o in s)n.o(s,o)&&(n.m[o]=s[o]);if(l)var c=l(n)}for(t&&t(r);u<a.length;u++)i=a[u],n.o(e,i)&&e[i]&&e[i][0](),e[i]=0;return n.O(c)},r=self["webpackChunkmonitor_vue_h5"]=self["webpackChunkmonitor_vue_h5"]||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))}();var r=n.O(void 0,[998],(function(){return n(5679)}));r=n.O(r)})();
//# sourceMappingURL=app.43bcf837.js.map