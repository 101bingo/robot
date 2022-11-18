(function(){"use strict";var t={4268:function(t,e,n){n.r(e),n.d(e,{default:function(){return w}});var r=function(){var t=this,e=t._self._c;return e("div",{staticClass:"login-container"},[e("van-nav-bar",{attrs:{title:"首页--实时数据","left-text":"返回","left-arrow":""},scopedSlots:t._u([{key:"right",fn:function(){return[e("van-icon",{attrs:{name:"search",size:"18"}})]},proxy:!0}])}),e("van-cell-group",{attrs:{inset:""}},[e("van-field",{attrs:{label:"溶氧：",placeholder:"0","label-align":"right","input-align":"center"},model:{value:t.oxygenData,callback:function(e){t.oxygenData=e},expression:"oxygenData"}}),e("van-field",{attrs:{label:"温度：",placeholder:"0","label-align":"right","input-align":"center"},model:{value:t.temprature,callback:function(e){t.temprature=e},expression:"temprature"}})],1),e("LineChart",{attrs:{testData11:t.testresponse},on:{temperChange:t.updateTemp}})],1)},o=[],i=(n(7658),function(){var t=this,e=t._self._c;return e("div",{class:t.className,style:{height:t.height,width:t.width}})}),a=[],s=n(3139),l=n(2325),u={data(){return{$_sidebarElm:null,$_resizeHandler:null}},mounted(){this.$_resizeHandler=(0,l.Ds)((()=>{this.chart&&this.chart.resize()}),100),this.$_initResizeEvent(),this.$_initSidebarResizeEvent()},beforeDestroy(){this.$_destroyResizeEvent(),this.$_destroySidebarResizeEvent()},activated(){this.$_initResizeEvent(),this.$_initSidebarResizeEvent()},deactivated(){this.$_destroyResizeEvent(),this.$_destroySidebarResizeEvent()},methods:{$_initResizeEvent(){window.addEventListener("resize",this.$_resizeHandler)},$_destroyResizeEvent(){window.removeEventListener("resize",this.$_resizeHandler)},$_sidebarResizeHandler(t){"width"===t.propertyName&&this.$_resizeHandler()},$_initSidebarResizeEvent(){this.$_sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.$_sidebarElm&&this.$_sidebarElm.addEventListener("transitionend",this.$_sidebarResizeHandler)},$_destroySidebarResizeEvent(){this.$_sidebarElm&&this.$_sidebarElm.removeEventListener("transitionend",this.$_sidebarResizeHandler)}}};n(3630);let c=new Date(1997,9,3),d=1e3*Math.random();var h={mixins:[u],props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"550px"},autoResize:{type:Boolean,default:!0},testData11:{type:Array,default:[["2022-11-09 17:54:43",11],["2022-11-09 17:56:43",13]]}},data(){return{chart:null,testData:[]}},watch:{testData11:{handler(t){this.chart.setOption({series:[{data:t}]})}}},mounted(){this.height=window.screen.height/2+"px",this.$nextTick((()=>{this.initChart()}))},beforeDestroy(){this.chart&&(this.chart.dispose(),this.chart=null,clearInterval(this.dataTimer))},methods:{initChart(){this.chart=s.init(this.$el,"macarons"),this.setOptions()},setOptions(){this.chart.setOption({xAxis:{type:"time",boundaryGap:!1,axisLabel:{align:"center",formatter:function(t,e){let n=new Date(t),r=n.getMinutes().toString().padStart(2,"0"),o=n.getSeconds().toString().padStart(2,"0");var i=[r,o];return i.join(":")}},splitLine:{show:!1}},grid:{left:10,right:10,bottom:20,top:30,containLabel:!0},tooltip:{trigger:"axis",backgroundColor:"#00A1F1",formatter:function(t){let e=t[0].value[t[0].encode.x[0]];var n=new Date(e.replace(/-/g,"/"));return n.getFullYear().toString()+"/"+(n.getMonth()+1).toString()+"/"+n.getDate().toString()+" "+n.getHours().toString()+":"+n.getMinutes().toString().padStart(2,"0")+":"+n.getSeconds().toString().padStart(2,"0")+" -> "+t[0].value[1]},axisPointer:{animation:!1},padding:[5,10]},yAxis:{type:"value",axisTick:{show:!1}},legend:{data:["expected"]},dataZoom:{type:"inside"},series:[{name:"expected",markLine:{data:[{name:"阈值",yAxis:3,label:{show:"true",position:"middle",formatter:"溶氧红线：3",color:"inherit",fontSize:20,fontWeight:"bold"},lineStyle:{normal:{width:2,color:"#FF5D1D"}}}]},itemStyle:{normal:{color:"#FF005A",lineStyle:{color:"#FF005A",width:2}}},smooth:!0,type:"line",data:this.testData11,animationDuration:2800,animationEasing:"cubicInOut"}]})},createData(){let t=this;t.dataTimer=setInterval((()=>{t.testData.shift(),t.testData.push(t.randomData()),t.chart.setOption({series:[{data:t.testData}]})}),1e3)},randomData(){return c=new Date,d=d+21*Math.random()-10,this.$emit("temperChange",`${Math.round(d)} mg/L`),{name:c.toString(),value:[[c.getFullYear(),c.getMonth(),c.getDate()].join("/")+" "+c.getHours()+":"+c.getMinutes().toString().padStart(2,"0")+":"+c.getSeconds().toString().padStart(2,"0"),Math.round(d)]}}}},p=h,f=n(1001),m=(0,f.Z)(p,i,a,!1,null,null,null),g=m.exports,v={name:"HomePage",components:{LineChart:g},data(){return{ischecked:!1,active:0,oxygenData:"",temprature:"",testresponse:[]}},watch:{$route:{handler:function(t){this.redirect=t.query&&t.query.redirect},immediate:!0}},mounted(){this.openWebSocket()},methods:{showPwd(){"password"===this.passwordType?this.passwordType="":this.passwordType="password",this.$nextTick((()=>{this.$refs.password.focus()}))},updateTemp(t){this.temprature=t},updateOxygen(t){this.oxygenData=t},openWebSocket(){let t=this,e=location.host,n=`ws://${e}/ws`;console.log("websocketUrl:",n),"WebSocket"in window?console.log("您的浏览器支持WebSocket"):console.log("您的浏览器不支持WebSocket");const r=new WebSocket(n);r.onopen=function(t){console.log(new Date),console.log("websocket 已连接"),console.log(n)},r.onerror=function(t){console.log(t)},r.onclose=function(t){console.log(new Date),console.log("websocket 断开连接！")},r.onmessage=function(e){console.log(e.data);let n=e.data,r=JSON.parse(n);t.oxygenData=`${r.oxygen} mg/L`,t.temprature=`${r.temper} ℃`,t.testresponse.push([r.date_time,r.oxygen])},window.onbeforeunload=function(){r.close()}}}},b=v,y=(0,f.Z)(b,r,o,!1,null,"39ae5466",null),w=y.exports},5679:function(t,e,n){var r=n(6369),o=function(){var t=this,e=t._self._c;return e("div",{attrs:{id:"app"}},[e("router-view"),e("van-tabbar",{model:{value:t.active,callback:function(e){t.active=e},expression:"active"}},[e("van-tabbar-item",{attrs:{icon:"home-o"},on:{click:t.onClickHome}},[t._v("首页")]),e("van-tabbar-item",{attrs:{icon:"chart-trending-o"},on:{click:t.onClickHistory}},[t._v("历史数据")]),e("van-tabbar-item",{attrs:{icon:"setting-o"}},[t._v("控制")]),e("van-tabbar-item",{attrs:{icon:"manager-o"}},[t._v("我的")])],1)],1)},i=[],a=(n(7658),n(4268)),s={name:"App",components:{HomePage:a["default"]},data(){return{active:0}},methods:{onClickHome(){this.$router.push({path:"/home"})},onClickHistory(){this.$router.push({path:"/history"})},onClickControl(){this.$router.push({path:"/history"})},onClickMy(){this.$router.push({path:"/history"})}}},l=s,u=n(1001),c=(0,u.Z)(l,o,i,!1,null,null,null),d=c.exports,h=n(2631);r.ZP.use(h.ZP);const p=[{path:"/",name:"Home",component:()=>Promise.resolve().then(n.bind(n,4268))},{path:"/home",name:"Home",component:()=>Promise.resolve().then(n.bind(n,4268))},{path:"/history",name:"History",component:()=>n.e(289).then(n.bind(n,289))}],f=()=>new h.ZP({mode:"history",scrollBehavior:()=>({y:0}),routes:p}),m=f(),g=h.ZP.prototype.push;h.ZP.prototype.push=function(t){return g.call(this,t).catch((t=>t))};var v=m,b=n(3713),y=(n(5110),n(9821)),w=n.n(y);r.ZP.config.productionTip=!1,r.ZP.use(b.ZP);const S=new(w());r.ZP.use(S),new r.ZP({router:v,render:t=>t(d)}).$mount("#app")},2325:function(t,e,n){n.d(e,{Ds:function(){return r}});n(7658);function r(t,e,n){let r,o,i,a,s;const l=function(){const u=+new Date-a;u<e&&u>0?r=setTimeout(l,e-u):(r=null,n||(s=t.apply(i,o),r||(i=o=null)))};return function(...o){i=this,a=+new Date;const u=n&&!r;return r||(r=setTimeout(l,e)),u&&(s=t.apply(i,o),i=o=null),s}}}},e={};function n(r){var o=e[r];if(void 0!==o)return o.exports;var i=e[r]={exports:{}};return t[r].call(i.exports,i,i.exports,n),i.exports}n.m=t,function(){var t=[];n.O=function(e,r,o,i){if(!r){var a=1/0;for(c=0;c<t.length;c++){r=t[c][0],o=t[c][1],i=t[c][2];for(var s=!0,l=0;l<r.length;l++)(!1&i||a>=i)&&Object.keys(n.O).every((function(t){return n.O[t](r[l])}))?r.splice(l--,1):(s=!1,i<a&&(a=i));if(s){t.splice(c--,1);var u=o();void 0!==u&&(e=u)}}return e}i=i||0;for(var c=t.length;c>0&&t[c-1][2]>i;c--)t[c]=t[c-1];t[c]=[r,o,i]}}(),function(){n.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return n.d(e,{a:e}),e}}(),function(){n.d=function(t,e){for(var r in e)n.o(e,r)&&!n.o(t,r)&&Object.defineProperty(t,r,{enumerable:!0,get:e[r]})}}(),function(){n.f={},n.e=function(t){return Promise.all(Object.keys(n.f).reduce((function(e,r){return n.f[r](t,e),e}),[]))}}(),function(){n.u=function(t){return"static/js/"+t+".1f94a14c.js"}}(),function(){n.miniCssF=function(t){return"static/css/"+t+".424a8ba7.css"}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){var t={},e="monitor-vue-h5:";n.l=function(r,o,i,a){if(t[r])t[r].push(o);else{var s,l;if(void 0!==i)for(var u=document.getElementsByTagName("script"),c=0;c<u.length;c++){var d=u[c];if(d.getAttribute("src")==r||d.getAttribute("data-webpack")==e+i){s=d;break}}s||(l=!0,s=document.createElement("script"),s.charset="utf-8",s.timeout=120,n.nc&&s.setAttribute("nonce",n.nc),s.setAttribute("data-webpack",e+i),s.src=r),t[r]=[o];var h=function(e,n){s.onerror=s.onload=null,clearTimeout(p);var o=t[r];if(delete t[r],s.parentNode&&s.parentNode.removeChild(s),o&&o.forEach((function(t){return t(n)})),e)return e(n)},p=setTimeout(h.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=h.bind(null,s.onerror),s.onload=h.bind(null,s.onload),l&&document.head.appendChild(s)}}}(),function(){n.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){n.p="/"}(),function(){var t=function(t,e,n,r){var o=document.createElement("link");o.rel="stylesheet",o.type="text/css";var i=function(i){if(o.onerror=o.onload=null,"load"===i.type)n();else{var a=i&&("load"===i.type?"missing":i.type),s=i&&i.target&&i.target.href||e,l=new Error("Loading CSS chunk "+t+" failed.\n("+s+")");l.code="CSS_CHUNK_LOAD_FAILED",l.type=a,l.request=s,o.parentNode.removeChild(o),r(l)}};return o.onerror=o.onload=i,o.href=e,document.head.appendChild(o),o},e=function(t,e){for(var n=document.getElementsByTagName("link"),r=0;r<n.length;r++){var o=n[r],i=o.getAttribute("data-href")||o.getAttribute("href");if("stylesheet"===o.rel&&(i===t||i===e))return o}var a=document.getElementsByTagName("style");for(r=0;r<a.length;r++){o=a[r],i=o.getAttribute("data-href");if(i===t||i===e)return o}},r=function(r){return new Promise((function(o,i){var a=n.miniCssF(r),s=n.p+a;if(e(a,s))return o();t(r,s,o,i)}))},o={143:0};n.f.miniCss=function(t,e){var n={289:1};o[t]?e.push(o[t]):0!==o[t]&&n[t]&&e.push(o[t]=r(t).then((function(){o[t]=0}),(function(e){throw delete o[t],e})))}}(),function(){var t={143:0};n.f.j=function(e,r){var o=n.o(t,e)?t[e]:void 0;if(0!==o)if(o)r.push(o[2]);else{var i=new Promise((function(n,r){o=t[e]=[n,r]}));r.push(o[2]=i);var a=n.p+n.u(e),s=new Error,l=function(r){if(n.o(t,e)&&(o=t[e],0!==o&&(t[e]=void 0),o)){var i=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;s.message="Loading chunk "+e+" failed.\n("+i+": "+a+")",s.name="ChunkLoadError",s.type=i,s.request=a,o[1](s)}};n.l(a,l,"chunk-"+e,e)}},n.O.j=function(e){return 0===t[e]};var e=function(e,r){var o,i,a=r[0],s=r[1],l=r[2],u=0;if(a.some((function(e){return 0!==t[e]}))){for(o in s)n.o(s,o)&&(n.m[o]=s[o]);if(l)var c=l(n)}for(e&&e(r);u<a.length;u++)i=a[u],n.o(t,i)&&t[i]&&t[i][0](),t[i]=0;return n.O(c)},r=self["webpackChunkmonitor_vue_h5"]=self["webpackChunkmonitor_vue_h5"]||[];r.forEach(e.bind(null,0)),r.push=e.bind(null,r.push.bind(r))}();var r=n.O(void 0,[998],(function(){return n(5679)}));r=n.O(r)})();
//# sourceMappingURL=app.a30c9023.js.map