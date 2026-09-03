const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["chunks/loaded-SMPR6KZF-D8OLGQ-t.js","chunks/index-Cb9k1ARE.js","chunks/client-BP6gqO-q.js","chunks/index-C-SMbPlM.js","chunks/loaded-JKA25A3T-BxXqvxXU.js","chunks/loaded-36WRJPBT-D05DBu2k.js","chunks/full-7ZJV44EE-DwaRnnCc.js","chunks/Render-DQXAYUBI-tp0YyC1G.js","chunks/chunk-2CNEFIQP-DT3gzLHT.js","chunks/Editor-44C53YAG-FHX0eoLj.js"])))=>i.map(i=>d[i]);
import{g as Dc,R as Er,r as g,j as f,a as Wy,b as xi,c as Hy}from"./chunks/client-BP6gqO-q.js";const Vy="modulepreload",qy=function(e){return"/"+e},Rd={},Nr=function(t,r,n){let o=Promise.resolve();if(r&&r.length>0){let a=function(c){return Promise.all(c.map(d=>Promise.resolve(d).then(u=>({status:"fulfilled",value:u}),u=>({status:"rejected",reason:u}))))};document.getElementsByTagName("link");const s=document.querySelector("meta[property=csp-nonce]"),l=(s==null?void 0:s.nonce)||(s==null?void 0:s.getAttribute("nonce"));o=a(r.map(c=>{if(c=qy(c),c in Rd)return;Rd[c]=!0;const d=c.endsWith(".css"),u=d?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${c}"]${u}`))return;const p=document.createElement("link");if(p.rel=d?"stylesheet":Vy,d||(p.as="script"),p.crossOrigin="",p.href=c,l&&p.setAttribute("nonce",l),document.head.appendChild(p),d)return new Promise((v,h)=>{p.addEventListener("load",v),p.addEventListener("error",()=>h(new Error(`Unable to preload CSS for ${c}`)))})}))}function i(a){const s=new Event("vite:preloadError",{cancelable:!0});if(s.payload=a,window.dispatchEvent(s),!s.defaultPrevented)throw a}return o.then(a=>{for(const s of a||[])s.status==="rejected"&&i(s.reason);return t().catch(i)})};var Uy=Object.create,Tc=Object.defineProperty,Zy=Object.defineProperties,Yy=Object.getOwnPropertyDescriptor,Ky=Object.getOwnPropertyDescriptors,Mc=Object.getOwnPropertyNames,Aa=Object.getOwnPropertySymbols,Xy=Object.getPrototypeOf,Rc=Object.prototype.hasOwnProperty,Jf=Object.prototype.propertyIsEnumerable,Ld=(e,t,r)=>t in e?Tc(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,D=(e,t)=>{for(var r in t||(t={}))Rc.call(t,r)&&Ld(e,r,t[r]);if(Aa)for(var r of Aa(t))Jf.call(t,r)&&Ld(e,r,t[r]);return e},N=(e,t)=>Zy(e,Ky(t)),Tt=(e,t)=>{var r={};for(var n in e)Rc.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&Aa)for(var n of Aa(e))t.indexOf(n)<0&&Jf.call(e,n)&&(r[n]=e[n]);return r},Gy=(e,t)=>function(){return e&&(t=(0,e[Mc(e)[0]])(e=0)),t},Jy=(e,t)=>function(){return t||(0,e[Mc(e)[0]])((t={exports:{}}).exports,t),t.exports},Qy=(e,t,r,n)=>{if(t&&typeof t=="object"||typeof t=="function")for(let o of Mc(t))!Rc.call(e,o)&&o!==r&&Tc(e,o,{get:()=>t[o],enumerable:!(n=Yy(t,o))||n.enumerable});return e},eb=(e,t,r)=>(r=e!=null?Uy(Xy(e)):{},Qy(!e||!e.__esModule?Tc(r,"default",{value:e,enumerable:!0}):r,e)),Se=(e,t,r)=>new Promise((n,o)=>{var i=l=>{try{s(r.next(l))}catch(c){o(c)}},a=l=>{try{s(r.throw(l))}catch(c){o(c)}},s=l=>l.done?n(l.value):Promise.resolve(l.value).then(i,a);s((r=r.apply(e,t)).next())}),z=Gy({"../tsup-config/react-import.js"(){}});z();var Qf={RichTextEditor:"_RichTextEditor_5wzos_1","RichTextEditor--editor":"_RichTextEditor--editor_5wzos_50","RichTextEditor--disabled":"_RichTextEditor--disabled_5wzos_123","RichTextEditor--isActive":"_RichTextEditor--isActive_5wzos_159","RichTextEditor-menu":"_RichTextEditor-menu_5wzos_165"},Ds,Fd;function tb(){if(Fd)return Ds;Fd=1,Ds=r,r.flatten=r,r.unflatten=n;function e(o){return o&&o.constructor&&typeof o.constructor.isBuffer=="function"&&o.constructor.isBuffer(o)}function t(o){return o}function r(o,i){i=i||{};const a=i.delimiter||".",s=i.maxDepth,l=i.transformKey||t,c={};function d(u,p,v){v=v||1,Object.keys(u).forEach(function(h){const m=u[h],y=i.safe&&Array.isArray(m),b=Object.prototype.toString.call(m),k=e(m),x=b==="[object Object]"||b==="[object Array]",_=p?p+a+l(h):l(h);if(!y&&!k&&x&&Object.keys(m).length&&(!i.maxDepth||v<s))return d(m,_,v+1);c[_]=m})}return d(o),c}function n(o,i){i=i||{};const a=i.delimiter||".",s=i.overwrite||!1,l=i.transformKey||t,c={};if(e(o)||Object.prototype.toString.call(o)!=="[object Object]")return o;function u(h){const m=Number(h);return isNaN(m)||h.indexOf(".")!==-1||i.object?h:m}function p(h,m,y){return Object.keys(y).reduce(function(b,k){return b[h+a+k]=y[k],b},m)}function v(h){const m=Object.prototype.toString.call(h),y=m==="[object Array]",b=m==="[object Object]";if(h){if(y)return!h.length;if(b)return!Object.keys(h).length}else return!0}return o=Object.keys(o).reduce(function(h,m){const y=Object.prototype.toString.call(o[m]);return!(y==="[object Object]"||y==="[object Array]")||v(o[m])?(h[m]=o[m],h):p(m,h,r(o[m],i))},{}),Object.keys(o).forEach(function(h){const m=h.split(a).map(l);let y=u(m.shift()),b=u(m[0]),k=c;for(;b!==void 0;){if(y==="__proto__")return;const x=Object.prototype.toString.call(k[y]),_=x==="[object Object]"||x==="[object Array]";if(!s&&!_&&typeof k[y]<"u")return;(s&&!_||!s&&k[y]==null)&&(k[y]=typeof b=="number"&&!i.object?[]:{}),k=k[y],m.length>0&&(y=u(m.shift()),b=u(m[0]))}k[y]=n(o[h],i)}),c}return Ds}var rb=tb();const nb=Dc(rb);z();z();z();var eh=(e,t)=>Object.keys(t).reduce((r,n)=>t[n].type==="slot"?D({[n]:[]},r):r,e),Lc=e=>!!e&&typeof e.then=="function",Nd=e=>e.reduce((t,r)=>D(D({},t),r),{}),xl=e=>e.some(Lc),Fc=({value:e,fields:t,mappers:r,propKey:n="",propPath:o="",id:i="",config:a,recurseSlots:s=!1})=>{var l,c,d,u;const p=(l=t[n])==null?void 0:l.type,v=r[p];if(v&&p==="slot"){const h=e||[],m=s?h.map(y=>{if(!a.components[y.type])throw new Error(`Could not find component config for ${y.type}`);return un(y,r,a,s)}):h;return xl(m)?Promise.all(m):v({value:m,parentId:i,propName:o,field:t[n],propPath:o})}else if(v&&t[n])return v({value:e,parentId:i,propName:n,field:t[n],propPath:o});if(e&&typeof e=="object")if(Array.isArray(e)){const h=((c=t[n])==null?void 0:c.type)==="array"?t[n].arrayFields:null;if(!h)return e;const m=e.map((y,b)=>Fc({value:y,fields:h,mappers:r,propKey:n,propPath:`${o}[${b}]`,id:i,config:a,recurseSlots:s}));return xl(m)?Promise.all(m):m}else{if("$$typeof"in e)return e;{const h=((d=t[n])==null?void 0:d.type)==="object"?t[n].objectFields:t;return th({value:e,fields:h,mappers:r,id:i,getPropPath:m=>`${o}.${m}`,config:a,recurseSlots:s,ownedFields:((u=t[n])==null?void 0:u.type)==="object"})}}return e},th=({value:e,fields:t,mappers:r,id:n,getPropPath:o,config:i,recurseSlots:a,ownedFields:s,keysToWalk:l})=>{const c=l??Object.keys(e);if(!l&&s)for(const u in t){const p=t[u].type;p!=="slot"&&r[p]&&!(u in e)&&c.push(u)}const d=c.map(u=>{const p={value:e[u],fields:t,mappers:r,propKey:u,propPath:o(u),id:n,config:i,recurseSlots:a},v=Fc(p);return Lc(v)?v.then(h=>({[u]:h})):{[u]:v}},{});return xl(d)?Promise.all(d).then(Nd):Nd(d)};function un(e,t,r,n=!1,o=!0,i){var a,s,l,c,d;const u="type"in e?e.type:"root",p=u==="root"?r.root:(a=r.components)==null?void 0:a[u],v=th({value:o?eh((s=e.props)!=null?s:{},(l=p==null?void 0:p.fields)!=null?l:{}):e.props,fields:(c=p==null?void 0:p.fields)!=null?c:{},mappers:t,id:e.props&&(d=e.props.id)!=null?d:"root",getPropPath:h=>h,config:r,recurseSlots:n,ownedFields:!0,keysToWalk:i});return Lc(v)?v.then(h=>N(D({},e),{props:h})):N(D({},e),{props:v})}function rh(e,t,r){var n,o;const i=c=>un(c,{slot:({value:d,parentId:u,propName:p})=>{var v;const h=d;return(v=r(h,{parentId:u,propName:p}))!=null?v:h}},t,!0);if("props"in e)return i(e);const a=e,s=(n=a.zones)!=null?n:{},l=a.content.map(i);return{root:i(a.root),content:(o=r(l,{parentId:"root",propName:"default-zone"}))!=null?o:l,zones:Object.keys(s).reduce((c,d)=>N(D({},c),{[d]:s[d].map(i)}),{})}}z();var on="root",kl="default-zone",Je=`${on}:${kl}`;z();z();var ob=(e,t)=>un(e,{slot:()=>null},t),{flatten:ib,unflatten:ab}=nb,sb=e=>e!=null&&Object.prototype.toString.call(e)==="[object Object]",nh="__puck_[]",oh="__puck_{}";function lb(e={}){const t={};for(const r in e){if(!Object.prototype.hasOwnProperty.call(e,r))continue;const n=e[r];Array.isArray(n)&&n.length===0?t[r]=nh:sb(n)&&Object.keys(n).length===0?t[r]=oh:t[r]=n}return t}function cb(e={}){const t={};for(const r in e){if(!Object.prototype.hasOwnProperty.call(e,r))continue;const n=e[r];n===nh?t[r]=[]:n===oh?t[r]={}:t[r]=n}return t}var ub=(e,t)=>N(D({},e),{props:lb(ib(ob(e,t).props))}),ih=e=>{const t=ab(cb(e.props));return N(D({},e),{props:t})};z();var ro=e=>"type"in e?e:N(D({},e),{props:N(D({},e.props),{id:"root"}),type:"root"});z();z();z();var db=e=>e?e&&e.indexOf(":")>-1?e.split(":"):[Je,e]:[];function pb(e,t,r,n=[]){Object.entries(t.zones||{}).forEach(([o,i])=>{const[a]=db(o);a===e.props.id&&r(n,o,i)})}function mt(e,t,r=o=>o,n=o=>o){var o;let i={};const a={},s={},l=(x,_,I,w,A)=>{var E;const[C]=_.split(":"),S=((E=r(I,_,w))!=null?E:I)||[],[j,O]=_.split(":"),L=`${A||C}:${O}`,$=S.map((F,M)=>d(F,[...x,L],M));return a[L]={contentIds:$.map(F=>F.props.id),type:w},[L,$]},c=(x,_,I)=>{pb(x,e.data,(w,A,E)=>{const[C,S]=l(w,A,E,"dropzone",_);i[C]=S},I)},d=(x,_,I)=>{const w=n(x,_,I);if(!w)return x;const A=w.props.id,E=N(D({},un(w,{slot:({value:$,parentId:F,propPath:M})=>{const q=$,W=`${F}:${M}`,[B,Z]=l(_,W,q,"slot",F);return Z}},t).props),{id:A});c(x,A,_);const C=N(D({},w),{props:E}),S=_[_.length-1],[j,O]=S?S.split(":"):[null,""];s[A]={data:C,flatData:ub(C,t),path:_,parentId:j,zone:O};const L=N(D({},C),{props:D({},C.props)});return E.id==="root"&&(delete L.type,delete L.props.id),L},u=e.data.zones||{},[p,v]=l([],Je,e.data.content,"root"),h=v,m=Object.keys(i);Object.keys(u||{}).forEach(x=>{const[_]=x.split(":");if(m.includes(x))return;const[I,w]=l([Je],x,u[x],"dropzone",_);i[x]=w},i);let y=ro({props:D({},(o=e.data.root.props)!=null?o:e.data.root)});e.data.root.readOnly&&(y.readOnly=e.data.root.readOnly);const b=d(y,[],-1),k=D(D({},e.data.root),b);return N(D({},e),{data:{root:k,content:h,zones:D(D({},e.data.zones),i)},indexes:{nodes:D(D({},e.indexes.nodes),s),zones:D(D({},e.indexes.zones),a)}})}z();var ah=(e,t)=>{if(t===Je)return e;const r=N(D({},e),{zones:e.zones?D({},e.zones):{}});return r.zones[t]=r.zones[t]||[],r};z();z();var fb=(e,t,r)=>{if(typeof t.state=="object"){const n=D(D({},e),t.state);return t.state.indexes?n:(console.warn("`set` is expensive and may cause unnecessary re-renders. Consider using a more atomic action instead."),mt(n,r.config))}return D(D({},e),t.state(e))};z();z();var ei=(e,t,r)=>{const n=Array.from(e||[]);return n.splice(t,0,r),n};z();z();z();var hb=new Uint8Array(16);function vb(){return crypto.getRandomValues(hb)}z();var Ue=[];for(let e=0;e<256;++e)Ue.push((e+256).toString(16).slice(1));function gb(e,t=0){return(Ue[e[t+0]]+Ue[e[t+1]]+Ue[e[t+2]]+Ue[e[t+3]]+"-"+Ue[e[t+4]]+Ue[e[t+5]]+"-"+Ue[e[t+6]]+Ue[e[t+7]]+"-"+Ue[e[t+8]]+Ue[e[t+9]]+"-"+Ue[e[t+10]]+Ue[e[t+11]]+Ue[e[t+12]]+Ue[e[t+13]]+Ue[e[t+14]]+Ue[e[t+15]]).toLowerCase()}function mb(e,t,r){return!t&&!e&&crypto.randomUUID?crypto.randomUUID():_b(e,t,r)}function _b(e,t,r){var n,o,i;e=e||{};const a=(i=(o=e.random)!=null?o:(n=e.rng)==null?void 0:n.call(e))!=null?i:vb();if(a.length<16)throw new Error("Random bytes length must be >= 16");if(a[6]=a[6]&15|64,a[8]=a[8]&63|128,t){if(r=r||0,r<0||r+16>t.length)throw new RangeError(`UUID byte range ${r}:${r+15} is out of buffer bounds`);for(let s=0;s<16;++s)t[r+s]=a[s];return t}return gb(a)}var Bd=mb,dt=e=>e?`${e}-${Bd()}`:Bd();z();var ti=(e,t)=>{const[r]=e.split(":"),n=t.indexes.nodes[r];return((n==null?void 0:n.path)||[]).map(o=>o.split(":")[0])};z();var Nc=(e,t,r=!1)=>{const n=dt(e.type);return rh(N(D({},e),{props:r?N(D({},e.props),{id:n}):D({},e.props)}),t,o=>o.map(i=>{const a=dt(i.type);return N(D({},i),{props:r?N(D({},i.props),{id:a}):D({id:a},i.props)})}))};function sh(e,t,r){const n=t.id||dt(t.componentType),o=Nc({type:t.componentType,props:N(D({},r.config.components[t.componentType].defaultProps||{}),{id:n})},r.config),[i]=t.destinationZone.split(":"),a=ti(t.destinationZone,e);return mt(e,r.config,(s,l)=>l===t.destinationZone?ei(s||[],t.destinationIndex,o):s,(s,l)=>s.props.id===n||s.props.id===i||a.includes(s.props.id)||l.includes(t.destinationZone)?s:null)}z();var yb=(e,t,r)=>{const[n]=t.destinationZone.split(":"),o=ti(t.destinationZone,e),i=e.indexes.zones[t.destinationZone].contentIds[t.destinationIndex];if(i!==t.data.props.id)throw new Error(`Can't change the id during a replace action. Please us "remove" and "insert" to define a new node.`);const s=[],l=rh(t.data,r.config,(d,u)=>(s.push(`${u.parentId}:${u.propName}`),d.map(p=>{const v=dt(p.type);return N(D({},p),{props:D({id:v},p.props)})}))),c=N(D({},e),{ui:D(D({},e.ui),t.ui)});return Object.keys(e.indexes.zones).forEach(d=>{d.split(":")[0]===i&&(s.includes(d)||delete c.indexes.zones[d])}),mt(c,r.config,(d,u)=>{const p=[...d];return u===t.destinationZone&&(p[t.destinationIndex]=l),p},(d,u)=>{const p=u.map(v=>v.split(":")[0]);return d.props.id===l.props.id?l:d.props.id===n||o.indexOf(d.props.id)>-1||p.indexOf(l.props.id)>-1?d:null})};z();var bb=(e,t,r)=>mt(e,r.config,n=>n,n=>n.props.id==="root"?N(D({},n),{props:D(D({},n.props),t.root.props),readOnly:t.root.readOnly}):n);z();z();function et(e,t){var r,n;const o=(r=t.indexes.zones)==null?void 0:r[e.zone||Je];return o?(n=t.indexes.nodes[o.contentIds[e.index]])==null?void 0:n.data:void 0}function xb(e,t,r){const n=et({index:t.sourceIndex,zone:t.sourceZone},e),o=ti(t.sourceZone,e),i=N(D({},n),{props:N(D({},n.props),{id:dt(n.type)})}),a=mt(e,r.config,(s,l)=>l===t.sourceZone?ei(s,t.sourceIndex+1,n):s,(s,l,c)=>{const d=l[l.length-1];if(l.map(v=>v.split(":")[0]).indexOf(i.props.id)>-1)return N(D({},s),{props:N(D({},s.props),{id:dt(s.type)})});if(d===t.sourceZone&&c===t.sourceIndex+1)return i;const[p]=t.sourceZone.split(":");return p===s.props.id||o.indexOf(s.props.id)>-1?s:null});return N(D({},a),{ui:N(D({},a.ui),{itemSelector:{index:t.sourceIndex+1,zone:t.sourceZone}})})}z();z();z();var wl=(e,t)=>{const r=Array.from(e);return r.splice(t,1),r},lh=(e,t,r)=>{if(t.sourceZone===t.destinationZone&&t.sourceIndex===t.destinationIndex)return e;const n=et({zone:t.sourceZone,index:t.sourceIndex},e);if(!n)return e;const o=ti(t.sourceZone,e),i=ti(t.destinationZone,e);return mt(e,r.config,(a,s)=>s===t.sourceZone&&s===t.destinationZone?ei(wl(a,t.sourceIndex),t.destinationIndex,n):s===t.sourceZone?wl(a,t.sourceIndex):s===t.destinationZone?ei(a,t.destinationIndex,n):a,(a,s)=>{const[l]=t.sourceZone.split(":"),[c]=t.destinationZone.split(":"),d=a.props.id;return l===d||c===d||n.props.id===d||o.indexOf(d)>-1||i.indexOf(d)>-1||s.includes(t.destinationZone)?a:null})},kb=(e,t,r)=>lh(e,{sourceIndex:t.sourceIndex,sourceZone:t.destinationZone,destinationIndex:t.destinationIndex,destinationZone:t.destinationZone},r);z();var wb=(e,t,r)=>{const n=et({index:t.index,zone:t.zone},e),o=new Set([n.props.id]);Object.entries(e.indexes.nodes).forEach(([s,l])=>{l.path.map(d=>d.split(":")[0]).includes(n.props.id)&&o.add(s)});const i=mt(e,r.config,(s,l)=>l===t.zone?wl(s,t.index):s);Object.keys(i.data.zones||{}).forEach(s=>{const l=s.split(":")[0];o.has(l)&&i.data.zones&&delete i.data.zones[s]}),Object.keys(i.indexes.zones).forEach(s=>{const l=s.split(":")[0];o.has(l)&&delete i.indexes.zones[s]});const a=D({},i.ui.itemExpanded);return o.forEach(s=>{delete i.indexes.nodes[s],delete a[s]}),i.ui=N(D({},i.ui),{itemExpanded:a}),i};z();var fa={};function Sb(e,t){return fa[t.zone]?N(D({},e),{data:N(D({},e.data),{zones:N(D({},e.data.zones),{[t.zone]:fa[t.zone]})}),indexes:N(D({},e.indexes),{zones:N(D({},e.indexes.zones),{[t.zone]:N(D({},e.indexes.zones[t.zone]),{contentIds:fa[t.zone].map(r=>r.props.id),type:"dropzone"})})})}):N(D({},e),{data:ah(e.data,t.zone)})}function Eb(e,t){const r=D({},e.data.zones||{}),n=D({},e.indexes.zones||{});return r[t.zone]&&(fa[t.zone]=r[t.zone],delete r[t.zone]),delete n[t.zone],N(D({},e),{data:N(D({},e.data),{zones:r}),indexes:N(D({},e.indexes),{zones:n})})}z();var Ib=(e,t,r)=>typeof t.data=="object"?(console.warn("`setData` is expensive and may cause unnecessary re-renders. Consider using a more atomic action instead."),mt(N(D({},e),{data:D(D({},e.data),t.data)}),r.config)):mt(N(D({},e),{data:D(D({},e.data),t.data(e.data))}),r.config);z();var Cb=(e,t)=>{var r,n;const o=t.itemSelector;if(!o)return t;const i=et(o,e);if(!i)return t;const s=((n=(r=e.indexes.nodes[i.props.id])==null?void 0:r.path)!=null?n:[]).map(c=>c.split(":")[0]).filter(c=>{var d,u;return c&&c!==on&&!((d=e.ui.itemExpanded)!=null&&d[c])&&!((u=t.itemExpanded)!=null&&u[c])});if(s.length===0)return t;const l=D(D({},e.ui.itemExpanded),t.itemExpanded);return s.forEach(c=>{l[c]=!0}),N(D({},t),{itemExpanded:l})},Pb=(e,t)=>{const r=typeof t.ui=="object"?t.ui:t.ui(e.ui);return N(D({},e),{ui:D(D({},e.ui),Cb(e,r))})};z();var ri=e=>{const{data:t,ui:r}=e;return{data:t,ui:r}};z();function zb(e,t,r){return(n,o)=>{const i=e(n,o),a=!["registerZone","unregisterZone","setData","setUi","set"].includes(o.type);return(typeof o.recordHistory<"u"?o.recordHistory:a)&&t&&t(i),r==null||r(o,ri(i),ri(n)),i}}function $d({record:e,onAction:t,appStore:r}){return zb((n,o)=>o.type==="set"?fb(n,o,r):o.type==="insert"?sh(n,o,r):o.type==="replace"?yb(n,o,r):o.type==="replaceRoot"?bb(n,o,r):o.type==="duplicate"?xb(n,o,r):o.type==="reorder"?kb(n,o,r):o.type==="move"?lh(n,o,r):o.type==="remove"?wb(n,o,r):o.type==="registerZone"?Sb(n,o):o.type==="unregisterZone"?Eb(n,o):o.type==="setData"?Ib(n,o,r):o.type==="setUi"?Pb(n,o):n,e,t)}var Ab=Object.getOwnPropertyNames,jb=Object.getOwnPropertySymbols,Ob=Object.prototype.hasOwnProperty;function Wd(e,t){return function(n,o,i){return e(n,o,i)&&t(n,o,i)}}function $i(e){return function(r,n,o){if(!r||!n||typeof r!="object"||typeof n!="object")return e(r,n,o);var i=o.cache,a=i.get(r),s=i.get(n);if(a&&s)return a===n&&s===r;i.set(r,n),i.set(n,r);var l=e(r,n,o);return i.delete(r),i.delete(n),l}}function Hd(e){return Ab(e).concat(jb(e))}var Db=Object.hasOwn||(function(e,t){return Ob.call(e,t)});function dn(e,t){return e===t||!e&&!t&&e!==e&&t!==t}var Tb="__v",Mb="__o",Rb="_owner",Vd=Object.getOwnPropertyDescriptor,qd=Object.keys;function Lb(e,t,r){var n=e.length;if(t.length!==n)return!1;for(;n-- >0;)if(!r.equals(e[n],t[n],n,n,e,t,r))return!1;return!0}function Fb(e,t){return dn(e.getTime(),t.getTime())}function Nb(e,t){return e.name===t.name&&e.message===t.message&&e.cause===t.cause&&e.stack===t.stack}function Bb(e,t){return e===t}function Ud(e,t,r){var n=e.size;if(n!==t.size)return!1;if(!n)return!0;for(var o=new Array(n),i=e.entries(),a,s,l=0;(a=i.next())&&!a.done;){for(var c=t.entries(),d=!1,u=0;(s=c.next())&&!s.done;){if(o[u]){u++;continue}var p=a.value,v=s.value;if(r.equals(p[0],v[0],l,u,e,t,r)&&r.equals(p[1],v[1],p[0],v[0],e,t,r)){d=o[u]=!0;break}u++}if(!d)return!1;l++}return!0}var $b=dn;function Wb(e,t,r){var n=qd(e),o=n.length;if(qd(t).length!==o)return!1;for(;o-- >0;)if(!ch(e,t,r,n[o]))return!1;return!0}function Eo(e,t,r){var n=Hd(e),o=n.length;if(Hd(t).length!==o)return!1;for(var i,a,s;o-- >0;)if(i=n[o],!ch(e,t,r,i)||(a=Vd(e,i),s=Vd(t,i),(a||s)&&(!a||!s||a.configurable!==s.configurable||a.enumerable!==s.enumerable||a.writable!==s.writable)))return!1;return!0}function Hb(e,t){return dn(e.valueOf(),t.valueOf())}function Vb(e,t){return e.source===t.source&&e.flags===t.flags}function Zd(e,t,r){var n=e.size;if(n!==t.size)return!1;if(!n)return!0;for(var o=new Array(n),i=e.values(),a,s;(a=i.next())&&!a.done;){for(var l=t.values(),c=!1,d=0;(s=l.next())&&!s.done;){if(!o[d]&&r.equals(a.value,s.value,a.value,s.value,e,t,r)){c=o[d]=!0;break}d++}if(!c)return!1}return!0}function qb(e,t){var r=e.length;if(t.length!==r)return!1;for(;r-- >0;)if(e[r]!==t[r])return!1;return!0}function Ub(e,t){return e.hostname===t.hostname&&e.pathname===t.pathname&&e.protocol===t.protocol&&e.port===t.port&&e.hash===t.hash&&e.username===t.username&&e.password===t.password}function ch(e,t,r,n){return(n===Rb||n===Mb||n===Tb)&&(e.$$typeof||t.$$typeof)?!0:Db(t,n)&&r.equals(e[n],t[n],n,n,e,t,r)}var Zb="[object Arguments]",Yb="[object Boolean]",Kb="[object Date]",Xb="[object Error]",Gb="[object Map]",Jb="[object Number]",Qb="[object Object]",ex="[object RegExp]",tx="[object Set]",rx="[object String]",nx="[object URL]",ox=Array.isArray,Yd=typeof ArrayBuffer=="function"&&ArrayBuffer.isView?ArrayBuffer.isView:null,Kd=Object.assign,ix=Object.prototype.toString.call.bind(Object.prototype.toString);function ax(e){var t=e.areArraysEqual,r=e.areDatesEqual,n=e.areErrorsEqual,o=e.areFunctionsEqual,i=e.areMapsEqual,a=e.areNumbersEqual,s=e.areObjectsEqual,l=e.arePrimitiveWrappersEqual,c=e.areRegExpsEqual,d=e.areSetsEqual,u=e.areTypedArraysEqual,p=e.areUrlsEqual;return function(h,m,y){if(h===m)return!0;if(h==null||m==null)return!1;var b=typeof h;if(b!==typeof m)return!1;if(b!=="object")return b==="number"?a(h,m,y):b==="function"?o(h,m,y):!1;var k=h.constructor;if(k!==m.constructor)return!1;if(k===Object)return s(h,m,y);if(ox(h))return t(h,m,y);if(Yd!=null&&Yd(h))return u(h,m,y);if(k===Date)return r(h,m,y);if(k===RegExp)return c(h,m,y);if(k===Map)return i(h,m,y);if(k===Set)return d(h,m,y);var x=ix(h);return x===Kb?r(h,m,y):x===ex?c(h,m,y):x===Gb?i(h,m,y):x===tx?d(h,m,y):x===Qb?typeof h.then!="function"&&typeof m.then!="function"&&s(h,m,y):x===nx?p(h,m,y):x===Xb?n(h,m,y):x===Zb?s(h,m,y):x===Yb||x===Jb||x===rx?l(h,m,y):!1}}function sx(e){var t=e.circular,r=e.createCustomConfig,n=e.strict,o={areArraysEqual:n?Eo:Lb,areDatesEqual:Fb,areErrorsEqual:Nb,areFunctionsEqual:Bb,areMapsEqual:n?Wd(Ud,Eo):Ud,areNumbersEqual:$b,areObjectsEqual:n?Eo:Wb,arePrimitiveWrappersEqual:Hb,areRegExpsEqual:Vb,areSetsEqual:n?Wd(Zd,Eo):Zd,areTypedArraysEqual:n?Eo:qb,areUrlsEqual:Ub};if(r&&(o=Kd({},o,r(o))),t){var i=$i(o.areArraysEqual),a=$i(o.areMapsEqual),s=$i(o.areObjectsEqual),l=$i(o.areSetsEqual);o=Kd({},o,{areArraysEqual:i,areMapsEqual:a,areObjectsEqual:s,areSetsEqual:l})}return o}function lx(e){return function(t,r,n,o,i,a,s){return e(t,r,s)}}function cx(e){var t=e.circular,r=e.comparator,n=e.createState,o=e.equals,i=e.strict;if(n)return function(l,c){var d=n(),u=d.cache,p=u===void 0?t?new WeakMap:void 0:u,v=d.meta;return r(l,c,{cache:p,equals:o,meta:v,strict:i})};if(t)return function(l,c){return r(l,c,{cache:new WeakMap,equals:o,meta:void 0,strict:i})};var a={cache:void 0,equals:o,meta:void 0,strict:i};return function(l,c){return r(l,c,a)}}var ni=Br();Br({strict:!0});Br({circular:!0});Br({circular:!0,strict:!0});Br({createInternalComparator:function(){return dn}});Br({strict:!0,createInternalComparator:function(){return dn}});Br({circular:!0,createInternalComparator:function(){return dn}});Br({circular:!0,createInternalComparator:function(){return dn},strict:!0});function Br(e){e===void 0&&(e={});var t=e.circular,r=t===void 0?!1:t,n=e.createInternalComparator,o=e.createState,i=e.strict,a=i===void 0?!1:i,s=sx(e),l=ax(s),c=n?n(l):lx(l);return cx({circular:r,comparator:l,createState:o,equals:c,strict:a})}z();var oi=[{width:360,height:"auto",icon:"Smartphone",label:"Small"},{width:768,height:"auto",icon:"Tablet",label:"Medium"},{width:1280,height:"auto",icon:"Monitor",label:"Large"},{width:"100%",height:"auto",icon:"FullWidth",label:"Full-width"}];z();z();var Bc=(e,t)=>e?Object.keys(e.props||{}).reduce((r,n)=>{const o=(e==null?void 0:e.props)||{},i=(t==null?void 0:t.props)||{};return N(D({},r),{[n]:!ni(i[n],o[n])})},{}):{},ux={lastChange:{}},uh=(e,t,...r)=>Se(null,[e,t,...r],function*(n,o,i={},a,s,l="replace",c=null,d={props:{}},u=ux){const p="type"in n&&n.type!=="root"?o.components[n.type]:o.root,v=D({},n),h=(p==null?void 0:p.resolveData)&&n.props,m="id"in n.props?n.props.id:"root";if(h){const{item:k=null,resolved:x={},parentId:_=null}=u.lastChange[m]||{},w=!(_===null)&&(c==null?void 0:c.props.id)!==_,A=n&&!ni(n,k);if(l==="move"&&!w||l!=="move"&&l!=="force"&&!A)return{node:x,didChange:!1};const C=Bc(n,k);a&&a(n);const{props:S,readOnly:j={}}=yield p.resolveData(n,{changed:C,lastData:k,metadata:D(D({},i),p.metadata),trigger:l,parent:c,root:d});v.props=D(D({},n.props),S),Object.keys(j).length&&(v.readOnly=j)}const y=ro(v);let b=yield un(v,{slot:k=>Se(null,[k],function*({value:x}){const _=x;return yield Promise.all(_.map(I=>Se(null,null,function*(){return(yield uh(I,o,i,a,s,l,y,d,u)).node})))})},o);return h&&s&&s(v),u.lastChange[m]={item:n,resolved:b,parentId:c==null?void 0:c.props.id},{node:b,didChange:!ni(n,b)}});z();var Sl={data:{content:[],root:{},zones:{}},ui:{leftSideBarVisible:!0,rightSideBarVisible:!0,arrayState:{},itemSelector:null,componentList:{},isDragging:!1,itemExpanded:{},previewMode:"edit",viewports:{current:{width:oi[0].width,height:oi[0].height||"auto"},options:[],controlsVisible:!0},field:{focus:null},plugin:{current:null}},indexes:{nodes:{},zones:{}}},dx=Jy({"../../node_modules/classnames/index.js"(e,t){z(),(function(){var r={}.hasOwnProperty;function n(){for(var a="",s=0;s<arguments.length;s++){var l=arguments[s];l&&(a=i(a,o(l)))}return a}function o(a){if(typeof a=="string"||typeof a=="number")return a;if(typeof a!="object")return"";if(Array.isArray(a))return n.apply(null,a);if(a.toString!==Object.prototype.toString&&!a.toString.toString().includes("[native code]"))return a.toString();var s="";for(var l in a)r.call(a,l)&&a[l]&&(s=i(s,l));return s}function i(a,s){return s?a?a+" "+s:a+s:a}typeof t<"u"&&t.exports?(n.default=n,t.exports=n):typeof define=="function"&&typeof define.amd=="object"&&define.amd?define("classnames",[],function(){return n}):window.classNames=n})()}});z();var px=eb(dx()),fx=(e,t,r={baseClass:""})=>(n={})=>{if(typeof n=="string"){const o=n;return t[`${e}-${o}`]&&r.baseClass+t[`${e}-${o}`]||""}else if(typeof n=="object"){const o=n,i={};for(let s in o)i[t[`${e}--${s}`]]=o[s];const a=t[e];return r.baseClass+(0,px.default)(D({[a]:!!a},i))}else return r.baseClass+t[e]||""},ee=fx;/*! Bundled license information:

classnames/index.js:
  (*!
  	Copyright (c) 2018 Jed Watson.
  	Licensed under the MIT License (MIT), see
  	http://jedwatson.github.io/classnames
  *)
*/const Xd=e=>{let t;const r=new Set,n=(c,d)=>{const u=typeof c=="function"?c(t):c;if(!Object.is(u,t)){const p=t;t=d??(typeof u!="object"||u===null)?u:Object.assign({},t,u),r.forEach(v=>v(t,p))}},o=()=>t,s={setState:n,getState:o,getInitialState:()=>l,subscribe:c=>(r.add(c),()=>r.delete(c))},l=t=e(n,o,s);return s},$r=(e=>e?Xd(e):Xd),hx=e=>e;function ts(e,t=hx){const r=Er.useSyncExternalStore(e.subscribe,Er.useCallback(()=>t(e.getState()),[e,t]),Er.useCallback(()=>t(e.getInitialState()),[e,t]));return Er.useDebugValue(r),r}const vx=e=>{const t=$r(e),r=n=>ts(t,n);return Object.assign(r,t),r},dh=(e=>vx),gx=e=>(t,r,n)=>{const o=n.subscribe;return n.subscribe=((a,s,l)=>{let c=a;if(s){const d=(l==null?void 0:l.equalityFn)||Object.is;let u=a(n.getState());c=p=>{const v=a(p);if(!d(u,v)){const h=u;s(u=v,h)}},l!=null&&l.fireImmediately&&s(u,u)}return o(c)}),e(t,r,n)},$c=gx;var mx=Object.defineProperty,no=(e,t)=>mx(e,"name",{value:t,configurable:!0}),ph=!!(typeof window<"u"&&window.document&&window.document.createElement);function Ar(e,t,{checkForDefaultPrevented:r=!0}={}){return no(function(o){if(e==null||e(o),r===!1||!o||!o.defaultPrevented)return t==null?void 0:t(o)},"handleEvent")}no(Ar,"composeEventHandlers");function _x(e){var t;if(!ph)throw new Error("Cannot access window outside of the DOM");return((t=e==null?void 0:e.ownerDocument)==null?void 0:t.defaultView)??window}no(_x,"getOwnerWindow");function El(e){if(!ph)throw new Error("Cannot access document outside of the DOM");return(e==null?void 0:e.ownerDocument)??document}no(El,"getOwnerDocument");function fh(e,t=!1){const{activeElement:r}=El(e);if(!(r!=null&&r.nodeName))return null;if(hh(r)&&r.contentDocument)return fh(r.contentDocument.body,t);if(t){const n=r.getAttribute("aria-activedescendant");if(n){const o=El(r).getElementById(n);if(o)return o}}return r}no(fh,"getActiveElement");function hh(e){return e.tagName==="IFRAME"}no(hh,"isFrame");var yx=Object.defineProperty,Wc=(e,t)=>yx(e,"name",{value:t,configurable:!0});function Il(e,t){if(typeof e=="function")return e(t);e!=null&&(e.current=t)}Wc(Il,"setRef");function vh(...e){return t=>{let r=!1;const n=e.map(o=>{const i=Il(o,t);return!r&&typeof i=="function"&&(r=!0),i});if(r)return()=>{for(let o=0;o<n.length;o++){const i=n[o];typeof i=="function"?i():Il(e[o],null)}}}}Wc(vh,"composeRefs");function Wr(...e){return g.useCallback(vh(...e),e)}Wc(Wr,"useComposedRefs");var bx=Object.defineProperty,bt=(e,t)=>bx(e,"name",{value:t,configurable:!0});function xx(e,t){const r=g.createContext(t);r.displayName=e+"Context";const n=bt(i=>{const{children:a,...s}=i,l=g.useMemo(()=>s,Object.values(s));return f.jsx(r.Provider,{value:l,children:a})},"Provider");n.displayName=e+"Provider";function o(i,a={}){const{optional:s=!1}=a,l=g.useContext(r);if(l)return l;if(t!==void 0)return t;if(!s)throw new Error(`\`${i}\` must be used within \`${e}\``)}return bt(o,"useContext"),[n,o]}bt(xx,"createContext");function Hc(e,t=[]){let r=[];function n(i,a){const s=g.createContext(a);s.displayName=i+"Context";const l=r.length;r=[...r,a];const c=bt(u=>{var b;const{scope:p,children:v,...h}=u,m=((b=p==null?void 0:p[e])==null?void 0:b[l])||s,y=g.useMemo(()=>h,Object.values(h));return f.jsx(m.Provider,{value:y,children:v})},"Provider");c.displayName=i+"Provider";function d(u,p,v={}){var b;const{optional:h=!1}=v,m=((b=p==null?void 0:p[e])==null?void 0:b[l])||s,y=g.useContext(m);if(y)return y;if(a!==void 0)return a;if(!h)throw new Error(`\`${u}\` must be used within \`${i}\``)}return bt(d,"useContext"),[c,d]}bt(n,"createContext");const o=bt(()=>{const i=r.map(a=>g.createContext(a));return bt(function(s){const l=(s==null?void 0:s[e])||i;return g.useMemo(()=>({[`__scope${e}`]:{...s,[e]:l}}),[s,l])},"useScope")},"createScope");return o.scopeName=e,[n,gh(o,...t)]}bt(Hc,"createContextScope");function gh(...e){const t=e[0];if(e.length===1)return t;const r=bt(()=>{const n=e.map(o=>({useScope:o(),scopeName:o.scopeName}));return bt(function(i){const a=n.reduce((s,{useScope:l,scopeName:c})=>{const u=l(i)[`__scope${c}`];return{...s,...u}},{});return g.useMemo(()=>({[`__scope${t.scopeName}`]:a}),[a])},"useComposedScopes")},"createScope");return r.scopeName=t.scopeName,r}bt(gh,"composeContextScopes");var pr=Wy();const wj=Dc(pr);var kx=Object.defineProperty,Mt=(e,t)=>kx(e,"name",{value:t,configurable:!0});function Vc(e){const t=g.forwardRef((r,n)=>{let{children:o,...i}=r,a=null,s=!1;const l=[];Cl(o)&&typeof Wi=="function"&&(o=Wi(o._payload)),g.Children.forEach(o,p=>{var v;if(bh(p)){s=!0;const h=p;let m="child"in h.props?h.props.child:h.props.children;Cl(m)&&typeof Wi=="function"&&(m=Wi(m._payload)),a=Sx(h,m),l.push((v=a==null?void 0:a.props)==null?void 0:v.children)}else l.push(p)}),a?a=g.cloneElement(a,void 0,l):!s&&g.Children.count(o)===1&&g.isValidElement(o)&&(a=o);const c=a?yh(a):void 0,d=Wr(n,c);if(!a){if(o||o===0)throw new Error(s?Cx(e):Ix(e));return o}const u=_h(i,a.props??{});return a.type!==g.Fragment&&(u.ref=n?d:c),g.cloneElement(a,u)});return t.displayName=`${e}.Slot`,t}Mt(Vc,"createSlot");var mh=Symbol.for("radix.slottable");function wx(e){const t=Mt(r=>"child"in r?r.children(r.child):r.children,"Slottable");return t.displayName=`${e}.Slottable`,t.__radixId=mh,t}Mt(wx,"createSlottable");var Sx=Mt((e,t)=>{if("child"in e.props){const r=e.props.child;return g.isValidElement(r)?g.cloneElement(r,void 0,e.props.children(r.props.children)):null}return g.isValidElement(t)?t:null},"getSlottableElementFromSlottable");function _h(e,t){const r={...t};for(const n in t){const o=e[n],i=t[n];/^on[A-Z]/.test(n)?o&&i?r[n]=(...s)=>{const l=i(...s);return o(...s),l}:o&&(r[n]=o):n==="style"?r[n]={...o,...i}:n==="className"&&(r[n]=[o,i].filter(Boolean).join(" "))}return{...e,...r}}Mt(_h,"mergeProps");function yh(e){var n,o;let t=(n=Object.getOwnPropertyDescriptor(e.props,"ref"))==null?void 0:n.get,r=t&&"isReactWarning"in t&&t.isReactWarning;return r?e.ref:(t=(o=Object.getOwnPropertyDescriptor(e,"ref"))==null?void 0:o.get,r=t&&"isReactWarning"in t&&t.isReactWarning,r?e.props.ref:e.props.ref||e.ref)}Mt(yh,"getElementRef");function bh(e){return g.isValidElement(e)&&typeof e.type=="function"&&"__radixId"in e.type&&e.type.__radixId===mh}Mt(bh,"isSlottable");var Ex=Symbol.for("react.lazy");function Cl(e){return e!=null&&typeof e=="object"&&"$$typeof"in e&&e.$$typeof===Ex&&"_payload"in e&&xh(e._payload)}Mt(Cl,"isLazyComponent");function xh(e){return typeof e=="object"&&e!==null&&"then"in e}Mt(xh,"isPromiseLike");var Ix=Mt(e=>`${e} failed to slot onto its children. Expected a single React element child or \`Slottable\`.`,"createSlotError"),Cx=Mt(e=>`${e} failed to slot onto its \`Slottable\`. Expected \`Slottable\` to receive a single React element child.`,"createSlottableError"),Wi=xi[" use ".trim().toString()],Px=Object.defineProperty,zx=(e,t)=>Px(e,"name",{value:t,configurable:!0}),Ax=["a","button","div","form","h2","h3","img","input","label","li","nav","ol","p","select","span","svg","ul"],oo=Ax.reduce((e,t)=>{const r=Vc(`Primitive.${t}`),n=g.forwardRef((o,i)=>{const{asChild:a,...s}=o,l=a?r:t;return typeof window<"u"&&(window[Symbol.for("radix-ui")]=!0),f.jsx(l,{...s,ref:i})});return n.displayName=`Primitive.${t}`,{...e,[t]:n}},{});function kh(e,t){e&&pr.flushSync(()=>e.dispatchEvent(t))}zx(kh,"dispatchDiscreteCustomEvent");var jx=Object.defineProperty,Ox=(e,t)=>jx(e,"name",{value:t,configurable:!0});function an(e){const t=g.useRef(e);return g.useEffect(()=>{t.current=e}),g.useMemo(()=>((...r)=>{var n;return(n=t.current)==null?void 0:n.call(t,...r)}),[])}Ox(an,"useCallbackRef");var Dx=Object.defineProperty,We=(e,t)=>Dx(e,"name",{value:t,configurable:!0}),Pl="dismissableLayer.update",Tx="dismissableLayer.pointerDownOutside",Mx="dismissableLayer.focusOutside",Gd,wh=g.createContext({layers:new Set,layersWithOutsidePointerEventsDisabled:new Set,branches:new Set,dismissableSurfaces:new Set}),Rx=g.forwardRef(We(function(t,r){const{disableOutsidePointerEvents:n=!1,deferPointerDownOutside:o=!1,onEscapeKeyDown:i,onPointerDownOutside:a,onFocusOutside:s,onInteractOutside:l,onDismiss:c,...d}=t,u=g.useContext(wh),[p,v]=g.useState(null),h=(p==null?void 0:p.ownerDocument)??(globalThis==null?void 0:globalThis.document),[,m]=g.useState({}),y=Wr(r,v),b=Array.from(u.layers),[k]=[...u.layersWithOutsidePointerEventsDisabled].slice(-1),x=k?b.indexOf(k):-1,_=p?b.indexOf(p):-1,I=u.layersWithOutsidePointerEventsDisabled.size>0,w=_>=x,A=g.useRef(!1),E=Sh(O=>{a==null||a(O),l==null||l(O),O.defaultPrevented||c==null||c()},{ownerDocument:h,deferPointerDownOutside:o,isDeferredPointerDownOutsideRef:A,dismissableSurfaces:u.dismissableSurfaces,shouldHandlePointerDownOutside:g.useCallback(O=>{if(!(O instanceof Node))return!1;const L=[...u.branches].some($=>$.contains(O));return w&&!L},[u.branches,w])}),C=Eh(O=>{if(o&&A.current)return;const L=O.target;[...u.branches].some(F=>F.contains(L))||(s==null||s(O),l==null||l(O),O.defaultPrevented||c==null||c())},h),S=p?_===b.length-1:!1,j=an(O=>{O.key==="Escape"&&(i==null||i(O),!O.defaultPrevented&&c&&(O.preventDefault(),c()))});return g.useEffect(()=>{if(S)return h.addEventListener("keydown",j,{capture:!0}),()=>h.removeEventListener("keydown",j,{capture:!0})},[h,S,j]),g.useEffect(()=>{if(p)return n&&(u.layersWithOutsidePointerEventsDisabled.size===0&&(Gd=h.body.style.pointerEvents,h.body.style.pointerEvents="none"),u.layersWithOutsidePointerEventsDisabled.add(p)),u.layers.add(p),zl(),()=>{n&&(u.layersWithOutsidePointerEventsDisabled.delete(p),u.layersWithOutsidePointerEventsDisabled.size===0&&(h.body.style.pointerEvents=Gd))}},[p,h,n,u]),g.useEffect(()=>()=>{p&&(u.layers.delete(p),u.layersWithOutsidePointerEventsDisabled.delete(p),zl())},[p,u]),g.useEffect(()=>{const O=We(()=>m({}),"handleUpdate");return document.addEventListener(Pl,O),()=>document.removeEventListener(Pl,O)},[]),f.jsx(oo.div,{...d,ref:y,style:{pointerEvents:I?w?"auto":"none":void 0,...t.style},onFocusCapture:Ar(t.onFocusCapture,C.onFocusCapture),onBlurCapture:Ar(t.onBlurCapture,C.onBlurCapture),onPointerDownCapture:Ar(t.onPointerDownCapture,E.onPointerDownCapture)})},"DismissableLayer"));function Lx(){const e=g.useContext(wh),[t,r]=g.useState(null);return g.useEffect(()=>{if(t)return e.dismissableSurfaces.add(t),()=>{e.dismissableSurfaces.delete(t)}},[t,e.dismissableSurfaces]),r}We(Lx,"useDismissableLayerSurface");var Fx=We(()=>!0,"IS_TRUE");function Sh(e,t){const{ownerDocument:r=globalThis==null?void 0:globalThis.document,deferPointerDownOutside:n=!1,isDeferredPointerDownOutsideRef:o,dismissableSurfaces:i,shouldHandlePointerDownOutside:a=Fx}=t,s=an(e),l=g.useRef(!1),c=g.useRef(!1),d=g.useRef(new Map),u=g.useRef(()=>{});return g.useEffect(()=>{function p(){c.current=!1,o.current=!1,d.current.clear()}We(p,"resetOutsideInteraction");function v(){return Array.from(d.current.values()).some(Boolean)}We(v,"isOutsideInteractionIntercepted");function h(x){if(!c.current)return;const _=x.target;_ instanceof Node&&[...i].some(w=>w.contains(_))||d.current.set(x.type,!0),x.type==="click"&&window.setTimeout(()=>{c.current&&u.current()},0)}We(h,"handleInteractionCapture");function m(x){c.current&&d.current.set(x.type,!1)}We(m,"handleInteractionBubble");const y=We(x=>{if(x.target&&!l.current){let _=function(){r.removeEventListener("click",u.current);const w=v();p(),w||qc(Tx,s,I,{discrete:!0})};if(We(_,"handleAndDispatchPointerDownOutsideEvent"),!a(x.target)){r.removeEventListener("click",u.current),p(),l.current=!1;return}const I={originalEvent:x};c.current=!0,o.current=n&&x.button===0,d.current.clear(),!n||x.button!==0?_():(r.removeEventListener("click",u.current),u.current=_,r.addEventListener("click",u.current,{once:!0}))}else r.removeEventListener("click",u.current),p();l.current=!1},"handlePointerDown"),b=["pointerup","mousedown","mouseup","touchstart","touchend","click"];for(const x of b)r.addEventListener(x,h,!0),r.addEventListener(x,m);const k=window.setTimeout(()=>{r.addEventListener("pointerdown",y)},0);return()=>{window.clearTimeout(k),r.removeEventListener("pointerdown",y),r.removeEventListener("click",u.current);for(const x of b)r.removeEventListener(x,h,!0),r.removeEventListener(x,m)}},[r,s,n,o,i,a]),{onPointerDownCapture:We(()=>l.current=!0,"onPointerDownCapture")}}We(Sh,"usePointerDownOutside");function Eh(e,t=globalThis==null?void 0:globalThis.document){const r=an(e),n=g.useRef(!1);return g.useEffect(()=>{const o=We(i=>{i.target&&!n.current&&qc(Mx,r,{originalEvent:i},{discrete:!1})},"handleFocus");return t.addEventListener("focusin",o),()=>t.removeEventListener("focusin",o)},[t,r]),{onFocusCapture:We(()=>n.current=!0,"onFocusCapture"),onBlurCapture:We(()=>n.current=!1,"onBlurCapture")}}We(Eh,"useFocusOutside");function zl(){const e=new CustomEvent(Pl);document.dispatchEvent(e)}We(zl,"dispatchUpdate");function qc(e,t,r,{discrete:n}){const o=r.originalEvent.target,i=new CustomEvent(e,{bubbles:!1,cancelable:!0,detail:r});t&&o.addEventListener(e,t,{once:!0}),n?kh(o,i):o.dispatchEvent(i)}We(qc,"handleAndDispatchCustomEvent");var Nx=Object.defineProperty,Uc=(e,t)=>Nx(e,"name",{value:t,configurable:!0}),Hi=0,Nt=null;function Bx(e){return Zc(),e.children}Uc(Bx,"FocusGuards");function Zc(){g.useEffect(()=>{Nt||(Nt={start:Al(),end:Al()});const{start:e,end:t}=Nt;return document.body.firstElementChild!==e&&document.body.insertAdjacentElement("afterbegin",e),document.body.lastElementChild!==t&&document.body.insertAdjacentElement("beforeend",t),Hi++,()=>{Hi===1&&(Nt==null||Nt.start.remove(),Nt==null||Nt.end.remove(),Nt=null),Hi=Math.max(0,Hi-1)}},[])}Uc(Zc,"useFocusGuards");function Al(){const e=document.createElement("span");return e.setAttribute("data-radix-focus-guard",""),e.tabIndex=0,e.style.outline="none",e.style.opacity="0",e.style.position="fixed",e.style.pointerEvents="none",e}Uc(Al,"createFocusGuard");var $x=Object.defineProperty,ot=(e,t)=>$x(e,"name",{value:t,configurable:!0}),Ts="focusScope.autoFocusOnMount",Ms="focusScope.autoFocusOnUnmount",Jd={bubbles:!1,cancelable:!0},Wx=g.forwardRef(ot(function(t,r){const{loop:n=!1,trapped:o=!1,onMountAutoFocus:i,onUnmountAutoFocus:a,...s}=t,[l,c]=g.useState(null),d=an(i),u=an(a),p=g.useRef(null),v=Wr(r,c),h=g.useRef({paused:!1,pause(){this.paused=!0},resume(){this.paused=!1}}).current;g.useEffect(()=>{if(o){let y=function(_){if(h.paused||!l)return;const I=_.target;l.contains(I)?p.current=I:nr(p.current,{select:!0})},b=function(_){if(h.paused||!l)return;const I=_.relatedTarget;I!==null&&(l.contains(I)||nr(p.current,{select:!0}))},k=function(_){if(document.activeElement===document.body)for(const w of _)w.removedNodes.length>0&&nr(l)};ot(y,"handleFocusIn"),ot(b,"handleFocusOut"),ot(k,"handleMutations"),document.addEventListener("focusin",y),document.addEventListener("focusout",b);const x=new MutationObserver(k);return l&&x.observe(l,{childList:!0,subtree:!0}),()=>{document.removeEventListener("focusin",y),document.removeEventListener("focusout",b),x.disconnect()}}},[o,l,h.paused]),g.useEffect(()=>{if(l){Qd.add(h);const y=document.activeElement;if(!l.contains(y)){const k=new CustomEvent(Ts,Jd);l.addEventListener(Ts,d),l.dispatchEvent(k),k.defaultPrevented||(Ih(jh(Yc(l)),{select:!0}),document.activeElement===y&&nr(l))}return()=>{l.removeEventListener(Ts,d),setTimeout(()=>{const k=new CustomEvent(Ms,Jd);l.addEventListener(Ms,u),l.dispatchEvent(k),k.defaultPrevented||nr(y??document.body,{select:!0}),l.removeEventListener(Ms,u),Qd.remove(h)},0)}}},[l,d,u,h]);const m=g.useCallback(y=>{if(!n&&!o||h.paused)return;const b=y.key==="Tab"&&!y.altKey&&!y.ctrlKey&&!y.metaKey,k=document.activeElement;if(b&&k){const x=y.currentTarget,[_,I]=Ch(x);_&&I?!y.shiftKey&&k===I?(y.preventDefault(),n&&nr(_,{select:!0})):y.shiftKey&&k===_&&(y.preventDefault(),n&&nr(I,{select:!0})):k===x&&y.preventDefault()}},[n,o,h.paused]);return f.jsx(oo.div,{tabIndex:-1,...s,ref:v,onKeyDown:m})},"FocusScope"));function Ih(e,{select:t=!1}={}){const r=document.activeElement;for(const n of e)if(nr(n,{select:t}),document.activeElement!==r)return}ot(Ih,"focusFirst");function Ch(e){const t=Yc(e),r=jl(t,e),n=jl(t.reverse(),e);return[r,n]}ot(Ch,"getTabbableEdges");function Yc(e){const t=[],r=document.createTreeWalker(e,NodeFilter.SHOW_ELEMENT,{acceptNode:ot(n=>{const o=n.tagName==="INPUT"&&n.type==="hidden";return n.disabled||n.hidden||o?NodeFilter.FILTER_SKIP:n.tabIndex>=0?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_SKIP},"acceptNode")});for(;r.nextNode();)t.push(r.currentNode);return t}ot(Yc,"getTabbableCandidates");function jl(e,t){const r=typeof t.checkVisibility=="function"&&t.checkVisibility({checkVisibilityCSS:!0});for(const n of e)if(!(r?!n.checkVisibility({checkVisibilityCSS:!0}):Ph(n,{upTo:t})))return n}ot(jl,"findVisible");function Ph(e,{upTo:t}){if(getComputedStyle(e).visibility==="hidden")return!0;for(;e;){if(t!==void 0&&e===t)return!1;if(getComputedStyle(e).display==="none")return!0;e=e.parentElement}return!1}ot(Ph,"isHidden");function zh(e){return e instanceof HTMLInputElement&&"select"in e}ot(zh,"isSelectableInput");function nr(e,{select:t=!1}={}){if(e&&e.focus){const r=document.activeElement;e.focus({preventScroll:!0}),e!==r&&zh(e)&&t&&e.select()}}ot(nr,"focus");var Qd=Ah();function Ah(){let e=[];return{add(t){const r=e[0];t!==r&&(r==null||r.pause()),e=Ol(e,t),e.unshift(t)},remove(t){var r;e=Ol(e,t),(r=e[0])==null||r.resume()}}}ot(Ah,"createFocusScopesStack");function Ol(e,t){const r=[...e],n=r.indexOf(t);return n!==-1&&r.splice(n,1),r}ot(Ol,"arrayRemove");function jh(e){return e.filter(t=>t.tagName!=="A")}ot(jh,"removeLinks");var Ut=globalThis!=null&&globalThis.document?g.useLayoutEffect:()=>{},Hx=Object.defineProperty,Vx=(e,t)=>Hx(e,"name",{value:t,configurable:!0}),qx=xi[" useId ".trim().toString()]||(()=>{}),Ux=0;function Oh(e){const[t,r]=g.useState(qx());return Ut(()=>{e||r(n=>n??String(Ux++))},[e]),e||(t?`radix-${t}`:"")}Vx(Oh,"useId");const Zx=["top","right","bottom","left"],Tr=Math.min,ir=Math.max,ja=Math.round,Vi=Math.floor,ar=e=>({x:e,y:e}),Yx={left:"right",right:"left",bottom:"top",top:"bottom"};function Dh(e,t,r){return ir(e,Tr(t,r))}function cr(e,t){return typeof e=="function"?e(t):e}function Mr(e){return e.split("-")[0]}function io(e){return e.split("-")[1]}function Kc(e){return e==="x"?"y":"x"}function Xc(e){return e==="y"?"height":"width"}function qt(e){const t=e[0];return t==="t"||t==="b"?"y":"x"}function Gc(e){return Kc(qt(e))}function Kx(e,t,r){r===void 0&&(r=!1);const n=io(e),o=Gc(e),i=Xc(o);let a=o==="x"?n===(r?"end":"start")?"right":"left":n==="start"?"bottom":"top";return t.reference[i]>t.floating[i]&&(a=Oa(a)),[a,Oa(a)]}function Xx(e){const t=Oa(e);return[Dl(e),t,Dl(t)]}function Dl(e){return e.includes("start")?e.replace("start","end"):e.replace("end","start")}const ep=["left","right"],tp=["right","left"],Gx=["top","bottom"],Jx=["bottom","top"];function Qx(e,t,r){switch(e){case"top":case"bottom":return r?t?tp:ep:t?ep:tp;case"left":case"right":return t?Gx:Jx;default:return[]}}function ek(e,t,r,n){const o=io(e);let i=Qx(Mr(e),r==="start",n);return o&&(i=i.map(a=>a+"-"+o),t&&(i=i.concat(i.map(Dl)))),i}function Oa(e){const t=Mr(e);return Yx[t]+e.slice(t.length)}function tk(e){var t,r,n,o;return{top:(t=e.top)!=null?t:0,right:(r=e.right)!=null?r:0,bottom:(n=e.bottom)!=null?n:0,left:(o=e.left)!=null?o:0}}function Th(e){return typeof e!="number"?tk(e):{top:e,right:e,bottom:e,left:e}}function Da(e){const{x:t,y:r,width:n,height:o}=e;return{width:n,height:o,top:r,left:t,right:t+n,bottom:r+o,x:t,y:r}}function rp(e,t,r){let{reference:n,floating:o}=e;const i=qt(t),a=Gc(t),s=Xc(a),l=Mr(t),c=i==="y",d=n.x+n.width/2-o.width/2,u=n.y+n.height/2-o.height/2,p=n[s]/2-o[s]/2;let v;switch(l){case"top":v={x:d,y:n.y-o.height};break;case"bottom":v={x:d,y:n.y+n.height};break;case"right":v={x:n.x+n.width,y:u};break;case"left":v={x:n.x-o.width,y:u};break;default:v={x:n.x,y:n.y}}const h=io(t);return h&&(v[a]+=p*(h==="end"?1:-1)*(r&&c?-1:1)),v}async function rk(e,t){var r;t===void 0&&(t={});const{x:n,y:o,platform:i,rects:a,elements:s,strategy:l}=e,{boundary:c="clippingAncestors",rootBoundary:d="viewport",elementContext:u="floating",altBoundary:p=!1,padding:v=0}=cr(t,e),h=Th(v),y=s[p?u==="floating"?"reference":"floating":u],b=Da(await i.getClippingRect({element:(r=await(i.isElement==null?void 0:i.isElement(y)))==null||r?y:y.contextElement||await(i.getDocumentElement==null?void 0:i.getDocumentElement(s.floating)),boundary:c,rootBoundary:d,strategy:l})),k=u==="floating"?{x:n,y:o,width:a.floating.width,height:a.floating.height}:a.reference,x=await(i.getOffsetParent==null?void 0:i.getOffsetParent(s.floating)),_=await(i.isElement==null?void 0:i.isElement(x))&&await(i.getScale==null?void 0:i.getScale(x))||{x:1,y:1},I=Da(i.convertOffsetParentRelativeRectToViewportRelativeRect?await i.convertOffsetParentRelativeRectToViewportRelativeRect({elements:s,rect:k,offsetParent:x,strategy:l}):k);return{top:(b.top-I.top+h.top)/_.y,bottom:(I.bottom-b.bottom+h.bottom)/_.y,left:(b.left-I.left+h.left)/_.x,right:(I.right-b.right+h.right)/_.x}}const nk=50,ok=async(e,t,r)=>{const{placement:n="bottom",strategy:o="absolute",middleware:i=[],platform:a}=r,s=a.detectOverflow?a:{...a,detectOverflow:rk},l=await(a.isRTL==null?void 0:a.isRTL(t));let c=await a.getElementRects({reference:e,floating:t,strategy:o}),{x:d,y:u}=rp(c,n,l),p=n,v=0;const h={};for(let m=0;m<i.length;m++){const y=i[m];if(!y)continue;const{name:b,fn:k}=y,{x,y:_,data:I,reset:w}=await k({x:d,y:u,initialPlacement:n,placement:p,strategy:o,middlewareData:h,rects:c,platform:s,elements:{reference:e,floating:t}});d=x??d,u=_??u,h[b]={...h[b],...I},w&&v<nk&&(v++,typeof w=="object"&&(w.placement&&(p=w.placement),w.rects&&(c=w.rects===!0?await a.getElementRects({reference:e,floating:t,strategy:o}):w.rects),{x:d,y:u}=rp(c,p,l)),m=-1)}return{x:d,y:u,placement:p,strategy:o,middlewareData:h}},ik=e=>({name:"arrow",options:e,async fn(t){const{x:r,y:n,placement:o,rects:i,platform:a,elements:s,middlewareData:l}=t,{element:c,padding:d=0}=cr(e,t)||{};if(c==null)return{};const u=Th(d),p={x:r,y:n},v=Gc(o),h=Xc(v),m=await a.getDimensions(c),y=v==="y",b=y?"top":"left",k=y?"bottom":"right",x=y?"clientHeight":"clientWidth",_=i.reference[h]+i.reference[v]-p[v]-i.floating[h],I=p[v]-i.reference[v],w=await(a.getOffsetParent==null?void 0:a.getOffsetParent(c));let A=w?w[x]:0;(!A||!await(a.isElement==null?void 0:a.isElement(w)))&&(A=s.floating[x]||i.floating[h]);const E=_/2-I/2,C=A/2-m[h]/2-1,S=Tr(u[b],C),j=Tr(u[k],C),O=A-m[h]-j,L=A/2-m[h]/2+E,$=Dh(S,L,O),F=!l.arrow&&io(o)!=null&&L!==$&&i.reference[h]/2-(L<S?S:j)-m[h]/2<0,M=F?L<S?L-S:L-O:0;return{[v]:p[v]+M,data:{[v]:$,centerOffset:L-$-M,...F&&{alignmentOffset:M}},reset:F}}}),ak=function(e){return e===void 0&&(e={}),{name:"flip",options:e,async fn(t){var r,n;const{placement:o,middlewareData:i,rects:a,initialPlacement:s,platform:l,elements:c}=t,{mainAxis:d=!0,crossAxis:u=!0,fallbackPlacements:p,fallbackStrategy:v="bestFit",fallbackAxisSideDirection:h="none",flipAlignment:m=!0,...y}=cr(e,t);if((r=i.arrow)!=null&&r.alignmentOffset)return{};const b=Mr(o),k=qt(s),x=Mr(s)===s,_=await(l.isRTL==null?void 0:l.isRTL(c.floating)),I=p||(x||!m?[Oa(s)]:Xx(s)),w=h!=="none";!p&&w&&I.push(...ek(s,m,h,_));const A=[s,...I],E=await l.detectOverflow(t,y),C=[];let S=((n=i.flip)==null?void 0:n.overflows)||[];if(d&&C.push(E[b]),u){const $=Kx(o,a,_);C.push(E[$[0]],E[$[1]])}if(S=[...S,{placement:o,overflows:C}],!C.every($=>$<=0)){var j,O;const $=(((j=i.flip)==null?void 0:j.index)||0)+1,F=A[$];if(F&&(!(u==="alignment"?k!==qt(F):!1)||S.every(W=>qt(W.placement)===k?W.overflows[0]>0:!0)))return{data:{index:$,overflows:S},reset:{placement:F}};let M=(O=S.filter(q=>q.overflows[0]<=0).sort((q,W)=>q.overflows[1]-W.overflows[1])[0])==null?void 0:O.placement;if(!M)switch(v){case"bestFit":{var L;const q=(L=S.filter(W=>{if(w){const B=qt(W.placement);return B===k||B==="y"}return!0}).map(W=>[W.placement,W.overflows.filter(B=>B>0).reduce((B,Z)=>B+Z,0)]).sort((W,B)=>W[1]-B[1])[0])==null?void 0:L[0];q&&(M=q);break}case"initialPlacement":M=s;break}if(o!==M)return{reset:{placement:M}}}return{}}}};function np(e,t){return{top:e.top-t.height,right:e.right-t.width,bottom:e.bottom-t.height,left:e.left-t.width}}function op(e){return Zx.some(t=>e[t]>=0)}const sk=function(e){return e===void 0&&(e={}),{name:"hide",options:e,async fn(t){const{rects:r,platform:n}=t,{strategy:o="referenceHidden",...i}=cr(e,t);switch(o){case"referenceHidden":{const a=await n.detectOverflow(t,{...i,elementContext:"reference"}),s=np(a,r.reference);return{data:{referenceHiddenOffsets:s,referenceHidden:op(s)}}}case"escaped":{const a=await n.detectOverflow(t,{...i,altBoundary:!0}),s=np(a,r.floating);return{data:{escapedOffsets:s,escaped:op(s)}}}default:return{}}}}},Mh=new Set(["left","top"]);async function lk(e,t){const{placement:r,platform:n,elements:o}=e,i=await(n.isRTL==null?void 0:n.isRTL(o.floating)),a=Mr(r),s=io(r),l=qt(r)==="y",c=Mh.has(a)?-1:1,d=i&&l?-1:1,u=cr(t,e);let{mainAxis:p,crossAxis:v,alignmentAxis:h}=typeof u=="number"?{mainAxis:u,crossAxis:0,alignmentAxis:null}:{mainAxis:u.mainAxis||0,crossAxis:u.crossAxis||0,alignmentAxis:u.alignmentAxis};return s&&typeof h=="number"&&(v=s==="end"?h*-1:h),l?{x:v*d,y:p*c}:{x:p*c,y:v*d}}const ck=function(e){return e===void 0&&(e=0),{name:"offset",options:e,async fn(t){var r,n;const{x:o,y:i,placement:a,middlewareData:s}=t,l=await lk(t,e);return a===((r=s.offset)==null?void 0:r.placement)&&(n=s.arrow)!=null&&n.alignmentOffset?{}:{x:o+l.x,y:i+l.y,data:{...l,placement:a}}}}},uk=function(e){return e===void 0&&(e={}),{name:"shift",options:e,async fn(t){const{x:r,y:n,placement:o,platform:i}=t,{mainAxis:a=!0,crossAxis:s=!1,limiter:l={fn:k=>{let{x,y:_}=k;return{x,y:_}}},...c}=cr(e,t),d={x:r,y:n},u=await i.detectOverflow(t,c),p=qt(o),v=Kc(p);let h=d[v],m=d[p];const y=(k,x)=>Dh(x+u[k==="y"?"top":"left"],x,x-u[k==="y"?"bottom":"right"]);a&&(h=y(v,h)),s&&(m=y(p,m));const b=l.fn({...t,[v]:h,[p]:m});return{...b,data:{x:b.x-r,y:b.y-n,enabled:{[v]:a,[p]:s}}}}}},dk=function(e){return e===void 0&&(e={}),{options:e,fn(t){var r,n;const{x:o,y:i,placement:a,rects:s,middlewareData:l}=t,{offset:c=0,mainAxis:d=!0,crossAxis:u=!0}=cr(e,t),p={x:o,y:i},v=qt(a),h=Kc(v);let m=p[h],y=p[v];const b=cr(c,t),k=typeof b=="number"?{mainAxis:b,crossAxis:0}:{mainAxis:(r=b.mainAxis)!=null?r:0,crossAxis:(n=b.crossAxis)!=null?n:0};if(d){const I=h==="y"?"height":"width",w=s.reference[h]-s.floating[I]+k.mainAxis,A=s.reference[h]+s.reference[I]-k.mainAxis;m<w?m=w:m>A&&(m=A)}if(u){var x,_;const I=h==="y"?"width":"height",w=Mh.has(Mr(a)),A=s.reference[v]-s.floating[I]+(w&&((x=l.offset)==null?void 0:x[v])||0)+(w?0:k.crossAxis),E=s.reference[v]+s.reference[I]+(w?0:((_=l.offset)==null?void 0:_[v])||0)-(w?k.crossAxis:0);y<A?y=A:y>E&&(y=E)}return{[h]:m,[v]:y}}}},pk=function(e){return e===void 0&&(e={}),{name:"size",options:e,async fn(t){const{placement:r,rects:n,platform:o,elements:i}=t,{apply:a=()=>{},...s}=cr(e,t),l=await o.detectOverflow(t,s),c=Mr(r),d=io(r),u=qt(r)==="y",{width:p,height:v}=n.floating;let h,m;c==="top"||c==="bottom"?(h=c,m=d===(await(o.isRTL==null?void 0:o.isRTL(i.floating))?"start":"end")?"left":"right"):(m=c,h=d==="end"?"top":"bottom");const y=v-l.top-l.bottom,b=p-l.left-l.right,k=Tr(v-l[h],y),x=Tr(p-l[m],b),_=t.middlewareData.shift,I=!_;let w=k,A=x;_!=null&&_.enabled.x&&(A=b),_!=null&&_.enabled.y&&(w=y),I&&!d&&(u?A=p-2*ir(l.left,l.right):w=v-2*ir(l.top,l.bottom)),await a({...t,availableWidth:A,availableHeight:w});const E=await o.getDimensions(i.floating);return p!==E.width||v!==E.height?{reset:{rects:!0}}:{}}}};function rs(){return typeof window<"u"}function ao(e){return Rh(e)?(e.nodeName||"").toLowerCase():"#document"}function ut(e){var t;return(e==null||(t=e.ownerDocument)==null?void 0:t.defaultView)||window}function fr(e){var t;return(t=(Rh(e)?e.ownerDocument:e.document)||window.document)==null?void 0:t.documentElement}function Rh(e){return rs()?e instanceof Node||e instanceof ut(e).Node:!1}function Yt(e){return rs()?e instanceof Element||e instanceof ut(e).Element:!1}function Hr(e){return rs()?e instanceof HTMLElement||e instanceof ut(e).HTMLElement:!1}function ip(e){return!rs()||typeof ShadowRoot>"u"?!1:e instanceof ShadowRoot||e instanceof ut(e).ShadowRoot}function ns(e){const{overflow:t,overflowX:r,overflowY:n,display:o}=Kt(e);return/auto|scroll|overlay|hidden|clip/.test(t+n+r)&&o!=="inline"&&o!=="contents"}function fk(e){return/^(table|td|th)$/.test(ao(e))}function os(e){try{if(e.matches(":popover-open"))return!0}catch{}try{return e.matches(":modal")}catch{return!1}}const hk=/transform|translate|scale|rotate|perspective|filter/,vk=/paint|layout|strict|content/,Ur=e=>!!e&&e!=="none";let Rs;function Jc(e){const t=Yt(e)?Kt(e):e;return Ur(t.transform)||Ur(t.translate)||Ur(t.scale)||Ur(t.rotate)||Ur(t.perspective)||!Qc()&&(Ur(t.backdropFilter)||Ur(t.filter))||hk.test(t.willChange||"")||vk.test(t.contain||"")}function gk(e){let t=sn(e);for(;Hr(t)&&!ii(t);){if(Jc(t))return t;if(os(t))return null;t=sn(t)}return null}function Qc(){return Rs==null&&(Rs=typeof CSS<"u"&&CSS.supports&&CSS.supports("-webkit-backdrop-filter","none")),Rs}function ii(e){return/^(html|body|#document)$/.test(ao(e))}function Kt(e){return ut(e).getComputedStyle(e)}function is(e){return Yt(e)?{scrollLeft:e.scrollLeft,scrollTop:e.scrollTop}:{scrollLeft:e.scrollX,scrollTop:e.scrollY}}function sn(e){if(ao(e)==="html")return e;const t=e.assignedSlot||e.parentNode||ip(e)&&e.host||fr(e);return ip(t)?t.host:t}function Lh(e){const t=sn(e);return ii(t)?(e.ownerDocument||e).body:Hr(t)&&ns(t)?t:Lh(t)}function ai(e,t,r){var n;t===void 0&&(t=[]),r===void 0&&(r=!0);const o=Lh(e),i=o===((n=e.ownerDocument)==null?void 0:n.body),a=ut(o);if(i){const s=Tl(a);return t.concat(a,a.visualViewport||[],ns(o)?o:[],s&&r?ai(s):[])}else return t.concat(o,ai(o,[],r))}function Tl(e){return e.parent&&Object.getPrototypeOf(e.parent)?e.frameElement:null}function Fh(e){const t=Kt(e);let r=parseFloat(t.width)||0,n=parseFloat(t.height)||0;const o=Hr(e),i=o?e.offsetWidth:r,a=o?e.offsetHeight:n,s=ja(r)!==i||ja(n)!==a;return s&&(r=i,n=a),{width:r,height:n,$:s}}function eu(e){return Yt(e)?e:e.contextElement}function Vn(e){const t=eu(e);if(!Hr(t))return ar(1);const r=t.getBoundingClientRect(),{width:n,height:o,$:i}=Fh(t);let a=(i?ja(r.width):r.width)/n,s=(i?ja(r.height):r.height)/o;return(!a||!Number.isFinite(a))&&(a=1),(!s||!Number.isFinite(s))&&(s=1),{x:a,y:s}}const mk=ar(0);function Nh(e){const t=ut(e);return!Qc()||!t.visualViewport?mk:{x:t.visualViewport.offsetLeft,y:t.visualViewport.offsetTop}}function _k(e,t,r){return t===void 0&&(t=!1),!!r&&t&&r===ut(e)}function ln(e,t,r,n){t===void 0&&(t=!1),r===void 0&&(r=!1);const o=e.getBoundingClientRect(),i=eu(e);let a=ar(1);t&&(n?Yt(n)&&(a=Vn(n)):a=Vn(e));const s=_k(i,r,n)?Nh(i):ar(0);let l=(o.left+s.x)/a.x,c=(o.top+s.y)/a.y,d=o.width/a.x,u=o.height/a.y;if(i&&n){const p=ut(i),v=Yt(n)?ut(n):n;let h=p,m=Tl(h);for(;m&&v!==h;){const y=Vn(m),b=m.getBoundingClientRect(),k=Kt(m),x=b.left+(m.clientLeft+parseFloat(k.paddingLeft))*y.x,_=b.top+(m.clientTop+parseFloat(k.paddingTop))*y.y;l*=y.x,c*=y.y,d*=y.x,u*=y.y,l+=x,c+=_,h=ut(m),m=Tl(h)}}return Da({width:d,height:u,x:l,y:c})}function as(e,t){const r=is(e).scrollLeft;return t?t.left+r:ln(fr(e)).left+r}function Bh(e,t){const r=e.getBoundingClientRect(),n=r.left+t.scrollLeft-as(e,r),o=r.top+t.scrollTop;return{x:n,y:o}}function yk(e){let{elements:t,rect:r,offsetParent:n,strategy:o}=e;const i=o==="fixed",a=fr(n),s=t?os(t.floating):!1;if(n===a||s&&i)return r;let l={scrollLeft:0,scrollTop:0},c=ar(1);const d=ar(0),u=Hr(n);if((u||!i)&&((ao(n)!=="body"||ns(a))&&(l=is(n)),u)){const v=ln(n);c=Vn(n),d.x=v.x+n.clientLeft,d.y=v.y+n.clientTop}const p=a&&!u&&!i?Bh(a,l):ar(0);return{width:r.width*c.x,height:r.height*c.y,x:r.x*c.x-l.scrollLeft*c.x+d.x+p.x,y:r.y*c.y-l.scrollTop*c.y+d.y+p.y}}function bk(e){return e.getClientRects?Array.from(e.getClientRects()):[]}function xk(e){const t=is(e),r=e.ownerDocument.body,n=ir(e.scrollWidth,e.clientWidth,r.scrollWidth,r.clientWidth),o=ir(e.scrollHeight,e.clientHeight,r.scrollHeight,r.clientHeight);let i=-t.scrollLeft+as(e);const a=-t.scrollTop;return Kt(r).direction==="rtl"&&(i+=ir(e.clientWidth,r.clientWidth)-n),{width:n,height:o,x:i,y:a}}const kk=25;function wk(e,t,r){r===void 0&&(r="viewport");const n=r==="layoutViewport",o=ut(e),i=fr(e),a=o.visualViewport;let s=i.clientWidth,l=i.clientHeight,c=0,d=0;if(a){const p=!Qc()||t==="fixed";n?p||(c=-a.offsetLeft,d=-a.offsetTop):(s=a.width,l=a.height,p&&(c=a.offsetLeft,d=a.offsetTop))}if(as(i)<=0){const p=i.ownerDocument,v=p.body,h=getComputedStyle(v),m=p.compatMode==="CSS1Compat"&&parseFloat(h.marginLeft)+parseFloat(h.marginRight)||0,y=Math.abs(i.clientWidth-v.clientWidth-m),b=getComputedStyle(i).scrollbarGutter==="stable both-edges"?y/2:y;b<=kk&&(s-=b)}return{width:s,height:l,x:c,y:d}}function Sk(e,t){const r=ln(e,!0,t==="fixed"),n=r.top+e.clientTop,o=r.left+e.clientLeft,i=Vn(e),a=e.clientWidth*i.x,s=e.clientHeight*i.y,l=o*i.x,c=n*i.y;return{width:a,height:s,x:l,y:c}}function ap(e,t,r){let n;if(t==="viewport"||t==="layoutViewport")n=wk(e,r,t);else if(t==="document")n=xk(fr(e));else if(Yt(t))n=Sk(t,r);else{const o=Nh(e);n={x:t.x-o.x,y:t.y-o.y,width:t.width,height:t.height}}return Da(n)}function Ek(e,t){const r=t.get(e);if(r)return r;let n=ai(e,[],!1).filter(s=>Yt(s)&&ao(s)!=="body"),o=null;const i=Kt(e).position==="fixed";let a=i?sn(e):e;for(;Yt(a)&&!ii(a);){const s=Kt(a),l=Jc(a),c=o?o.position:i?"fixed":"";!l&&(c==="fixed"||c==="absolute"&&s.position==="static")?n=n.filter(u=>u!==a):o=s,a=sn(a)}return t.set(e,n),n}function Ik(e){let{element:t,boundary:r,rootBoundary:n,strategy:o}=e;const a=[...r==="clippingAncestors"?os(t)?[]:Ek(t,this._c):[].concat(r),n],s=ap(t,a[0],o);let l=s.top,c=s.right,d=s.bottom,u=s.left;for(let p=1;p<a.length;p++){const v=ap(t,a[p],o);l=ir(v.top,l),c=Tr(v.right,c),d=Tr(v.bottom,d),u=ir(v.left,u)}return{width:c-u,height:d-l,x:u,y:l}}function Ck(e){const{width:t,height:r}=Fh(e);return{width:t,height:r}}function Pk(e,t,r){const n=Hr(t),o=fr(t),i=r==="fixed",a=ln(e,!0,i,t);let s={scrollLeft:0,scrollTop:0};const l=ar(0);if((n||!i)&&((ao(t)!=="body"||ns(o))&&(s=is(t)),n)){const p=ln(t,!0,i,t);l.x=p.x+t.clientLeft,l.y=p.y+t.clientTop}!n&&o&&(l.x=as(o));const c=o&&!n&&!i?Bh(o,s):ar(0),d=a.left+s.scrollLeft-l.x-c.x,u=a.top+s.scrollTop-l.y-c.y;return{x:d,y:u,width:a.width,height:a.height}}function Ls(e){return Kt(e).position==="static"}function sp(e,t){if(!Hr(e)||Kt(e).position==="fixed")return null;if(t)return t(e);let r=e.offsetParent;return fr(e)===r&&(r=r.ownerDocument.body),r}function $h(e,t){const r=ut(e);if(os(e))return r;if(!Hr(e)){let o=sn(e);for(;o&&!ii(o);){if(Yt(o)&&!Ls(o))return o;o=sn(o)}return r}let n=sp(e,t);for(;n&&fk(n)&&Ls(n);)n=sp(n,t);return n&&ii(n)&&Ls(n)&&!Jc(n)?r:n||gk(e)||r}const zk=async function(e){const t=this.getOffsetParent||$h,r=this.getDimensions,n=await r(e.floating);return{reference:Pk(e.reference,await t(e.floating),e.strategy),floating:{x:0,y:0,width:n.width,height:n.height}}};function Ak(e){return Kt(e).direction==="rtl"}const jk={convertOffsetParentRelativeRectToViewportRelativeRect:yk,getDocumentElement:fr,getClippingRect:Ik,getOffsetParent:$h,getElementRects:zk,getClientRects:bk,getDimensions:Ck,getScale:Vn,isElement:Yt,isRTL:Ak};function Wh(e,t){return e.x===t.x&&e.y===t.y&&e.width===t.width&&e.height===t.height}function Ok(e,t,r){let n=null,o;const i=fr(e);function a(){var d;clearTimeout(o),(d=n)==null||d.disconnect(),n=null}function s(d,u){d===void 0&&(d=!1),u===void 0&&(u=1),a();const p=e.getBoundingClientRect(),{left:v,top:h,width:m,height:y}=p;if(d||t(),!m||!y)return;const b=Vi(h),k=Vi(i.clientWidth-(v+m)),x=Vi(i.clientHeight-(h+y)),_=Vi(v),w={rootMargin:-b+"px "+-k+"px "+-x+"px "+-_+"px",threshold:ir(0,Tr(1,u))||1};let A=!0;function E(C){const S=C[0].intersectionRatio;if(!Wh(p,e.getBoundingClientRect()))return s();if(S!==u){if(!A)return s();S?s(!1,S):o=setTimeout(()=>{s(!1,1e-7)},1e3)}A=!1}try{n=new IntersectionObserver(E,{...w,root:i.ownerDocument})}catch{n=new IntersectionObserver(E,w)}n.observe(e)}const l=ut(e),c=()=>s(r);return l.addEventListener("resize",c),s(!0),()=>{l.removeEventListener("resize",c),a()}}function Dk(e,t,r,n){n===void 0&&(n={});const{ancestorScroll:o=!0,ancestorResize:i=!0,elementResize:a=typeof ResizeObserver=="function",layoutShift:s=typeof IntersectionObserver=="function",animationFrame:l=!1}=n,c=eu(e),d=o||i?[...c?ai(c):[],...t?ai(t):[]]:[];d.forEach(b=>{o&&b.addEventListener("scroll",r),i&&b.addEventListener("resize",r)});const u=c&&s?Ok(c,r,i):null;let p=-1,v=null;a&&(v=new ResizeObserver(b=>{let[k]=b;k&&k.target===c&&v&&t&&(v.unobserve(t),cancelAnimationFrame(p),p=requestAnimationFrame(()=>{var x;(x=v)==null||x.observe(t)})),r()}),c&&!l&&v.observe(c),t&&v.observe(t));let h,m=l?ln(e):null;l&&y();function y(){const b=ln(e);m&&!Wh(m,b)&&r(),m=b,h=requestAnimationFrame(y)}return r(),()=>{var b;d.forEach(k=>{o&&k.removeEventListener("scroll",r),i&&k.removeEventListener("resize",r)}),u==null||u(),(b=v)==null||b.disconnect(),v=null,l&&cancelAnimationFrame(h)}}const Tk=ck,Mk=uk,Rk=ak,Lk=pk,Fk=sk,lp=ik,Nk=dk,Bk=(e,t,r)=>{const n=new Map,o=r??{},i={...jk,...o.platform,_c:n};return ok(e,t,{...o,platform:i})};var $k=typeof document<"u",Wk=function(){},ha=$k?g.useLayoutEffect:Wk;function Ta(e,t){if(e===t)return!0;if(typeof e!=typeof t)return!1;if(typeof e=="function"&&e.toString()===t.toString())return!0;let r,n,o;if(e&&t&&typeof e=="object"){if(Array.isArray(e)){if(r=e.length,r!==t.length)return!1;for(n=r;n--!==0;)if(!Ta(e[n],t[n]))return!1;return!0}if(o=Object.keys(e),r=o.length,r!==Object.keys(t).length)return!1;for(n=r;n--!==0;)if(!{}.hasOwnProperty.call(t,o[n]))return!1;for(n=r;n--!==0;){const i=o[n];if(!(i==="_owner"&&e.$$typeof)&&!Ta(e[i],t[i]))return!1}return!0}return e!==e&&t!==t}function Hh(e){return typeof window>"u"?1:(e.ownerDocument.defaultView||window).devicePixelRatio||1}function cp(e,t){const r=Hh(e);return Math.round(t*r)/r}function Fs(e){const t=g.useRef(e);return ha(()=>{t.current=e}),t}function Hk(e){e===void 0&&(e={});const{placement:t="bottom",strategy:r="absolute",middleware:n=[],platform:o,elements:{reference:i,floating:a}={},transform:s=!0,whileElementsMounted:l,open:c}=e,[d,u]=g.useState({x:0,y:0,strategy:r,placement:t,middlewareData:{},isPositioned:!1}),[p,v]=g.useState(n);Ta(p,n)||v(n);const[h,m]=g.useState(null),[y,b]=g.useState(null),k=g.useCallback(W=>{W!==w.current&&(w.current=W,m(W))},[]),x=g.useCallback(W=>{W!==A.current&&(A.current=W,b(W))},[]),_=i||h,I=a||y,w=g.useRef(null),A=g.useRef(null),E=g.useRef(d),C=l!=null,S=Fs(l),j=Fs(o),O=Fs(c),L=g.useCallback(()=>{if(!w.current||!A.current)return;const W={placement:t,strategy:r,middleware:p};j.current&&(W.platform=j.current),Bk(w.current,A.current,W).then(B=>{const Z={...B,isPositioned:O.current!==!1};$.current&&!Ta(E.current,Z)&&(E.current=Z,pr.flushSync(()=>{u(Z)}))})},[p,t,r,j,O]);ha(()=>{c===!1&&E.current.isPositioned&&(E.current.isPositioned=!1,u(W=>({...W,isPositioned:!1})))},[c]);const $=g.useRef(!1);ha(()=>($.current=!0,()=>{$.current=!1}),[]),ha(()=>{if(_&&(w.current=_),I&&(A.current=I),_&&I){if(S.current)return S.current(_,I,L);L()}},[_,I,L,S,C]);const F=g.useMemo(()=>({reference:w,floating:A,setReference:k,setFloating:x}),[k,x]),M=g.useMemo(()=>({reference:_,floating:I}),[_,I]),q=g.useMemo(()=>{const W={position:r,left:0,top:0};if(!M.floating)return W;const B=cp(M.floating,d.x),Z=cp(M.floating,d.y);return s?{...W,transform:"translate("+B+"px, "+Z+"px)",...Hh(M.floating)>=1.5&&{willChange:"transform"}}:{position:r,left:B,top:Z}},[r,s,M.floating,d.x,d.y]);return g.useMemo(()=>({...d,update:L,refs:F,elements:M,floatingStyles:q}),[d,L,F,M,q])}const Vk=e=>{function t(r){return{}.hasOwnProperty.call(r,"current")}return{name:"arrow",options:e,fn(r){const{element:n,padding:o}=typeof e=="function"?e(r):e;return n&&t(n)?n.current!=null?lp({element:n.current,padding:o}).fn(r):{}:n?lp({element:n,padding:o}).fn(r):{}}}},qk=(e,t)=>{const r=Tk(e);return{name:r.name,fn:r.fn,options:[e,t]}},Uk=(e,t)=>{const r=Mk(e);return{name:r.name,fn:r.fn,options:[e,t]}},Zk=(e,t)=>({fn:Nk(e).fn,options:[e,t]}),Yk=(e,t)=>{const r=Rk(e);return{name:r.name,fn:r.fn,options:[e,t]}},Kk=(e,t)=>{const r=Lk(e);return{name:r.name,fn:r.fn,options:[e,t]}},Xk=(e,t)=>{const r=Fk(e);return{name:r.name,fn:r.fn,options:[e,t]}},Gk=(e,t)=>{const r=Vk(e);return{name:r.name,fn:r.fn,options:[e,t]}};var Jk=Object.defineProperty,Qk=(e,t)=>Jk(e,"name",{value:t,configurable:!0});function Vh(e){const[t,r]=g.useState(void 0);return Ut(()=>{if(e){r({width:e.offsetWidth,height:e.offsetHeight});const n=new ResizeObserver(o=>{if(!Array.isArray(o)||!o.length)return;const i=o[0];let a,s;if("borderBoxSize"in i){const l=i.borderBoxSize,c=Array.isArray(l)?l[0]:l;a=c.inlineSize,s=c.blockSize}else a=e.offsetWidth,s=e.offsetHeight;r({width:a,height:s})});return n.observe(e,{box:"border-box"}),()=>n.unobserve(e)}else r(void 0)},[e]),t}Qk(Vh,"useSize");var e0=Object.defineProperty,jr=(e,t)=>e0(e,"name",{value:t,configurable:!0}),qh="Popper",[Uh,Zh]=Hc(qh),[t0,Yh]=Uh(qh),r0=jr(e=>{const{__scopePopper:t,children:r}=e,[n,o]=g.useState(null),[i,a]=g.useState(void 0);return f.jsx(t0,{scope:t,anchor:n,onAnchorChange:o,placementState:i,setPlacementState:a,children:r})},"Popper"),n0="PopperAnchor",o0=g.forwardRef(jr(function(t,r){const{__scopePopper:n,virtualRef:o,...i}=t,a=Yh(n0,n),s=g.useRef(null),l=a.onAnchorChange,c=g.useCallback(m=>{s.current=m,m&&l(m)},[l]),d=Wr(r,c),u=g.useRef(null);g.useEffect(()=>{if(!o)return;const m=u.current;u.current=o.current,m!==u.current&&l(u.current)});const p=a.placementState&&ss(a.placementState),v=p==null?void 0:p[0],h=p==null?void 0:p[1];return o?null:f.jsx(oo.div,{"data-radix-popper-side":v,"data-radix-popper-align":h,...i,ref:d})},"PopperAnchor")),Kh="PopperContent",[i0,Sj]=Uh(Kh),a0=g.forwardRef(jr(function(t,r){var P,T,R,U,V,G,ne;const{__scopePopper:n,side:o="bottom",sideOffset:i=0,align:a="center",alignOffset:s=0,arrowPadding:l=0,avoidCollisions:c=!0,collisionBoundary:d=[],collisionPadding:u=0,sticky:p="partial",hideWhenDetached:v=!1,updatePositionStrategy:h="optimized",onPlaced:m,...y}=t,b=Yh(Kh,n),[k,x]=g.useState(null),_=Wr(r,x),[I,w]=g.useState(null),A=Vh(I),E=(A==null?void 0:A.width)??0,C=(A==null?void 0:A.height)??0,S=o+(a!=="center"?"-"+a:""),j=typeof u=="number"?u:{top:0,right:0,bottom:0,left:0,...u},O=Array.isArray(d)?d:[d],L=O.length>0,$={padding:j,boundary:O.filter(Xh),altBoundary:L},{refs:F,floatingStyles:M,placement:q,isPositioned:W,middlewareData:B}=Hk({strategy:"fixed",placement:S,whileElementsMounted:jr((...ue)=>Dk(...ue,{animationFrame:h==="always"}),"whileElementsMounted"),elements:{reference:b.anchor},middleware:[qk({mainAxis:i+C,alignmentAxis:s}),c&&Uk({mainAxis:!0,crossAxis:!1,limiter:p==="partial"?Zk():void 0,...$}),c&&Yk({...$}),Kk({...$,apply:jr(({elements:ue,rects:ve,availableWidth:$e,availableHeight:je})=>{const{width:Ee,height:we}=ve.reference,he=ue.floating.style;he.setProperty("--radix-popper-available-width",`${$e}px`),he.setProperty("--radix-popper-available-height",`${je}px`),he.setProperty("--radix-popper-anchor-width",`${Ee}px`),he.setProperty("--radix-popper-anchor-height",`${we}px`)},"apply")}),I&&Gk({element:I,padding:l}),s0({arrowWidth:E,arrowHeight:C}),v&&Xk({strategy:"referenceHidden",...$,boundary:L?$.boundary:void 0})]}),Z=b.setPlacementState;Ut(()=>(Z(q),()=>{Z(void 0)}),[q,Z]);const[oe,K]=ss(q),te=an(m);Ut(()=>{W&&(te==null||te())},[W,te]);const be=(P=B.arrow)==null?void 0:P.x,Q=(T=B.arrow)==null?void 0:T.y,ie=((R=B.arrow)==null?void 0:R.centerOffset)!==0,[ke,Y]=g.useState();return Ut(()=>{k&&Y(window.getComputedStyle(k).zIndex)},[k]),f.jsx("div",{ref:F.setFloating,"data-radix-popper-content-wrapper":"",style:{...M,transform:W?M.transform:"translate(0, -200%)",minWidth:"max-content",zIndex:ke,"--radix-popper-transform-origin":[(U=B.transformOrigin)==null?void 0:U.x,(V=B.transformOrigin)==null?void 0:V.y].join(" "),...((G=B.hide)==null?void 0:G.referenceHidden)&&{visibility:"hidden",pointerEvents:"none"}},dir:t.dir,children:f.jsx(i0,{scope:n,placedSide:oe,placedAlign:K,onArrowChange:w,arrowX:be,arrowY:Q,shouldHideArrow:ie,children:f.jsx(oo.div,{"data-side":oe,"data-align":K,...y,ref:_,style:{...y.style,animation:W?(ne=y.style)==null?void 0:ne.animation:"none"}})})})},"PopperContent"));function Xh(e){return e!==null}jr(Xh,"isNotNull");var s0=jr(e=>({name:"transformOrigin",options:e,fn(t){var y,b,k;const{placement:r,rects:n,middlewareData:o}=t,a=((y=o.arrow)==null?void 0:y.centerOffset)!==0,s=a?0:e.arrowWidth,l=a?0:e.arrowHeight,[c,d]=ss(r),u={start:"0%",center:"50%",end:"100%"}[d],p=(((b=o.arrow)==null?void 0:b.x)??0)+s/2,v=(((k=o.arrow)==null?void 0:k.y)??0)+l/2;let h="",m="";return c==="bottom"?(h=a?u:`${p}px`,m=`${-l}px`):c==="top"?(h=a?u:`${p}px`,m=`${n.floating.height+l}px`):c==="right"?(h=`${-l}px`,m=a?u:`${v}px`):c==="left"&&(h=`${n.floating.width+l}px`,m=a?u:`${v}px`),{data:{x:h,y:m}}}}),"transformOrigin");function ss(e){const[t,r="center"]=e.split("-");return[t,r]}jr(ss,"getSideAndAlignFromPlacement");var l0=r0,c0=o0,u0=a0,d0=Object.defineProperty,p0=(e,t)=>d0(e,"name",{value:t,configurable:!0}),f0=g.forwardRef(p0(function(t,r){var l;const{container:n,...o}=t,[i,a]=g.useState(!1);Ut(()=>a(!0),[]);const s=n||i&&((l=globalThis==null?void 0:globalThis.document)==null?void 0:l.body);return s?pr.createPortal(f.jsx(oo.div,{...o,ref:r}),s):null},"Portal")),h0=Object.defineProperty,ur=(e,t)=>h0(e,"name",{value:t,configurable:!0});function Gh(e,t){return g.useReducer((r,n)=>t[r][n]??r,e)}ur(Gh,"useStateMachine");var Jh=ur(e=>{const{present:t,children:r}=e,n=Qh(t),o=typeof r=="function"?r({present:n.isPresent}):g.Children.only(r),i=ev(n.ref,tv(o));return typeof r=="function"||n.isPresent?g.cloneElement(o,{ref:i}):null},"Presence");function Qh(e){const[t,r]=g.useState(),n=g.useRef(null),o=g.useRef(e),i=g.useRef("none"),a=g.useRef(void 0),s=e?"mounted":"unmounted",[l,c]=Gh(s,{mounted:{UNMOUNT:"unmounted",ANIMATION_OUT:"unmountSuspended"},unmountSuspended:{MOUNT:"mounted",ANIMATION_END:"unmounted"},unmounted:{MOUNT:"mounted"}});return g.useEffect(()=>{l==="mounted"?(i.current=a.current??Dn(n.current),a.current=void 0):i.current="none"},[l]),Ut(()=>{const d=n.current,u=o.current;if(u!==e){const v=i.current,h=Dn(d);e?(a.current=h,c("MOUNT")):h==="none"||(d==null?void 0:d.display)==="none"?c("UNMOUNT"):c(u&&v!==h?"ANIMATION_OUT":"UNMOUNT"),o.current=e}},[e,c]),Ut(()=>{if(t){let d;const u=t.ownerDocument.defaultView??window,p=ur(h=>{const y=Dn(n.current).includes(CSS.escape(h.animationName));if(h.target===t&&y&&(c("ANIMATION_END"),!o.current)){const b=t.style.animationFillMode;t.style.animationFillMode="forwards",d=u.setTimeout(()=>{t.style.animationFillMode==="forwards"&&(t.style.animationFillMode=b)})}},"handleAnimationEnd"),v=ur(h=>{h.target===t&&(i.current=Dn(n.current))},"handleAnimationStart");return t.addEventListener("animationstart",v),t.addEventListener("animationcancel",p),t.addEventListener("animationend",p),()=>{u.clearTimeout(d),t.removeEventListener("animationstart",v),t.removeEventListener("animationcancel",p),t.removeEventListener("animationend",p)}}else c("ANIMATION_END")},[t,c]),{isPresent:["mounted","unmountSuspended"].includes(l),ref:g.useCallback(d=>{if(d){const u=getComputedStyle(d);n.current=u,a.current=Dn(u)}else n.current=null;r(d)},[])}}ur(Qh,"usePresence");function Ml(e,t){if(typeof e=="function")return e(t);e!=null&&(e.current=t)}ur(Ml,"setRef");function ev(...e){const t=g.useRef(e);return t.current=e,g.useCallback(r=>{const n=t.current;let o=!1;const i=n.map(a=>{const s=Ml(a,r);return!o&&typeof s=="function"&&(o=!0),s});if(o)return()=>{for(let a=0;a<i.length;a++){const s=i[a];typeof s=="function"?s():Ml(n[a],null)}}},[])}ur(ev,"useStableComposedRefs");function Dn(e){return(e==null?void 0:e.animationName)||"none"}ur(Dn,"getAnimationName");function tv(e){var n,o;let t=(n=Object.getOwnPropertyDescriptor(e.props,"ref"))==null?void 0:n.get,r=t&&"isReactWarning"in t&&t.isReactWarning;return r?e.ref:(t=(o=Object.getOwnPropertyDescriptor(e,"ref"))==null?void 0:o.get,r=t&&"isReactWarning"in t&&t.isReactWarning,r?e.props.ref:e.props.ref||e.ref)}ur(tv,"getElementRef");var v0=Object.defineProperty,g0=(e,t)=>v0(e,"name",{value:t,configurable:!0}),up=xi[" useEffectEvent ".trim().toString()],dp=xi[" useInsertionEffect ".trim().toString()];function rv(e){if(typeof up=="function")return up(e);const t=g.useRef(()=>{throw new Error("Cannot call an event handler while rendering.")});return typeof dp=="function"?dp(()=>{t.current=e}):Ut(()=>{t.current=e}),g.useMemo(()=>((...r)=>{var n;return(n=t.current)==null?void 0:n.call(t,...r)}),[])}g0(rv,"useEffectEvent");var m0=Object.defineProperty,ki=(e,t)=>m0(e,"name",{value:t,configurable:!0}),_0=xi[" useInsertionEffect ".trim().toString()]||Ut;function nv({prop:e,defaultProp:t,onChange:r=ki(()=>{},"onChange"),caller:n}){const[o,i,a]=ov({defaultProp:t,onChange:r}),s=e!==void 0,l=s?e:o,c=g.useCallback(d=>{var u;if(s){const p=iv(d)?d(e):d;p!==e&&((u=a.current)==null||u.call(a,p))}else i(d)},[s,e,i,a]);return[l,c]}ki(nv,"useControllableState");function ov({defaultProp:e,onChange:t}){const[r,n]=g.useState(e),o=g.useRef(r),i=g.useRef(t);return _0(()=>{i.current=t},[t]),g.useEffect(()=>{var a;o.current!==r&&((a=i.current)==null||a.call(i,r),o.current=r)},[r,o]),[r,n,i]}ki(ov,"useUncontrolledState");function iv(e){return typeof e=="function"}ki(iv,"isFunction");var pp=Symbol("RADIX:SYNC_STATE");function y0(e,t,r,n){const{prop:o,defaultProp:i,onChange:a,caller:s}=t,l=o!==void 0,c=rv(a),d=[{...r,state:i}];n&&d.push(n);const[u,p]=g.useReducer((y,b)=>{if(b.type===pp)return{...y,state:b.state};const k=e(y,b);return l&&!Object.is(k.state,y.state)&&c(k.state),k},...d),v=u.state,h=g.useRef(v);g.useEffect(()=>{h.current!==v&&(h.current=v,l||c(v))},[v,h,l]);const m=g.useMemo(()=>o!==void 0?{...u,state:o}:u,[u,o]);return g.useEffect(()=>{l&&!Object.is(o,u.state)&&p({type:pp,state:o})},[o,u.state,l]),[m,p]}ki(y0,"useControllableStateReducer");var b0=function(e){if(typeof document>"u")return null;var t=Array.isArray(e)?e[0]:e;return t.ownerDocument.body},wn=new WeakMap,qi=new WeakMap,Ui={},Ns=0,av=function(e){return e&&(e.host||av(e.parentNode))},x0=function(e,t){return t.map(function(r){if(e.contains(r))return r;var n=av(r);return n&&e.contains(n)?n:(console.error("aria-hidden",r,"in not contained inside",e,". Doing nothing"),null)}).filter(function(r){return!!r})},k0=function(e,t,r,n){var o=x0(t,Array.isArray(e)?e:[e]);Ui[r]||(Ui[r]=new WeakMap);var i=Ui[r],a=[],s=new Set,l=new Set(o),c=function(u){!u||s.has(u)||(s.add(u),c(u.parentNode))};o.forEach(c);var d=function(u){!u||l.has(u)||Array.prototype.forEach.call(u.children,function(p){if(s.has(p))d(p);else try{var v=p.getAttribute(n),h=v!==null&&v!=="false",m=(wn.get(p)||0)+1,y=(i.get(p)||0)+1;wn.set(p,m),i.set(p,y),a.push(p),m===1&&h&&qi.set(p,!0),y===1&&p.setAttribute(r,"true"),h||p.setAttribute(n,"true")}catch(b){console.error("aria-hidden: cannot operate on ",p,b)}})};return d(t),s.clear(),Ns++,function(){a.forEach(function(u){var p=wn.get(u)-1,v=i.get(u)-1;wn.set(u,p),i.set(u,v),p||(qi.has(u)||u.removeAttribute(n),qi.delete(u)),v||u.removeAttribute(r)}),Ns--,Ns||(wn=new WeakMap,wn=new WeakMap,qi=new WeakMap,Ui={})}},w0=function(e,t,r){r===void 0&&(r="data-aria-hidden");var n=Array.from(Array.isArray(e)?e:[e]),o=b0(e);return o?(n.push.apply(n,Array.from(o.querySelectorAll("[aria-live], script"))),k0(n,o,r,"aria-hidden")):function(){return null}},Vt=function(){return Vt=Object.assign||function(t){for(var r,n=1,o=arguments.length;n<o;n++){r=arguments[n];for(var i in r)Object.prototype.hasOwnProperty.call(r,i)&&(t[i]=r[i])}return t},Vt.apply(this,arguments)};function sv(e,t){var r={};for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var o=0,n=Object.getOwnPropertySymbols(e);o<n.length;o++)t.indexOf(n[o])<0&&Object.prototype.propertyIsEnumerable.call(e,n[o])&&(r[n[o]]=e[n[o]]);return r}function S0(e,t,r){if(r||arguments.length===2)for(var n=0,o=t.length,i;n<o;n++)(i||!(n in t))&&(i||(i=Array.prototype.slice.call(t,0,n)),i[n]=t[n]);return e.concat(i||Array.prototype.slice.call(t))}var va="right-scroll-bar-position",ga="width-before-scroll-bar",E0="with-scroll-bars-hidden",I0="--removed-body-scroll-bar-size";function Bs(e,t){return typeof e=="function"?e(t):e&&(e.current=t),e}function C0(e,t){var r=g.useState(function(){return{value:e,callback:t,facade:{get current(){return r.value},set current(n){var o=r.value;o!==n&&(r.value=n,r.callback(n,o))}}}})[0];return r.callback=t,r.facade}var P0=typeof window<"u"?g.useLayoutEffect:g.useEffect,fp=new WeakMap;function z0(e,t){var r=C0(null,function(n){return e.forEach(function(o){return Bs(o,n)})});return P0(function(){var n=fp.get(r);if(n){var o=new Set(n),i=new Set(e),a=r.current;o.forEach(function(s){i.has(s)||Bs(s,null)}),i.forEach(function(s){o.has(s)||Bs(s,a)})}fp.set(r,e)},[e]),r}function A0(e){return e}function j0(e,t){t===void 0&&(t=A0);var r=[],n=!1,o={read:function(){if(n)throw new Error("Sidecar: could not `read` from an `assigned` medium. `read` could be used only with `useMedium`.");return r.length?r[r.length-1]:e},useMedium:function(i){var a=t(i,n);return r.push(a),function(){r=r.filter(function(s){return s!==a})}},assignSyncMedium:function(i){for(n=!0;r.length;){var a=r;r=[],a.forEach(i)}r={push:function(s){return i(s)},filter:function(){return r}}},assignMedium:function(i){n=!0;var a=[];if(r.length){var s=r;r=[],s.forEach(i),a=r}var l=function(){var d=a;a=[],d.forEach(i)},c=function(){return Promise.resolve().then(l)};c(),r={push:function(d){a.push(d),c()},filter:function(d){return a=a.filter(d),r}}}};return o}function O0(e){e===void 0&&(e={});var t=j0(null);return t.options=Vt({async:!0,ssr:!1},e),t}var lv=function(e){var t=e.sideCar,r=sv(e,["sideCar"]);if(!t)throw new Error("Sidecar: please provide `sideCar` property to import the right car");var n=t.read();if(!n)throw new Error("Sidecar medium not found");return g.createElement(n,Vt({},r))};lv.isSideCarExport=!0;function D0(e,t){return e.useMedium(t),lv}var cv=O0(),$s=function(){},ls=g.forwardRef(function(e,t){var r=g.useRef(null),n=g.useState({onScrollCapture:$s,onWheelCapture:$s,onTouchMoveCapture:$s}),o=n[0],i=n[1],a=e.forwardProps,s=e.children,l=e.className,c=e.removeScrollBar,d=e.enabled,u=e.shards,p=e.sideCar,v=e.noRelative,h=e.noIsolation,m=e.inert,y=e.allowPinchZoom,b=e.as,k=b===void 0?"div":b,x=e.gapMode,_=sv(e,["forwardProps","children","className","removeScrollBar","enabled","shards","sideCar","noRelative","noIsolation","inert","allowPinchZoom","as","gapMode"]),I=p,w=z0([r,t]),A=Vt(Vt({},_),o);return g.createElement(g.Fragment,null,d&&g.createElement(I,{sideCar:cv,removeScrollBar:c,shards:u,noRelative:v,noIsolation:h,inert:m,setCallbacks:i,allowPinchZoom:!!y,lockRef:r,gapMode:x}),a?g.cloneElement(g.Children.only(s),Vt(Vt({},A),{ref:w})):g.createElement(k,Vt({},A,{className:l,ref:w}),s))});ls.defaultProps={enabled:!0,removeScrollBar:!0,inert:!1};ls.classNames={fullWidth:ga,zeroRight:va};var T0=function(){if(typeof __webpack_nonce__<"u")return __webpack_nonce__};function M0(){if(!document)return null;var e=document.createElement("style");e.type="text/css";var t=T0();return t&&e.setAttribute("nonce",t),e}function R0(e,t){e.styleSheet?e.styleSheet.cssText=t:e.appendChild(document.createTextNode(t))}function L0(e){var t=document.head||document.getElementsByTagName("head")[0];t.appendChild(e)}var F0=function(){var e=0,t=null;return{add:function(r){e==0&&(t=M0())&&(R0(t,r),L0(t)),e++},remove:function(){e--,!e&&t&&(t.parentNode&&t.parentNode.removeChild(t),t=null)}}},N0=function(){var e=F0();return function(t,r){g.useEffect(function(){return e.add(t),function(){e.remove()}},[t&&r])}},uv=function(){var e=N0(),t=function(r){var n=r.styles,o=r.dynamic;return e(n,o),null};return t},B0={left:0,top:0,right:0,gap:0},Ws=function(e){return parseInt(e||"",10)||0},$0=function(e){var t=window.getComputedStyle(document.body),r=t[e==="padding"?"paddingLeft":"marginLeft"],n=t[e==="padding"?"paddingTop":"marginTop"],o=t[e==="padding"?"paddingRight":"marginRight"];return[Ws(r),Ws(n),Ws(o)]},W0=function(e){if(e===void 0&&(e="margin"),typeof window>"u")return B0;var t=$0(e),r=document.documentElement.clientWidth,n=window.innerWidth;return{left:t[0],top:t[1],right:t[2],gap:Math.max(0,n-r+t[2]-t[0])}},H0=uv(),qn="data-scroll-locked",V0=function(e,t,r,n){var o=e.left,i=e.top,a=e.right,s=e.gap;return r===void 0&&(r="margin"),`
  .`.concat(E0,` {
   overflow: hidden `).concat(n,`;
   padding-right: `).concat(s,"px ").concat(n,`;
  }
  body[`).concat(qn,`] {
    overflow: hidden `).concat(n,`;
    overscroll-behavior: contain;
    `).concat([t&&"position: relative ".concat(n,";"),r==="margin"&&`
    padding-left: `.concat(o,`px;
    padding-top: `).concat(i,`px;
    padding-right: `).concat(a,`px;
    margin-left:0;
    margin-top:0;
    margin-right: `).concat(s,"px ").concat(n,`;
    `),r==="padding"&&"padding-right: ".concat(s,"px ").concat(n,";")].filter(Boolean).join(""),`
  }
  
  .`).concat(va,` {
    right: `).concat(s,"px ").concat(n,`;
  }
  
  .`).concat(ga,` {
    margin-right: `).concat(s,"px ").concat(n,`;
  }
  
  .`).concat(va," .").concat(va,` {
    right: 0 `).concat(n,`;
  }
  
  .`).concat(ga," .").concat(ga,` {
    margin-right: 0 `).concat(n,`;
  }
  
  body[`).concat(qn,`] {
    `).concat(I0,": ").concat(s,`px;
  }
`)},hp=function(){var e=parseInt(document.body.getAttribute(qn)||"0",10);return isFinite(e)?e:0},q0=function(){g.useEffect(function(){return document.body.setAttribute(qn,(hp()+1).toString()),function(){var e=hp()-1;e<=0?document.body.removeAttribute(qn):document.body.setAttribute(qn,e.toString())}},[])},U0=function(e){var t=e.noRelative,r=e.noImportant,n=e.gapMode,o=n===void 0?"margin":n;q0();var i=g.useMemo(function(){return W0(o)},[o]);return g.createElement(H0,{styles:V0(i,!t,o,r?"":"!important")})},Rl=!1;if(typeof window<"u")try{var Zi=Object.defineProperty({},"passive",{get:function(){return Rl=!0,!0}});window.addEventListener("test",Zi,Zi),window.removeEventListener("test",Zi,Zi)}catch{Rl=!1}var Sn=Rl?{passive:!1}:!1,Z0=function(e){return e.tagName==="TEXTAREA"},dv=function(e,t){if(!(e instanceof Element))return!1;var r=window.getComputedStyle(e);return r[t]!=="hidden"&&!(r.overflowY===r.overflowX&&!Z0(e)&&r[t]==="visible")},Y0=function(e){return dv(e,"overflowY")},K0=function(e){return dv(e,"overflowX")},vp=function(e,t){var r=t.ownerDocument,n=t;do{typeof ShadowRoot<"u"&&n instanceof ShadowRoot&&(n=n.host);var o=pv(e,n);if(o){var i=fv(e,n),a=i[1],s=i[2];if(a>s)return!0}n=n.parentNode}while(n&&n!==r.body);return!1},X0=function(e){var t=e.scrollTop,r=e.scrollHeight,n=e.clientHeight;return[t,r,n]},G0=function(e){var t=e.scrollLeft,r=e.scrollWidth,n=e.clientWidth;return[t,r,n]},pv=function(e,t){return e==="v"?Y0(t):K0(t)},fv=function(e,t){return e==="v"?X0(t):G0(t)},J0=function(e,t){return e==="h"&&t==="rtl"?-1:1},Q0=function(e,t,r,n,o){var i=J0(e,window.getComputedStyle(t).direction),a=i*n,s=r.target,l=t.contains(s),c=!1,d=a>0,u=0,p=0;do{if(!s)break;var v=fv(e,s),h=v[0],m=v[1],y=v[2],b=m-y-i*h;(h||b)&&pv(e,s)&&(u+=b,p+=h);var k=s.parentNode;s=k&&k.nodeType===Node.DOCUMENT_FRAGMENT_NODE?k.host:k}while(!l&&s!==document.body||l&&(t.contains(s)||t===s));return(d&&Math.abs(u)<1||!d&&Math.abs(p)<1)&&(c=!0),c},Yi=function(e){return"changedTouches"in e?[e.changedTouches[0].clientX,e.changedTouches[0].clientY]:[0,0]},gp=function(e){return[e.deltaX,e.deltaY]},mp=function(e){return e&&"current"in e?e.current:e},e1=function(e,t){return e[0]===t[0]&&e[1]===t[1]},t1=function(e){return`
  .block-interactivity-`.concat(e,` {pointer-events: none;}
  .allow-interactivity-`).concat(e,` {pointer-events: all;}
`)},r1=0,En=[];function n1(e){var t=g.useRef([]),r=g.useRef([0,0]),n=g.useRef(),o=g.useState(r1++)[0],i=g.useState(uv)[0],a=g.useRef(e);g.useEffect(function(){a.current=e},[e]),g.useEffect(function(){if(e.inert){document.body.classList.add("block-interactivity-".concat(o));var m=S0([e.lockRef.current],(e.shards||[]).map(mp),!0).filter(Boolean);return m.forEach(function(y){return y.classList.add("allow-interactivity-".concat(o))}),function(){document.body.classList.remove("block-interactivity-".concat(o)),m.forEach(function(y){return y.classList.remove("allow-interactivity-".concat(o))})}}},[e.inert,e.lockRef.current,e.shards]);var s=g.useCallback(function(m,y){if("touches"in m&&m.touches.length===2||m.type==="wheel"&&m.ctrlKey)return!a.current.allowPinchZoom;var b=Yi(m),k=r.current,x="deltaX"in m?m.deltaX:k[0]-b[0],_="deltaY"in m?m.deltaY:k[1]-b[1],I,w=m.target,A=Math.abs(x)>Math.abs(_)?"h":"v";if("touches"in m&&A==="h"&&w.type==="range")return!1;var E=window.getSelection(),C=E&&E.anchorNode,S=C?C===w||C.contains(w):!1;if(S)return!1;var j=vp(A,w);if(!j)return!0;if(j?I=A:(I=A==="v"?"h":"v",j=vp(A,w)),!j)return!1;if(!n.current&&"changedTouches"in m&&(x||_)&&(n.current=I),!I)return!0;var O=n.current||I;return Q0(O,y,m,O==="h"?x:_)},[]),l=g.useCallback(function(m){var y=m;if(!(!En.length||En[En.length-1]!==i)){var b="deltaY"in y?gp(y):Yi(y),k=t.current.filter(function(I){return I.name===y.type&&(I.target===y.target||y.target===I.shadowParent)&&e1(I.delta,b)})[0];if(k&&k.should){y.cancelable&&y.preventDefault();return}if(!k){var x=(a.current.shards||[]).map(mp).filter(Boolean).filter(function(I){return I.contains(y.target)}),_=x.length>0?s(y,x[0]):!a.current.noIsolation;_&&y.cancelable&&y.preventDefault()}}},[]),c=g.useCallback(function(m,y,b,k){var x={name:m,delta:y,target:b,should:k,shadowParent:o1(b)};t.current.push(x),setTimeout(function(){t.current=t.current.filter(function(_){return _!==x})},1)},[]),d=g.useCallback(function(m){r.current=Yi(m),n.current=void 0},[]),u=g.useCallback(function(m){c(m.type,gp(m),m.target,s(m,e.lockRef.current))},[]),p=g.useCallback(function(m){c(m.type,Yi(m),m.target,s(m,e.lockRef.current))},[]);g.useEffect(function(){return En.push(i),e.setCallbacks({onScrollCapture:u,onWheelCapture:u,onTouchMoveCapture:p}),document.addEventListener("wheel",l,Sn),document.addEventListener("touchmove",l,Sn),document.addEventListener("touchstart",d,Sn),function(){En=En.filter(function(m){return m!==i}),document.removeEventListener("wheel",l,Sn),document.removeEventListener("touchmove",l,Sn),document.removeEventListener("touchstart",d,Sn)}},[]);var v=e.removeScrollBar,h=e.inert;return g.createElement(g.Fragment,null,h?g.createElement(i,{styles:t1(o)}):null,v?g.createElement(U0,{noRelative:e.noRelative,gapMode:e.gapMode}):null)}function o1(e){for(var t=null;e!==null;)e instanceof ShadowRoot&&(t=e.host,e=e.host),e=e.parentNode;return t}const i1=D0(cv,n1);var hv=g.forwardRef(function(e,t){return g.createElement(ls,Vt({},e,{ref:t,sideCar:i1}))});hv.classNames=ls.classNames;var a1=Object.defineProperty,Vr=(e,t)=>a1(e,"name",{value:t,configurable:!0}),tu="Popover",[vv,Ej]=Hc(tu,[Zh]),ru=Zh(),[s1,so]=vv(tu),l1=Vr(e=>{const{__scopePopover:t,children:r,open:n,defaultOpen:o,onOpenChange:i,modal:a=!1}=e,s=ru(t),l=g.useRef(null),[c,d]=g.useState(!1),[u,p]=nv({prop:n,defaultProp:o??!1,onChange:i,caller:tu});return f.jsx(l0,{...s,children:f.jsx(s1,{scope:t,contentId:Oh(),triggerRef:l,open:u,onOpenChange:p,onOpenToggle:g.useCallback(()=>p(v=>!v),[p]),hasCustomAnchor:c,onCustomAnchorAdd:g.useCallback(()=>d(!0),[]),onCustomAnchorRemove:g.useCallback(()=>d(!1),[]),modal:a,children:r})})},"Popover"),c1="PopoverTrigger",u1=g.forwardRef(Vr(function(t,r){const{__scopePopover:n,...o}=t,i=so(c1,n),a=ru(n),s=Wr(r,i.triggerRef),l=f.jsx(oo.button,{type:"button","aria-haspopup":"dialog","aria-expanded":i.open,"aria-controls":i.open?i.contentId:void 0,"data-state":nu(i.open),...o,ref:s,onClick:Ar(t.onClick,i.onOpenToggle)});return i.hasCustomAnchor?l:f.jsx(c0,{asChild:!0,...a,children:l})},"PopoverTrigger")),gv="PopoverPortal",[d1,p1]=vv(gv,{forceMount:void 0}),f1=Vr(e=>{const{__scopePopover:t,forceMount:r,children:n,container:o}=e,i=so(gv,t);return f.jsx(d1,{scope:t,forceMount:r,children:f.jsx(Jh,{present:r||i.open,children:f.jsx(f0,{asChild:!0,container:o,children:n})})})},"PopoverPortal"),si="PopoverContent",h1=g.forwardRef(Vr(function(t,r){const n=p1(si,t.__scopePopover),{forceMount:o=n.forceMount,...i}=t,a=so(si,t.__scopePopover);return f.jsx(Jh,{present:o||a.open,children:a.modal?f.jsx(g1,{...i,ref:r}):f.jsx(m1,{...i,ref:r})})},"PopoverContent")),v1=Vc("PopoverContent.RemoveScroll"),g1=g.forwardRef(Vr(function(t,r){const n=so(si,t.__scopePopover),o=g.useRef(null),i=Wr(r,o),a=g.useRef(!1);return g.useEffect(()=>{const s=o.current;if(s)return w0(s)},[]),f.jsx(hv,{as:v1,allowPinchZoom:!0,children:f.jsx(mv,{...t,ref:i,trapFocus:n.open,disableOutsidePointerEvents:!0,onCloseAutoFocus:Ar(t.onCloseAutoFocus,s=>{var l;s.preventDefault(),a.current||(l=n.triggerRef.current)==null||l.focus()}),onPointerDownOutside:Ar(t.onPointerDownOutside,s=>{const l=s.detail.originalEvent,c=l.button===0&&l.ctrlKey===!0,d=l.button===2||c;a.current=d},{checkForDefaultPrevented:!1}),onFocusOutside:Ar(t.onFocusOutside,s=>s.preventDefault(),{checkForDefaultPrevented:!1})})})},"PopoverContentModal")),m1=g.forwardRef(Vr(function(t,r){const n=so(si,t.__scopePopover),o=g.useRef(!1),i=g.useRef(!1);return f.jsx(mv,{...t,ref:r,trapFocus:!1,disableOutsidePointerEvents:!1,onCloseAutoFocus:a=>{var s,l;(s=t.onCloseAutoFocus)==null||s.call(t,a),a.defaultPrevented||(o.current||(l=n.triggerRef.current)==null||l.focus(),a.preventDefault()),o.current=!1,i.current=!1},onInteractOutside:a=>{var c,d;(c=t.onInteractOutside)==null||c.call(t,a),a.defaultPrevented||(o.current=!0,a.detail.originalEvent.type==="pointerdown"&&(i.current=!0));const s=a.target;((d=n.triggerRef.current)==null?void 0:d.contains(s))&&a.preventDefault(),a.detail.originalEvent.type==="focusin"&&i.current&&a.preventDefault()}})},"PopoverContentNonModal")),mv=g.forwardRef(Vr(function(t,r){const{__scopePopover:n,trapFocus:o,onOpenAutoFocus:i,onCloseAutoFocus:a,disableOutsidePointerEvents:s,onEscapeKeyDown:l,onPointerDownOutside:c,onFocusOutside:d,onInteractOutside:u,...p}=t,v=so(si,n),h=ru(n);return Zc(),f.jsx(Wx,{asChild:!0,loop:!0,trapped:o,onMountAutoFocus:i,onUnmountAutoFocus:a,children:f.jsx(Rx,{asChild:!0,disableOutsidePointerEvents:s,onInteractOutside:u,onEscapeKeyDown:l,onPointerDownOutside:c,onFocusOutside:d,onDismiss:()=>v.onOpenChange(!1),deferPointerDownOutside:!0,children:f.jsx(u0,{"data-state":nu(v.open),role:"dialog",id:v.contentId,...h,...p,ref:r,style:{...p.style,"--radix-popover-content-transform-origin":"var(--radix-popper-transform-origin)","--radix-popover-content-available-width":"var(--radix-popper-available-width)","--radix-popover-content-available-height":"var(--radix-popper-available-height)","--radix-popover-trigger-width":"var(--radix-popper-anchor-width)","--radix-popover-trigger-height":"var(--radix-popper-anchor-height)"}})})})},"PopoverContentImpl"));function nu(e){return e?"open":"closed"}Vr(nu,"getState");z();z();var _v={ActionBar:"_ActionBar_5vdfr_1","ActionBar-label":"_ActionBar-label_5vdfr_17",ActionBarAction:"_ActionBarAction_5vdfr_30","ActionBar-group":"_ActionBar-group_5vdfr_38","ActionBarAction--disabled":"_ActionBarAction--disabled_5vdfr_74","ActionBarAction--active":"_ActionBarAction--active_5vdfr_104","ActionBar-separator":"_ActionBar-separator_5vdfr_117"},li=ee("ActionBar",_v),_1=ee("ActionBarAction",_v),ht=({label:e,children:t})=>f.jsxs("div",{className:li(),onClick:r=>{r.stopPropagation()},children:[e&&f.jsx(ht.Group,{children:f.jsx("div",{className:li("label"),children:e})}),t]}),cs=g.forwardRef((e,t)=>{var r=e,{children:n,label:o,onClick:i,active:a=!1,disabled:s}=r,l=Tt(r,["children","label","onClick","active","disabled"]);return f.jsx("button",N(D({type:"button"},l),{ref:t,className:_1({active:a,disabled:s}),onClick:i,title:o,tabIndex:0,disabled:s,children:n}))});cs.displayName="Action";var y1=({children:e})=>f.jsx("div",{className:li("group"),children:e}),b1=({label:e})=>f.jsx("div",{className:li("label"),children:e}),x1=()=>f.jsx("div",{className:li("separator")});ht.Action=cs;ht.Label=b1;ht.Group=y1;ht.Separator=x1;z();z();z();var k1=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase(),yv=(...e)=>e.filter((t,r,n)=>!!t&&t.trim()!==""&&n.indexOf(t)===r).join(" ").trim();z();z();var w1={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"},S1=g.forwardRef((e,t)=>{var r=e,{color:n="currentColor",size:o=24,strokeWidth:i=2,absoluteStrokeWidth:a,className:s="",children:l,iconNode:c}=r,d=Tt(r,["color","size","strokeWidth","absoluteStrokeWidth","className","children","iconNode"]);return g.createElement("svg",D(N(D({ref:t},w1),{width:o,height:o,stroke:n,strokeWidth:a?Number(i)*24/Number(o):i,className:yv("lucide",s)}),d),[...c.map(([u,p])=>g.createElement(u,p)),...Array.isArray(l)?l:[l]])}),re=(e,t)=>{const r=g.forwardRef((n,o)=>{var i=n,{className:a}=i,s=Tt(i,["className"]);return g.createElement(S1,D({ref:o,iconNode:t,className:yv(`lucide-${k1(e)}`,a)},s))});return r.displayName=`${e}`,r},ou=re("AlignLeft",[["path",{d:"M15 12H3",key:"6jk70r"}],["path",{d:"M17 18H3",key:"1amg6g"}],["path",{d:"M21 6H3",key:"1jwq7v"}]]);z();var E1=re("Heading",[["path",{d:"M6 12h12",key:"8npq4p"}],["path",{d:"M6 20V4",key:"1w1bmo"}],["path",{d:"M18 20V4",key:"o2hl4u"}]]);z();var us=re("List",[["path",{d:"M3 12h.01",key:"nlz23k"}],["path",{d:"M3 18h.01",key:"1tta3j"}],["path",{d:"M3 6h.01",key:"1rqtza"}],["path",{d:"M8 12h13",key:"1za7za"}],["path",{d:"M8 18h13",key:"1lx6n3"}],["path",{d:"M8 6h13",key:"ik3vkj"}]]);z();z();var bv=re("AlignCenter",[["path",{d:"M17 12H7",key:"16if0g"}],["path",{d:"M19 18H5",key:"18s9l3"}],["path",{d:"M21 6H3",key:"1jwq7v"}]]);z();var xv=re("AlignJustify",[["path",{d:"M3 12h18",key:"1i2n21"}],["path",{d:"M3 18h18",key:"1h113x"}],["path",{d:"M3 6h18",key:"d0wm0j"}]]);z();var kv=re("AlignRight",[["path",{d:"M21 12H9",key:"dn1m92"}],["path",{d:"M21 18H7",key:"1ygte8"}],["path",{d:"M21 6H3",key:"1jwq7v"}]]);z();var I1=re("Bold",[["path",{d:"M6 12h9a4 4 0 0 1 0 8H7a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h7a4 4 0 0 1 0 8",key:"mg9rjx"}]]);z();var ci=re("ChevronDown",[["path",{d:"m6 9 6 6 6-6",key:"qrunsl"}]]);z();var wv=re("ChevronRight",[["path",{d:"m9 18 6-6-6-6",key:"mthhwq"}]]);z();var Sv=re("ChevronUp",[["path",{d:"m18 15-6-6-6 6",key:"153udz"}]]);z();var C1=re("ChevronsDownUp",[["path",{d:"m7 20 5-5 5 5",key:"13a0gw"}],["path",{d:"m7 4 5 5 5-5",key:"1kwcof"}]]);z();var P1=re("CircleCheckBig",[["path",{d:"M21.801 10A10 10 0 1 1 17 3.335",key:"yps3ct"}],["path",{d:"m9 11 3 3L22 4",key:"1pflzl"}]]);z();var z1=re("Code",[["polyline",{points:"16 18 22 12 16 6",key:"z7tu5w"}],["polyline",{points:"8 6 2 12 8 18",key:"1eg1df"}]]);z();var iu=re("Copy",[["rect",{width:"14",height:"14",x:"8",y:"8",rx:"2",ry:"2",key:"17jyea"}],["path",{d:"M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2",key:"zix9uf"}]]);z();var A1=re("CornerLeftUp",[["polyline",{points:"14 9 9 4 4 9",key:"m9oyvo"}],["path",{d:"M20 20h-7a4 4 0 0 1-4-4V4",key:"1blwi3"}]]);z();var j1=re("EllipsisVertical",[["circle",{cx:"12",cy:"12",r:"1",key:"41hilf"}],["circle",{cx:"12",cy:"5",r:"1",key:"gxeob9"}],["circle",{cx:"12",cy:"19",r:"1",key:"lyex9k"}]]);z();var O1=re("Expand",[["path",{d:"m21 21-6-6m6 6v-4.8m0 4.8h-4.8",key:"1c15vz"}],["path",{d:"M3 16.2V21m0 0h4.8M3 21l6-6",key:"1fsnz2"}],["path",{d:"M21 7.8V3m0 0h-4.8M21 3l-6 6",key:"hawz9i"}],["path",{d:"M3 7.8V3m0 0h4.8M3 3l6 6",key:"u9ee12"}]]);z();var _p=re("Globe",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20",key:"13o1zl"}],["path",{d:"M2 12h20",key:"9i4pu4"}]]);z();var D1=re("Hammer",[["path",{d:"m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9",key:"eefl8a"}],["path",{d:"m18 15 4-4",key:"16gjal"}],["path",{d:"m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5",key:"b7pghm"}]]);z();var T1=re("Hash",[["line",{x1:"4",x2:"20",y1:"9",y2:"9",key:"4lhtct"}],["line",{x1:"4",x2:"20",y1:"15",y2:"15",key:"vyu0kd"}],["line",{x1:"10",x2:"8",y1:"3",y2:"21",key:"1ggp8o"}],["line",{x1:"16",x2:"14",y1:"3",y2:"21",key:"weycgp"}]]);z();var M1=re("Heading1",[["path",{d:"M4 12h8",key:"17cfdx"}],["path",{d:"M4 18V6",key:"1rz3zl"}],["path",{d:"M12 18V6",key:"zqpxq5"}],["path",{d:"m17 12 3-2v8",key:"1hhhft"}]]);z();var R1=re("Heading2",[["path",{d:"M4 12h8",key:"17cfdx"}],["path",{d:"M4 18V6",key:"1rz3zl"}],["path",{d:"M12 18V6",key:"zqpxq5"}],["path",{d:"M21 18h-4c0-4 4-3 4-6 0-1.5-2-2.5-4-1",key:"9jr5yi"}]]);z();var L1=re("Heading3",[["path",{d:"M4 12h8",key:"17cfdx"}],["path",{d:"M4 18V6",key:"1rz3zl"}],["path",{d:"M12 18V6",key:"zqpxq5"}],["path",{d:"M17.5 10.5c1.7-1 3.5 0 3.5 1.5a2 2 0 0 1-2 2",key:"68ncm8"}],["path",{d:"M17 17.5c2 1.5 4 .3 4-1.5a2 2 0 0 0-2-2",key:"1ejuhz"}]]);z();var F1=re("Heading4",[["path",{d:"M12 18V6",key:"zqpxq5"}],["path",{d:"M17 10v3a1 1 0 0 0 1 1h3",key:"tj5zdr"}],["path",{d:"M21 10v8",key:"1kdml4"}],["path",{d:"M4 12h8",key:"17cfdx"}],["path",{d:"M4 18V6",key:"1rz3zl"}]]);z();var N1=re("Heading5",[["path",{d:"M4 12h8",key:"17cfdx"}],["path",{d:"M4 18V6",key:"1rz3zl"}],["path",{d:"M12 18V6",key:"zqpxq5"}],["path",{d:"M17 13v-3h4",key:"1nvgqp"}],["path",{d:"M17 17.7c.4.2.8.3 1.3.3 1.5 0 2.7-1.1 2.7-2.5S19.8 13 18.3 13H17",key:"2nebdn"}]]);z();var B1=re("Heading6",[["path",{d:"M4 12h8",key:"17cfdx"}],["path",{d:"M4 18V6",key:"1rz3zl"}],["path",{d:"M12 18V6",key:"zqpxq5"}],["circle",{cx:"19",cy:"16",r:"2",key:"15mx69"}],["path",{d:"M20 10c-2 2-3 3.5-3 6",key:"f35dl0"}]]);z();var $1=re("Italic",[["line",{x1:"19",x2:"10",y1:"4",y2:"4",key:"15jd3p"}],["line",{x1:"14",x2:"5",y1:"20",y2:"20",key:"bu0au3"}],["line",{x1:"15",x2:"9",y1:"4",y2:"20",key:"uljnxc"}]]);z();var Ev=re("Layers",[["path",{d:"M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z",key:"zw3jo"}],["path",{d:"M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12",key:"1wduqc"}],["path",{d:"M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17",key:"kqbvx6"}]]);z();var W1=re("LayoutGrid",[["rect",{width:"7",height:"7",x:"3",y:"3",rx:"1",key:"1g98yp"}],["rect",{width:"7",height:"7",x:"14",y:"3",rx:"1",key:"6d4xhi"}],["rect",{width:"7",height:"7",x:"14",y:"14",rx:"1",key:"nxv5o0"}],["rect",{width:"7",height:"7",x:"3",y:"14",rx:"1",key:"1bb6yr"}]]);z();var Iv=re("Link",[["path",{d:"M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71",key:"1cjeqo"}],["path",{d:"M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71",key:"19qd67"}]]);z();var Cv=re("ListOrdered",[["path",{d:"M10 12h11",key:"6m4ad9"}],["path",{d:"M10 18h11",key:"11hvi2"}],["path",{d:"M10 6h11",key:"c7qv1k"}],["path",{d:"M4 10h2",key:"16xx2s"}],["path",{d:"M4 6h1v4",key:"cnovpq"}],["path",{d:"M6 18H4c0-1 2-2 2-3s-1-1.5-2-1",key:"m9a95d"}]]);z();var H1=re("LockOpen",[["rect",{width:"18",height:"11",x:"3",y:"11",rx:"2",ry:"2",key:"1w4ew1"}],["path",{d:"M7 11V7a5 5 0 0 1 9.9-1",key:"1mm8w8"}]]);z();var V1=re("Lock",[["rect",{width:"18",height:"11",x:"3",y:"11",rx:"2",ry:"2",key:"1w4ew1"}],["path",{d:"M7 11V7a5 5 0 0 1 10 0v4",key:"fwvmzm"}]]);z();var q1=re("Maximize2",[["polyline",{points:"15 3 21 3 21 9",key:"mznyad"}],["polyline",{points:"9 21 3 21 3 15",key:"1avn1i"}],["line",{x1:"21",x2:"14",y1:"3",y2:"10",key:"ota7mn"}],["line",{x1:"3",x2:"10",y1:"21",y2:"14",key:"1atl0r"}]]);z();var U1=re("Minimize2",[["polyline",{points:"4 14 10 14 10 20",key:"11kfnr"}],["polyline",{points:"20 10 14 10 14 4",key:"rlmsce"}],["line",{x1:"14",x2:"21",y1:"10",y2:"3",key:"o5lafz"}],["line",{x1:"3",x2:"10",y1:"21",y2:"14",key:"1atl0r"}]]);z();var Z1=re("Minus",[["path",{d:"M5 12h14",key:"1ays0h"}]]);z();var Pv=re("Monitor",[["rect",{width:"20",height:"14",x:"2",y:"3",rx:"2",key:"48i651"}],["line",{x1:"8",x2:"16",y1:"21",y2:"21",key:"1svkeh"}],["line",{x1:"12",x2:"12",y1:"17",y2:"21",key:"vw1qmm"}]]);z();var Y1=re("PanelLeft",[["rect",{width:"18",height:"18",x:"3",y:"3",rx:"2",key:"afitv7"}],["path",{d:"M9 3v18",key:"fh3hqa"}]]);z();var K1=re("PanelRight",[["rect",{width:"18",height:"18",x:"3",y:"3",rx:"2",key:"afitv7"}],["path",{d:"M15 3v18",key:"14nvp0"}]]);z();var X1=re("Plus",[["path",{d:"M5 12h14",key:"1ays0h"}],["path",{d:"M12 5v14",key:"s699le"}]]);z();var G1=re("Quote",[["path",{d:"M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z",key:"rib7q0"}],["path",{d:"M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z",key:"1ymkrd"}]]);z();var J1=re("RectangleEllipsis",[["rect",{width:"20",height:"12",x:"2",y:"6",rx:"2",key:"9lu3g6"}],["path",{d:"M12 12h.01",key:"1mp3jc"}],["path",{d:"M17 12h.01",key:"1m0b6t"}],["path",{d:"M7 12h.01",key:"eqddd0"}]]);z();var Q1=re("Redo2",[["path",{d:"m15 14 5-5-5-5",key:"12vg1m"}],["path",{d:"M20 9H9.5A5.5 5.5 0 0 0 4 14.5A5.5 5.5 0 0 0 9.5 20H13",key:"6uklza"}]]);z();var ew=re("Search",[["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}],["path",{d:"m21 21-4.3-4.3",key:"1qie3q"}]]);z();var tw=re("SlidersHorizontal",[["line",{x1:"21",x2:"14",y1:"4",y2:"4",key:"obuewd"}],["line",{x1:"10",x2:"3",y1:"4",y2:"4",key:"1q6298"}],["line",{x1:"21",x2:"12",y1:"12",y2:"12",key:"1iu8h1"}],["line",{x1:"8",x2:"3",y1:"12",y2:"12",key:"ntss68"}],["line",{x1:"21",x2:"16",y1:"20",y2:"20",key:"14d8ph"}],["line",{x1:"12",x2:"3",y1:"20",y2:"20",key:"m0wm8r"}],["line",{x1:"14",x2:"14",y1:"2",y2:"6",key:"14e1ph"}],["line",{x1:"8",x2:"8",y1:"10",y2:"14",key:"1i6ji0"}],["line",{x1:"16",x2:"16",y1:"18",y2:"22",key:"1lctlv"}]]);z();var rw=re("Smartphone",[["rect",{width:"14",height:"20",x:"5",y:"2",rx:"2",ry:"2",key:"1yt0o3"}],["path",{d:"M12 18h.01",key:"mhygvu"}]]);z();var nw=re("SquareCode",[["path",{d:"M10 9.5 8 12l2 2.5",key:"3mjy60"}],["path",{d:"m14 9.5 2 2.5-2 2.5",key:"1bir2l"}],["rect",{width:"18",height:"18",x:"3",y:"3",rx:"2",key:"afitv7"}]]);z();var ow=re("Strikethrough",[["path",{d:"M16 4H9a3 3 0 0 0-2.83 4",key:"43sutm"}],["path",{d:"M14 12a4 4 0 0 1 0 8H6",key:"nlfj13"}],["line",{x1:"4",x2:"20",y1:"12",y2:"12",key:"1e0a9i"}]]);z();var iw=re("Tablet",[["rect",{width:"16",height:"20",x:"4",y:"2",rx:"2",ry:"2",key:"76otgf"}],["line",{x1:"12",x2:"12.01",y1:"18",y2:"18",key:"1dp563"}]]);z();var aw=re("ToyBrick",[["rect",{width:"18",height:"12",x:"3",y:"8",rx:"1",key:"158fvp"}],["path",{d:"M10 8V5c0-.6-.4-1-1-1H6a1 1 0 0 0-1 1v3",key:"s0042v"}],["path",{d:"M19 8V5c0-.6-.4-1-1-1h-3a1 1 0 0 0-1 1v3",key:"9wmeh2"}]]);z();var au=re("Trash",[["path",{d:"M3 6h18",key:"d0wm0j"}],["path",{d:"M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6",key:"4alrt4"}],["path",{d:"M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2",key:"v07s0e"}]]);z();var ds=re("Type",[["polyline",{points:"4 7 4 4 20 4 20 7",key:"1nosan"}],["line",{x1:"9",x2:"15",y1:"20",y2:"20",key:"swin9y"}],["line",{x1:"12",x2:"12",y1:"4",y2:"20",key:"1tx1rr"}]]);z();var sw=re("Underline",[["path",{d:"M6 4v6a6 6 0 0 0 12 0V4",key:"9kb039"}],["line",{x1:"4",x2:"20",y1:"20",y2:"20",key:"nun2al"}]]);z();var lw=re("Undo2",[["path",{d:"M9 14 4 9l5-5",key:"102s5s"}],["path",{d:"M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11",key:"f3b9sd"}]]);z();var cw=re("X",[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]);z();var uw=re("ZoomIn",[["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}],["line",{x1:"21",x2:"16.65",y1:"21",y2:"16.65",key:"13gj7c"}],["line",{x1:"11",x2:"11",y1:"8",y2:"14",key:"1vmskp"}],["line",{x1:"8",x2:"14",y1:"11",y2:"11",key:"durymu"}]]);z();var dw=re("ZoomOut",[["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}],["line",{x1:"21",x2:"16.65",y1:"21",y2:"16.65",key:"13gj7c"}],["line",{x1:"8",x2:"14",y1:"11",y2:"11",key:"durymu"}]]);z();z();z();var yp={ControlLeft:"ctrl",ControlRight:"ctrl",MetaLeft:"meta",MetaRight:"meta",ShiftLeft:"shift",ShiftRight:"shift",KeyA:"a",KeyB:"b",KeyC:"c",KeyD:"d",KeyE:"e",KeyF:"f",KeyG:"g",KeyH:"h",KeyI:"i",KeyJ:"j",KeyK:"k",KeyL:"l",KeyM:"m",KeyN:"n",KeyO:"o",KeyP:"p",KeyQ:"q",KeyR:"r",KeyS:"s",KeyT:"t",KeyU:"u",KeyV:"v",KeyW:"w",KeyX:"x",KeyY:"y",KeyZ:"z",Delete:"delete",Backspace:"backspace",AltRight:"altRight"},$t=dh()($c(e=>({held:{},hold:t=>e(r=>r.held[t]?r:{held:N(D({},r.held),{[t]:!0})}),release:t=>e(r=>r.held[t]?{held:N(D({},r.held),{[t]:!1})}:r),reset:(t={})=>e(()=>({held:t})),triggers:{}}))),zv=e=>{const t=i=>{if(i.getModifierState("AltGraph")){$t.getState().hold("altRight");return}const a=yp[i.code];if(a){$t.getState().hold(a);const{held:s,triggers:l}=$t.getState();Object.values(l).forEach(({combo:c,cb:d})=>{Object.entries(c).every(([p,v])=>v===!!s[p])&&Object.entries(s).every(([p,v])=>v===!!c[p])&&d(i)!==!1&&i.preventDefault()}),a!=="meta"&&a!=="ctrl"&&a!=="shift"&&$t.getState().release(a)}},r=i=>{if(!i.getModifierState("AltGraph")&&i.code==="ControlRight"){$t.getState().release("altRight");return}const a=yp[i.code];a&&(a==="meta"?$t.getState().reset():$t.getState().release(a))},n=i=>{document.visibilityState==="hidden"&&$t.getState().reset()},o=()=>{$t.getState().reset()};return window.addEventListener("blur",o),e.addEventListener("keydown",t),e.addEventListener("keyup",r),e.addEventListener("visibilitychange",n),()=>{e.removeEventListener("keydown",t),e.removeEventListener("keyup",r),e.removeEventListener("visibilitychange",n),window.removeEventListener("blur",o)}},pw=()=>{g.useEffect(()=>zv(document),[])},Ht=(e,t)=>{g.useEffect(()=>$t.setState(r=>({triggers:N(D({},r.triggers),{[`${Object.keys(e).join("+")}`]:{combo:e,cb:t}})})),[])},bp=0;function fw(e,t=300){let r;return(...n)=>{clearTimeout(r),r=setTimeout(()=>{e(...n)},t)}}var xp=e=>N(D({},e),{ui:N(D({},e.ui),{field:N(D({},e.ui.field),{focus:null})})}),hw=(e,t)=>{const r=fw(n=>{const{histories:o,index:i}=t().history,a={state:n,id:dt("history")},s=[...o.slice(0,i+1),a];e({history:N(D({},t().history),{histories:s,index:s.length-1})})},250);return{initialAppState:{},index:bp,histories:[],hasPast:()=>t().history.index>bp,hasFuture:()=>t().history.index<t().history.histories.length-1,prevHistory:()=>{const{history:n}=t();return n.hasPast()?n.histories[n.index-1]:null},nextHistory:()=>{const n=t().history;return n.hasFuture()?n.histories[n.index+1]:null},currentHistory:()=>t().history.histories[t().history.index],back:()=>{var n;const{history:o,dispatch:i}=t();if(o.hasPast()){const a=xp(((n=o.prevHistory())==null?void 0:n.state)||o.initialAppState);i({type:"set",state:a}),e({history:N(D({},o),{index:o.index-1})})}},forward:()=>{var n;const{history:o,dispatch:i}=t();if(o.hasFuture()){const a=(n=o.nextHistory())==null?void 0:n.state;i({type:"set",state:a?xp(a):{}}),e({history:N(D({},o),{index:o.index+1})})}},setHistories:n=>{var o;const{dispatch:i,history:a}=t();i({type:"set",state:((o=n[n.length-1])==null?void 0:o.state)||a.initialAppState}),e({history:N(D({},a),{histories:n,index:n.length-1})})},setHistoryIndex:n=>{var o;const{dispatch:i,history:a}=t();i({type:"set",state:((o=a.histories[n])==null?void 0:o.state)||a.initialAppState}),e({history:N(D({},a),{index:n})})},record:r}};function vw(e,{histories:t,index:r,initialAppState:n}){g.useEffect(()=>e.setState({history:N(D({},e.getState().history),{histories:t,index:r,initialAppState:n})}),[t,r,n]);const o=()=>{e.getState().history.back()},i=()=>{e.getState().history.forward()};Ht({altRight:!1,meta:!0,z:!0},o),Ht({altRight:!1,meta:!0,shift:!0,z:!0},i),Ht({altRight:!1,meta:!0,y:!0},i),Ht({altRight:!1,ctrl:!0,z:!0},o),Ht({altRight:!1,ctrl:!0,shift:!0,z:!0},i),Ht({altRight:!1,ctrl:!0,y:!0},i)}z();var gw=(e,t)=>{const r=new Map;return{registerNode:(n,o)=>{r.set(n,o)},unregisterNode:n=>{r.delete(n)},syncNode:n=>{var o;n&&((o=r.get(n))==null||o.sync())},syncNodes:n=>{n.forEach(o=>{var i;o&&((i=r.get(o))==null||i.sync())})},setOverlayVisible:(n,o)=>{if(!n)return;const i=r.get(n);if(i){if(o){i.showOverlay();return}i.hideOverlay()}}}};z();z();var kp=(e,t)=>{const r=[];return mt(e,t,n=>n,n=>(r.push(n),n)),r},mw=(e,t)=>{const r=(...o)=>Se(null,[...o],function*(i={},a){const{state:s,permissions:l,config:c}=t(),{cache:d,globalPermissions:u}=l,p=(b,k=!1)=>Se(null,null,function*(){var x,_;const{config:I,state:w,setComponentLoading:A}=t(),E=d[b.props.id],C=w.indexes.nodes,S=(x=C[b.props.id])==null?void 0:x.parentId,j=S?C[S]:null,O=(_=j==null?void 0:j.data)!=null?_:null,L=b.type==="root"?I.root:I.components[b.type];if(!L)return;const $=D(D({},u),L.permissions);if(L.resolvePermissions){const F=Bc(b,E==null?void 0:E.lastData),M=Object.values(F).some(W=>W===!0),q=(E==null?void 0:E.lastParentId)!==S;if(M||q||k){const W=A(b.props.id,!0,50),B=yield L.resolvePermissions(b,{changed:F,lastPermissions:(E==null?void 0:E.lastPermissions)||null,permissions:$,appState:ri(w),lastData:(E==null?void 0:E.lastData)||null,parent:O}),Z=t().permissions;e({permissions:N(D({},Z),{cache:N(D({},Z.cache),{[b.props.id]:{lastParentId:S,lastData:b,lastPermissions:B}}),resolvedPermissions:N(D({},Z.resolvedPermissions),{[b.props.id]:B})})}),W()}}}),v=(b=!1)=>{const{state:k}=t();p({type:"root",props:N(D({},k.data.root.props),{id:"root"})},b)},{item:h,type:m,root:y}=i;h?yield p(h,a):m?kp(s,c).filter(b=>b.type===m).map(b=>Se(null,null,function*(){yield p(b,a)})):y?v(a):kp(s,c).map(b=>Se(null,null,function*(){yield p(b,a)}))});return{cache:{},globalPermissions:{drag:!0,edit:!0,delete:!0,duplicate:!0,insert:!0},resolvedPermissions:{},getPermissions:({item:o,type:i,root:a}={})=>{const{config:s,permissions:l}=t(),{globalPermissions:c,resolvedPermissions:d}=l;if(o){const u=s.components[o.type],p=D(D({},c),u==null?void 0:u.permissions),v=d[o.props.id];return v?D(D({},c),v):p}else if(i){const u=s.components[i];return D(D({},c),u==null?void 0:u.permissions)}else if(a){const u=s.root,p=D(D({},c),u==null?void 0:u.permissions),v=d.root;return v?D(D({},c),v):p}return c},resolvePermissions:r,refreshPermissions:o=>r(o,!0)}},_w=(e,t)=>{g.useEffect(()=>{const{permissions:r}=e.getState(),{globalPermissions:n}=r;e.setState({permissions:N(D({},r),{globalPermissions:D(D({},n),t)})}),r.resolvePermissions()},[t]),g.useEffect(()=>e.subscribe(r=>r.state.data,()=>{e.getState().permissions.resolvePermissions()}),[]),g.useEffect(()=>e.subscribe(r=>r.config,()=>{e.getState().permissions.resolvePermissions()}),[])};z();var yw=(e,t)=>({fields:{},loading:!1,lastResolvedData:{},id:void 0}),bw=(e,t)=>{const r=g.useCallback(n=>Se(null,null,function*(){var o,i;const{fields:a,lastResolvedData:s}=e.getState().fields,l=e.getState().metadata,c=e.getState().state.indexes.nodes,d=c[t||"root"],u=d==null?void 0:d.data,p=d!=null&&d.parentId?c[d.parentId]:null,v=(p==null?void 0:p.data)||null,{getComponentConfig:h,state:m,config:y}=e.getState(),b=h(u==null?void 0:u.type);if(!u||!b)return;const k=b.fields||{},x=b.resolveFields;let _=a;if(n&&(e.setState(I=>({fields:N(D({},I.fields),{fields:k,id:t})})),_=k),x){const I=setTimeout(()=>{e.setState(C=>({fields:N(D({},C.fields),{loading:!0})}))},50),w=((o=s.props)==null?void 0:o.id)===t?s:null,A=Bc(u,w),E=yield x(u,{changed:A,fields:k,lastFields:_,metadata:D(D({},l),b.metadata),lastData:w,appState:ri(m),parent:v});if(clearTimeout(I),((i=e.getState().selectedItem)==null?void 0:i.props.id)!==t||e.getState().config!==y)return;e.setState({fields:{fields:E,loading:!1,lastResolvedData:u,id:t}})}else e.setState(I=>({fields:N(D({},I.fields),{fields:k,id:t})}))}),[t]);g.useEffect(()=>{r(!0);const n=e.subscribe(i=>i.state.indexes.nodes[t||"root"],()=>r()),o=e.subscribe(i=>i.config,()=>r(!0));return()=>{n(),o()}},[t])};z();var xw=e=>{if("type"in e&&e.type!=="root")throw new Error("Converting non-root item to root.");const{readOnly:t}=e;if(e.props){if("id"in e.props){const r=e.props,{id:n}=r;return{props:Tt(r,["id"]),readOnly:t}}return{props:e.props,readOnly:t}}return{props:{},readOnly:t}},kw={title:{type:"text"}},Av=e=>dh()($c((t,r)=>{var n,o;return N(D({instanceId:dt(),state:Sl,config:{components:{}},componentState:{},plugins:[],overrides:{},viewports:oi,zoomConfig:{autoZoom:1,rootHeight:0,zoom:1},status:"LOADING",iframe:{},_experimentalFullScreenCanvas:!1,_experimentalVirtualization:!1,metadata:{},dictionary:{},dnd:{},fieldTransforms:{}},e),{fields:yw(),history:hw(t,r),nodes:gw(),permissions:mw(t,r),getCurrentData:()=>{var i;const a=r();return(i=a.selectedItem)!=null?i:a.state.data.root},getComponentConfig:i=>{var a;const{config:s,selectedItem:l}=r(),c=((a=s.root)==null?void 0:a.fields)||kw;return i&&i!=="root"?s.components[i]:l?s.components[l.type]:N(D({},s.root),{fields:c})},selectedItem:(n=e==null?void 0:e.state)!=null&&n.ui.itemSelector?et((o=e==null?void 0:e.state)==null?void 0:o.ui.itemSelector,e.state):null,dispatch:i=>t(a=>{var s,l;const{record:c}=r().history,u=$d({record:c,appStore:a})(a.state,i),p=u.ui.itemSelector?et(u.ui.itemSelector,u):null;return(l=(s=r()).onAction)==null||l.call(s,i,u,r().state),N(D({},a),{state:u,selectedItem:p})}),setZoomConfig:i=>t({zoomConfig:i}),setStatus:i=>t({status:i}),setComponentState:i=>t({componentState:i}),pendingLoadTimeouts:{},setComponentLoading:(i,a=!0,s=0)=>{const{setComponentState:l,pendingLoadTimeouts:c}=r(),d=dt(),u=()=>{var h;const{componentState:m}=r();l(N(D({},m),{[i]:N(D({},m[i]),{loadingCount:(((h=m[i])==null?void 0:h.loadingCount)||0)+1})}))},p=()=>{var h;const{componentState:m}=r();clearTimeout(v),delete c[d],t({pendingLoadTimeouts:c}),l(N(D({},m),{[i]:N(D({},m[i]),{loadingCount:Math.max((((h=m[i])==null?void 0:h.loadingCount)||0)-1,0)})}))},v=setTimeout(()=>{a?u():p(),delete c[d],t({pendingLoadTimeouts:c})},s);return t({pendingLoadTimeouts:N(D({},c),{[i]:v})}),p},unsetComponentLoading:i=>{const{setComponentLoading:a}=r();a(i,!1)},setUi:(i,a)=>t(s=>{const c=$d({record:()=>{},appStore:s})(s.state,{type:"setUi",ui:i,recordHistory:a}),d=c.ui.itemSelector?et(c.ui.itemSelector,c):null;return N(D({},s),{state:c,selectedItem:d})}),resolveComponentData:(i,a)=>Se(null,null,function*(){var s,l;const{config:c,metadata:d,setComponentLoading:u,permissions:p,state:v}=r(),h="id"in i.props?i.props.id:"root",m=(s=v.indexes.nodes[h])==null?void 0:s.parentId,y=m?v.indexes.nodes[m]:null,b=(l=y==null?void 0:y.data)!=null?l:null,k={};return yield uh(i,c,d,x=>{const _="id"in x.props?x.props.id:"root";k[_]=u(_,!0,50)},x=>Se(null,null,function*(){const _="id"in x.props?x.props.id:"root";"type"in x?yield p.refreshPermissions({item:x}):yield p.refreshPermissions({root:!0}),k[_]()}),a,b,v.data.root)}),resolveAndCommitData:()=>Se(null,null,function*(){const{config:i,state:a,dispatch:s,resolveComponentData:l}=r();mt(a,i,c=>c,(c,d)=>(d.length>1||l(c,"load").then(u=>{const{state:p}=r(),v=p.indexes.nodes[u.node.props.id];if(v&&u.didChange)if(u.node.props.id==="root")s({type:"replaceRoot",root:xw(u.node)});else{const h=`${v.parentId}:${v.zone}`,y=p.indexes.zones[h].contentIds.indexOf(u.node.props.id);s({type:"replace",data:u.node,destinationIndex:y,destinationZone:h})}}),c))})})})),su=g.createContext(null),Hs=null,jv=()=>(Hs||(Hs=Av()),Hs);function H(e){var t;const r=(t=g.useContext(su))!=null?t:jv();return ts(r,e)}function ye(){var e;return(e=g.useContext(su))!=null?e:jv()}z();z();var ww={IconButton:"_IconButton_1pxxt_1","IconButton--active":"_IconButton--active_1pxxt_15","IconButton--disabled":"_IconButton--disabled_1pxxt_28"};z();z();z();z();var wp=(e,t,r)=>{const n=Array.from(e),[o]=n.splice(t,1);return n.splice(r,0,o),n};z();var Sw=(e,t,r)=>{const n=Array.from(e);return n.splice(t,1),n.splice(t,0,r),n};z();z();z();z();var Ew="Invariant failed";function Iw(e,t){throw new Error(Ew)}var Ki=function(t){var r=t.top,n=t.right,o=t.bottom,i=t.left,a=n-i,s=o-r,l={top:r,right:n,bottom:o,left:i,width:a,height:s,x:i,y:r,center:{x:(n+i)/2,y:(o+r)/2}};return l},Cw=function(t,r){return{top:t.top-r.top,left:t.left-r.left,bottom:t.bottom+r.bottom,right:t.right+r.right}},Sp=function(t,r){return{top:t.top+r.top,left:t.left+r.left,bottom:t.bottom-r.bottom,right:t.right-r.right}},Vs={top:0,right:0,bottom:0,left:0},Pw=function(t){var r=t.borderBox,n=t.margin,o=n===void 0?Vs:n,i=t.border,a=i===void 0?Vs:i,s=t.padding,l=s===void 0?Vs:s,c=Ki(Cw(r,o)),d=Ki(Sp(r,a)),u=Ki(Sp(d,l));return{marginBox:c,borderBox:Ki(r),paddingBox:d,contentBox:u,margin:o,border:a,padding:l}},yt=function(t){var r=t.slice(0,-2),n=t.slice(-2);if(n!=="px")return 0;var o=Number(r);return isNaN(o)&&Iw(),o},zw=function(t,r){var n={top:yt(r.marginTop),right:yt(r.marginRight),bottom:yt(r.marginBottom),left:yt(r.marginLeft)},o={top:yt(r.paddingTop),right:yt(r.paddingRight),bottom:yt(r.paddingBottom),left:yt(r.paddingLeft)},i={top:yt(r.borderTopWidth),right:yt(r.borderRightWidth),bottom:yt(r.borderBottomWidth),left:yt(r.borderLeftWidth)};return Pw({borderBox:t,margin:n,padding:o,border:i})},Ov=function(t){var r=t.getBoundingClientRect(),n=window.getComputedStyle(t);return zw(r,n)},Aw=(e,t,r)=>{const n=Ov(t),{width:o,height:i}=n.contentBox,a=e.height==="auto"?i:e.height;let s=0,l=1;if(typeof e.width=="number"&&(e.width>o||a>i)){const c=Math.min(o/e.width,1),d=Math.min(i/a,1);r=c,c<d?s=a/r:(s=a,r=d),l=r}else l=1,r=1,s=a;return{autoZoom:l,rootHeight:s,zoom:r}},Dv=e=>{const t=ye();return n=>{const{state:o,zoomConfig:i,setZoomConfig:a}=t.getState(),{viewports:s}=o.ui,l=(n==null?void 0:n.viewports)||s;e.current&&a(Aw(l==null?void 0:l.current,e.current,i.zoom))}};z();var jw={Loader:"_Loader_1w5zn_13","loader-animation":"_loader-animation_1w5zn_1"};z();z();var Ow={"header-publish":"Publish","header-undo":"undo","header-redo":"redo","header-toggle-leftsidebar":"Toggle left sidebar","header-toggle-rightsidebar":"Toggle right sidebar","header-toggle-menubar":"Toggle menu bar","action-selectparent":"Select parent","action-duplicate":"Duplicate","action-delete":"Delete","label-page":"Page","label-component":"Component","outline-empty":"No items","outline-item-collapse":"Collapse","outline-item-expand":"Expand","outline-header-title":"Outline","outline-header-collapseall":"Collapse all","outline-item-duplicate":"Duplicate","outline-item-delete":"Delete","drawer-category-collapse":"Collapse {title}","drawer-category-expand":"Expand {title}","drawer-category-other":"Other","canvas-noconfig":"No configuration for {type}","field-readonly":"Read-only","field-arrayitem-summary":"Item #{index}","field-arrayitem-duplicate":"Duplicate","field-arrayitem-delete":"Delete","field-external-selectdata":"Select data","field-external-search":"Search","field-external-togglefilters":"Toggle filters","field-external-item":"External item","field-external-result-singular":"{count} result","field-external-result-plural":"{count} results","field-richtext-bold":"Bold","field-richtext-italic":"Italic","field-richtext-underline":"Underline","field-richtext-strikethrough":"Strikethrough","field-richtext-blockquote":"Blockquote","field-richtext-code-inline":"Inline code","field-richtext-code-block":"Code block","field-richtext-list-bullet":"Bullet list","field-richtext-list-ordered":"Ordered list","field-richtext-horizontalrule":"Horizontal rule","field-richtext-align-left":"Align left","field-richtext-align-center":"Align center","field-richtext-align-right":"Align right","field-richtext-align-justify":"Justify","field-richtext-select":"Select","field-richtext-headingselect-1":"Heading 1","field-richtext-headingselect-2":"Heading 2","field-richtext-headingselect-3":"Heading 3","field-richtext-headingselect-4":"Heading 4","field-richtext-headingselect-5":"Heading 5","field-richtext-headingselect-6":"Heading 6","field-richtext-alignselect-left":"Left","field-richtext-alignselect-center":"Center","field-richtext-alignselect-right":"Right","field-richtext-alignselect-justify":"Justify","field-richtext-listselect-bullet":"Bullet list","field-richtext-listselect-ordered":"Ordered list","viewport-zoom-in":"Zoom viewport in","viewport-zoom-out":"Zoom viewport out","viewport-zoom-auto":"{zoom}% (Auto)","viewport-toggle-menu":"Toggle viewport menu","viewport-switch":"Switch to {label} viewport","viewport-switch-default":"Switch viewport","plugin-blocks":"Blocks","plugin-outline":"Outline","plugin-fields":"Fields","plugin-components":"Components","layout-maximize":"maximize","layout-minimize":"minimize","loader-loading":"loading"},Dw=(e,t)=>e.replace(/\{(\w+)\}/g,(r,n)=>t[n]!==void 0?String(t[n]):r),Tw=(e,t,r)=>{var n;const o=(n=e[t])!=null?n:Ow[t];return r?Dw(o,r):o},J=(e,t)=>H(r=>Tw(r.dictionary,e,t)),Mw=ee("Loader",jw),pn=e=>{var t=e,{color:r,size:n=16}=t,o=Tt(t,["color","size"]);const i=J("loader-loading");return f.jsx("span",D({className:Mw(),style:{width:n,height:n,color:r},"aria-label":i},o))},Rw=ee("IconButton",ww),Ke=g.forwardRef((e,t)=>{var r=e,{active:n=!1,children:o,href:i,onClick:a,type:s,disabled:l,tabIndex:c,newTab:d,fullWidth:u,title:p,suppressHydrationWarning:v}=r,h=Tt(r,["active","children","href","onClick","type","disabled","tabIndex","newTab","fullWidth","title","suppressHydrationWarning"]);const[m,y]=g.useState(!1),b=i?"a":"button";return f.jsxs(b,N(D({},h),{ref:t,className:Rw({active:n,disabled:l,fullWidth:u}),onClick:k=>{a&&(y(!0),Promise.resolve(a(k)).then(()=>{y(!1)}))},type:s,disabled:l||m,tabIndex:c,target:d?"_blank":void 0,rel:d?"noreferrer":void 0,href:i,title:p,"aria-label":p,suppressHydrationWarning:v,children:[o,m&&f.jsxs(f.Fragment,{children:["  ",f.jsx(pn,{size:14})]})]}))});Ke.displayName="IconButton";z();var Tv=g.createContext({}),Re=()=>g.useContext(Tv);z();z();z();var Mv={Select:"_Select_1n4iv_1","Select-buttonInner":"_Select-buttonInner_1n4iv_6","Select-buttonIcon":"_Select-buttonIcon_1n4iv_11","Select--standalone":"_Select--standalone_1n4iv_17","Select--actionBar":"_Select--actionBar_1n4iv_22","Select-items":"_Select-items_1n4iv_27",SelectItem:"_SelectItem_1n4iv_38","SelectItem--isSelected":"_SelectItem--isSelected_1n4iv_53","SelectItem-icon":"_SelectItem-icon_1n4iv_59"};z();var Xi=ee("Select",Mv),Rv=ee("SelectItem",Mv),Lw=({children:e,isSelected:t,onClick:r})=>f.jsx("button",{className:Rv({isSelected:t}),onClick:r,children:e}),Fw=({children:e,options:t,onChange:r,value:n,defaultValue:o,mode:i,disabled:a=!1})=>{const[s,l]=g.useState(!1),c=J("field-richtext-select"),d=t.length>0,u=a||!d,p=f.jsxs("div",{className:Xi("buttonInner"),children:[f.jsx("span",{className:Xi("buttonIcon"),children:e}),f.jsx(ci,{size:12})]}),v=i==="actionBar"?f.jsx(cs,{active:n!==o,disabled:u,children:p}):f.jsx(Ke,{title:c,active:n!==o,disabled:u,children:p});return f.jsx("div",{className:Xi({actionBar:i==="actionBar",standalone:i==="standalone"}),children:f.jsxs(l1,{open:s,onOpenChange:l,children:[d?f.jsx(u1,{asChild:!0,children:v}):v,t.length>0&&f.jsx(f1,{children:f.jsx(h1,{align:"start",children:f.jsx("ul",{className:Xi("items"),"data-puck-rte-menu":!0,children:t.map(h=>{const m=h.icon;return f.jsx("li",{children:f.jsxs(Lw,{isSelected:n===h.value,onClick:()=>{r(h.value),l(!1)},children:[m&&f.jsx("div",{className:Rv("icon"),children:f.jsx(m,{size:16})}),h.label]})},h.value)})})})})]})})};function lu({renderDefaultIcon:e,onChange:t,options:r,value:n,defaultValue:o}){var i,a;const{inline:s,readOnly:l}=Re(),c=g.useMemo(()=>r.reduce((u,p)=>N(D({},u),{[p.value]:p}),{}),[r]),d=(a=n&&((i=c[n])==null?void 0:i.icon))!=null?a:e;return f.jsx(Fw,{options:r,onChange:t,value:n,defaultValue:o,mode:s?"actionBar":"standalone",disabled:l,children:f.jsx(d,{})})}/*! Bundled license information:

lucide-react/dist/esm/shared/src/utils.js:
lucide-react/dist/esm/defaultAttributes.js:
lucide-react/dist/esm/Icon.js:
lucide-react/dist/esm/createLucideIcon.js:
lucide-react/dist/esm/icons/align-left.js:
lucide-react/dist/esm/icons/heading.js:
lucide-react/dist/esm/icons/list.js:
lucide-react/dist/esm/icons/align-center.js:
lucide-react/dist/esm/icons/align-justify.js:
lucide-react/dist/esm/icons/align-right.js:
lucide-react/dist/esm/icons/bold.js:
lucide-react/dist/esm/icons/chevron-down.js:
lucide-react/dist/esm/icons/chevron-right.js:
lucide-react/dist/esm/icons/chevron-up.js:
lucide-react/dist/esm/icons/chevrons-down-up.js:
lucide-react/dist/esm/icons/circle-check-big.js:
lucide-react/dist/esm/icons/code.js:
lucide-react/dist/esm/icons/copy.js:
lucide-react/dist/esm/icons/corner-left-up.js:
lucide-react/dist/esm/icons/ellipsis-vertical.js:
lucide-react/dist/esm/icons/expand.js:
lucide-react/dist/esm/icons/globe.js:
lucide-react/dist/esm/icons/hammer.js:
lucide-react/dist/esm/icons/hash.js:
lucide-react/dist/esm/icons/heading-1.js:
lucide-react/dist/esm/icons/heading-2.js:
lucide-react/dist/esm/icons/heading-3.js:
lucide-react/dist/esm/icons/heading-4.js:
lucide-react/dist/esm/icons/heading-5.js:
lucide-react/dist/esm/icons/heading-6.js:
lucide-react/dist/esm/icons/italic.js:
lucide-react/dist/esm/icons/layers.js:
lucide-react/dist/esm/icons/layout-grid.js:
lucide-react/dist/esm/icons/link.js:
lucide-react/dist/esm/icons/list-ordered.js:
lucide-react/dist/esm/icons/lock-open.js:
lucide-react/dist/esm/icons/lock.js:
lucide-react/dist/esm/icons/maximize-2.js:
lucide-react/dist/esm/icons/minimize-2.js:
lucide-react/dist/esm/icons/minus.js:
lucide-react/dist/esm/icons/monitor.js:
lucide-react/dist/esm/icons/panel-left.js:
lucide-react/dist/esm/icons/panel-right.js:
lucide-react/dist/esm/icons/plus.js:
lucide-react/dist/esm/icons/quote.js:
lucide-react/dist/esm/icons/rectangle-ellipsis.js:
lucide-react/dist/esm/icons/redo-2.js:
lucide-react/dist/esm/icons/search.js:
lucide-react/dist/esm/icons/sliders-horizontal.js:
lucide-react/dist/esm/icons/smartphone.js:
lucide-react/dist/esm/icons/square-code.js:
lucide-react/dist/esm/icons/strikethrough.js:
lucide-react/dist/esm/icons/tablet.js:
lucide-react/dist/esm/icons/toy-brick.js:
lucide-react/dist/esm/icons/trash.js:
lucide-react/dist/esm/icons/type.js:
lucide-react/dist/esm/icons/underline.js:
lucide-react/dist/esm/icons/undo-2.js:
lucide-react/dist/esm/icons/x.js:
lucide-react/dist/esm/icons/zoom-in.js:
lucide-react/dist/esm/icons/zoom-out.js:
lucide-react/dist/esm/lucide-react.js:
  (**
   * @license lucide-react v0.468.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)
*/z();var Nw={left:ou,center:bv,right:kv,justify:xv},Bw=e=>{var t;const r=J("field-richtext-alignselect-left"),n=J("field-richtext-alignselect-center"),o=J("field-richtext-alignselect-right"),i=J("field-richtext-alignselect-justify"),a={left:r,center:n,right:o,justify:i};let s=[];return(e==null?void 0:e.textAlign)!==!1&&((t=e==null?void 0:e.textAlign)!=null&&t.alignments?(e!=null&&e.textAlign.alignments.includes("left")&&s.push("left"),e!=null&&e.textAlign.alignments.includes("center")&&s.push("center"),e!=null&&e.textAlign.alignments.includes("right")&&s.push("right"),e!=null&&e.textAlign.alignments.includes("justify")&&s.push("justify")):s=["left","center","right","justify"]),g.useMemo(()=>s.map(l=>({value:l,label:a[l],icon:Nw[l]})),[s,a])};z();var $w={h1:M1,h2:R1,h3:L1,h4:F1,h5:N1,h6:B1},Ww=e=>{var t;const r=J("field-richtext-headingselect-1"),n=J("field-richtext-headingselect-2"),o=J("field-richtext-headingselect-3"),i=J("field-richtext-headingselect-4"),a=J("field-richtext-headingselect-5"),s=J("field-richtext-headingselect-6"),l={h1:r,h2:n,h3:o,h4:i,h5:a,h6:s};let c=[];return(e==null?void 0:e.heading)!==!1&&((t=e==null?void 0:e.heading)!=null&&t.levels?(e!=null&&e.heading.levels.includes(1)&&c.push("h1"),e!=null&&e.heading.levels.includes(2)&&c.push("h2"),e!=null&&e.heading.levels.includes(3)&&c.push("h3"),e!=null&&e.heading.levels.includes(4)&&c.push("h4"),e!=null&&e.heading.levels.includes(5)&&c.push("h5"),e!=null&&e.heading.levels.includes(6)&&c.push("h6")):c=["h1","h2","h3","h4","h5","h6"]),g.useMemo(()=>c.map(d=>({value:d,label:l[d],icon:$w[d]})),[c,l])};z();var Hw={ul:us,ol:Cv},Vw=e=>{const t=J("field-richtext-listselect-bullet"),r=J("field-richtext-listselect-ordered"),n={ul:t,ol:r};let o=[];return(e==null?void 0:e.listItem)!==!1&&(o=["ul","ol"]),g.useMemo(()=>o.map(i=>({value:i,label:n[i],icon:Hw[i]})),[o,n])};z();z();var qw={RichTextMenu:"_RichTextMenu_1ve2j_1","RichTextMenu--form":"_RichTextMenu--form_1ve2j_7","RichTextMenu-group":"_RichTextMenu-group_1ve2j_21","RichTextMenu--inline":"_RichTextMenu--inline_1ve2j_39"};z();z();z();z();var Uw={Control:"_Control_id4pm_1","Control--inline":"_Control--inline_id4pm_6"},Ep=ee("Control",Uw);function at({icon:e,disabled:t,active:r,onClick:n,title:o}){const{inline:i}=Re();return i?f.jsx("span",{className:Ep({inline:!0}),children:f.jsx(cs,{onClick:n,disabled:t,active:r,label:o,children:e})}):f.jsx("span",{className:Ep(),children:f.jsx(Ke,{onClick:n,disabled:t,active:r,title:o,children:e})})}function Zw(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-align-left");return f.jsx(at,{icon:f.jsx(ou,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().setTextAlign("left").run()},disabled:!(t!=null&&t.canAlignLeft),active:t==null?void 0:t.isAlignLeft,title:r})}z();function Yw(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-align-center");return f.jsx(at,{icon:f.jsx(bv,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().setTextAlign("center").run()},disabled:!(t!=null&&t.canAlignCenter),active:t==null?void 0:t.isAlignCenter,title:r})}z();function Kw(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-align-right");return f.jsx(at,{icon:f.jsx(kv,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().setTextAlign("right").run()},disabled:!(t!=null&&t.canAlignRight),active:t==null?void 0:t.isAlignRight,title:r})}z();function Xw(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-align-justify");return f.jsx(at,{icon:f.jsx(xv,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().setTextAlign("justify").run()},disabled:!(t!=null&&t.canAlignJustify),active:t==null?void 0:t.isAlignJustify,title:r})}z();z();function Gw(){const e=Re(),t=Bw(e.options);return f.jsx(lu,{options:t,onChange:()=>{},value:"left",defaultValue:"left",renderDefaultIcon:ou})}var Jw=g.lazy(()=>Nr(()=>import("./chunks/loaded-SMPR6KZF-D8OLGQ-t.js"),__vite__mapDeps([0,1,2,3])).then(e=>({default:e.AlignSelectLoaded}))),Lv=()=>f.jsx(g.Suspense,{fallback:f.jsx(Gw,{}),children:f.jsx(Jw,{})});z();function Ll(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-bold");return f.jsx(at,{icon:f.jsx(I1,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleBold().run()},disabled:!(t!=null&&t.canBold),active:t==null?void 0:t.isBold,title:r})}z();function Fl(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-italic");return f.jsx(at,{icon:f.jsx($1,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleItalic().run()},disabled:!(t!=null&&t.canItalic),active:t==null?void 0:t.isItalic,title:r})}z();function Nl(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-underline");return f.jsx(at,{icon:f.jsx(sw,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleUnderline().run()},disabled:!(t!=null&&t.canUnderline),active:t==null?void 0:t.isUnderline,title:r})}z();function Qw(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-strikethrough");return f.jsx(at,{icon:f.jsx(ow,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleStrike().run()},disabled:!(t!=null&&t.canStrike),active:t==null?void 0:t.isStrike,title:r})}z();function e2(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-code-inline");return f.jsx(at,{icon:f.jsx(z1,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleCode().run()},disabled:!(t!=null&&t.canInlineCode),active:t==null?void 0:t.isInlineCode,title:r})}z();function t2(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-list-bullet");return f.jsx(at,{icon:f.jsx(us,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleBulletList().run()},disabled:!(t!=null&&t.canBulletList),active:t==null?void 0:t.isBulletList,title:r})}z();function r2(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-list-ordered");return f.jsx(at,{icon:f.jsx(Cv,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleOrderedList().run()},disabled:!(t!=null&&t.canOrderedList),active:t==null?void 0:t.isOrderedList,title:r})}z();function n2(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-code-block");return f.jsx(at,{icon:f.jsx(nw,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleCodeBlock().run()},disabled:!(t!=null&&t.canCodeBlock),active:t==null?void 0:t.isCodeBlock,title:r})}z();function o2(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-blockquote");return f.jsx(at,{icon:f.jsx(G1,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().toggleBlockquote().run()},disabled:!(t!=null&&t.canBlockquote),active:t==null?void 0:t.isBlockquote,title:r})}z();function i2(){const{editor:e,editorState:t}=Re(),r=J("field-richtext-horizontalrule");return f.jsx(at,{icon:f.jsx(Z1,{}),onClick:n=>{n.stopPropagation(),e==null||e.chain().focus().setHorizontalRule().run()},disabled:!(t!=null&&t.canHorizontalRule),title:r})}z();z();function a2(){const e=Re(),t=Ww(e.options);return f.jsx(lu,{options:t,onChange:()=>{},value:"p",defaultValue:"p",renderDefaultIcon:E1})}var s2=g.lazy(()=>Nr(()=>import("./chunks/loaded-JKA25A3T-BxXqvxXU.js"),__vite__mapDeps([4,1,2,3])).then(e=>({default:e.HeadingSelectLoaded}))),Fv=()=>f.jsx(g.Suspense,{fallback:f.jsx(a2,{}),children:f.jsx(s2,{})});z();z();function l2(){const e=Re(),t=Vw(e.options);return f.jsx(lu,{options:t,onChange:()=>{},value:"p",defaultValue:"p",renderDefaultIcon:us})}var c2=g.lazy(()=>Nr(()=>import("./chunks/loaded-36WRJPBT-D05DBu2k.js"),__vite__mapDeps([5,1,2,3])).then(e=>({default:e.ListSelectLoaded}))),Nv=()=>f.jsx(g.Suspense,{fallback:f.jsx(l2,{}),children:f.jsx(c2,{})}),Bv=ee("RichTextMenu",qw),Ip=({children:e})=>f.jsx(Le,{children:e}),Le=({children:e})=>{const{inline:t}=Re();return f.jsx("div",{className:Bv({inline:t,form:!t}),"data-puck-rte-menu":!0,children:e})},Ao=({children:e})=>f.jsx("div",{className:Bv("group"),children:e});Le.Group=Ao;Le.Control=at;Le.AlignCenter=Yw;Le.AlignJustify=Xw;Le.AlignLeft=Zw;Le.AlignRight=Kw;Le.AlignSelect=Lv;Le.Blockquote=o2;Le.Bold=Ll;Le.BulletList=t2;Le.CodeBlock=n2;Le.HeadingSelect=Fv;Le.HorizontalRule=i2;Le.InlineCode=e2;Le.Italic=Fl;Le.ListSelect=Nv;Le.OrderedList=r2;Le.Strikethrough=Qw;Le.Underline=Nl;var $v=({editor:e=null,editorState:t=null,field:r,readOnly:n,inline:o})=>{const{renderMenu:i,renderInlineMenu:a}=r,s=g.useMemo(()=>a||Ip,[a]),l=g.useMemo(()=>i||Ip,[i]);return f.jsx(Tv.Provider,{value:{editor:e,editorState:t,inline:o,options:r.options,readOnly:n},children:o?f.jsx(s,{editor:e,editorState:t,readOnly:n,children:f.jsxs(Ao,{children:[f.jsx(Ll,{}),f.jsx(Fl,{}),f.jsx(Nl,{})]})}):f.jsxs(l,{editor:e,editorState:t,readOnly:n,children:[f.jsxs(Ao,{children:[f.jsx(Fv,{}),f.jsx(Nv,{})]}),f.jsxs(Ao,{children:[f.jsx(Ll,{}),f.jsx(Fl,{}),f.jsx(Nl,{})]}),f.jsx(Ao,{children:f.jsx(Lv,{})})]})})};z();var Cp=ee("RichTextEditor",Qf),Wv=g.memo(({children:e,menu:t,readOnly:r=!1,field:n,inline:o=!1,editor:i,id:a})=>{const{initialHeight:s}=n,l=H(p=>{var v;return((v=p.currentRichText)==null?void 0:v.id)===a&&o===p.currentRichText.inline}),c=ye(),d=g.useCallback(p=>{var v,h;(p.metaKey||p.ctrlKey)&&p.key.toLowerCase()==="i"&&(p.stopPropagation(),p.preventDefault(),(h=i==null?void 0:(v=i.commands).toggleItalic)==null||h.call(v)),p.key.toLowerCase()==="backspace"&&p.stopPropagation()},[i]),u=g.useCallback(p=>{var v,h;const m=!!((h=(v=p.relatedTarget)==null?void 0:v.closest)!=null&&h.call(v,"[data-puck-rte-menu]"));p.relatedTarget&&!m?c.setState({currentRichText:null}):p.stopPropagation()},[c]);return f.jsxs("div",{className:Cp({editor:!o,inline:o,isActive:l,disabled:r}),style:o?{}:{height:s??192,overflowY:"auto"},onKeyDownCapture:d,onBlur:u,children:[!o&&f.jsx("div",{className:Cp("menu"),children:t}),e]})});Wv.displayName="EditorInner";z();var u2=g.lazy(()=>Nr(()=>import("./chunks/full-7ZJV44EE-DwaRnnCc.js"),__vite__mapDeps([6,1,2,3])).then(e=>({default:e.LoadedRichTextMenuFull}))),d2=e=>f.jsx(g.Suspense,{fallback:f.jsx($v,D({},e)),children:f.jsx(u2,D({},e))});z();z();z();z();z();z();var cu=(e,t=e)=>({slot:({value:r,propName:n,field:o,isReadOnly:i})=>{const a=i?t:e;return l=>a(N(D({allow:(o==null?void 0:o.type)==="slot"?o.allow:[],disallow:(o==null?void 0:o.type)==="slot"?o.disallow:[]},l),{zone:n,content:r}))}});z();z();z();function Hv(e,t,r){const n={};return Object.keys(e).forEach(o=>{const i=o;n[i]=a=>{var s=a,{parentId:l}=s,c=Tt(s,["parentId"]);const d=c.propPath.replace(/\[\d+\]/g,"[*]"),u=(t==null?void 0:t[c.propPath])||(t==null?void 0:t[d])||r||!1,p=e[i];return p==null?void 0:p(N(D({},c),{field:c.field,isReadOnly:u,componentId:l}))}}),n}function p2(e,t,r,n,o){const i=g.useMemo(()=>Hv(r,n,o),[r,n,o]),a=g.useMemo(()=>un(t,i,e).props,[e,t,i]);return g.useMemo(()=>D(D({},t.props),a),[t.props,a])}function uu(e,t,r,n=r,o,i){return p2(e,t,cu(r,n),o,i)}z();z();var f2=ee("RichTextEditor",Qf);function Vv({content:e}){return f.jsx("div",{className:f2(),children:f.jsx("div",{className:"rich-text",dangerouslySetInnerHTML:{__html:e}})})}z();var Bl=(e,t,r)=>{if(!e)return null;if(t.length===0)return r(e);const[n,...o]=t;return Array.isArray(e)?e.map(i=>Bl(i,t,r)):N(D({},e),{[n]:Bl(e[n],o,r)})},h2=g.lazy(()=>Nr(()=>import("./chunks/Render-DQXAYUBI-tp0YyC1G.js"),__vite__mapDeps([7,8,3,2])).then(e=>({default:e.RichTextRender})));function ps(e,t){const r=(i,a=[])=>{if(!i)return[];const s=[];for(const[l,c]of Object.entries(i)){const d=[...a,l];c.type==="richtext"&&s.push({path:d,field:c}),c.type==="array"&&"arrayFields"in c&&s.push(...r(c.arrayFields,d)),c.type==="object"&&"objectFields"in c&&s.push(...r(c.objectFields,d))}return s},n=g.useMemo(()=>r(e),[e]);return g.useMemo(()=>{if(!(n!=null&&n.length))return{};let i=D({},t);for(const{path:a,field:s}of n)i=Bl(i,a,l=>f.jsx(g.Suspense,{fallback:f.jsx(Vv,{content:l}),children:f.jsx(h2,{content:l,field:s})},a.join(".")));return i},[n,t,e])}z();var du=e=>f.jsx(qv,D({},e)),v2=({config:e,item:t,metadata:r})=>{const n=e.components[t.type],o=uu(e,t,a=>f.jsx(du,N(D({},a),{config:e,metadata:r}))),i=ps(n.fields,o);return f.jsx(n.render,N(D(D({},o),i),{puck:N(D({},o.puck),{metadata:r||{}})}))},qv=g.forwardRef(function({className:t,style:r,content:n,config:o,metadata:i,as:a},s){const l=a??"div";return f.jsx(l,{className:t,style:r,ref:s,children:n.map(c=>o.components[c.type]?f.jsx(v2,{config:o,item:c,metadata:i},c.props.id):null)})});const Pp=e=>Symbol.iterator in e,zp=e=>"entries"in e,Ap=(e,t)=>{const r=e instanceof Map?e:new Map(e.entries()),n=t instanceof Map?t:new Map(t.entries());if(r.size!==n.size)return!1;for(const[o,i]of r)if(!n.has(o)||!Object.is(i,n.get(o)))return!1;return!0},g2=(e,t)=>{const r=e[Symbol.iterator](),n=t[Symbol.iterator]();let o=r.next(),i=n.next();for(;!o.done&&!i.done;){if(!Object.is(o.value,i.value))return!1;o=r.next(),i=n.next()}return!!o.done&&!!i.done};function m2(e,t){return Object.is(e,t)?!0:typeof e!="object"||e===null||typeof t!="object"||t===null||Object.getPrototypeOf(e)!==Object.getPrototypeOf(t)?!1:Pp(e)&&Pp(t)?zp(e)&&zp(t)?Ap(e,t):g2(e,t):Ap({entries:()=>Object.entries(e)},{entries:()=>Object.entries(t)})}function Be(e){const t=Er.useRef(void 0);return r=>{const n=e(r);return m2(t.current,n)?t.current:t.current=n}}var _2=Symbol.for("preact-signals");function fs(){if(sr>1)sr--;else{var e,t=!1;for((function(){var o=Ra;for(Ra=void 0;o!==void 0;){var i=o.S;if(i.v===o.v)for(var a=i.t;a!==void 0;a=a.x)a.i===o.i&&(a.i=i.i);o=o.o}})();Yo!==void 0;){var r=Yo;for(Yo=void 0,Ma++;r!==void 0;){var n=r.u;if(r.u=void 0,r.f&=-3,!(8&r.f)&&Zv(r))try{r.c()}catch(o){t||(e=o,t=!0)}r=n}}if(Ma=0,sr--,t)throw e}}function Ae(e){if(sr>0)return e();$l=++y2,sr++;try{return e()}finally{fs()}}var Zo,Ce=void 0;function de(e){var t=Ce,r=Zo;Ce=void 0,Zo=void 0;try{return e()}finally{Ce=t,Zo=r}}var Yo=void 0,sr=0,Ma=0,y2=0,$l=0,Ra=void 0,La=0;function Uv(e){if(Ce!==void 0){var t=e.n;if(t===void 0||t.t!==Ce)return t={i:0,S:e,p:Ce.s,n:void 0,t:Ce,e:void 0,x:void 0,r:t},Ce.s!==void 0&&(Ce.s.n=t),Ce.s=t,e.n=t,32&Ce.f&&e.S(t),t;if(t.i===-1)return t.i=0,t.n!==void 0&&(t.n.p=t.p,t.p!==void 0&&(t.p.n=t.n),t.p=Ce.s,t.n=void 0,Ce.s.n=t,Ce.s=t),t}}function st(e,t){this.v=e,this.i=0,this.n=void 0,this.t=void 0,this.l=0,this.W=t==null?void 0:t.watched,this.Z=t==null?void 0:t.unwatched,this.name=t==null?void 0:t.name}st.prototype.brand=_2;st.prototype.h=function(){return!0};st.prototype.S=function(e){var t=this,r=this.t;r!==e&&e.e===void 0&&(e.x=r,this.t=e,r!==void 0?r.e=e:de(function(){var n;(n=t.W)==null||n.call(t)}))};st.prototype.U=function(e){var t=this;if(this.t!==void 0){var r=e.e,n=e.x;r!==void 0&&(r.x=n,e.e=void 0),n!==void 0&&(n.e=r,e.x=void 0),e===this.t&&(this.t=n,n===void 0&&de(function(){var o;(o=t.Z)==null||o.call(t)}))}};st.prototype.subscribe=function(e){var t=this;return pt(function(){var r=t.value;de(function(){return e(r)})},{name:"sub"})};st.prototype.valueOf=function(){return this.value};st.prototype.toString=function(){return this.value+""};st.prototype.toJSON=function(){return this.value};st.prototype.peek=function(){var e=this;return de(function(){return e.value})};Object.defineProperty(st.prototype,"value",{get:function(){var e=Uv(this);return e!==void 0&&(e.i=this.i),this.v},set:function(e){if(e!==this.v){if(Ma>100)throw new Error("Cycle detected");(function(r){sr!==0&&Ma===0&&r.l!==$l&&(r.l=$l,Ra={S:r,v:r.v,i:r.i,o:Ra})})(this),this.v=e,this.i++,La++,sr++;try{for(var t=this.t;t!==void 0;t=t.x)t.t.N()}finally{fs()}}}});function lo(e,t){return new st(e,t)}function Zv(e){for(var t=e.s;t!==void 0;t=t.n)if(t.S.i!==t.i||!t.S.h()||t.S.i!==t.i)return!0;return!1}function Yv(e){for(var t=e.s;t!==void 0;t=t.n){var r=t.S.n;if(r!==void 0&&(t.r=r),t.S.n=t,t.i=-1,t.n===void 0){e.s=t;break}}}function Kv(e){for(var t=e.s,r=void 0;t!==void 0;){var n=t.p;t.i===-1?(t.S.U(t),n!==void 0&&(n.n=t.n),t.n!==void 0&&(t.n.p=n)):r=t,t.S.n=t.r,t.r!==void 0&&(t.r=void 0),t=n}e.s=r}function fn(e,t){st.call(this,void 0,t),this.x=e,this.s=void 0,this.g=La-1,this.f=4}fn.prototype=new st;fn.prototype.h=function(){if(this.f&=-3,1&this.f)return!1;if((36&this.f)==32||(this.f&=-5,this.g===La))return!0;if(this.g=La,this.f|=1,this.i>0&&!Zv(this))return this.f&=-2,!0;var e=Ce;try{Yv(this),Ce=this;var t=this.x();(16&this.f||this.v!==t||this.i===0)&&(this.v=t,this.f&=-17,this.i++)}catch(r){this.v=r,this.f|=16,this.i++}return Ce=e,Kv(this),this.f&=-2,!0};fn.prototype.S=function(e){if(this.t===void 0){this.f|=36;for(var t=this.s;t!==void 0;t=t.n)t.S.S(t)}st.prototype.S.call(this,e)};fn.prototype.U=function(e){if(this.t!==void 0&&(st.prototype.U.call(this,e),this.t===void 0)){this.f&=-33;for(var t=this.s;t!==void 0;t=t.n)t.S.U(t)}};fn.prototype.N=function(){if(!(2&this.f)){this.f|=6;for(var e=this.t;e!==void 0;e=e.x)e.t.N()}};Object.defineProperty(fn.prototype,"value",{get:function(){if(1&this.f)throw new Error("Cycle detected");var e=Uv(this);if(this.h(),e!==void 0&&(e.i=this.i),16&this.f)throw this.v;return this.v}});function jp(e,t){return new fn(e,t)}function Xv(e){var t=e.m;if(e.m=void 0,typeof t=="function"){sr++;var r=Ce;Ce=void 0;try{t()}catch(n){throw e.f&=-2,e.f|=8,pu(e),n}finally{Ce=r,fs()}}}function pu(e){for(var t=e.s;t!==void 0;t=t.n)t.S.U(t);e.x=void 0,e.s=void 0,Xv(e)}function b2(e){if(Ce!==this)throw new Error("Out-of-order effect");Kv(this),Ce=e,this.f&=-2,8&this.f&&pu(this),fs()}function co(e,t){this.x=e,this.m=void 0,this.s=void 0,this.u=void 0,this.f=32,this.name=t==null?void 0:t.name,Zo&&Zo.push(this)}co.prototype.c=function(){var e=this.S();try{if(8&this.f||this.x===void 0)return;var t=this.x();typeof t=="function"&&(this.m=t)}finally{e()}};co.prototype.S=function(){if(1&this.f)throw new Error("Cycle detected");this.f|=1,this.f&=-9,Xv(this),Yv(this),sr++;var e=Ce;return Ce=this,b2.bind(this,e)};co.prototype.N=function(){2&this.f||(this.f|=2,this.u=Yo,Yo=this)};co.prototype.d=function(){this.f|=8,1&this.f||pu(this)};co.prototype.dispose=function(){this.d()};function pt(e,t){var r=new co(e,t);try{r.c()}catch(o){throw r.d(),o}var n=r.d.bind(r);return n[Symbol.dispose]=n,n}var x2=Object.create,fu=Object.defineProperty,k2=Object.defineProperties,w2=Object.getOwnPropertyDescriptor,S2=Object.getOwnPropertyDescriptors,Op=Object.getOwnPropertySymbols,E2=Object.prototype.hasOwnProperty,I2=Object.prototype.propertyIsEnumerable,C2=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),uo=e=>{throw TypeError(e)},Wl=(e,t,r)=>t in e?fu(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,P2=(e,t)=>{for(var r in t||(t={}))E2.call(t,r)&&Wl(e,r,t[r]);if(Op)for(var r of Op(t))I2.call(t,r)&&Wl(e,r,t[r]);return e},z2=(e,t)=>k2(e,S2(t)),Dp=(e,t)=>fu(e,"name",{value:t,configurable:!0}),A2=e=>{var t;return[,,,x2((t=void 0)!=null?t:null)]},Gv=["class","method","getter","setter","accessor","field","value","get","set"],jo=e=>e!==void 0&&typeof e!="function"?uo("Function expected"):e,j2=(e,t,r,n,o)=>({kind:Gv[e],name:t,metadata:n,addInitializer:i=>r._?uo("Already initialized"):o.push(jo(i||null))}),Jv=(e,t)=>Wl(t,C2("metadata"),e[3]),Zr=(e,t,r,n)=>{for(var o=0,i=e[t>>1],a=i&&i.length;o<a;o++)t&1?i[o].call(r):n=i[o].call(r,n);return n},po=(e,t,r,n,o,i)=>{var a,s,l,c,d,u=t&7,p=!!(t&8),v=!!(t&16),h=u>3?e.length+1:u?p?1:2:0,m=Gv[u+5],y=u>3&&(e[h-1]=[]),b=e[h]||(e[h]=[]),k=u&&(!v&&!p&&(o=o.prototype),u<5&&(u>3||!v)&&w2(u<4?o:{get[r](){return xt(this,i)},set[r](_){return wr(this,i,_)}},r));u?v&&u<4&&Dp(i,(u>2?"set ":u>1?"get ":"")+r):Dp(o,r);for(var x=n.length-1;x>=0;x--)c=j2(u,r,l={},e[3],b),u&&(c.static=p,c.private=v,d=c.access={has:v?_=>O2(o,_):_=>r in _},u^3&&(d.get=v?_=>(u^1?xt:D2)(_,o,u^4?i:k.get):_=>_[r]),u>2&&(d.set=v?(_,I)=>wr(_,o,I,u^4?i:k.set):(_,I)=>_[r]=I)),s=(0,n[x])(u?u<4?v?i:k[m]:u>4?void 0:{get:k.get,set:k.set}:o,c),l._=1,u^4||s===void 0?jo(s)&&(u>4?y.unshift(s):u?v?i=s:k[m]=s:o=s):typeof s!="object"||s===null?uo("Object expected"):(jo(a=s.get)&&(k.get=a),jo(a=s.set)&&(k.set=a),jo(a=s.init)&&y.unshift(a));return u||Jv(e,o),k&&fu(o,r,k),v?u^4?i:k:o},hu=(e,t,r)=>t.has(e)||uo("Cannot "+r),O2=(e,t)=>Object(t)!==t?uo('Cannot use the "in" operator on this value'):e.has(t),xt=(e,t,r)=>(hu(e,t,"read from private field"),r?r.call(e):t.get(e)),Oo=(e,t,r)=>t.has(e)?uo("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),wr=(e,t,r,n)=>(hu(e,t,"write to private field"),n?n.call(e,r):t.set(e,r),r),D2=(e,t,r)=>(hu(e,t,"access private method"),r);function Hl(e,t){if(t){let r;return jp(()=>{const n=e();return n&&r&&t(r,n)?r:(r=n,n)})}return jp(e)}function Ot(e,t){if(Object.is(e,t))return!0;if(e===null||t===null)return!1;if(typeof e=="function"&&typeof t=="function")return e===t;if(e instanceof Set&&t instanceof Set){if(e.size!==t.size)return!1;for(const r of e)if(!t.has(r))return!1;return!0}if(Array.isArray(e))return!Array.isArray(t)||e.length!==t.length?!1:!e.some((n,o)=>!Ot(n,t[o]));if(typeof e=="object"&&typeof t=="object"){const r=Object.keys(e),n=Object.keys(t);return r.length!==n.length?!1:!r.some(i=>!Ot(e[i],t[i]))}return!1}function pe({get:e},t){return{init(r){return lo(r)},get(){return e.call(this).value},set(r){const n=e.call(this);n.peek()!==r&&(n.value=r)}}}function Te(e,t){const r=new WeakMap;return function(){let n=r.get(this);return n||(n=Hl(e.bind(this)),r.set(this,n)),n.value}}function qs(e=!0){return function(t,r){r.addInitializer(function(){const n=r.kind==="field"?this:r.static?this:Object.getPrototypeOf(this),o=Object.getOwnPropertyDescriptor(n,r.name);o&&Object.defineProperty(n,r.name,z2(P2({},o),{enumerable:e}))})}}function wi(...e){const t=e.map(r=>pt(r));return()=>t.forEach(r=>r())}var Qv,eg,tg,rg,ng,og,rt,vu,Us,Vl,ql,Ge,gu,Zs,ig,Ul,mu,Ys,Zl,Yl;og=[pe],ng=[pe],rg=[pe],tg=[qs()],eg=[qs()],Qv=[qs()];var hn=class{constructor(e,t=Object.is){this.defaultValue=e,this.equals=t,Zr(rt,5,this),Oo(this,Ge),Oo(this,vu,Zr(rt,8,this)),Zr(rt,11,this),Oo(this,gu,Zr(rt,12,this)),Zr(rt,15,this),Oo(this,mu,Zr(rt,16,this)),Zr(rt,19,this),this.reset=this.reset.bind(this),this.reset()}get current(){return xt(this,Ge,Zl)}get initial(){return xt(this,Ge,Vl)}get previous(){return xt(this,Ge,ig)}set current(e){const t=de(()=>xt(this,Ge,Zl));e&&t&&this.equals(t,e)||Ae(()=>{xt(this,Ge,Vl)||wr(this,Ge,e,ql),wr(this,Ge,t,Ul),wr(this,Ge,e,Yl)})}reset(e=this.defaultValue){Ae(()=>{wr(this,Ge,void 0,Ul),wr(this,Ge,e,ql),wr(this,Ge,e,Yl)})}};rt=A2();vu=new WeakMap;Ge=new WeakSet;gu=new WeakMap;mu=new WeakMap;Us=po(rt,20,"#initial",og,Ge,vu),Vl=Us.get,ql=Us.set;Zs=po(rt,20,"#previous",ng,Ge,gu),ig=Zs.get,Ul=Zs.set;Ys=po(rt,20,"#current",rg,Ge,mu),Zl=Ys.get,Yl=Ys.set;po(rt,2,"current",tg,hn);po(rt,2,"initial",eg,hn);po(rt,2,"previous",Qv,hn);Jv(rt,hn);function Ks(e){return de(()=>{const t={};for(const r in e)t[r]=e[r];return t})}var Yr,T2=class{constructor(){Oo(this,Yr,new WeakMap)}get(e,t){var r;return e?(r=xt(this,Yr).get(e))==null?void 0:r.get(t):void 0}set(e,t,r){var n;if(e)return xt(this,Yr).has(e)||xt(this,Yr).set(e,new Map),(n=xt(this,Yr).get(e))==null?void 0:n.set(t,r)}clear(e){var t;return e?(t=xt(this,Yr).get(e))==null?void 0:t.clear():void 0}};Yr=new WeakMap;var M2=Object.create,ag=Object.defineProperty,R2=Object.getOwnPropertyDescriptor,Tp=Object.getOwnPropertySymbols,L2=Object.prototype.hasOwnProperty,F2=Object.prototype.propertyIsEnumerable,sg=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),hs=e=>{throw TypeError(e)},Mp=Math.pow,Kl=(e,t,r)=>t in e?ag(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,N2=(e,t)=>{for(var r in t||(t={}))L2.call(t,r)&&Kl(e,r,t[r]);if(Tp)for(var r of Tp(t))F2.call(t,r)&&Kl(e,r,t[r]);return e},B2=e=>{var t;return[,,,M2((t=e==null?void 0:e[sg("metadata")])!=null?t:null)]},lg=["class","method","getter","setter","accessor","field","value","get","set"],cg=e=>e!==void 0&&typeof e!="function"?hs("Function expected"):e,$2=(e,t,r,n,o)=>({kind:lg[e],name:t,metadata:n,addInitializer:i=>r._?hs("Already initialized"):o.push(cg(i||null))}),W2=(e,t)=>Kl(t,sg("metadata"),e[3]),H2=(e,t,r,n)=>{for(var o=0,i=e[t>>1],a=i&&i.length;o<a;o++)i[o].call(r);return n},ug=(e,t,r,n,o,i)=>{for(var a,s,l,c,d=t&7,u=!1,p=!1,v=2,h=lg[d+5],m=e[v]||(e[v]=[]),y=(o=o.prototype,R2(o,r)),b=n.length-1;b>=0;b--)l=$2(d,r,s={},e[3],m),l.static=u,l.private=p,c=l.access={has:k=>r in k},c.get=k=>k[r],a=(0,n[b])(y[h],l),s._=1,cg(a)&&(y[h]=a);return y&&ag(o,r,y),o},dg=(e,t,r)=>t.has(e)||hs("Cannot "+r),V2=(e,t,r)=>(dg(e,t,"read from private field"),t.get(e)),q2=(e,t,r)=>t.has(e)?hs("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),U2=(e,t,r,n)=>(dg(e,t,"write to private field"),t.set(e,r),r),Qe=class Xl{constructor(t,r){this.x=t,this.y=r}static delta(t,r){return new Xl(t.x-r.x,t.y-r.y)}static distance(t,r){return Math.hypot(t.x-r.x,t.y-r.y)}static equals(t,r){return t.x===r.x&&t.y===r.y}static from({x:t,y:r}){return new Xl(t,r)}},It=class Kr{constructor(t,r,n,o){this.left=t,this.top=r,this.width=n,this.height=o,this.scale={x:1,y:1}}get inverseScale(){return{x:1/this.scale.x,y:1/this.scale.y}}translate(t,r){const{top:n,left:o,width:i,height:a,scale:s}=this,l=new Kr(o+t,n+r,i,a);return l.scale=N2({},s),l}get boundingRectangle(){const{width:t,height:r,left:n,top:o,right:i,bottom:a}=this;return{width:t,height:r,left:n,top:o,right:i,bottom:a}}get center(){const{left:t,top:r,right:n,bottom:o}=this;return new Qe((t+n)/2,(r+o)/2)}get area(){const{width:t,height:r}=this;return t*r}equals(t){if(!(t instanceof Kr))return!1;const{left:r,top:n,width:o,height:i}=this;return r===t.left&&n===t.top&&o===t.width&&i===t.height}containsPoint(t){const{top:r,left:n,bottom:o,right:i}=this;return r<=t.y&&t.y<=o&&n<=t.x&&t.x<=i}intersectionArea(t){return t instanceof Kr?Z2(this,t):0}intersectionRatio(t){const{area:r}=this,n=this.intersectionArea(t);return n/(t.area+r-n)}get bottom(){const{top:t,height:r}=this;return t+r}get right(){const{left:t,width:r}=this;return t+r}get aspectRatio(){const{width:t,height:r}=this;return t/r}get corners(){return[{x:this.left,y:this.top},{x:this.right,y:this.top},{x:this.left,y:this.bottom},{x:this.right,y:this.bottom}]}static from({top:t,left:r,width:n,height:o}){return new Kr(r,t,n,o)}static delta(t,r,n={x:"center",y:"center"}){const o=(i,a)=>{const s=n[a],l=a==="x"?i.left:i.top,c=a==="x"?i.width:i.height;return s=="start"?l:s=="end"?l+c:l+c/2};return Qe.delta({x:o(t,"x"),y:o(t,"y")},{x:o(r,"x"),y:o(r,"y")})}static intersectionRatio(t,r){return Kr.from(t).intersectionRatio(Kr.from(r))}};function Z2(e,t){const r=Math.max(t.top,e.top),n=Math.max(t.left,e.left),o=Math.min(t.left+t.width,e.left+e.width),i=Math.min(t.top+t.height,e.top+e.height),a=o-n,s=i-r;return n<o&&r<i?a*s:0}var pg,fg,Gl,ma,Si,vs=class extends(Gl=hn,fg=[Te],pg=[Te],Gl){constructor(t){const r=Qe.from(t);super(r,(n,o)=>Qe.equals(n,o)),H2(Si,5,this),q2(this,ma,0),this.velocity={x:0,y:0}}get delta(){return Qe.delta(this.current,this.initial)}get direction(){const{current:t,previous:r}=this;if(!r)return null;const n={x:t.x-r.x,y:t.y-r.y};return!n.x&&!n.y?null:Math.abs(n.x)>Math.abs(n.y)?n.x>0?"right":"left":n.y>0?"down":"up"}get current(){return super.current}set current(t){const{current:r}=this,n=Qe.from(t),o={x:n.x-r.x,y:n.y-r.y},i=Date.now(),a=i-V2(this,ma),s=l=>Math.round(l/a*100);Ae(()=>{U2(this,ma,i),this.velocity={x:s(o.x),y:s(o.y)},super.current=n})}reset(t=this.defaultValue){super.reset(Qe.from(t)),this.velocity={x:0,y:0}}};Si=B2(Gl);ma=new WeakMap;ug(Si,2,"delta",fg,vs);ug(Si,2,"direction",pg,vs);W2(Si,vs);function Jl({x:e,y:t},r){const n=Math.abs(e),o=Math.abs(t);return typeof r=="number"?Math.sqrt(Mp(n,2)+Mp(o,2))>r:"x"in r&&"y"in r?n>r.x&&o>r.y:"x"in r?n>r.x:"y"in r?o>r.y:!1}var hg=(e=>(e.Horizontal="x",e.Vertical="y",e))(hg||{}),vg=Object.values(hg),Y2=Object.create,_u=Object.defineProperty,K2=Object.defineProperties,X2=Object.getOwnPropertyDescriptor,G2=Object.getOwnPropertyDescriptors,Fa=Object.getOwnPropertySymbols,gg=Object.prototype.hasOwnProperty,mg=Object.prototype.propertyIsEnumerable,_g=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),fo=e=>{throw TypeError(e)},Ql=(e,t,r)=>t in e?_u(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,yu=(e,t)=>{for(var r in t||(t={}))gg.call(t,r)&&Ql(e,r,t[r]);if(Fa)for(var r of Fa(t))mg.call(t,r)&&Ql(e,r,t[r]);return e},bu=(e,t)=>K2(e,G2(t)),Rp=(e,t)=>_u(e,"name",{value:t,configurable:!0}),yg=(e,t)=>{var r={};for(var n in e)gg.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&Fa)for(var n of Fa(e))t.indexOf(n)<0&&mg.call(e,n)&&(r[n]=e[n]);return r},ho=e=>{var t;return[,,,Y2((t=e==null?void 0:e[_g("metadata")])!=null?t:null)]},bg=["class","method","getter","setter","accessor","field","value","get","set"],Do=e=>e!==void 0&&typeof e!="function"?fo("Function expected"):e,J2=(e,t,r,n,o)=>({kind:bg[e],name:t,metadata:n,addInitializer:i=>r._?fo("Already initialized"):o.push(Do(i||null))}),vn=(e,t)=>Ql(t,_g("metadata"),e[3]),ce=(e,t,r,n)=>{for(var o=0,i=e[t>>1],a=i&&i.length;o<a;o++)t&1?i[o].call(r):n=i[o].call(r,n);return n},fe=(e,t,r,n,o,i)=>{var a,s,l,c,d,u=t&7,p=!!(t&8),v=!!(t&16),h=u>3?e.length+1:u?p?1:2:0,m=bg[u+5],y=u>3&&(e[h-1]=[]),b=e[h]||(e[h]=[]),k=u&&(!v&&!p&&(o=o.prototype),u<5&&(u>3||!v)&&X2(u<4?o:{get[r](){return De(this,i)},set[r](_){return vt(this,i,_)}},r));u?v&&u<4&&Rp(i,(u>2?"set ":u>1?"get ":"")+r):Rp(o,r);for(var x=n.length-1;x>=0;x--)c=J2(u,r,l={},e[3],b),u&&(c.static=p,c.private=v,d=c.access={has:v?_=>Q2(o,_):_=>r in _},u^3&&(d.get=v?_=>(u^1?De:xg)(_,o,u^4?i:k.get):_=>_[r]),u>2&&(d.set=v?(_,I)=>vt(_,o,I,u^4?i:k.set):(_,I)=>_[r]=I)),s=(0,n[x])(u?u<4?v?i:k[m]:u>4?void 0:{get:k.get,set:k.set}:o,c),l._=1,u^4||s===void 0?Do(s)&&(u>4?y.unshift(s):u?v?i=s:k[m]=s:o=s):typeof s!="object"||s===null?fo("Object expected"):(Do(a=s.get)&&(k.get=a),Do(a=s.set)&&(k.set=a),Do(a=s.init)&&y.unshift(a));return u||vn(e,o),k&&_u(o,r,k),v?u^4?i:k:o},xu=(e,t,r)=>t.has(e)||fo("Cannot "+r),Q2=(e,t)=>Object(t)!==t?fo('Cannot use the "in" operator on this value'):e.has(t),De=(e,t,r)=>(xu(e,t,"read from private field"),r?r.call(e):t.get(e)),_e=(e,t,r)=>t.has(e)?fo("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),vt=(e,t,r,n)=>(xu(e,t,"write to private field"),n?n.call(e,r):t.set(e,r),r),xg=(e,t,r)=>(xu(e,t,"access private method"),r);function kg(e,t){return{plugin:e,options:t}}function Ei(e){return t=>kg(e,t)}function ui(e){return typeof e=="function"?{plugin:e,options:void 0}:e}var wg,di,ku,_a;wg=[pe];var Xe=class{constructor(e,t){this.manager=e,this.options=t,_e(this,ku,ce(di,8,this,!1)),ce(di,11,this),_e(this,_a,new Set)}enable(){this.disabled=!1}disable(){this.disabled=!0}isDisabled(){return de(()=>this.disabled)}configure(e){this.options=e}registerEffect(e){const t=pt(e.bind(this));return De(this,_a).add(t),t}destroy(){De(this,_a).forEach(e=>e())}static configure(e){return kg(this,e)}};di=ho(null);ku=new WeakMap;_a=new WeakMap;fe(di,4,"disabled",wg,Xe,ku);vn(di,Xe);var Ii=class extends Xe{},ya,Xs=class{constructor(e){this.manager=e,this.instances=new Map,_e(this,ya,[])}get values(){return Array.from(this.instances.values())}set values(e){const t=e.map(ui).reduce((n,o)=>{const i=n.find(({plugin:a})=>a===o.plugin);return i?(i.options=o.options,n):[...n,o]},[]),r=t.map(({plugin:n})=>n);for(const n of De(this,ya))if(!r.includes(n)){if(n.prototype instanceof Ii)continue;this.unregister(n)}for(const{plugin:n,options:o}of t)this.register(n,o);vt(this,ya,r)}get(e){return this.instances.get(e)}register(e,t){const r=this.instances.get(e);if(r)return r.options!==t&&(r.options=t),r;const n=new e(this.manager,t);return this.instances.set(e,n),n}unregister(e){const t=this.instances.get(e);t&&(t.destroy(),this.instances.delete(e))}destroy(){for(const e of this.instances.values())e.destroy();this.instances.clear()}};ya=new WeakMap;function eS(e,t){return e.priority===t.priority?e.type===t.type?t.value-e.value:t.type-e.type:t.priority-e.priority}var Gi=[],Tn,Mn,tS=class extends Xe{constructor(e){super(e),_e(this,Tn),_e(this,Mn),this.computeCollisions=this.computeCollisions.bind(this),vt(this,Mn,lo(Gi)),this.destroy=wi(()=>{const t=this.computeCollisions(),r=de(()=>this.manager.dragOperation.position.current);if(t!==Gi){const n=De(this,Tn);if(vt(this,Tn,r),n&&r.x==n.x&&r.y==n.y)return}else vt(this,Tn,void 0);De(this,Mn).value=t},()=>{const{dragOperation:t}=this.manager;t.status.initialized&&this.forceUpdate()})}forceUpdate(e=!0){de(()=>{e?De(this,Mn).value=this.computeCollisions():vt(this,Tn,void 0)})}computeCollisions(e,t){const{registry:r,dragOperation:n}=this.manager,{source:o,shape:i,status:a}=n;if(!a.initialized||!i)return Gi;const s=[],l=[];for(const c of e??r.droppables){if(c.disabled||o&&!c.accepts(o))continue;const d=t??c.collisionDetector;if(!d)continue;l.push(c),c.shape;const u=de(()=>d({droppable:c,dragOperation:n}));u&&(c.collisionPriority!=null&&(u.priority=c.collisionPriority),s.push(u))}return l.length===0?Gi:(s.sort(eS),s)}get collisions(){return De(this,Mn).value}};Tn=new WeakMap;Mn=new WeakMap;var Sg,Eg,Ig,wu,Cg,jt,Su,Wn,Eu,Iu;Ig=[pe],Eg=[pe],Sg=[pe];var dr=class Xr{constructor(t,r){_e(this,Su,ce(jt,8,this)),ce(jt,11,this),_e(this,Wn),_e(this,Eu,ce(jt,12,this)),ce(jt,15,this),_e(this,Iu,ce(jt,16,this)),ce(jt,19,this);const{effects:n,id:o,data:i={},disabled:a=!1,register:s=!0}=t;let l=o;vt(this,Wn,lo(o)),this.manager=r,this.data=i,this.disabled=a,this.effects=()=>{var c;return[()=>{const{id:d,manager:u}=this;if(d!==l)return l=d,u==null||u.registry.register(this),()=>u==null?void 0:u.registry.unregister(this)},...(c=n==null?void 0:n())!=null?c:[]]},this.register=this.register.bind(this),this.unregister=this.unregister.bind(this),this.destroy=this.destroy.bind(this),r&&s&&queueMicrotask(this.register)}get id(){var t,r;const n=De(this,Wn).value;return(r=(t=Xr.pendingIdChanges)==null?void 0:t.get(this))!=null?r:n}set id(t){var r,n;const o=(n=(r=Xr.pendingIdChanges)==null?void 0:r.get(this))!=null?n:De(this,Wn).peek();t!==o&&(Xr.pendingIdChanges||(Xr.pendingIdChanges=new Map,queueMicrotask(()=>{var i;return xg(i=Xr,wu,Cg).call(i)})),Xr.pendingIdChanges.set(this,t))}register(){var t;return(t=this.manager)==null?void 0:t.registry.register(this)}unregister(){var t;(t=this.manager)==null||t.registry.unregister(this)}destroy(){var t;(t=this.manager)==null||t.registry.unregister(this)}};jt=ho(null);wu=new WeakSet;Cg=function(){const e=dr.pendingIdChanges;dr.pendingIdChanges=null,e&&Ae(()=>{for(const[t,r]of e)De(t,Wn).value=r})};Su=new WeakMap;Wn=new WeakMap;Eu=new WeakMap;Iu=new WeakMap;fe(jt,4,"manager",Ig,dr,Su);fe(jt,4,"data",Eg,dr,Eu);fe(jt,4,"disabled",Sg,dr,Iu);_e(dr,wu);vn(jt,dr);dr.pendingIdChanges=null;var gs=dr,Lp=class{constructor(){this.map=lo(new Map),this.cleanupFunctions=new WeakMap,this.register=(e,t)=>{const r=this.map.peek(),n=r.get(e),o=()=>this.unregister(e,t);if(n===t)return o;if(n&&n.id===e){const s=this.cleanupFunctions.get(n);s==null||s(),this.cleanupFunctions.delete(n)}const i=new Map(r);for(const[s,l]of r)if(l===t&&s!==e){i.delete(s);break}i.set(e,t),this.map.value=i;const a=wi(...t.effects());return this.cleanupFunctions.set(t,a),o},this.unregister=(e,t)=>{const r=this.map.peek();if(r.get(e)!==t)return;const n=this.cleanupFunctions.get(t);n==null||n(),this.cleanupFunctions.delete(t);const o=new Map(r);o.delete(e),this.map.value=o}}[Symbol.iterator](){return this.map.peek().values()}get value(){return this.map.value.values()}has(e){return this.map.value.has(e)}get(e){return this.map.value.get(e)}destroy(){for(const e of this){const t=this.cleanupFunctions.get(e);t==null||t(),e.destroy()}this.map.value=new Map}},Pg,zg,Ag,jg,Og,Dg,ec,nt,Cu,Pu,zu,Xt=class extends(ec=gs,Dg=[pe],Og=[pe],jg=[pe],Ag=[Te],zg=[Te],Pg=[Te],ec){constructor(t,r){var n=t,{modifiers:o,type:i,sensors:a,plugins:s,effects:l}=n,c=yg(n,["modifiers","type","sensors","plugins","effects"]);super(bu(yu({},c),{effects:()=>{var d;return[...(d=l==null?void 0:l())!=null?d:[],()=>{const{manager:u,plugins:p}=this;if(!(!u||!p))for(const v of p){const{plugin:h}=ui(v);u.registry.plugins.register(h)}}]}}),r),ce(nt,5,this),_e(this,Cu,ce(nt,8,this)),ce(nt,11,this),_e(this,Pu,ce(nt,12,this)),ce(nt,15,this),_e(this,zu,ce(nt,16,this,this.isDragSource?"dragging":"idle")),ce(nt,19,this),this.type=i,this.sensors=a,this.modifiers=o,this.alignment=c.alignment,this.plugins=s}pluginConfig(t){if(this.plugins)for(const r of this.plugins){const n=ui(r);if(n.plugin===t)return n.options}}get isDropping(){return this.status==="dropping"&&this.isDragSource}get isDragging(){return this.status==="dragging"&&this.isDragSource}get isDragSource(){var t,r;return((r=(t=this.manager)==null?void 0:t.dragOperation.source)==null?void 0:r.id)===this.id}};nt=ho(ec);Cu=new WeakMap;Pu=new WeakMap;zu=new WeakMap;fe(nt,4,"type",Dg,Xt,Cu);fe(nt,4,"modifiers",Og,Xt,Pu);fe(nt,4,"status",jg,Xt,zu);fe(nt,2,"isDropping",Ag,Xt);fe(nt,2,"isDragging",zg,Xt);fe(nt,2,"isDragSource",Pg,Xt);vn(nt,Xt);var Tg,Mg,Rg,Lg,Fg,Ng,tc,Fe,Au,ju,Ou,Du,Tu,Gt=class extends(tc=gs,Ng=[pe],Fg=[pe],Lg=[pe],Rg=[pe],Mg=[pe],Tg=[Te],tc){constructor(t,r){var n=t,{accept:o,collisionDetector:i,collisionPriority:a,type:s}=n,l=yg(n,["accept","collisionDetector","collisionPriority","type"]);super(l,r),ce(Fe,5,this),_e(this,Au,ce(Fe,8,this)),ce(Fe,11,this),_e(this,ju,ce(Fe,12,this)),ce(Fe,15,this),_e(this,Ou,ce(Fe,16,this)),ce(Fe,19,this),_e(this,Du,ce(Fe,20,this)),ce(Fe,23,this),_e(this,Tu,ce(Fe,24,this)),ce(Fe,27,this),this.accept=o,this.collisionDetector=i,this.collisionPriority=a,this.type=s}accepts(t){const{accept:r}=this;return r?typeof r=="function"?r(t):t.type?Array.isArray(r)?r.includes(t.type):t.type===r:!1:!0}get isDropTarget(){var t,r;return((r=(t=this.manager)==null?void 0:t.dragOperation.target)==null?void 0:r.id)===this.id}};Fe=ho(tc);Au=new WeakMap;ju=new WeakMap;Ou=new WeakMap;Du=new WeakMap;Tu=new WeakMap;fe(Fe,4,"accept",Ng,Gt,Au);fe(Fe,4,"type",Fg,Gt,ju);fe(Fe,4,"collisionDetector",Lg,Gt,Ou);fe(Fe,4,"collisionPriority",Rg,Gt,Du);fe(Fe,4,"shape",Mg,Gt,Tu);fe(Fe,2,"isDropTarget",Tg,Gt);vn(Fe,Gt);var rS=class{constructor(){this.registry=new Map}addEventListener(e,t){const{registry:r}=this,n=new Set(r.get(e));return n.add(t),r.set(e,n),()=>this.removeEventListener(e,t)}removeEventListener(e,t){const{registry:r}=this,n=new Set(r.get(e));n.delete(t),r.set(e,n)}dispatch(e,...t){const{registry:r}=this,n=r.get(e);if(n)for(const o of n)o(...t)}},nS=class extends rS{constructor(e){super(),this.manager=e}dispatch(e,t){const r=[t,this.manager];super.dispatch(e,...r)}};function ba(e,t=!0){let r=!1;return bu(yu({},e),{cancelable:t,get defaultPrevented(){return r},preventDefault(){t&&(r=!0)}})}var oS=class extends Ii{constructor(e){super(e);const t=(n,o)=>n.map(({id:i})=>i).join("")===o.map(({id:i})=>i).join("");let r=[];this.destroy=wi(()=>{const{dragOperation:n,collisionObserver:o}=e;n.status.initializing&&(r=[],o.enable())},()=>{const{collisionObserver:n,monitor:o}=e,{collisions:i}=n;if(n.isDisabled()||gs.pendingIdChanges)return;const a=ba({collisions:i});if(o.dispatch("collision",a),a.defaultPrevented||t(i,r))return;r=i;const[s]=i;de(()=>{var l;(s==null?void 0:s.id)!==((l=e.dragOperation.target)==null?void 0:l.id)&&(n.disable(),e.actions.setDropTarget(s==null?void 0:s.id).then(()=>{n.enable()}))})})}},kt=(e=>(e[e.Lowest=0]="Lowest",e[e.Low=1]="Low",e[e.Normal=2]="Normal",e[e.High=3]="High",e[e.Highest=4]="Highest",e))(kt||{}),Jt=(e=>(e[e.Collision=0]="Collision",e[e.ShapeIntersection=1]="ShapeIntersection",e[e.PointerIntersection=2]="PointerIntersection",e))(Jt||{}),Bg,$g,Wg,Hg,Vg,qg,Ug,St,Mu;Ug=[pe],qg=[Te],Vg=[Te],Hg=[Te],Wg=[Te],$g=[Te],Bg=[Te];var hr=class{constructor(){ce(St,5,this),_e(this,Mu,ce(St,8,this,"idle")),ce(St,11,this)}get current(){return this.value}get idle(){return this.value==="idle"}get initializing(){return this.value==="initializing"}get initialized(){const{value:e}=this;return e!=="idle"&&e!=="initialization-pending"}get dragging(){return this.value==="dragging"}get dropped(){return this.value==="dropped"}set(e){this.value=e}};St=ho(null);Mu=new WeakMap;fe(St,4,"value",Ug,hr,Mu);fe(St,2,"current",qg,hr);fe(St,2,"idle",Vg,hr);fe(St,2,"initializing",Hg,hr);fe(St,2,"initialized",Wg,hr);fe(St,2,"dragging",$g,hr);fe(St,2,"dropped",Bg,hr);vn(St,hr);var iS=class{constructor(e){this.manager=e}setDragSource(e){const{dragOperation:t}=this.manager;t.sourceIdentifier=typeof e=="string"||typeof e=="number"?e:e.id}setDropTarget(e){return de(()=>{const{dragOperation:t}=this.manager,r=e??null;if(t.targetIdentifier===r)return Promise.resolve(!1);t.targetIdentifier=r;const n=ba({operation:t.snapshot()});return t.status.dragging&&this.manager.monitor.dispatch("dragover",n),this.manager.renderer.rendering.then(()=>n.defaultPrevented)})}start(e){return de(()=>{const{dragOperation:t}=this.manager;if(e.source!=null&&this.setDragSource(e.source),!t.source)throw new Error("Cannot start a drag operation without a drag source");if(!t.status.idle)throw new Error("Cannot start a drag operation while another is active");const n=new AbortController,{event:o,coordinates:i}=e;Ae(()=>{t.status.set("initialization-pending"),t.shape=null,t.canceled=!1,t.activatorEvent=o??null,t.position.reset(i)});const a=ba({operation:t.snapshot()});return this.manager.monitor.dispatch("beforedragstart",a),a.defaultPrevented?(t.reset(),n.abort(),n):(t.status.set("initializing"),t.controller=n,this.manager.renderer.rendering.then(()=>{if(n.signal.aborted)return;const{status:s}=t;s.current==="initializing"&&Ae(()=>{t.status.set("dragging"),this.manager.monitor.dispatch("dragstart",{nativeEvent:o,operation:t.snapshot(),cancelable:!1})})}),n)})}move(e){return de(()=>{var t,r;const{dragOperation:n}=this.manager,{status:o,controller:i}=n;if(!o.dragging||!i||i.signal.aborted)return;const a=ba({nativeEvent:e.event,operation:n.snapshot(),by:e.by,to:e.to},(t=e.cancelable)!=null?t:!0);((r=e.propagate)==null||r)&&this.manager.monitor.dispatch("dragmove",a),queueMicrotask(()=>{var s,l,c,d,u;if(a.defaultPrevented)return;const p=(u=e.to)!=null?u:{x:n.position.current.x+((l=(s=e.by)==null?void 0:s.x)!=null?l:0),y:n.position.current.y+((d=(c=e.by)==null?void 0:c.y)!=null?d:0)};n.position.current=p})})}stop(e={}){return de(()=>{var t,r;const{dragOperation:n}=this.manager,{controller:o}=n;if(!o||o.signal.aborted)return;let i;const a=()=>{const l={resume:()=>{},abort:()=>{}};return i=new Promise((c,d)=>{l.resume=c,l.abort=d}),l};o.abort();const s=()=>{this.manager.renderer.rendering.then(()=>{n.status.set("dropped");const l=de(()=>{var d;return((d=n.source)==null?void 0:d.status)==="dropping"}),c=()=>{n.controller===o&&(n.controller=void 0),n.reset()};if(l){const{source:d}=n,u=pt(()=>{(d==null?void 0:d.status)==="idle"&&(u(),c())})}else this.manager.renderer.rendering.then(c)})};n.canceled=(t=e.canceled)!=null?t:!1,this.manager.monitor.dispatch("dragend",{nativeEvent:e.event,operation:n.snapshot(),canceled:(r=e.canceled)!=null?r:!1,suspend:a}),i?i.then(s).catch(()=>n.reset()):s()})}},Yn=class extends Xe{constructor(e,t){super(e,t),this.manager=e,this.options=t}},aS=class extends AbortController{constructor(e,t){super(),this.constraints=e,this.onActivate=t,this.activated=!1;for(const r of e??[])r.controller=this}onEvent(e){var t;if(!this.activated)if((t=this.constraints)!=null&&t.length)for(const r of this.constraints)r.onEvent(e);else this.activate(e)}activate(e){this.activated||(this.activated=!0,this.onActivate(e))}abort(e){this.activated=!1,super.abort(e)}},xa,Zg=class{constructor(e){this.options=e,_e(this,xa)}set controller(e){vt(this,xa,e),e.signal.addEventListener("abort",()=>this.abort())}activate(e){var t;(t=De(this,xa))==null||t.activate(e)}};xa=new WeakMap;var Fp=class extends Xe{constructor(e,t){super(e,t),this.manager=e,this.options=t}apply(e){return e.transform}},sS=class{constructor(e){this.draggables=new Lp,this.droppables=new Lp,this.plugins=new Xs(e),this.sensors=new Xs(e),this.modifiers=new Xs(e)}register(e,t){if(e instanceof Xt)return this.draggables.register(e.id,e);if(e instanceof Gt)return this.droppables.register(e.id,e);if(e.prototype instanceof Fp)return this.modifiers.register(e,t);if(e.prototype instanceof Yn)return this.sensors.register(e,t);if(e.prototype instanceof Xe)return this.plugins.register(e,t);throw new Error("Invalid instance type")}unregister(e){if(e instanceof gs)return e instanceof Xt?this.draggables.unregister(e.id,e):e instanceof Gt?this.droppables.unregister(e.id,e):()=>{};if(e.prototype instanceof Fp)return this.modifiers.unregister(e);if(e.prototype instanceof Yn)return this.sensors.unregister(e);if(e.prototype instanceof Xe)return this.plugins.unregister(e);throw new Error("Invalid instance type")}destroy(){this.draggables.destroy(),this.droppables.destroy(),this.plugins.destroy(),this.sensors.destroy(),this.modifiers.destroy()}},Yg,Kg,Xg,Gg,Jg,Qg,em,tm,rm,To,ka,Rn,ze,Ru,Lu,Fu,Nu,Bu,Mo;rm=[Te],tm=[pe],em=[pe],Qg=[pe],Jg=[pe],Gg=[pe],Xg=[Te],Kg=[Te],Yg=[Te];var Rt=class{constructor(e){ce(ze,5,this),_e(this,To),_e(this,ka),_e(this,Rn,new hn(void 0,(t,r)=>t&&r?t.equals(r):t===r)),this.status=new hr,_e(this,Ru,ce(ze,8,this,!1)),ce(ze,11,this),_e(this,Lu,ce(ze,12,this,null)),ce(ze,15,this),_e(this,Fu,ce(ze,16,this,null)),ce(ze,19,this),_e(this,Nu,ce(ze,20,this,null)),ce(ze,23,this),_e(this,Bu,ce(ze,24,this,[])),ce(ze,27,this),this.position=new vs({x:0,y:0}),_e(this,Mo,{x:0,y:0}),vt(this,To,e)}get shape(){const{current:e,initial:t,previous:r}=De(this,Rn);return!e||!t?null:{current:e,initial:t,previous:r}}set shape(e){e?De(this,Rn).current=e:De(this,Rn).reset()}get source(){var e;const t=this.sourceIdentifier;if(t==null)return null;const r=De(this,To).registry.draggables.get(t);return r&&vt(this,ka,r),(e=r??De(this,ka))!=null?e:null}get target(){var e;const t=this.targetIdentifier;return t!=null&&(e=De(this,To).registry.droppables.get(t))!=null?e:null}get transform(){const{x:e,y:t}=this.position.delta;let r={x:e,y:t};for(const n of this.modifiers)r=n.apply(bu(yu({},this.snapshot()),{transform:r}));return vt(this,Mo,r),r}snapshot(){return de(()=>({source:this.source,target:this.target,activatorEvent:this.activatorEvent,transform:De(this,Mo),shape:this.shape?Ks(this.shape):null,position:Ks(this.position),status:Ks(this.status),canceled:this.canceled}))}reset(){Ae(()=>{this.status.set("idle"),this.sourceIdentifier=null,this.targetIdentifier=null,De(this,Rn).reset(),this.position.reset({x:0,y:0}),vt(this,Mo,{x:0,y:0}),this.modifiers=[]})}};ze=ho(null);To=new WeakMap;ka=new WeakMap;Rn=new WeakMap;Ru=new WeakMap;Lu=new WeakMap;Fu=new WeakMap;Nu=new WeakMap;Bu=new WeakMap;Mo=new WeakMap;fe(ze,2,"shape",rm,Rt);fe(ze,4,"canceled",tm,Rt,Ru);fe(ze,4,"activatorEvent",em,Rt,Lu);fe(ze,4,"sourceIdentifier",Qg,Rt,Fu);fe(ze,4,"targetIdentifier",Jg,Rt,Nu);fe(ze,4,"modifiers",Gg,Rt,Bu);fe(ze,2,"source",Xg,Rt);fe(ze,2,"target",Kg,Rt);fe(ze,2,"transform",Yg,Rt);vn(ze,Rt);var lS={get rendering(){return Promise.resolve()}};function Dt(e,t){return typeof e=="function"?e(t):e??t}var cS=class{constructor(t){this.destroy=()=>{this.dragOperation.status.idle||this.actions.stop({canceled:!0}),this.dragOperation.modifiers.forEach(p=>p.destroy()),this.registry.destroy(),this.collisionObserver.destroy()};var r;const n=t??{},o=Dt(n.plugins,[]),i=Dt(n.sensors,[]),a=Dt(n.modifiers,[]),s=(r=n.renderer)!=null?r:lS,l=new nS(this),c=new sS(this);this.registry=c,this.monitor=l,this.renderer=s,this.actions=new iS(this),this.dragOperation=new Rt(this),this.collisionObserver=new tS(this),this.plugins=[oS,...o],this.modifiers=a,this.sensors=i;const{destroy:d}=this,u=wi(()=>{var p,v,h;const m=de(()=>this.dragOperation.modifiers),y=this.modifiers;for(const b of m)y.includes(b)||b.destroy();this.dragOperation.modifiers=(h=(v=(p=this.dragOperation.source)==null?void 0:p.modifiers)==null?void 0:v.map(b=>{const{plugin:k,options:x}=ui(b);return new k(this,x)}))!=null?h:y});this.destroy=()=>{u(),d()}}get plugins(){return this.registry.plugins.values}set plugins(t){this.registry.plugins.values=t}get modifiers(){return this.registry.modifiers.values}set modifiers(t){this.registry.modifiers.values=t}get sensors(){return this.registry.sensors.values}set sensors(t){this.registry.sensors.values=t}},nm=e=>{throw TypeError(e)},$u=(e,t,r)=>t.has(e)||nm("Cannot "+r),le=(e,t,r)=>($u(e,t,"read from private field"),t.get(e)),ct=(e,t,r)=>t.has(e)?nm("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),ft=(e,t,r,n)=>($u(e,t,"write to private field"),t.set(e,r),r),om=(e,t,r)=>($u(e,t,"access private method"),r);function ms(e){return e?e instanceof KeyframeEffect?!0:"getKeyframes"in e&&typeof e.getKeyframes=="function":!1}function im(e,t){const r=e.getAnimations();let n=null;for(const o of r){if(o.playState!=="running")continue;const{effect:i}=o,s=(ms(i)?i.getKeyframes():[]).filter(t);s.length>0&&(n=[s[s.length-1],o])}return n}function _s(e){const{width:t,height:r,top:n,left:o,bottom:i,right:a}=e.getBoundingClientRect();return{width:t,height:r,top:n,left:o,bottom:i,right:a}}function Wu(e){const t=Object.prototype.toString.call(e);return t==="[object Window]"||t==="[object global]"}function Ci(e){return"nodeType"in e}function _t(e){var t,r,n;return e?Wu(e)?e:Ci(e)?"defaultView"in e?(t=e.defaultView)!=null?t:window:(n=(r=e.ownerDocument)==null?void 0:r.defaultView)!=null?n:window:window:window}function Hu(e){const{Document:t}=_t(e);return e instanceof t||"nodeType"in e&&e.nodeType===Node.DOCUMENT_NODE}function Rr(e){return!e||Wu(e)?!1:e instanceof _t(e).HTMLElement||"namespaceURI"in e&&typeof e.namespaceURI=="string"&&e.namespaceURI.endsWith("html")}function am(e){return e instanceof _t(e).SVGElement||"namespaceURI"in e&&typeof e.namespaceURI=="string"&&e.namespaceURI.endsWith("svg")}function vo(e){return e?Wu(e)?e.document:Ci(e)?Hu(e)?e:Rr(e)||am(e)?e.ownerDocument:document:document:document}function uS(e){var t,r,n,o;const{documentElement:i}=vo(e),a=_t(e).visualViewport,s=(t=a==null?void 0:a.width)!=null?t:i.clientWidth,l=(r=a==null?void 0:a.height)!=null?r:i.clientHeight,c=(n=a==null?void 0:a.offsetTop)!=null?n:0,d=(o=a==null?void 0:a.offsetLeft)!=null?o:0;return{top:c,left:d,right:d+s,bottom:c+l,width:s,height:l}}function dS(e,t){if(pS(e)&&e.open===!1)return!1;const{overflow:r,overflowX:n,overflowY:o}=getComputedStyle(e);return r==="visible"&&n==="visible"&&o==="visible"}function pS(e){return e.tagName==="DETAILS"}function pi(e,t=e.getBoundingClientRect(),r=0){var n,o,i,a,s;let l=t;const{ownerDocument:c}=e,d=(n=c.defaultView)!=null?n:window;let u=e.parentElement;for(;u&&u!==c.documentElement;){if(!dS(u)){const x=u.getBoundingClientRect(),_=r*(x.bottom-x.top),I=r*(x.right-x.left),w=r*(x.bottom-x.top),A=r*(x.right-x.left);l={top:Math.max(l.top,x.top-_),right:Math.min(l.right,x.right+I),bottom:Math.min(l.bottom,x.bottom+w),left:Math.max(l.left,x.left-A),width:0,height:0},l.width=l.right-l.left,l.height=l.bottom-l.top}u=u.parentElement}const p=d.visualViewport,v=(o=p==null?void 0:p.offsetTop)!=null?o:0,h=(i=p==null?void 0:p.offsetLeft)!=null?i:0,m=(a=p==null?void 0:p.width)!=null?a:d.innerWidth,y=(s=p==null?void 0:p.height)!=null?s:d.innerHeight,b=r*y,k=r*m;return l={top:Math.max(l.top,v-b),right:Math.min(l.right,h+m+k),bottom:Math.min(l.bottom,v+y+b),left:Math.max(l.left,h-k),width:0,height:0},l.width=l.right-l.left,l.height=l.bottom-l.top,l.width<0&&(l.width=0),l.height<0&&(l.height=0),l}function Kn(e){return{x:e.clientX,y:e.clientY}}var sm=typeof window<"u"&&typeof window.document<"u"&&typeof window.document.createElement<"u";function rc(e=document,t=new Set){if(t.has(e))return[];t.add(e);const r=[e];for(const n of Array.from(e.querySelectorAll("iframe, frame")))try{const o=n.contentDocument;o&&!t.has(o)&&r.push(...rc(o,t))}catch{}try{const n=e.defaultView;if(n&&n!==window.top){const o=n.parent;o&&o.document&&o.document!==e&&r.push(...rc(o.document,t))}}catch{}return r}function Vu(){return/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}function lm(){var e,t;const r=Vu()?window.visualViewport:null;return{x:(e=r==null?void 0:r.offsetLeft)!=null?e:0,y:(t=r==null?void 0:r.offsetTop)!=null?t:0}}function qu(e){return!e||!Ci(e)?!1:e instanceof _t(e).ShadowRoot}function Na(e){if(e&&Ci(e)){let t=e.getRootNode();if(qu(t))return t;if(t instanceof Document)return t}return vo(e)}function Uu(e){return e.matchMedia("(prefers-reduced-motion: reduce)").matches}function fS(e){const t="input, textarea, select, canvas, [contenteditable]",r=e.cloneNode(!0),n=Array.from(e.querySelectorAll(t));return Array.from(r.querySelectorAll(t)).forEach((i,a)=>{const s=n[a];if(Np(i)&&Np(s)&&(i.type!=="file"&&(i.value=s.value),i.type==="radio"&&i.name&&(i.name=`Cloned__${i.name}`)),Bp(i)&&Bp(s)&&s.width>0&&s.height>0){const l=i.getContext("2d");l==null||l.drawImage(s,0,0)}}),r}function Np(e){return"value"in e}function Bp(e){return e.tagName==="CANVAS"}function cm(e,{x:t,y:r}){const n=e.elementFromPoint(t,r);if(hS(n)){const{contentDocument:o}=n;if(o){const{left:i,top:a}=n.getBoundingClientRect();return cm(o,{x:t-i,y:r-a})}}return n}function hS(e){return(e==null?void 0:e.tagName)==="IFRAME"}var nc=new WeakMap;function vS(e){return!!e.closest(`
      input:not([disabled]),
      select:not([disabled]),
      textarea:not([disabled]),
      button:not([disabled]),
      a[href],
      [contenteditable]:not([contenteditable="false"])
    `)}var um=class{constructor(){this.entries=new Set,this.clear=()=>{for(const e of this.entries){const[t,{type:r,listener:n,options:o}]=e;t.removeEventListener(r,n,o)}this.entries.clear()}}bind(e,t){const r=Array.isArray(e)?e:[e],n=Array.isArray(t)?t:[t],o=[];for(const a of r)for(const s of n){const{type:l,listener:c,options:d}=s,u=[a,s];a.addEventListener(l,c,d),this.entries.add(u),o.push(u)}const i=this.entries;return function(){for(const s of o){const[l,{type:c,listener:d,options:u}]=s;l.removeEventListener(c,d,u),i.delete(s)}}}};function Xn(e){const t=e==null?void 0:e.ownerDocument.defaultView;if(t&&t.self!==t.parent)return t.frameElement}function gS(e){const t=new Set;let r=Xn(e);for(;r;)t.add(r),r=Xn(r);return t}function mS(e,t){const r=setTimeout(e,t);return()=>clearTimeout(r)}function dm(e,t){const r=()=>performance.now();let n,o;return function(...i){const a=this;o?(n==null||n(),n=mS(()=>{e.apply(a,i),o=r()},t-(r()-o))):(e.apply(a,i),o=r())}}function _S(e,t){return e===t?!0:!e||!t?!1:e.top==t.top&&e.left==t.left&&e.right==t.right&&e.bottom==t.bottom}function yS(e,t=e.getBoundingClientRect()){const{width:r,height:n}=pi(e,t);return r>0&&n>0}var bS=sm?ResizeObserver:class{observe(){}unobserve(){}disconnect(){}},wa,xS=class extends bS{constructor(e){super(t=>{if(!le(this,wa)){ft(this,wa,!0);return}e(t,this)}),ct(this,wa,!1)}};wa=new WeakMap;var $p=Array.from({length:100},(e,t)=>t/100),pm=75,Gr,Ba,xr,Jr,Ro,Ye,Ko,Lo,$a,fm,hm,vm=class{constructor(e,t,r={debug:!1,skipInitial:!1}){this.element=e,this.callback=t,ct(this,$a),this.disconnect=()=>{var i,a,s;ft(this,Ko,!0),(i=le(this,xr))==null||i.disconnect(),(a=le(this,Jr))==null||a.disconnect(),le(this,Ro).disconnect(),(s=le(this,Ye))==null||s.remove()},ct(this,Gr,!0),ct(this,Ba),ct(this,xr),ct(this,Jr),ct(this,Ro),ct(this,Ye),ct(this,Ko,!1),ct(this,Lo,dm(()=>{var i,a,s;const{element:l}=this;if((i=le(this,Jr))==null||i.disconnect(),le(this,Ko)||!le(this,Gr)||!l.isConnected)return;const c=(a=l.ownerDocument)!=null?a:document,{innerHeight:d,innerWidth:u}=(s=c.defaultView)!=null?s:window,p=l.getBoundingClientRect(),v=pi(l,p),{top:h,left:m,bottom:y,right:b}=v,k=-Math.floor(h),x=-Math.floor(m),_=-Math.floor(u-b),I=-Math.floor(d-y),w=`${k}px ${_}px ${I}px ${x}px`;this.boundingClientRect=p,ft(this,Jr,new IntersectionObserver(A=>{const[E]=A,{intersectionRect:C}=E;(E.intersectionRatio!==1?E.intersectionRatio:It.intersectionRatio(C,pi(l)))!==1&&le(this,Lo).call(this)},{threshold:$p,rootMargin:w,root:c})),le(this,Jr).observe(l),om(this,$a,fm).call(this)},pm)),this.boundingClientRect=e.getBoundingClientRect(),ft(this,Gr,yS(e,this.boundingClientRect));let n=!0;this.callback=i=>{n&&(n=!1,r.skipInitial)||t(i)};const o=e.ownerDocument;r!=null&&r.debug&&(ft(this,Ye,document.createElement("div")),le(this,Ye).style.background="rgba(0,0,0,0.15)",le(this,Ye).style.position="fixed",le(this,Ye).style.pointerEvents="none",o.body.appendChild(le(this,Ye))),ft(this,Ro,new IntersectionObserver(i=>{var a,s;const l=i[i.length-1],{boundingClientRect:c,isIntersecting:d}=l,{width:u,height:p}=c,v=le(this,Gr);ft(this,Gr,d),!(!u&&!p)&&(v&&!d?((a=le(this,Jr))==null||a.disconnect(),this.callback(null),(s=le(this,xr))==null||s.disconnect(),ft(this,xr,void 0),le(this,Ye)&&(le(this,Ye).style.visibility="hidden")):le(this,Lo).call(this),d&&!le(this,xr)&&(ft(this,xr,new xS(le(this,Lo))),le(this,xr).observe(e)))},{threshold:$p,root:o})),le(this,Gr)&&!r.skipInitial&&this.callback(this.boundingClientRect),le(this,Ro).observe(e)}};Gr=new WeakMap;Ba=new WeakMap;xr=new WeakMap;Jr=new WeakMap;Ro=new WeakMap;Ye=new WeakMap;Ko=new WeakMap;Lo=new WeakMap;$a=new WeakSet;fm=function(){le(this,Ko)||(om(this,$a,hm).call(this),!_S(this.boundingClientRect,le(this,Ba))&&(this.callback(this.boundingClientRect),ft(this,Ba,this.boundingClientRect)))};hm=function(){if(le(this,Ye)){const{top:e,left:t,width:r,height:n}=pi(this.element);le(this,Ye).style.overflow="hidden",le(this,Ye).style.visibility="visible",le(this,Ye).style.top=`${Math.floor(e)}px`,le(this,Ye).style.left=`${Math.floor(t)}px`,le(this,Ye).style.width=`${Math.floor(r)}px`,le(this,Ye).style.height=`${Math.floor(n)}px`}};var Ji=new WeakMap,Qi=new WeakMap;function kS(e,t){let r=Ji.get(e);return r||(r={disconnect:new vm(e,o=>{const i=Ji.get(e);i&&i.callbacks.forEach(a=>a(o))},{skipInitial:!0}).disconnect,callbacks:new Set}),r.callbacks.add(t),Ji.set(e,r),()=>{r.callbacks.delete(t),r.callbacks.size===0&&(Ji.delete(e),r.disconnect())}}function wS(e,t){const r=new Set;for(const n of e){const o=kS(n,t);r.add(o)}return()=>r.forEach(n=>n())}function SS(e,t){var r;const n=e.ownerDocument;if(!Qi.has(n)){const a=new AbortController,s=new Set;document.addEventListener("scroll",l=>s.forEach(c=>c(l)),{capture:!0,passive:!0,signal:a.signal}),Qi.set(n,{disconnect:()=>a.abort(),listeners:s})}const{listeners:o,disconnect:i}=(r=Qi.get(n))!=null?r:{};return!o||!i?()=>{}:(o.add(t),()=>{o.delete(t),o.size===0&&(i(),Qi.delete(n))})}var Fo,No,Sa,oc,ES=class{constructor(e,t,r){this.callback=t,ct(this,Fo),ct(this,No,!1),ct(this,Sa),ct(this,oc,dm(a=>{if(!le(this,No)&&a.target&&"contains"in a.target&&typeof a.target.contains=="function"){for(const s of le(this,Sa))if(a.target.contains(s)){this.callback(le(this,Fo).boundingClientRect);break}}},pm));const n=gS(e),o=wS(n,t),i=SS(e,le(this,oc));ft(this,Sa,n),ft(this,Fo,new vm(e,t,r)),this.disconnect=()=>{le(this,No)||(ft(this,No,!0),o(),i(),le(this,Fo).disconnect())}}};Fo=new WeakMap;No=new WeakMap;Sa=new WeakMap;oc=new WeakMap;function ic(e){return"showPopover"in e&&"hidePopover"in e&&typeof e.showPopover=="function"&&typeof e.hidePopover=="function"}function Un(e){try{ic(e)&&e.isConnected&&e.hasAttribute("popover")&&!e.matches(":popover-open")&&e.showPopover()}catch{}}function Wp(e){return!sm||!e?!1:e===vo(e).scrollingElement}function gm(e){var t,r;const n=_t(e),o=Wp(e)?uS(e):_s(e),i=n.visualViewport,a=Wp(e)?{height:(t=i==null?void 0:i.height)!=null?t:n.innerHeight,width:(r=i==null?void 0:i.width)!=null?r:n.innerWidth}:{height:e.clientHeight,width:e.clientWidth},s={current:{x:e.scrollLeft,y:e.scrollTop},max:{x:e.scrollWidth-a.width,y:e.scrollHeight-a.height}},l=s.current.y<=0,c=s.current.x<=0,d=s.current.y>=s.max.y,u=s.current.x>=s.max.x;return{rect:o,position:s,isTop:l,isLeft:c,isBottom:d,isRight:u}}function IS(e,t){const{isTop:r,isBottom:n,isLeft:o,isRight:i,position:a}=gm(e),{x:s,y:l}=t??{x:0,y:0},c=!r&&a.current.y+l>0,d=!n&&a.current.y+l<a.max.y,u=!o&&a.current.x+s>0,p=!i&&a.current.x+s<a.max.x;return{top:c,bottom:d,left:u,right:p,x:u||p,y:c||d}}var Zu=class{constructor(t){this.scheduler=t,this.pending=!1,this.tasks=new Set,this.resolvers=new Set,this.flush=()=>{const{tasks:r,resolvers:n}=this;this.pending=!1,this.tasks=new Set,this.resolvers=new Set;for(const o of r)o();for(const o of n)o()}}schedule(t){return this.tasks.add(t),this.pending||(this.pending=!0,this.scheduler(this.flush)),new Promise(r=>this.resolvers.add(r))}},Wa=new Zu(e=>{typeof requestAnimationFrame=="function"?requestAnimationFrame(e):e()}),CS=new Zu(e=>setTimeout(e,50)),Ha=new Map,PS=Ha.clear.bind(Ha);function Lt(e,t=!1){if(!t)return Hp(e);let r=Ha.get(e);return r||(r=Hp(e),Ha.set(e,r),CS.schedule(PS),r)}function Hp(e){return _t(e).getComputedStyle(e)}function zS(e,t=Lt(e,!0)){return t.position==="fixed"||t.position==="sticky"}function AS(e,t=Lt(e,!0)){const r=/(auto|scroll|overlay)/;return["overflow","overflowX","overflowY"].some(o=>{const i=t[o];return typeof i=="string"?r.test(i):!1})}var jS={excludeElement:!0,escapeShadowDOM:!0};function ac(e,t=jS){const{limit:r,excludeElement:n,escapeShadowDOM:o}=t,i=new Set;function a(s){if(r!=null&&i.size>=r||!s)return i;if(Hu(s)&&s.scrollingElement!=null&&!i.has(s.scrollingElement))return i.add(s.scrollingElement),i;if(o&&qu(s))return a(s.host);if(!Rr(s))return am(s)?a(s.parentElement):i;if(i.has(s))return i;const l=Lt(s,!0);if(n&&s===e||AS(s,l)&&i.add(s),zS(s,l)){const{scrollingElement:c}=s.ownerDocument;return c&&i.add(c),i}return a(s.parentNode)}return e?a(e):i}function Gn(e,t=window.frameElement){const r={x:0,y:0,scaleX:1,scaleY:1};if(!e)return r;let n=Xn(e);for(;n;){if(n===t)return r;const o=_s(n),{x:i,y:a}=OS(n,o);r.x=r.x+o.left,r.y=r.y+o.top,r.scaleX=r.scaleX*i,r.scaleY=r.scaleY*a,n=Xn(n)}return r}function OS(e,t=_s(e)){const r=Math.round(t.width),n=Math.round(t.height);if(Rr(e))return{x:r/e.offsetWidth,y:n/e.offsetHeight};const o=Lt(e,!0);return{x:(parseFloat(o.width)||r)/r,y:(parseFloat(o.height)||n)/n}}function DS(e){if(e==="none")return null;const t=e.split(" "),r=parseFloat(t[0]),n=parseFloat(t[1]);return isNaN(r)&&isNaN(n)?null:{x:isNaN(r)?n:r,y:isNaN(n)?r:n}}function Jn(e){if(e==="none")return null;const[t,r,n="0"]=e.split(" "),o={x:parseFloat(t),y:parseFloat(r),z:parseInt(n,10)};return isNaN(o.x)&&isNaN(o.y)?null:{x:isNaN(o.x)?0:o.x,y:isNaN(o.y)?0:o.y,z:isNaN(o.z)?0:o.z}}function ys(e){var t,r,n,o,i,a,s,l,c;const{scale:d,transform:u,translate:p}=e,v=DS(d),h=Jn(p),m=TS(u);if(!m&&!v&&!h)return null;const y={x:(t=v==null?void 0:v.x)!=null?t:1,y:(r=v==null?void 0:v.y)!=null?r:1},b={x:(n=h==null?void 0:h.x)!=null?n:0,y:(o=h==null?void 0:h.y)!=null?o:0},k={x:(i=m==null?void 0:m.x)!=null?i:0,y:(a=m==null?void 0:m.y)!=null?a:0,scaleX:(s=m==null?void 0:m.scaleX)!=null?s:1,scaleY:(l=m==null?void 0:m.scaleY)!=null?l:1};return{x:b.x+k.x,y:b.y+k.y,z:(c=h==null?void 0:h.z)!=null?c:0,scaleX:y.x*k.scaleX,scaleY:y.y*k.scaleY}}function TS(e){if(e.startsWith("matrix3d(")){const t=e.slice(9,-1).split(/, /);return{x:+t[12],y:+t[13],scaleX:+t[0],scaleY:+t[5]}}else if(e.startsWith("matrix(")){const t=e.slice(7,-1).split(/, /);return{x:+t[4],y:+t[5],scaleX:+t[0],scaleY:+t[3]}}return null}var wt=(e=>(e[e.Idle=0]="Idle",e[e.Forward=1]="Forward",e[e.Reverse=-1]="Reverse",e))(wt||{}),MS={x:.2,y:.2},RS={x:10,y:10};function LS(e,t,r,n=25,o=MS,i=RS){const{x:a,y:s}=t,{rect:l,isTop:c,isBottom:d,isLeft:u,isRight:p}=gm(e),v=Gn(e),h=Lt(e,!0),m=ys(h),y=m!==null?(m==null?void 0:m.scaleX)<0:!1,b=m!==null?(m==null?void 0:m.scaleY)<0:!1,k=new It(l.left*v.scaleX+v.x,l.top*v.scaleY+v.y,l.width*v.scaleX,l.height*v.scaleY),x={x:0,y:0},_={x:0,y:0},I={height:k.height*o.y,width:k.width*o.x};return I.height>0&&(!c||b&&!d)&&s<=k.top+I.height&&(r==null?void 0:r.y)!==1&&a>=k.left-i.x&&a<=k.right+i.x?(x.y=b?1:-1,_.y=n*Math.abs((k.top+I.height-s)/I.height)):I.height>0&&(!d||b&&!c)&&s>=k.bottom-I.height&&(r==null?void 0:r.y)!==-1&&a>=k.left-i.x&&a<=k.right+i.x&&(x.y=b?-1:1,_.y=n*Math.abs((k.bottom-I.height-s)/I.height)),I.width>0&&(!p||y&&!u)&&a>=k.right-I.width&&(r==null?void 0:r.x)!==-1&&s>=k.top-i.y&&s<=k.bottom+i.y?(x.x=y?-1:1,_.x=n*Math.abs((k.right-I.width-a)/I.width)):I.width>0&&(!u||y&&!p)&&a<=k.left+I.width&&(r==null?void 0:r.x)!==1&&s>=k.top-i.y&&s<=k.bottom+i.y&&(x.x=y?1:-1,_.x=n*Math.abs((k.left+I.width-a)/I.width)),{direction:x,speed:_}}function mm(e,{block:t="nearest",inline:r="nearest"}={}){if(!Rr(e))return;const n=ac(e),o=[];for(const i of n){if(!Rr(i))continue;const{top:a,left:s}=FS(e,i);let l=a,c=s;for(const d of o)l-=d.scrollTop,c-=d.scrollLeft;if(t!=="none"){const d=l<i.scrollTop,u=l+e.offsetHeight>i.scrollTop+i.clientHeight;d!==u&&(t==="center"?i.scrollTop=l-i.clientHeight/2+e.offsetHeight/2:d?i.scrollTop=l:i.scrollTop=l+e.offsetHeight-i.clientHeight)}if(r!=="none"){const d=c<i.scrollLeft,u=c+e.offsetWidth>i.scrollLeft+i.clientWidth;d!==u&&(r==="center"?i.scrollLeft=c-i.clientWidth/2+e.offsetWidth/2:d?i.scrollLeft=c:i.scrollLeft=c+e.offsetWidth-i.clientWidth)}o.push(i)}}function Vp(e){let t=0,r=0,n=e;for(;n;){t+=n.offsetTop,r+=n.offsetLeft;const o=n.offsetParent;if(!Rr(o))break;t+=o.clientTop,r+=o.clientLeft,n=o}return{top:t,left:r}}function FS(e,t){const r=Vp(e),n=Vp(t);return{top:r.top-n.top-t.clientTop,left:r.left-n.left-t.clientLeft}}function NS(e,t,r){const{scaleX:n,scaleY:o,x:i,y:a}=t,s=e.left+i+(1-n)*parseFloat(r),l=e.top+a+(1-o)*parseFloat(r.slice(r.indexOf(" ")+1)),c=n?e.width*n:e.width,d=o?e.height*o:e.height;return{width:c,height:d,top:l,right:s+c,bottom:l+d,left:s}}function BS(e,t,r){const{scaleX:n,scaleY:o,x:i,y:a}=t,s=e.left-i-(1-n)*parseFloat(r),l=e.top-a-(1-o)*parseFloat(r.slice(r.indexOf(" ")+1)),c=n?e.width/n:e.width,d=o?e.height/o:e.height;return{width:c,height:d,top:l,right:s+c,bottom:l+d,left:s}}function _m({element:e,keyframes:t,options:r}){return e.animate(t,r).finished}function qp(e,t=Lt(e).translate,r=!0){if(r){const n=im(e,o=>"translate"in o);if(n){const{translate:o=""}=n[0];if(typeof o=="string"){const i=Jn(o);if(i)return i}}}if(t){const n=Jn(t);if(n)return n}return{x:0,y:0,z:0}}var $S=new Zu(e=>setTimeout(e,0)),Xo=new Map,WS=Xo.clear.bind(Xo);function HS(e){const t=e.ownerDocument;let r=Xo.get(t);if(r)return r;r=t.getAnimations(),Xo.set(t,r),$S.schedule(WS);const n=r.filter(o=>ms(o.effect)&&o.effect.target===e);return Xo.set(e,n),r}function VS(e,t){const r=HS(e).filter(n=>{var o,i;if(ms(n.effect)){const{target:a}=n.effect;if((i=a&&((o=t.isValidTarget)==null?void 0:o.call(t,a)))!=null?i:!0)return n.effect.getKeyframes().some(l=>{for(const c of t.properties)if(l[c])return!0})}}).map(n=>{const{effect:o,currentTime:i}=n,a=o==null?void 0:o.getComputedTiming().duration;if(!(n.pending||n.playState==="finished")&&typeof a=="number"&&typeof i=="number"&&i<a)return n.currentTime=a,()=>{n.currentTime=i}});if(r.length>0)return()=>r.forEach(n=>n==null?void 0:n())}var Et=class extends It{constructor(e,t={}){var r,n,o,i;const{frameTransform:a=Gn(e),ignoreTransforms:s,getBoundingClientRect:l=_s}=t,c=VS(e,{properties:["transform","translate","scale","width","height"],isValidTarget:I=>(I!==e||Vu())&&I.contains(e)}),d=l(e);let{top:u,left:p,width:v,height:h}=d,m;const y=Lt(e),b=ys(y),k={x:(r=b==null?void 0:b.scaleX)!=null?r:1,y:(n=b==null?void 0:b.scaleY)!=null?n:1},x=qS(e,y);c==null||c(),b&&(m=BS(d,b,y.transformOrigin),(s||x)&&(u=m.top,p=m.left,v=m.width,h=m.height));const _={width:(o=m==null?void 0:m.width)!=null?o:v,height:(i=m==null?void 0:m.height)!=null?i:h};if(x&&!s&&m){const I=NS(m,x,y.transformOrigin);u=I.top,p=I.left,v=I.width,h=I.height,k.x=x.scaleX,k.y=x.scaleY}a&&(s||(p*=a.scaleX,v*=a.scaleX,u*=a.scaleY,h*=a.scaleY),p+=a.x,u+=a.y),super(p,u,v,h),this.scale=k,this.intrinsicWidth=_.width,this.intrinsicHeight=_.height}};function qS(e,t){const r=e.getAnimations();if(!r.length)return null;let n,o,i,a=!1;for(const s of r){if(s.playState!=="running")continue;const l=ms(s.effect)?s.effect.getKeyframes():[],c=l[l.length-1];if(!c)continue;const{transform:d,translate:u,scale:p}=c;typeof d=="string"&&d&&(n=d,a=!0),typeof u=="string"&&u&&(o=u,a=!0),typeof p=="string"&&p&&(i=p,a=!0)}return a?ys({transform:n??t.transform,translate:o??t.translate,scale:i??t.scale}):null}function Go(e){return"style"in e&&typeof e.style=="object"&&e.style!==null&&"setProperty"in e.style&&"removeProperty"in e.style&&typeof e.style.setProperty=="function"&&typeof e.style.removeProperty=="function"}var US=class{constructor(e){this.element=e,this.initial=new Map}set(e,t=""){const{element:r}=this;if(Go(r))for(const[n,o]of Object.entries(e)){const i=`${t}${n}`;this.initial.has(i)||this.initial.set(i,r.style.getPropertyValue(i)),r.style.setProperty(i,typeof o=="string"?o:`${o}px`)}}remove(e,t=""){const{element:r}=this;if(Go(r))for(const n of e){const o=`${t}${n}`;r.style.removeProperty(o)}}reset(){const{element:e}=this;if(Go(e)){for(const[t,r]of this.initial)e.style.setProperty(t,r);e.getAttribute("style")===""&&e.removeAttribute("style")}}};function Lr(e){return e?e instanceof _t(e).Element||Ci(e)&&e.nodeType===Node.ELEMENT_NODE:!1}function fi(e){if(!e)return!1;const{KeyboardEvent:t}=_t(e.target);return e instanceof t}function ZS(e){if(!e)return!1;const{PointerEvent:t}=_t(e.target);return e instanceof t}function YS(e){if(!Lr(e))return!1;const{tagName:t}=e;return t==="INPUT"||t==="TEXTAREA"||KS(e)}function KS(e){return e.hasAttribute("contenteditable")&&e.getAttribute("contenteditable")!=="false"}var Gs={};function sc(e){const t=Gs[e]==null?0:Gs[e]+1;return Gs[e]=t,`${e}-${t}`}var XS=({dragOperation:e,droppable:t})=>{const r=e.position.current;if(!r)return null;const{id:n}=t;if(!t.shape)return null;if(t.shape.containsPoint(r)){const o=Qe.distance(t.shape.center,r);return{id:n,value:1/o,type:Jt.PointerIntersection,priority:kt.High}}return null},GS=({dragOperation:e,droppable:t})=>{const{shape:r}=e;if(!t.shape||!(r!=null&&r.current))return null;const n=r.current.intersectionArea(t.shape);if(n){const{position:o}=e,i=Qe.distance(t.shape.center,o.current),s=n/(r.current.area+t.shape.area-n)/i;return{id:t.id,value:s,type:Jt.ShapeIntersection,priority:kt.Normal}}return null},ym=e=>{var t;return(t=XS(e))!=null?t:GS(e)},JS=e=>{const{dragOperation:t,droppable:r}=e,{shape:n,position:o}=t;if(!r.shape)return null;const i=n?It.from(n.current.boundingRectangle).corners:void 0,s=It.from(r.shape.boundingRectangle).corners.reduce((l,c,d)=>{var u;return l+Qe.distance(Qe.from(c),(u=i==null?void 0:i[d])!=null?u:o.current)},0)/4;return{id:r.id,value:1/s,type:Jt.Collision,priority:kt.Normal}},QS=Object.create,Yu=Object.defineProperty,eE=Object.defineProperties,tE=Object.getOwnPropertyDescriptor,rE=Object.getOwnPropertyDescriptors,Va=Object.getOwnPropertySymbols,bm=Object.prototype.hasOwnProperty,xm=Object.prototype.propertyIsEnumerable,km=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),go=e=>{throw TypeError(e)},lc=(e,t,r)=>t in e?Yu(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,hi=(e,t)=>{for(var r in t||(t={}))bm.call(t,r)&&lc(e,r,t[r]);if(Va)for(var r of Va(t))xm.call(t,r)&&lc(e,r,t[r]);return e},Ku=(e,t)=>eE(e,rE(t)),Up=(e,t)=>Yu(e,"name",{value:t,configurable:!0}),wm=(e,t)=>{var r={};for(var n in e)bm.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&Va)for(var n of Va(e))t.indexOf(n)<0&&xm.call(e,n)&&(r[n]=e[n]);return r},mo=e=>{var t;return[,,,QS((t=e==null?void 0:e[km("metadata")])!=null?t:null)]},Sm=["class","method","getter","setter","accessor","field","value","get","set"],Bo=e=>e!==void 0&&typeof e!="function"?go("Function expected"):e,nE=(e,t,r,n,o)=>({kind:Sm[e],name:t,metadata:n,addInitializer:i=>r._?go("Already initialized"):o.push(Bo(i||null))}),gn=(e,t)=>lc(t,km("metadata"),e[3]),Ne=(e,t,r,n)=>{for(var o=0,i=e[t>>1],a=i&&i.length;o<a;o++)t&1?i[o].call(r):n=i[o].call(r,n);return n},Ct=(e,t,r,n,o,i)=>{var a,s,l,c,d,u=t&7,p=!!(t&8),v=!!(t&16),h=u>3?e.length+1:u?p?1:2:0,m=Sm[u+5],y=u>3&&(e[h-1]=[]),b=e[h]||(e[h]=[]),k=u&&(!v&&!p&&(o=o.prototype),u<5&&(u>3||!v)&&tE(u<4?o:{get[r](){return xe(this,i)},set[r](_){return it(this,i,_)}},r));u?v&&u<4&&Up(i,(u>2?"set ":u>1?"get ":"")+r):Up(o,r);for(var x=n.length-1;x>=0;x--)c=nE(u,r,l={},e[3],b),u&&(c.static=p,c.private=v,d=c.access={has:v?_=>oE(o,_):_=>r in _},u^3&&(d.get=v?_=>(u^1?xe:cn)(_,o,u^4?i:k.get):_=>_[r]),u>2&&(d.set=v?(_,I)=>it(_,o,I,u^4?i:k.set):(_,I)=>_[r]=I)),s=(0,n[x])(u?u<4?v?i:k[m]:u>4?void 0:{get:k.get,set:k.set}:o,c),l._=1,u^4||s===void 0?Bo(s)&&(u>4?y.unshift(s):u?v?i=s:k[m]=s:o=s):typeof s!="object"||s===null?go("Object expected"):(Bo(a=s.get)&&(k.get=a),Bo(a=s.set)&&(k.set=a),Bo(a=s.init)&&y.unshift(a));return u||gn(e,o),k&&Yu(o,r,k),v?u^4?i:k:o},Xu=(e,t,r)=>t.has(e)||go("Cannot "+r),oE=(e,t)=>Object(t)!==t?go('Cannot use the "in" operator on this value'):e.has(t),xe=(e,t,r)=>(Xu(e,t,"read from private field"),r?r.call(e):t.get(e)),Me=(e,t,r)=>t.has(e)?go("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),it=(e,t,r,n)=>(Xu(e,t,"write to private field"),n?n.call(e,r):t.set(e,r),r),cn=(e,t,r)=>(Xu(e,t,"access private method"),r),Zp={role:"button",roleDescription:"draggable"},iE="dnd-kit-description",aE="dnd-kit-announcement",sE={draggable:"To pick up a draggable item, press the space bar. While dragging, use the arrow keys to move the item in a given direction. Press space again to drop the item in its new position, or press escape to cancel."},lE={dragstart({operation:{source:e}}){if(e)return`Picked up draggable item ${e.id}.`},dragover({operation:{source:e,target:t}}){if(!(!e||e.id===(t==null?void 0:t.id)))return t?`Draggable item ${e.id} was moved over droppable target ${t.id}.`:`Draggable item ${e.id} is no longer over a droppable target.`},dragend({operation:{source:e,target:t},canceled:r}){if(e)return r?`Dragging was cancelled. Draggable item ${e.id} was dropped.`:t?`Draggable item ${e.id} was dropped over droppable target ${t.id}`:`Draggable item ${e.id} was dropped.`}};function cE(e){const t=e.tagName.toLowerCase();return["input","select","textarea","a","button"].includes(t)}function uE(e,t){const r=document.createElement("div");return r.id=e,r.style.setProperty("display","none"),r.textContent=t,r}function dE(e){const t=document.createElement("div");return t.id=e,t.setAttribute("role","status"),t.setAttribute("aria-live","polite"),t.setAttribute("aria-atomic","true"),t.style.setProperty("position","fixed"),t.style.setProperty("width","1px"),t.style.setProperty("height","1px"),t.style.setProperty("margin","-1px"),t.style.setProperty("border","0"),t.style.setProperty("padding","0"),t.style.setProperty("overflow","hidden"),t.style.setProperty("clip","rect(0 0 0 0)"),t.style.setProperty("clip-path","inset(100%)"),t.style.setProperty("white-space","nowrap"),t}var pE=["dragover","dragmove"],fE=class extends Xe{constructor(e,t){super(e);const{id:r,idPrefix:{description:n=iE,announcement:o=aE}={},announcements:i=lE,screenReaderInstructions:a=sE,debounce:s=500}=t??{},l=r?`${n}-${r}`:sc(n),c=r?`${o}-${r}`:sc(o);let d,u,p,v;const h=(I=v)=>{!p||!I||(p==null?void 0:p.nodeValue)!==I&&(p.nodeValue=I)},m=()=>Wa.schedule(h),y=hE(m,s),b=Object.entries(i).map(([I,w])=>this.manager.monitor.addEventListener(I,(A,E)=>{const C=p;if(!C)return;const S=w==null?void 0:w(A,E);S&&C.nodeValue!==S&&(v=S,pE.includes(I)?y():(m(),y.cancel()))})),k=()=>{let I=[];d!=null&&d.isConnected||(d=uE(l,a.draggable),I.push(d)),u!=null&&u.isConnected||(u=dE(c),p=document.createTextNode(""),u.appendChild(p),I.push(u)),I.length>0&&document.body.append(...I)},x=new Set;function _(){for(const I of x)I()}this.registerEffect(()=>{var I;x.clear();for(const w of this.manager.registry.draggables.value){const A=(I=w.handle)!=null?I:w.element;if(A){(!d||!u)&&x.add(k),(!cE(A)||Vu())&&!A.hasAttribute("tabindex")&&x.add(()=>A.setAttribute("tabindex","0")),!A.hasAttribute("role")&&A.tagName.toLowerCase()!=="button"&&x.add(()=>A.setAttribute("role",Zp.role)),A.hasAttribute("aria-roledescription")||x.add(()=>A.setAttribute("aria-roledescription",Zp.roleDescription)),A.hasAttribute("aria-describedby")||x.add(()=>A.setAttribute("aria-describedby",l));for(const C of["aria-pressed","aria-grabbed"]){const S=String(w.isDragging);A.getAttribute(C)!==S&&x.add(()=>A.setAttribute(C,S))}const E=String(w.disabled);A.getAttribute("aria-disabled")!==E&&x.add(()=>A.setAttribute("aria-disabled",E))}}x.size>0&&Wa.schedule(_)}),this.destroy=()=>{super.destroy(),d==null||d.remove(),u==null||u.remove(),b.forEach(I=>I())}}};function hE(e,t){let r;const n=()=>{clearTimeout(r),r=setTimeout(e,t)};return n.cancel=()=>clearTimeout(r),n}var qa=new Map,Em,Im,Cm,Pm,cc,Jo,lr,Gu,Qn,zm,Am,jm,Om,Fr=class extends(cc=Ii,Pm=[pe],Cm=[Te],Im=[Te],Em=[Te],cc){constructor(t,r){super(t,r),Ne(lr,5,this),Me(this,Qn),Me(this,Jo,new Set),Me(this,Gu,Ne(lr,8,this,new Set)),Ne(lr,11,this),this.registerEffect(cn(this,Qn,zm))}register(t){return xe(this,Jo).add(t),()=>{xe(this,Jo).delete(t)}}addRoot(t){return de(()=>{const r=new Set(this.additionalRoots);r.add(t),this.additionalRoots=r}),()=>{de(()=>{const r=new Set(this.additionalRoots);r.delete(t),this.additionalRoots=r})}}get sourceRoot(){var t;const{source:r}=this.manager.dragOperation;return Na((t=r==null?void 0:r.element)!=null?t:null)}get targetRoot(){var t;const{target:r}=this.manager.dragOperation;return Na((t=r==null?void 0:r.element)!=null?t:null)}get roots(){const{status:t}=this.manager.dragOperation;if(t.initializing||t.initialized){const r=[this.sourceRoot,this.targetRoot].filter(n=>n!=null);return new Set([...r,...this.additionalRoots])}return new Set}};lr=mo(cc);Jo=new WeakMap;Gu=new WeakMap;Qn=new WeakSet;zm=function(){const{roots:e}=this,t=[];for(const r of e)for(const n of xe(this,Jo))t.push(cn(this,Qn,Am).call(this,r,n));return()=>{for(const r of t)r()}};Am=function(e,t){let r=qa.get(e);r||(r=new Map,qa.set(e,r));let n=r.get(t);if(!n){const i=Hu(e)?cn(this,Qn,jm).call(this,e,r,t):cn(this,Qn,Om).call(this,e,r,t);if(!i)return()=>{};n=i,r.set(t,n)}n.refCount++;let o=!1;return()=>{o||(o=!0,n.refCount--,n.refCount===0&&n.cleanup())}};jm=function(e,t,r){var n;const o=e.createElement("style"),{nonce:i}=(n=this.options)!=null?n:{};i&&o.setAttribute("nonce",i),o.textContent=r,e.head.prepend(o);const a=new MutationObserver(s=>{for(const l of s)for(const c of Array.from(l.removedNodes))if(c===o){e.head.prepend(o);return}});return a.observe(e.head,{childList:!0}),{refCount:0,cleanup:()=>{a.disconnect(),o.remove(),t.delete(r),t.size===0&&qa.delete(e)}}};Om=function(e,t,r){"adoptedStyleSheets"in e&&Array.isArray(e.adoptedStyleSheets);const n=e.ownerDocument.defaultView,{CSSStyleSheet:o}=n??{};if(!o)return null;const i=new o;return i.replaceSync(r),e.adoptedStyleSheets.push(i),{refCount:0,cleanup:()=>{var a;if(qu(e)&&((a=e.host)!=null&&a.isConnected)){const s=e.adoptedStyleSheets.indexOf(i);s!==-1&&e.adoptedStyleSheets.splice(s,1)}t.delete(r),t.size===0&&qa.delete(e)}}};Ct(lr,4,"additionalRoots",Pm,Fr,Gu);Ct(lr,2,"sourceRoot",Cm,Fr);Ct(lr,2,"targetRoot",Im,Fr);Ct(lr,2,"roots",Em,Fr);gn(lr,Fr);Fr.configure=Ei(Fr);var bs=Fr,vE=class extends Xe{constructor(e,t){super(e,t),this.manager=e;const{cursor:r="grabbing"}=t??{},n=e.registry.plugins.get(bs),o=n==null?void 0:n.register(`* { cursor: ${r} !important; }`);if(o){const i=this.destroy.bind(this);this.destroy=()=>{o(),i()}}}},Pi="data-dnd-",uc=`${Pi}dropping`,Ze="--dnd-",Wt=`${Pi}dragging`,Ua=`${Pi}placeholder`,gE=[Wt,Ua,"popover","aria-pressed","aria-grabbing"],mE=["view-transition-name"],_E=`
  :is(:root,:host) [${Wt}] {
    position: fixed !important;
    pointer-events: none !important;
    touch-action: none;
    z-index: calc(infinity);
    will-change: translate;
    top: var(${Ze}top, 0px) !important;
    left: var(${Ze}left, 0px) !important;
    right: unset !important;
    bottom: unset !important;
    width: var(${Ze}width, auto);
    max-width: var(${Ze}width, auto);
    height: var(${Ze}height, auto);
    max-height: var(${Ze}height, auto);
    transform: var(${Ze}transform, none) !important;
    transition: var(${Ze}transition) !important;
  }

  :is(:root,:host) [${Ua}] {
    transition: none;
  }

  :is(:root,:host) [${Ua}='hidden'] {
    visibility: hidden;
  }

  [${Wt}] * {
    pointer-events: none !important;
  }

  [${Wt}]:not([${uc}]) {
    translate: var(${Ze}translate) !important;
  }

  [${Wt}][style*='${Ze}scale'] {
    scale: var(${Ze}scale) !important;
    transform-origin: var(${Ze}transform-origin) !important;
  }

  @layer dnd-kit {
    :where([${Wt}][popover]) {
      overflow: visible;
      background: unset;
      border: unset;
      margin: unset;
      padding: unset;
      color: inherit;

      &:is(input, button) {
        border: revert;
        background: revert;
      }
    }
  }
  [${Wt}]::backdrop, [${Pi}overlay]:not([${Wt}]) {
    display: none;
    visibility: hidden;
  }
`.replace(/\n+/g," ").replace(/\s+/g," ").trim();function yE(e,t="hidden"){return de(()=>{const{element:r,manager:n}=e;if(!r||!n)return;const o=bE(r,n.registry.droppables),i=[],a=fS(r),{remove:s}=a;return xE(o,a,i),kE(a,t),a.remove=()=>{i.forEach(l=>l()),s.call(a)},a})}function bE(e,t){const r=new Map;for(const n of t)if(n.element&&(e===n.element||e.contains(n.element))){const o=`${Pi}${sc("dom-id")}`;n.element.setAttribute(o,""),r.set(n,o)}return r}function xE(e,t,r){for(const[n,o]of e){if(!n.element)continue;const i=`[${o}]`,a=t.matches(i)?t:t.querySelector(i);if(n.element.removeAttribute(o),!a)continue;const s=n.element;n.proxy=a,a.removeAttribute(o),nc.set(s,a),r.push(()=>{nc.delete(s),n.proxy=void 0})}}function kE(e,t="hidden"){e.setAttribute("inert","true"),e.setAttribute("tab-index","-1"),e.setAttribute("aria-hidden","true"),e.setAttribute(Ua,t)}function Dm(e,t){return e===t?!0:Xn(e)===Xn(t)}function Yp(e){const{target:t}=e;"newState"in e&&e.newState==="closed"&&Lr(t)&&t.hasAttribute("popover")&&requestAnimationFrame(()=>Un(t))}function dc(e){return e.tagName==="TR"}function wE(e,t,r){const n=new MutationObserver(o=>{let i=!1;for(const a of o){if(a.target!==e){i=!0;continue}if(a.type!=="attributes")continue;const s=a.attributeName;if(s.startsWith("aria-")||gE.includes(s))continue;const l=e.getAttribute(s);if(s==="style"){if(Go(e)&&Go(t)){const c=e.style;for(const d of Array.from(t.style))c.getPropertyValue(d)===""&&t.style.removeProperty(d);for(const d of Array.from(c)){if(mE.includes(d)||d.startsWith(Ze))continue;const u=c.getPropertyValue(d);t.style.setProperty(d,u)}}}else l!==null?t.setAttribute(s,l):t.removeAttribute(s)}i&&r&&t.replaceChildren(...e.cloneNode(!0).childNodes)});return n.observe(e,{attributes:!0,subtree:!0,childList:!0}),n}function SE(e,t,r){const n=new MutationObserver(o=>{for(const i of o)if(i.addedNodes.length!==0)for(const a of Array.from(i.addedNodes)){if(a.contains(e)&&e.nextElementSibling!==t){e.insertAdjacentElement("afterend",t),Un(r);return}if(a.contains(t)&&t.previousElementSibling!==e){t.insertAdjacentElement("beforebegin",e),Un(r);return}}e.isConnected&&t.isConnected&&e.nextElementSibling!==t&&(e.insertAdjacentElement("afterend",t),Un(r))});return n.observe(e.ownerDocument.body,{childList:!0,subtree:!0}),n}function EE(e){return new ResizeObserver(()=>{var t,r,n;const o=new Et(e.placeholder,{frameTransform:e.frameTransform,ignoreTransforms:!0}),i=(t=e.transformOrigin)!=null?t:{x:1,y:1},a=(e.width-o.width)*i.x+e.delta.x,s=(e.height-o.height)*i.y+e.delta.y,l=lm();if(e.styles.set({width:o.width-e.widthOffset,height:o.height-e.heightOffset,top:e.top+s+l.y,left:e.left+a+l.x},Ze),(r=e.getElementMutationObserver())==null||r.takeRecords(),dc(e.element)&&dc(e.placeholder)){const m=Array.from(e.element.cells),y=Array.from(e.placeholder.cells);e.getSavedCellWidths()||e.setSavedCellWidths(m.map(b=>b.style.width));for(const[b,k]of m.entries()){const x=y[b];k.style.width=`${x.getBoundingClientRect().width}px`}}const c=(n=e.getTranslate())!=null?n:{x:0,y:0},d=e.left+a+l.x+c.x,u=e.top+s+l.y+c.y,p=o.width-e.widthOffset,v=o.height-e.heightOffset,h=e.frameTransform;e.dragOperation.shape=new It(d*h.scaleX+h.x,u*h.scaleY+h.y,p*h.scaleX,v*h.scaleY)})}var IE=250,CE="ease";function PE(e){var t,r,n,o;const{animation:i}=e;if(typeof i=="function"){const k=i({source:e.source,element:e.element,feedbackElement:e.feedbackElement,placeholder:e.placeholder,translate:e.translate,moved:e.moved});Promise.resolve(k).then(()=>{e.cleanup(),requestAnimationFrame(e.restoreFocus)});return}const{duration:a=IE,easing:s=CE}=i??{};Un(e.feedbackElement);const[,l]=(t=im(e.feedbackElement,k=>"translate"in k))!=null?t:[];l==null||l.pause();const c=(r=e.placeholder)!=null?r:e.element,d={frameTransform:Dm(e.feedbackElement,c)?null:void 0},u=new Et(e.feedbackElement,d),p=(n=Jn(Lt(e.feedbackElement).translate))!=null?n:e.translate,v=new Et(c,d),h=It.delta(u,v,e.alignment),m={x:p.x-h.x,y:p.y-h.y},y=Math.round(u.intrinsicHeight)!==Math.round(v.intrinsicHeight)?{minHeight:[`${u.intrinsicHeight}px`,`${v.intrinsicHeight}px`],maxHeight:[`${u.intrinsicHeight}px`,`${v.intrinsicHeight}px`]}:{},b=Math.round(u.intrinsicWidth)!==Math.round(v.intrinsicWidth)?{minWidth:[`${u.intrinsicWidth}px`,`${v.intrinsicWidth}px`],maxWidth:[`${u.intrinsicWidth}px`,`${v.intrinsicWidth}px`]}:{};e.styles.set({transition:e.transition},Ze),e.feedbackElement.setAttribute(uc,""),(o=e.getElementMutationObserver())==null||o.takeRecords(),_m({element:e.feedbackElement,keyframes:Ku(hi(hi({},y),b),{translate:[`${p.x}px ${p.y}px 0`,`${m.x}px ${m.y}px 0`]}),options:{duration:Uu(_t(e.feedbackElement))?0:e.moved||e.feedbackElement!==e.element?a:0,easing:s}}).then(()=>{e.feedbackElement.removeAttribute(uc),l==null||l.finish(),e.cleanup(),requestAnimationFrame(e.restoreFocus)})}var Tm,pc,vi,Ju,Ea,Mm,Rm,eo=class extends(pc=Xe,Tm=[pe],pc){constructor(t,r){super(t,r),Me(this,Ea),Me(this,Ju,Ne(vi,8,this)),Ne(vi,11,this),this.state={initial:{},current:{}};const n=t.registry.plugins.get(bs),o=n==null?void 0:n.register(_E);if(o){const i=this.destroy.bind(this);this.destroy=()=>{o(),i()}}this.registerEffect(cn(this,Ea,Mm).bind(this,n)),this.registerEffect(cn(this,Ea,Rm))}};vi=mo(pc);Ju=new WeakMap;Ea=new WeakSet;Mm=function(e){const{overlay:t}=this;if(!t||!e)return;const r=Na(t);if(r)return e.addRoot(r)};Rm=function(){var e,t,r,n,o,i,a;const{state:s,manager:l,options:c}=this,{dragOperation:d}=l,{position:u,source:p,status:v}=d;if(v.idle){s.current={},s.initial={};return}if(!p)return;const{element:h}=p,m=p.pluginConfig(eo),y=(t=(e=m==null?void 0:m.feedback)!=null?e:c==null?void 0:c.feedback)!=null?t:"default",b=typeof y=="function"?y(p,l):y;if(!h||b==="none"||!v.initialized||v.initializing)return;const{initial:k}=s,x=(r=this.overlay)!=null?r:h,_=Gn(x),I=Gn(h),w=!Dm(h,x),A=new Et(h,{frameTransform:w?I:null,ignoreTransforms:!w}),E={x:I.scaleX/_.scaleX,y:I.scaleY/_.scaleY};let{width:C,height:S,top:j,left:O}=A;w&&(C=C/E.x,S=S/E.y);const L=new US(x),$=Lt(h),{transition:F,translate:M,boxSizing:q,paddingBlockStart:W,paddingBlockEnd:B,paddingInlineStart:Z,paddingInlineEnd:oe,borderInlineStartWidth:K,borderInlineEndWidth:te,borderBlockStartWidth:be,borderBlockEndWidth:Q}=$,ie=F.split(",").filter(ge=>!/^\s*(transform|translate|scale)\b/.test(ge)).join(","),ke=ys($),Y=$.transform,P=b==="clone",T=q==="content-box",R=T?parseInt(Z)+parseInt(oe)+parseInt(K)+parseInt(te):0,U=T?parseInt(W)+parseInt(B)+parseInt(be)+parseInt(Q):0,V=b!=="move"&&!this.overlay?yE(p,P?"clone":"hidden"):null,G=de(()=>fi(l.dragOperation.activatorEvent));if(!k.translate){if(this.overlay&&ke)k.translate={x:ke.x,y:ke.y};else if(M!=="none"){const ge=Jn(M);ge&&(k.translate=ge)}}if(!k.transformOrigin){const ge=de(()=>u.current),Oe=O+((n=ke==null?void 0:ke.x)!=null?n:0),Ve=j+((o=ke==null?void 0:ke.y)!=null?o:0);k.transformOrigin={x:(ge.x-Oe*_.scaleX-_.x)/(C*_.scaleX),y:(ge.y-Ve*_.scaleY-_.y)/(S*_.scaleY)}}const{transformOrigin:ne}=k,ue=j*_.scaleY+_.y,ve=O*_.scaleX+_.x;if(!k.coordinates&&(k.coordinates={x:ve,y:ue},E.x!==1||E.y!==1)){const{scaleX:ge,scaleY:Oe}=I,{x:Ve,y:Ft}=ne;k.coordinates.x+=(C*ge-C)*Ve,k.coordinates.y+=(S*Oe-S)*Ft}k.dimensions||(k.dimensions={width:C,height:S}),k.frameTransform||(k.frameTransform=_);const $e={x:k.coordinates.x-ve,y:k.coordinates.y-ue},je={width:(k.dimensions.width*k.frameTransform.scaleX-C*_.scaleX)*ne.x,height:(k.dimensions.height*k.frameTransform.scaleY-S*_.scaleY)*ne.y},Ee={x:$e.x/_.scaleX+je.width,y:$e.y/_.scaleY+je.height},we={left:O+Ee.x,top:j+Ee.y};x.setAttribute(Wt,"true");const he=de(()=>d.transform),Pt=(i=k.translate)!=null?i:{x:0,y:0},Qt=he.x*_.scaleX+Pt.x,_n=he.y*_.scaleY+Pt.y,yn=lm();L.set({width:C-R,height:S-U,top:we.top+yn.y,left:we.left+yn.x,translate:`${Qt}px ${_n}px 0`,transform:this.overlay?"none":Y,transition:ie?`${ie}, translate 0ms linear`:"translate 0ms linear",scale:w?`${E.x} ${E.y}`:"","transform-origin":`${ne.x*100}% ${ne.y*100}%`},Ze),V&&(h.insertAdjacentElement("afterend",V),c!=null&&c.rootElement&&(typeof c.rootElement=="function"?c.rootElement(p):c.rootElement).appendChild(h)),ic(x)&&(x.hasAttribute("popover")||x.setAttribute("popover","manual"),Un(x),x.addEventListener("beforetoggle",Yp));let er,vr,gr;const ko=EE({placeholder:V,element:h,feedbackElement:x,frameTransform:_,transformOrigin:ne,width:C,height:S,top:j,left:O,widthOffset:R,heightOffset:U,delta:Ee,styles:L,dragOperation:d,getTranslate:()=>s.current.translate,getElementMutationObserver:()=>er,getSavedCellWidths:()=>gr,setSavedCellWidths:ge=>{gr=ge}}),js=new Et(x);de(()=>d.shape=js);const bn=_t(x),wo=ge=>{this.manager.actions.stop({event:ge})},Li=Uu(bn);G&&bn.addEventListener("resize",wo),de(()=>p.status)==="idle"&&requestAnimationFrame(()=>p.status="dragging"),V&&(ko.observe(V),er=wE(h,V,P),vr=SE(h,V,x));const So=(a=l.dragOperation.source)==null?void 0:a.id,Fi=()=>{var ge;if(!G||So==null)return;const Oe=l.registry.draggables.get(So),Ve=(ge=Oe==null?void 0:Oe.handle)!=null?ge:Oe==null?void 0:Oe.element;Rr(Ve)&&Ve.focus()},qr=()=>{var ge;if(er==null||er.disconnect(),vr==null||vr.disconnect(),ko.disconnect(),bn.removeEventListener("resize",wo),ic(x)&&(x.removeEventListener("beforetoggle",Yp),x.removeAttribute("popover")),x.removeAttribute(Wt),L.reset(),gr&&dc(h)){const Ft=Array.from(h.cells);for(const[X,ae]of Ft.entries())ae.style.width=(ge=gr[X])!=null?ge:""}p.status="idle";const Oe=s.current.translate!=null,Ve=d.status.dragging;V&&(!Ve&&Oe||V.parentElement!==x.parentElement)&&x.isConnected&&V.replaceWith(x),V==null||V.remove()},Ni=c==null?void 0:c.dropAnimation,Bi=this,Os=wi(()=>{var ge,Oe,Ve;const{transform:Ft,status:X}=d;if(!(!Ft.x&&!Ft.y&&!s.current.translate)&&X.dragging){const ae=(ge=k.translate)!=null?ge:{x:0,y:0},se={x:Ft.x/_.scaleX+ae.x,y:Ft.y/_.scaleY+ae.y},Ie=s.current.translate,qe=de(()=>d.modifiers),lt=de(()=>{var zt;return(zt=d.shape)==null?void 0:zt.current}),tt=c==null?void 0:c.keyboardTransition,mr=G&&!Li&&tt!==null?`${(Oe=tt==null?void 0:tt.duration)!=null?Oe:250}ms ${(Ve=tt==null?void 0:tt.easing)!=null?Ve:"cubic-bezier(0.25, 1, 0.5, 1)"}`:"0ms linear";if(L.set({transition:ie?`${ie}, translate ${mr}`:`translate ${mr}`,translate:`${se.x}px ${se.y}px 0`},Ze),er==null||er.takeRecords(),lt&&lt!==js&&Ie&&!qe.length){const zt=Qe.delta(se,Ie);d.shape=It.from(lt.boundingRectangle).translate(zt.x*_.scaleX,zt.y*_.scaleY)}else d.shape=new Et(x);s.current.translate=se}},function(){if(d.status.dropped){this.dispose(),p.status="dropping";const ge=(m==null?void 0:m.dropAnimation)!==void 0?m.dropAnimation:Bi.dropAnimation!==void 0?Bi.dropAnimation:Ni;let Oe=s.current.translate;const Ve=Oe!=null;if(!Oe&&h!==x&&(Oe={x:0,y:0}),!Oe||ge===null){qr();return}l.renderer.rendering.then(()=>{PE({source:p,element:h,feedbackElement:x,placeholder:V,translate:Oe,moved:Ve,transition:F,alignment:p.alignment,styles:L,animation:ge??void 0,getElementMutationObserver:()=>er,cleanup:qr,restoreFocus:Fi})})}});return()=>{qr(),Os()}};Ct(vi,4,"overlay",Tm,eo,Ju);gn(vi,eo);eo.configure=Ei(eo);var zi=eo,Io=!0,zE=!1,Lm,Fm,Nm,Bm,Ir,Qu,ed;Bm=(Nm=[pe],wt.Forward),Fm=(Lm=[pe],wt.Reverse);var gi=class{constructor(){Me(this,Qu,Ne(Ir,8,this,Io)),Ne(Ir,11,this),Me(this,ed,Ne(Ir,12,this,Io)),Ne(Ir,15,this)}isLocked(e){return e===wt.Idle?!1:e==null?this[wt.Forward]===Io&&this[wt.Reverse]===Io:this[e]===Io}unlock(e){e!==wt.Idle&&(this[e]=zE)}};Ir=mo(null);Qu=new WeakMap;ed=new WeakMap;Ct(Ir,4,Bm,Nm,gi,Qu);Ct(Ir,4,Fm,Lm,gi,ed);gn(Ir,gi);var AE=[wt.Forward,wt.Reverse],Kp=class{constructor(){this.x=new gi,this.y=new gi}isLocked(){return this.x.isLocked()&&this.y.isLocked()}},jE=class extends Xe{constructor(e){super(e);const t=lo(new Kp);let r=null;this.signal=t,pt(()=>{const{status:n}=e.dragOperation;if(!n.initialized){r=null,t.value=new Kp;return}const{delta:o}=e.dragOperation.position;if(r){const i={x:Xp(o.x,r.x),y:Xp(o.y,r.y)},a=t.peek();Ae(()=>{for(const s of vg)for(const l of AE)i[s]===l&&a[s].unlock(l);t.value=a})}r=o})}get current(){return this.signal.peek()}};function Xp(e,t){return Math.sign(e-t)}var $m,fc,mi,td,kr,hc,Ai=class extends(fc=Ii,$m=[pe],fc){constructor(e){super(e),Me(this,td,Ne(mi,8,this,!1)),Ne(mi,11,this),Me(this,kr),Me(this,hc,()=>{if(!xe(this,kr))return;const{element:i,by:a}=xe(this,kr);a.y&&(i.scrollTop+=a.y),a.x&&(i.scrollLeft+=a.x)}),this.scroll=(i,a)=>{var s;if(this.disabled)return!1;const l=this.getScrollableElements();if(!l)return it(this,kr,void 0),!1;const{position:c}=this.manager.dragOperation,d=c==null?void 0:c.current;if(d){const{by:u}=i??{},p=u?{x:Gp(u.x),y:Gp(u.y)}:void 0,v=p?void 0:this.scrollIntentTracker.current;if(v!=null&&v.isLocked())return!1;for(const h of l){const m=IS(h,u);if(m.x||m.y){const{speed:y,direction:b}=LS(h,d,p,a==null?void 0:a.acceleration,a==null?void 0:a.threshold);if(v)for(const k of vg)v[k].isLocked(b[k])&&(y[k]=0,b[k]=0);if(b.x||b.y){const{x:k,y:x}=u??b,_=k*y.x,I=x*y.y;if(_||I){const w=(s=xe(this,kr))==null?void 0:s.by;if(this.autoScrolling&&w&&(w.x&&!_||w.y&&!I))continue;return it(this,kr,{element:h,by:{x:_,y:I}}),Wa.schedule(xe(this,hc)),!0}}}}}return it(this,kr,void 0),!1};let t=null,r=null;const n=Hl(()=>{const{position:i,source:a}=e.dragOperation;if(!i)return null;const s=cm(Na(a==null?void 0:a.element),i.current);return s&&(t=s),s??t}),o=Hl(()=>{const i=n.value,{documentElement:a}=vo(i);if(!i||i===a){const{target:s}=e.dragOperation,l=s==null?void 0:s.element;if(l){const c=ac(l,{excludeElement:!1});return r=c,c}}if(i){const s=ac(i,{excludeElement:!1});return this.autoScrolling&&r&&s.size<(r==null?void 0:r.size)?r:(r=s,s)}return r=null,null},Ot);this.getScrollableElements=()=>o.value,this.scrollIntentTracker=new jE(e),this.destroy=e.monitor.addEventListener("dragmove",i=>{this.disabled||i.defaultPrevented||!fi(e.dragOperation.activatorEvent)||!i.by||this.scroll({by:i.by})&&i.preventDefault()})}};mi=mo(fc);td=new WeakMap;kr=new WeakMap;hc=new WeakMap;Ct(mi,4,"autoScrolling",$m,Ai,td);gn(mi,Ai);function Gp(e){return e>0?wt.Forward:e<0?wt.Reverse:wt.Idle}var OE=class{constructor(e){this.scheduler=e,this.pending=!1,this.tasks=new Set,this.resolvers=new Set,this.flush=()=>{const{tasks:t,resolvers:r}=this;this.pending=!1,this.tasks=new Set,this.resolvers=new Set;for(const n of t)n();for(const n of r)n()}}schedule(e){return this.tasks.add(e),this.pending||(this.pending=!0,this.scheduler(this.flush)),new Promise(t=>this.resolvers.add(t))}},DE=new OE(e=>{typeof requestAnimationFrame=="function"?requestAnimationFrame(e):e()}),TE=10,vc=class extends Xe{constructor(t,r){super(t,r);const n=t.registry.plugins.get(Ai);if(!n)throw new Error("AutoScroller plugin depends on Scroller plugin");this.destroy=pt(()=>{var o,i,a;if(this.disabled)return;const{position:s,status:l}=t.dragOperation;if(l.dragging){const c={acceleration:(o=this.options)==null?void 0:o.acceleration,threshold:typeof((i=this.options)==null?void 0:i.threshold)=="number"?{x:this.options.threshold,y:this.options.threshold}:(a=this.options)==null?void 0:a.threshold};if(n.scroll(void 0,c)){n.autoScrolling=!0;const u=setInterval(()=>DE.schedule(()=>n.scroll(void 0,c)),TE);return()=>{clearInterval(u)}}else n.autoScrolling=!1}})}};vc.configure=Ei(vc);var rd=vc,Jp={capture:!0,passive:!0},$o,ME=class extends Ii{constructor(e){super(e),Me(this,$o),this.handleScroll=()=>{xe(this,$o)==null&&it(this,$o,setTimeout(()=>{this.manager.collisionObserver.forceUpdate(!1),it(this,$o,void 0)},50))};const{dragOperation:t}=this.manager;this.destroy=pt(()=>{var r,n,o;if(t.status.dragging){const a=(o=(n=(r=t.source)==null?void 0:r.element)==null?void 0:n.ownerDocument)!=null?o:document;return a.addEventListener("scroll",this.handleScroll,Jp),()=>{a.removeEventListener("scroll",this.handleScroll,Jp)}}})}};$o=new WeakMap;var RE="* { user-select: none !important; -webkit-user-select: none !important; }",LE=class extends Xe{constructor(e){super(e),this.manager=e;const t=e.registry.plugins.get(bs),r=t==null?void 0:t.register(RE);if(this.destroy=pt(()=>{const{dragOperation:n}=this.manager;if(n.status.initialized)return Js(),document.addEventListener("selectionchange",Js,{capture:!0}),()=>{document.removeEventListener("selectionchange",Js,{capture:!0})}}),r){const n=this.destroy.bind(this);this.destroy=()=>{r(),n()}}}};function Js(){var e;(e=document.getSelection())==null||e.removeAllRanges()}var Wo=Object.freeze({offset:10,keyboardCodes:{start:["Space","Enter"],cancel:["Escape"],end:["Space","Enter","Tab"],up:["ArrowUp"],down:["ArrowDown"],left:["ArrowLeft"],right:["ArrowRight"]},preventActivation(e,t){var r;const n=(r=t.handle)!=null?r:t.element;return e.target!==n}}),Ln,Za=class extends Yn{constructor(t,r){super(t),this.manager=t,this.options=r,Me(this,Ln,[]),this.listeners=new um,this.handleSourceKeyDown=(n,o,i)=>{if(this.disabled||n.defaultPrevented||!Lr(n.target)||o.disabled)return;const{keyboardCodes:a=Wo.keyboardCodes,preventActivation:s=Wo.preventActivation}=i??{};a.start.includes(n.code)&&this.manager.dragOperation.status.idle&&(s!=null&&s(n,o)||this.handleStart(n,o,i))}}bind(t,r=this.options){return pt(()=>{var o;const i=(o=t.handle)!=null?o:t.element,a=s=>{fi(s)&&this.handleSourceKeyDown(s,t,r)};if(i)return i.addEventListener("keydown",a),()=>{i.removeEventListener("keydown",a)}})}handleStart(t,r,n){const{element:o}=r;if(!o)throw new Error("Source draggable does not have an associated element");t.preventDefault(),t.stopImmediatePropagation(),mm(o);const{center:i}=new Et(o);if(this.manager.actions.start({event:t,coordinates:{x:i.x,y:i.y},source:r}).signal.aborted)return this.cleanup();this.sideEffects();const s=vo(o),l=[this.listeners.bind(s,[{type:"keydown",listener:c=>this.handleKeyDown(c,r,n),options:{capture:!0}}])];xe(this,Ln).push(...l)}handleKeyDown(t,r,n){const{keyboardCodes:o=Wo.keyboardCodes}=n??{};if(In(t,[...o.end,...o.cancel])){t.preventDefault();const i=In(t,o.cancel);this.handleEnd(t,i);return}In(t,o.up)?this.handleMove("up",t):In(t,o.down)&&this.handleMove("down",t),In(t,o.left)?this.handleMove("left",t):In(t,o.right)&&this.handleMove("right",t)}handleEnd(t,r){this.manager.actions.stop({event:t,canceled:r}),this.cleanup()}handleMove(t,r){var n,o;const{shape:i}=this.manager.dragOperation,a=r.shiftKey?5:1;let s={x:0,y:0},l=(o=(n=this.options)==null?void 0:n.offset)!=null?o:Wo.offset;if(typeof l=="number"&&(l={x:l,y:l}),!!i){switch(t){case"up":s={x:0,y:-l.y*a};break;case"down":s={x:0,y:l.y*a};break;case"left":s={x:-l.x*a,y:0};break;case"right":s={x:l.x*a,y:0};break}(s.x||s.y)&&(r.preventDefault(),this.manager.actions.move({event:r,by:s}))}}sideEffects(){const t=this.manager.registry.plugins.get(rd);(t==null?void 0:t.disabled)===!1&&(t.disable(),xe(this,Ln).push(()=>{t.enable()}))}cleanup(){xe(this,Ln).forEach(t=>t()),it(this,Ln,[])}destroy(){this.cleanup(),this.listeners.clear()}};Ln=new WeakMap;Za.configure=Ei(Za);Za.defaults=Wo;var FE=Za;function In(e,t){return t.includes(e.code)}var Qr,NE=class extends Zg{constructor(){super(...arguments),Me(this,Qr)}onEvent(e){switch(e.type){case"pointerdown":it(this,Qr,Kn(e));break;case"pointermove":if(!xe(this,Qr))return;const{x:t,y:r}=Kn(e),n={x:t-xe(this,Qr).x,y:r-xe(this,Qr).y},{tolerance:o}=this.options;if(o&&Jl(n,o)){this.abort();return}Jl(n,this.options.value)&&this.activate(e);break;case"pointerup":this.abort();break}}abort(){it(this,Qr,void 0)}};Qr=new WeakMap;var Fn,en,BE=class extends Zg{constructor(){super(...arguments),Me(this,Fn),Me(this,en)}onEvent(e){switch(e.type){case"pointerdown":it(this,en,Kn(e)),it(this,Fn,setTimeout(()=>this.activate(e),this.options.value));break;case"pointermove":if(!xe(this,en))return;const{x:t,y:r}=Kn(e),n={x:t-xe(this,en).x,y:r-xe(this,en).y};Jl(n,this.options.tolerance)&&this.abort();break;case"pointerup":this.abort();break}}abort(){xe(this,Fn)&&(clearTimeout(xe(this,Fn)),it(this,en,void 0),it(this,Fn,void 0))}};Fn=new WeakMap;en=new WeakMap;var or=class{};or.Delay=BE;or.Distance=NE;var gc=Object.freeze({activationConstraints(e,t){var r;const{pointerType:n,target:o}=e;if(!(n==="mouse"&&Lr(o)&&(t.handle===o||(r=t.handle)!=null&&r.contains(o))))return n==="touch"?[new or.Delay({value:250,tolerance:5})]:YS(o)&&!e.defaultPrevented?[new or.Delay({value:200,tolerance:0})]:[new or.Delay({value:200,tolerance:10}),new or.Distance({value:5})]},preventActivation(e,t){var r;const{target:n}=e;return n===t.element||n===t.handle||!Lr(n)||(r=t.handle)!=null&&r.contains(n)?!1:vS(n)}}),Nn,Ya=class extends Yn{constructor(t,r){super(t),this.manager=t,this.options=r,Me(this,Nn,new Set),this.listeners=new um,this.latest={event:void 0,coordinates:void 0},this.handleMove=()=>{const{event:n,coordinates:o}=this.latest;!n||!o||this.manager.actions.move({event:n,to:o})},this.handleCancel=this.handleCancel.bind(this),this.handlePointerUp=this.handlePointerUp.bind(this),this.handleKeyDown=this.handleKeyDown.bind(this)}activationConstraints(t,r,n=this.options){const{activationConstraints:o=gc.activationConstraints}=n??{};return typeof o=="function"?o(t,r):o}bind(t,r=this.options){return pt(()=>{var o;const i=new AbortController,{signal:a}=i,s=c=>{ZS(c)&&this.handlePointerDown(c,t,r)};let l=[(o=t.handle)!=null?o:t.element];r!=null&&r.activatorElements&&(Array.isArray(r.activatorElements)?l=r.activatorElements:l=r.activatorElements(t));for(const c of l)c&&(HE(c.ownerDocument.defaultView),c.addEventListener("pointerdown",s,{signal:a}));return()=>i.abort()})}handlePointerDown(t,r,n){if(this.disabled||!t.isPrimary||t.button!==0||!Lr(t.target)||r.disabled||$E(t)||!this.manager.dragOperation.status.idle)return;const{preventActivation:o=gc.preventActivation}=n??{};if(o!=null&&o(t,r))return;const{target:i}=t,a=Rr(i)&&i.draggable&&i.getAttribute("draggable")==="true",s=Gn(r.element),{x:l,y:c}=Kn(t);this.initialCoordinates={x:l*s.scaleX+s.x,y:c*s.scaleY+s.y};const d=this.activationConstraints(t,r,n);t.sensor=this;const u=new aS(d,m=>this.handleStart(r,m));u.signal.onabort=()=>this.handleCancel(t),u.onEvent(t),this.controller=u;const p=rc(),v=this.listeners.bind(p,[{type:"pointermove",listener:m=>this.handlePointerMove(m,r)},{type:"pointerup",listener:this.handlePointerUp,options:{capture:!0}},{type:"pointercancel",listener:this.handleCancel},{type:"dragstart",listener:a?this.handleCancel:ea,options:{capture:!0}}]),h=()=>{v(),this.initialCoordinates=void 0};xe(this,Nn).add(h)}handlePointerMove(t,r){var n,o;if(((n=this.controller)==null?void 0:n.activated)===!1){(o=this.controller)==null||o.onEvent(t);return}if(this.manager.dragOperation.status.dragging){const i=Kn(t),a=Gn(r.element);i.x=i.x*a.scaleX+a.x,i.y=i.y*a.scaleY+a.y,t.preventDefault(),t.stopPropagation(),this.latest.event=t,this.latest.coordinates=i,Wa.schedule(this.handleMove)}}handlePointerUp(t){const{status:r}=this.manager.dragOperation;if(!r.idle){t.preventDefault(),t.stopPropagation();const n=!r.initialized;this.manager.actions.stop({event:t,canceled:n})}this.cleanup()}handleKeyDown(t){t.key==="Escape"&&(t.preventDefault(),this.handleCancel(t))}handleStart(t,r){const{manager:n,initialCoordinates:o}=this;if(!o||!n.dragOperation.status.idle||r.defaultPrevented)return;if(n.actions.start({coordinates:o,event:r,source:t}).signal.aborted)return this.cleanup();r.preventDefault();const s=vo(r.target).body;try{s.setPointerCapture(r.pointerId)}catch{this.handleCancel(r);return}const l=Lr(r.target)?[r.target,s]:s,c=this.listeners.bind(l,[{type:"touchmove",listener:ea,options:{passive:!1}},{type:"click",listener:ea},{type:"contextmenu",listener:ea},{type:"keydown",listener:this.handleKeyDown}]);xe(this,Nn).add(c)}handleCancel(t){const{dragOperation:r}=this.manager;r.status.initialized&&this.manager.actions.stop({event:t,canceled:!0}),this.cleanup()}cleanup(){const{controller:t}=this;this.controller=void 0,t&&!t.signal.aborted&&t.abort(),this.latest={event:void 0,coordinates:void 0},xe(this,Nn).forEach(r=>r()),xe(this,Nn).clear()}destroy(){this.cleanup(),this.listeners.clear()}};Nn=new WeakMap;Ya.configure=Ei(Ya);Ya.defaults=gc;var Wm=Ya;function $E(e){return"sensor"in e}function ea(e){e.preventDefault()}function WE(){}var Qp=new WeakSet;function HE(e){!e||Qp.has(e)||(e.addEventListener("touchmove",WE,{capture:!1,passive:!1}),Qp.add(e))}var Or={modifiers:[],plugins:[fE,rd,vE,zi,LE],sensors:[Wm,FE]},Hm=class extends cS{constructor(e={}){const t=Dt(e.plugins,Or.plugins),r=Dt(e.sensors,Or.sensors),n=Dt(e.modifiers,Or.modifiers);super(Ku(hi({},e),{plugins:[ME,Ai,bs,...t],sensors:r,modifiers:n}))}},Vm,qm,mc,Cr,nd,od,ji=class extends(mc=Xt,qm=[pe],Vm=[pe],mc){constructor(e,t){var r=e,{element:n,effects:o=()=>[],handle:i}=r,a=wm(r,["element","effects","handle"]);super(hi({effects:()=>[...o(),()=>{var s,l;const{manager:c}=this;if(!c)return;const u=((l=(s=this.sensors)==null?void 0:s.map(ui))!=null?l:[...c.sensors]).map(p=>{const v=p instanceof Yn?p:c.registry.register(p.plugin),h=p instanceof Yn?void 0:p.options;return v.bind(this,h)});return function(){u.forEach(v=>v())}}]},a),t),Me(this,nd,Ne(Cr,8,this)),Ne(Cr,11,this),Me(this,od,Ne(Cr,12,this)),Ne(Cr,15,this),this.element=n,this.handle=i}};Cr=mo(mc);nd=new WeakMap;od=new WeakMap;Ct(Cr,4,"handle",qm,ji,nd);Ct(Cr,4,"element",Vm,ji,od);gn(Cr,ji);var Um,Zm,_c,Pr,id,Qs,Ym,Km,Qo,ad,xs=class extends(_c=Gt,Zm=[pe],Um=[pe],_c){constructor(e,t){var r=e,{element:n,effects:o=()=>[]}=r,i=wm(r,["element","effects"]);const{collisionDetector:a=ym}=i,s=c=>{const{manager:d,element:u}=this;if(!u||c===null){this.shape=void 0;return}if(!d)return;const p=new Et(u),v=de(()=>this.shape);return p&&(v!=null&&v.equals(p))?v:(this.shape=p,p)},l=lo(!1);super(Ku(hi({},i),{collisionDetector:a,effects:()=>[...o(),()=>{const{element:c,manager:d}=this;if(!d)return;const{dragOperation:u}=d,{source:p}=u;l.value=!!(p&&u.status.initialized&&c&&!this.disabled&&this.accepts(p))},()=>{const{element:c}=this;if(l.value&&c){const d=new ES(c,s);return()=>{d.disconnect(),this.shape=void 0}}},()=>{var c;if((c=this.manager)!=null&&c.dragOperation.status.initialized)return()=>{this.shape=void 0}}]}),t),Me(this,Qo),Me(this,id,Ne(Pr,8,this)),Ne(Pr,11,this),Me(this,ad,Ne(Pr,12,this)),Ne(Pr,15,this),this.element=n,this.refreshShape=()=>s()}set element(e){it(this,Qo,e,Km)}get element(){var e;return(e=this.proxy)!=null?e:xe(this,Qo,Ym)}};Pr=mo(_c);id=new WeakMap;Qo=new WeakSet;ad=new WeakMap;Qs=Ct(Pr,20,"#element",Zm,Qo,id),Ym=Qs.get,Km=Qs.set;Ct(Pr,4,"proxy",Um,xs,ad);gn(Pr,xs);function VE(e){return e!=null&&typeof e=="object"&&"current"in e}function Dr(e){var t;if(e!=null)return VE(e)?(t=e.current)!=null?t:void 0:e}var qE=typeof window<"u"&&typeof window.document<"u"&&typeof window.document.createElement<"u",_o=qE?g.useLayoutEffect:g.useEffect;function UE(){const e=g.useState(0)[1];return g.useCallback(()=>{e(t=>t+1)},[e])}function sd(e,t){const r=g.useRef(new Map),n=UE();return _o(()=>{if(!e){r.current.clear();return}return pt(()=>{var o;let i=!1,a=!1;for(const s of r.current){const[l]=s,c=de(()=>s[1]),d=e[l];c!==d&&(i=!0,r.current.set(l,d),a=(o=t==null?void 0:t(l,c,d))!=null?o:!1)}i&&(a?queueMicrotask(()=>pr.flushSync(n)):n())})},[e]),g.useMemo(()=>e&&new Proxy(e,{get(o,i){const a=o[i];return r.current.set(i,a),a}}),[e])}function ZE(e,t){e()}function Cn(e){const t=g.useRef(e);return _o(()=>{t.current=e},[e]),t}function me(e,t,r=g.useEffect,n=Object.is){const o=g.useRef(e);r(()=>{const i=o.current;n(e,i)||(o.current=e,t(e,i))},[t,e])}function Zn(e,t){const r=g.useRef(Dr(e));_o(()=>{const n=Dr(e);n!==r.current&&(r.current=n,t(n))})}var YE=Object.defineProperty,KE=Object.defineProperties,XE=Object.getOwnPropertyDescriptors,Ka=Object.getOwnPropertySymbols,Xm=Object.prototype.hasOwnProperty,Gm=Object.prototype.propertyIsEnumerable,ef=(e,t,r)=>t in e?YE(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,Jm=(e,t)=>{for(var r in t||(t={}))Xm.call(t,r)&&ef(e,r,t[r]);if(Ka)for(var r of Ka(t))Gm.call(t,r)&&ef(e,r,t[r]);return e},Qm=(e,t)=>KE(e,XE(t)),GE=(e,t)=>{var r={};for(var n in e)Xm.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&Ka)for(var n of Ka(e))t.indexOf(n)<0&&Gm.call(e,n)&&(r[n]=e[n]);return r},JE=new Hm,e_=g.createContext(JE),QE=g.memo(g.forwardRef(({children:e},t)=>{const[r,n]=g.useState(0),o=g.useRef(null),i=g.useRef(null),a=g.useMemo(()=>({renderer:{get rendering(){var s;return(s=o.current)!=null?s:Promise.resolve()}},trackRendering(s){o.current||(o.current=new Promise(l=>{i.current=l})),g.startTransition(()=>{s(),n(l=>l+1)})}}),[]);return _o(()=>{var s;(s=i.current)==null||s.call(i),o.current=null},[e,r]),g.useImperativeHandle(t,()=>a),null})),el=[void 0,Ot];function ld(e){var t=e,{children:r,onCollision:n,onBeforeDragStart:o,onDragStart:i,onDragMove:a,onDragOver:s,onDragEnd:l}=t,c=GE(t,["children","onCollision","onBeforeDragStart","onDragStart","onDragMove","onDragOver","onDragEnd"]);const d=g.useRef(null),{plugins:u,modifiers:p,sensors:v}=c,h=Dt(u,Or.plugins),m=Dt(v,Or.sensors),y=Dt(p,Or.modifiers),b=Cn(o),k=Cn(i),x=Cn(s),_=Cn(a),I=Cn(l),w=Cn(n),A=eI(()=>{var E;return(E=c.manager)!=null?E:new Hm(c)});return g.useEffect(()=>{if(!d.current)throw new Error("Renderer not found");const{renderer:E,trackRendering:C}=d.current,{monitor:S}=A;A.renderer=E;const j=[S.addEventListener("beforedragstart",O=>{const L=b.current;L&&C(()=>L(O,A))}),S.addEventListener("dragstart",O=>{var L;return(L=k.current)==null?void 0:L.call(k,O,A)}),S.addEventListener("dragover",O=>{const L=x.current;L&&C(()=>L(O,A))}),S.addEventListener("dragmove",O=>{const L=_.current;L&&C(()=>L(O,A))}),S.addEventListener("dragend",O=>{const L=I.current;L&&C(()=>L(O,A))}),S.addEventListener("collision",O=>{var L;return(L=w.current)==null?void 0:L.call(w,O,A)})];return()=>j.forEach(O=>O())},[A]),me(h,()=>A&&(A.plugins=h),...el),me(m,()=>A&&(A.sensors=m),...el),me(y,()=>A&&(A.modifiers=y),...el),f.jsxs(e_.Provider,{value:A,children:[f.jsx(QE,{ref:d,children:r}),r]})}function eI(e){const t=g.useRef(null);return t.current||(t.current=e()),g.useInsertionEffect(()=>()=>{var r;return(r=t.current)==null?void 0:r.destroy()},[]),t.current}function t_(){return g.useContext(e_)}function cd(e){var t;const r=(t=t_())!=null?t:void 0,[n]=g.useState(()=>e(r));return n.manager!==r&&(n.manager=r),_o(n.register,[r,n]),n}function tI(e){const{disabled:t,data:r,element:n,handle:o,id:i,modifiers:a,sensors:s,plugins:l}=e,c=cd(u=>new ji(Qm(Jm({},e),{register:!1,handle:Dr(o),element:Dr(n)}),u)),d=sd(c,rI);return me(i,()=>c.id=i),Zn(o,u=>c.handle=u),Zn(n,u=>c.element=u),me(r,()=>r&&(c.data=r)),me(t,()=>c.disabled=t===!0),me(s,()=>c.sensors=s),me(a,()=>c.modifiers=a,void 0,Ot),me(l,()=>c.plugins=l,void 0,Ot),me(e.alignment,()=>c.alignment=e.alignment),{draggable:d,get isDragging(){return d.isDragging},get isDropping(){return d.isDropping},get isDragSource(){return d.isDragSource},handleRef:g.useCallback(u=>{c.handle=u??void 0},[c]),ref:g.useCallback(u=>{var p,v;!u&&((p=c.element)!=null&&p.isConnected)&&!((v=c.manager)!=null&&v.dragOperation.status.idle)||(c.element=u??void 0)},[c])}}function rI(e,t,r){return!!(e==="isDragSource"&&!r&&t)}var nI=Object.create,r_=Object.defineProperty,oI=Object.getOwnPropertyDescriptor,n_=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),ks=e=>{throw TypeError(e)},iI=(e,t,r)=>t in e?r_(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,aI=e=>{var t;return[,,,nI((t=e==null?void 0:e[n_("metadata")])!=null?t:null)]},o_=["class","method","getter","setter","accessor","field","value","get","set"],i_=e=>e!==void 0&&typeof e!="function"?ks("Function expected"):e,sI=(e,t,r,n,o)=>({kind:o_[e],name:t,metadata:n,addInitializer:i=>r._?ks("Already initialized"):o.push(i_(i||null))}),lI=(e,t)=>iI(t,n_("metadata"),e[3]),cI=(e,t,r,n)=>{for(var o=0,i=e[t>>1],a=i&&i.length;o<a;o++)i[o].call(r);return n},a_=(e,t,r,n,o,i)=>{for(var a,s,l,c,d=t&7,u=!1,p=!1,v=2,h=o_[d+5],m=e[v]||(e[v]=[]),y=(o=o.prototype,oI(o,r)),b=n.length-1;b>=0;b--)l=sI(d,r,s={},e[3],m),l.static=u,l.private=p,c=l.access={has:k=>r in k},c.get=k=>k[r],a=(0,n[b])(y[h],l),s._=1,i_(a)&&(y[h]=a);return y&&r_(o,r,y),o},s_=(e,t,r)=>t.has(e)||ks("Cannot "+r),uI=(e,t,r)=>(s_(e,t,"read from private field"),t.get(e)),dI=(e,t,r)=>t.has(e)?ks("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),pI=(e,t,r,n)=>(s_(e,t,"write to private field"),t.set(e,r),r),rn=class yc{constructor(t,r){this.x=t,this.y=r}static delta(t,r){return new yc(t.x-r.x,t.y-r.y)}static distance(t,r){return Math.hypot(t.x-r.x,t.y-r.y)}static equals(t,r){return t.x===r.x&&t.y===r.y}static from({x:t,y:r}){return new yc(t,r)}},l_,c_,bc,Ia,Oi,ud=class extends(bc=hn,c_=[Te],l_=[Te],bc){constructor(e){const t=rn.from(e);super(t,(r,n)=>rn.equals(r,n)),cI(Oi,5,this),dI(this,Ia,0),this.velocity={x:0,y:0}}get delta(){return rn.delta(this.current,this.initial)}get direction(){const{current:e,previous:t}=this;if(!t)return null;const r={x:e.x-t.x,y:e.y-t.y};return!r.x&&!r.y?null:Math.abs(r.x)>Math.abs(r.y)?r.x>0?"right":"left":r.y>0?"down":"up"}get current(){return super.current}set current(e){const{current:t}=this,r=rn.from(e),n={x:r.x-t.x,y:r.y-t.y},o=Date.now(),i=o-uI(this,Ia),a=s=>Math.round(s/i*100);Ae(()=>{pI(this,Ia,o),this.velocity={x:a(n.x),y:a(n.y)},super.current=r})}reset(e=this.defaultValue){super.reset(rn.from(e)),this.velocity={x:0,y:0}}};Oi=aI(bc);Ia=new WeakMap;a_(Oi,2,"delta",c_,ud);a_(Oi,2,"direction",l_,ud);lI(Oi,ud);var u_=(e=>(e.Horizontal="x",e.Vertical="y",e))(u_||{});Object.values(u_);var fI=({dragOperation:e,droppable:t})=>{const r=e.position.current;if(!r)return null;const{id:n}=t;if(!t.shape)return null;if(t.shape.containsPoint(r)){const o=rn.distance(t.shape.center,r);return{id:n,value:1/o,type:Jt.PointerIntersection,priority:kt.High}}return null},hI=({dragOperation:e,droppable:t})=>{const{shape:r}=e;if(!t.shape||!(r!=null&&r.current))return null;const n=r.current.intersectionArea(t.shape);if(n){const{position:o}=e,i=rn.distance(t.shape.center,o.current),s=n/(r.current.area+t.shape.area-n)/i;return{id:t.id,value:s,type:Jt.ShapeIntersection,priority:kt.Normal}}return null},vI=e=>{var t;return(t=fI(e))!=null?t:hI(e)};function dd(e){const{collisionDetector:t,data:r,disabled:n,element:o,id:i,accept:a,type:s}=e,l=cd(d=>new xs(Qm(Jm({},e),{register:!1,element:Dr(o)}),d)),c=sd(l);return me(i,()=>l.id=i),Zn(o,d=>l.element=d),me(a,()=>l.accept=a,void 0,Ot),me(t,()=>l.collisionDetector=t??vI),me(r,()=>r&&(l.data=r)),me(n,()=>l.disabled=n===!0),me(s,()=>l.type=s),{droppable:c,get isDropTarget(){return c.isDropTarget},ref:g.useCallback(d=>{var u,p;!d&&((u=l.element)!=null&&u.isConnected)&&!((p=l.manager)!=null&&p.dragOperation.status.idle)||(l.element=d??void 0)},[l])}}var gI=Object.create,d_=Object.defineProperty,mI=Object.defineProperties,_I=Object.getOwnPropertyDescriptor,yI=Object.getOwnPropertyDescriptors,Xa=Object.getOwnPropertySymbols,p_=Object.prototype.hasOwnProperty,f_=Object.prototype.propertyIsEnumerable,bI=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),Di=e=>{throw TypeError(e)},xc=(e,t,r)=>t in e?d_(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,tf=(e,t)=>{for(var r in t||(t={}))p_.call(t,r)&&xc(e,r,t[r]);if(Xa)for(var r of Xa(t))f_.call(t,r)&&xc(e,r,t[r]);return e},rf=(e,t)=>mI(e,yI(t)),xI=(e,t)=>{var r={};for(var n in e)p_.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&Xa)for(var n of Xa(e))t.indexOf(n)<0&&f_.call(e,n)&&(r[n]=e[n]);return r},kI=e=>{var t;return[,,,gI((t=void 0)!=null?t:null)]},h_=["class","method","getter","setter","accessor","field","value","get","set"],Ho=e=>e!==void 0&&typeof e!="function"?Di("Function expected"):e,wI=(e,t,r,n,o)=>({kind:h_[e],name:t,metadata:n,addInitializer:i=>r._?Di("Already initialized"):o.push(Ho(i||null))}),SI=(e,t)=>xc(t,bI("metadata"),e[3]),ta=(e,t,r,n)=>{for(var o=0,i=e[t>>1],a=i&&i.length;o<a;o++)t&1?i[o].call(r):n=i[o].call(r,n);return n},v_=(e,t,r,n,o,i)=>{for(var a,s,l,c,d,u=t&7,p=!1,v=!1,h=e.length+1,m=h_[u+5],y=e[h-1]=[],b=e[h]||(e[h]=[]),k=(o=o.prototype,_I({get[r](){return Vo(this,i)},set[r](_){return tn(this,i,_)}},r)),x=n.length-1;x>=0;x--)c=wI(u,r,l={},e[3],b),c.static=p,c.private=v,d=c.access={has:_=>r in _},d.get=_=>_[r],d.set=(_,I)=>_[r]=I,s=(0,n[x])({get:k.get,set:k.set},c),l._=1,s===void 0?Ho(s)&&(k[m]=s):typeof s!="object"||s===null?Di("Object expected"):(Ho(a=s.get)&&(k.get=a),Ho(a=s.set)&&(k.set=a),Ho(a=s.init)&&y.unshift(a));return k&&d_(o,r,k),o},g_=(e,t,r)=>t.has(e)||Di("Cannot "+r),Vo=(e,t,r)=>(g_(e,t,"read from private field"),t.get(e)),Co=(e,t,r)=>t.has(e)?Di("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,r),tn=(e,t,r,n)=>(g_(e,t,"write to private field"),t.set(e,r),r);function nn(e){return e instanceof hd||e instanceof b_}var ra=10,EI=class extends Xe{constructor(e){super(e);const t=pt(()=>{const{dragOperation:n}=e;if(fi(n.activatorEvent)&&nn(n.source)&&n.status.initialized){const o=e.registry.plugins.get(Ai);if(o)return o.disable(),()=>o.enable()}}),r=e.monitor.addEventListener("dragmove",(n,o)=>{queueMicrotask(()=>{if(this.disabled||n.defaultPrevented||!n.nativeEvent)return;const{dragOperation:i}=o;if(!fi(n.nativeEvent)||!nn(i.source)||!i.shape)return;const{actions:a,collisionObserver:s,registry:l}=o,{by:c}=n;if(!c)return;const d=II(c),{source:u,target:p}=i,{center:v}=i.shape.current,h=[],m=[];Ae(()=>{for(const I of l.droppables){const{id:w}=I;if(!I.accepts(u)||w===(p==null?void 0:p.id)&&nn(I)||!I.element)continue;let A=I.shape;const E=new Et(I.element,{getBoundingClientRect:C=>pi(C,void 0,.2)});!E.height||!E.width||(d=="down"&&v.y+ra<E.center.y||d=="up"&&v.y-ra>E.center.y||d=="left"&&v.x-ra>E.center.x||d=="right"&&v.x+ra<E.center.x)&&(h.push(I),I.shape=E,m.push(()=>I.shape=A))}}),n.preventDefault(),s.disable();const y=s.computeCollisions(h,JS);Ae(()=>m.forEach(I=>I()));const[b]=y;if(!b)return;const{id:k}=b,{index:x,group:_}=u.sortable;a.setDropTarget(k).then(()=>{const{source:I,target:w,shape:A}=i;if(!I||!nn(I)||!A)return;const{index:E,group:C,target:S}=I.sortable,j=x!==E||_!==C,O=j?S:w==null?void 0:w.element;if(!O)return;mm(O);const L=new Et(O);if(!L)return;const $=It.delta(L,It.from(A.current.boundingRectangle),I.alignment);a.move({by:$}),j?a.setDropTarget(I.id).then(()=>s.enable()):s.enable()})})});this.destroy=()=>{r(),t()}}};function II(e){const{x:t,y:r}=e;if(t>0)return"right";if(t<0)return"left";if(r>0)return"down";if(r<0)return"up"}var CI=Object.defineProperty,PI=Object.defineProperties,zI=Object.getOwnPropertyDescriptors,nf=Object.getOwnPropertySymbols,AI=Object.prototype.hasOwnProperty,jI=Object.prototype.propertyIsEnumerable,of=(e,t,r)=>t in e?CI(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,Pn=(e,t)=>{for(var r in t||(t={}))AI.call(t,r)&&of(e,r,t[r]);if(nf)for(var r of nf(t))jI.call(t,r)&&of(e,r,t[r]);return e},zn=(e,t)=>PI(e,zI(t));function OI(e,t,r){if(t===r)return e;const n=e.slice();return n.splice(r,0,n.splice(t,1)[0]),n}function tl(e){return"initialIndex"in e&&typeof e.initialIndex=="number"&&"index"in e&&typeof e.index=="number"}function DI(e,t,r){var n,o,i;const{source:a,target:s,canceled:l}=t.operation;if(!a||!s||l)return"preventDefault"in t&&t.preventDefault(),e;const c=(_,I)=>_===I||typeof _=="object"&&"id"in _&&_.id===I;if(Array.isArray(e)){const _=e.findIndex(w=>c(w,a.id)),I=e.findIndex(w=>c(w,s.id));if(_===-1||I===-1){if(tl(a)){const w=a.initialIndex,A=a.index;return w===A||w<0||w>=e.length?("preventDefault"in t&&t.preventDefault(),e):r(e,w,A)}return e}if(!l&&"index"in a&&typeof a.index=="number"){const w=a.index;if(w!==_)return r(e,_,w)}return r(e,_,I)}const d=Object.entries(e);let u=-1,p,v=-1,h;for(const[_,I]of d)if(u===-1&&(u=I.findIndex(w=>c(w,a.id)),u!==-1&&(p=_)),v===-1&&(v=I.findIndex(w=>c(w,s.id)),v!==-1&&(h=_)),u!==-1&&v!==-1)break;if(u===-1&&tl(a)){const _=a.initialGroup,I=a.initialIndex,w=a.group,A=a.index;if(_==null||w==null||!(_ in e)||!(w in e)||_===w&&I===A)return"preventDefault"in t&&t.preventDefault(),e;if(_===w)return zn(Pn({},e),{[_]:r(e[_],I,A)});const E=e[_][I];return zn(Pn({},e),{[_]:[...e[_].slice(0,I),...e[_].slice(I+1)],[w]:[...e[w].slice(0,A),E,...e[w].slice(A)]})}if(!a.manager)return e;const{dragOperation:m}=a.manager,y=(o=(n=m.shape)==null?void 0:n.current.center)!=null?o:m.position.current;if(h==null&&s.id in e){const _=s.shape&&y.y>s.shape.center.y?e[s.id].length:0;h=s.id,v=_}if(p==null||h==null||p===h&&u===v){if(p!=null&&p===h&&u===v&&tl(a)){const _=a.group!=null&&a.group!==p,I=a.index!==u;if(_||I){const w=(i=a.group)!=null?i:p;if(w in e){if(p===w)return zn(Pn({},e),{[p]:r(e[p],u,a.index)});const A=e[p][u];return zn(Pn({},e),{[p]:[...e[p].slice(0,u),...e[p].slice(u+1)],[w]:[...e[w].slice(0,a.index),A,...e[w].slice(a.index)]})}}}return"preventDefault"in t&&t.preventDefault(),e}if(p===h)return zn(Pn({},e),{[p]:r(e[p],u,v)});const k=s.shape&&Math.round(y.y)>Math.round(s.shape.center.y)?1:0,x=e[p][u];return zn(Pn({},e),{[p]:[...e[p].slice(0,u),...e[p].slice(u+1)],[h]:[...e[h].slice(0,v+k),x,...e[h].slice(v+k)]})}function TI(e,t){return DI(e,t,OI)}var af="__default__",MI=class extends Xe{constructor(e){super(e);const t=()=>{const n=new Map;for(const o of e.registry.droppables)if(o instanceof hd){const{sortable:i}=o,{group:a}=i;let s=n.get(a);s||(s=new Set,n.set(a,s)),s.add(i)}for(const[o,i]of n)n.set(o,new Set(na(i)));return n},r=[e.monitor.addEventListener("dragover",(n,o)=>{if(this.disabled)return;const{dragOperation:i}=o,{source:a,target:s}=i;if(!nn(a)||!nn(s)||a.sortable===s.sortable)return;const l=t(),c=a.sortable.group===s.sortable.group,d=l.get(a.sortable.group),u=c?d:l.get(s.sortable.group);!d||!u||queueMicrotask(()=>{n.defaultPrevented||o.renderer.rendering.then(()=>{var p,v,h;const m=t();for(const[S,j]of l.entries()){const O=Array.from(j).entries();for(const[L,$]of O)if($.index!==L||$.group!==S||!((p=m.get(S))!=null&&p.has($)))return}const y=a.sortable.element,b=s.sortable.element;if(!b||!y||!c&&s.id===a.sortable.group)return;const k=na(d),x=c?k:na(u),_=(v=a.sortable.group)!=null?v:af,I=(h=s.sortable.group)!=null?h:af,w={[_]:k,[I]:x},A=TI(w,n);if(w===A)return;const E=A[I].indexOf(a.sortable),C=A[I].indexOf(s.sortable);o.collisionObserver.disable(),sf(y,E,b,C),Ae(()=>{for(const[S,j]of A[_].entries())j.index=S;if(!c)for(const[S,j]of A[I].entries())j.group=s.sortable.group,j.index=S}),o.actions.setDropTarget(a.id).then(()=>o.collisionObserver.enable())})})}),e.monitor.addEventListener("dragend",(n,o)=>{if(!n.canceled)return;const{dragOperation:i}=o,{source:a}=i;nn(a)&&(a.sortable.initialIndex===a.sortable.index&&a.sortable.initialGroup===a.sortable.group||queueMicrotask(()=>{const s=t(),l=s.get(a.sortable.initialGroup);l&&o.renderer.rendering.then(()=>{for(const[v,h]of s.entries()){const m=Array.from(h).entries();for(const[y,b]of m)if(b.index!==y||b.group!==v)return}const c=na(l),d=a.sortable.element,u=c[a.sortable.initialIndex],p=u==null?void 0:u.element;!u||!p||!d||(sf(d,u.index,p,a.index),Ae(()=>{for(const[v,h]of s.entries()){const m=Array.from(h).values();for(const y of m)y.index=y.initialIndex,y.group=y.initialGroup}}))})}))})];this.destroy=()=>{for(const n of r)n()}}};function sf(e,t,r,n){const o=n<t?"afterend":"beforebegin";r.insertAdjacentElement(o,e)}function RI(e,t){return e.index-t.index}function na(e){return Array.from(e).sort(RI)}var lf=[EI,MI],m_={duration:250,easing:"cubic-bezier(0.25, 1, 0.5, 1)",idle:!1},oa=new T2,__,y_,zr,pd,qo,Uo,fd,Bn;y_=[pe],__=[pe];var ws=class{constructor(e,t){Co(this,pd,ta(zr,8,this)),ta(zr,11,this),Co(this,qo),Co(this,Uo),Co(this,fd,ta(zr,12,this)),ta(zr,15,this),Co(this,Bn),this.register=()=>(Ae(()=>{var p,v;(p=this.manager)==null||p.registry.register(this.droppable),(v=this.manager)==null||v.registry.register(this.draggable)}),()=>this.unregister()),this.unregister=()=>{Ae(()=>{var p,v;(p=this.manager)==null||p.registry.unregister(this.droppable),(v=this.manager)==null||v.registry.unregister(this.draggable)})},this.destroy=()=>{Ae(()=>{this.droppable.destroy(),this.draggable.destroy()})};var r=e,{effects:n=()=>[],group:o,index:i,sensors:a,type:s,transition:l=m_,plugins:c}=r,d=xI(r,["effects","group","index","sensors","type","transition","plugins"]);const u=Dt(c,lf);this.droppable=new hd(d,t,this),this.draggable=new b_(rf(tf({},d),{plugins:u,effects:()=>[()=>{var p,v,h;const m=(p=this.manager)==null?void 0:p.dragOperation.status;m!=null&&m.initializing&&this.id===((h=(v=this.manager)==null?void 0:v.dragOperation.source)==null?void 0:h.id)&&oa.clear(this.manager),m!=null&&m.dragging&&oa.set(this.manager,this.id,de(()=>({initialIndex:this.index,initialGroup:this.group})))},()=>{const{index:p,group:v,manager:h}=this,m=Vo(this,Uo),y=Vo(this,qo);(p!==m||v!==y)&&(tn(this,Uo,p),tn(this,qo,v),this.animate())},()=>{var p,v;const{target:h}=this,{isDragSource:m}=this.draggable;((v=(p=this.draggable.pluginConfig(zi))==null?void 0:p.feedback)!=null?v:"default")==="move"&&m&&(this.droppable.disabled=!h)},...n()],type:s,sensors:a}),t,this),tn(this,Bn,d.element),this.manager=t,this.index=i,tn(this,Uo,i),this.group=o,tn(this,qo,o),this.type=s,this.transition=l}get initialIndex(){var e,t;return(t=(e=oa.get(this.manager,this.id))==null?void 0:e.initialIndex)!=null?t:this.index}get initialGroup(){var e,t;return(t=(e=oa.get(this.manager,this.id))==null?void 0:e.initialGroup)!=null?t:this.group}animate(){de(()=>{const{manager:e,transition:t}=this,{shape:r}=this.droppable;if(!e)return;const{idle:n}=e.dragOperation.status;!r||!t||n&&!t.idle||e.renderer.rendering.then(()=>{const{element:o}=this;if(!o)return;for(const d of o.getAnimations())"transitionProperty"in d&&(d.transitionProperty==="transform"||d.transitionProperty==="translate"||d.transitionProperty==="scale")&&d.cancel();const i=this.refreshShape();if(!i)return;const a={x:r.boundingRectangle.left-i.boundingRectangle.left,y:r.boundingRectangle.top-i.boundingRectangle.top},{translate:s}=Lt(o),l=qp(o,s,!1),c=qp(o,s);if(a.x||a.y){const d=Uu(_t(o))?rf(tf({},t),{duration:0}):t;_m({element:o,keyframes:{translate:[`${l.x+a.x}px ${l.y+a.y}px ${l.z}`,`${c.x}px ${c.y}px ${c.z}`]},options:d}).then(()=>{e.dragOperation.status.dragging||(this.droppable.shape=void 0)})}})})}get manager(){return this.draggable.manager}set manager(e){Ae(()=>{this.draggable.manager=e,this.droppable.manager=e})}set element(e){Ae(()=>{const t=Vo(this,Bn),r=this.droppable.element,n=this.draggable.element;(!r||r===t)&&(this.droppable.element=e),(!n||n===t)&&(this.draggable.element=e),tn(this,Bn,e)})}get element(){var e,t;const r=Vo(this,Bn);if(r)return(t=(e=nc.get(r))!=null?e:r)!=null?t:this.droppable.element}set target(e){this.droppable.element=e}get target(){return this.droppable.element}set source(e){this.draggable.element=e}get source(){return this.draggable.element}get disabled(){return this.draggable.disabled&&this.droppable.disabled}set plugins(e){this.draggable.plugins=Dt(e,lf)}set disabled(e){Ae(()=>{this.droppable.disabled=e,this.draggable.disabled=e})}set data(e){Ae(()=>{this.droppable.data=e,this.draggable.data=e})}set handle(e){this.draggable.handle=e}set id(e){this.droppable.id=e,this.draggable.id=e}get id(){return this.droppable.id}set sensors(e){this.draggable.sensors=e}set modifiers(e){this.draggable.modifiers=e}set collisionPriority(e){this.droppable.collisionPriority=e}set collisionDetector(e){this.droppable.collisionDetector=e??ym}set alignment(e){this.draggable.alignment=e}get alignment(){return this.draggable.alignment}set type(e){Ae(()=>{this.droppable.type=e,this.draggable.type=e})}get type(){return this.draggable.type}set accept(e){this.droppable.accept=e}get accept(){return this.droppable.accept}get isDropTarget(){return this.droppable.isDropTarget}get isDragSource(){return this.draggable.isDragSource}get isDragging(){return this.draggable.isDragging}get isDropping(){return this.draggable.isDropping}get status(){return this.draggable.status}refreshShape(){return this.droppable.refreshShape()}accepts(e){return this.droppable.accepts(e)}};zr=kI();pd=new WeakMap;qo=new WeakMap;Uo=new WeakMap;fd=new WeakMap;Bn=new WeakMap;v_(zr,4,"index",y_,ws,pd);v_(zr,4,"group",__,ws,fd);SI(zr,ws);var b_=class extends ji{constructor(e,t,r){super(e,t),this.sortable=r}get index(){return this.sortable.index}get initialIndex(){return this.sortable.initialIndex}get group(){return this.sortable.group}get initialGroup(){return this.sortable.initialGroup}},hd=class extends xs{constructor(e,t,r){super(e,t),this.sortable=r}get index(){return this.sortable.index}get group(){return this.sortable.group}},LI=Object.defineProperty,FI=Object.defineProperties,NI=Object.getOwnPropertyDescriptors,cf=Object.getOwnPropertySymbols,BI=Object.prototype.hasOwnProperty,$I=Object.prototype.propertyIsEnumerable,uf=(e,t,r)=>t in e?LI(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,rl=(e,t)=>{for(var r in t||(t={}))BI.call(t,r)&&uf(e,r,t[r]);if(cf)for(var r of cf(t))$I.call(t,r)&&uf(e,r,t[r]);return e},WI=(e,t)=>FI(e,NI(t));function vd(e){const{accept:t,collisionDetector:r,collisionPriority:n,id:o,data:i,element:a,handle:s,index:l,group:c,disabled:d,modifiers:u,sensors:p,target:v,type:h,plugins:m}=e,y=rl(rl({},m_),e.transition),b=cd(x=>new ws(WI(rl({},e),{transition:y,register:!1,handle:Dr(s),element:Dr(a),target:Dr(v)}),x)),k=sd(b,HI);return me(o,()=>b.id=o),_o(()=>{Ae(()=>{b.group=c,b.index=l})},[b,c,l]),me(h,()=>b.type=h),me(t,()=>b.accept=t,void 0,Ot),me(i,()=>i&&(b.data=i)),me(l,()=>{var x;(x=b.manager)!=null&&x.dragOperation.status.idle&&(y!=null&&y.idle)&&b.refreshShape()},ZE),Zn(s,x=>b.handle=x),Zn(a,x=>b.element=x),Zn(v,x=>b.target=x),me(d,()=>b.disabled=d===!0),me(p,()=>b.sensors=p),me(r,()=>b.collisionDetector=r),me(n,()=>b.collisionPriority=n),me(m,()=>b.plugins=m,void 0,Ot),me(y,()=>b.transition=y,void 0,Ot),me(u,()=>b.modifiers=u,void 0,Ot),me(e.alignment,()=>b.alignment=e.alignment),{sortable:k,get isDragging(){return k.isDragging},get isDropping(){return k.isDropping},get isDragSource(){return k.isDragSource},get isDropTarget(){return k.isDropTarget},handleRef:g.useCallback(x=>{b.handle=x??void 0},[b]),ref:g.useCallback(x=>{var _,I;!x&&((_=b.element)!=null&&_.isConnected)&&!((I=b.manager)!=null&&I.dragOperation.status.idle)||(b.element=x??void 0)},[b]),sourceRef:g.useCallback(x=>{var _,I;!x&&((_=b.source)!=null&&_.isConnected)&&!((I=b.manager)!=null&&I.dragOperation.status.idle)||(b.source=x??void 0)},[b]),targetRef:g.useCallback(x=>{var _,I;!x&&((_=b.target)!=null&&_.isConnected)&&!((I=b.manager)!=null&&I.dragOperation.status.idle)||(b.target=x??void 0)},[b])}}function HI(e,t,r){return!!(e==="isDragSource"&&!r&&t)}function x_(e,t,r){var n=this,o=g.useRef(null),i=g.useRef(0),a=g.useRef(null),s=g.useRef([]),l=g.useRef(),c=g.useRef(),d=g.useRef(e),u=g.useRef(!0);g.useEffect(function(){d.current=e},[e]);var p=!t&&t!==0&&typeof window<"u";if(typeof e!="function")throw new TypeError("Expected a function");t=+t||0;var v=!!(r=r||{}).leading,h=!("trailing"in r)||!!r.trailing,m="maxWait"in r,y=m?Math.max(+r.maxWait||0,t):null;g.useEffect(function(){return u.current=!0,function(){u.current=!1}},[]);var b=g.useMemo(function(){var k=function(E){var C=s.current,S=l.current;return s.current=l.current=null,i.current=E,c.current=d.current.apply(S,C)},x=function(E,C){p&&cancelAnimationFrame(a.current),a.current=p?requestAnimationFrame(E):setTimeout(E,C)},_=function(E){if(!u.current)return!1;var C=E-o.current;return!o.current||C>=t||C<0||m&&E-i.current>=y},I=function(E){return a.current=null,h&&s.current?k(E):(s.current=l.current=null,c.current)},w=function E(){var C=Date.now();if(_(C))return I(C);if(u.current){var S=t-(C-o.current),j=m?Math.min(S,y-(C-i.current)):S;x(E,j)}},A=function(){var E=Date.now(),C=_(E);if(s.current=[].slice.call(arguments),l.current=n,o.current=E,C){if(!a.current&&u.current)return i.current=o.current,x(w,t),v?k(o.current):c.current;if(m)return x(w,t),k(o.current)}return a.current||x(w,t),c.current};return A.cancel=function(){a.current&&(p?cancelAnimationFrame(a.current):clearTimeout(a.current)),i.current=0,s.current=o.current=l.current=a.current=null},A.isPending=function(){return!!a.current},A.flush=function(){return a.current?I(Date.now()):c.current},A},[v,m,t,y,h,p]);return b}function VI(e,t){return e===t}function df(e){return typeof e=="function"?function(){return e}:e}function Lj(e,t,r){var n,o,i=r&&r.equalityFn||VI,a=(n=g.useState(df(e)),o=n[1],[n[0],g.useCallback(function(u){return o(df(u))},[])]),s=a[0],l=a[1],c=x_(g.useCallback(function(u){return l(u)},[l]),t,r),d=g.useRef(e);return i(d.current,e)||(c(e),d.current=e),[s,c]}function qI(e,t,r){const n=new Array(e);return new Proxy(n,{get(o,i,a){if(typeof i=="string"){const s=i.charCodeAt(0);if(s>=48&&s<=57){const l=+i;if(Number.isInteger(l)&&l>=0&&l<e){let c=o[l];if(!c){const d=t[l*2];c=o[l]={index:l,key:r(l),start:d,size:t[l*2+1],end:d+t[l*2+1],lane:0}}return c}}if(i==="length")return e}return Reflect.get(o,i,a)}})}function An(e,t,r){let n=r.initialDeps??[],o,i=!0;function a(){const s=e();return(s.length!==n.length||s.some((c,d)=>n[d]!==c))&&(n=s,o=t(...s),r!=null&&r.onChange&&!(i&&r.skipInitialOnChange)&&r.onChange(o),i=!1),o}return a.updateDeps=s=>{n=s},a}function pf(e,t){if(e===void 0)throw new Error("Unexpected undefined");return e}const UI=(e,t)=>Math.abs(e-t)<1.01,ZI=(e,t,r)=>{let n;return Object.assign(function(...o){e.clearTimeout(n),n=e.setTimeout(()=>t.apply(this,o),r)},{cancel:()=>{e.clearTimeout(n)}})};let Po;const nl=()=>{if(Po!==void 0)return Po;if(typeof navigator>"u")return Po=!1;if(/iP(hone|od|ad)/.test(navigator.userAgent))return Po=!0;const e=navigator.maxTouchPoints;return Po=navigator.platform==="MacIntel"&&e!==void 0&&e>0},ff=e=>{const{offsetWidth:t,offsetHeight:r}=e;return{width:t,height:r}},YI=e=>e,gd=e=>{const t=Math.max(e.startIndex-e.overscan,0),n=Math.min(e.endIndex+e.overscan,e.count-1)-t+1,o=new Array(n);for(let i=0;i<n;i++)o[i]=t+i;return o},k_=(e,t)=>{const r=e.scrollElement;if(!r)return;const n=e.targetWindow;if(!n)return;const o=a=>{const{width:s,height:l}=a;t({width:Math.round(s),height:Math.round(l)})};if(o(ff(r)),!n.ResizeObserver)return()=>{};const i=new n.ResizeObserver(a=>{const s=()=>{const l=a[0];if(l!=null&&l.borderBoxSize){const c=l.borderBoxSize[0];if(c){o({width:c.inlineSize,height:c.blockSize});return}}o(ff(r))};e.options.useAnimationFrameWithResizeObserver?requestAnimationFrame(s):s()});return i.observe(r,{box:"border-box"}),()=>{i.unobserve(r)}},_i={passive:!0},KI=(e,t)=>{const r=e.scrollElement;if(!r)return;const n=()=>{t({width:r.innerWidth,height:r.innerHeight})};return n(),r.addEventListener("resize",n,_i),()=>{r.removeEventListener("resize",n)}},XI=typeof window>"u"?!0:"onscrollend"in window,w_=(e,t,r)=>{const n=e.scrollElement;if(!n)return;const o=e.targetWindow;if(!o)return;const i=e.options.useScrollendEvent&&XI;let a=0;const s=i?null:ZI(o,()=>t(a,!1),e.options.isScrollingResetDelay),l=u=>()=>{a=r(n),s==null||s(),t(a,u)},c=l(!0),d=l(!1);return n.addEventListener("scroll",c,_i),i&&n.addEventListener("scrollend",d,_i),()=>{n.removeEventListener("scroll",c),i&&n.removeEventListener("scrollend",d),s==null||s.cancel()}},S_=(e,t)=>w_(e,t,r=>{const{horizontal:n,isRtl:o}=e.options;return n?r.scrollLeft*(o&&-1||1):r.scrollTop}),GI=(e,t)=>w_(e,t,r=>e.options.horizontal?r.scrollX:r.scrollY),JI=(e,t,r)=>{if(r.options.useCachedMeasurements){const n=r.indexFromElement(e),o=r.options.getItemKey(n);return r.itemSizeCache.get(o)??r.options.estimateSize(n)}if(t!=null&&t.borderBoxSize){const n=t.borderBoxSize[0];if(n)return Math.round(n[r.options.horizontal?"inlineSize":"blockSize"])}if(!t){const n=r.indexFromElement(e),o=r.options.getItemKey(n),i=r.itemSizeCache.get(o);if(i!==void 0)return i}return e[r.options.horizontal?"offsetWidth":"offsetHeight"]},E_=(e,{adjustments:t=0,behavior:r},n)=>{var o,i;(i=(o=n.scrollElement)==null?void 0:o.scrollTo)==null||i.call(o,{[n.options.horizontal?"left":"top"]:e+t,behavior:r})},QI=E_,I_=E_;class eC{constructor(t){this.unsubs=[],this.scrollElement=null,this.targetWindow=null,this.isScrolling=!1,this.scrollState=null,this.measurementsCache=[],this._flatMeasurements=null,this.itemSizeCache=new Map,this.itemSizeCacheVersion=0,this.laneAssignments=new Map,this.pendingMin=null,this.prevLanes=void 0,this.lanesChangedFlag=!1,this.lanesSettling=!1,this.pendingScrollAnchor=null,this.scrollRect=null,this.scrollOffset=null,this.scrollDirection=null,this.scrollAdjustments=0,this._iosDeferredAdjustment=0,this._iosTouching=!1,this._iosJustTouchEnded=!1,this._iosTouchEndTimerId=null,this._intendedScrollOffset=null,this.elementsCache=new Map,this.now=()=>{var r,n,o;return((o=(n=(r=this.targetWindow)==null?void 0:r.performance)==null?void 0:n.now)==null?void 0:o.call(n))??Date.now()},this.observer=(()=>{let r=null;const n=()=>r||(!this.targetWindow||!this.targetWindow.ResizeObserver?null:r=new this.targetWindow.ResizeObserver(o=>{o.forEach(i=>{const a=()=>{const s=i.target,l=this.indexFromElement(s);if(!s.isConnected){this.observer.unobserve(s);for(const[c,d]of this.elementsCache)if(d===s){this.elementsCache.delete(c);break}return}this.isIndexInRange(l)&&this.shouldMeasureDuringScroll(l)&&this.resizeItem(l,this.options.measureElement(s,i,this))};this.options.useAnimationFrameWithResizeObserver?requestAnimationFrame(a):a()})}));return{disconnect:()=>{var o;(o=n())==null||o.disconnect(),r=null},observe:o=>{var i;return(i=n())==null?void 0:i.observe(o,{box:"border-box"})},unobserve:o=>{var i;return(i=n())==null?void 0:i.unobserve(o)}}})(),this.range=null,this.setOptions=r=>{var n,o;const i={debug:!1,initialOffset:0,overscan:1,paddingStart:0,paddingEnd:0,scrollPaddingStart:0,scrollPaddingEnd:0,horizontal:!1,getItemKey:YI,rangeExtractor:gd,onChange:()=>{},measureElement:JI,initialRect:{width:0,height:0},scrollMargin:0,gap:0,indexAttribute:"data-index",initialMeasurementsCache:[],lanes:1,anchorTo:"start",followOnAppend:!1,scrollEndThreshold:1,isScrollingResetDelay:150,enabled:!0,isRtl:!1,useScrollendEvent:!1,useAnimationFrameWithResizeObserver:!1,laneAssignmentMode:"estimate",useCachedMeasurements:!1};for(const p in r){const v=r[p];v!==void 0&&(i[p]=v)}const a=this.options;let s=null,l=null,c=!1;if(a!==void 0&&a.enabled&&i.enabled&&i.anchorTo==="end"&&this.scrollElement!==null){const p=a.count,v=i.count,h=this.getMeasurements(),m=p>0?((n=h[0])==null?void 0:n.key)??a.getItemKey(0):null,y=p>0?((o=h[p-1])==null?void 0:o.key)??a.getItemKey(p-1):null;if(v!==p||p>0&&v>0&&(i.getItemKey(0)!==m||i.getItemKey(v-1)!==y)){c=!0;const x=p>0?this.getVirtualItemForOffset(this.getScrollOffset())??h[0]:null;x&&(s=[x.key,this.getScrollOffset()-x.start]);const _=i.followOnAppend===!0?"auto":i.followOnAppend||null;_&&v>p&&this.isAtEnd(a.scrollEndThreshold)&&(p===0||i.getItemKey(v-1)!==y)&&(l=_)}}this.options=i,c&&(this.pendingMin=0,this.itemSizeCacheVersion++);let d=!1,u=0;if(s&&this.scrollOffset!==null){const[p,v]=s,h=this.getMeasurements(),{count:m,getItemKey:y}=this.options;let b=0;for(;b<m&&y(b)!==p;)b++;if(b<m){const k=h[b];if(k){const x=Math.max(0,k.start+v);x!==this.scrollOffset&&(u=x-this.scrollOffset,this.scrollOffset=x,d=!0)}}}(d||l)&&(this.pendingScrollAnchor=[d?s[0]:null,d?s[1]:0,l,u])},this.notify=r=>{var n,o;(o=(n=this.options).onChange)==null||o.call(n,this,r)},this.maybeNotify=An(()=>(this.calculateRange(),[this.isScrolling,this.range?this.range.startIndex:null,this.range?this.range.endIndex:null]),r=>{this.notify(r)},{key:!1,debug:()=>this.options.debug,initialDeps:[this.isScrolling,this.range?this.range.startIndex:null,this.range?this.range.endIndex:null]}),this.cleanup=()=>{this.unsubs.filter(Boolean).forEach(r=>r()),this.unsubs=[],this.observer.disconnect(),this.rafId!=null&&this.targetWindow&&(this.targetWindow.cancelAnimationFrame(this.rafId),this.rafId=null),this.scrollState=null,this.isScrolling=!1,this.scrollDirection=null,this._iosDeferredAdjustment=0,this._iosTouching=!1,this._iosJustTouchEnded=!1,this.scrollElement=null,this.targetWindow=null},this._didMount=()=>()=>{this.cleanup()},this._willUpdate=()=>{var r;const n=this.options.enabled?this.options.getScrollElement():null;if(this.scrollElement!==n){if(this.cleanup(),!n){this.maybeNotify();return}if(this.scrollElement=n,this.scrollElement&&"ownerDocument"in this.scrollElement?this.targetWindow=this.scrollElement.ownerDocument.defaultView:this.targetWindow=((r=this.scrollElement)==null?void 0:r.window)??null,this.elementsCache.forEach(i=>{this.observer.observe(i)}),this.unsubs.push(this.options.observeElementRect(this,i=>{this.scrollRect=i,this.maybeNotify()})),this.unsubs.push(this.options.observeElementOffset(this,(i,a)=>{if(a&&this._intendedScrollOffset===null&&i===this.scrollOffset)return;this._intendedScrollOffset!==null&&Math.abs(i-this._intendedScrollOffset)<1.5&&(i=this._intendedScrollOffset),this._intendedScrollOffset=null,this.scrollAdjustments=0;const s=this.getScrollOffset();this.scrollDirection=a?s===i?this.scrollDirection:s<i?"forward":"backward":null,this.scrollOffset=i,this.isScrolling=a,this._flushIosDeferredIfReady(),this.scrollState&&this.scheduleScrollReconcile(),this.maybeNotify()})),"addEventListener"in this.scrollElement){const i=this.scrollElement,a=()=>{this._iosTouching=!0,this._iosJustTouchEnded=!1,this._iosTouchEndTimerId!==null&&this.targetWindow!=null&&(this.targetWindow.clearTimeout(this._iosTouchEndTimerId),this._iosTouchEndTimerId=null)},s=()=>{this._iosTouching=!1,!(!nl()||this.targetWindow==null)&&(this._iosJustTouchEnded=!0,this._iosTouchEndTimerId=this.targetWindow.setTimeout(()=>{this._iosJustTouchEnded=!1,this._iosTouchEndTimerId=null,this._flushIosDeferredIfReady()},150))};i.addEventListener("touchstart",a,_i),i.addEventListener("touchend",s,_i),this.unsubs.push(()=>{i.removeEventListener("touchstart",a),i.removeEventListener("touchend",s),this._iosTouchEndTimerId!==null&&this.targetWindow!=null&&(this.targetWindow.clearTimeout(this._iosTouchEndTimerId),this._iosTouchEndTimerId=null)})}this._scrollToOffset(this.getScrollOffset(),{adjustments:void 0,behavior:void 0})}const o=this.pendingScrollAnchor;if(this.pendingScrollAnchor=null,o&&this.scrollElement&&this.options.enabled){const[i,a,s,l]=o;i!==null&&!s&&(nl()&&(this.isScrolling||this._iosTouching||this._iosJustTouchEnded)?l!==0&&(this._iosDeferredAdjustment+=l):this._scrollToOffset(this.getScrollOffset(),{adjustments:void 0,behavior:void 0})),s&&this.scrollToEnd({behavior:s})}},this._flushIosDeferredIfReady=()=>{if(this._iosDeferredAdjustment===0||this.isScrolling||this._iosTouching||this._iosJustTouchEnded)return;const r=this.getScrollOffset(),n=this.getMaxScrollOffset();if(r<0||r>n)return;if(this._iosDeferredAdjustment<0&&r>=n-1){this._iosDeferredAdjustment=0;return}const o=this._iosDeferredAdjustment;this._iosDeferredAdjustment=0,this._scrollToOffset(r,{adjustments:this.scrollAdjustments+=o,behavior:void 0})},this.rafId=null,this.getSize=()=>this.options.enabled?(this.scrollRect=this.scrollRect??this.options.initialRect,this.scrollRect[this.options.horizontal?"width":"height"]):(this.scrollRect=null,0),this.getScrollOffset=()=>this.options.enabled?(this.scrollOffset=this.scrollOffset??(typeof this.options.initialOffset=="function"?this.options.initialOffset():this.options.initialOffset),this.scrollOffset):(this.scrollOffset=null,0),this.getMeasurementOptions=An(()=>[this.options.count,this.options.paddingStart,this.options.scrollMargin,this.options.getItemKey,this.options.enabled,this.options.lanes,this.options.laneAssignmentMode,this.options.gap],(r,n,o,i,a,s,l,c)=>(this.prevLanes!==void 0&&this.prevLanes!==s&&(this.lanesChangedFlag=!0),this.prevLanes=s,this.pendingMin=null,{count:r,paddingStart:n,scrollMargin:o,getItemKey:i,enabled:a,lanes:s,laneAssignmentMode:l,gap:c}),{key:!1}),this.isIndexInRange=r=>r>=0&&r<this.options.count,this.getMeasurements=An(()=>[this.getMeasurementOptions(),this.itemSizeCacheVersion],({count:r,paddingStart:n,scrollMargin:o,getItemKey:i,enabled:a,lanes:s,laneAssignmentMode:l,gap:c},d)=>{const u=this.itemSizeCache;if(!a)return this.measurementsCache=[],this.itemSizeCache.clear(),this.laneAssignments.clear(),[];if(this.laneAssignments.size>r)for(const b of this.laneAssignments.keys())b>=r&&this.laneAssignments.delete(b);this.lanesChangedFlag&&(this.lanesChangedFlag=!1,this.lanesSettling=!0,this.measurementsCache=[],this.itemSizeCache.clear(),this.laneAssignments.clear(),this.pendingMin=null),this.measurementsCache.length===0&&!this.lanesSettling&&(this.measurementsCache=this.options.initialMeasurementsCache,this.measurementsCache.forEach(b=>{this.itemSizeCache.set(b.key,b.size)}));const p=this.lanesSettling?0:this.pendingMin??0;if(this.pendingMin=null,this.lanesSettling&&this.measurementsCache.length===r&&(this.lanesSettling=!1),s===1){const b=r*2;let k=this._flatMeasurements;if(!k||k.length<b){const I=new Float64Array(b);k&&p>0&&I.set(k.subarray(0,p*2)),k=I,this._flatMeasurements=k}let x;if(p===0)x=n+o;else{const I=p-1;x=k[I*2]+k[I*2+1]+c}for(let I=p;I<r;I++){const w=i(I),A=u.get(w),E=typeof A=="number"?A:this.options.estimateSize(I);k[I*2]=x,k[I*2+1]=E,x+=E+c}const _=qI(r,k,i);return this.measurementsCache=_,_}const v=this.measurementsCache.slice(0,p),h=new Array(s).fill(void 0),m=new Float64Array(s);let y=0;for(let b=0;b<p;b++){const k=v[b];k&&(h[k.lane]===void 0&&y++,h[k.lane]=b,m[k.lane]=k.end)}for(let b=p;b<r;b++){const k=i(b),x=this.laneAssignments.get(b);let _,I;const w=l==="estimate"||u.has(k);if(x!==void 0&&this.options.lanes>1){_=x;const S=h[_],j=S!==void 0?v[S]:void 0;I=j?j.end+c:n+o}else if(y===s){let S=0,j=m[0],O=h[0];for(let L=1;L<s;L++){const $=m[L];($<j||$===j&&h[L]<O)&&(S=L,j=$,O=h[L])}_=S,I=j+c,w&&this.laneAssignments.set(b,_)}else _=b%this.options.lanes,I=n+o,w&&this.laneAssignments.set(b,_);const A=u.get(k),E=typeof A=="number"?A:this.options.estimateSize(b),C=I+E;v[b]={index:b,start:I,size:E,end:C,key:k,lane:_},h[_]===void 0&&y++,h[_]=b,m[_]=C}return this.measurementsCache=v,v},{key:!1,debug:()=>this.options.debug}),this.calculateRange=An(()=>[this.getMeasurements(),this.getSize(),this.getScrollOffset(),this.options.lanes],(r,n,o,i)=>r.length===0||n===0?(this.range=null,null):(this.range=rC(r,n,o,i,i===1&&this._flatMeasurements!=null?this._flatMeasurements:null),this.range),{key:!1,debug:()=>this.options.debug}),this.getVirtualIndexes=An(()=>{let r=null,n=null;const o=this.calculateRange();return o&&(r=o.startIndex,n=o.endIndex),this.maybeNotify.updateDeps([this.isScrolling,r,n]),[this.options.rangeExtractor,this.options.overscan,this.options.count,r,n]},(r,n,o,i,a)=>i===null||a===null?[]:r({startIndex:i,endIndex:a,overscan:n,count:o}),{key:!1,debug:()=>this.options.debug}),this.indexFromElement=r=>{const n=this.options.indexAttribute,o=r.getAttribute(n);return o?parseInt(o,10):(console.warn(`Missing attribute name '${n}={index}' on measured element.`),-1)},this.shouldMeasureDuringScroll=r=>{var n;if(!this.scrollState||this.scrollState.behavior!=="smooth")return!0;const o=this.scrollState.index??((n=this.getVirtualItemForOffset(this.scrollState.lastTargetOffset))==null?void 0:n.index);if(o!==void 0&&this.range){const i=Math.max(this.options.overscan,Math.ceil((this.range.endIndex-this.range.startIndex)/2)),a=Math.max(0,o-i),s=Math.min(this.options.count-1,o+i);return r>=a&&r<=s}return!0},this.measureElement=r=>{if(!r){this.elementsCache.forEach((a,s)=>{a.isConnected||(this.observer.unobserve(a),this.elementsCache.delete(s))});return}const n=this.indexFromElement(r);if(!this.isIndexInRange(n))return;const o=this.options.getItemKey(n),i=this.elementsCache.get(o);i!==r&&(i&&this.observer.unobserve(i),this.observer.observe(r),this.elementsCache.set(o,r)),(!this.isScrolling||this.scrollState)&&this.shouldMeasureDuringScroll(n)&&this.resizeItem(n,this.options.measureElement(r,void 0,this))},this.resizeItem=(r,n)=>{var o,i;if(!this.isIndexInRange(r))return;let a,s,l;const c=this._flatMeasurements;if(this.options.lanes===1&&c!==null)l=this.options.getItemKey(r),s=c[r*2],a=c[r*2+1];else{const p=this.measurementsCache[r];if(!p)return;l=p.key,s=p.start,a=p.size}const d=this.itemSizeCache.get(l)??a,u=n-d;if(u!==0){const p=this.options.anchorTo==="end"&&((o=this.scrollState)==null?void 0:o.behavior)!=="smooth"&&this.getVirtualDistanceFromEnd()<=this.options.scrollEndThreshold,v=p?this.getTotalSize():0,h=this.getScrollOffset()+this.scrollAdjustments,y=!this.itemSizeCache.has(l)?s<h:s+d<=h&&this.scrollDirection!=="backward",b=((i=this.scrollState)==null?void 0:i.behavior)!=="smooth"&&(this.shouldAdjustScrollPositionOnItemSizeChange!==void 0?this.shouldAdjustScrollPositionOnItemSizeChange(this.measurementsCache[r]??{index:r,key:l,start:s,size:a,end:s+a,lane:0},u,this):y);(this.pendingMin===null||r<this.pendingMin)&&(this.pendingMin=r),this.itemSizeCache.set(l,n),this.itemSizeCacheVersion++;let k=!1;p?k=this.applyScrollAdjustment(this.getTotalSize()-v):b&&(k=this.applyScrollAdjustment(u)),this.notify(k)}},this.getVirtualItems=An(()=>[this.getVirtualIndexes(),this.getMeasurements()],(r,n)=>{const o=[];for(let i=0,a=r.length;i<a;i++){const s=r[i],l=n[s];o.push(l)}return o},{key:!1,debug:()=>this.options.debug}),this.getVirtualItemForOffset=r=>{const n=this.getMeasurements();if(n.length===0)return;const o=this._flatMeasurements,i=this.options.lanes===1&&o!=null,a=C_(0,n.length-1,i?s=>o[s*2]:s=>pf(n[s]).start,r);return pf(n[a])},this.getMaxScrollOffset=()=>{if(!this.scrollElement)return 0;if("scrollHeight"in this.scrollElement)return this.options.horizontal?this.scrollElement.scrollWidth-this.scrollElement.clientWidth:this.scrollElement.scrollHeight-this.scrollElement.clientHeight;{const r=this.scrollElement.document.documentElement;return this.options.horizontal?r.scrollWidth-this.scrollElement.innerWidth:r.scrollHeight-this.scrollElement.innerHeight}},this.getVirtualDistanceFromEnd=()=>Math.max(this.getTotalSize()-this.getSize()-this.getScrollOffset(),0),this.getDistanceFromEnd=()=>Math.max(this.getMaxScrollOffset()-this.getScrollOffset(),0),this.isAtEnd=(r=this.options.scrollEndThreshold)=>this.getDistanceFromEnd()<=r,this.getOffsetForAlignment=(r,n,o=0)=>{if(!this.scrollElement)return 0;const i=this.getSize(),a=this.getScrollOffset();n==="auto"&&(n=r>=a+i?"end":"start"),n==="center"?r+=(o-i)/2:n==="end"&&(r-=i);const s=this.getMaxScrollOffset();return Math.max(Math.min(s,r),0)},this.getOffsetForIndex=(r,n="auto")=>{r=Math.max(0,Math.min(r,this.options.count-1));const o=this.getSize(),i=this.getScrollOffset(),a=this.measurementsCache[r];if(!a)return;if(n==="auto")if(a.end>=i+o-this.options.scrollPaddingEnd)n="end";else if(a.start<=i+this.options.scrollPaddingStart)n="start";else return[i,n];if(n==="end"&&r===this.options.count-1)return[this.getMaxScrollOffset(),n];const s=n==="end"?a.end+this.options.scrollPaddingEnd:a.start-this.options.scrollPaddingStart;return[this.getOffsetForAlignment(s,n,a.size),n]},this.scrollToOffset=(r,{align:n="start",behavior:o="auto"}={})=>{this._iosDeferredAdjustment=0;const i=this.getOffsetForAlignment(r,n),a=this.now();this.scrollState={index:null,align:n,behavior:o,startedAt:a,lastTargetOffset:i,stableFrames:0},this._scrollToOffset(i,{adjustments:void 0,behavior:o}),this.scheduleScrollReconcile()},this.scrollToIndex=(r,{align:n="auto",behavior:o="auto"}={})=>{this._iosDeferredAdjustment=0,r=Math.max(0,Math.min(r,this.options.count-1));const i=this.getOffsetForIndex(r,n);if(!i)return;const[a,s]=i,l=this.now();this.scrollState={index:r,align:s,behavior:o,startedAt:l,lastTargetOffset:a,stableFrames:0},this._scrollToOffset(a,{adjustments:void 0,behavior:o}),this.scheduleScrollReconcile()},this.scrollBy=(r,{behavior:n="auto"}={})=>{const o=this.getScrollOffset()+r,i=this.now();this.scrollState={index:null,align:"start",behavior:n,startedAt:i,lastTargetOffset:o,stableFrames:0},this._scrollToOffset(o,{adjustments:void 0,behavior:n}),this.scheduleScrollReconcile()},this.scrollToEnd=({behavior:r="auto"}={})=>{if(this.options.count>0){this.scrollToIndex(this.options.count-1,{align:"end",behavior:r});return}this.scrollToOffset(Math.max(this.getTotalSize()-this.getSize(),0),{behavior:r})},this.getTotalSize=()=>{var r;const n=this.getMeasurements();let o;if(n.length===0)o=this.options.paddingStart;else if(this.options.lanes===1){const i=n.length-1,a=this._flatMeasurements;a!=null?o=a[i*2]+a[i*2+1]:o=((r=n[i])==null?void 0:r.end)??0}else{const i=Array(this.options.lanes).fill(null);let a=n.length-1;for(;a>=0&&i.some(s=>s===null);){const s=n[a];i[s.lane]===null&&(i[s.lane]=s.end),a--}o=Math.max(...i.filter(s=>s!==null))}return Math.max(o-this.options.scrollMargin+this.options.paddingEnd,0)},this.takeSnapshot=()=>{const r=[];if(this.itemSizeCache.size===0)return r;const n=this.getMeasurements();for(const o of n)o&&this.itemSizeCache.has(o.key)&&r.push({index:o.index,key:o.key,start:o.start,size:o.size,end:o.end,lane:o.lane});return r},this._scrollToOffset=(r,{adjustments:n,behavior:o})=>{this._intendedScrollOffset=r+(n??0),this.options.scrollToFn(r,{behavior:o,adjustments:n},this)},this.measure=()=>{this.pendingMin=null,this.itemSizeCache.clear(),this.laneAssignments.clear(),this.itemSizeCacheVersion++,this.notify(!1)},this.setOptions(t)}applyScrollAdjustment(t,r){return t===0?!1:nl()&&(this.isScrolling||this._iosTouching||this._iosJustTouchEnded)?(this._iosDeferredAdjustment+=t,!1):(this._scrollToOffset(this.getScrollOffset(),{adjustments:this.scrollAdjustments+=t,behavior:r}),this.scrollOffset!==null&&(this.scrollOffset+=this.scrollAdjustments,this.scrollOffset<0&&(this.scrollOffset=0),this.scrollAdjustments=0),!0)}scheduleScrollReconcile(){if(!this.targetWindow){this.scrollState=null;return}this.rafId==null&&(this.rafId=this.targetWindow.requestAnimationFrame(()=>{this.rafId=null,this.reconcileScroll()}))}reconcileScroll(){if(!this.scrollState||!this.scrollElement)return;if(this.now()-this.scrollState.startedAt>5e3){this.scrollState=null;return}const n=this.scrollState.index!=null?this.getOffsetForIndex(this.scrollState.index,this.scrollState.align):void 0,o=n?n[0]:this.scrollState.lastTargetOffset,i=1,a=o!==this.scrollState.lastTargetOffset;if(!a&&UI(o,this.getScrollOffset())){if(this.scrollState.stableFrames++,this.scrollState.stableFrames>=i){this.getScrollOffset()!==o&&this._scrollToOffset(o,{adjustments:void 0,behavior:"auto"}),this.scrollState=null;return}}else if(this.scrollState.stableFrames=0,a){const s=this.getSize()||600,l=Math.abs(o-this.getScrollOffset()),c=this.scrollState.behavior==="smooth"&&l>s;this.scrollState.lastTargetOffset=o,c||(this.scrollState.behavior="auto"),this._scrollToOffset(o,{adjustments:void 0,behavior:c?"smooth":"auto"})}this.scheduleScrollReconcile()}}const C_=(e,t,r,n)=>{for(;e<=t;){const o=(e+t)/2|0,i=r(o);if(i<n)e=o+1;else if(i>n)t=o-1;else return o}return e>0?e-1:0};function tC(e,t,r){let n=0;for(;n<=t;){const o=(n+t)/2|0,i=e[o*2];if(i<r)n=o+1;else if(i>r)t=o-1;else return o}return n>0?n-1:0}function rC(e,t,r,n,o){const i=e.length-1;if(e.length<=n)return{startIndex:0,endIndex:i};if(n===1&&o!==null){const c=tC(o,i,r);let d=c;const u=r+t;for(;d<i&&o[d*2]+o[d*2+1]<u;)d++;return{startIndex:c,endIndex:d}}let s=C_(0,i,c=>e[c].start,r),l=s;if(n===1)for(;l<i&&e[l].end<r+t;)l++;else if(n>1){const c=Array(n).fill(0);for(;l<i&&c.some(u=>u<r+t);){const u=e[l];c[u.lane]=u.end,l++}const d=Array(n).fill(r+t);for(;s>=0&&d.some(u=>u>=r);){const u=e[s];d[u.lane]=u.start,s--}s=Math.max(0,s-s%n),l=Math.min(i,l+(n-1-l%n))}return{startIndex:s,endIndex:l}}const ol=typeof document<"u"?g.useLayoutEffect:g.useEffect;function nC({useFlushSync:e=!0,directDomUpdates:t=!1,directDomUpdatesMode:r="transform",...n}){const o=g.useReducer(d=>d+1,0)[1],i=g.useRef({enabled:t,mode:r,container:null,lastSize:null,lastPositions:new WeakMap,prevRange:null});i.current.enabled=t,i.current.mode=r;const a=d=>{const u=i.current;if(!u.enabled||!u.container)return;const p=d.getTotalSize();if(p!==u.lastSize){u.lastSize=p;const v=d.options.horizontal?"width":"height";u.container.style[v]=`${p}px`}},s=d=>{const u=i.current;if(!u.enabled||!u.container)return;a(d);const p=!!d.options.horizontal,v=u.mode==="transform",h=p?"left":"top",m=d.options.scrollMargin,y=d.getVirtualItems();for(const b of y){const k=b.start-m,x=d.elementsCache.get(b.key);x&&u.lastPositions.get(x)!==k&&(u.lastPositions.set(x,k),v?x.style.transform=p?`translate3d(${k}px, 0, 0)`:`translate3d(0, ${k}px, 0)`:x.style[h]=`${k}px`)}},l={...n,onChange:(d,u)=>{var p;const v=i.current;let h=!0;if(v.enabled){s(d);const m=d.range,y=v.prevRange;h=!y||y.isScrolling!==d.isScrolling||y.startIndex!==(m==null?void 0:m.startIndex)||y.endIndex!==(m==null?void 0:m.endIndex),h&&(v.prevRange=m?{startIndex:m.startIndex,endIndex:m.endIndex,isScrolling:d.isScrolling}:null)}h&&(e&&u?pr.flushSync(o):o()),(p=n.onChange)==null||p.call(n,d,u)}},[c]=g.useState(()=>{const d=new eC(l);return Object.assign(d,{containerRef:u=>{const p=i.current;if(p.container=u,p.lastSize=null,u&&p.enabled){const v=d.getTotalSize();p.lastSize=v;const h=d.options.horizontal?"width":"height";u.style[h]=`${v}px`}}})});return c.setOptions(l),ol(()=>c._didMount(),[]),ol(()=>(a(c),c._willUpdate())),ol(()=>{s(c)}),c}function P_(e){return nC({observeElementRect:k_,observeElementOffset:S_,scrollToFn:I_,...e})}function ia(e){throw new Error('Could not dynamically require "'+e+'". Please configure the dynamicRequireTargets or/and ignoreDynamicRequires option of @rollup/plugin-commonjs appropriately for this require call to work.')}var il={exports:{}},hf;function oC(){return hf||(hf=1,(function(e,t){(function(r){e.exports=r()})(function(){return(function r(n,o,i){function a(c,d){if(!o[c]){if(!n[c]){var u=typeof ia=="function"&&ia;if(!d&&u)return u(c,!0);if(s)return s(c,!0);throw new Error("Cannot find module '"+c+"'")}d=o[c]={exports:{}},n[c][0].call(d.exports,function(p){var v=n[c][1][p];return a(v||p)},d,d.exports,r,n,o,i)}return o[c].exports}for(var s=typeof ia=="function"&&ia,l=0;l<i.length;l++)a(i[l]);return a})({1:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){var h=r("crypto");function m(w,A){A=k(w,A);var E;return(E=A.algorithm!=="passthrough"?h.createHash(A.algorithm):new I).write===void 0&&(E.write=E.update,E.end=E.update),_(A,E).dispatch(w),E.update||E.end(""),E.digest?E.digest(A.encoding==="buffer"?void 0:A.encoding):(w=E.read(),A.encoding!=="buffer"?w.toString(A.encoding):w)}(o=n.exports=m).sha1=function(w){return m(w)},o.keys=function(w){return m(w,{excludeValues:!0,algorithm:"sha1",encoding:"hex"})},o.MD5=function(w){return m(w,{algorithm:"md5",encoding:"hex"})},o.keysMD5=function(w){return m(w,{algorithm:"md5",encoding:"hex",excludeValues:!0})};var y=h.getHashes?h.getHashes().slice():["sha1","md5"],b=(y.push("passthrough"),["buffer","hex","binary","base64"]);function k(w,A){var E={};if(E.algorithm=(A=A||{}).algorithm||"sha1",E.encoding=A.encoding||"hex",E.excludeValues=!!A.excludeValues,E.algorithm=E.algorithm.toLowerCase(),E.encoding=E.encoding.toLowerCase(),E.ignoreUnknown=A.ignoreUnknown===!0,E.respectType=A.respectType!==!1,E.respectFunctionNames=A.respectFunctionNames!==!1,E.respectFunctionProperties=A.respectFunctionProperties!==!1,E.unorderedArrays=A.unorderedArrays===!0,E.unorderedSets=A.unorderedSets!==!1,E.unorderedObjects=A.unorderedObjects!==!1,E.replacer=A.replacer||void 0,E.excludeKeys=A.excludeKeys||void 0,w===void 0)throw new Error("Object argument required.");for(var C=0;C<y.length;++C)y[C].toLowerCase()===E.algorithm.toLowerCase()&&(E.algorithm=y[C]);if(y.indexOf(E.algorithm)===-1)throw new Error('Algorithm "'+E.algorithm+'"  not supported. supported values: '+y.join(", "));if(b.indexOf(E.encoding)===-1&&E.algorithm!=="passthrough")throw new Error('Encoding "'+E.encoding+'"  not supported. supported values: '+b.join(", "));return E}function x(w){if(typeof w=="function")return/^function\s+\w*\s*\(\s*\)\s*{\s+\[native code\]\s+}$/i.exec(Function.prototype.toString.call(w))!=null}function _(w,A,E){E=E||[];function C(S){return A.update?A.update(S,"utf8"):A.write(S,"utf8")}return{dispatch:function(S){return this["_"+((S=w.replacer?w.replacer(S):S)===null?"null":typeof S)](S)},_object:function(S){var j,O=Object.prototype.toString.call(S),L=/\[object (.*)\]/i.exec(O);if(L=(L=L?L[1]:"unknown:["+O+"]").toLowerCase(),0<=(O=E.indexOf(S)))return this.dispatch("[CIRCULAR:"+O+"]");if(E.push(S),s!==void 0&&s.isBuffer&&s.isBuffer(S))return C("buffer:"),C(S);if(L==="object"||L==="function"||L==="asyncfunction")return O=Object.keys(S),w.unorderedObjects&&(O=O.sort()),w.respectType===!1||x(S)||O.splice(0,0,"prototype","__proto__","constructor"),w.excludeKeys&&(O=O.filter(function($){return!w.excludeKeys($)})),C("object:"+O.length+":"),j=this,O.forEach(function($){j.dispatch($),C(":"),w.excludeValues||j.dispatch(S[$]),C(",")});if(!this["_"+L]){if(w.ignoreUnknown)return C("["+L+"]");throw new Error('Unknown object type "'+L+'"')}this["_"+L](S)},_array:function(S,$){$=$!==void 0?$:w.unorderedArrays!==!1;var O=this;if(C("array:"+S.length+":"),!$||S.length<=1)return S.forEach(function(F){return O.dispatch(F)});var L=[],$=S.map(function(F){var M=new I,q=E.slice();return _(w,M,q).dispatch(F),L=L.concat(q.slice(E.length)),M.read().toString()});return E=E.concat(L),$.sort(),this._array($,!1)},_date:function(S){return C("date:"+S.toJSON())},_symbol:function(S){return C("symbol:"+S.toString())},_error:function(S){return C("error:"+S.toString())},_boolean:function(S){return C("bool:"+S.toString())},_string:function(S){C("string:"+S.length+":"),C(S.toString())},_function:function(S){C("fn:"),x(S)?this.dispatch("[native]"):this.dispatch(S.toString()),w.respectFunctionNames!==!1&&this.dispatch("function-name:"+String(S.name)),w.respectFunctionProperties&&this._object(S)},_number:function(S){return C("number:"+S.toString())},_xml:function(S){return C("xml:"+S.toString())},_null:function(){return C("Null")},_undefined:function(){return C("Undefined")},_regexp:function(S){return C("regex:"+S.toString())},_uint8array:function(S){return C("uint8array:"),this.dispatch(Array.prototype.slice.call(S))},_uint8clampedarray:function(S){return C("uint8clampedarray:"),this.dispatch(Array.prototype.slice.call(S))},_int8array:function(S){return C("int8array:"),this.dispatch(Array.prototype.slice.call(S))},_uint16array:function(S){return C("uint16array:"),this.dispatch(Array.prototype.slice.call(S))},_int16array:function(S){return C("int16array:"),this.dispatch(Array.prototype.slice.call(S))},_uint32array:function(S){return C("uint32array:"),this.dispatch(Array.prototype.slice.call(S))},_int32array:function(S){return C("int32array:"),this.dispatch(Array.prototype.slice.call(S))},_float32array:function(S){return C("float32array:"),this.dispatch(Array.prototype.slice.call(S))},_float64array:function(S){return C("float64array:"),this.dispatch(Array.prototype.slice.call(S))},_arraybuffer:function(S){return C("arraybuffer:"),this.dispatch(new Uint8Array(S))},_url:function(S){return C("url:"+S.toString())},_map:function(S){return C("map:"),S=Array.from(S),this._array(S,w.unorderedSets!==!1)},_set:function(S){return C("set:"),S=Array.from(S),this._array(S,w.unorderedSets!==!1)},_file:function(S){return C("file:"),this.dispatch([S.name,S.size,S.type,S.lastModfied])},_blob:function(){if(w.ignoreUnknown)return C("[blob]");throw Error(`Hashing Blob objects is currently not supported
(see https://github.com/puleos/object-hash/issues/26)
Use "options.replacer" or "options.ignoreUnknown"
`)},_domwindow:function(){return C("domwindow")},_bigint:function(S){return C("bigint:"+S.toString())},_process:function(){return C("process")},_timer:function(){return C("timer")},_pipe:function(){return C("pipe")},_tcp:function(){return C("tcp")},_udp:function(){return C("udp")},_tty:function(){return C("tty")},_statwatcher:function(){return C("statwatcher")},_securecontext:function(){return C("securecontext")},_connection:function(){return C("connection")},_zlib:function(){return C("zlib")},_context:function(){return C("context")},_nodescript:function(){return C("nodescript")},_httpparser:function(){return C("httpparser")},_dataview:function(){return C("dataview")},_signal:function(){return C("signal")},_fsevent:function(){return C("fsevent")},_tlswrap:function(){return C("tlswrap")}}}function I(){return{buf:"",write:function(w){this.buf+=w},end:function(w){this.buf+=w},read:function(){return this.buf}}}o.writeToStream=function(w,A,E){return E===void 0&&(E=A,A={}),_(A=k(w,A),E).dispatch(w)}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/fake_9a5aa49d.js","/")},{buffer:3,crypto:5,lYpoI2:11}],2:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){(function(h){var m=typeof Uint8Array<"u"?Uint8Array:Array,y=43,b=47,k=48,x=97,_=65,I=45,w=95;function A(E){return E=E.charCodeAt(0),E===y||E===I?62:E===b||E===w?63:E<k?-1:E<k+10?E-k+26+26:E<_+26?E-_:E<x+26?E-x+26:void 0}h.toByteArray=function(E){var C,S;if(0<E.length%4)throw new Error("Invalid string. Length must be a multiple of 4");var j=E.length,j=E.charAt(j-2)==="="?2:E.charAt(j-1)==="="?1:0,O=new m(3*E.length/4-j),L=0<j?E.length-4:E.length,$=0;function F(M){O[$++]=M}for(C=0;C<L;C+=4,0)F((16711680&(S=A(E.charAt(C))<<18|A(E.charAt(C+1))<<12|A(E.charAt(C+2))<<6|A(E.charAt(C+3))))>>16),F((65280&S)>>8),F(255&S);return j==2?F(255&(S=A(E.charAt(C))<<2|A(E.charAt(C+1))>>4)):j==1&&(F((S=A(E.charAt(C))<<10|A(E.charAt(C+1))<<4|A(E.charAt(C+2))>>2)>>8&255),F(255&S)),O},h.fromByteArray=function(E){var C,S,j,O,L=E.length%3,$="";function F(M){return"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(M)}for(C=0,j=E.length-L;C<j;C+=3)S=(E[C]<<16)+(E[C+1]<<8)+E[C+2],$+=F((O=S)>>18&63)+F(O>>12&63)+F(O>>6&63)+F(63&O);switch(L){case 1:$=($+=F((S=E[E.length-1])>>2))+F(S<<4&63)+"==";break;case 2:$=($=($+=F((S=(E[E.length-2]<<8)+E[E.length-1])>>10))+F(S>>4&63))+F(S<<2&63)+"="}return $}})(o===void 0?this.base64js={}:o)}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/base64-js/lib/b64.js","/node_modules/gulp-browserify/node_modules/base64-js/lib")},{buffer:3,lYpoI2:11}],3:[function(r,n,o){(function(i,a,y,l,c,d,u,p,v){var h=r("base64-js"),m=r("ieee754");function y(P,T,R){if(!(this instanceof y))return new y(P,T,R);var U,V,G,ne,ue=typeof P;if(T==="base64"&&ue=="string")for(P=(ne=P).trim?ne.trim():ne.replace(/^\s+|\s+$/g,"");P.length%4!=0;)P+="=";if(ue=="number")U=W(P);else if(ue=="string")U=y.byteLength(P,T);else{if(ue!="object")throw new Error("First argument needs to be a number, array or string.");U=W(P.length)}if(y._useTypedArrays?V=y._augment(new Uint8Array(U)):((V=this).length=U,V._isBuffer=!0),y._useTypedArrays&&typeof P.byteLength=="number")V._set(P);else if(B(ne=P)||y.isBuffer(ne)||ne&&typeof ne=="object"&&typeof ne.length=="number")for(G=0;G<U;G++)y.isBuffer(P)?V[G]=P.readUInt8(G):V[G]=P[G];else if(ue=="string")V.write(P,0,T);else if(ue=="number"&&!y._useTypedArrays&&!R)for(G=0;G<U;G++)V[G]=0;return V}function b(P,T,R,U){return y._charsWritten=te((function(V){for(var G=[],ne=0;ne<V.length;ne++)G.push(255&V.charCodeAt(ne));return G})(T),P,R,U)}function k(P,T,R,U){return y._charsWritten=te((function(V){for(var G,ne,ue=[],ve=0;ve<V.length;ve++)ne=V.charCodeAt(ve),G=ne>>8,ne=ne%256,ue.push(ne),ue.push(G);return ue})(T),P,R,U)}function x(P,T,R){var U="";R=Math.min(P.length,R);for(var V=T;V<R;V++)U+=String.fromCharCode(P[V]);return U}function _(P,T,R,G){G||(Y(typeof R=="boolean","missing or invalid endian"),Y(T!=null,"missing offset"),Y(T+1<P.length,"Trying to read beyond buffer length"));var V,G=P.length;if(!(G<=T))return R?(V=P[T],T+1<G&&(V|=P[T+1]<<8)):(V=P[T]<<8,T+1<G&&(V|=P[T+1])),V}function I(P,T,R,G){G||(Y(typeof R=="boolean","missing or invalid endian"),Y(T!=null,"missing offset"),Y(T+3<P.length,"Trying to read beyond buffer length"));var V,G=P.length;if(!(G<=T))return R?(T+2<G&&(V=P[T+2]<<16),T+1<G&&(V|=P[T+1]<<8),V|=P[T],T+3<G&&(V+=P[T+3]<<24>>>0)):(T+1<G&&(V=P[T+1]<<16),T+2<G&&(V|=P[T+2]<<8),T+3<G&&(V|=P[T+3]),V+=P[T]<<24>>>0),V}function w(P,T,R,U){if(U||(Y(typeof R=="boolean","missing or invalid endian"),Y(T!=null,"missing offset"),Y(T+1<P.length,"Trying to read beyond buffer length")),!(P.length<=T))return U=_(P,T,R,!0),32768&U?-1*(65535-U+1):U}function A(P,T,R,U){if(U||(Y(typeof R=="boolean","missing or invalid endian"),Y(T!=null,"missing offset"),Y(T+3<P.length,"Trying to read beyond buffer length")),!(P.length<=T))return U=I(P,T,R,!0),2147483648&U?-1*(4294967295-U+1):U}function E(P,T,R,U){return U||(Y(typeof R=="boolean","missing or invalid endian"),Y(T+3<P.length,"Trying to read beyond buffer length")),m.read(P,T,R,23,4)}function C(P,T,R,U){return U||(Y(typeof R=="boolean","missing or invalid endian"),Y(T+7<P.length,"Trying to read beyond buffer length")),m.read(P,T,R,52,8)}function S(P,T,R,U,V){if(V||(Y(T!=null,"missing value"),Y(typeof U=="boolean","missing or invalid endian"),Y(R!=null,"missing offset"),Y(R+1<P.length,"trying to write beyond buffer length"),Q(T,65535)),V=P.length,!(V<=R))for(var G=0,ne=Math.min(V-R,2);G<ne;G++)P[R+G]=(T&255<<8*(U?G:1-G))>>>8*(U?G:1-G)}function j(P,T,R,U,V){if(V||(Y(T!=null,"missing value"),Y(typeof U=="boolean","missing or invalid endian"),Y(R!=null,"missing offset"),Y(R+3<P.length,"trying to write beyond buffer length"),Q(T,4294967295)),V=P.length,!(V<=R))for(var G=0,ne=Math.min(V-R,4);G<ne;G++)P[R+G]=T>>>8*(U?G:3-G)&255}function O(P,T,R,U,V){V||(Y(T!=null,"missing value"),Y(typeof U=="boolean","missing or invalid endian"),Y(R!=null,"missing offset"),Y(R+1<P.length,"Trying to write beyond buffer length"),ie(T,32767,-32768)),P.length<=R||S(P,0<=T?T:65535+T+1,R,U,V)}function L(P,T,R,U,V){V||(Y(T!=null,"missing value"),Y(typeof U=="boolean","missing or invalid endian"),Y(R!=null,"missing offset"),Y(R+3<P.length,"Trying to write beyond buffer length"),ie(T,2147483647,-2147483648)),P.length<=R||j(P,0<=T?T:4294967295+T+1,R,U,V)}function $(P,T,R,U,V){V||(Y(T!=null,"missing value"),Y(typeof U=="boolean","missing or invalid endian"),Y(R!=null,"missing offset"),Y(R+3<P.length,"Trying to write beyond buffer length"),ke(T,34028234663852886e22,-34028234663852886e22)),P.length<=R||m.write(P,T,R,U,23,4)}function F(P,T,R,U,V){V||(Y(T!=null,"missing value"),Y(typeof U=="boolean","missing or invalid endian"),Y(R!=null,"missing offset"),Y(R+7<P.length,"Trying to write beyond buffer length"),ke(T,17976931348623157e292,-17976931348623157e292)),P.length<=R||m.write(P,T,R,U,52,8)}o.Buffer=y,o.SlowBuffer=y,o.INSPECT_MAX_BYTES=50,y.poolSize=8192,y._useTypedArrays=(function(){try{var P=new ArrayBuffer(0),T=new Uint8Array(P);return T.foo=function(){return 42},T.foo()===42&&typeof T.subarray=="function"}catch{return!1}})(),y.isEncoding=function(P){switch(String(P).toLowerCase()){case"hex":case"utf8":case"utf-8":case"ascii":case"binary":case"base64":case"raw":case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return!0;default:return!1}},y.isBuffer=function(P){return!(P==null||!P._isBuffer)},y.byteLength=function(P,T){var R;switch(P+="",T||"utf8"){case"hex":R=P.length/2;break;case"utf8":case"utf-8":R=oe(P).length;break;case"ascii":case"binary":case"raw":R=P.length;break;case"base64":R=K(P).length;break;case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":R=2*P.length;break;default:throw new Error("Unknown encoding")}return R},y.concat=function(P,T){if(Y(B(P),`Usage: Buffer.concat(list, [totalLength])
list should be an Array.`),P.length===0)return new y(0);if(P.length===1)return P[0];if(typeof T!="number")for(V=T=0;V<P.length;V++)T+=P[V].length;for(var R=new y(T),U=0,V=0;V<P.length;V++){var G=P[V];G.copy(R,U),U+=G.length}return R},y.prototype.write=function(P,T,R,U){isFinite(T)?isFinite(R)||(U=R,R=void 0):(ve=U,U=T,T=R,R=ve),T=Number(T)||0;var V,G,ne,ue,ve=this.length-T;switch((!R||ve<(R=Number(R)))&&(R=ve),U=String(U||"utf8").toLowerCase()){case"hex":V=(function($e,je,Ee,we){Ee=Number(Ee)||0;var he=$e.length-Ee;(!we||he<(we=Number(we)))&&(we=he),Y((he=je.length)%2==0,"Invalid hex string"),he/2<we&&(we=he/2);for(var Pt=0;Pt<we;Pt++){var Qt=parseInt(je.substr(2*Pt,2),16);Y(!isNaN(Qt),"Invalid hex string"),$e[Ee+Pt]=Qt}return y._charsWritten=2*Pt,Pt})(this,P,T,R);break;case"utf8":case"utf-8":G=this,ne=T,ue=R,V=y._charsWritten=te(oe(P),G,ne,ue);break;case"ascii":case"binary":V=b(this,P,T,R);break;case"base64":G=this,ne=T,ue=R,V=y._charsWritten=te(K(P),G,ne,ue);break;case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":V=k(this,P,T,R);break;default:throw new Error("Unknown encoding")}return V},y.prototype.toString=function(P,T,R){var U,V,G,ne,ue=this;if(P=String(P||"utf8").toLowerCase(),T=Number(T)||0,(R=R!==void 0?Number(R):ue.length)===T)return"";switch(P){case"hex":U=(function(ve,$e,je){var Ee=ve.length;(!$e||$e<0)&&($e=0),(!je||je<0||Ee<je)&&(je=Ee);for(var we="",he=$e;he<je;he++)we+=Z(ve[he]);return we})(ue,T,R);break;case"utf8":case"utf-8":U=(function(ve,$e,je){var Ee="",we="";je=Math.min(ve.length,je);for(var he=$e;he<je;he++)ve[he]<=127?(Ee+=be(we)+String.fromCharCode(ve[he]),we=""):we+="%"+ve[he].toString(16);return Ee+be(we)})(ue,T,R);break;case"ascii":case"binary":U=x(ue,T,R);break;case"base64":V=ue,ne=R,U=(G=T)===0&&ne===V.length?h.fromByteArray(V):h.fromByteArray(V.slice(G,ne));break;case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":U=(function(ve,$e,je){for(var Ee=ve.slice($e,je),we="",he=0;he<Ee.length;he+=2)we+=String.fromCharCode(Ee[he]+256*Ee[he+1]);return we})(ue,T,R);break;default:throw new Error("Unknown encoding")}return U},y.prototype.toJSON=function(){return{type:"Buffer",data:Array.prototype.slice.call(this._arr||this,0)}},y.prototype.copy=function(P,T,R,U){if(T=T||0,(U=U||U===0?U:this.length)!==(R=R||0)&&P.length!==0&&this.length!==0){Y(R<=U,"sourceEnd < sourceStart"),Y(0<=T&&T<P.length,"targetStart out of bounds"),Y(0<=R&&R<this.length,"sourceStart out of bounds"),Y(0<=U&&U<=this.length,"sourceEnd out of bounds"),U>this.length&&(U=this.length);var V=(U=P.length-T<U-R?P.length-T+R:U)-R;if(V<100||!y._useTypedArrays)for(var G=0;G<V;G++)P[G+T]=this[G+R];else P._set(this.subarray(R,R+V),T)}},y.prototype.slice=function(P,T){var R=this.length;if(P=q(P,R,0),T=q(T,R,R),y._useTypedArrays)return y._augment(this.subarray(P,T));for(var U=T-P,V=new y(U,void 0,!0),G=0;G<U;G++)V[G]=this[G+P];return V},y.prototype.get=function(P){return console.log(".get() is deprecated. Access using array indexes instead."),this.readUInt8(P)},y.prototype.set=function(P,T){return console.log(".set() is deprecated. Access using array indexes instead."),this.writeUInt8(P,T)},y.prototype.readUInt8=function(P,T){if(T||(Y(P!=null,"missing offset"),Y(P<this.length,"Trying to read beyond buffer length")),!(P>=this.length))return this[P]},y.prototype.readUInt16LE=function(P,T){return _(this,P,!0,T)},y.prototype.readUInt16BE=function(P,T){return _(this,P,!1,T)},y.prototype.readUInt32LE=function(P,T){return I(this,P,!0,T)},y.prototype.readUInt32BE=function(P,T){return I(this,P,!1,T)},y.prototype.readInt8=function(P,T){if(T||(Y(P!=null,"missing offset"),Y(P<this.length,"Trying to read beyond buffer length")),!(P>=this.length))return 128&this[P]?-1*(255-this[P]+1):this[P]},y.prototype.readInt16LE=function(P,T){return w(this,P,!0,T)},y.prototype.readInt16BE=function(P,T){return w(this,P,!1,T)},y.prototype.readInt32LE=function(P,T){return A(this,P,!0,T)},y.prototype.readInt32BE=function(P,T){return A(this,P,!1,T)},y.prototype.readFloatLE=function(P,T){return E(this,P,!0,T)},y.prototype.readFloatBE=function(P,T){return E(this,P,!1,T)},y.prototype.readDoubleLE=function(P,T){return C(this,P,!0,T)},y.prototype.readDoubleBE=function(P,T){return C(this,P,!1,T)},y.prototype.writeUInt8=function(P,T,R){R||(Y(P!=null,"missing value"),Y(T!=null,"missing offset"),Y(T<this.length,"trying to write beyond buffer length"),Q(P,255)),T>=this.length||(this[T]=P)},y.prototype.writeUInt16LE=function(P,T,R){S(this,P,T,!0,R)},y.prototype.writeUInt16BE=function(P,T,R){S(this,P,T,!1,R)},y.prototype.writeUInt32LE=function(P,T,R){j(this,P,T,!0,R)},y.prototype.writeUInt32BE=function(P,T,R){j(this,P,T,!1,R)},y.prototype.writeInt8=function(P,T,R){R||(Y(P!=null,"missing value"),Y(T!=null,"missing offset"),Y(T<this.length,"Trying to write beyond buffer length"),ie(P,127,-128)),T>=this.length||(0<=P?this.writeUInt8(P,T,R):this.writeUInt8(255+P+1,T,R))},y.prototype.writeInt16LE=function(P,T,R){O(this,P,T,!0,R)},y.prototype.writeInt16BE=function(P,T,R){O(this,P,T,!1,R)},y.prototype.writeInt32LE=function(P,T,R){L(this,P,T,!0,R)},y.prototype.writeInt32BE=function(P,T,R){L(this,P,T,!1,R)},y.prototype.writeFloatLE=function(P,T,R){$(this,P,T,!0,R)},y.prototype.writeFloatBE=function(P,T,R){$(this,P,T,!1,R)},y.prototype.writeDoubleLE=function(P,T,R){F(this,P,T,!0,R)},y.prototype.writeDoubleBE=function(P,T,R){F(this,P,T,!1,R)},y.prototype.fill=function(P,T,R){if(T=T||0,R=R||this.length,Y(typeof(P=typeof(P=P||0)=="string"?P.charCodeAt(0):P)=="number"&&!isNaN(P),"value is not a number"),Y(T<=R,"end < start"),R!==T&&this.length!==0){Y(0<=T&&T<this.length,"start out of bounds"),Y(0<=R&&R<=this.length,"end out of bounds");for(var U=T;U<R;U++)this[U]=P}},y.prototype.inspect=function(){for(var P=[],T=this.length,R=0;R<T;R++)if(P[R]=Z(this[R]),R===o.INSPECT_MAX_BYTES){P[R+1]="...";break}return"<Buffer "+P.join(" ")+">"},y.prototype.toArrayBuffer=function(){if(typeof Uint8Array>"u")throw new Error("Buffer.toArrayBuffer not supported in this browser");if(y._useTypedArrays)return new y(this).buffer;for(var P=new Uint8Array(this.length),T=0,R=P.length;T<R;T+=1)P[T]=this[T];return P.buffer};var M=y.prototype;function q(P,T,R){return typeof P!="number"?R:T<=(P=~~P)?T:0<=P||0<=(P+=T)?P:0}function W(P){return(P=~~Math.ceil(+P))<0?0:P}function B(P){return(Array.isArray||function(T){return Object.prototype.toString.call(T)==="[object Array]"})(P)}function Z(P){return P<16?"0"+P.toString(16):P.toString(16)}function oe(P){for(var T=[],R=0;R<P.length;R++){var U=P.charCodeAt(R);if(U<=127)T.push(P.charCodeAt(R));else for(var V=R,G=(55296<=U&&U<=57343&&R++,encodeURIComponent(P.slice(V,R+1)).substr(1).split("%")),ne=0;ne<G.length;ne++)T.push(parseInt(G[ne],16))}return T}function K(P){return h.toByteArray(P)}function te(P,T,R,U){for(var V=0;V<U&&!(V+R>=T.length||V>=P.length);V++)T[V+R]=P[V];return V}function be(P){try{return decodeURIComponent(P)}catch{return"�"}}function Q(P,T){Y(typeof P=="number","cannot write a non-number as a number"),Y(0<=P,"specified a negative value for writing an unsigned value"),Y(P<=T,"value is larger than maximum value for type"),Y(Math.floor(P)===P,"value has a fractional component")}function ie(P,T,R){Y(typeof P=="number","cannot write a non-number as a number"),Y(P<=T,"value larger than maximum allowed value"),Y(R<=P,"value smaller than minimum allowed value"),Y(Math.floor(P)===P,"value has a fractional component")}function ke(P,T,R){Y(typeof P=="number","cannot write a non-number as a number"),Y(P<=T,"value larger than maximum allowed value"),Y(R<=P,"value smaller than minimum allowed value")}function Y(P,T){if(!P)throw new Error(T||"Failed assertion")}y._augment=function(P){return P._isBuffer=!0,P._get=P.get,P._set=P.set,P.get=M.get,P.set=M.set,P.write=M.write,P.toString=M.toString,P.toLocaleString=M.toString,P.toJSON=M.toJSON,P.copy=M.copy,P.slice=M.slice,P.readUInt8=M.readUInt8,P.readUInt16LE=M.readUInt16LE,P.readUInt16BE=M.readUInt16BE,P.readUInt32LE=M.readUInt32LE,P.readUInt32BE=M.readUInt32BE,P.readInt8=M.readInt8,P.readInt16LE=M.readInt16LE,P.readInt16BE=M.readInt16BE,P.readInt32LE=M.readInt32LE,P.readInt32BE=M.readInt32BE,P.readFloatLE=M.readFloatLE,P.readFloatBE=M.readFloatBE,P.readDoubleLE=M.readDoubleLE,P.readDoubleBE=M.readDoubleBE,P.writeUInt8=M.writeUInt8,P.writeUInt16LE=M.writeUInt16LE,P.writeUInt16BE=M.writeUInt16BE,P.writeUInt32LE=M.writeUInt32LE,P.writeUInt32BE=M.writeUInt32BE,P.writeInt8=M.writeInt8,P.writeInt16LE=M.writeInt16LE,P.writeInt16BE=M.writeInt16BE,P.writeInt32LE=M.writeInt32LE,P.writeInt32BE=M.writeInt32BE,P.writeFloatLE=M.writeFloatLE,P.writeFloatBE=M.writeFloatBE,P.writeDoubleLE=M.writeDoubleLE,P.writeDoubleBE=M.writeDoubleBE,P.fill=M.fill,P.inspect=M.inspect,P.toArrayBuffer=M.toArrayBuffer,P}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/buffer/index.js","/node_modules/gulp-browserify/node_modules/buffer")},{"base64-js":2,buffer:3,ieee754:10,lYpoI2:11}],4:[function(r,n,o){(function(i,a,h,l,c,d,u,p,v){var h=r("buffer").Buffer,m=4,y=new h(m);y.fill(0),n.exports={hash:function(b,k,x,_){for(var I=k((function(S,j){S.length%m!=0&&(O=S.length+(m-S.length%m),S=h.concat([S,y],O));for(var O,L=[],$=j?S.readInt32BE:S.readInt32LE,F=0;F<S.length;F+=m)L.push($.call(S,F));return L})(b=h.isBuffer(b)?b:new h(b),_),8*b.length),k=_,w=new h(x),A=k?w.writeInt32BE:w.writeInt32LE,E=0;E<I.length;E++)A.call(w,I[E],4*E,!0);return w}}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/crypto-browserify/helpers.js","/node_modules/gulp-browserify/node_modules/crypto-browserify")},{buffer:3,lYpoI2:11}],5:[function(r,n,o){(function(i,a,h,l,c,d,u,p,v){var h=r("buffer").Buffer,m=r("./sha"),y=r("./sha256"),b=r("./rng"),k={sha1:m,sha256:y,md5:r("./md5")},x=64,_=new h(x);function I(S,j){var O=k[S=S||"sha1"],L=[];return O||w("algorithm:",S,"is not yet supported"),{update:function($){return h.isBuffer($)||($=new h($)),L.push($),$.length,this},digest:function($){var F=h.concat(L),F=j?(function(M,q,W){h.isBuffer(q)||(q=new h(q)),h.isBuffer(W)||(W=new h(W)),q.length>x?q=M(q):q.length<x&&(q=h.concat([q,_],x));for(var B=new h(x),Z=new h(x),oe=0;oe<x;oe++)B[oe]=54^q[oe],Z[oe]=92^q[oe];return W=M(h.concat([B,W])),M(h.concat([Z,W]))})(O,j,F):O(F);return L=null,$?F.toString($):F}}}function w(){var S=[].slice.call(arguments).join(" ");throw new Error([S,"we accept pull requests","http://github.com/dominictarr/crypto-browserify"].join(`
`))}_.fill(0),o.createHash=function(S){return I(S)},o.createHmac=I,o.randomBytes=function(S,j){if(!j||!j.call)return new h(b(S));try{j.call(this,void 0,new h(b(S)))}catch(O){j(O)}};var A,E=["createCredentials","createCipher","createCipheriv","createDecipher","createDecipheriv","createSign","createVerify","createDiffieHellman","pbkdf2"],C=function(S){o[S]=function(){w("sorry,",S,"is not implemented yet")}};for(A in E)C(E[A])}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/crypto-browserify/index.js","/node_modules/gulp-browserify/node_modules/crypto-browserify")},{"./md5":6,"./rng":7,"./sha":8,"./sha256":9,buffer:3,lYpoI2:11}],6:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){var h=r("./helpers");function m(w,A){w[A>>5]|=128<<A%32,w[14+(A+64>>>9<<4)]=A;for(var E=1732584193,C=-271733879,S=-1732584194,j=271733878,O=0;O<w.length;O+=16){var L=E,$=C,F=S,M=j,E=b(E,C,S,j,w[O+0],7,-680876936),j=b(j,E,C,S,w[O+1],12,-389564586),S=b(S,j,E,C,w[O+2],17,606105819),C=b(C,S,j,E,w[O+3],22,-1044525330);E=b(E,C,S,j,w[O+4],7,-176418897),j=b(j,E,C,S,w[O+5],12,1200080426),S=b(S,j,E,C,w[O+6],17,-1473231341),C=b(C,S,j,E,w[O+7],22,-45705983),E=b(E,C,S,j,w[O+8],7,1770035416),j=b(j,E,C,S,w[O+9],12,-1958414417),S=b(S,j,E,C,w[O+10],17,-42063),C=b(C,S,j,E,w[O+11],22,-1990404162),E=b(E,C,S,j,w[O+12],7,1804603682),j=b(j,E,C,S,w[O+13],12,-40341101),S=b(S,j,E,C,w[O+14],17,-1502002290),E=k(E,C=b(C,S,j,E,w[O+15],22,1236535329),S,j,w[O+1],5,-165796510),j=k(j,E,C,S,w[O+6],9,-1069501632),S=k(S,j,E,C,w[O+11],14,643717713),C=k(C,S,j,E,w[O+0],20,-373897302),E=k(E,C,S,j,w[O+5],5,-701558691),j=k(j,E,C,S,w[O+10],9,38016083),S=k(S,j,E,C,w[O+15],14,-660478335),C=k(C,S,j,E,w[O+4],20,-405537848),E=k(E,C,S,j,w[O+9],5,568446438),j=k(j,E,C,S,w[O+14],9,-1019803690),S=k(S,j,E,C,w[O+3],14,-187363961),C=k(C,S,j,E,w[O+8],20,1163531501),E=k(E,C,S,j,w[O+13],5,-1444681467),j=k(j,E,C,S,w[O+2],9,-51403784),S=k(S,j,E,C,w[O+7],14,1735328473),E=x(E,C=k(C,S,j,E,w[O+12],20,-1926607734),S,j,w[O+5],4,-378558),j=x(j,E,C,S,w[O+8],11,-2022574463),S=x(S,j,E,C,w[O+11],16,1839030562),C=x(C,S,j,E,w[O+14],23,-35309556),E=x(E,C,S,j,w[O+1],4,-1530992060),j=x(j,E,C,S,w[O+4],11,1272893353),S=x(S,j,E,C,w[O+7],16,-155497632),C=x(C,S,j,E,w[O+10],23,-1094730640),E=x(E,C,S,j,w[O+13],4,681279174),j=x(j,E,C,S,w[O+0],11,-358537222),S=x(S,j,E,C,w[O+3],16,-722521979),C=x(C,S,j,E,w[O+6],23,76029189),E=x(E,C,S,j,w[O+9],4,-640364487),j=x(j,E,C,S,w[O+12],11,-421815835),S=x(S,j,E,C,w[O+15],16,530742520),E=_(E,C=x(C,S,j,E,w[O+2],23,-995338651),S,j,w[O+0],6,-198630844),j=_(j,E,C,S,w[O+7],10,1126891415),S=_(S,j,E,C,w[O+14],15,-1416354905),C=_(C,S,j,E,w[O+5],21,-57434055),E=_(E,C,S,j,w[O+12],6,1700485571),j=_(j,E,C,S,w[O+3],10,-1894986606),S=_(S,j,E,C,w[O+10],15,-1051523),C=_(C,S,j,E,w[O+1],21,-2054922799),E=_(E,C,S,j,w[O+8],6,1873313359),j=_(j,E,C,S,w[O+15],10,-30611744),S=_(S,j,E,C,w[O+6],15,-1560198380),C=_(C,S,j,E,w[O+13],21,1309151649),E=_(E,C,S,j,w[O+4],6,-145523070),j=_(j,E,C,S,w[O+11],10,-1120210379),S=_(S,j,E,C,w[O+2],15,718787259),C=_(C,S,j,E,w[O+9],21,-343485551),E=I(E,L),C=I(C,$),S=I(S,F),j=I(j,M)}return Array(E,C,S,j)}function y(w,A,E,C,S,j){return I((A=I(I(A,w),I(C,j)))<<S|A>>>32-S,E)}function b(w,A,E,C,S,j,O){return y(A&E|~A&C,w,A,S,j,O)}function k(w,A,E,C,S,j,O){return y(A&C|E&~C,w,A,S,j,O)}function x(w,A,E,C,S,j,O){return y(A^E^C,w,A,S,j,O)}function _(w,A,E,C,S,j,O){return y(E^(A|~C),w,A,S,j,O)}function I(w,A){var E=(65535&w)+(65535&A);return(w>>16)+(A>>16)+(E>>16)<<16|65535&E}n.exports=function(w){return h.hash(w,m,16)}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/crypto-browserify/md5.js","/node_modules/gulp-browserify/node_modules/crypto-browserify")},{"./helpers":4,buffer:3,lYpoI2:11}],7:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){n.exports=function(h){for(var m,y=new Array(h),b=0;b<h;b++)(3&b)==0&&(m=4294967296*Math.random()),y[b]=m>>>((3&b)<<3)&255;return y}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/crypto-browserify/rng.js","/node_modules/gulp-browserify/node_modules/crypto-browserify")},{buffer:3,lYpoI2:11}],8:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){var h=r("./helpers");function m(k,x){k[x>>5]|=128<<24-x%32,k[15+(x+64>>9<<4)]=x;for(var _,I,w,A=Array(80),E=1732584193,C=-271733879,S=-1732584194,j=271733878,O=-1009589776,L=0;L<k.length;L+=16){for(var $=E,F=C,M=S,q=j,W=O,B=0;B<80;B++){A[B]=B<16?k[L+B]:b(A[B-3]^A[B-8]^A[B-14]^A[B-16],1);var Z=y(y(b(E,5),(Z=C,I=S,w=j,(_=B)<20?Z&I|~Z&w:!(_<40)&&_<60?Z&I|Z&w|I&w:Z^I^w)),y(y(O,A[B]),(_=B)<20?1518500249:_<40?1859775393:_<60?-1894007588:-899497514)),O=j,j=S,S=b(C,30),C=E,E=Z}E=y(E,$),C=y(C,F),S=y(S,M),j=y(j,q),O=y(O,W)}return Array(E,C,S,j,O)}function y(k,x){var _=(65535&k)+(65535&x);return(k>>16)+(x>>16)+(_>>16)<<16|65535&_}function b(k,x){return k<<x|k>>>32-x}n.exports=function(k){return h.hash(k,m,20,!0)}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/crypto-browserify/sha.js","/node_modules/gulp-browserify/node_modules/crypto-browserify")},{"./helpers":4,buffer:3,lYpoI2:11}],9:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){function h(x,_){var I=(65535&x)+(65535&_);return(x>>16)+(_>>16)+(I>>16)<<16|65535&I}function m(x,_){var I,w=new Array(1116352408,1899447441,3049323471,3921009573,961987163,1508970993,2453635748,2870763221,3624381080,310598401,607225278,1426881987,1925078388,2162078206,2614888103,3248222580,3835390401,4022224774,264347078,604807628,770255983,1249150122,1555081692,1996064986,2554220882,2821834349,2952996808,3210313671,3336571891,3584528711,113926993,338241895,666307205,773529912,1294757372,1396182291,1695183700,1986661051,2177026350,2456956037,2730485921,2820302411,3259730800,3345764771,3516065817,3600352804,4094571909,275423344,430227734,506948616,659060556,883997877,958139571,1322822218,1537002063,1747873779,1955562222,2024104815,2227730452,2361852424,2428436474,2756734187,3204031479,3329325298),A=new Array(1779033703,3144134277,1013904242,2773480762,1359893119,2600822924,528734635,1541459225),E=new Array(64);x[_>>5]|=128<<24-_%32,x[15+(_+64>>9<<4)]=_;for(var C,S,j=0;j<x.length;j+=16){for(var O=A[0],L=A[1],$=A[2],F=A[3],M=A[4],q=A[5],W=A[6],B=A[7],Z=0;Z<64;Z++)E[Z]=Z<16?x[Z+j]:h(h(h((S=E[Z-2],b(S,17)^b(S,19)^k(S,10)),E[Z-7]),(S=E[Z-15],b(S,7)^b(S,18)^k(S,3))),E[Z-16]),I=h(h(h(h(B,b(S=M,6)^b(S,11)^b(S,25)),M&q^~M&W),w[Z]),E[Z]),C=h(b(C=O,2)^b(C,13)^b(C,22),O&L^O&$^L&$),B=W,W=q,q=M,M=h(F,I),F=$,$=L,L=O,O=h(I,C);A[0]=h(O,A[0]),A[1]=h(L,A[1]),A[2]=h($,A[2]),A[3]=h(F,A[3]),A[4]=h(M,A[4]),A[5]=h(q,A[5]),A[6]=h(W,A[6]),A[7]=h(B,A[7])}return A}var y=r("./helpers"),b=function(x,_){return x>>>_|x<<32-_},k=function(x,_){return x>>>_};n.exports=function(x){return y.hash(x,m,32,!0)}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/crypto-browserify/sha256.js","/node_modules/gulp-browserify/node_modules/crypto-browserify")},{"./helpers":4,buffer:3,lYpoI2:11}],10:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){o.read=function(h,m,y,b,j){var x,_,I=8*j-b-1,w=(1<<I)-1,A=w>>1,E=-7,C=y?j-1:0,S=y?-1:1,j=h[m+C];for(C+=S,x=j&(1<<-E)-1,j>>=-E,E+=I;0<E;x=256*x+h[m+C],C+=S,E-=8);for(_=x&(1<<-E)-1,x>>=-E,E+=b;0<E;_=256*_+h[m+C],C+=S,E-=8);if(x===0)x=1-A;else{if(x===w)return _?NaN:1/0*(j?-1:1);_+=Math.pow(2,b),x-=A}return(j?-1:1)*_*Math.pow(2,x-b)},o.write=function(h,m,y,b,k,O){var _,I,w=8*O-k-1,A=(1<<w)-1,E=A>>1,C=k===23?Math.pow(2,-24)-Math.pow(2,-77):0,S=b?0:O-1,j=b?1:-1,O=m<0||m===0&&1/m<0?1:0;for(m=Math.abs(m),isNaN(m)||m===1/0?(I=isNaN(m)?1:0,_=A):(_=Math.floor(Math.log(m)/Math.LN2),m*(b=Math.pow(2,-_))<1&&(_--,b*=2),2<=(m+=1<=_+E?C/b:C*Math.pow(2,1-E))*b&&(_++,b/=2),A<=_+E?(I=0,_=A):1<=_+E?(I=(m*b-1)*Math.pow(2,k),_+=E):(I=m*Math.pow(2,E-1)*Math.pow(2,k),_=0));8<=k;h[y+S]=255&I,S+=j,I/=256,k-=8);for(_=_<<k|I,w+=k;0<w;h[y+S]=255&_,S+=j,_/=256,w-=8);h[y+S-j]|=128*O}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/ieee754/index.js","/node_modules/gulp-browserify/node_modules/ieee754")},{buffer:3,lYpoI2:11}],11:[function(r,n,o){(function(i,a,s,l,c,d,u,p,v){var h,m,y;function b(){}(i=n.exports={}).nextTick=(m=typeof window<"u"&&window.setImmediate,y=typeof window<"u"&&window.postMessage&&window.addEventListener,m?function(k){return window.setImmediate(k)}:y?(h=[],window.addEventListener("message",function(k){var x=k.source;x!==window&&x!==null||k.data!=="process-tick"||(k.stopPropagation(),0<h.length&&h.shift()())},!0),function(k){h.push(k),window.postMessage("process-tick","*")}):function(k){setTimeout(k,0)}),i.title="browser",i.browser=!0,i.env={},i.argv=[],i.on=b,i.addListener=b,i.once=b,i.off=b,i.removeListener=b,i.removeAllListeners=b,i.emit=b,i.binding=function(k){throw new Error("process.binding is not supported")},i.cwd=function(){return"/"},i.chdir=function(k){throw new Error("process.chdir is not supported")}}).call(this,r("lYpoI2"),typeof self<"u"?self:typeof window<"u"?window:{},r("buffer").Buffer,arguments[3],arguments[4],arguments[5],arguments[6],"/node_modules/gulp-browserify/node_modules/process/browser.js","/node_modules/gulp-browserify/node_modules/process")},{buffer:3,lYpoI2:11}]},{},[1])(1)})})(il)),il.exports}var iC=oC();const al=Dc(iC);z();z();z();var aC=e=>{if(typeof e!="object"||e===null)return!1;const t=Object.getPrototypeOf(e);return t===Object.prototype||t===null},vf=e=>Array.isArray(e)?[...e]:aC(e)?D({},e):{};function Ss(e,t,r){const n=t.split("."),o=D({},e);let i=o;for(let a=0;a<n.length;a++){const[s,l]=n[a].replace("]","").split("["),c=a===n.length-1;if(l!==void 0){i[s]=Array.isArray(i[s])?[...i[s]]:[];const d=Number(l);if(c){i[s][d]=r;continue}i[s][d]=vf(i[s][d]),i=i[s][d];continue}if(c){i[s]=r;continue}i[s]=vf(i[s]),i=i[s]}return o}z();z();var sC={Button:"_Button_oe4qj_1","Button--medium":"_Button--medium_oe4qj_34","Button--large":"_Button--large_oe4qj_62","Button-icon":"_Button-icon_oe4qj_89","Button--primary":"_Button--primary_oe4qj_93","Button--disabled":"_Button--disabled_oe4qj_123","Button--secondary":"_Button--secondary_oe4qj_135","Button--flush":"_Button--flush_oe4qj_171","Button--fullWidth":"_Button--fullWidth_oe4qj_179","Button-spinner":"_Button-spinner_oe4qj_184"};z();var lC=/^(data-.*)$/,cC=e=>{let t={};for(const r in e)Object.prototype.hasOwnProperty.call(e,r)&&lC.test(r)&&(t[r]=e[r]);return t},sl=ee("Button",sC),kc=e=>{var t=e,{children:r,href:n,onClick:o,variant:i="primary",type:a,disabled:s,tabIndex:l,newTab:c,fullWidth:d,icon:u,size:p="medium",loading:v=!1}=t,h=Tt(t,["children","href","onClick","variant","type","disabled","tabIndex","newTab","fullWidth","icon","size","loading"]);const[m,y]=g.useState(v);g.useEffect(()=>y(v),[v]);const b=n?"a":a?"button":"span",k=cC(h);return f.jsxs(b,N(D({className:sl({primary:i==="primary",secondary:i==="secondary",disabled:s,fullWidth:d,[p]:!0}),onClick:_=>{o&&(y(!0),Promise.resolve(o(_)).then(()=>{y(!1)}))},type:a,disabled:s||m,tabIndex:l,target:c?"_blank":void 0,rel:c?"noreferrer":void 0,href:n},k),{children:[u&&f.jsx("div",{className:sl("icon"),children:u}),r,m&&f.jsx("div",{className:sl("spinner"),children:f.jsx(pn,{size:14})})]}))};z();z();var mn={InputWrapper:"_InputWrapper_qyenz_1","Input-label":"_Input-label_qyenz_5","Input-labelIcon":"_Input-labelIcon_qyenz_17","Input-disabledIcon":"_Input-disabledIcon_qyenz_24","Input-input":"_Input-input_qyenz_29","Input-select":"_Input-select_qyenz_61","Input-selectIcon":"_Input-selectIcon_qyenz_71",Input:"_Input_qyenz_1","Input--readOnly":"_Input--readOnly_qyenz_111","Input-radioGroupItems":"_Input-radioGroupItems_qyenz_150","Input-radio":"_Input-radio_qyenz_150","Input-radioInner":"_Input-radioInner_qyenz_179","Input-radioInput":"_Input-radioInput_qyenz_261"},Ca=ee("Input",mn),z_=({children:e,icon:t,label:r,el:n="label",readOnly:o,className:i})=>{const a=n,s=J("field-readonly");return f.jsxs(a,{className:i,children:[f.jsxs("div",{className:Ca("label"),children:[t?f.jsx("div",{className:Ca("labelIcon"),children:t}):f.jsx(f.Fragment,{}),r,o&&f.jsx("div",{className:Ca("disabledIcon"),title:s,children:f.jsx(V1,{size:"12"})})]}),e]})},uC=({children:e,icon:t,label:r,el:n="label",readOnly:o})=>{const i=H(s=>s.overrides),a=g.useMemo(()=>i.fieldLabel||z_,[i]);return r?f.jsx(a,{label:r,icon:t,className:Ca({readOnly:o}),readOnly:o,el:n,children:e}):f.jsx(f.Fragment,{children:e})};z();z();z();z();var A_={ArrayField:"_ArrayField_62huh_5","ArrayField--isDraggingFrom":"_ArrayField--isDraggingFrom_62huh_30","ArrayField-addButton":"_ArrayField-addButton_62huh_38","ArrayField--hasItems":"_ArrayField--hasItems_62huh_58","ArrayField-inner":"_ArrayField-inner_62huh_93",ArrayFieldItem:"_ArrayFieldItem_62huh_101","ArrayFieldItem--isDragging":"_ArrayFieldItem--isDragging_62huh_110","ArrayFieldItem--isExpanded":"_ArrayFieldItem--isExpanded_62huh_114","ArrayFieldItem-summary":"_ArrayFieldItem-summary_62huh_132","ArrayFieldItem--noFields":"_ArrayFieldItem--noFields_62huh_167","ArrayField--addDisabled":"_ArrayField--addDisabled_62huh_176","ArrayFieldItem-body":"_ArrayFieldItem-body_62huh_228","ArrayFieldItem-fieldset":"_ArrayFieldItem-fieldset_62huh_237","ArrayFieldItem-rhs":"_ArrayFieldItem-rhs_62huh_250","ArrayFieldItem-actions":"_ArrayFieldItem-actions_62huh_256"};z();z();function Zt(e,t){const r=g.useContext(e);if(!r)throw new Error("useContextStore must be used inside context");return ts(r,Be(t))}function dC(e){return({children:r,value:n})=>{const[o]=g.useState(()=>$r(()=>n));return f.jsx(e.Provider,{value:o,children:r})}}function pC(e){const t=g.createContext($r($c(()=>e)));return{ctx:t,Provider:dC(t)}}var Ti=pC({}),Es=()=>g.useContext(Ti.ctx);function md(e){const t=g.useContext(Ti.ctx);if(!t)throw new Error("useContextStore must be used inside context");return ts(t,Be(e))}z();z();var fC={DragIcon:"_DragIcon_5e515_1","DragIcon--disabled":"_DragIcon--disabled_5e515_10"},hC=ee("DragIcon",fC),j_=({isDragDisabled:e})=>f.jsx("div",{className:hC({disabled:e}),children:f.jsx("svg",{viewBox:"0 0 20 20",width:"12",fill:"currentColor",children:f.jsx("path",{d:"M7 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 2zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 14zm6-8a2 2 0 1 0-.001-4.001A2 2 0 0 0 13 6zm0 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 14z"})})});z();z();var{Delay:O_,Distance:vC}=or,gf=[new O_({value:200,tolerance:10})],mf=[new O_({value:200,tolerance:10}),new vC({value:5})],_d=({other:e=mf,mouse:t,touch:r=gf}={touch:gf,other:mf})=>{const[n]=g.useState(()=>[Wm.configure({activationConstraints(o,i){var a;const{pointerType:s,target:l}=o;return s==="mouse"&&Lr(l)&&(i.handle===l||(a=i.handle)!=null&&a.contains(l))?t:s==="touch"?r:e}})]);return n};z();z();z();var $n=(e,t,r,n,o)=>{},ll="increasing",gC=(e,t)=>{var r;const{dragOperation:n,droppable:o}=e,{shape:i}=o,{position:a}=n,s=(r=n.shape)==null?void 0:r.current;if(!s||!i)return null;const l=i.center,c=Math.sqrt(Math.pow(l.x-t.x,2)+Math.pow(l.y-t.y,2)),d=Math.sqrt(Math.pow(l.x-a.current.x,2)+Math.pow(l.y-a.current.y,2));return ll=d===c?ll:d<c?"decreasing":"increasing",$n(s.center,l,o.id.toString()),ll==="decreasing"?{id:o.id,value:1,type:Jt.Collision}:null};z();var D_=(e,t)=>e==="dynamic"?Math.abs(t.y)>Math.abs(t.x)?t.y===0?null:t.y>0?"down":"up":t.x===0?null:t.x>0?"right":"left":e==="x"?t.x===0?null:t.x>0?"right":"left":t.y===0?null:t.y>0?"down":"up";z();var mC=(e,t,r,n=0)=>{const o=e.boundingRectangle,i=t.center;if(r==="down"){const s=n*t.boundingRectangle.height;return o.bottom>=i.y+s}else if(r==="up"){const s=n*t.boundingRectangle.height;return o.top<i.y-s}else if(r==="left"){const s=n*t.boundingRectangle.width;return i.x-s>=o.left}const a=n*t.boundingRectangle.width;return o.right-a>=i.x};z();var _f=10,At={current:{x:0,y:0},delta:{x:0,y:0},previous:{x:0,y:0},direction:null},_C=(e,t="dynamic")=>(At.current=e,At.delta={x:e.x-At.previous.x,y:e.y-At.previous.y},At.direction=D_(t,At.delta)||At.direction,(Math.abs(At.delta.x)>_f||Math.abs(At.delta.y)>_f)&&(At.previous=Qe.from(e)),At);z();var T_=({dragOperation:e,droppable:t})=>{const r=e.position.current;if(!r)return null;const{id:n}=t;if(!t.shape)return null;if(t.shape.containsPoint(r)){const o=Qe.distance(t.shape.center,r);return{id:n,value:1/o,type:Jt.PointerIntersection,priority:kt.High}}return null},yC=e=>{const{dragOperation:t,droppable:r}=e,{shape:n,position:o}=t;if(!r.shape)return null;const i=n?It.from(n.current.boundingRectangle).corners:void 0,s=It.from(r.shape.boundingRectangle).corners.reduce((l,c,d)=>{var u;return l+Qe.distance(Qe.from(c),(u=i==null?void 0:i[d])!=null?u:o.current)},0)/4;return{id:r.id,value:1/s,type:Jt.Collision,priority:kt.Normal}};z();var wc=$r(()=>({fallbackEnabled:!1})),cl="",yd=(e,t=.05)=>(r=>{var n,o,i,a,s;const{dragOperation:l,droppable:c}=r,{position:d}=l,u=(n=l.shape)==null?void 0:n.current,{shape:p}=c;if(!u||!p)return null;const{center:v}=u,{fallbackEnabled:h}=wc.getState(),m=_C(d.current,e),y={direction:m.direction},{center:b}=p,k=mC(u,p,m.direction,t);if(((o=l.source)==null?void 0:o.id)===c.id){const I=gC(r,m.previous);if($n(v,b,c.id.toString()),I)return N(D({},I),{priority:kt.Highest,data:y})}const x=u.intersectionArea(p),_=x/p.area;if(x&&k){$n(v,b,c.id.toString());const I={id:c.id,value:_,priority:kt.High,type:Jt.Collision},w=cl===c.id;return cl="",N(D({},I),{id:w?"flush":I.id,data:y})}if(h&&((i=l.source)==null?void 0:i.id)!==c.id){const I=p.boundingRectangle.right>u.boundingRectangle.left&&p.boundingRectangle.left<u.boundingRectangle.right,w=p.boundingRectangle.bottom>u.boundingRectangle.top&&p.boundingRectangle.top<u.boundingRectangle.bottom;if(e==="y"&&I||w){const A=yC(r);if(A){const E=D_(e,{x:u.center.x-(((a=c.shape)==null?void 0:a.center.x)||0),y:u.center.y-(((s=c.shape)==null?void 0:s.center.y)||0)});return y.direction=E,x?($n(v,b,c.id.toString()),cl=c.id,N(D({},A),{priority:kt.Low,data:y})):($n(v,b,c.id.toString()),N(D({},A),{priority:kt.Lowest,data:y}))}}}return $n(v,b,c.id.toString()),null});z();var bd=(e,t="ltr")=>e==="up"||t==="ltr"&&e==="left"||t==="rtl"&&e==="right"?"before":"after",xd=({position:e,sourceIndex:t,targetIndex:r,isSameZone:n})=>{let o=r;return n&&o>=t&&(o=o-1),e==="after"&&(o=o+1),o},bC=({children:e,onDragStart:t,onDragEnd:r,onMove:n})=>{const o=_d({mouse:[new or.Distance({value:5})]});return f.jsx(ld,{sensors:o,onDragStart:i=>{var a,s;return t((s=(a=i.operation.source)==null?void 0:a.id.toString())!=null?s:"")},onDragOver:(i,a)=>{var s;i.preventDefault();const{operation:l}=i,{source:c,target:d}=l;if(!c||!d)return;const u=c.data.index,p=d.data.index,v=(s=a.collisionObserver.collisions[0])==null?void 0:s.data;u!==p&&c.id!==d.id&&n({source:u,target:xd({position:bd(v==null?void 0:v.direction),sourceIndex:u,targetIndex:p,isSameZone:!0})})},onDragEnd:()=>{setTimeout(()=>{r()},250)},children:e})},xC=({id:e,index:t,disabled:r,children:n,type:o="item"})=>{const{ref:i,isDragging:a,isDropping:s,handleRef:l}=vd({id:e,type:o,index:t,disabled:r,data:{index:t},collisionDetector:yd("y")});return n({isDragging:a,isDropping:s,ref:i,handleRef:l})};z();var Ga=g.createContext({}),kd=()=>{const e=g.useContext(Ga);return N(D({},e),{readOnlyFields:e.readOnlyFields||{}})},kC=({children:e,name:t,subName:r,wildcardName:n=t,readOnlyFields:o})=>{const i=`${t}.${r}`,a=`${n}.${r}`,s=g.useMemo(()=>Object.keys(o).reduce((l,c)=>{if(c.indexOf(i)>-1||c.indexOf(a)>-1){const u=new RegExp(`^(${t}|${n}).`.replace(/\[/g,"\\[").replace(/\]/g,"\\]").replace(/\./g,"\\.").replace(/\*/g,"\\*")),p=c.replace(u,"");return N(D({},l),{[p]:o[c]})}return l},{}),[t,r,n,o]);return f.jsx(Ga.Provider,{value:{readOnlyFields:s,localName:r},children:e})};z();var Is=(e,t)=>t.split(".").reduce((n,o)=>{if(!n)return;const[i,a]=o.replace("]","").split("["),s=n[i];return a&&s?s[parseInt(a)]:s},e);z();var wC=({field:e,id:t,index:r,name:n,subName:o,localName:i,onChange:a,forceReadOnly:s})=>{const l=typeof r<"u"?`${n}[${r}]`:n,c=n?`${l}.${o}`:o,d=typeof r<"u"?`${i}[${r}]`:i??o,u=typeof r<"u"?`${i}[*]`:i,p=`${d}.${o}`,v=`${u}.${o}`,{readOnlyFields:h}=kd(),m=s||(typeof h[c]<"u"?h[p]:h[v]),y=e.label||o;return f.jsx(kC,{name:d,wildcardName:u,subName:o,readOnlyFields:h,children:f.jsx(F_,{name:c,label:y,id:t,readOnly:m,field:N(D({},e),{label:y}),onChange:(b,k)=>{a(b,k,o)}})})},M_=g.memo(wC),ul=ee("ArrayField",A_),Sr=ee("ArrayFieldItem",A_),SC=({index:e,originalIndex:t,field:r,name:n})=>{const o=md(s=>{const l=`${[n]}[${e}]`;return Is(s,l)}),i=J("field-arrayitem-summary",{index:t});return g.useMemo(()=>o&&r.getItemSummary?r.getItemSummary(o,e):i,[o,r,t,e,i])},EC=g.memo(SC),IC=({id:e,arrayId:t,index:r,dragIndex:n,originalIndex:o,field:i,onChange:a,onToggleExpand:s,readOnly:l,actions:c,name:d,localName:u})=>{const p=H(m=>{var y;return((y=m.state.ui.arrayState[t])==null?void 0:y.openId)===e}),v=H(m=>m.permissions.getPermissions({item:m.selectedItem}).edit),h=g.useMemo(()=>i.arrayFields?Object.values(i.arrayFields).some(m=>m.type!=="slot"&&m.visible!==!1):!1,[i.arrayFields]);return f.jsx(xC,{id:e,index:n,disabled:l,children:({isDragging:m,ref:y,handleRef:b})=>f.jsxs("div",{ref:y,className:Sr({isExpanded:p&&h,isDragging:m,noFields:!h}),children:[f.jsxs("div",{ref:b,onClick:k=>{m||(k.preventDefault(),k.stopPropagation(),h&&s(e,p))},className:Sr("summary"),children:[f.jsx(EC,{index:r,originalIndex:o,field:i,name:d}),f.jsxs("div",{className:Sr("rhs"),children:[!l&&f.jsx("div",{className:Sr("actions"),children:c}),f.jsx("div",{children:f.jsx(j_,{})})]})]}),f.jsx("div",{className:Sr("body"),children:p&&h&&f.jsx("fieldset",{className:Sr("fieldset"),children:Object.keys(i.arrayFields).map(k=>{const x=i.arrayFields[k];return f.jsx(M_,{id:`${e}_${k}`,name:d,index:r,subName:k,localName:u,field:x,onChange:a,forceReadOnly:!v},`${e}_${k}_${r}`)})})})]})})},CC=g.memo(IC),PC=({field:e,onChange:t,id:r,name:n=r,label:o,labelIcon:i,readOnly:a,Label:s=l=>f.jsx("div",D({},l))})=>{const l=H(F=>F.setUi),c=ye(),d=Es(),{localName:u=n}=kd(),p=()=>{var F;return(F=Is(d.getState(),n))!=null?F:[]},v=g.useCallback(()=>{var F;const{state:M}=c.getState(),q=M.ui.arrayState[r];if((F=q==null?void 0:q.items)!=null&&F.length)return q;const W=p();return{items:Array.from(W||[]).map((B,Z)=>({_originalIndex:Z,_currentIndex:Z,_arrayId:`${r}-${Z}`})),openId:""}},[c,r,p,n]),h=md(()=>p().length),m=g.useMemo(v,[v]),y=H(F=>{const M=F.state.ui.arrayState[r];return M??m}),b=ye(),k=g.useCallback(F=>{const M=b.getState().state;return{arrayState:N(D({},M.ui.arrayState),{[r]:D(D({},v()),F)})}},[b]),x=g.useCallback(()=>v().items.reduce((F,M)=>M._originalIndex>F?M._originalIndex:F,-1),[]),_=g.useCallback(F=>{let M=x();const q=v(),W=Array.from(F||[]).map((B,Z)=>{var oe,K,te;const be=q.items[Z],Q={_originalIndex:(oe=be==null?void 0:be._originalIndex)!=null?oe:M+1,_currentIndex:(K=be==null?void 0:be._currentIndex)!=null?K:Z,_arrayId:((te=q.items[Z])==null?void 0:te._arrayId)||`${r}-${M+1}`};return Q._originalIndex>M&&(M=Q._originalIndex),Q});return N(D({},q),{items:W})},[]),[I,w]=g.useState(""),A=!!I,E=g.useRef([]);g.useEffect(()=>{E.current=p()},[]);const C=g.useCallback(F=>{if(e.type!=="array"||!e.arrayFields)return;const M=b.getState().config;return Fc({value:F,fields:e.arrayFields,mappers:{slot:({value:q})=>q.map(B=>Nc(B,M,!0))},config:M})},[b,e]),S=g.useCallback(()=>{const F=v(),M=F.items.map((B,Z)=>N(D({},B),{_currentIndex:Z})),q=b.getState().state,W={arrayState:N(D({},q.ui.arrayState),{[r]:N(D({},F),{items:M})})};l(W,!1)},[]),j=g.useCallback(F=>{const M=_(F);l(k(M),!1),t(F)},[_,l,k,t]);g.useEffect(()=>{const F=_(p());l(k(F),!1)},[h]);const O=J("field-arrayitem-duplicate"),L=J("field-arrayitem-delete");if(e.type!=="array"||!e.arrayFields)return null;const $=e.max!==void 0&&(y==null?void 0:y.items.length)>=e.max||a;return f.jsx(s,{label:o||n,icon:i||f.jsx(us,{size:16}),el:"div",readOnly:a,children:f.jsx(bC,{onDragStart:F=>{E.current=p(),w(F),S()},onDragEnd:()=>{w(""),t(E.current);const F=d.getState();d.setState(Ss(F,n,E.current)),S()},onMove:F=>{const M=v();if(M.items[F.source]._arrayId!==I)return;const q=wp(E.current,F.source,F.target),W=wp(M.items,F.source,F.target),B=b.getState().state,Z={arrayState:N(D({},B.ui.arrayState),{[r]:N(D({},M),{items:W})})};l(Z,!1),E.current=q},children:f.jsxs("div",{className:ul({hasItems:h>0,addDisabled:$}),children:[y.items.length>0&&f.jsx("div",{className:ul("inner"),"data-dnd-container":!0,children:y.items.map((F,M)=>{const{_arrayId:q=`${r}-${M}`,_originalIndex:W=M,_currentIndex:B=M}=F;return f.jsx(CC,{index:B,dragIndex:M,originalIndex:W,arrayId:r,id:q,readOnly:a,field:e,name:n,localName:u,onChange:(Z,oe,K)=>{const te=p(),be=Array.from(te||[])[M]||{};t(Sw(te,M,N(D({},be),{[K]:Z})),oe)},onToggleExpand:(Z,oe)=>{l(k(oe?{openId:""}:{openId:Z}))},actions:f.jsxs(f.Fragment,{children:[f.jsx("div",{className:Sr("action"),children:f.jsx(Ke,{type:"button",disabled:!!$,onClick:Z=>{Z.stopPropagation();const K=[...p()||[]],te=C(K[M]);K.splice(M,0,te),j(K)},title:O,children:f.jsx(iu,{size:16})})}),f.jsx("div",{className:Sr("action"),children:f.jsx(Ke,{type:"button",disabled:e.min!==void 0&&e.min>=y.items.length,onClick:Z=>{Z.stopPropagation();const K=[...p()||[]];K.splice(M,1),j(K)},title:L,children:f.jsx(au,{size:16})})})]})},q)})}),!$&&f.jsx("button",{type:"button",className:ul("addButton"),onClick:()=>{var F;if(A)return;const q=p()||[],W=typeof e.defaultItemProps=="function"?e.defaultItemProps(q.length):(F=e.defaultItemProps)!=null?F:{},B=eh(C(W),e.arrayFields),Z=[...q,B];j(Z)},children:f.jsx(X1,{size:21})})]})})})};z();z();z();var Mi=(e,t=!0)=>md(r=>t?Is(r,e):void 0);z();var zC=e=>H(t=>t.state.ui.field.focus===e),wd=(e,t,{tracked:r=!0,fallback:n}={})=>{const o=Mi(e,r),i=zC(e),[a,s]=g.useState(o),l=g.useCallback((c,...d)=>{s(c),t(c,...d)},[t]);return g.useEffect(()=>{r&&(i||s(o))},[r,i,o]),r?[typeof n<"u"&&a==null?n:a,l]:[void 0,t]},AC=ee("Input",mn),yf=({field:e,onChange:t,readOnly:r,id:n,name:o=n,label:i,labelIcon:a,Label:s})=>{const[l,c]=wd(o,t,{fallback:""});return f.jsx(s,{label:i||o,icon:a||f.jsxs(f.Fragment,{children:[e.type==="text"&&f.jsx(ds,{size:16}),e.type==="number"&&f.jsx(T1,{size:16})]}),readOnly:r,children:f.jsx("input",{className:AC("input"),autoComplete:"off",type:e.type,title:i||o,name:o,value:l,onChange:d=>{if(e.type==="number"){const u=Number(d.currentTarget.value);if(typeof e.min<"u"&&u<e.min||typeof e.max<"u"&&u>e.max)return;c(u)}else c(d.currentTarget.value)},readOnly:r,tabIndex:r?-1:void 0,id:n,min:e.type==="number"?e.min:void 0,max:e.type==="number"?e.max:void 0,placeholder:e.type==="text"||e.type==="number"?e.placeholder:void 0,step:e.type==="number"?e.step:void 0})})};z();z();z();var R_={"ExternalInput-actions":"_ExternalInput-actions_143vl_1","ExternalInput-button":"_ExternalInput-button_143vl_5","ExternalInput--dataSelected":"_ExternalInput--dataSelected_143vl_34","ExternalInput--readOnly":"_ExternalInput--readOnly_143vl_41","ExternalInput-detachButton":"_ExternalInput-detachButton_143vl_48",ExternalInput:"_ExternalInput_143vl_1",ExternalInputModal:"_ExternalInputModal_143vl_118","ExternalInputModal-grid":"_ExternalInputModal-grid_143vl_128","ExternalInputModal--filtersToggled":"_ExternalInputModal--filtersToggled_143vl_139","ExternalInputModal-filters":"_ExternalInputModal-filters_143vl_144","ExternalInputModal-masthead":"_ExternalInputModal-masthead_143vl_164","ExternalInputModal-tableWrapper":"_ExternalInputModal-tableWrapper_143vl_173","ExternalInputModal-table":"_ExternalInputModal-table_143vl_173","ExternalInputModal-thead":"_ExternalInputModal-thead_143vl_189","ExternalInputModal-th":"_ExternalInputModal-th_143vl_189","ExternalInputModal-td":"_ExternalInputModal-td_143vl_204","ExternalInputModal-tr":"_ExternalInputModal-tr_143vl_210","ExternalInputModal-tbody":"_ExternalInputModal-tbody_143vl_217","ExternalInputModal--hasData":"_ExternalInputModal--hasData_143vl_244","ExternalInputModal-loadingBanner":"_ExternalInputModal-loadingBanner_143vl_248","ExternalInputModal--isLoading":"_ExternalInputModal--isLoading_143vl_265","ExternalInputModal-searchForm":"_ExternalInputModal-searchForm_143vl_269","ExternalInputModal-search":"_ExternalInputModal-search_143vl_269","ExternalInputModal-searchIcon":"_ExternalInputModal-searchIcon_143vl_306","ExternalInputModal-searchIconText":"_ExternalInputModal-searchIconText_143vl_333","ExternalInputModal-searchInput":"_ExternalInputModal-searchInput_143vl_343","ExternalInputModal-searchActions":"_ExternalInputModal-searchActions_143vl_358","ExternalInputModal-searchActionIcon":"_ExternalInputModal-searchActionIcon_143vl_371","ExternalInputModal-footerContainer":"_ExternalInputModal-footerContainer_143vl_375","ExternalInputModal-footer":"_ExternalInputModal-footer_143vl_375","ExternalInputModal-field":"_ExternalInputModal-field_143vl_388"};z();z();var jC={Modal:"_Modal_g5xob_1","Modal--isOpen":"_Modal--isOpen_g5xob_15","Modal-inner":"_Modal-inner_g5xob_19"},bf=ee("Modal",jC),OC=({children:e,onClose:t,isOpen:r})=>{const[n,o]=g.useState(null);return g.useEffect(()=>{o(document.getElementById("puck-portal-root"))},[]),n?pr.createPortal(f.jsx("div",{className:bf({isOpen:r}),onClick:t,children:f.jsx("div",{className:bf("inner"),onClick:i=>i.stopPropagation(),children:e})}),n):f.jsx("div",{})};z();z();var DC={Heading:"_Heading_97eh4_1","Heading--xxxxl":"_Heading--xxxxl_97eh4_12","Heading--xxxl":"_Heading--xxxl_97eh4_18","Heading--xxl":"_Heading--xxl_97eh4_22","Heading--xl":"_Heading--xl_97eh4_26","Heading--l":"_Heading--l_97eh4_30","Heading--m":"_Heading--m_97eh4_34","Heading--s":"_Heading--s_97eh4_38","Heading--xs":"_Heading--xs_97eh4_42"},TC=ee("Heading",DC),Cs=({children:e,rank:t,size:r="m"})=>{const n=t?`h${t}`:"span";return f.jsx(n,{className:TC({[r]:!0}),children:e})};z();var aa=ee("ExternalInput",R_),Pe=ee("ExternalInputModal",R_),MC=({count:e})=>{const t=J("field-external-result-singular",{count:e}),r=J("field-external-result-plural",{count:e});return f.jsx("span",{className:Pe("footer"),children:e===1?t:r})},dl={},RC=({field:e,onChange:t,value:r=null,name:n,id:o,readOnly:i})=>{var a;const{mapProp:s=M=>M,mapRow:l=M=>M,filterFields:c}=e||{},{enabled:d}=(a=e.cache)!=null?a:{enabled:!0},[u,p]=g.useState([]),[v,h]=g.useState(!1),[m,y]=g.useState(!0),b=!!c,[k,x]=g.useState(e.initialFilters||{}),[_,I]=g.useState(b),w=g.useMemo(()=>u.map(l),[u]),A=g.useMemo(()=>{const M=new Set;for(const q of w)for(const W of Object.keys(q))(typeof q[W]=="string"||typeof q[W]=="number"||g.isValidElement(q[W]))&&M.add(W);return Array.from(M)},[w]),[E,C]=g.useState(e.initialQuery||""),S=g.useCallback((M,q)=>Se(null,null,function*(){y(!0);const W=`${o}-${M}-${JSON.stringify(q)}`;let B;d&&dl[W]?B=dl[W]:B=yield e.fetchList({query:M,filters:q}),B&&(p(B),y(!1),d&&(dl[W]=B))}),[o,e]),j=g.useCallback(M=>e.renderFooter?e.renderFooter(M):f.jsx(MC,{count:M.items.length}),[e.renderFooter]);g.useEffect(()=>{S(E,k)},[]);const O=J("field-external-item"),L=J("field-external-search"),$=J("field-external-togglefilters"),F=J("field-external-selectdata");return f.jsxs("div",{className:aa({dataSelected:!!r,modalVisible:v,readOnly:i}),id:o,children:[f.jsxs("div",{className:aa("actions"),children:[f.jsx("button",{type:"button",onClick:()=>h(!0),className:aa("button"),disabled:i,children:r?e.getItemSummary?e.getItemSummary(r):O:f.jsxs(f.Fragment,{children:[f.jsx(Iv,{size:"16"}),f.jsx("span",{children:e.placeholder})]})}),r&&f.jsx("button",{type:"button",className:aa("detachButton"),onClick:()=>{t(null)},disabled:i,children:f.jsx(H1,{size:16})})]}),f.jsx(OC,{onClose:()=>h(!1),isOpen:v,children:f.jsxs("form",{className:Pe({isLoading:m,loaded:!m,hasData:w.length>0,filtersToggled:_}),onSubmit:M=>{M.preventDefault(),M.stopPropagation(),S(E,k)},children:[f.jsx("div",{className:Pe("masthead"),children:e.showSearch?f.jsxs("div",{className:Pe("searchForm"),children:[f.jsxs("label",{className:Pe("search"),children:[f.jsx("span",{className:Pe("searchIconText"),children:L}),f.jsx("div",{className:Pe("searchIcon"),children:f.jsx(ew,{size:"18"})}),f.jsx("input",{className:Pe("searchInput"),name:"q",type:"search",placeholder:e.placeholder,onChange:M=>{C(M.currentTarget.value)},autoComplete:"off",value:E})]}),f.jsxs("div",{className:Pe("searchActions"),children:[f.jsx(kc,{type:"submit",loading:m,fullWidth:!0,children:L}),b&&f.jsx("div",{className:Pe("searchActionIcon"),children:f.jsx(Ke,{type:"button",title:$,onClick:M=>{M.preventDefault(),M.stopPropagation(),I(!_)},children:f.jsx(tw,{size:20})})})]})]}):f.jsx(Cs,{rank:"2",size:"xs",children:e.placeholder||F})}),f.jsxs("div",{className:Pe("grid"),children:[b&&f.jsx("div",{className:Pe("filters"),children:b&&Object.keys(c).map(M=>{const q=c[M];return f.jsx("div",{className:Pe("field"),children:f.jsx(z_,{label:q.label||M,children:f.jsx(KC,{field:q,id:`external_field_${M}_filter`,value:k[M],onChange:W=>{x(B=>{const Z=N(D({},B),{[M]:W});return S(E,Z),Z})}})})},M)})}),f.jsxs("div",{className:Pe("tableWrapper"),children:[f.jsxs("table",{className:Pe("table"),children:[f.jsx("thead",{className:Pe("thead"),children:f.jsx("tr",{className:Pe("tr"),children:A.map(M=>f.jsx("th",{className:Pe("th"),style:{textAlign:"left"},children:M},M))})}),f.jsx("tbody",{className:Pe("tbody"),children:w.map((M,q)=>f.jsx("tr",{style:{whiteSpace:"nowrap"},className:Pe("tr"),onClick:()=>{t(s(u[q])),h(!1)},children:A.map(W=>f.jsx("td",{className:Pe("td"),children:M[W]},W))},q))})]}),f.jsx("div",{className:Pe("loadingBanner"),children:f.jsx(pn,{size:24})})]})]}),f.jsx("div",{className:Pe("footerContainer"),children:f.jsx(j,{items:w})})]})})]})},LC=({field:e,onChange:t,id:r,name:n=r,label:o,labelIcon:i,Label:a,readOnly:s})=>{var l,c,d;const u=Mi(n),p=e,v=e,h=J("field-external-selectdata");return g.useEffect(()=>{v.adaptor&&console.error("Warning: The `adaptor` API is deprecated. Please use updated APIs on the `external` field instead. This will be a breaking change in a future release.")},[]),e.type!=="external"?null:f.jsx(a,{label:o||n,icon:i||f.jsx(Iv,{size:16}),el:"div",children:f.jsx(RC,{name:n,field:N(D({},p),{placeholder:(l=v.adaptor)!=null&&l.name?`Select from ${v.adaptor.name}`:p.placeholder||h,mapProp:((c=v.adaptor)==null?void 0:c.mapProp)||p.mapProp,mapRow:p.mapRow,fetchList:(d=v.adaptor)!=null&&d.fetchList?()=>Se(null,null,function*(){return yield v.adaptor.fetchList(v.adaptorParams)}):p.fetchList}),onChange:t,value:u,id:r,readOnly:s})})};z();var sa=ee("Input",mn),FC=({field:e,onChange:t,readOnly:r,id:n,name:o=n,label:i,labelIcon:a,Label:s})=>{const l=Mi(o);return e.type!=="radio"||!e.options?null:f.jsx(s,{icon:a||f.jsx(P1,{size:16}),label:i||o,readOnly:r,el:"div",children:f.jsx("div",{className:sa("radioGroupItems"),id:n,children:e.options.map(c=>{var d;return f.jsxs("label",{className:sa("radio"),children:[f.jsx("input",{type:"radio",className:sa("radioInput"),value:JSON.stringify({value:c.value}),name:o,onChange:u=>{t(JSON.parse(u.target.value).value)},disabled:r,checked:l===c.value}),f.jsx("div",{className:sa("radioInner"),children:c.label||((d=c.value)==null?void 0:d.toString())})]},c.label+c.value)})})})};z();var pl=ee("Input",mn),NC=({field:e,onChange:t,label:r,labelIcon:n,Label:o,id:i,name:a=i,readOnly:s})=>{const l=Mi(a);return e.type!=="select"||!e.options?null:f.jsx(o,{label:r||a,icon:n||f.jsx(ci,{size:16}),readOnly:s,children:f.jsxs("div",{className:pl("select"),children:[f.jsx("select",{id:i,title:r||a,className:pl("input"),disabled:s,onChange:c=>{t(JSON.parse(c.target.value).value)},value:JSON.stringify({value:l}),children:e.options.map(c=>f.jsx("option",{label:c.label,value:JSON.stringify({value:c.value})},c.label+JSON.stringify(c.value)))}),f.jsx(ci,{size:18,className:pl("selectIcon")})]})})};z();var BC=ee("Input",mn),$C=({field:e,onChange:t,readOnly:r,id:n,name:o=n,label:i,labelIcon:a,Label:s})=>{const[l,c]=wd(o,t,{fallback:""});return f.jsx(s,{label:i||o,icon:a||f.jsx(ds,{size:16}),readOnly:r,children:f.jsx("textarea",{id:n,className:BC("input"),autoComplete:"off",name:o,value:l,onChange:d=>c(d.currentTarget.value),readOnly:r,tabIndex:r?-1:void 0,rows:5,placeholder:e.type==="textarea"?e.placeholder:void 0})})};z();z();var Sd=g.memo(e=>{var t;return f.jsx(Wv,N(D({},e),{editor:null,menu:f.jsx($v,{field:e.field,editor:null,editorState:null,readOnly:(t=e.readOnly)!=null?t:!1}),children:f.jsx("div",{className:"rich-text",dangerouslySetInnerHTML:{__html:e.content},contentEditable:!0})}))});Sd.displayName="EditorFallback";var WC=g.lazy(()=>Nr(()=>import("./chunks/Editor-44C53YAG-FHX0eoLj.js"),__vite__mapDeps([9,8,3,2,1])).then(e=>({default:e.Editor}))),HC=({onChange:e,readOnly:t=!1,id:r,name:n=r,label:o,labelIcon:i,Label:a,field:s})=>{const l=Mi(n),c={onChange:e,content:l,readOnly:t,field:s,id:r,name:n};return f.jsx(f.Fragment,{children:f.jsx(a,{label:o||n,icon:i||f.jsx(ds,{size:16}),readOnly:t,el:"div",children:f.jsx(g.Suspense,{fallback:f.jsx(Sd,D({},c)),children:f.jsx(WC,D({},c))})})})};z();z();var VC={ObjectField:"_ObjectField_c5reb_1","ObjectField-fieldset":"_ObjectField-fieldset_c5reb_10"},xf=ee("ObjectField",VC),qC=({field:e,onChange:t,id:r,name:n=r,label:o,labelIcon:i,Label:a,readOnly:s})=>{const{localName:l=n}=kd(),c=Es(),d=H(p=>p.permissions.getPermissions({item:p.selectedItem}).edit),u=()=>{var p;return(p=Is(c.getState(),n))!=null?p:{}};return e.type!=="object"||!e.objectFields?null:f.jsx(a,{label:o||n,icon:i||f.jsx(j1,{size:16}),el:"div",readOnly:s,children:f.jsx("div",{className:xf(),children:f.jsx("fieldset",{className:xf("fieldset"),children:Object.keys(e.objectFields).map(p=>{const v=e.objectFields[p],h=`${l}.${p}`;return f.jsx(M_,{id:`${r}_${p}`,name:n,subName:p,localName:l,field:v,forceReadOnly:!d,onChange:(m,y,b)=>{const k=u();k[b]!==m&&t(N(D({},k),{[b]:m}),y)}},h)})})})})};z();var Ps=()=>{if(typeof Er.useId<"u")return Er.useId();const[e]=g.useState(dt());return e},UC=ee("Input",mn),ZC=ee("InputWrapper",mn),Bt={array:PC,external:LC,object:qC,select:NC,textarea:$C,radio:FC,text:yf,number:yf,richtext:HC};function L_(e){var t,r,n;const o=H(L=>L.dispatch),i=H(L=>L.overrides),a=H(Be(L=>{var $;return($=L.selectedItem)==null?void 0:$.readOnly})),s=g.useContext(Ga),{id:l,Label:c=uC}=e,d=e.field,u=d.label,p=d.labelIcon,v=Ps(),h=l||v,m=g.useMemo(()=>{var L,$,F,M,q,W,B,Z,oe,K;return N(D({},i.fieldTypes),{custom:(L=i.fieldTypes)==null?void 0:L.custom,array:(($=i.fieldTypes)==null?void 0:$.array)||Bt.array,external:((F=i.fieldTypes)==null?void 0:F.external)||Bt.external,object:((M=i.fieldTypes)==null?void 0:M.object)||Bt.object,select:((q=i.fieldTypes)==null?void 0:q.select)||Bt.select,textarea:((W=i.fieldTypes)==null?void 0:W.textarea)||Bt.textarea,radio:((B=i.fieldTypes)==null?void 0:B.radio)||Bt.radio,text:((Z=i.fieldTypes)==null?void 0:Z.text)||Bt.text,number:((oe=i.fieldTypes)==null?void 0:oe.number)||Bt.number,richtext:((K=i.fieldTypes)==null?void 0:K.richtext)||Bt.richtext})},[i]),y=d.type==="custom"||!!((t=i.fieldTypes)!=null&&t[d.type]),b=(r=e.name)!=null?r:h,k=Es(),x=g.useMemo(()=>y?(L,$)=>{var F;(F=e.onChange)==null||F.call(e,L,$),k.setState(Ss(k.getState(),b,L))}:e.onChange,[y,e.onChange,b,k]),[_,I]=wd(b,x,{tracked:y}),w=g.useMemo(()=>N(D({},e),{field:d,label:u,labelIcon:p,Label:c,id:h,value:_,onChange:I}),[e,d,u,p,c,h,_,I]),A=g.useCallback(L=>{w.name&&(L.target.nodeName==="INPUT"||L.target.nodeName==="TEXTAREA")&&(L.stopPropagation(),o({type:"setUi",ui:{field:{focus:w.name}}}))},[w.name]),E=g.useCallback(L=>{"name"in L.target&&o({type:"setUi",ui:{field:{focus:null}}})},[]);let C=g.useMemo(()=>d.type!=="custom"&&d.type!=="slot"?Bt[d.type]:L=>null,[d.type]);const S=d.type==="custom"?d.key:void 0;let j=g.useMemo(()=>{if(d.type==="custom"&&!m[d.type])return d.render?d.render:null;if(d.type!=="slot")return m[d.type]},[d.type,S,m]);const{visible:O=!0}=e.field;if(!O||d.type==="slot")return null;if(!j)throw new Error(`Field type for ${d.type} did not exist.`);return f.jsx(Ga.Provider,{value:{readOnlyFields:s.readOnlyFields||a||{},localName:(n=s.localName)!=null?n:w.name},children:f.jsx("div",{className:ZC(),onFocus:A,onBlur:E,onClick:L=>{L.stopPropagation()},children:f.jsx(j,N(D({},w),{children:f.jsx(C,D({},w))}))})})}function F_(e){return f.jsx(L_,D({},e))}function YC(e){var t=e,{value:r}=t,n=Tt(t,["value"]);const o=g.useMemo(()=>l=>f.jsx("div",N(D({},l),{className:UC({readOnly:n.readOnly})})),[n.readOnly]),i=Es(),a=g.useCallback(s=>{n.id&&(i.setState({[n.id]:s}),n.onChange(s))},[i,n.onChange,n.id]);return g.useEffect(()=>{n.id&&i.setState({[n.id]:r})},[n.id,r,i]),f.jsx(L_,N(D({},n),{onChange:a,Label:o}))}function KC(e){const t=Ps();return e.field.type==="slot"?null:f.jsx(Ti.Provider,{value:{[t]:e.value},children:f.jsx(YC,N(D({},e),{id:t}))})}z();z();z();z();var XC={DraggableComponent:"_DraggableComponent_1627v_1","DraggableComponent-overlayWrapper":"_DraggableComponent-overlayWrapper_1627v_6","DraggableComponent-overlay":"_DraggableComponent-overlay_1627v_6","DraggableComponent-loadingOverlay":"_DraggableComponent-loadingOverlay_1627v_38","DraggableComponent--hover":"_DraggableComponent--hover_1627v_54","DraggableComponent--isSelected":"_DraggableComponent--isSelected_1627v_72","DraggableComponent-actionsOverlay":"_DraggableComponent-actionsOverlay_1627v_89","DraggableComponent-actions":"_DraggableComponent-actions_1627v_89","DraggableComponent-actionsAction":"_DraggableComponent-actionsAction_1627v_111"};z();function kf(e){let t={x:0,y:0},r=e;for(;r&&r!==document.documentElement;){const n=r.parentElement;n&&(t.x+=n.scrollLeft,t.y+=n.scrollTop),r=n}return t}z();var yo=g.createContext(null),He=g.createContext($r(()=>({zoneDepthIndex:{},nextZoneDepthIndex:{},areaDepthIndex:{},nextAreaDepthIndex:{},draggedItem:null,previewIndex:{},enabledIndex:{},hoveringComponent:null,registerRootVirtualizer:()=>{},unregisterRootVirtualizer:()=>{},scrollToComponent:()=>!1}))),GC=({children:e,store:t})=>f.jsx(He.Provider,{value:t,children:e}),yi=({children:e,value:t})=>{const r=H(i=>i.dispatch),n=g.useCallback(i=>{r({type:"registerZone",zone:i})},[r]),o=g.useMemo(()=>D({registerZone:n},t),[t]);return f.jsx(f.Fragment,{children:o&&f.jsx(yo.Provider,{value:o,children:e})})};z();var N_=(e,t=[])=>{const r=ye();return g.useCallback(()=>{let n=()=>{};const o=a=>{a?e(!1):(setTimeout(()=>{e(!0)},0),n&&n())},i=r.getState().state.ui.isDragging;return o(i),i&&(n=r.subscribe(a=>a.state.ui.isDragging,a=>{o(a)})),n},[r,...t])};z();z();z();var gt=()=>{if(typeof window>"u")return;let e=document.querySelector("#preview-frame");return(e==null?void 0:e.tagName)==="IFRAME"?e.contentDocument||document:(e==null?void 0:e.ownerDocument)||document};z();z();var B_=e=>typeof CSS<"u"&&typeof CSS.escape=="function"?CSS.escape(e):e,to=e=>`[data-puck-component="${B_(e)}"]`,bi=e=>`[data-puck-dropzone="${B_(e)}"]`,Ed={duration:250,easing:"ease"},JC=10,Id=e=>{var t,r;return(r=(t=e.defaultView)==null?void 0:t.matchMedia("(prefers-reduced-motion: reduce)").matches)!=null?r:!1},$_=(e,{zones:t,itemId:r,targetZone:n,getExpectedOrder:o,initialExpectedOrder:i=[]},a)=>{const s=new Set(i);let l=0;const c=()=>{var d;const u=e.querySelector(bi(n)),p=o(),v=r??p.find(_=>!s.has(_)),h=v&&(d=u==null?void 0:u.querySelector(`:scope > ${to(v)}:not([data-dnd-dragging]):not([data-dnd-placeholder])`))!=null?d:null,m=u?Array.from(u.querySelectorAll(":scope > [data-puck-component]:not([data-dnd-dragging]):not([data-dnd-placeholder])")).map(_=>_.getAttribute("data-puck-component")):[],y=new Set(m),b=p.filter(_=>y.has(_)),k=m.length===b.length&&m.every((_,I)=>_===b[I]),x=t.every(_=>_===n||!v||!e.querySelector(`${bi(_)} > ${to(v)}`));if((!h||!k||!x)&&l<JC){l++,requestAnimationFrame(c);return}a(h)};requestAnimationFrame(c)},QC=(e,t)=>{var r,n;const o={x:0,y:0,scaleX:1,scaleY:1};let i=(r=e.ownerDocument.defaultView)==null?void 0:r.frameElement;for(;i&&i!==t;){const a=i.getBoundingClientRect(),s=i.offsetWidth?a.width/i.offsetWidth:1,l=i.offsetHeight?a.height/i.offsetHeight:1;o.x+=a.left,o.y+=a.top,o.scaleX*=s,o.scaleY*=l,i=(n=i.ownerDocument.defaultView)==null?void 0:n.frameElement}return o},eP=(e,t)=>{var r,n;const o=e.getBoundingClientRect();if(e.ownerDocument===t)return o;const i=QC(e,(n=(r=t.defaultView)==null?void 0:r.frameElement)!=null?n:null);return{left:o.left*i.scaleX+i.x,top:o.top*i.scaleY+i.y,width:o.width*i.scaleX,height:o.height*i.scaleY}},tP=({element:e,feedbackElement:t,placeholder:r,translate:n})=>{var o;if(Id(t.ownerDocument))return;const i=r??e,s={frameTransform:t.ownerDocument===i.ownerDocument?null:void 0},l=new Et(t,s),c=new Et(i,s),d=(o=Jn(Lt(t).translate))!=null?o:n,u={x:d.x-(l.center.x-c.center.x),y:d.y-(l.center.y-c.center.y)};return t.setAttribute("data-dnd-dropping",""),t.animate({translate:[`${d.x}px ${d.y}px 0`,`${u.x}px ${u.y}px 0`]},Ed).finished.catch(()=>{}).then(()=>{t.removeAttribute("data-dnd-dropping")})},rP=({feedbackElement:e,itemId:t,targetZone:r,getExpectedOrder:n})=>{var o;const i=e.ownerDocument,a=(o=gt())!=null?o:i;if(Id(i))return;const s=e.getBoundingClientRect(),l=n(),c=e.cloneNode(!0);c.removeAttribute("id"),c.removeAttribute("popover"),c.removeAttribute("data-puck-component"),c.removeAttribute("data-puck-dnd"),c.removeAttribute("data-dnd-dragging"),c.setAttribute("inert","true"),Object.assign(c.style,{position:"fixed",left:`${s.left}px`,top:`${s.top}px`,width:`${s.width}px`,height:`${s.height}px`,margin:"0",overflow:"hidden",pointerEvents:"none",transform:"none",transition:"none",translate:"none",zIndex:"2147483647"});const d=a.createElement("style");d.textContent=`
    ${t?`${to(t)} { visibility: hidden !important; }`:""}
    [data-puck-overlay] { opacity: 0 !important; }
  `,a.head.appendChild(d),i.body.appendChild(c);const u=()=>{c.remove(),d.remove()};$_(a,{zones:[r],itemId:t,targetZone:r,getExpectedOrder:n,initialExpectedOrder:l},p=>{if(!p){u();return}const v=p.getAttribute("data-puck-component");!t&&v&&(d.textContent+=`
          ${to(v)} { visibility: hidden !important; }
        `);const h=eP(p,i);c.animate({left:[`${s.left}px`,`${h.left}px`],top:[`${s.top}px`,`${h.top}px`],width:[`${s.width}px`,`${h.width}px`],height:[`${s.height}px`,`${h.height}px`]},N(D({},Ed),{fill:"forwards"})).finished.catch(()=>{}).then(u)})},nP=(e,t)=>{var r,n,o;const i=(r=e.source.manager)==null?void 0:r.dragOperation;if(!(((n=i==null?void 0:i.canceled)!=null?n:!1)||((o=i==null?void 0:i.target)==null?void 0:o.type)==="void")&&t){rP(N(D({},t),{feedbackElement:e.feedbackElement}));return}return tP(e)};z();var Ja=(e,t)=>{var r,n;return(n=(r=e.indexes.zones[t])==null?void 0:r.contentIds)!=null?n:[]},W_=(e,t)=>{const r=ye();return g.useCallback(n=>{var o;const i=Object.values((o=e.getState().previewIndex)!=null?o:{}),a=t?i.find(l=>(l==null?void 0:l.props.id)===t&&!l.ghost):i.find(l=>(l==null?void 0:l.type)==="insert"),s=t?(a==null?void 0:a.linePlaceholder)||(a==null?void 0:a.type)==="insert":!!a;return nP(n,a&&s?{itemId:a.type==="move"?t:void 0,targetZone:a.zone,getExpectedOrder:()=>Ja(r.getState().state,a.zone)}:void 0)},[r,e,t])};z();function oP(e,t){typeof e=="function"?e(t):e&&typeof e=="object"&&"current"in e&&(e.current=t)}function Sc(e,t){e.forEach(r=>{oP(r,t)})}var yr=ee("DraggableComponent",XC),iP=100,H_=8,aP=H_*6.5,sP=-44,wf=H_,lP=({label:e,children:t,parentAction:r})=>f.jsxs(ht,{children:[f.jsxs(ht.Group,{children:[r,e&&f.jsx(ht.Label,{label:e})]}),f.jsx(ht.Group,{children:t})]}),cP=({children:e})=>f.jsx(f.Fragment,{children:e}),uP=({children:e,depth:t,componentType:r,id:n,index:o,zoneCompound:i,isLoading:a=!1,isSelected:s=!1,debug:l,label:c,autoDragAxis:d,userDragAxis:u,inDroppableZone:p=!0,itemRef:v})=>{const h=H(X=>{var ae;return((ae=X.selectedItem)==null?void 0:ae.props.id)===n?X.zoomConfig.zoom:1}),m=H(X=>X._experimentalFullScreenCanvas),y=H(X=>X.overrides),b=H(X=>X.dispatch),k=H(X=>X.iframe),x=g.useRef(0),_=g.useContext(yo),[I,w]=g.useState({}),A=g.useCallback((X,ae)=>{var se;(se=_==null?void 0:_.registerLocalZone)==null||se.call(_,X,ae),w(Ie=>N(D({},Ie),{[X]:ae}))},[w]),E=g.useCallback(X=>{var ae;(ae=_==null?void 0:_.unregisterLocalZone)==null||ae.call(_,X),w(se=>{const Ie=D({},se);return delete Ie[X],Ie})},[w]),C=Object.values(I).filter(Boolean).length>0,S=H(Be(X=>{var ae;return(ae=X.state.indexes.nodes[n])==null?void 0:ae.path})),j=H(Be(X=>{const ae=et({index:o,zone:i},X.state);return X.permissions.getPermissions({item:ae})})),O=g.useContext(He),L=ye(),[$,F]=g.useState(u||d),M=g.useMemo(()=>yd($),[$]),q=W_(O,n),{ref:W,isDragging:B,sortable:Z}=vd({id:n,index:o,group:i,type:"component",data:{areaId:_==null?void 0:_.areaId,zone:i,index:o,componentType:r,containsActiveZone:C,depth:t,path:S||[],inDroppableZone:p},collisionPriority:t,collisionDetector:M,transition:{duration:200,easing:"cubic-bezier(0.2, 0, 0, 1)"},plugins:X=>[...X,zi.configure({feedback:"clone",dropAnimation:q})]});g.useEffect(()=>{const X=O.getState().enabledIndex[i];Z.droppable.disabled=!X,Z.draggable.disabled=!j.drag;const ae=O.subscribe(se=>{Z.droppable.disabled=!se.enabledIndex[i]});return K.current&&!j.drag?(K.current.setAttribute("data-puck-disabled",""),()=>{var se;(se=K.current)==null||se.removeAttribute("data-puck-disabled"),ae()}):ae},[j.drag,i]);const[,oe]=g.useState(0),K=g.useRef(null),te=g.useCallback(X=>{W(X),K.current!==X&&(K.current=X,oe(ae=>ae+1),v&&Sc([v],X))},[v,W]),[be,Q]=g.useState();g.useEffect(()=>{var X,ae,se;Q(k.enabled?(X=K.current)==null?void 0:X.ownerDocument.body:(se=(ae=K.current)==null?void 0:ae.closest("[data-puck-preview]"))!=null?se:document.body)},[k.enabled]);const ie=g.useCallback(()=>{var X,ae;if(!K.current)return;const se=K.current,Ie=se.getBoundingClientRect(),qe=k.enabled?null:se.closest("[data-puck-preview]"),lt=(()=>{let kn=se;for(;kn&&kn!==document.documentElement;){if(getComputedStyle(kn).position==="fixed")return!0;kn=kn.parentElement}return!1})(),tt=qe==null?void 0:qe.getBoundingClientRect(),mr=qe?kf(qe):{x:0,y:0},zt=lt?{x:0,y:0}:kf(se),_r=lt?{x:0,y:0}:{x:zt.x-mr.x-((X=tt==null?void 0:tt.left)!=null?X:0),y:zt.y-mr.y-((ae=tt==null?void 0:tt.top)!=null?ae:0)};return{left:`${Ie.left+_r.x}px`,top:`${Ie.top+_r.y}px`,height:`${Ie.height}px`,width:`${Ie.width}px`,position:lt?"fixed":void 0}},[k.enabled]),[ke,Y]=g.useState(),P=g.useRef(null),T=g.useRef(null),R=g.useCallback(()=>{Y(ie()),v&&Sc([v],K.current)},[ie,v]),U=g.useCallback(()=>{T.current==null&&(T.current=requestAnimationFrame(()=>{T.current=null,R()}))},[R]);g.useEffect(()=>()=>{T.current!=null&&(cancelAnimationFrame(T.current),T.current=null)},[]),g.useEffect(()=>{if(K.current){const X=new ResizeObserver(()=>{U()});return X.observe(K.current),()=>{X.disconnect()}}},[U,v]);const V=H(X=>X.nodes.registerNode),G=H(X=>X.nodes.unregisterNode),ne=g.useCallback(()=>{vr(!1)},[]),ue=g.useCallback(()=>{vr(!0)},[]),ve=g.useRef({sync:()=>null,hideOverlay:()=>null,showOverlay:()=>null});g.useLayoutEffect(()=>{ve.current.sync=R,ve.current.hideOverlay=ne,ve.current.showOverlay=ue},[ne,ue,R]),g.useEffect(()=>(V(n,ve.current),()=>{G(n)}),[n,V,G]);const $e=g.useMemo(()=>y.actionBar||lP,[y.actionBar]),je=g.useMemo(()=>y.componentOverlay||cP,[y.componentOverlay]),Ee=g.useCallback(X=>{if(!!O.getState().draggedItem)return;X.target.closest("[data-puck-overlay-portal]")||X.stopPropagation(),b(m?{type:"setUi",ui:{itemSelector:s?null:{index:o,zone:i}}}:{type:"setUi",ui:{itemSelector:{index:o,zone:i}}})},[o,i,n,s,m]),we=g.useCallback(()=>{const{nodes:X,zones:ae}=L.getState().state.indexes,se=X[n],Ie=se!=null&&se.parentId?X[se==null?void 0:se.parentId]:null;if(!Ie||!se.parentId)return;const qe=`${Ie.parentId}:${Ie.zone}`,lt=ae[qe].contentIds.indexOf(se.parentId);b({type:"setUi",ui:{itemSelector:{zone:qe,index:lt}}})},[_,S]),he=g.useCallback(()=>{b({type:"duplicate",sourceIndex:o,sourceZone:i})},[o,i]),Pt=g.useCallback(()=>{b({type:"remove",index:o,zone:i})},[o,i]),[Qt,_n]=g.useState(!1),yn=Zt(He,X=>X.hoveringComponent===n);g.useEffect(()=>{if(!K.current)return;const X=K.current,ae=Ie=>{const qe=!!O.getState().draggedItem;_n(qe?!!B:!0),Ie.stopPropagation()},se=Ie=>{Ie.stopPropagation(),_n(!1)};return X.setAttribute("data-puck-component",n),X.setAttribute("data-puck-dnd",n),X.style.position="relative",X.addEventListener("click",Ee),X.addEventListener("mouseover",ae),X.addEventListener("mouseout",se),()=>{X.removeAttribute("data-puck-component"),X.removeAttribute("data-puck-dnd"),X.removeEventListener("click",Ee),X.removeEventListener("mouseover",ae),X.removeEventListener("mouseout",se)}},[K.current,Ee,C,i,n,B,p]);const[er,vr]=g.useState(!1),[gr,ko]=g.useState(!0),[js,bn]=g.useTransition();g.useEffect(()=>{bn(()=>{Qt||yn||s?(U(),vr(!0),Li(!1)):vr(!1)})},[Qt,yn,s,k]);const[wo,Li]=g.useState(!1),So=N_(X=>{X?bn(()=>{R(),ko(!0)}):ko(!1)});g.useEffect(()=>{B&&Li(!0)},[B]),g.useEffect(()=>{if(wo)return So()},[wo,So]),g.useEffect(()=>{if(!gr||!(s||B))return;const X=K.current;if(!X)return;const ae=X.ownerDocument,se=ae.defaultView;if(!se)return;x.current=0,U();const Ie=()=>U(),qe=()=>U();ae.addEventListener("scroll",Ie,!0),se.addEventListener("resize",qe);let lt=0;const tt=mr=>{if(mr-x.current>=iP){x.current=mr;const zt=K.current;if(zt){const _r=zt.getBoundingClientRect(),xn=P.current;(!xn||Math.abs(_r.x-xn.x)>.5||Math.abs(_r.y-xn.y)>.5||Math.abs(_r.width-xn.width)>.5||Math.abs(_r.height-xn.height)>.5)&&(P.current=_r,U())}}lt=requestAnimationFrame(tt)};return lt=requestAnimationFrame(tt),()=>{ae.removeEventListener("scroll",Ie,!0),se.removeEventListener("resize",qe),cancelAnimationFrame(lt)}},[gr,s,B,U]);const Fi=g.useCallback(X=>{if(X&&X.ownerDocument.defaultView){const se=X.getBoundingClientRect(),qe=se.x<0,tt=se.y<0;qe&&(X.style.transformOrigin="left top",X.style.left="0px"),tt&&(X.style.top="12px",qe||(X.style.transformOrigin="right top"))}},[h]),qr=g.useRef(null);g.useEffect(()=>{Fi(qr.current)},[qr.current,Fi]),g.useEffect(()=>{if(u){F(u);return}if(K.current){const X=window.getComputedStyle(K.current);if(X.display==="inline"||X.display==="inline-block"){F("x");return}}F(d)},[K,u,d]);const Ni=J("action-selectparent"),Bi=J("action-duplicate"),Os=J("action-delete"),ge=g.useMemo(()=>(_==null?void 0:_.areaId)&&(_==null?void 0:_.areaId)!=="root"&&f.jsx(ht.Action,{onClick:we,label:Ni,children:f.jsx(A1,{size:16})}),[_==null?void 0:_.areaId,Ni]),Oe=g.useMemo(()=>N(D({},_),{areaId:n,zoneCompound:i,index:o,depth:t+1,registerLocalZone:A,unregisterLocalZone:E}),[_,n,i,o,t,A,E]),Ve=H(X=>{var ae;return((ae=X.currentRichText)==null?void 0:ae.inlineComponentId)===n?X.currentRichText:null}),Ft=j.duplicate||j.delete;return f.jsxs(yi,{value:Oe,children:[gr&&er&&pr.createPortal(f.jsxs("div",{className:yr({isSelected:s,isDragging:B,hover:Qt||yn}),style:D({},ke),"data-puck-overlay":!0,children:[l,a&&f.jsx("div",{className:yr("loadingOverlay"),children:f.jsx(pn,{})}),f.jsx("div",{className:yr("actionsOverlay"),style:{top:aP/h},children:f.jsx("div",{className:yr("actions"),style:{transform:`scale(${1/h}`,top:sP/h,right:0,paddingLeft:wf,paddingRight:wf},ref:qr,children:f.jsxs($e,{parentAction:ge,label:c,children:[Ve&&f.jsxs(f.Fragment,{children:[f.jsx(d2,{editor:Ve.editor,field:Ve.field,inline:!0,readOnly:!1}),Ft&&f.jsx(ht.Separator,{})]}),j.duplicate&&f.jsx(ht.Action,{onClick:he,label:Bi,children:f.jsx(iu,{className:yr("actionsAction")})}),j.delete&&f.jsx(ht.Action,{onClick:Pt,label:Os,children:f.jsx(au,{className:yr("actionsAction")})})]})})}),f.jsx("div",{className:yr("overlayWrapper"),children:f.jsx(je,{componentId:n,componentType:r,hover:Qt,isSelected:s,children:f.jsx("div",{className:yr("overlay")})})})]}),be||document.body),e(te)]})};z();var V_={DropZone:"_DropZone_wc2ks_1","DropZone--hasChildren":"_DropZone--hasChildren_wc2ks_11","DropZone--isAreaSelected":"_DropZone--isAreaSelected_wc2ks_24","DropZone--hoveringOverArea":"_DropZone--hoveringOverArea_wc2ks_25","DropZone--isRootZone":"_DropZone--isRootZone_wc2ks_25","DropZone-item":"_DropZone-item_wc2ks_39","DropZone-linePlaceholder":"_DropZone-linePlaceholder_wc2ks_43","DropZone-hitbox":"_DropZone-hitbox_wc2ks_55","DropZone--isEnabled":"_DropZone--isEnabled_wc2ks_63","DropZone--isAnimating":"_DropZone--isAnimating_wc2ks_74"};z();var q_=(e,{allow:t,disallow:r})=>{if(!e)return!0;const n=new Set(t),o=new Set(r);return r?(o.has(e)&&n.has(e)&&o.delete(e),!o.has(e)):t?n.has(e):!0};z();z();var U_={Drawer:"_Drawer_1n90m_1","Drawer-draggable":"_Drawer-draggable_1n90m_8","Drawer-draggableBg":"_Drawer-draggableBg_1n90m_12","DrawerItem-draggable":"_DrawerItem-draggable_1n90m_22","DrawerItem--disabled":"_DrawerItem--disabled_1n90m_38",DrawerItem:"_DrawerItem_1n90m_22","Drawer--isDraggingFrom":"_Drawer--isDraggingFrom_1n90m_48","DrawerItem-name":"_DrawerItem-name_1n90m_72"};z();z();z();function dP(e,t){const r=setTimeout(e,t);return()=>clearTimeout(r)}function pP(e,t){const r=()=>performance.now();let n,o=0;return function(...i){const a=r(),s=this;a-o>=t?(e.apply(s,i),o=a):(n==null||n(),n=dP(()=>{e.apply(s,i),o=r()},t-(a-o)))}}z();var fP=class{constructor(e,t){this.scaleFactor=1,this.frameEl=null,this.frameRect=null;var r;this.target=e,this.original=t,this.frameEl=document.querySelector("iframe#preview-frame"),this.frameEl&&(this.frameRect=this.frameEl.getBoundingClientRect(),this.scaleFactor=this.frameRect.width/(((r=this.frameEl.contentWindow)==null?void 0:r.innerWidth)||1))}get x(){return this.original.x}get y(){return this.original.y}get global(){return document!==this.target.ownerDocument&&this.frameRect?{x:this.x*this.scaleFactor+this.frameRect.left,y:this.y*this.scaleFactor+this.frameRect.top}:this.original}get frame(){return document===this.target.ownerDocument&&this.frameRect?{x:(this.x-this.frameRect.left)/this.scaleFactor,y:(this.y-this.frameRect.top)/this.scaleFactor}:this.original}};z();var hP=typeof PointerEvent<"u"?PointerEvent:Event,Z_=class extends hP{constructor(e,t){super(e,t),this._originalTarget=null,this.originalTarget=t.originalTarget}set originalTarget(e){this._originalTarget=e}get originalTarget(){return this._originalTarget}},vP=e=>e.sort((t,r)=>{const n=t.data,o=r.data;return n.depth>o.depth?1:o.depth>n.depth?-1:0}),gP=e=>{let t=e==null?void 0:e.id;if(!e)return null;if(e.type==="component"){const r=e.data;r.containsActiveZone?t=null:t=r.zone}else if(e.type==="void")return"void";return t},la=6,mP=(e,t)=>{const r=[];let n=e.target.ownerDocument.elementsFromPoint(e.x,e.y);const o=n.find(a=>a.getAttribute("data-puck-preview")),i=n.find(a=>a.getAttribute("data-puck-drawer"));if(i&&(n=[i]),o){const a=gt();a&&(n=a.elementsFromPoint(e.frame.x,e.frame.y))}if(n)for(let a=0;a<n.length;a++){const s=n[a],l=s.getAttribute("data-puck-dropzone"),c=s.getAttribute("data-puck-dnd"),d=s.hasAttribute("data-puck-dnd-void");if((l||c)&&!d){const u=s.getBoundingClientRect(),p={left:u.left+la,right:u.right-la,top:u.top+la,bottom:u.bottom-la};if(e.frame.x<p.left||e.frame.x>p.right||e.frame.y>p.bottom||e.frame.y<p.top)continue}if(l){const u=t.registry.droppables.get(l);u&&r.push(u)}if(c){const u=t.registry.droppables.get(c);u&&r.push(u)}}return r},_P=(e,t)=>{var r;const n=mP(e,t);if(n.length>0){const o=vP(n),i=t.dragOperation.source,a=o.findIndex(h=>h.id===(i==null?void 0:i.id)),s=i==null?void 0:i.id;let l=[...o];s&&a>-1&&l.splice(a,1),l=l.filter(h=>{const m=h.data;if(s&&a>-1&&m.path.indexOf(s)>-1)return!1;if(h.type==="dropzone"){const y=h.data;if(!y.isDroppableTarget||y.areaId===s)return!1}else if(h.type==="component"&&!h.data.inDroppableZone)return!1;return!0}),l.reverse();const c=l[0];if(!c)return{zone:null,area:null};const d=c.data,u="containsActiveZone"in d,p=gP(c),v=u&&d.containsActiveZone?l[0].id:(r=l[0])==null?void 0:r.data.areaId;return{zone:p,area:v}}return{zone:Je,area:on}},yP=({onChange:e},t)=>class extends Xe{constructor(n,o){super(n),!(typeof window>"u")&&this.registerEffect(()=>{const a=pP(c=>{const d=c instanceof Z_&&c.originalTarget||c.target,u=new fP(d,{x:c.clientX,y:c.clientY});document.elementsFromPoint(u.global.x,u.global.y).some(h=>h.id===t)&&e(_P(u,n),n)},50),s=c=>{a(c)};return document.body.addEventListener("pointermove",s,{capture:!0}),()=>{document.body.removeEventListener("pointermove",s,{capture:!0})}})}};z();var bP=({zones:e,itemId:t,targetZone:r,getExpectedOrder:n})=>{const o=gt();if(!o||Id(o))return()=>{};const i=Array.from(new Set(e)).map(c=>`${bi(c)} > [data-puck-component]:not([data-dnd-dragging]):not([data-dnd-placeholder])`).join(", "),a=()=>{const c=new Map;return o.querySelectorAll(i).forEach(d=>{const u=d.getAttribute("data-puck-component");u&&u!==t&&c.set(u,{el:d,rect:d.getBoundingClientRect()})}),c},s=a(),l=n();return()=>{$_(o,{zones:e,itemId:t,targetZone:r,getExpectedOrder:n,initialExpectedOrder:l},()=>{a().forEach(({el:c,rect:d},u)=>{var p;const v=(p=s.get(u))==null?void 0:p.rect;if(!v)return;const h=v.x-d.x,m=v.y-d.y;Math.abs(h)<1&&Math.abs(m)<1||c.animate({translate:[`${h}px ${m}px 0`,"0px 0px 0"]},Ed)})})}};z();var fl=(e,{isDraggingBetweenSlots:t=!1,isNewComponent:r=!1}={})=>e==="auto"?t||r?"static":"fluid":e;z();z();z();var Ri=(e,t)=>{const r=e.indexes.nodes[t];if(!r)return;const n=`${r.parentId}:${r.zone}`,o=e.indexes.zones[n].contentIds.indexOf(t);return{zone:n,index:o}};function bo(e,t,r="force",n=!1,o){return Se(this,null,function*(){const i=yield t().resolveComponentData(e,r);if(!i.didChange&&!n)return;const a=Ri(t().state,i.node.props.id);if(!a){console.warn(`Warning: Could not find component with id "${e.props.id}" to resolve its data. Component may have been removed or the id is invalid.`);return}t().dispatch({type:"replace",data:ro(i.node),destinationIndex:a.index,destinationZone:a.zone,ui:o})})}var xP=(e,t,r,n)=>Se(null,null,function*(){const{getState:o}=n,i=dt(e),a={type:"insert",componentType:e,destinationIndex:r,destinationZone:t,id:i},s=o().state,l=sh(s,a,o()),c=o().dispatch;c(N(D({},a),{recordHistory:!0}));const d={index:r,zone:t};c({type:"setUi",ui:{itemSelector:d}});const u=et(d,l);u&&(yield bo(u,o,"insert"))});z();var Y_=(e,t,r,n)=>Se(null,null,function*(){var o,i,a;const s=n.getState().dispatch;s({type:"move",sourceIndex:t.index,sourceZone:(o=t.zone)!=null?o:Je,destinationIndex:r.index,destinationZone:(i=r.zone)!=null?i:Je,recordHistory:!1});const l=(a=n.getState().state.indexes.nodes[e])==null?void 0:a.data;l&&(yield bo(l,n.getState,"move"))});z();function K_(e){function t(r){return r?r.getAttribute("dir")||t(r.parentElement):"ltr"}return e?t(e):"ltr"}z();z();z();var Qa=(e,t,r)=>Math.max(t,Math.min(r,e)),kP=(e,t)=>{const r=Qa(e.x,Math.min(t.x1,t.x2),Math.max(t.x1,t.x2)),n=Qa(e.y,Math.min(t.y1,t.y2),Math.max(t.y1,t.y2));return Math.hypot(e.x-r,e.y-n)};z();var wP=e=>{const t=e.replace(/\[[^\]]*\]/g," ").trim();return t&&t!=="none"?t.split(/\s+/).length:0},X_=(e,t,r=t.getComputedStyle(e))=>{const n=r.display,o=K_(e)==="rtl";if(n==="flex"||n==="inline-flex"){const i=r.flexDirection;if(i.startsWith("row")){const a=i==="row-reverse";return{axis:"x",reversed:o?!a:a}}return{axis:"y",reversed:i==="column-reverse"}}return n==="grid"||n==="inline-grid"?r.gridAutoFlow.startsWith("column")||wP(r.gridTemplateColumns)>1?{axis:"x",reversed:o}:{axis:"y",reversed:!1}:{axis:"y",reversed:!1}},G_=({axis:e,reversed:t})=>{const r=e==="x",n=t?-1:1;return{horizontal:r,reversed:t,forward:n,start:s=>r?t?s.right:s.left:t?s.bottom:s.top,end:s=>r?t?s.left:s.right:t?s.top:s.bottom,isBefore:(s,l)=>n>0?s<=l:s>=l}},Sf=(e,t,r)=>{var n,o;const i=e.ownerDocument.defaultView;if(!i)return null;const a=new Map(r.map((I,w)=>[I,w])),s=Array.from(e.querySelectorAll(":scope > [data-puck-component]:not([data-dnd-dragging]):not([data-dnd-placeholder])")).map(I=>{var w,A;return{index:(A=a.get((w=I.getAttribute("data-puck-component"))!=null?w:""))!=null?A:-1,el:I}}).filter(I=>I.index!==-1).sort((I,w)=>I.index-w.index).map(({index:I,el:w})=>({index:I,rect:w.getBoundingClientRect()}));if(s.length===0)return 0;const l=X_(e,i),{horizontal:c,reversed:d,start:u,end:p}=G_(l),v=(I,w,A,E=[A])=>{let C=1/0,S=-1/0;for(const j of E)C=Math.min(C,c?j.top:j.left),S=Math.max(S,c?j.bottom:j.right);return c?{index:I,x1:w,x2:w,y1:A.top,y2:A.bottom,laneStart:C,laneEnd:S}:{index:I,x1:A.left,x2:A.right,y1:w,y2:w,laneStart:C,laneEnd:S}},h=[],m=(I,w,A)=>{const E=A==="before"?u(w):p(w);return v(I,E,w)};for(let I=0;I<=s.length;I++){const w=s[I-1],A=s[I];if(!A)h.push(m(w.index+1,w.rect,"after"));else if(!w)h.push(m(A.index,A.rect,"before"));else if(A.index-w.index>1)h.push(m(w.index+1,w.rect,"after")),h.push(m(A.index,A.rect,"before"));else if(d?p(w.rect)<u(A.rect):p(w.rect)>u(A.rect))h.push(m(A.index,A.rect,"before")),h.push(m(A.index,w.rect,"after"));else{const E=(p(w.rect)+u(A.rect))/2;h.push(v(A.index,E,A.rect,[w.rect,A.rect]))}}const y=c?t.y:t.x;let b=null,k=1/0,x=null,_=1/0;for(const I of h){const w=kP(t,I);w<k&&(k=w,b=I),y>=I.laneStart&&y<=I.laneEnd&&w<_&&(_=w,x=I)}return(o=(n=x??b)==null?void 0:n.index)!=null?o:null};z();var Ef=(e,t)=>{var r;const n=document.querySelector("iframe#preview-frame");if(!n||e.ownerDocument!==n.contentDocument)return t;const o=n.getBoundingClientRect(),i=o.width/(((r=n.contentWindow)==null?void 0:r.innerWidth)||1);return i>0?{x:(t.x-o.left)/i,y:(t.y-o.top)/i}:t},SP=e=>{const t=ye(),r=g.useRef(null),n=g.useCallback(l=>{var c;const d=(c=gt())==null?void 0:c.querySelector("[data-puck-entry]");l?d==null||d.setAttribute("data-puck-line-drag","true"):d==null||d.removeAttribute("data-puck-line-drag")},[]),o=g.useCallback((l,c)=>{var d;const u=(d=gt())==null?void 0:d.querySelector(bi(l));if(!u)return null;const p=Ef(u,c.dragOperation.position.current),v=Ja(t.getState().state,l);return Sf(u,p,v)},[t]),i=g.useCallback(l=>{var c;const{previewIndex:d={}}=e.getState(),u=Object.values(d).find(b=>b==null?void 0:b.linePlaceholder);if(!u)return;const p=(c=gt())==null?void 0:c.querySelector(bi(u.zone));if(!p)return;const v=Ef(p,l.dragOperation.position.current),h=p.getBoundingClientRect();if(!(v.x>=h.left&&v.x<=h.right&&v.y>=h.top&&v.y<=h.bottom))return;const y=Sf(p,v,Ja(t.getState().state,u.zone));y!==null&&y!==u.index&&e.setState({previewIndex:N(D({},d),{[u.zone]:N(D({},u),{index:y})})})},[t,e]),a=g.useCallback(()=>{var l;(l=r.current)==null||l.call(r),r.current=null},[]),s=g.useCallback(l=>{a();const c=gt();if(!c)return;let d=null;const u=()=>{d===null&&(d=requestAnimationFrame(()=>{d=null,i(l)}))};c.addEventListener("scroll",u,{capture:!0,passive:!0}),r.current=()=>{d!==null&&cancelAnimationFrame(d),c.removeEventListener("scroll",u,{capture:!0})}},[a,i]);return g.useEffect(()=>a,[a]),{getTargetIndex:o,setActive:n,startScrollTracking:s,stopScrollTracking:a,update:i}},J_=g.createContext({dragListeners:{}});function EP(e,t,r=[]){const{setDragListeners:n}=g.useContext(J_);g.useEffect(()=>{n&&n(o=>N(D({},o),{[e]:[...o[e]||[],t]}))},r)}var IP=100,CP=e=>{const t=g.useRef(null);return g.useCallback(r=>{wc.setState({fallbackEnabled:!1});const n=dt();t.current=n,setTimeout(()=>{t.current===n&&(wc.setState({fallbackEnabled:!0}),r.collisionObserver.forceUpdate(!0))},e)},[])},PP=({children:e,disableAutoScroll:t,behavior:r="auto"})=>{const n=H(C=>C.dispatch),o=H(C=>C.instanceId),i=ye(),a=g.useRef(null),s=CP(100),[l]=g.useState(()=>{const C=new Map;return $r(()=>({zoneDepthIndex:{},nextZoneDepthIndex:{},areaDepthIndex:{},nextAreaDepthIndex:{},draggedItem:null,previewIndex:{},enabledIndex:{},hoveringComponent:null,registerRootVirtualizer:(S,j)=>{C.set(S,j)},unregisterRootVirtualizer:S=>{C.delete(S)},scrollToComponent:S=>{const j=Array.from(C.values());if(j.length>0)for(const O of j){const L=O.resolveIndex(S);L<0||O.virtualizer.scrollToIndex(L,{behavior:"auto",align:"auto"})}else{const O=gt(),L=O==null?void 0:O.querySelector(to(S));L==null||L.scrollIntoView({behavior:"smooth"})}}}))}),c=g.useCallback(C=>{const{zoneDepthIndex:S={},areaDepthIndex:j={}}=l.getState()||{},O=Object.keys(S).length>0,L=Object.keys(j).length>0;let $=!1,F=!1;return(C.zone&&!S[C.zone]||!C.zone&&O)&&($=!0),(C.area&&!j[C.area]||!C.area&&L)&&(F=!0),{zoneChanged:$,areaChanged:F}},[l]),d=g.useCallback((C,S)=>{const{zoneChanged:j,areaChanged:O}=c(C);!j&&!O||(l.setState({zoneDepthIndex:C.zone?{[C.zone]:!0}:{},areaDepthIndex:C.area?{[C.area]:!0}:{}}),s(S),setTimeout(()=>{S.collisionObserver.forceUpdate(!0)},50),a.current=null)},[l]),u=x_(d,IP),p=()=>{u.cancel(),a.current=null};g.useEffect(()=>{},[]);const[v]=g.useState(()=>[...t?Or.plugins.filter(C=>C!==rd):Or.plugins,yP({onChange:(C,S)=>{const j=l.getState(),{zoneChanged:O,areaChanged:L}=c(C),$=S.dragOperation.status.dragging;if(L||O){let F={},M={};C.zone&&(F={[C.zone]:!0}),C.area&&(M={[C.area]:!0}),l.setState({nextZoneDepthIndex:F,nextAreaDepthIndex:M})}if(C.zone!=="void"&&(j!=null&&j.zoneDepthIndex.void)){d(C,S);return}if(L){if($){const F=a.current;F&&F.area===C.area&&F.zone===C.zone||(p(),u(C,S),a.current=C)}else p(),d(C,S);return}O&&d(C,S),p()}},o)]),h=_d(),[m,y]=g.useState({}),b=g.useRef(null),k=g.useRef(void 0),{getTargetIndex:x,setActive:_,startScrollTracking:I,stopScrollTracking:w,update:A}=SP(l),E=g.useMemo(()=>({mode:"edit",areaId:"root",depth:0}),[]);return f.jsx(J_.Provider,{value:{dragListeners:m,setDragListeners:y},children:f.jsx(ld,{plugins:v,sensors:h,onDragEnd:(C,S)=>{var j,O;w();const L=(j=gt())==null?void 0:j.querySelector("[data-puck-entry]");L==null||L.removeAttribute("data-puck-dragging");const{source:$,target:F}=C.operation;if(!$){_(!1),l.setState({draggedItem:null});return}const{zone:M,index:q}=$.data,{previewIndex:W={}}=l.getState()||{},B=(O=Object.values(W).find(te=>(te==null?void 0:te.props.id)===$.id&&!te.ghost))!=null?O:null,Z=!C.canceled&&(F==null?void 0:F.type)!=="void"&&(B!=null&&B.linePlaceholder)?bP({zones:k.current?[k.current.zone,B.zone]:[B.zone],itemId:B.type==="move"?B.props.id:void 0,targetZone:B.zone,getExpectedOrder:()=>Ja(i.getState().state,B.zone)}):null,oe=()=>{var te,be,Q,ie,ke;if(_(!1),l.setState({draggedItem:null}),C.canceled||(F==null?void 0:F.type)==="void"){l.setState({previewIndex:{}}),(te=m.dragend)==null||te.forEach(T=>{T(C,S)}),n({type:"setUi",ui:{itemSelector:null,isDragging:!1}});return}const Y=B&&B.linePlaceholder&&k.current&&B.zone===k.current.zone&&B.index>k.current.index?B.index-1:(be=B==null?void 0:B.index)!=null?be:q;B&&(l.setState({previewIndex:{}}),B.type==="insert"?xP(B.componentType,B.zone,B.index,i):k.current&&Y_(B.props.id,k.current,N(D({},B),{index:Y}),i),Z==null||Z());const P=((Q=k.current)==null?void 0:Q.zone)!==(B==null?void 0:B.zone)||((ie=k.current)==null?void 0:ie.index)!==Y;n({type:"setUi",ui:{itemSelector:B?{index:Y,zone:B.zone}:{index:q,zone:M},isDragging:!1},recordHistory:P}),(ke=m.dragend)==null||ke.forEach(T=>{T(C,S)})};let K;K=pt(()=>{$.status==="idle"&&(oe(),K==null||K())})},onDragMove:(C,S)=>{var j;A(S),(j=m.dragmove)==null||j.forEach(O=>{O(C,S)})},onDragOver:(C,S)=>{var j,O,L,$,F,M;if(C.preventDefault(),!((j=l.getState())==null?void 0:j.draggedItem))return;p();const{source:W,target:B}=C.operation;if(!B||!W||B.type==="void")return;const[Z]=W.id.split(":"),[oe]=B.id.split(":"),K=W.data;let te=K.zone,be=K.index,Q="",ie=0;if(B.type==="component"){const Y=B.data;Q=Y.zone;const P=(O=S.collisionObserver.collisions[0])==null?void 0:O.data,T=bd(P==null?void 0:P.direction,K_(B.element));ie=xd({position:T,sourceIndex:be,targetIndex:Y.index,isSameZone:te===Q})}else Q=B.id.toString(),ie=0;const ke=((L=i.getState().state.indexes.nodes[B.id])==null?void 0:L.path)||[];if(!(oe===Z||ke.find(Y=>{const[P]=Y.split(":");return P===Z}))){if(b.current==="new"){const Y=fl(r,{isNewComponent:!0})==="static";Y&&(ie=($=x(Q,S))!=null?$:ie),_(Y),l.setState({previewIndex:{[Q]:{componentType:K.componentType,type:"insert",index:ie,zone:Q,element:W.element,props:{id:W.id.toString()},linePlaceholder:Y}}})}else{k.current||(k.current={zone:K.zone,index:K.index});const Y=et(k.current,i.getState().state);if(Y){const P=k.current.zone,T=P!==Q,R=fl(r,{isDraggingBetweenSlots:T})==="static";R&&(ie=(F=x(Q,S))!=null?F:ie),_(R);const U={[Q]:{componentType:K.componentType,type:"move",index:ie,zone:Q,props:Y.props,element:W.element,linePlaceholder:R}};if(R&&T){const V=l.getState().previewIndex[P];let G=k.current.index;V&&!V.linePlaceholder&&(G=V.index),U[P]={componentType:K.componentType,type:"move",index:G,zone:P,props:Y.props,element:W.element,ghost:!0}}l.setState({previewIndex:U})}}(M=m.dragover)==null||M.forEach(Y=>{Y(C,S)})}},onDragStart:(C,S)=>{var j;r!=="fluid"&&I(S);const{source:O}=C.operation;if((O==null?void 0:O.type)==="component"){const L=O.data,$={zone:L.zone,index:L.index};k.current=$;const F=et($,i.getState().state);if(F){const M=fl(r)==="static";_(M),l.setState({previewIndex:{[L.zone]:{componentType:L.componentType,type:"move",index:L.index,zone:L.zone,props:F.props,element:O.element,linePlaceholder:M}}})}}(j=m.dragstart)==null||j.forEach(L=>{L(C,S)})},onBeforeDragStart:C=>{var S,j,O,L;const $=((S=C.operation.source)==null?void 0:S.type)==="drawer";b.current=$?"new":"existing",k.current=void 0,l.setState({draggedItem:C.operation.source}),((j=i.getState().selectedItem)==null?void 0:j.props.id)!==((O=C.operation.source)==null?void 0:O.id)?n({type:"setUi",ui:{itemSelector:null,isDragging:!0},recordHistory:!1}):n({type:"setUi",ui:{isDragging:!0},recordHistory:!1});const F=(L=gt())==null?void 0:L.querySelector("[data-puck-entry]");F==null||F.setAttribute("data-puck-dragging","true"),_(!1)},children:f.jsx(GC,{store:l,children:f.jsx(yi,{value:E,children:e})})})})},zP=({children:e,disableAutoScroll:t,behavior:r})=>H(o=>o.status)==="LOADING"?e:f.jsx(PP,{disableAutoScroll:t,behavior:r,children:e}),Pa=ee("Drawer",U_),jn=ee("DrawerItem",U_),Ec=({children:e,name:t,label:r,dragRef:n,isDragDisabled:o})=>{const i=g.useMemo(()=>e||(({children:a})=>f.jsx("div",{className:jn("default"),children:a})),[e]);return f.jsx("div",{className:jn({disabled:o}),ref:n,onMouseDown:a=>a.preventDefault(),"data-testid":n?`drawer-item:${t}`:"","data-puck-drawer-item":!0,children:f.jsx(i,{name:t,children:f.jsx("div",{className:jn("draggableWrapper"),children:f.jsxs("div",{className:jn("draggable"),children:[f.jsx("div",{className:jn("name"),children:r??t}),f.jsx("div",{className:jn("icon"),children:f.jsx(j_,{})})]})})})})},AP=({children:e,name:t,label:r,id:n,isDragDisabled:o})=>{const i=g.useContext(He),a=W_(i),{ref:s}=tI({id:n,data:{componentType:t},disabled:o,type:"drawer",plugins:[zi.configure({dropAnimation:a})]});return f.jsxs("div",{className:Pa("draggable"),children:[f.jsx("div",{className:Pa("draggableBg"),children:f.jsx(Ec,{name:t,label:r,children:e})}),f.jsx("div",{className:Pa("draggableFg"),children:f.jsx(Ec,{name:t,label:r,dragRef:s,isDragDisabled:o,children:e})})]})},jP=({name:e,children:t,id:r,label:n,index:o,isDragDisabled:i})=>{const a=r||e,[s,l]=g.useState(dt(a));return typeof o<"u"&&console.error("Warning: The `index` prop on Drawer.Item is deprecated and no longer required."),EP("dragend",()=>{l(dt(a))},[a]),f.jsx("div",{children:f.jsx(AP,{name:e,label:n,id:s,isDragDisabled:i,children:t})},s)},Cd=({children:e,droppableId:t,direction:r})=>{t&&console.error("Warning: The `droppableId` prop on Drawer is deprecated and no longer required."),r&&console.error("Warning: The `direction` prop on Drawer is deprecated and no longer required to achieve multi-directional dragging.");const n=Ps(),{ref:o}=dd({id:n,type:"void",collisionPriority:0});return f.jsx("div",{className:Pa(),ref:o,"data-puck-dnd":n,"data-puck-drawer":!0,"data-puck-dnd-void":!0,children:e})};Cd.Item=jP;z();var If=(e,t)=>e.getState().state.indexes.zones[t].contentIds.length,OP=({zoneCompound:e,userMinEmptyHeight:t,ref:r})=>{const n=ye(),[o,i]=g.useState(0),[a,s]=g.useState(!1),{draggedItem:l,isZone:c}=Zt(He,v=>{var h,m;return{draggedItem:((h=v.draggedItem)==null?void 0:h.data.zone)===e?v.draggedItem:null,isZone:((m=v.draggedItem)==null?void 0:m.data.zone)===e}}),d=g.useRef(0),u=N_(v=>{if(v){const h=If(n,e);if(i(0),h||d.current===0){s(!1);return}const m=n.getState().selectedItem,y=n.getState().state.indexes.zones,b=n.getState().nodes;b.setOverlayVisible(m==null?void 0:m.props.id,!1),setTimeout(()=>{var k;const x=((k=y[e])==null?void 0:k.contentIds)||[];b.syncNodes(x),m&&setTimeout(()=>{b.syncNode(m.props.id),b.setOverlayVisible(m.props.id,!0)},200),s(!1)},100)}},[n,o,e]);g.useEffect(()=>{if(l&&r.current&&c){const v=r.current.getBoundingClientRect();return d.current=If(n,e),i(v.height),s(!0),u()}},[r.current,l,u]);const p=isNaN(Number(t))?t:`${t}px`;return[o?`${o}px`:p,a]};z();z();function DP(e,t){const r=t_();return g.useCallback((...n)=>Se(null,null,function*(){return yield r==null?void 0:r.renderer.rendering,e(...n)}),[...t,r])}var TP=(e,t)=>{const r=g.useContext(He),n=Zt(He,d=>d.previewIndex[t]),o=H(d=>d.state.ui.isDragging),[i,a]=g.useState(e),[s,l]=g.useState(n),c=DP((d,u,p,v,h,m)=>{p&&!h||(u&&!u.linePlaceholder?a(ei(d.filter(y=>y!==u.props.id),u.index,u.props.id)):a(h&&!m?d.filter(y=>y!==v):d),l(u))},[]);return g.useEffect(()=>{var d;const u=r.getState(),p=(d=u.draggedItem)==null?void 0:d.id,v=Object.values(u.previewIndex||{}),h=v.length>0,m=v.some(y=>y==null?void 0:y.linePlaceholder);c(e,n,o,p,h,m)},[e,n,o]),[i,s]};z();var MP="dynamic",RP="x",Cf="y",LP=(e,t)=>{const r=H(a=>a.status),[n,o]=g.useState(t||Cf),i=g.useCallback(()=>{if(e.current){const a=window.getComputedStyle(e.current);a.display==="grid"?o(MP):a.display==="flex"&&a.flexDirection==="row"?o(RP):o(Cf)}},[e.current]);return g.useEffect(()=>{const a=()=>{i()};return window.addEventListener("viewportchange",a),()=>{window.removeEventListener("viewportchange",a)}},[]),g.useEffect(i,[r,t]),[n,i]};z();var FP=({componentId:e,zone:t})=>{const r=H(i=>i.config),n=H(i=>i.metadata),o=H(Be(i=>{var a,s;const l=i.state.indexes;return((s=(a=l.zones[`${e}:${t}`])==null?void 0:a.contentIds)!=null?s:[]).map(d=>l.nodes[d].flatData)}));return f.jsx(du,{content:o,zone:t,config:r,metadata:n})};z();function Q_(e,t,r,n,o){const i=g.useRef(null),a=g.useRef(null),s=g.useRef(t.props),l=g.useMemo(()=>Hv(r,n,o),[r,n,o]),c=g.useMemo(()=>{var u,p,v,h;const m=t.type==="root"?e.root:(u=e.components)==null?void 0:u[t.type],y=(p=m==null?void 0:m.fields)!=null?p:{},b=i.current!==l;let k,x=!1;if(!a.current||b)for(const I in t.props)((v=y[I])==null?void 0:v.type)==="slot"&&(x=!0);else{k=["id"];const I=new Set([...Object.keys(t.props),...Object.keys(a.current)]);for(const w of I)t.props[w]!==a.current[w]&&(k.push(w),((h=y[w])==null?void 0:h.type)==="slot"&&(x=!0))}const _=un(t,l,e,!1,x,k).props;return a.current=t.props,i.current=l,s.current=k?D(D({},s.current),_):_,s.current},[e,t,l]);return g.useMemo(()=>D(D({},t.props),c),[t.props,c])}z();z();z();var ey=(e,t={})=>{if(!e)return;const{disableDrag:r=!1,disableDragOnFocus:n=!0}=t,o=s=>{s.stopPropagation()};e.addEventListener("mouseover",o,{capture:!0});const i=()=>{setTimeout(()=>{e.addEventListener("pointerdown",o,{capture:!0})},200)},a=()=>{e.removeEventListener("pointerdown",o,{capture:!0})};return r?e.addEventListener("pointerdown",o,{capture:!0}):n&&(e.addEventListener("focus",i,{capture:!0}),e.addEventListener("blur",a,{capture:!0})),e.setAttribute("data-puck-overlay-portal","true"),()=>{e.removeEventListener("mouseover",o,{capture:!0}),r?e.removeEventListener("pointerdown",o,{capture:!0}):n&&(e.removeEventListener("focus",i,{capture:!0}),e.removeEventListener("blur",a,{capture:!0})),e.removeAttribute("data-puck-overlay-portal")}};z();var NP={InlineTextField:"_InlineTextField_104qp_1"},BP=ee("InlineTextField",NP),$P=({propPath:e,componentId:t,value:r,isReadOnly:n,opts:o={}})=>{var i;const a=g.useRef(null),s=ye(),l=(i=o.disableLineBreaks)!=null?i:!1;g.useEffect(()=>{const v=s.getState(),h=v.state.indexes.nodes[t].data;if(!v.getComponentConfig(h.type))throw new Error(`InlineTextField Error: No config defined for ${h.type}`);if(a.current){const y=r??"";y!==a.current.innerText&&a.current.replaceChildren(y);const b=ey(a.current),k=x=>Se(null,null,function*(){const I=s.getState().state.indexes.nodes[t];let w=x.target.innerText;l&&(w=w.replaceAll(/\n/gm,""));const A=Ss(I.data.props,e,w);yield bo(N(D({},I.data),{props:A}),s.getState,"replace",!0)});return a.current.addEventListener("input",k),()=>{var x;(x=a.current)==null||x.removeEventListener("input",k),b==null||b()}}},[s,a.current,r,l]);const[c,d]=g.useState(!1),[u,p]=g.useState(!1);return f.jsx("span",{className:BP(),ref:a,contentEditable:c||u?"plaintext-only":"false",onClick:v=>{v.preventDefault(),v.stopPropagation()},onClickCapture:v=>{v.preventDefault(),v.stopPropagation();const h=Ri(s.getState().state,t);s.getState().setUi({itemSelector:h})},onKeyDown:v=>{v.stopPropagation(),(l&&v.key==="Enter"||n)&&v.preventDefault()},onKeyUp:v=>{v.stopPropagation(),v.preventDefault()},onMouseOverCapture:()=>d(!0),onMouseOutCapture:()=>d(!1),onFocus:()=>p(!0),onBlur:()=>p(!1)})},hl=g.memo($P),WP=()=>({text:({value:e,componentId:t,field:r,propPath:n,isReadOnly:o})=>r.contentEditable?f.jsx(hl,{propPath:n,componentId:t,value:e,opts:{disableLineBreaks:!0},isReadOnly:o}):e,textarea:({value:e,componentId:t,field:r,propPath:n,isReadOnly:o})=>r.contentEditable?f.jsx(hl,{propPath:n,componentId:t,value:e,isReadOnly:o}):e,custom:({value:e,componentId:t,field:r,propPath:n,isReadOnly:o})=>r.contentEditable&&typeof e=="string"?f.jsx(hl,{propPath:n,componentId:t,value:e,isReadOnly:o}):e});z();var HP=g.lazy(()=>Nr(()=>import("./chunks/Editor-44C53YAG-FHX0eoLj.js"),__vite__mapDeps([9,8,3,2,1])).then(e=>({default:e.Editor}))),ty=g.lazy(()=>Nr(()=>import("./chunks/Render-DQXAYUBI-tp0YyC1G.js"),__vite__mapDeps([7,8,3,2])).then(e=>({default:e.RichTextRender}))),ry=g.memo(({value:e,componentId:t,propPath:r,field:n,id:o})=>{const i=g.useRef(null),a=ye(),s=p=>{p.preventDefault(),p.stopPropagation()},l=p=>{p.preventDefault(),p.stopPropagation();const v=Ri(a.getState().state,t);a.getState().setUi({itemSelector:v})};g.useEffect(()=>{if(!i.current)return;const p=ey(i.current,{disableDragOnFocus:!0});return()=>p==null?void 0:p()},[i.current]);const c=g.useCallback((p,v)=>Se(null,null,function*(){const m=a.getState().state.indexes.nodes[t],y=Ss(m.data.props,r,p);yield bo(N(D({},m.data),{props:y}),a.getState,"replace",!0,v)}),[a,t,r]),d=g.useCallback(p=>{a.setState({currentRichText:{inlineComponentId:t,inline:!0,field:n,editor:p,id:o}})},[n,t]);if(!n.contentEditable)return f.jsx(g.Suspense,{fallback:f.jsx(Vv,{content:e}),children:f.jsx(ty,{content:e,field:n})});const u={content:e,onChange:c,field:n,inline:!0,onFocus:d,id:o,name:r};return f.jsx("div",{ref:i,onClick:s,onClickCapture:l,children:f.jsx(g.Suspense,{fallback:f.jsx(Sd,D({},u)),children:f.jsx(HP,D({},u))})})});ry.displayName="InlineEditorWrapper";var VP=()=>({richtext:({value:e,componentId:t,field:r,propPath:n,isReadOnly:o})=>{const{contentEditable:i=!0,tiptap:a}=r;if(i===!1||o)return f.jsx(ty,{content:e,field:r});const s=`${t}_${r.type}_${n}`;return f.jsx(ry,{value:e,componentId:t,propPath:n,field:r,id:s},s)}});z();z();function qP(e,t,r=[]){if(Object.is(e,t))return!0;if(typeof e!="object"||e===null||typeof t!="object"||t===null||Object.getPrototypeOf(e)!==Object.getPrototypeOf(t))return!1;const n=new Set(r),o=Object.keys(e).filter(a=>!n.has(a)),i=Object.keys(t).filter(a=>!n.has(a));if(o.length!==i.length)return!1;for(let a=0;a<o.length;a++){const s=o[a];if(!Object.prototype.hasOwnProperty.call(t,s))return!1;const l=e[s],c=t[s];if(!Object.is(l,c))return!1}return!0}var UP=({Component:e,componentProps:t})=>f.jsx(e,D({},t)),Pf=g.memo(UP,(e,t)=>{let r=!0;return"puck"in e.componentProps&&"puck"in t.componentProps&&(r=ni(e.componentProps.puck,t.componentProps.puck)),e.Component===t.Component&&qP(e.componentProps,t.componentProps,["puck"])&&r});z();var ZP=5,ny=320,oy=new Map,YP=e=>{var t;return(t=oy.get(e))!=null?t:ny},KP=(e,t)=>{t<=0||oy.set(e,t)},XP=({contentIds:e,zoneCompound:t,renderItem:r})=>{const n=H(x=>{var _,I;return(I=(_=x.selectedItem)==null?void 0:_.props.id)!=null?I:null}),o=gt(),i=g.useContext(He),a=Zt(He,x=>{var _;const I=(_=x.draggedItem)==null?void 0:_.id;return I?String(I):null}),s=Zt(He,x=>{var _,I,w;if((_=x.draggedItem)!=null&&_.id){const[A]=(w=Object.entries((I=x.previewIndex)!=null?I:{}).find(([,E])=>!(E!=null&&E.ghost)))!=null?w:[];return A==null?void 0:A.split(":")[0]}return null}),l=o==null?void 0:o.defaultView,c=g.useRef(new Map),d=ye(),u=g.useCallback(x=>{var _,I,w,A;if(!x||x==="root")return-1;const E=e.indexOf(x);if(E>-1)return E;const C=(w=(I=(_=d.getState().state.indexes.nodes)==null?void 0:_[x])==null?void 0:I.path)!=null?w:[];for(let S=C.length-1;S>=0;S-=1){const j=(A=C[S])==null?void 0:A.split(":")[0];if(!j||j==="root")continue;const O=e.indexOf(j);if(O>-1)return O}return-1},[d,e]),p=g.useMemo(()=>{const x=new Set;return[n,a,s].forEach(_=>{const I=u(_);I>-1&&x.add(I)}),Array.from(x).sort((_,I)=>_-I)},[s,a,u,n]),v=g.useCallback(x=>{const _=gd(x);return p.forEach(I=>{_.includes(I)||_.push(I)}),_.sort((I,w)=>I-w),_},[p]),h=P_({count:e.length,getItemKey:x=>e[x],estimateSize:x=>YP(e[x]),getScrollElement:()=>l??null,overscan:ZP,observeElementRect:(x,_)=>l?KI(x,_):k_(x,_),observeElementOffset:(x,_)=>l?GI(x,_):S_(x,_),scrollToFn:(x,_,I)=>l?QI(x,_,I):I_(x,_,I),rangeExtractor:v,initialOffset:()=>l?l.scrollY:0});g.useEffect(()=>(i.getState().registerRootVirtualizer(t,{resolveIndex:x=>u(x),virtualizer:h}),()=>{i.getState().unregisterRootVirtualizer(t)}),[u,h,t,i]);const m=g.useCallback(x=>{const _=c.current.get(x);if(_)return _;const I=w=>{if(!w)return;const A=Math.ceil(w.getBoundingClientRect().height)||ny;typeof A=="number"&&A>0&&KP(x,A)};return c.current.set(x,I),I},[]);g.useEffect(()=>{const x=new Set(e);Array.from(c.current.keys()).forEach(_=>{x.has(_)||c.current.delete(_)})},[e]);const y=h.getVirtualItems(),b=h.getTotalSize(),k=g.useMemo(()=>{const x=[];let _=0,I=-1;y.forEach(A=>{if(!A)return;const E=e[A.index],C=Math.max(A.start-_,0);C>0&&x.push(f.jsx("div",{style:{height:`${C}px`}},`gap:${I}:${A.index}`)),x.push(r({componentId:E,index:A.index,measureRef:m(E)})),_=A.end,I=A.index});const w=Math.max(b-_,0);return w>0&&x.push(f.jsx("div",{style:{height:`${w}px`}},`gap:${I}:end`)),x},[b,y,m]);return f.jsx(f.Fragment,{children:k})};z();var GP=ee("DropZone",V_),zf="var(--puck-line-placeholder-width, 2px)",JP=({zoneRef:e,contentIds:t,index:r})=>{const[n,o]=g.useState();return g.useLayoutEffect(()=>{var i,a,s,l;const c=e.current,d=c==null?void 0:c.ownerDocument.defaultView;if(!c||!d)return;const u=q=>q?d.getComputedStyle(q):void 0,p=q=>parseFloat(q??"")||0,v=q=>{const W=t[q];if(typeof W>"u")return;const B=c.querySelector(`:scope > ${to(W)}:not([data-dnd-dragging])`);if(B)return{el:B,rect:B.getBoundingClientRect()}},h=c.getBoundingClientRect(),m=d.getComputedStyle(c),y=v(r-1),b=v(r),k=b??y,x=X_(c,d,m),{horizontal:_,reversed:I,forward:w,start:A,end:E,isBefore:C}=G_(x),S=p(_?m.columnGap:m.rowGap),j=(q,W)=>{var B;const Z=W==="start"==!I?_?"marginLeft":"marginTop":_?"marginRight":"marginBottom";return p((B=u(q))==null?void 0:B[Z])},O=p(m.borderLeftWidth),L=p(m.borderTopWidth),$=p(m.borderRightWidth),F=p(m.borderBottomWidth);let M;b?y&&C(E(y.rect),A(b.rect))?M=(E(y.rect)+A(b.rect))/2:M=A(b.rect)-w*(Math.max(j(b.el,"start"),S)/2):y?M=E(y.rect)+w*(Math.max(j(y.el,"end"),S)/2):M=_?I?h.right-$-p(m.paddingRight):h.left+O+p(m.paddingLeft):I?h.bottom-F-p(m.paddingBottom):h.top+L+p(m.paddingTop),o(_?{top:((i=k==null?void 0:k.rect.top)!=null?i:h.top+L+p(m.paddingTop))-h.top+c.scrollTop-L,height:(a=k==null?void 0:k.rect.height)!=null?a:h.height-L-F-p(m.paddingTop)-p(m.paddingBottom),left:Qa(M-h.left+c.scrollLeft-O,0,c.scrollWidth),width:zf,transform:"translateX(-50%)"}:{left:((s=k==null?void 0:k.rect.left)!=null?s:h.left+O+p(m.paddingLeft))-h.left+c.scrollLeft-O,width:(l=k==null?void 0:k.rect.width)!=null?l:h.width-O-$-p(m.paddingLeft)-p(m.paddingRight),top:Qa(M-h.top+c.scrollTop-L,0,c.scrollHeight),height:zf,transform:"translateY(-50%)"})},[e,t,r]),n?f.jsx("div",{className:GP("linePlaceholder"),style:n,"data-puck-line-placeholder":!0}):null},QP=ee("DropZone",V_),ez=({element:e,label:t,override:r})=>e?f.jsx("div",{dangerouslySetInnerHTML:{__html:e.outerHTML}}):f.jsx(Ec,{name:t,children:r}),Ic=e=>f.jsx(iy,D({},e)),tz=({zoneCompound:e,componentId:t,index:r,dragAxis:n,collisionAxis:o,inDroppableZone:i,itemRef:a})=>{var s,l,c,d;const u=H(K=>K.metadata),p=g.useContext(yo),{depth:v=1}=p??{},h=g.useContext(He),m=H(Be(K=>{var te;return(te=K.state.indexes.nodes[t])==null?void 0:te.flatData.props})),y=H(K=>{var te;return(te=K.state.indexes.nodes[t])==null?void 0:te.data.type}),b=H(Be(K=>{var te;return(te=K.state.indexes.nodes[t])==null?void 0:te.data.readOnly})),k=ye(),x=g.useMemo(()=>{if(m)return ih({type:y,props:m});const K=h.getState().previewIndex[e];return t===(K==null?void 0:K.props.id)?{type:K.componentType,props:K.props,previewType:K.type,element:K.element}:null},[k,t,e,y,m]),_=H(K=>x!=null&&x.type?K.config.components[x.type]:null),I=g.useMemo(()=>({renderDropZone:Ic,isEditing:!0,dragRef:null,metadata:D(D({},u),_==null?void 0:_.metadata)}),[u,_==null?void 0:_.metadata]),w=H(K=>K.overrides),A=H(K=>{var te;return((te=K.componentState[t])==null?void 0:te.loadingCount)>0}),E=H(K=>{var te;return((te=K.selectedItem)==null?void 0:te.props.id)===t||!1}),C=J("label-component"),S=J("canvas-noconfig",{type:(l=(s=x==null?void 0:x.type)==null?void 0:s.toString())!=null?l:""});let j=(d=(c=_==null?void 0:_.label)!=null?c:x==null?void 0:x.type.toString())!=null?d:C;const O=g.useMemo(()=>N(D(D({},_==null?void 0:_.defaultProps),x==null?void 0:x.props),{puck:I,editMode:!0}),[_==null?void 0:_.defaultProps,x==null?void 0:x.props,I]),L=g.useMemo(()=>{var K;return{type:(K=x==null?void 0:x.type)!=null?K:y,props:O}},[x==null?void 0:x.type,y,O]),$=H(K=>K.config),F=H(K=>K.plugins),M=H(K=>K.fieldTransforms),q=g.useMemo(()=>D(D(D(D(D({},cu(Ic,K=>f.jsx(FP,{componentId:t,zone:K.zone}))),WP()),VP()),F.reduce((K,te)=>D(D({},K),te.fieldTransforms),{})),M),[F,M]),W=Q_($,L,q,b,A);if(!x)return;const B=_?_.render:()=>f.jsx("div",{style:{padding:48,textAlign:"center"},children:S});let Z=x.type;const oe="previewType"in x?x.previewType==="insert":!1;return f.jsx(uP,{id:t,componentType:Z,zoneCompound:e,depth:v+1,index:r,isLoading:A,isSelected:E,label:j,autoDragAxis:n,userDragAxis:o,inDroppableZone:i,itemRef:a,children:K=>{var te;return _!=null&&_.inline&&!oe?f.jsx(Pf,{Component:B,componentProps:N(D({},W),{puck:N(D({},W.puck),{dragRef:K})})}):f.jsx("div",{ref:K,children:oe?f.jsx(ez,{label:j,override:(te=w.componentItem)!=null?te:w.drawerItem,element:"element"in x&&x.element?x.element:void 0}):f.jsx(Pf,{Component:B,componentProps:W})})}})},Af=g.memo(tz),iy=g.forwardRef(function({zone:t,allow:r,disallow:n,style:o,className:i,minEmptyHeight:a="128px",collisionAxis:s,as:l},c){const d=g.useContext(yo),u=ye(),{areaId:p,depth:v=0,registerLocalZone:h,unregisterLocalZone:m}=d??{},y=H(Be(P=>{var T;return p?(T=P.state.indexes.nodes[p])==null?void 0:T.path:null}));let b=Je;p&&t!==Je&&(b=`${p}:${t}`);const k=b===Je||t===Je||p==="root",x=Zt(He,P=>P.nextAreaDepthIndex[p||""]),_=H(Be(P=>{var T;return(T=P.state.indexes.zones[b])==null?void 0:T.contentIds})),I=H(Be(P=>{var T;return(T=P.state.indexes.zones[b])==null?void 0:T.type}));g.useEffect(()=>{(!I||I==="dropzone")&&d!=null&&d.registerZone&&(d==null||d.registerZone(b))},[I,u]),g.useEffect(()=>{I==="dropzone"&&b!==Je&&console.warn("DropZones have been deprecated in favor of slot fields and will be removed in a future version of Puck. Please see the migration guide: https://www.puckeditor.com/docs/guides/migrations/dropzones-to-slots")},[I]);const w=g.useMemo(()=>_||[],[_]),A=g.useRef(null),E=g.useCallback(P=>q_(P,{allow:r,disallow:n}),[r,n]),C=Zt(He,P=>{var T;const R=(T=P.draggedItem)==null?void 0:T.data.componentType;return E(R)}),S=x||k,j=Zt(He,P=>{var T;let R=!0;return R=(T=P.zoneDepthIndex[b])!=null?T:!1,R&&(R=C),R});g.useEffect(()=>(h&&h(b,C||j),()=>{m&&m(b)}),[C,j,b]);const[O,L]=TP(w,b),$=L&&!L.linePlaceholder?1:0,F=O.length===$,M=j&&F,q=g.useContext(He);g.useEffect(()=>{const{enabledIndex:P}=q.getState();q.setState({enabledIndex:N(D({},P),{[b]:j})})},[j,q,b]);const W={id:b,collisionPriority:j?v:0,disabled:!M,collisionDetector:T_,type:"dropzone",data:{areaId:p,depth:v,isDroppableTarget:C,path:y||[]}},{ref:B}=dd(W),Z=H(P=>(P==null?void 0:P.selectedItem)&&p===(P==null?void 0:P.selectedItem.props.id)),[oe]=LP(A,s),[K,te]=OP({zoneCompound:b,userMinEmptyHeight:a,ref:A}),be=g.useCallback(P=>{Sc([A,B,c],P)},[B]),Q=H(P=>P._experimentalVirtualization),ie=l??"div",Y=Q&&((p??on)===on&&v===0);return f.jsxs(ie,{className:`${QP({isRootZone:k,hoveringOverArea:S,isEnabled:j,isAreaSelected:Z,hasChildren:w.length>0,isAnimating:te})}${i?` ${i}`:""}`,ref:be,"data-testid":`dropzone:${b}`,"data-puck-dropzone":b,style:N(D({},o),{"--puck-slot-min-empty-height":K,backgroundColor:o==null?void 0:o.backgroundColor}),children:[Y?f.jsx(XP,{contentIds:O,zoneCompound:b,renderItem:P=>f.jsx(Af,{zoneCompound:b,componentId:P.componentId,dragAxis:oe,index:P.index,collisionAxis:s,inDroppableZone:C,itemRef:P.measureRef},P.componentId)}):O.map((P,T)=>f.jsx(Af,{zoneCompound:b,componentId:P,dragAxis:oe,index:T,collisionAxis:s,inDroppableZone:C},P)),(L==null?void 0:L.linePlaceholder)&&f.jsx(JP,{zoneRef:A,contentIds:w,index:L.index})]})}),rz=({config:e,item:t,metadata:r})=>{const n=e.components[t.type],o=uu(e,t,s=>f.jsx(du,N(D({},s),{config:e,metadata:r}))),i=g.useMemo(()=>({areaId:o.id,depth:1}),[o]),a=ps(n.fields,o);return f.jsx(yi,{value:i,children:f.jsx(n.render,N(D(D({},o),a),{puck:N(D({},o.puck),{renderDropZone:Cc,metadata:D(D({},r),n.metadata)})}))},o.id)},Cc=e=>f.jsx(ay,D({},e)),ay=g.forwardRef(function({className:t,style:r,zone:n,as:o},i){const a=g.useContext(yo),{areaId:s="root"}=a||{},{config:l,data:c,metadata:d}=g.useContext(zc);let u=`${s}:${n}`,p=(c==null?void 0:c.content)||[];g.useEffect(()=>{p||a!=null&&a.registerZone&&(a==null||a.registerZone(u))},[p]);const v=o??"div";return!c||!l?null:(u!==Je&&(p=ah(c,u).zones[u]),f.jsx(v,{className:t,style:r,ref:i,children:p.map(h=>l.components[h.type]?f.jsx(rz,{config:l,item:h,metadata:d},h.props.id):null)}))}),Pc=e=>f.jsx(nz,D({},e)),nz=g.forwardRef(function(t,r){const n=g.useContext(yo);return(n==null?void 0:n.mode)==="edit"?f.jsx(f.Fragment,{children:f.jsx(iy,N(D({},t),{ref:r}))}):f.jsx(f.Fragment,{children:f.jsx(ay,N(D({},t),{ref:r}))})}),zc=Er.createContext({config:{components:{}},data:{root:{},content:[]},metadata:{}});function oz({config:e,data:t,metadata:r={}}){var n,o;const i=N(D({},t),{root:t.root||{},content:t.content||[]}),a="props"in i.root?i.root.props:i.root,s=(a==null?void 0:a.title)||"",l=N(D({},a),{puck:{renderDropZone:Pc,isEditing:!1,dragRef:null,metadata:r},title:s,editMode:!1,id:"puck-root"}),c=uu(e,{type:"root",props:l},p=>f.jsx(qv,N(D({},p),{config:e,metadata:r}))),d=ps((n=e.root)==null?void 0:n.fields,l),u=g.useMemo(()=>({mode:"render",depth:0}),[]);return(o=e.root)!=null&&o.render?f.jsx(zc.Provider,{value:{config:e,data:i,metadata:r},children:f.jsx(yi,{value:u,children:f.jsx(e.root.render,N(D(D({},c),d),{children:f.jsx(Cc,{zone:kl})}))})}):f.jsx(zc.Provider,{value:{config:e,data:i,metadata:r},children:f.jsx(yi,{value:u,children:f.jsx(Cc,{zone:kl})})})}z();z();function iz(e,t,r){return Se(this,null,function*(){const n=t().state.indexes.nodes[e];if(!n){console.warn(`Warning: Could not find component with id "${e}" to resolve its data. Component may have been removed or the id is invalid.`);return}yield bo(n.data,t,r)})}z();function az(e,t,r){return Se(this,null,function*(){const n=et(e,t().state);if(!n){console.warn(`Warning: Could not find component for selector "${JSON.stringify(e)}" to resolve its data. Component may have been removed or the selector is invalid.`);return}const o=ro(n);yield bo(o,t,r)})}var jf=(e,t)=>{const r={back:e.history.back,forward:e.history.forward,setHistories:e.history.setHistories,setHistoryIndex:e.history.setHistoryIndex,hasPast:e.history.hasPast(),hasFuture:e.history.hasFuture(),histories:e.history.histories,index:e.history.index},n={appState:ri(e.state),config:e.config,dispatch:e.dispatch,getPermissions:e.permissions.getPermissions,refreshPermissions:e.permissions.refreshPermissions,resolveDataById:(o,i)=>iz(o,t,i),resolveDataBySelector:(o,i)=>az(o,t,i),history:r,selectedItem:e.selectedItem||null,getItemBySelector:o=>et(o,e.state),getItemById:o=>e.state.indexes.nodes[o].data,getSelectorForId:o=>Ri(e.state,o),getParentById:o=>{const a=e.state.indexes.nodes[o].parentId;if(a===null)return;const s=e.state.indexes.nodes[a];if(s)return s.data},dictionary:e.dictionary};return n.__private={appState:e.state},n},sz=g.createContext(null),Of=e=>({state:e.state,config:e.config,dispatch:e.dispatch,permissions:e.permissions,history:e.history,selectedItem:e.selectedItem,dictionary:e.dictionary}),lz=e=>{const[t]=g.useState(()=>$r(()=>jf(Of(e.getState()),e.getState)));return g.useEffect(()=>e.subscribe(r=>Of(r),r=>{t.setState(jf(r,e.getState))}),[]),t};z();z();z();z();z();var cz={ComponentList:"_ComponentList_htktj_1","ComponentList--isExpanded":"_ComponentList--isExpanded_htktj_5","ComponentList-content":"_ComponentList-content_htktj_9","ComponentList-title":"_ComponentList-title_htktj_17","ComponentList-titleIcon":"_ComponentList-titleIcon_htktj_63"},ca=ee("ComponentList",cz),sy=({name:e,label:t})=>{var r;const n=H(i=>i.overrides),o=H(i=>i.permissions.getPermissions({type:e}).insert);return g.useEffect(()=>{n.componentItem&&console.warn("The `componentItem` override has been deprecated and renamed to `drawerItem`")},[n]),f.jsx(Cd.Item,{label:t,name:e,isDragDisabled:!o,children:(r=n.componentItem)!=null?r:n.drawerItem})},Hn=({children:e,title:t,id:r})=>{const n=H(d=>d.config),o=H(d=>d.setUi),i=H(d=>d.state.ui.componentList),{expanded:a=!0}=i[r]||{},s=`puck-drawer-category-${r}`,l=J("drawer-category-collapse",{title:t??""}),c=J("drawer-category-expand",{title:t??""});return f.jsxs("div",{className:ca({isExpanded:a}),children:[t&&f.jsxs("button",{type:"button",className:ca("title"),"aria-expanded":a,"aria-controls":s,onClick:()=>o({componentList:N(D({},i),{[r]:N(D({},i[r]),{expanded:!a})})}),title:a?l:c,children:[f.jsx("div",{children:t}),f.jsx("div",{className:ca("titleIcon"),children:a?f.jsx(Sv,{size:12}):f.jsx(ci,{size:12})})]}),f.jsx("div",{className:ca("content"),id:s,children:f.jsx(Cd,{children:e||Object.keys(n.components).map(d=>{var u;return f.jsx(sy,{label:(u=n.components[d].label)!=null?u:d,name:d},d)})})})]})};Hn.Item=sy;var uz=()=>{const[e,t]=g.useState(),r=H(i=>i.config),n=H(i=>i.state.ui.componentList),o=J("drawer-category-other");return g.useEffect(()=>{var i,a,s;if(Object.keys(n).length>0){const l=[];let c;c=Object.entries(n).map(([u,p])=>{var v,h;return!p.components||(p.components.forEach(m=>{l.push(m)}),p.visible===!1)?null:f.jsx(Hn,{id:u,title:((h=(v=r.categories)==null?void 0:v[u])==null?void 0:h.title)||p.title||u,children:p.components.map((m,y)=>{var b;const k=r.components[m]||{};return f.jsx(Hn.Item,{label:(b=k.label)!=null?b:m,name:m,index:y},m)})},u)});const d=Object.keys(r.components).filter(u=>l.indexOf(u)===-1);d.length>0&&!((i=n.other)!=null&&i.components)&&((a=n.other)==null?void 0:a.visible)!==!1&&c.push(f.jsx(Hn,{id:"other",title:((s=n.other)==null?void 0:s.title)||o,children:d.map((u,p)=>{var v;const h=r.components[u]||{};return f.jsx(Hn.Item,{name:u,label:(v=h.label)!=null?v:u,index:p},u)})},"other")),t(c)}},[r.categories,r.components,n,o]),e},ly=()=>{const e=H(n=>n.overrides),t=uz(),r=g.useMemo(()=>(e.components&&console.warn("The `components` override has been deprecated and renamed to `drawer`"),e.components||e.drawer||"div"),[e]);return f.jsx(r,{children:t||f.jsx(Hn,{id:"all"})})};z();var dz={BlocksPlugin:"_BlocksPlugin_9af19_1"},pz=ee("BlocksPlugin",dz),fz=(e={})=>{var t,r;return{name:"blocks",label:(t=e.label)!=null?t:"Blocks",render:()=>f.jsx("div",{className:pz(),children:f.jsx(ly,{})}),icon:(r=e.icon)!=null?r:f.jsx(D1,{})}};z();z();z();var hz=(e,t)=>Object.keys(e.indexes.zones).filter(r=>r.split(":")[0]===t);z();z();z();z();z();z();z();function vz(e,t){if(typeof e!="string")throw new Error(`Can't get field definition for path (${e}): Path should be a string`);if(!t||typeof t!="object")return;const r=e.split(/\.|\[\d+\]/).filter(Boolean);let n=t,o;for(let i=0;i<r.length;i++){const a=r[i];if(o=n[a],i===r.length-1)return o;if(!o||(o.type!=="object"||!o.objectFields)&&(o.type!=="array"||!o.arrayFields))return;o.type==="object"&&(n=o.objectFields),o.type==="array"&&(n=o.arrayFields)}}var cy=(e,t,r)=>{var n;const[o,i]=e.split(":");if(!i)return;const a=(n=r[o])==null?void 0:n.data.type,s=a&&a!==on?t.components[a]:t.root;return vz(i,s==null?void 0:s.fields)},Df={},gz=(e,t,r)=>{var n;if(((n=r.zones[e])==null?void 0:n.type)!=="slot")return Df;const o=cy(e,t,r.nodes);return(o==null?void 0:o.type)!=="slot"?Df:{allow:o.allow,disallow:o.disallow}},uy="outline-item",mz="outline-zone",Pd=(e,t,r)=>{const n=e.get(t);if(n!==void 0)return n;const o=r();return e.set(t,o),o},es=(e,t,r,n,o)=>Pd(e,`zone:${t}`,()=>{const i=gz(t,n,o);return q_(r,i)}),_z=(e,t,r,n,o)=>Pd(e,`childZones:${t}`,()=>Object.keys(o.zones).some(i=>i.startsWith(`${t}:`)&&es(e,i,r,n,o))),yz=(e,t,r,n)=>Pd(e,`subtree:${t}`,()=>{var o;return t===r?!0:(((o=n[t])==null?void 0:o.path)||[]).some(a=>a.split(":")[0]===r)}),dy=(e,t)=>r=>{if(r.type!==uy)return!1;const n=r.data,o=e.outlineStore.getState().acceptCache,{config:i,state:a}=e.appStore.getState(),s=a.indexes,l=t.kind==="row"?t.itemId:t.zoneCompound.split(":")[0];return yz(o,l,n.itemId,s.nodes)?!1:t.kind==="zone"?es(o,t.zoneCompound,n.componentType,i,s):es(o,t.zoneCompound,n.componentType,i,s)||_z(o,t.itemId,n.componentType,i,s)};z();var bz=600,py=()=>{let e=null,t=null;const r=()=>{e!==null&&(clearTimeout(e),e=null),t=null};return $r((n,o)=>({status:"idle",draggedRow:null,tempExpandedIds:new Set,expandCandidateId:null,indicator:null,drop:null,acceptCache:new Map,startDrag:i=>n({status:"dragging",draggedRow:i,acceptCache:new Map}),setTarget:(i,a)=>{var s,l,c,d;const u=o();((s=u.indicator)==null?void 0:s.targetId)===i.targetId&&((l=u.indicator)==null?void 0:l.position)===i.position&&((c=u.drop)==null?void 0:c.zone)===a.zone&&((d=u.drop)==null?void 0:d.index)===a.index||n({indicator:i,drop:a})},clearTarget:()=>{o().indicator===null&&o().drop===null||n({indicator:null,drop:null})},scheduleExpand:(i,a)=>{t===i||o().tempExpandedIds.has(i)||(r(),t=i,n({expandCandidateId:i}),e=setTimeout(()=>{e=null,t=null,n(s=>({tempExpandedIds:new Set(s.tempExpandedIds).add(i),expandCandidateId:null})),a()},bz))},cancelPendingExpand:()=>{r(),o().expandCandidateId!==null&&n({expandCandidateId:null})},endDrag:()=>{r(),n({status:"dropping",indicator:null,drop:null,expandCandidateId:null})},reset:()=>{r(),n({status:"idle",draggedRow:null,tempExpandedIds:new Set,expandCandidateId:null,indicator:null,drop:null,acceptCache:new Map})}}))},zd=g.createContext(py()),zs=()=>g.useContext(zd),Ad=e=>Zt(zd,e),xz=({kind:e,zoneCompound:t})=>{const r=ye(),n=zs(),o=`${e}:${t}`,i=g.useMemo(()=>dy({appStore:r,outlineStore:n},{kind:"zone",zoneCompound:t}),[r,n,t]),{ref:a}=dd({id:o,type:mz,accept:i,collisionDetector:T_,data:{kind:"zone",zoneCompound:t}}),s=Ad(c=>{var d;return((d=c.indicator)==null?void 0:d.targetId)===o});return g.useMemo(()=>({isDropTarget:s,ref:a}),[s,a])},fy=xz;z();z();var kz={DropLine:"_DropLine_eyz3q_2","DropLine--top":"_DropLine--top_eyz3q_12","DropLine--bottom":"_DropLine--bottom_eyz3q_16","DropLine--outset":"_DropLine--outset_eyz3q_20"},wz=ee("DropLine",kz),jd=({edge:e,outset:t})=>f.jsx("div",{className:wz({top:e==="top",bottom:e==="bottom",outset:!!t})});z();z();z();z();var Sz=(...e)=>[...e].filter(Boolean).join(" "),hy=Sz;z();var Ez={"LayerTree-helper":"_LayerTree-helper_1m7e4_2","LayerTree-helperRoot":"_LayerTree-helperRoot_1m7e4_11"},Tf=ee("LayerTree",Ez),vy=({zoneCompound:e})=>{const{ref:t,isDropTarget:r}=fy({kind:"empty",zoneCompound:e}),n=J("outline-empty"),[o]=e.split(":"),i=o===on;return f.jsxs("li",{className:hy(Tf("helper"),i?Tf("helperRoot"):void 0),"data-puck-drop-target":r||void 0,ref:t,children:[n,r&&f.jsx(jd,{edge:"top"})]})};z();z();var Iz=({componentType:e,index:t,itemId:r,zoneCompound:n})=>{const o=ye(),i=zs(),a=g.useMemo(()=>dy({appStore:o,outlineStore:i},{kind:"row",itemId:r,zoneCompound:n}),[o,i,r,n]),s=g.useMemo(()=>yd("y"),[]),{handleRef:l,ref:c,isDragSource:d}=vd({id:r,index:t,group:n,type:uy,accept:a,data:{kind:"row",itemId:r,zoneCompound:n,index:t,componentType:e},collisionPriority:1,collisionDetector:s,transition:{duration:0},plugins:m=>[...m,zi.configure({feedback:"clone",dropAnimation:null})]}),{indicatorPosition:u,isExpandCandidate:p,isTempExpanded:v}=Ad(m=>{var y;return{indicatorPosition:((y=m.indicator)==null?void 0:y.targetId)===r?m.indicator.position:null,isExpandCandidate:m.expandCandidateId===r,isTempExpanded:m.tempExpandedIds.has(r)}});return{rowRef:g.useCallback(m=>{c(m),l(m)},[c,l]),isDragSource:d,indicatorPosition:u,isExpandCandidate:p,isTempExpanded:v}};z();var Cz={Layer:"_Layer_onfgu_1","Layer-inner":"_Layer-inner_onfgu_8","Layer--isSortable":"_Layer--isSortable_onfgu_18","Layer-content":"_Layer-content_onfgu_22","Layer-clickable":"_Layer-clickable_onfgu_29","Layer-caret":"_Layer-caret_onfgu_57","Layer--containsZone":"_Layer--containsZone_onfgu_68","Layer-title":"_Layer-title_onfgu_76","Layer-name":"_Layer-name_onfgu_85","Layer-icon":"_Layer-icon_onfgu_91","Layer-zones":"_Layer-zones_onfgu_101","Layer--isExpanded":"_Layer--isExpanded_onfgu_106","Layer--isSelected":"_Layer--isSelected_onfgu_115","Layer--isExpandCandidate":"_Layer--isExpandCandidate_onfgu_138","Layer--isDragSource":"_Layer--isDragSource_onfgu_143"};z();z();var Pz={LayerActions:"_LayerActions_d90t9_2","LayerActions--visible":"_LayerActions--visible_d90t9_18"},zz=ee("LayerActions",Pz),Az=({node:e,visible:t})=>{const r=H(c=>c.dispatch),n=zs(),o=H(Be(c=>{const d=et({index:e.index,zone:e.zoneCompound},c.state),u=c.permissions.getPermissions({item:d});return{delete:u.delete,duplicate:u.duplicate}})),i=J("outline-item-duplicate"),a=J("outline-item-delete"),s=g.useCallback(c=>{c.stopPropagation(),n.getState().status==="idle"&&r({type:"remove",index:e.index,zone:e.zoneCompound})},[r,n,e]),l=g.useCallback(c=>{c.stopPropagation(),n.getState().status==="idle"&&r({type:"duplicate",sourceIndex:e.index,sourceZone:e.zoneCompound})},[r,n,e.index,e.zoneCompound]);return!o.delete&&!o.duplicate?null:f.jsxs("div",{className:zz({visible:t}),children:[o.duplicate&&f.jsx(Ke,{onClick:l,title:i,type:"button",children:f.jsx(iu,{})}),o.delete&&f.jsx(Ke,{onClick:s,title:a,type:"button",children:f.jsx(au,{})})]})},tr=ee("Layer",Cz),gy=g.forwardRef(function({dataIndex:t,depth:r,isSelected:n,node:o,selectedId:i},a){const s=H(C=>C.dispatch),l=H(C=>{var S,j;return(j=(S=C.state.ui.itemExpanded)==null?void 0:S[o.itemId])!=null?j:!1}),c=Zt(He,C=>C.hoveringComponent===o.itemId),d=H(C=>{var S;const j=et({index:o.index,zone:o.zoneCompound},C.state);return(S=C.permissions.getPermissions({item:j}))==null?void 0:S.drag}),{indicatorPosition:u,isDragSource:p,isExpandCandidate:v,isTempExpanded:h,rowRef:m}=Iz({componentType:o.componentType,index:o.index,itemId:o.itemId,zoneCompound:o.zoneCompound}),y=g.useContext(He),b=zs(),k=J("outline-item-collapse"),x=J("outline-item-expand"),_=o.childZones.length>0,I=g.useCallback(C=>{s({type:"setUi",ui:{itemSelector:C}})},[s]),w=l||h,A=u!==null,E=o.childZones.length!==1;return f.jsxs("li",{ref:a,className:tr({containsZone:_,isDragSource:p,isExpandCandidate:v,isExpanded:w,isHovering:c,isSelected:n,isSortable:d}),"data-index":t,"data-puck-layer-tree-id":o.itemId,children:[A&&f.jsx(jd,{edge:u==="before"?"top":"bottom",outset:!0}),f.jsxs("div",{className:tr("inner"),ref:m,onMouseEnter:C=>{C.stopPropagation(),b.getState().status==="idle"&&y.setState({hoveringComponent:o.itemId})},onMouseLeave:C=>{C.stopPropagation(),y.setState({hoveringComponent:null})},children:[f.jsx("div",{className:tr("caret"),children:f.jsx(Ke,{onClick:C=>{C.stopPropagation(),b.getState().status==="idle"&&s({type:"setUi",ui:S=>{var j;const O=D({},S.itemExpanded);return(j=S.itemExpanded)!=null&&j[o.itemId]?delete O[o.itemId]:O[o.itemId]=!0,{itemExpanded:O}},recordHistory:!1})},title:l?k:x,type:"button",children:f.jsx(wv,{})})}),f.jsxs("div",{className:tr("content"),children:[f.jsx("button",{type:"button",className:tr("clickable"),onClick:()=>{b.getState().status==="idle"&&(I({index:o.index,zone:o.zoneCompound}),y.getState().scrollToComponent(o.itemId))},children:f.jsxs("div",{className:tr("title"),children:[f.jsx("div",{className:tr("icon"),children:o.componentType==="Text"||o.componentType==="Heading"?f.jsx(ds,{}):f.jsx(W1,{})}),f.jsx("div",{className:tr("name"),children:o.label})]})}),f.jsx(Az,{node:o,visible:c&&!p})]})]}),_&&w&&o.childZones.map(C=>f.jsx("div",{className:tr("zones"),children:f.jsx(by,{depth:E?r+1:r,selectedId:i,tree:E?C:N(D({},C),{label:void 0})})},C.zoneCompound))]})});z();var my={LayerTree:"_LayerTree_o5tyt_1","LayerTree--nested":"_LayerTree--nested_o5tyt_12"},jz=ee("LayerTree",my),Oz=({depth:e,selectedId:t,tree:r})=>f.jsxs("ul",{className:jz({nested:e>0}),children:[r.items.length===0&&f.jsx(vy,{zoneCompound:r.zoneCompound}),r.items.map(n=>f.jsx(gy,{depth:e,isSelected:t===n.itemId,node:n,selectedId:t},n.itemId))]});z();var Dz=ee("LayerTree",my),_y=32,Tz=8,yy=new Map,Mz=e=>{var t;return(t=yy.get(e))!=null?t:_y},Rz=(e,t)=>{t<=0||yy.set(e,t)},Lz=e=>{var t;let r=(t=e==null?void 0:e.parentElement)!=null?t:null;for(;r;){const{overflow:n,overflowY:o}=getComputedStyle(r);if([n,o].some(i=>/auto|scroll/.test(i)))return r;r=r.parentElement}return null},Fz=({depth:e,selectedId:t,tree:r})=>{const n=g.useRef(null),o=Ad(v=>{var h;return((h=v.draggedRow)==null?void 0:h.zoneCompound)===r.zoneCompound?v.draggedRow.index:null}),i=g.useCallback(v=>{const h=gd(v);return o!==null&&!h.includes(o)&&(h.push(o),h.sort((m,y)=>m-y)),h},[o]),a=P_({count:r.items.length,estimateSize:v=>Mz(r.items[v].itemId),getItemKey:v=>r.items[v].itemId,getScrollElement:()=>Lz(n.current),overscan:Tz,rangeExtractor:i,measureElement:v=>{const h=Math.ceil(v.getBoundingClientRect().height),m=v.dataset.puckLayerTreeId;return m&&Rz(m,h),h||_y}}),s=a.getVirtualItems(),l=a.getTotalSize(),c=[];let d=0,u=-1;s.forEach(v=>{const h=r.items[v.index],m=Math.max(v.start-d,0);m>0&&c.push(f.jsx("li",{"aria-hidden":"true",style:{height:`${m}px`}},`gap:${r.zoneCompound}:${u}:${v.index}`)),c.push(f.jsx(gy,{dataIndex:v.index,depth:e,isSelected:t===h.itemId,node:h,ref:a.measureElement,selectedId:t},h.itemId)),d=v.end,u=v.index});const p=Math.max(l-d,0);return p>0&&c.push(f.jsx("li",{"aria-hidden":"true",style:{height:`${p}px`}},`gap:${r.zoneCompound}:${u}:end`)),f.jsxs("ul",{className:Dz({nested:e>0}),ref:n,children:[r.items.length===0&&f.jsx(vy,{zoneCompound:r.zoneCompound}),c]})};z();var Nz={"LayerTree-zoneTitle":"_LayerTree-zoneTitle_fvhlh_2","LayerTree-zoneIcon":"_LayerTree-zoneIcon_fvhlh_19"},Mf=ee("LayerTree",Nz),Bz=25,$z=({label:e,zoneCompound:t})=>{const{ref:r,isDropTarget:n}=fy({kind:"label",zoneCompound:t});return f.jsxs("div",{className:Mf("zoneTitle"),"data-puck-drop-target":n||void 0,ref:r,children:[f.jsx("div",{className:Mf("zoneIcon"),children:f.jsx(Ev,{})}),e,n&&f.jsx(jd,{edge:"bottom"})]})},by=({depth:e,selectedId:t,tree:r})=>{const n=e===0&&r.items.length>=Bz;return f.jsxs(f.Fragment,{children:[r.label&&f.jsx($z,{label:r.label,zoneCompound:r.zoneCompound}),n?f.jsx(Fz,{depth:e,selectedId:t,tree:r}):f.jsx(Oz,{depth:e,selectedId:t,tree:r})]})};z();z();z();function Wz(e,t){return Object.keys(t).some(r=>r.startsWith(`${e}:`))}var Hz=2,Vz=60,qz=(e,t)=>{let r,n=0,o=0;const i=()=>{var a;const s=(a=gt())==null?void 0:a.querySelector(`[data-puck-component="${e}"]`),l=s?s.getBoundingClientRect().top:null;if(n=l===r?n+1:0,r=l,o+=1,n>=Hz||o>=Vz){t(e);return}requestAnimationFrame(i)};requestAnimationFrame(i)},xy=e=>{if(typeof document>"u")return;const t=document.getElementById("preview-frame");e?t==null||t.setAttribute("data-puck-outline-dragging","true"):t==null||t.removeAttribute("data-puck-outline-dragging")},Uz=(e,t)=>{const r=e.operation.source,n=r==null?void 0:r.data;if(!r||!n)return;const o=t.appStore.getState(),i=et({zone:n.zoneCompound,index:n.index},o.state);if(!i||!o.permissions.getPermissions({item:i}).drag){e.preventDefault();return}t.outlineDndStore.getState().startDrag({itemId:n.itemId,zoneCompound:n.zoneCompound,index:n.index,componentType:n.componentType}),xy(!0),o.dispatch({type:"setUi",ui:{isDragging:!0},recordHistory:!1})},Rf=(e,t,r)=>{var n,o;const i=r.outlineDndStore.getState(),a=i.draggedRow;if(!a)return;const s=e.operation.target;if(!s){i.cancelPendingExpand(),i.clearTarget();return}const l=s.data;if(l.kind==="zone"){i.cancelPendingExpand(),i.setTarget({targetId:s.id.toString(),position:"inside"},{zone:l.zoneCompound,index:0});return}const{config:c,state:d}=r.appStore.getState(),u=d.indexes,p=i.acceptCache;if(es(p,l.zoneCompound,a.componentType,c,u)){const m=(n=t.collisionObserver.collisions[0])==null?void 0:n.data,y=bd(m==null?void 0:m.direction);i.setTarget({targetId:s.id.toString(),position:y},{zone:l.zoneCompound,index:xd({position:y,sourceIndex:a.index,targetIndex:l.index,isSameZone:l.zoneCompound===a.zoneCompound})})}else i.clearTarget();const v=!!((o=d.ui.itemExpanded)!=null&&o[l.itemId])||i.tempExpandedIds.has(l.itemId),h=Wz(l.itemId,u.zones);!v&&h?i.scheduleExpand(l.itemId,()=>{requestAnimationFrame(()=>t.collisionObserver.forceUpdate(!0))}):i.cancelPendingExpand()},Zz=(e,t)=>{const{source:r}=e.operation,n=t.outlineDndStore.getState(),o=n.draggedRow,i=e.canceled?null:n.drop,a=t.appStore.getState().dispatch;if(xy(!1),o&&i){Y_(o.itemId,{zone:o.zoneCompound,index:o.index},{zone:i.zone,index:i.index},t.appStore);const l=i.zone!==o.zoneCompound||i.index!==o.index;a({type:"setUi",ui:{itemSelector:{zone:i.zone,index:i.index},isDragging:!1},recordHistory:l}),qz(o.itemId,t.scrollToComponent)}else a({type:"setUi",ui:{isDragging:!1},recordHistory:!1});n.endDrag();const s=()=>t.outlineDndStore.getState().reset();if(!r||r.status==="idle")s();else{const l=pt(()=>{r.status==="idle"&&(s(),l==null||l())})}},Yz=[],Kz=({children:e})=>{const t=ye(),r=g.useContext(He),[n]=g.useState(()=>py()),o=H(s=>{var l,c;return(c=(l=s.dnd)==null?void 0:l.disableOutlineDrag)!=null?c:!1}),i=_d({mouse:[new or.Distance({value:5})]}),a=g.useMemo(()=>({outlineDndStore:n,appStore:t,scrollToComponent:s=>r.getState().scrollToComponent(s)}),[n,t,r]);return f.jsx(zd.Provider,{value:n,children:f.jsx(ld,{sensors:o?Yz:i,onBeforeDragStart:s=>{Uz(s,a)},onDragOver:(s,l)=>{s.preventDefault(),Rf(s,l,a)},onDragMove:(s,l)=>{Rf(s,l,a)},onDragEnd:s=>{Zz(s,a)},children:e})})};z();var Xz={LayerTreeRoot:"_LayerTreeRoot_1qowl_1"};z();var Gz=e=>{const t={};return Object.keys(e).forEach(r=>{const[n]=r.split(":");n&&(t[n]||(t[n]=[]),t[n].push(r))}),t},Jz=(e,t,r,n)=>{var o,i;if(n!==void 0)return n;const[,a]=e.split(":");if(a)return(i=(o=cy(e,r,t))==null?void 0:o.label)!=null?i:a},Qz=({config:e,itemId:t,index:r,nodes:n,zoneCompound:o,zones:i,zonesByParent:a,componentFallbackLabel:s})=>{var l,c,d,u;const p=n[t],v=(c=(l=p==null?void 0:p.data.type)==null?void 0:l.toString())!=null?c:s,h=(u=(d=e.components[v])==null?void 0:d.label)!=null?u:v;return{childZones:(a[t]||[]).map(y=>ky({config:e,nodes:n,zoneCompound:y,zones:i,zonesByParent:a})),componentType:v,index:r,itemId:t,label:h,zoneCompound:o}},ky=({config:e,label:t,nodes:r,zoneCompound:n,zones:o,zonesByParent:i=Gz(o),componentFallbackLabel:a})=>{var s,l;return{items:((l=(s=o[n])==null?void 0:s.contentIds)!=null?l:[]).map((d,u)=>Qz({config:e,itemId:d,index:u,nodes:r,zoneCompound:n,zones:o,zonesByParent:i})),label:Jz(n,r,e,t),zoneCompound:n}},eA=ee("LayerTreeRoot",Xz),tA=({selectedId:e,trees:t})=>{const r=H(n=>{var o,i;return(i=(o=n.dnd)==null?void 0:o.disableOutlineDrag)!=null?i:!1});return f.jsx(Kz,{children:f.jsx("div",{className:eA(),"data-puck-dnd-disabled":r||void 0,children:t.map(n=>f.jsx(by,{depth:0,selectedId:e,tree:n},n.zoneCompound))})})};z();z();var rA={CollapseAll:"_CollapseAll_1r4cy_1","CollapseAll-icon":"_CollapseAll-icon_1r4cy_5","CollapseAll--visible":"_CollapseAll--visible_1r4cy_10"},Lf=ee("CollapseAll",rA);function nA({className:e}){const t=H(i=>{var a;return Object.keys((a=i.state.ui.itemExpanded)!=null?a:{}).length>0}),r=H(i=>i.dispatch),n=J("outline-header-collapseall"),o=()=>{r({type:"setUi",ui:{itemExpanded:{}}})};return f.jsx("div",{className:hy(Lf({visible:t}),e),children:f.jsx(Ke,{title:n,onClick:o,children:f.jsx(C1,{className:Lf("icon")})})})}var oA=nA;z();z();var iA={OutlineHeader:"_OutlineHeader_ntv8r_1"},aA=ee("OutlineHeader",iA),sA=({children:e,title:t})=>{const r=J("outline-header-title");return f.jsxs("div",{className:aA(),children:[f.jsx(Cs,{rank:"2",size:"xs",children:r??t}),e]})},lA=sA;z();var cA={OutlineWrapper:"_OutlineWrapper_b9ln0_1","OutlineWrapper-collapseAll":"_OutlineWrapper-collapseAll_b9ln0_9","OutlineWrapper-layers":"_OutlineWrapper-layers_b9ln0_15"},Ac=ee("OutlineWrapper",cA),uA=({children:e})=>f.jsx("div",{className:Ac(),children:e}),wy=()=>{const e=H(c=>c.overrides.outline),t=H(c=>c.config),r=H(c=>c.state.indexes.nodes),n=H(c=>c.state.indexes.zones),o=H(c=>{var d;return((d=c.selectedItem)==null?void 0:d.props.id)||null}),i=J("label-component"),a=H(Be(c=>hz(c.state,"root"))),s=g.useMemo(()=>a.map(c=>ky({config:t,label:a.length===1?"":c.split(":")[1],nodes:r,zoneCompound:c,zones:n,componentFallbackLabel:i})),[t,r,a,n,i]),l=g.useMemo(()=>e||uA,[e]);return f.jsxs(l,{children:[f.jsx(lA,{children:f.jsx(oA,{className:Ac("collapseAll")})}),f.jsx("div",{className:Ac("layers"),children:f.jsx(tA,{selectedId:o,trees:s})})]})};z();var dA={OutlinePlugin:"_OutlinePlugin_1ylsc_1"},pA=ee("OutlinePlugin",dA),fA=(e={})=>{var t,r;return{name:"outline",label:(t=e.label)!=null?t:"Outline",render:()=>f.jsx("div",{className:pA(),children:f.jsx(wy,{})}),icon:(r=e.icon)!=null?r:f.jsx(Ev,{})}};z();z();z();var hA={Breadcrumbs:"_Breadcrumbs_8c6w5_1","Breadcrumbs-breadcrumbLabel":"_Breadcrumbs-breadcrumbLabel_8c6w5_7","Breadcrumbs-breadcrumb":"_Breadcrumbs-breadcrumb_8c6w5_7"};z();var vA=e=>{const t=H(s=>{var l;return(l=s.selectedItem)==null?void 0:l.props.id}),r=H(s=>s.config),n=H(s=>{var l;return(l=s.state.indexes.nodes[t])==null?void 0:l.path}),o=ye(),i=J("label-page"),a=J("label-component");return g.useMemo(()=>{const s=(n==null?void 0:n.map(l=>{var c,d,u,p;const[v]=l.split(":");if(v==="root")return{label:((c=r==null?void 0:r.root)==null?void 0:c.label)||i,selector:null};const h=o.getState().state.indexes.nodes[v],m=h.path[h.path.length-1],b=(((d=o.getState().state.indexes.zones[m])==null?void 0:d.contentIds)||[]).indexOf(v);return{label:h?(p=(u=r.components[h.data.type])==null?void 0:u.label)!=null?p:h.data.type:a,selector:h?{index:b,zone:h.path[h.path.length-1]}:null}}))||[];return e?s.slice(s.length-e):s},[n,e,i,a])},vl=ee("Breadcrumbs",hA),Sy=({children:e,numParents:t=1})=>{const r=H(o=>o.setUi),n=vA(t);return f.jsxs("div",{className:vl(),children:[n.map((o,i)=>f.jsxs("div",{className:vl("breadcrumb"),children:[f.jsx("button",{type:"button",className:vl("breadcrumbLabel"),onClick:()=>r({itemSelector:o.selector}),children:o.label}),f.jsx(wv,{size:16})]},i)),e]})};z();z();var gA={PuckFields:"_PuckFields_wnj25_1","PuckFields--isLoading":"_PuckFields--isLoading_wnj25_6","PuckFields-loadingOverlay":"_PuckFields-loadingOverlay_wnj25_10","PuckFields-loadingOverlayInner":"_PuckFields-loadingOverlayInner_wnj25_25","PuckFields-field":"_PuckFields-field_wnj25_32","PuckFields--wrapFields":"_PuckFields--wrapFields_wnj25_36"},za=ee("PuckFields",gA),mA=({children:e})=>f.jsx(f.Fragment,{children:e}),_A=(e,t)=>(r,n)=>Se(null,null,function*(){const{dispatch:o,state:i,selectedItem:a,resolveComponentData:s}=t.getState(),{data:l,ui:c}=i,{itemSelector:d}=c,u=l.root.props||l.root,p=a?a.props:u,v=N(D({},p),{[e]:r});if(a&&d){const h=yield s(N(D({},a),{props:v}),"replace"),m=Ri(t.getState().state,a.props.id);if(!m)return;o({type:"replace",destinationIndex:m.index,destinationZone:m.zone||Je,data:h.node,ui:n});return}if(l.root.props){o({type:"replaceRoot",root:(yield s(N(D({},l.root),{props:v}),"replace")).node,ui:D(D({},c),n),recordHistory:!0});return}o({type:"setData",data:{root:v}})}),yA=({fieldName:e})=>{const t=H(c=>c.fields.fields[e]),r=H(c=>((c.selectedItem?c.selectedItem.readOnly:c.state.data.root.readOnly)||{})[e]),n=H(c=>t?c.selectedItem?`${c.selectedItem.props.id}_${t.type}_${e}`:`root_${t.type}_${e}`:null),o=H(Be(c=>{const{selectedItem:d,permissions:u}=c;return d?u.getPermissions({item:d}):u.getPermissions({root:!0})})),i=ye(),a=g.useCallback(_A(e,i),[e]),{visible:s=!0}=t??{},l=g.useContext(Ti.ctx);return g.useEffect(()=>i.subscribe(c=>{var d;return(d=c.getCurrentData().props)==null?void 0:d[e]},c=>{l.setState({[e]:c})}),[i,l]),!t||!n||!s||t.type==="slot"?null:f.jsx("div",{className:za("field"),children:f.jsx(F_,{field:t,name:e,id:n,readOnly:!o.edit||r,onChange:a})},n)},bA=({fieldName:e})=>{const t=ye(),r=g.useMemo(()=>{var n;const o=(n=t.getState().getCurrentData().props)==null?void 0:n[e];return{[e]:o}},[]);return f.jsx(Ti.Provider,{value:r,children:f.jsx(yA,{fieldName:e})})},xA=g.memo(bA),kA=({wrapFields:e=!0})=>{const t=H(d=>d.overrides),r=H(d=>{var u,p;const v=d.selectedItem?(u=d.componentState[d.selectedItem.props.id])==null?void 0:u.loadingCount:(p=d.componentState.root)==null?void 0:p.loadingCount;return(v??0)>0}),n=H(Be(d=>d.state.ui.itemSelector)),o=H(d=>{var u;return(u=d.selectedItem)==null?void 0:u.props.id}),i=ye();bw(i,o);const a=H(d=>d.fields.loading),s=H(Be(d=>d.fields.id===o?Object.keys(d.fields.fields):[])),l=a||r,c=g.useMemo(()=>t.fields||mA,[t]);return f.jsxs("form",{className:za({wrapFields:e}),onSubmit:d=>{d.preventDefault()},children:[f.jsx(c,{isLoading:l,itemSelector:n,children:s.map(d=>f.jsx(xA,{fieldName:d},d))}),l&&f.jsx("div",{className:za("loadingOverlay"),children:f.jsx("div",{className:za("loadingOverlayInner"),children:f.jsx(pn,{size:16})})})]})},Od=g.memo(kA);z();var wA={FieldsPlugin:"_FieldsPlugin_18cj3_1","FieldsPlugin-header":"_FieldsPlugin-header_18cj3_7"},Ff=ee("FieldsPlugin",wA),SA=()=>{const e=J("label-page"),t=H(r=>{var n,o;const i=r.selectedItem;return i?(o=(n=r.config.components[i.type])==null?void 0:n.label)!=null?o:i.type:null});return t??e},EA=({desktopSideBar:e="right",label:t,icon:r}={})=>({name:"fields",label:t??"Fields",render:()=>f.jsxs("div",{className:Ff(),children:[f.jsx("div",{className:Ff("header"),children:f.jsx(Sy,{numParents:2,children:f.jsx(SA,{})})}),f.jsx(Od,{})]}),icon:r??f.jsx(J1,{}),mobileOnly:e==="right"});z();z();z();z();z();var IA=`@import "https://rsms.me/inter/inter.css";

/* styles/color.css */
@layer puck-tokens {
  :root {
    --puck-color-rose-01: #4a001c;
    --puck-color-rose-02: #670833;
    --puck-color-rose-03: #87114c;
    --puck-color-rose-04: #a81a66;
    --puck-color-rose-05: #bc5089;
    --puck-color-rose-06: #cc7ca5;
    --puck-color-rose-07: #d89aba;
    --puck-color-rose-08: #e3b8cf;
    --puck-color-rose-09: #efd6e3;
    --puck-color-rose-10: #f6eaf1;
    --puck-color-rose-11: #faf4f8;
    --puck-color-rose-12: #fef8fc;
    --puck-color-azure-01: #00175d;
    --puck-color-azure-02: #002c77;
    --puck-color-azure-03: #014292;
    --puck-color-azure-04: #0158ad;
    --puck-color-azure-05: #3479be;
    --puck-color-azure-06: #6499cf;
    --puck-color-azure-07: #88b0da;
    --puck-color-azure-08: #abc7e5;
    --puck-color-azure-09: #cfdff0;
    --puck-color-azure-10: #e7eef7;
    --puck-color-azure-11: #f3f6fb;
    --puck-color-azure-12: #f7faff;
    --puck-color-green-01: #002000;
    --puck-color-green-02: #043604;
    --puck-color-green-03: #084e08;
    --puck-color-green-04: #0c680c;
    --puck-color-green-05: #1d882f;
    --puck-color-green-06: #2faa53;
    --puck-color-green-07: #56c16f;
    --puck-color-green-08: #7dd78b;
    --puck-color-green-09: #b8e8bf;
    --puck-color-green-10: #ddf3e0;
    --puck-color-green-11: #eff8f0;
    --puck-color-green-12: #f3fcf4;
    --puck-color-yellow-01: #211000;
    --puck-color-yellow-02: #362700;
    --puck-color-yellow-03: #4c4000;
    --puck-color-yellow-04: #645a00;
    --puck-color-yellow-05: #877614;
    --puck-color-yellow-06: #ab9429;
    --puck-color-yellow-07: #bfac4e;
    --puck-color-yellow-08: #d4c474;
    --puck-color-yellow-09: #e6deb1;
    --puck-color-yellow-10: #f3efd9;
    --puck-color-yellow-11: #f9f7ed;
    --puck-color-yellow-12: #fcfaf0;
    --puck-color-red-01: #4c0000;
    --puck-color-red-02: #6a0a10;
    --puck-color-red-03: #8a1422;
    --puck-color-red-04: #ac1f35;
    --puck-color-red-05: #bf5366;
    --puck-color-red-06: #ce7e8e;
    --puck-color-red-07: #d99ca8;
    --puck-color-red-08: #e4b9c2;
    --puck-color-red-09: #efd7db;
    --puck-color-red-10: #f6eaec;
    --puck-color-red-11: #faf4f5;
    --puck-color-red-12: #fff9fa;
    --puck-color-grey-01: #181818;
    --puck-color-grey-02: #292929;
    --puck-color-grey-03: #404040;
    --puck-color-grey-04: #5a5a5a;
    --puck-color-grey-05: #767676;
    --puck-color-grey-06: #949494;
    --puck-color-grey-07: #ababab;
    --puck-color-grey-08: #c3c3c3;
    --puck-color-grey-09: #dcdcdc;
    --puck-color-grey-10: #efefef;
    --puck-color-grey-11: #f5f5f5;
    --puck-color-grey-12: #fafafa;
    --puck-color-black: #000000;
    --puck-color-white: #ffffff;
  }
}

/* styles/tokens.css */
@layer puck-tokens {
  :root {
    --puck-color-surface: var(--puck-color-white);
    --puck-color-surface-muted: var(--puck-color-grey-11);
    --puck-color-surface-subtle: var(--puck-color-grey-12);
    --puck-color-surface-inverse: var(--puck-color-grey-01);
    --puck-color-border: var(--puck-color-grey-09);
    --puck-color-border-hover: var(--puck-color-grey-05);
    --puck-color-border-muted: var(--puck-color-grey-10);
    --puck-color-border-inverse: var(--puck-color-grey-05);
    --puck-color-text: var(--puck-color-black);
    --puck-color-text-secondary: var(--puck-color-grey-04);
    --puck-color-text-muted: var(--puck-color-grey-05);
    --puck-color-text-subtle: var(--puck-color-grey-07);
    --puck-color-text-inverse: var(--puck-color-white);
    --puck-opacity-text-inverse: 0.75;
    --puck-color-interactive: var(--puck-color-azure-04);
    --puck-color-interactive-hover: var(--puck-color-azure-03);
    --puck-color-interactive-active: var(--puck-color-azure-02);
    --puck-color-interactive-subtle: var(--puck-color-azure-10);
    --puck-color-interactive-soft: var(--puck-color-azure-11);
    --puck-color-interactive-soft-hover: var(--puck-color-azure-12);
    --puck-color-interactive-neutral-hover: var(--puck-color-grey-10);
    --puck-color-interactive-inverse-hover: var(--puck-color-azure-06);
    --puck-color-interactive-inverse-active: var(--puck-color-azure-07);
    --puck-color-focus-ring: var(--puck-color-azure-05);
    --puck-color-selection-bg: color-mix( in srgb, var(--puck-color-azure-09) 30%, transparent );
    --puck-color-selection-border: var(--puck-color-azure-08);
    --puck-color-line-placeholder: var(--puck-color-azure-06);
    --puck-color-highlight: var(--puck-color-rose-07);
    --puck-color-bg-disabled: var(--puck-color-grey-07);
    --puck-color-text-disabled: var(--puck-color-grey-03);
    --puck-color-overlay-backdrop: color-mix( in srgb, var(--puck-color-black) 75%, transparent );
    --puck-space-1: 4px;
    --puck-space-2: 8px;
    --puck-space-3: 12px;
    --puck-space-4: 16px;
    --puck-space-5: 24px;
    --puck-space-chrome-gutter: var(--puck-space-4);
    --puck-radius-none: 0;
    --puck-radius-xs: 2px;
    --puck-radius-s: 3px;
    --puck-radius-m: 4px;
    --puck-radius-l: 8px;
    --puck-radius-pill: 30px;
    --puck-radius-round: 100%;
    --puck-border-width-hairline: 0.5px;
    --puck-border-width-regular: 1px;
    --puck-border-width-focus: 2px;
    --puck-border-width-strong: 4px;
    --puck-duration-fast: 50ms;
    --puck-duration-medium: 150ms;
    --puck-duration-slow: 250ms;
    --puck-ease-exit: ease-in;
    --puck-ease-emphasized: ease-in-out;
    --puck-ease-entrance: ease-out;
    --puck-font-weight-regular: 400;
    --puck-font-weight-medium: 500;
    --puck-font-weight-semibold: 600;
    --puck-font-weight-bold: 700;
    --puck-font-weight-heavy: 800;
    --puck-letter-spacing-ui: 0.05ch;
    --puck-letter-spacing-heading: 0.08ch;
    --puck-icon-size-xs: 14px;
    --puck-icon-size-s: 16px;
    --puck-icon-size-m: 18px;
    --puck-icon-size-l: 24px;
    --puck-space-m-unitless: 24;
    --puck-user-sidebar-left-width: var(--puck-sidebar-width);
    --puck-user-sidebar-right-width: var(--puck-sidebar-width);
    --puck-slot-min-empty-height: 128px;
    --puck-line-placeholder-width: 2px;
  }
}

/* styles/typography.css */
@layer puck-tokens {
  :root {
    --puck-font-size-scale-base-unitless: 12;
    --puck-font-size-xxxs-unitless: 12;
    --puck-font-size-xxs-unitless: 14;
    --puck-font-size-xs-unitless: 16;
    --puck-font-size-s-unitless: 18;
    --puck-font-size-m-unitless: 21;
    --puck-font-size-l-unitless: 24;
    --puck-font-size-xl-unitless: 28;
    --puck-font-size-xxl-unitless: 36;
    --puck-font-size-xxxl-unitless: 48;
    --puck-font-size-xxxxl-unitless: 56;
    --puck-font-size-xxxs: calc( 1rem * var(--puck-font-size-xxxs-unitless) / 16 );
    --puck-font-size-xxs: calc(1rem * var(--puck-font-size-xxs-unitless) / 16);
    --puck-font-size-xs: calc(1rem * var(--puck-font-size-xs-unitless) / 16);
    --puck-font-size-s: calc(1rem * var(--puck-font-size-s-unitless) / 16);
    --puck-font-size-m: calc(1rem * var(--puck-font-size-m-unitless) / 16);
    --puck-font-size-l: calc(1rem * var(--puck-font-size-l-unitless) / 16);
    --puck-font-size-xl: calc(1rem * var(--puck-font-size-xl-unitless) / 16);
    --puck-font-size-xxl: calc(1rem * var(--puck-font-size-xxl-unitless) / 16);
    --puck-font-size-xxxl: calc( 1rem * var(--puck-font-size-xxxl-unitless) / 16 );
    --puck-font-size-xxxxl: calc( 1rem * var(--puck-font-size-xxxxl-unitless) / 16 );
    --puck-font-size-base: var(--puck-font-size-xs);
    --puck-line-height-reset: 1;
    --puck-line-height-xs: calc( var(--puck-space-m-unitless) / var(--puck-font-size-m-unitless) );
    --puck-line-height-s: calc( var(--puck-space-m-unitless) / var(--puck-font-size-s-unitless) );
    --puck-line-height-m: calc( var(--puck-space-m-unitless) / var(--puck-font-size-xs-unitless) );
    --puck-line-height-l: calc( var(--puck-space-m-unitless) / var(--puck-font-size-xxs-unitless) );
    --puck-line-height-xl: calc( var(--puck-space-m-unitless) / var(--puck-font-size-scale-base-unitless) );
    --puck-line-height-base: var(--puck-line-height-m);
    --puck-fallback-font-stack:
      -apple-system,
      BlinkMacSystemFont,
      Segoe UI,
      Helvetica Neue,
      sans-serif,
      Apple Color Emoji,
      Segoe UI Emoji,
      Segoe UI Symbol;
    --puck-font-family: Inter, var(--puck-fallback-font-stack);
    --puck-font-family-monospaced:
      ui-monospace,
      "Cascadia Code",
      "Source Code Pro",
      Menlo,
      Consolas,
      "DejaVu Sans Mono",
      monospace;
  }
  @supports (font-variation-settings: normal) {
    :root {
      --puck-font-family: InterVariable, var(--puck-fallback-font-stack);
    }
  }
}

/* bundle/core.css */
:root {
  --_puck-styles-loaded: "true";
}
#frame-root {
  height: 1px;
  min-height: 100vh;
}
[data-puck-entry] {
  position: relative;
  z-index: 0;
}

/* bundle/index.css */

/* css-module:/home/runner/work/puck/puck/packages/core/components/ActionBar/styles.module.css/#css-module-data */
._ActionBar_5vdfr_1 {
  align-items: center;
  cursor: default;
  display: flex;
  width: auto;
  padding-top: var(--puck-actionbar-space-y, var(--puck-space-1));
  padding-bottom: var(--puck-actionbar-space-y, var(--puck-space-1));
  padding-inline-start: var(--puck-actionbar-space-x, 0);
  padding-inline-end: var(--puck-actionbar-space-x, 0);
  border-radius: var(--puck-actionbar-radius, var(--puck-radius-l));
  background: var(--puck-actionbar-color-bg, var(--puck-color-surface-inverse));
  color: var(--puck-color-text-inverse);
  font-family: var(--puck-font-family);
  min-height: 26px;
}
._ActionBar-label_5vdfr_17 {
  color: var(--puck-actionbar-color-text, var(--puck-color-text-inverse));
  font-size: var(--puck-actionbar-font-size, var(--puck-font-size-xxxs));
  opacity: var(--puck-actionbar-opacity-text, var(--puck-opacity-text-inverse));
  font-weight: var(--puck-font-weight-medium);
  padding-inline-start: var(--puck-space-2);
  padding-inline-end: var(--puck-space-2);
  margin-inline-start: var(--puck-space-1);
  margin-inline-end: var(--puck-space-1);
  text-overflow: ellipsis;
  white-space: nowrap;
}
._ActionBarAction_5vdfr_30 + ._ActionBar-label_5vdfr_17 {
  padding-inline-start: 0;
}
._ActionBar-label_5vdfr_17 + ._ActionBarAction_5vdfr_30 {
  margin-inline-start: calc(var(--puck-space-1) * -1);
}
._ActionBar-group_5vdfr_38 {
  align-items: center;
  border-inline-start: var(--puck-border-width-hairline) solid var(--puck-actionbar-color-separator, var(--puck-color-border-inverse));
  display: flex;
  height: 100%;
  padding-inline-start: var(--puck-space-1);
  padding-inline-end: var(--puck-space-1);
}
._ActionBar-group_5vdfr_38:first-of-type {
  border-inline-start: 0;
}
._ActionBar-group_5vdfr_38:empty {
  display: none;
}
._ActionBarAction_5vdfr_30 {
  background: transparent;
  border: none;
  color: var(--puck-actionbar-color-text, var(--puck-color-text-inverse));
  cursor: pointer;
  padding: var(--puck-actionbar-action-space, 6px);
  margin-inline-start: var(--puck-space-1);
  margin-inline-end: var(--puck-space-1);
  border-radius: var(--puck-radius-m);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: var(--puck-actionbar-opacity-text, var(--puck-opacity-text-inverse));
  transition: color var(--puck-duration-fast) var(--puck-ease-exit), opacity var(--puck-duration-fast) var(--puck-ease-exit);
}
._ActionBarAction--disabled_5vdfr_74 {
  cursor: auto;
  color: var( --puck-actionbar-color-action-disabled, var(--puck-color-text-inverse) );
  opacity: var(--puck-actionbar-opacity-action-disabled, 0.54);
}
._ActionBarAction_5vdfr_30 svg {
  max-width: none !important;
}
._ActionBarAction_5vdfr_30:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: calc(var(--puck-border-width-focus) * -1);
}
@media (hover: hover) and (pointer: fine) {
  ._ActionBarAction_5vdfr_30:hover:not(._ActionBarAction--disabled_5vdfr_74) {
    color: var( --puck-actionbar-color-action-hover, var(--puck-color-interactive-inverse-hover) );
    opacity: 1;
    transition: none;
  }
}
._ActionBarAction_5vdfr_30:active:not(._ActionBarAction--disabled_5vdfr_74),
._ActionBarAction--active_5vdfr_104 {
  color: var( --puck-actionbar-color-action-active, var(--puck-color-interactive-inverse-active) );
  opacity: 1;
  transition: none;
}
._ActionBar-group_5vdfr_38 * {
  margin: 0;
}
._ActionBar-separator_5vdfr_117 {
  background: var( --puck-actionbar-color-separator, var(--puck-color-border-inverse) );
  margin-inline: var(--puck-space-1);
  width: var( --puck-border-width-hairline );
  height: 100%;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/AutoField/styles.module.css/#css-module-data */
._InputWrapper_qyenz_1 + ._InputWrapper_qyenz_1 {
  margin-top: var(--puck-space-3);
}
._Input-label_qyenz_5 {
  align-items: center;
  color: var(--puck-field-label-color-text, var(--puck-color-text-secondary));
  display: flex;
  padding-bottom: var(--puck-field-label-space-y, var(--puck-space-3));
  font-size: var(--puck-field-label-font-size, var(--puck-font-size-xxs));
  font-weight: var( --puck-field-label-font-weight, var(--puck-font-weight-semibold) );
}
._Input-labelIcon_qyenz_17 {
  color: var(--puck-field-label-color-icon, var(--puck-color-text-subtle));
  display: flex;
  margin-inline-end: var(--puck-space-1);
  padding-inline-start: var(--puck-space-1);
}
._Input-disabledIcon_qyenz_24 {
  color: var(--puck-color-text-muted);
  margin-inline-start: auto;
}
._Input-input_qyenz_29 {
  background: var(--puck-field-color-bg, var(--puck-color-surface));
  border-width: var( --puck-field-border-width, var(--puck-border-width-regular) );
  border-style: solid;
  border-color: var(--puck-field-color-border, var(--puck-color-border));
  border-radius: var(--puck-field-radius, var(--puck-radius-m));
  box-sizing: border-box;
  color: var(--puck-field-color-text, var(--puck-color-text));
  font-family: inherit;
  font-size: var(--puck-font-size-xs);
  padding: var(--puck-field-space-y, var(--puck-space-3)) var( --puck-field-space-x, calc( var(--puck-space-4) - var(--puck-field-border-width, var(--puck-border-width-regular)) ) );
  transition: border-color var(--puck-duration-fast) var(--puck-ease-exit);
  width: 100%;
  max-width: 100%;
}
@media (min-width: 458px) {
  ._Input-input_qyenz_29 {
    font-size: var(--puck-field-font-size, var(--puck-font-size-xxs));
  }
}
._Input-select_qyenz_61 {
  position: relative;
  width: 100%;
}
select._Input-input_qyenz_29 {
  appearance: none;
  cursor: pointer;
}
._Input-selectIcon_qyenz_71 {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  fill: var(--puck-field-color-border, var(--puck-color-border));
  stroke-width: 0;
}
._Input-selectIcon_qyenz_71:dir(rtl) {
  right: auto;
  left: 12px;
}
@media (hover: hover) and (pointer: fine) {
  ._Input_qyenz_1:has(> input):hover ._Input-input_qyenz_29:not([readonly]),
  ._Input_qyenz_1:has(> textarea):hover ._Input-input_qyenz_29:not([readonly]) {
    border-color: var( --puck-field-color-border-hover, var(--puck-color-border-hover) );
    transition: none;
  }
  ._Input_qyenz_1:has(> ._Input-select_qyenz_61):hover ._Input-input_qyenz_29:not([disabled]) {
    color: var( --puck-field-color-text-hover, var(--puck-field-color-text, var(--puck-color-text)) );
    background-color: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    border-color: var( --puck-field-color-border-hover, var(--puck-color-border-hover) );
    transition: none;
  }
  ._Input_qyenz_1:not(._Input--readOnly_qyenz_111):has(> ._Input-select_qyenz_61):hover ._Input-selectIcon_qyenz_71 {
    fill: var(--puck-field-color-border-hover, var(--puck-color-border-hover));
  }
}
._Input-input_qyenz_29:focus {
  border-color: var( --puck-field-color-border-hover, var(--puck-color-border-hover) );
  outline: var(--puck-border-width-focus) solid var(--puck-field-color-border-focus, var(--puck-color-focus-ring));
  transition: none;
}
._Input--readOnly_qyenz_111 > ._Input-input_qyenz_29,
._Input--readOnly_qyenz_111 > ._Input-select_qyenz_61 > select._Input-input_qyenz_29 {
  background-color: var( --puck-field-color-bg-disabled, var(--puck-color-surface-muted) );
  border-color: var( --puck-field-color-border-disabled, var(--puck-color-border) );
  color: var( --puck-field-color-text-disabled, var(--puck-color-text-secondary) );
  cursor: default;
  opacity: 1;
  outline: 0;
  transition: none;
}
._Input--readOnly_qyenz_111 > ._Input-select_qyenz_61 > select._Input-input_qyenz_29 ~ ._Input-selectIcon_qyenz_71 {
  fill: var(--puck-field-color-text-disabled, var(--puck-color-text-secondary));
}
._Input-radioGroupItems_qyenz_150 {
  --_puck-field-radio-radius: var(--puck-field-radius, var(--puck-radius-m));
  --_puck-field-radio-border-width: var( --puck-field-border-width, var(--puck-border-width-regular) );
  --_puck-field-radio-border-color: var( --puck-field-color-border, var(--puck-color-border) );
  display: flex;
  border: var(--_puck-field-radio-border-width) solid var(--_puck-field-radio-border-color);
  border-radius: var(--_puck-field-radio-radius);
  flex-wrap: wrap;
}
._Input-radio_qyenz_150 {
  border-inline-end: var(--_puck-field-radio-border-width) solid var(--_puck-field-radio-border-color);
  flex-grow: 1;
}
._Input-radio_qyenz_150:first-of-type {
  border-bottom-left-radius: var(--_puck-field-radio-radius);
  border-top-left-radius: var(--_puck-field-radio-radius);
}
._Input-radio_qyenz_150:first-of-type ._Input-radioInner_qyenz_179 {
  border-bottom-left-radius: calc(var(--_puck-field-radio-radius) - var(--_puck-field-radio-border-width));
  border-top-left-radius: calc(var(--_puck-field-radio-radius) - var(--_puck-field-radio-border-width));
}
._Input-radio_qyenz_150:last-of-type {
  border-bottom-right-radius: var(--_puck-field-radio-radius);
  border-inline-end: 0;
  border-top-right-radius: var(--_puck-field-radio-radius);
}
._Input-radio_qyenz_150:last-of-type ._Input-radioInner_qyenz_179 {
  border-bottom-right-radius: calc(var(--_puck-field-radio-radius) - var(--_puck-field-radio-border-width));
  border-top-right-radius: calc(var(--_puck-field-radio-radius) - var(--_puck-field-radio-border-width));
}
._Input-radioInner_qyenz_179 {
  background-color: var(--puck-field-color-bg, var(--puck-color-surface));
  color: var(--puck-field-color-text, var(--puck-color-text));
  cursor: pointer;
  font-size: var(--puck-field-font-size, var(--puck-font-size-xxs));
  padding: var(--puck-field-space-y, var(--puck-space-3)) var( --puck-field-space-x, calc(var(--puck-space-4) - var(--_puck-field-radio-border-width)) );
  text-align: center;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
}
._Input-radio_qyenz_150:has(:focus-visible) {
  outline: var(--puck-border-width-focus) solid var(--puck-field-color-border-focus, var(--puck-color-focus-ring));
  outline-offset: var(--puck-border-width-focus);
  position: relative;
}
@media (hover: hover) and (pointer: fine) {
  ._Input-radioInner_qyenz_179:hover {
    background-color: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    color: var( --puck-field-color-text-hover, var(--puck-field-color-text, var(--puck-color-text)) );
    transition: none;
  }
}
._Input--readOnly_qyenz_111 ._Input-radioGroupItems_qyenz_150 {
  border-color: var( --puck-field-color-border-disabled, var(--puck-color-border) );
}
._Input--readOnly_qyenz_111 ._Input-radioInner_qyenz_179 {
  background-color: var(--puck-field-color-bg, var(--puck-color-surface));
  color: var(--puck-field-color-text, var(--puck-color-text-secondary));
  cursor: default;
}
._Input--readOnly_qyenz_111 ._Input-radio_qyenz_150 {
  border-inline-end: var(--_puck-field-radio-border-width) solid var(--puck-field-color-border-disabled, var(--puck-color-border));
}
._Input--readOnly_qyenz_111 ._Input-radio_qyenz_150:last-of-type {
  border-inline-end: 0;
}
._Input-radio_qyenz_150 ._Input-radioInput_qyenz_261:checked ~ ._Input-radioInner_qyenz_179 {
  background-color: var( --puck-field-color-bg-active, var(--puck-color-interactive-soft) );
  color: var(--puck-field-color-text-active, var(--puck-color-interactive));
  font-weight: var(--puck-font-weight-medium);
}
._Input--readOnly_qyenz_111 ._Input-radioInput_qyenz_261:checked ~ ._Input-radioInner_qyenz_179 {
  background-color: var( --puck-field-color-bg-disabled, var(--puck-color-surface-muted) );
  color: var( --puck-field-color-text-disabled, var(--puck-color-text-secondary) );
}
._Input-radio_qyenz_150 ._Input-radioInput_qyenz_261 {
  clip: rect(0 0 0 0);
  clip-path: inset(100%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
textarea._Input-input_qyenz_29 {
  margin-bottom: calc(var(--puck-space-1) * -1);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/AutoField/fields/ArrayField/styles.module.css/#css-module-data */
._ArrayField_62huh_5 {
  --_puck-field-array-border-color: var( --puck-field-color-border, var(--puck-color-border) );
  --_puck-field-array-border-width: var( --puck-field-border-width, var(--puck-border-width-regular) );
  --_puck-field-array-radius: var(--puck-field-radius, var(--puck-radius-m));
  --_puck-field-array-radius-inner: calc( var(--_puck-field-array-radius) - var(--_puck-field-array-border-width) );
  display: flex;
  flex-direction: column;
  background: var( --puck-field-color-bg-active, var(--puck-color-interactive-soft) );
  border: var(--_puck-field-array-border-width) solid var(--_puck-field-array-border-color);
  border-radius: var(--_puck-field-array-radius);
}
._ArrayField--isDraggingFrom_62huh_30 {
  background-color: var( --puck-field-color-bg-active, var(--puck-color-interactive-soft) );
  overflow: hidden;
}
._ArrayField-addButton_62huh_38 {
  background-color: var(--puck-field-color-bg, var(--puck-color-surface));
  border: none;
  border-radius: var(--_puck-field-array-radius-inner);
  display: flex;
  color: var(--puck-field-array-add-color-icon, var(--puck-color-interactive));
  justify-content: center;
  cursor: pointer;
  width: 100%;
  margin: 0;
  padding: calc(var(--puck-field-space-y, var(--puck-space-3)) + 2px) var( --puck-field-space-x, calc(var(--puck-space-4) - var(--_puck-field-array-border-width)) );
  text-align: left;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit);
}
._ArrayField--hasItems_62huh_58 > ._ArrayField-addButton_62huh_38 {
  border-top: var(--_puck-field-array-border-width) solid var(--_puck-field-array-border-color);
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
._ArrayField-addButton_62huh_38:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
  position: relative;
}
@media (hover: hover) and (pointer: fine) {
  ._ArrayField_62huh_5:not(._ArrayField--isDraggingFrom_62huh_30) > ._ArrayField-addButton_62huh_38:hover {
    background: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    color: var( --puck-field-color-text-hover, var(--puck-field-color-text, var(--puck-color-text)) );
    transition: none;
  }
}
._ArrayField_62huh_5:not(._ArrayField--isDraggingFrom_62huh_30) > ._ArrayField-addButton_62huh_38:active {
  background: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
  transition: none;
}
._ArrayField-inner_62huh_93 {
  margin-top: -1px;
}
._ArrayFieldItem_62huh_101 {
  display: block;
  position: relative;
  border-top-left-radius: var(--_puck-field-array-radius-inner);
  border-top-right-radius: var(--_puck-field-array-radius-inner);
  border-top: var(--_puck-field-array-border-width) solid var(--_puck-field-array-border-color);
}
._ArrayFieldItem--isDragging_62huh_110 {
  border-top: transparent;
}
._ArrayFieldItem--isExpanded_62huh_114::before {
  display: none;
}
._ArrayFieldItem--isExpanded_62huh_114 {
  border-bottom: 0;
  outline-offset: 0px !important;
  outline: var(--_puck-field-array-border-width) solid var(--puck-field-color-border-focus, var(--puck-color-focus-ring)) !important;
  z-index: 2;
}
._ArrayFieldItem--isDragging_62huh_110 {
  outline: var(--puck-border-width-focus) var(--puck-field-color-border-dragging, var(--puck-color-selection-border)) solid !important;
}
._ArrayFieldItem--isDragging_62huh_110 ._ArrayFieldItem-summary_62huh_132:active {
  background-color: var(--puck-field-color-bg, var(--puck-color-surface));
}
._ArrayFieldItem_62huh_101 + ._ArrayFieldItem_62huh_101 {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
._ArrayFieldItem-summary_62huh_132 {
  --_puck-drag-icon-color: var(--puck-field-color-text, var(--puck-color-text));
  --_puck-drag-icon-color-hover: var( --puck-field-color-text-hover, var(--puck-field-color-text, var(--puck-color-text)) );
  background: var(--puck-field-color-bg, var(--puck-color-surface));
  color: var(--puck-field-color-text, var(--puck-color-text));
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 2px;
  justify-content: space-between;
  font-size: var(--puck-field-font-size, var(--puck-font-size-xxs));
  list-style: none;
  padding: var(--puck-field-space-y, var(--puck-space-3)) var( --puck-field-space-x, calc(var(--puck-space-4) - var(--_puck-field-array-border-width)) );
  position: relative;
  overflow: hidden;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit);
}
._ArrayFieldItem--noFields_62huh_167 > ._ArrayFieldItem-summary_62huh_132 {
  cursor: grab;
}
._ArrayFieldItem_62huh_101:first-of-type > ._ArrayFieldItem-summary_62huh_132 {
  border-top-left-radius: var(--_puck-field-array-radius-inner);
  border-top-right-radius: var(--_puck-field-array-radius-inner);
}
._ArrayField--addDisabled_62huh_176 > ._ArrayField-inner_62huh_93 > ._ArrayFieldItem_62huh_101:last-of-type:not(._ArrayFieldItem--isExpanded_62huh_114) > ._ArrayFieldItem-summary_62huh_132 {
  border-bottom-left-radius: var(--_puck-field-array-radius-inner);
  border-bottom-right-radius: var(--_puck-field-array-radius-inner);
}
._ArrayField--addDisabled_62huh_176 > ._ArrayField-inner_62huh_93 > ._ArrayFieldItem--isExpanded_62huh_114:last-of-type {
  border-bottom-left-radius: var(--_puck-field-array-radius-inner);
  border-bottom-right-radius: var(--_puck-field-array-radius-inner);
}
._ArrayFieldItem-summary_62huh_132:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._ArrayFieldItem-summary_62huh_132:hover {
    background-color: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    color: var( --puck-field-color-text-hover, var(--puck-field-color-text, var(--puck-color-text)) );
    transition: none;
  }
}
._ArrayFieldItem-summary_62huh_132:active {
  background-color: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
  transition: none;
}
._ArrayFieldItem--isExpanded_62huh_114 > ._ArrayFieldItem-summary_62huh_132 {
  background: var( --puck-field-color-bg-active, var(--puck-color-interactive-soft) );
  color: var(--puck-field-color-text-active, var(--puck-color-interactive));
  font-weight: var(--puck-font-weight-semibold);
  transition: none;
}
._ArrayFieldItem-body_62huh_228 {
  background: var(--puck-field-color-surface, var(--puck-color-surface));
  display: none;
}
._ArrayFieldItem--isExpanded_62huh_114 > ._ArrayFieldItem-body_62huh_228 {
  display: block;
}
._ArrayFieldItem-fieldset_62huh_237 {
  border: none;
  border-top: var(--_puck-field-array-border-width) solid var(--_puck-field-array-border-color);
  margin: 0;
  min-width: 0;
  padding: var(--puck-field-space-surface-y, var(--puck-space-4)) var( --puck-field-space-surface-x, calc(var(--puck-space-4) - var(--_puck-field-array-border-width)) );
}
._ArrayFieldItem-rhs_62huh_250 {
  display: flex;
  gap: var(--puck-space-1);
  align-items: center;
}
._ArrayFieldItem-actions_62huh_256 {
  color: var(--puck-color-text-secondary);
  display: flex;
  gap: var(--puck-space-1);
  opacity: 0;
}
._ArrayFieldItem-summary_62huh_132:focus-within > ._ArrayFieldItem-rhs_62huh_250 > ._ArrayFieldItem-actions_62huh_256,
._ArrayFieldItem-summary_62huh_132:hover > ._ArrayFieldItem-rhs_62huh_250 > ._ArrayFieldItem-actions_62huh_256 {
  opacity: 1;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/IconButton/IconButton.module.css/#css-module-data */
._IconButton_1pxxt_1 {
  align-items: center;
  background: var(--puck-iconbutton-color-bg, transparent);
  border: none;
  border-radius: var(--puck-iconbutton-radius, var(--puck-radius-m));
  color: var(--puck-iconbutton-color-icon, currentColor);
  display: flex;
  font-family: var(--puck-font-family);
  justify-content: center;
  padding: var(--puck-iconbutton-space, var(--puck-space-1));
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
}
._IconButton--active_1pxxt_15 {
  color: var( --puck-iconbutton-color-icon-active, var(--puck-color-interactive) );
}
._IconButton_1pxxt_1:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: calc(var(--puck-border-width-focus) * -1);
}
@media (hover: hover) and (pointer: fine) {
  ._IconButton_1pxxt_1:hover:not(._IconButton--disabled_1pxxt_28) {
    background: var( --_puck-iconbutton-color-bg-hover, var( --puck-iconbutton-color-bg-hover, var(--puck-color-interactive-neutral-hover) ) );
    color: var( --puck-iconbutton-color-icon-hover, var(--puck-color-interactive) );
    cursor: pointer;
    transition: none;
  }
}
._IconButton_1pxxt_1:active {
  background: var( --puck-iconbutton-color-bg-active, var(--puck-color-interactive-soft) );
  transition: none;
}
._IconButton--disabled_1pxxt_28 {
  color: var( --puck-iconbutton-color-icon-disabled, var(--puck-color-text-subtle) );
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Loader/styles.module.css/#css-module-data */
@keyframes _loader-animation_1w5zn_1 {
  0% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(0.8);
  }
  100% {
    transform: rotate(360deg) scale(1);
  }
}
._Loader_1w5zn_13 {
  background: transparent;
  border-radius: var(--puck-radius-round);
  border: var(--puck-border-width-focus) solid currentColor;
  border-bottom-color: transparent;
  display: inline-block;
  animation: _loader-animation_1w5zn_1 1s 0s infinite linear;
  animation-fill-mode: both;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/DragIcon/styles.module.css/#css-module-data */
._DragIcon_5e515_1 {
  color: var(--_puck-drag-icon-color, var(--puck-color-text-muted));
  cursor: grab;
  padding: var(--puck-space-1);
  border-radius: var(--puck-radius-m);
}
._DragIcon--disabled_5e515_10 {
  cursor: no-drop;
}
@media (hover: hover) and (pointer: fine) {
  ._DragIcon_5e515_1:not(._DragIcon--disabled_5e515_10):hover {
    color: var(--_puck-drag-icon-color-hover, var(--puck-color-focus-ring));
  }
}

/* components/Sortable/styles.css */
[data-dnd-placeholder]:not([data-puck-line-drag] *) * {
  opacity: 0 !important;
}
[data-dnd-placeholder]:not([data-puck-line-drag] *) {
  background: var( --_puck-field-array-color-placeholder, var(--puck-color-azure-06) ) !important;
  border: none !important;
  color: transparent !important;
  opacity: 0.3 !important;
  outline: none !important;
  transition: none !important;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/ExternalInput/styles.module.css/#css-module-data */
._ExternalInput-actions_143vl_1 {
  display: flex;
}
._ExternalInput-button_143vl_5 {
  display: flex;
  gap: var(--puck-space-2);
  align-items: center;
  justify-content: center;
  background-color: var(--puck-field-color-bg, var(--puck-color-surface));
  border: var(--puck-field-border-width, var(--puck-border-width-regular)) solid var(--puck-field-color-border, var(--puck-color-border));
  border-radius: var(--puck-field-radius, var(--puck-radius-m));
  color: var(--puck-field-color-text-active, var(--puck-color-interactive));
  padding: var(--puck-field-space-y, var(--puck-space-3)) var( --puck-field-space-x, calc( var(--puck-space-4) - var(--puck-field-border-width, var(--puck-border-width-regular)) ) );
  font-size: var(--puck-field-font-size, var(--puck-font-size-xxs));
  font-weight: var(--puck-font-weight-medium);
  white-space: nowrap;
  text-overflow: ellipsis;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit);
  position: relative;
  overflow: hidden;
  flex-grow: 1;
  cursor: pointer;
}
._ExternalInput--dataSelected_143vl_34 ._ExternalInput-button_143vl_5 {
  color: var(--puck-field-color-text, var(--puck-color-text));
  display: block;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
}
._ExternalInput--readOnly_143vl_41 ._ExternalInput-button_143vl_5 {
  background-color: var( --puck-field-color-bg-disabled, var(--puck-color-surface-muted) );
}
._ExternalInput-detachButton_143vl_48 {
  border: var(--puck-field-border-width, var(--puck-border-width-regular)) solid var(--puck-field-color-border, var(--puck-color-border));
  border-top-right-radius: var(--puck-field-radius, var(--puck-radius-m));
  border-bottom-right-radius: var(--puck-field-radius, var(--puck-radius-m));
  background-color: var( --puck-field-external-detach-color-bg, var(--puck-color-surface-subtle) );
  color: var( --puck-field-external-detach-color-text, var(--puck-color-text-muted) );
  display: flex;
  gap: var(--puck-space-2);
  align-items: center;
  justify-content: center;
  padding: var(--puck-space-2) var(--puck-space-3);
  position: relative;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
  margin-inline-start: -1px;
  cursor: pointer;
}
._ExternalInput-button_143vl_5:focus-visible,
._ExternalInput-detachButton_143vl_48:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
  z-index: 1;
}
@media (hover: hover) and (pointer: fine) {
  ._ExternalInput_143vl_1:not(._ExternalInput--readOnly_143vl_41) ._ExternalInput-button_143vl_5:hover,
  ._ExternalInput_143vl_1:not(._ExternalInput--readOnly_143vl_41) ._ExternalInput-detachButton_143vl_48:hover {
    background: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    transition: none;
  }
  ._ExternalInput_143vl_1:not(._ExternalInput--readOnly_143vl_41) ._ExternalInput-detachButton_143vl_48:hover {
    color: var( --puck-field-color-text-hover, var(--puck-field-external-detach-color-text, var(--puck-color-text-muted)) );
  }
  ._ExternalInput--dataSelected_143vl_34:not(._ExternalInput--readOnly_143vl_41) ._ExternalInput-button_143vl_5:hover {
    color: var( --puck-field-color-text-hover, var(--puck-field-color-text, var(--puck-color-text)) );
  }
}
._ExternalInput_143vl_1:not(._ExternalInput--readOnly_143vl_41) ._ExternalInput-button_143vl_5:active,
._ExternalInput_143vl_1:not(._ExternalInput--readOnly_143vl_41) ._ExternalInput-detachButton_143vl_48:active {
  background: var( --puck-field-color-bg-hover, var(--puck-color-interactive-soft-hover) );
  transition: none;
}
._ExternalInputModal_143vl_118 {
  color: var(--puck-color-text);
  display: grid;
  grid-template-rows: min-content minmax(128px, 100%) min-content;
  grid-template-columns: 100%;
  position: relative;
  min-height: 50dvh;
  max-height: 90dvh;
}
._ExternalInputModal-grid_143vl_128 {
  display: flex;
  flex-direction: column;
}
@media (min-width: 458px) {
  ._ExternalInputModal-grid_143vl_128 {
    display: grid;
    grid-template-columns: 100%;
  }
  ._ExternalInputModal--filtersToggled_143vl_139 ._ExternalInputModal-grid_143vl_128 {
    grid-template-columns: 25% 75%;
  }
}
._ExternalInputModal-filters_143vl_144 {
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
}
._ExternalInputModal--filtersToggled_143vl_139 ._ExternalInputModal-filters_143vl_144 {
  display: none;
}
@media (min-width: 458px) {
  ._ExternalInputModal-filters_143vl_144 {
    border-inline-end: var(--puck-border-width-regular) solid var(--puck-color-border);
    display: none;
  }
  ._ExternalInputModal--filtersToggled_143vl_139 ._ExternalInputModal-filters_143vl_144 {
    display: block;
  }
}
._ExternalInputModal-masthead_143vl_164 {
  background-color: var(--puck-color-surface-subtle);
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  display: flex;
  flex-wrap: wrap;
  gap: var(--puck-space-5);
  padding: var(--puck-space-5);
}
._ExternalInputModal-tableWrapper_143vl_173 {
  position: relative;
  overflow-x: auto;
  overflow-y: auto;
  flex-grow: 1;
}
._ExternalInputModal-table_143vl_173 {
  border-collapse: unset;
  border-spacing: 0px;
  color: var(--puck-color-text);
  position: relative;
  z-index: 0;
  min-width: 100%;
}
._ExternalInputModal-thead_143vl_189 {
  background-color: var(--puck-color-surface);
  position: sticky;
  top: 0;
  z-index: 1;
}
._ExternalInputModal-th_143vl_189 {
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  color: var(--puck-color-text-secondary);
  font-weight: var(--puck-font-weight-medium);
  font-size: var(--puck-font-size-xxs);
  padding: var(--puck-space-4) var(--puck-space-5);
}
._ExternalInputModal-td_143vl_204 {
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border-muted);
  padding: var(--puck-space-4) var(--puck-space-5);
}
._ExternalInputModal-tr_143vl_210 ._ExternalInputModal-td_143vl_204:first-of-type {
  font-weight: var(--puck-font-weight-medium);
  width: 1%;
  white-space: nowrap;
}
@media (hover: hover) and (pointer: fine) {
  ._ExternalInputModal-tbody_143vl_217 ._ExternalInputModal-tr_143vl_210:hover {
    background: var(--puck-color-interactive-soft-hover);
    color: var(--puck-color-interactive);
    cursor: pointer;
    position: relative;
    margin-inline-start: -5px;
  }
  ._ExternalInputModal-tbody_143vl_217 ._ExternalInputModal-tr_143vl_210:hover ._ExternalInputModal-td_143vl_204:first-of-type {
    border-inline-start: var(--puck-border-width-strong) solid var(--puck-color-interactive);
    padding-inline-start: 20px;
  }
}
._ExternalInputModal-tbody_143vl_217 ._ExternalInputModal-tr_143vl_210:last-of-type ._ExternalInputModal-td_143vl_204 {
  border-bottom: none;
}
._ExternalInputModal-tableWrapper_143vl_173 {
  display: none;
}
._ExternalInputModal--hasData_143vl_244 ._ExternalInputModal-tableWrapper_143vl_173 {
  display: block;
}
._ExternalInputModal-loadingBanner_143vl_248 {
  display: none;
  background-color: color-mix(in srgb, var(--puck-color-surface) 90%, transparent);
  padding: 64px;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
._ExternalInputModal--isLoading_143vl_265 ._ExternalInputModal-loadingBanner_143vl_248 {
  display: flex;
}
._ExternalInputModal-searchForm_143vl_269 {
  display: flex;
  flex-wrap: wrap;
  gap: var(--puck-space-3);
  flex-grow: 1;
}
@media (min-width: 458px) {
  ._ExternalInputModal-searchForm_143vl_269 {
    flex-wrap: nowrap;
  }
}
._ExternalInputModal-search_143vl_269 {
  display: flex;
  background: var(--puck-color-surface);
  border-width: var(--puck-border-width-regular);
  border-style: solid;
  border-color: var(--puck-color-border);
  border-radius: var(--puck-radius-m);
  flex-grow: 1;
  transition: border-color var(--puck-duration-fast) var(--puck-ease-exit);
}
._ExternalInputModal-search_143vl_269:focus-within {
  border-color: var(--puck-color-border-hover);
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  transition: none;
}
@media (hover: hover) and (pointer: fine) {
  ._ExternalInputModal-search_143vl_269:hover {
    border-color: var(--puck-color-border-hover);
    transition: none;
  }
}
._ExternalInputModal-searchIcon_143vl_306 {
  align-items: center;
  background: var(--puck-color-surface-subtle);
  border-bottom-left-radius: var(--puck-radius-m);
  border-top-left-radius: var(--puck-radius-m);
  border-inline-end: var(--puck-border-width-regular) solid var(--puck-color-border);
  color: var(--puck-color-text-subtle);
  display: flex;
  justify-content: center;
  padding: var(--puck-space-3) calc(var(--puck-space-4) - var(--puck-border-width-regular));
  transition: color var(--puck-duration-fast) var(--puck-ease-exit);
}
._ExternalInputModal-search_143vl_269:focus-within ._ExternalInputModal-searchIcon_143vl_306 {
  color: var(--puck-color-text-secondary);
  transition: none;
}
@media (hover: hover) and (pointer: fine) {
  ._ExternalInputModal-search_143vl_269:hover ._ExternalInputModal-searchIcon_143vl_306 {
    color: var(--puck-color-text-secondary);
    transition: none;
  }
}
._ExternalInputModal-searchIconText_143vl_333 {
  clip: rect(0 0 0 0);
  clip-path: inset(100%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
._ExternalInputModal-searchInput_143vl_343 {
  border: none;
  border-radius: var(--puck-radius-m);
  background: var(--puck-color-surface);
  font-family: inherit;
  font-size: var(--puck-font-size-xxs);
  padding: var(--puck-space-3) calc(var(--puck-space-4) - var(--puck-border-width-regular));
  width: 100%;
}
._ExternalInputModal-searchInput_143vl_343:focus {
  outline: 0;
}
._ExternalInputModal-searchActions_143vl_358 {
  display: flex;
  gap: var(--puck-space-2);
  height: 44px;
  width: 100%;
}
@media (min-width: 458px) {
  ._ExternalInputModal-searchActions_143vl_358 {
    width: auto;
  }
}
._ExternalInputModal-searchActionIcon_143vl_371 {
  align-self: center;
}
._ExternalInputModal-footerContainer_143vl_375 {
  background-color: var(--puck-color-surface-subtle);
  border-top: var(--puck-border-width-regular) solid var(--puck-color-border);
  color: var(--puck-color-text-secondary);
  padding: var(--puck-space-4);
}
._ExternalInputModal-footer_143vl_375 {
  font-weight: var(--puck-font-weight-medium);
  font-size: var(--puck-font-size-xxs);
  text-align: right;
}
._ExternalInputModal-field_143vl_388 {
  color: var(--puck-color-text-secondary);
  margin: var(--puck-space-4);
  margin-bottom: var(--puck-space-3);
  display: block;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Modal/styles.module.css/#css-module-data */
._Modal_g5xob_1 {
  background: var(--puck-color-overlay-backdrop);
  display: none;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 1;
  padding: 32px;
}
._Modal--isOpen_g5xob_15 {
  display: flex;
}
._Modal-inner_g5xob_19 {
  width: 100%;
  max-width: 1024px;
  border-radius: var(--puck-radius-l);
  overflow: hidden;
  background: var(--puck-color-surface);
  display: flex;
  flex-direction: column;
  max-height: 90dvh;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Heading/styles.module.css/#css-module-data */
._Heading_97eh4_1 {
  display: block;
  color: var(--_puck-heading-color, var(--puck-color-text));
  font-weight: var(--puck-font-weight-bold);
  margin: 0;
}
._Heading_97eh4_1 b {
  font-weight: var(--puck-font-weight-bold);
}
._Heading--xxxxl_97eh4_12 {
  font-size: var(--puck-font-size-xxxxl);
  letter-spacing: var(--puck-letter-spacing-heading);
  font-weight: var(--puck-font-weight-heavy);
}
._Heading--xxxl_97eh4_18 {
  font-size: var(--puck-font-size-xxxl);
}
._Heading--xxl_97eh4_22 {
  font-size: var(--puck-font-size-xxl);
}
._Heading--xl_97eh4_26 {
  font-size: var(--puck-font-size-xl);
}
._Heading--l_97eh4_30 {
  font-size: var(--puck-font-size-l);
}
._Heading--m_97eh4_34 {
  font-size: var(--puck-font-size-m);
}
._Heading--s_97eh4_38 {
  font-size: var(--puck-font-size-s);
}
._Heading--xs_97eh4_42 {
  font-size: var(--puck-font-size-xs);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Button/Button.module.css/#css-module-data */
._Button_oe4qj_1 {
  --_puck-button-default-space-x: 20px;
  --_puck-button-default-font-size: var(--puck-font-size-xxs);
  --_puck-button-default-font-weight: var(--puck-font-weight-regular);
  --_puck-button-default-color-bg-disabled: var(--puck-color-bg-disabled);
  --_puck-button-default-color-text-disabled: var(--puck-color-text-disabled);
  appearance: none;
  background: none;
  border: var(--puck-border-width-regular) solid transparent;
  border-radius: var(--puck-button-radius, var(--puck-radius-m));
  color: var(--puck-color-text-inverse);
  display: inline-flex;
  align-items: center;
  gap: var(--puck-space-2);
  letter-spacing: var(--puck-letter-spacing-ui);
  font-family: var(--puck-font-family);
  box-sizing: border-box;
  line-height: 1;
  text-align: center;
  text-decoration: none;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
  cursor: pointer;
  white-space: nowrap;
  margin: 0;
}
._Button_oe4qj_1:hover,
._Button_oe4qj_1:active {
  transition: none;
}
._Button--medium_oe4qj_34 {
  min-height: 34px;
  padding-bottom: var( --puck-button-medium-space-y, calc(var(--puck-space-2) - var(--puck-border-width-regular)) );
  padding-inline-start: var( --puck-button-medium-space-x, calc(var(--_puck-button-default-space-x) - var(--puck-border-width-regular)) );
  padding-inline-end: var( --puck-button-medium-space-x, calc(var(--_puck-button-default-space-x) - var(--puck-border-width-regular)) );
  padding-top: var( --puck-button-medium-space-y, calc(var(--puck-space-2) - var(--puck-border-width-regular)) );
  font-weight: var( --puck-button-medium-font-weight, var(--_puck-button-default-font-weight) );
  font-size: var( --puck-button-medium-font-size, var(--_puck-button-default-font-size) );
}
._Button--large_oe4qj_62 {
  padding-bottom: var( --puck-button-large-space-y, calc(var(--puck-space-3) - var(--puck-border-width-regular)) );
  padding-inline-start: var( --puck-button-large-space-x, calc(var(--_puck-button-default-space-x) - var(--puck-border-width-regular)) );
  padding-inline-end: var( --puck-button-large-space-x, calc(var(--_puck-button-default-space-x) - var(--puck-border-width-regular)) );
  padding-top: var( --puck-button-large-space-y, calc(var(--puck-space-3) - var(--puck-border-width-regular)) );
  font-weight: var( --puck-button-large-font-weight, var(--_puck-button-default-font-weight) );
  font-size: var( --puck-button-large-font-size, var(--_puck-button-default-font-size) );
}
._Button-icon_oe4qj_89 {
  margin-top: 2px;
}
._Button--primary_oe4qj_93 {
  background: var( --puck-button-primary-color-bg, var(--puck-color-interactive) );
  border-color: var(--puck-button-primary-color-border, transparent);
  color: var(--puck-button-primary-color-text, var(--puck-color-text-inverse));
}
._Button_oe4qj_1:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._Button--primary_oe4qj_93:hover {
    background-color: var( --puck-button-primary-color-bg-hover, var(--puck-color-interactive-hover) );
  }
}
._Button--primary_oe4qj_93:active {
  background-color: var( --puck-button-primary-color-bg-active, var(--puck-color-interactive-active) );
}
._Button--primary_oe4qj_93._Button--disabled_oe4qj_123,
._Button--primary_oe4qj_93._Button--disabled_oe4qj_123:hover {
  background-color: var( --puck-button-primary-color-bg-disabled, var(--_puck-button-default-color-bg-disabled) );
  color: var( --puck-button-primary-color-text-disabled, var(--_puck-button-default-color-text-disabled) );
}
._Button--secondary_oe4qj_135 {
  background: var(--puck-button-secondary-color-bg, transparent);
  border-color: var(--puck-button-secondary-color-border, currentColor);
  color: var(--puck-button-secondary-color-text, currentColor);
}
@media (hover: hover) and (pointer: fine) {
  ._Button--secondary_oe4qj_135:hover {
    background-color: var( --puck-button-secondary-color-bg-hover, var(--puck-color-interactive-soft) );
    color: var(--puck-button-secondary-color-text, var(--puck-color-text));
  }
}
._Button--secondary_oe4qj_135:active {
  background-color: var( --puck-button-secondary-color-bg-active, var(--puck-color-interactive-soft) );
  color: var(--puck-button-secondary-color-text, var(--puck-color-text));
}
._Button--secondary_oe4qj_135._Button--disabled_oe4qj_123,
._Button--secondary_oe4qj_135._Button--disabled_oe4qj_123:hover {
  background-color: var( --puck-button-secondary-color-bg-disabled, var(--_puck-button-default-color-bg-disabled) );
  color: var( --puck-button-secondary-color-text-disabled, var(--_puck-button-default-color-text-disabled) );
}
._Button--flush_oe4qj_171 {
  border-radius: var(--puck-radius-none);
}
._Button--disabled_oe4qj_123:hover {
  cursor: not-allowed;
}
._Button--fullWidth_oe4qj_179 {
  justify-content: center;
  width: 100%;
}
._Button-spinner_oe4qj_184 {
  padding-inline-start: var(--puck-space-2);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/RichTextMenu/styles.module.css/#css-module-data */
._RichTextMenu_1ve2j_1 {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}
._RichTextMenu--form_1ve2j_7 {
  border-top-left-radius: var(--puck-field-radius, var(--puck-radius-m));
  border-top-right-radius: var(--puck-field-radius, var(--puck-radius-m));
  padding: var(--puck-field-richtext-menu-space-y, 6px) var(--puck-field-richtext-menu-space-x, 6px);
  background-color: var( --puck-field-richtext-menu-color-bg, var(--puck-color-surface-subtle) );
  position: relative;
  scrollbar-width: none;
  overflow-x: auto;
}
._RichTextMenu-group_1ve2j_21 {
  display: flex;
  align-items: space-between;
  flex-direction: row;
  flex-wrap: nowrap;
  padding-inline: 6px;
  gap: 2px;
  position: relative;
}
._RichTextMenu-group_1ve2j_21:first-of-type {
  padding-left: 0;
}
._RichTextMenu-group_1ve2j_21:last-of-type {
  padding-right: 0;
}
._RichTextMenu--inline_1ve2j_39 ._RichTextMenu-group_1ve2j_21 {
  color: var(--puck-color-text-inverse);
  gap: 0px;
  flex-wrap: nowrap;
}
._RichTextMenu-group_1ve2j_21 + ._RichTextMenu-group_1ve2j_21 {
  border-left: var(--puck-border-width-regular) solid var( --puck-field-richtext-menu-color-separator, var(--puck-color-border-muted) );
}
._RichTextMenu--inline_1ve2j_39 ._RichTextMenu-group_1ve2j_21 + ._RichTextMenu-group_1ve2j_21 {
  border-left: var(--puck-border-width-hairline) solid var(--puck-color-border-inverse);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/RichTextMenu/components/Control/styles.module.css/#css-module-data */
._Control_id4pm_1 .lucide {
  height: var(--puck-icon-size-m);
  width: var(--puck-icon-size-m);
}
._Control--inline_id4pm_6 .lucide {
  height: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
  width: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Select/styles.module.css/#css-module-data */
._Select_1n4iv_1 {
  position: relative;
  z-index: 1;
}
._Select-buttonInner_1n4iv_6 {
  align-items: center;
  display: flex;
}
._Select-buttonIcon_1n4iv_11 {
  align-items: center;
  display: flex;
  justify-content: center;
}
._Select--standalone_1n4iv_17 ._Select-buttonIcon_1n4iv_11 .lucide {
  height: var(--puck-icon-size-m);
  width: var(--puck-icon-size-m);
}
._Select--actionBar_1n4iv_22 ._Select-buttonIcon_1n4iv_11 .lucide {
  height: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
  width: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
}
._Select-items_1n4iv_27 {
  background: var(--puck-color-surface);
  border: var(--puck-border-width-regular) solid var(--puck-color-border);
  border-radius: var(--puck-radius-l);
  margin: 10px 8px;
  margin-left: 0;
  padding: var(--puck-space-1);
  z-index: 2;
  list-style: none;
}
._SelectItem_1n4iv_38 {
  background: transparent;
  border-radius: var(--puck-radius-m);
  border: none;
  color: var(--puck-color-text-secondary);
  cursor: pointer;
  display: flex;
  gap: var(--puck-space-2);
  align-items: center;
  font-size: var(--puck-font-size-xxs);
  margin: 0;
  padding: var(--puck-space-2) var(--puck-space-3);
  width: 100%;
}
._SelectItem--isSelected_1n4iv_53 {
  background: var(--puck-color-interactive-soft);
  color: var(--puck-color-interactive);
  font-weight: var(--puck-font-weight-medium);
}
._SelectItem--isSelected_1n4iv_53 ._SelectItem-icon_1n4iv_59 {
  color: var(--puck-color-interactive);
}
._SelectItem_1n4iv_38:hover {
  background: var(--puck-color-interactive-soft);
  color: var(--puck-color-interactive);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/RichTextEditor/styles.module.css/#css-module-data */
._RichTextEditor_5wzos_1 .ProseMirror {
  white-space: pre-wrap;
  word-wrap: break-word;
  cursor: text;
  outline: none;
  position: relative;
}
._RichTextEditor_5wzos_1 .rich-text * {
  white-space: pre-wrap;
  user-select: auto;
  -webkit-user-select: auto;
}
._RichTextEditor_5wzos_1 .rich-text blockquote {
  margin: 1em 0;
  padding: 0 1em;
  border-left: var(--puck-border-width-strong) solid var(--puck-color-border);
}
._RichTextEditor_5wzos_1 .rich-text code {
  background-color: var(--puck-color-surface-muted);
  padding: var(--puck-space-1) var(--puck-space-2);
  border-radius: var(--puck-radius-m);
}
._RichTextEditor_5wzos_1 .rich-text p:empty::before {
  content: "\\a0";
}
._RichTextEditor_5wzos_1 .rich-text pre code {
  display: block;
  padding: var(--puck-space-2) var(--puck-space-3);
}
._RichTextEditor_5wzos_1 .rich-text > *:first-child,
._RichTextEditor_5wzos_1 .ProseMirror > *:first-child,
._RichTextEditor_5wzos_1 .rich-text * p:first-of-type {
  margin-top: 0;
}
._RichTextEditor_5wzos_1 .rich-text > *:last-child,
._RichTextEditor_5wzos_1 .ProseMirror > *:last-child,
._RichTextEditor_5wzos_1 .rich-text * p:last-of-type {
  margin-bottom: 0;
}
._RichTextEditor--editor_5wzos_50 {
  color: var(--puck-field-color-text, var(--puck-color-text));
  background: var(--puck-field-color-bg, var(--puck-color-surface));
  border-width: var( --puck-field-border-width, var(--puck-border-width-regular) );
  border-style: solid;
  border-color: var(--puck-field-color-border, var(--puck-color-border));
  border-radius: var(--puck-field-radius, var(--puck-radius-m));
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  font-family: inherit;
  font-size: var(--puck-field-font-size, var(--puck-font-size-xxs));
  resize: vertical;
  text-align: initial;
  transition: border-color var(--puck-duration-fast) var(--puck-ease-exit);
  width: 100%;
  max-width: 100%;
  min-height: 128px;
}
._RichTextEditor--editor_5wzos_50 .rich-text {
  flex-grow: 1;
}
._RichTextEditor--editor_5wzos_50 .rich-text:not(:has(.ProseMirror)),
._RichTextEditor--editor_5wzos_50 .rich-text .ProseMirror {
  height: 100%;
  padding: var(--puck-field-space-y, var(--puck-space-3)) var( --puck-field-space-x, calc( var(--puck-space-4) - var(--puck-field-border-width, var(--puck-border-width-regular)) ) );
}
._RichTextEditor--editor_5wzos_50 .rich-text ul,
._RichTextEditor--editor_5wzos_50 .rich-text ol {
  padding-left: var(--puck-space-5);
}
._RichTextEditor--editor_5wzos_50 .rich-text li {
  line-height: 1.5;
}
._RichTextEditor--editor_5wzos_50 .rich-text p {
  margin-block: var(--puck-space-3);
}
._RichTextEditor--editor_5wzos_50 .rich-text ul {
  list-style: disc;
}
._RichTextEditor--editor_5wzos_50 .rich-text ol {
  list-style: decimal;
}
._RichTextEditor--editor_5wzos_50:focus-within {
  border-color: var( --puck-field-color-border-hover, var(--puck-color-border-hover) );
  outline: var(--puck-border-width-focus) solid var(--puck-field-color-border-focus, var(--puck-color-focus-ring));
  transition: none;
}
@media (hover: hover) and (pointer: fine) {
  ._RichTextEditor--editor_5wzos_50:hover:not(._RichTextEditor--disabled_5wzos_123) {
    border-color: var( --puck-field-color-border-hover, var(--puck-color-border-hover) );
    transition: none;
  }
}
._RichTextEditor--editor_5wzos_50._RichTextEditor--disabled_5wzos_123 {
  background: var( --puck-field-color-bg-disabled, var(--puck-color-surface-muted) );
  border-color: var( --puck-field-color-border-disabled, var(--puck-color-border) );
}
._RichTextEditor--editor_5wzos_50._RichTextEditor--disabled_5wzos_123 .rich-text:not(:has(.ProseMirror)),
._RichTextEditor--editor_5wzos_50._RichTextEditor--disabled_5wzos_123 .rich-text .ProseMirror {
  color: var( --puck-field-color-text-disabled, var(--puck-color-text-secondary) );
}
._RichTextEditor--editor_5wzos_50._RichTextEditor--disabled_5wzos_123 .ProseMirror[contenteditable=false] {
  cursor: default;
}
._RichTextEditor_5wzos_1:not(:focus-within):not(._RichTextEditor--isActive_5wzos_159) .ProseMirror ::selection {
  background-color: transparent;
}
._RichTextEditor-menu_5wzos_165 {
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border-muted);
  position: sticky;
  top: 0;
  z-index: 1;
}
._RichTextEditor--disabled_5wzos_123 ._RichTextEditor-menu_5wzos_165 {
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/AutoField/fields/ObjectField/styles.module.css/#css-module-data */
._ObjectField_c5reb_1 {
  display: flex;
  flex-direction: column;
  background-color: var(--puck-field-color-surface, var(--puck-color-surface));
  border: var(--puck-field-border-width, var(--puck-border-width-regular)) solid var(--puck-field-color-border, var(--puck-color-border));
  border-radius: var(--puck-field-radius, var(--puck-radius-m));
}
._ObjectField-fieldset_c5reb_10 {
  border: none;
  margin: 0;
  min-width: 0;
  padding: var(--puck-field-space-surface-y, var(--puck-space-4)) var( --puck-field-space-surface-x, calc( var(--puck-space-4) - var(--puck-field-border-width, var(--puck-border-width-regular)) ) );
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Drawer/styles.module.css/#css-module-data */
._Drawer_1n90m_1 {
  display: flex;
  flex-direction: column;
  font-family: var(--puck-font-family);
  gap: var(--puck-space-3);
}
._Drawer-draggable_1n90m_8 {
  position: relative;
}
._Drawer-draggableBg_1n90m_12 {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  pointer-events: none;
  z-index: -1;
}
._DrawerItem-draggable_1n90m_22 {
  background: var(--puck-drawer-item-color-bg, var(--puck-color-surface));
  color: var(--puck-drawer-item-color-text, var(--puck-color-text));
  cursor: grab;
  padding: var(--puck-drawer-item-space, var(--puck-space-3));
  display: flex;
  border: var(--puck-drawer-item-border-width, var(--puck-border-width-regular)) var(--puck-drawer-item-color-border, var(--puck-color-border)) solid;
  border-radius: var(--puck-drawer-item-radius, var(--puck-radius-m));
  font-size: var(--puck-drawer-item-font-size, var(--puck-font-size-xxs));
  justify-content: space-between;
  align-items: center;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
}
._DrawerItem--disabled_1n90m_38 ._DrawerItem-draggable_1n90m_22 {
  background: var(--puck-color-surface-muted);
  color: var(--puck-color-text-muted);
  cursor: not-allowed;
}
._DrawerItem_1n90m_22:focus-visible {
  outline: 0;
}
._Drawer_1n90m_1:not(._Drawer--isDraggingFrom_1n90m_48) ._DrawerItem_1n90m_22:focus-visible ._DrawerItem-draggable_1n90m_22 {
  border-radius: var(--puck-radius-m);
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._Drawer_1n90m_1:not(._Drawer--isDraggingFrom_1n90m_48) ._DrawerItem_1n90m_22:not(._DrawerItem--disabled_1n90m_38) ._DrawerItem-draggable_1n90m_22:hover {
    background-color: var( --puck-drawer-item-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    color: var( --puck-drawer-item-color-text-hover, var(--puck-color-interactive) );
    transition: none;
  }
}
._DrawerItem-name_1n90m_72 {
  overflow-x: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/DraggableComponent/styles.module.css/#css-module-data */
._DraggableComponent_1627v_1 {
  position: absolute;
  pointer-events: none;
}
._DraggableComponent-overlayWrapper_1627v_6 {
  height: 100%;
  width: 100%;
  top: 0;
  position: absolute;
  pointer-events: none;
  box-sizing: border-box;
  z-index: 1;
}
._DraggableComponent-overlay_1627v_6 {
  cursor: pointer;
  height: 100%;
  outline: var( --puck-slot-component-border-width, var(--puck-border-width-focus) ) var( --puck-slot-component-color-overlay-border, var(--puck-color-selection-border) ) solid;
  outline-offset: calc(var(--puck-slot-component-border-width, var(--puck-border-width-focus)) * -1);
  width: 100%;
}
._DraggableComponent_1627v_1:focus-visible > ._DraggableComponent-overlayWrapper_1627v_6 {
  outline: var(--puck-border-width-regular) solid var(--puck-color-focus-ring);
}
._DraggableComponent-loadingOverlay_1627v_38 {
  background: var(--puck-color-surface);
  color: var(--puck-color-text);
  border-radius: var(--puck-radius-m);
  display: flex;
  padding: var(--puck-space-2);
  top: var(--puck-space-2);
  right: var(--puck-space-2);
  position: absolute;
  z-index: 1;
  pointer-events: all;
  box-sizing: border-box;
  opacity: 0.8;
  z-index: 1;
}
._DraggableComponent--hover_1627v_54 > ._DraggableComponent-overlayWrapper_1627v_6 > ._DraggableComponent-overlay_1627v_6 {
  background: var( --puck-slot-component-color-overlay, var(--puck-color-selection-bg) );
  outline: var( --puck-slot-component-border-width, var(--puck-border-width-focus) ) var( --puck-slot-component-color-overlay-border, var(--puck-color-selection-border) ) solid;
}
._DraggableComponent--isSelected_1627v_72 > ._DraggableComponent-overlayWrapper_1627v_6 > ._DraggableComponent-overlay_1627v_6 {
  outline-color: var( --puck-slot-component-color-border-selected, var(--puck-color-selection-border) );
}
._DraggableComponent_1627v_1:has(._DraggableComponent--hover_1627v_54 > ._DraggableComponent-overlayWrapper_1627v_6) > ._DraggableComponent-overlayWrapper_1627v_6 {
  display: none;
}
._DraggableComponent-actionsOverlay_1627v_89 {
  position: sticky;
  opacity: 0;
  pointer-events: none;
  z-index: 2;
}
._DraggableComponent--isSelected_1627v_72 ._DraggableComponent-actionsOverlay_1627v_89 {
  opacity: 1;
  pointer-events: auto;
}
._DraggableComponent-actions_1627v_89 {
  position: absolute;
  width: auto;
  cursor: grab;
  display: flex;
  box-sizing: border-box;
  transform-origin: right top;
  min-height: 36px;
}
._DraggableComponent-actionsAction_1627v_111 {
  height: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
  width: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
}

/* components/DraggableComponent/styles.css */
[data-puck-component] * {
  pointer-events: none;
  user-select: none;
  -webkit-user-select: none;
}
[data-puck-component] {
  cursor: grab;
  pointer-events: auto !important;
  user-select: none;
  -webkit-user-select: none;
}
[data-puck-dropzone] {
  pointer-events: auto !important;
}
[data-puck-disabled] {
  cursor: pointer;
}
[data-dnd-placeholder]:not([data-puck-line-drag] *) {
  background: var( --puck-slot-component-color-placeholder, var(--puck-color-azure-06) ) !important;
  border: none !important;
  color: transparent !important;
  opacity: 0.3 !important;
  outline: none !important;
  transition: none !important;
}
[data-dnd-placeholder]:not([data-puck-line-drag] *) *,
[data-dnd-placeholder]:not([data-puck-line-drag] *)::after,
[data-dnd-placeholder]:not([data-puck-line-drag] *)::before {
  opacity: 0 !important;
}
[data-puck-line-drag] [data-dnd-placeholder] {
  opacity: 0.4 !important;
  outline: none !important;
  transition: none !important;
}
[data-puck-line-drag] [data-dnd-dragging][data-puck-component] {
  opacity: 0.9 !important;
}
[data-dnd-dragging][data-puck-component] {
  pointer-events: none !important;
  outline: var( --puck-slot-component-border-width, var(--puck-border-width-focus) ) var(--puck-slot-component-color-border-dragging, var(--puck-color-azure-09)) solid !important;
  outline-offset: calc(var(--puck-slot-component-border-width, var(--puck-border-width-focus)) * -1) !important;
}
[data-dnd-dragging][data-puck-component] > :first-child {
  margin-top: 0 !important;
}
[data-dnd-dragging][data-puck-component] > :last-child {
  margin-bottom: 0 !important;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/DropZone/styles.module.css/#css-module-data */
._DropZone_wc2ks_1 {
  position: relative;
  height: 100%;
  min-height: var(--puck-slot-min-empty-height);
  outline-offset: calc(var(--puck-slot-border-width, var(--puck-border-width-focus)) * -1);
  width: 100%;
}
._DropZone--hasChildren_wc2ks_11 {
  min-height: 0;
}
._DropZone_wc2ks_1:empty {
  min-height: var(--puck-slot-min-empty-height);
}
[data-puck-entry]:not([data-puck-dragging]) ._DropZone_wc2ks_1 {
  transition: min-height var(--puck-duration-medium) var(--puck-ease-exit);
}
._DropZone--isAreaSelected_wc2ks_24,
._DropZone--hoveringOverArea_wc2ks_25:not(._DropZone--isRootZone_wc2ks_25) {
  background: var(--puck-slot-color-bg, var(--puck-color-selection-bg));
  outline: var(--puck-slot-border-width, var(--puck-border-width-focus)) var(--puck-slot-border-style, dashed) var(--puck-slot-color-border, var(--puck-color-selection-border));
}
._DropZone_wc2ks_1:empty {
  background: var(--puck-slot-color-bg, var(--puck-color-selection-bg));
  outline: var(--puck-slot-border-width, var(--puck-border-width-focus)) var(--puck-slot-border-style, dashed) var(--puck-slot-color-border, var(--puck-color-selection-border));
}
._DropZone-item_wc2ks_39 {
  position: relative;
}
._DropZone-linePlaceholder_wc2ks_43 {
  background: var( --puck-slot-component-color-placeholder, var(--puck-color-line-placeholder) );
  border-radius: calc(var(--puck-line-placeholder-width, 2px) / 2);
  pointer-events: none;
  position: absolute;
  z-index: 1;
}
._DropZone-hitbox_wc2ks_55 {
  position: absolute;
  bottom: calc(var(--puck-space-3) * -1);
  height: var(--puck-space-5);
  width: 100%;
  z-index: 1;
}
[data-puck-dragging] ._DropZone--isEnabled_wc2ks_63 {
  outline: var(--puck-slot-border-width, var(--puck-border-width-focus)) var(--puck-slot-border-style, dashed) var(--puck-slot-color-border, var(--puck-color-selection-border));
}
._DropZone_wc2ks_1 > *:not([data-puck-component]):not([data-puck-line-placeholder]) {
  opacity: 0;
}
body:has(._DropZone--isAnimating_wc2ks_74:empty) [data-puck-overlay] {
  opacity: 0 !important;
}

/* lib/overlay-portal/styles.css */
[data-puck-overlay-portal],
[data-puck-overlay-portal] * {
  pointer-events: auto !important;
}
[data-puck-entry][data-puck-dragging] [data-puck-overlay-portal],
[data-puck-entry][data-puck-dragging] [data-puck-overlay-portal] * {
  pointer-events: none !important;
}
[data-puck-entry][data-puck-preview-mode=edit] [data-puck-overlay-portal]:hover {
  outline: 2px var(--puck-color-azure-09, #cfdff0) dashed;
  outline-offset: 2px;
}
[data-puck-entry][data-puck-preview-mode=edit] [data-puck-overlay-portal]:focus-within {
  outline: 2px var(--puck-color-azure-07, #88b0da) dashed;
  outline-offset: 2px;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/InlineTextField/styles.module.css/#css-module-data */
._InlineTextField_104qp_1 {
  cursor: text;
  display: inline-block;
  white-space: pre-wrap;
  text-decoration: inherit;
}
[data-dnd-dragging] ._InlineTextField_104qp_1 {
  cursor: none;
  caret-color: transparent;
}
[data-dnd-dragging] ._InlineTextField_104qp_1::selection {
  display: none;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Fields/styles.module.css/#css-module-data */
._PuckFields_wnj25_1 {
  position: relative;
  font-family: var(--puck-font-family);
}
._PuckFields--isLoading_wnj25_6 {
  min-height: 48px;
}
._PuckFields-loadingOverlay_wnj25_10 {
  background: var(--puck-color-surface);
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  height: 100%;
  width: 100%;
  top: 0px;
  position: absolute;
  z-index: 1;
  pointer-events: all;
  box-sizing: border-box;
  opacity: 0.8;
}
._PuckFields-loadingOverlayInner_wnj25_25 {
  display: flex;
  padding: var(--puck-space-4);
  position: sticky;
  top: 0;
}
._PuckFields-field_wnj25_32 * {
  box-sizing: border-box;
}
._PuckFields--wrapFields_wnj25_36 ._PuckFields-field_wnj25_32 {
  color: var(--puck-color-text-secondary);
  padding: var(--puck-space-4);
  padding-bottom: var(--puck-space-3);
  display: block;
}
._PuckFields--wrapFields_wnj25_36 ._PuckFields-field_wnj25_32 + ._PuckFields-field_wnj25_32 {
  border-top: var(--puck-border-width-regular) solid var(--puck-color-border);
  margin-top: var(--puck-space-2);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/ComponentList/styles.module.css/#css-module-data */
._ComponentList_htktj_1 {
  max-width: 100%;
}
._ComponentList--isExpanded_htktj_5 + ._ComponentList_htktj_1 {
  margin-top: var(--puck-space-3);
}
._ComponentList-content_htktj_9 {
  display: none;
}
._ComponentList--isExpanded_htktj_5 > ._ComponentList-content_htktj_9 {
  display: block;
}
._ComponentList-title_htktj_17 {
  background-color: transparent;
  border: 0;
  color: var(--puck-drawer-category-color-text, var(--puck-color-text-muted));
  cursor: pointer;
  display: flex;
  font: inherit;
  font-size: var(--puck-drawer-category-font-size, var(--puck-font-size-xxxs));
  list-style: none;
  margin-bottom: 6px;
  padding: var(--puck-drawer-category-space, var(--puck-space-2));
  text-transform: uppercase;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
  gap: var(--puck-space-1);
  border-radius: var(--puck-radius-m);
  width: 100%;
}
._ComponentList-title_htktj_17:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._ComponentList-title_htktj_17:hover {
    background-color: var( --puck-drawer-category-color-bg-hover, var(--puck-color-interactive-soft) );
    color: var( --puck-drawer-category-color-text-hover, var(--puck-color-interactive) );
    transition: none;
  }
}
._ComponentList-title_htktj_17:active {
  background-color: var( --puck-drawer-category-color-bg-active, var(--puck-color-interactive-subtle) );
  transition: none;
}
._ComponentList-titleIcon_htktj_63 {
  margin-inline-start: auto;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Preview/styles.module.css/#css-module-data */
._PuckPreview_zbic3_1 {
  position: relative;
  height: 100%;
}
._PuckPreview-frame_zbic3_6 {
  border: none;
  height: 100%;
  width: 100%;
}
._PuckPreview-frame_zbic3_6[data-puck-outline-dragging] {
  pointer-events: none;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/components/drop-line/styles.module.css/#css-module-data */
._DropLine_eyz3q_2 {
  background: var(--_puck-outline-color-drop-indicator);
  border-radius: calc(var(--_puck-outline-drop-indicator-size) / 2);
  height: var(--_puck-outline-drop-indicator-size);
  inset-inline: 0;
  pointer-events: none;
  position: absolute;
  z-index: 1;
}
._DropLine--top_eyz3q_12 {
  top: 0;
}
._DropLine--bottom_eyz3q_16 {
  bottom: 0;
}
._DropLine--top_eyz3q_12._DropLine--outset_eyz3q_20 {
  top: calc(-1 * var(--_puck-outline-drop-indicator-size));
}
._DropLine--bottom_eyz3q_16._DropLine--outset_eyz3q_20 {
  bottom: calc(-1 * var(--_puck-outline-drop-indicator-size));
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/components/empty-zone-placeholder/styles.module.css/#css-module-data */
._LayerTree-helper_1m7e4_2 {
  color: var(--puck-outline-color-text-helper, var(--puck-color-text-subtle));
  padding-top: var(--puck-space-1);
  padding-bottom: var(--puck-space-1);
  padding-inline-start: var(--_puck-outline-label-indent);
  border: var(--_puck-outline-border-width) solid transparent;
}
._LayerTree-helperRoot_1m7e4_11 {
  padding-inline-start: var(--puck-space-3);
}
._LayerTree-helper_1m7e4_2[data-puck-drop-target] {
  position: relative;
  overflow: visible;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/components/layer/styles.module.css/#css-module-data */
._Layer_onfgu_1 {
  position: relative;
  border: var(--_puck-outline-border-width) solid transparent;
  border-radius: var(--_puck-outline-radius);
}
._Layer-inner_onfgu_8 {
  align-items: center;
  border: var(--_puck-outline-border-width) solid transparent;
  border-radius: var(--_puck-outline-radius);
  cursor: pointer;
  display: flex;
  position: relative;
  transition: color var(--puck-duration-fast) var(--puck-ease-exit);
}
._Layer--isSortable_onfgu_18 > ._Layer-inner_onfgu_8 {
  cursor: grab;
}
._Layer-content_onfgu_22 {
  display: flex;
  gap: var(--puck-space-4);
  flex: 1 1 auto;
  min-width: 0;
}
._Layer-clickable_onfgu_29 {
  align-items: center;
  background: none;
  border: 0;
  border-radius: var(--_puck-outline-radius);
  color: inherit;
  cursor: inherit;
  display: flex;
  flex: 1 1 auto;
  font: inherit;
  min-width: 0;
  padding: 0;
}
[data-puck-dnd-disabled] ._Layer-inner_onfgu_8,
[data-puck-dnd-disabled] ._Layer-clickable_onfgu_29 {
  cursor: pointer;
}
._Layer-clickable_onfgu_29:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
  position: relative;
  z-index: 1;
}
._Layer-caret_onfgu_57 {
  visibility: hidden;
  display: flex;
  flex-shrink: 0;
}
._Layer-caret_onfgu_57 svg {
  height: var(--_puck-outline-caret-size);
  width: var(--_puck-outline-caret-size);
}
._Layer--containsZone_onfgu_68 > ._Layer-inner_onfgu_8 > ._Layer-content_onfgu_22 {
  font-weight: var(--puck-font-weight-bold);
}
._Layer--containsZone_onfgu_68 > ._Layer-inner_onfgu_8 > ._Layer-caret_onfgu_57 {
  visibility: visible;
}
._Layer-title_onfgu_76 {
  display: flex;
  gap: var(--puck-space-2);
  align-items: center;
  overflow-x: hidden;
  margin: var(--puck-space-1);
  cursor: pointer;
}
._Layer-name_onfgu_85 {
  overflow-x: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
._Layer-icon_onfgu_91 {
  color: var(--puck-outline-color-icon, var(--puck-color-text-subtle));
  margin-top: var(--puck-space-1);
}
._Layer-icon_onfgu_91 svg {
  height: var(--_puck-outline-icon-size);
  width: var(--_puck-outline-icon-size);
}
._Layer-zones_onfgu_101 {
  display: none;
  margin-inline-start: var(--puck-outline-space-indent, var(--puck-space-4));
}
._Layer--isExpanded_onfgu_106 > ._Layer-zones_onfgu_101 {
  display: block;
}
._Layer--isExpanded_onfgu_106 > ._Layer-inner_onfgu_8 > ._Layer-caret_onfgu_57 svg {
  transform: rotate(90deg);
}
@media (hover: hover) and (pointer: fine) {
  ._Layer_onfgu_1:not(._Layer--isSelected_onfgu_115) > ._Layer-inner_onfgu_8:hover {
    --_puck-outline-actions-color-bg: var(--_puck-outline-color-bg-hover);
    border-color: var(--_puck-outline-color-border-hover);
    background: var(--_puck-outline-color-bg-hover);
    transition: none;
  }
}
._Layer--isSelected_onfgu_115 > ._Layer-inner_onfgu_8 {
  border-color: var( --puck-outline-color-border-selected, var(--puck-color-selection-border) );
}
._Layer--isSelected_onfgu_115 > ._Layer-inner_onfgu_8 {
  --_puck-outline-actions-color-bg: var(--_puck-outline-color-bg-selected);
  background: var(--_puck-outline-color-bg-selected);
}
._Layer--isExpandCandidate_onfgu_138 > ._Layer-inner_onfgu_8 {
  border-color: var(--_puck-outline-color-border-hover);
  background: var(--_puck-outline-color-bg-hover);
}
._Layer--isDragSource_onfgu_143 > ._Layer-inner_onfgu_8 {
  color: var(--puck-color-text-muted);
  background: transparent;
}
._Layer--isDragSource_onfgu_143 > ._Layer-zones_onfgu_101 {
  opacity: 0.5;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/components/layer-actions/styles.module.css/#css-module-data */
._LayerActions_d90t9_2 {
  position: sticky;
  inset-inline-end: calc(var(--puck-space-1) * -1);
  padding-inline: var(--puck-space-1);
  display: flex;
  visibility: hidden;
  flex-shrink: 0;
  color: var(--_puck-outline-color-text);
  background: var(--_puck-outline-actions-color-bg);
  border-top-right-radius: var(--_puck-outline-radius);
  border-bottom-right-radius: var(--_puck-outline-radius);
}
._LayerActions--visible_d90t9_18 {
  visibility: visible;
}
._LayerActions_d90t9_2 svg {
  height: var(--_puck-outline-caret-size);
  width: var(--_puck-outline-caret-size);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/components/layer-tree-items/styles.module.css/#css-module-data */
._LayerTree_o5tyt_1 {
  color: var(--_puck-outline-color-text);
  font-family: var(--puck-outline-font-family, var(--puck-font-family));
  font-size: var(--puck-outline-font-size, var(--puck-font-size-xxxs));
  margin: 0;
  position: relative;
  list-style: none;
  padding: 0;
}
._LayerTree--nested_o5tyt_12 {
  margin-inline-start: var(--puck-outline-space-indent, var(--puck-space-3));
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/components/layer-tree-zone/styles.module.css/#css-module-data */
._LayerTree-zoneTitle_fvhlh_2 {
  color: var(--_puck-outline-zone-color-text);
  font-size: var( --puck-outline-zone-font-size, calc(var(--puck-font-size-xxxs) * 0.9) );
  display: flex;
  gap: var(--puck-space-2);
  align-items: center;
  overflow-x: hidden;
  padding-top: var(--puck-space-1);
  padding-bottom: var(--puck-space-1);
  padding-inline-start: var(--_puck-outline-label-indent);
  border: var(--_puck-outline-border-width) solid transparent;
}
._LayerTree-zoneIcon_fvhlh_19 {
  margin-top: var(--puck-space-1);
}
._LayerTree-zoneIcon_fvhlh_19 svg {
  height: var(--_puck-outline-icon-size);
  width: var(--_puck-outline-icon-size);
}
._LayerTree-zoneTitle_fvhlh_2[data-puck-drop-target] {
  color: var(--_puck-outline-color-text-hover);
  position: relative;
  overflow: visible;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/LayerTree/styles.module.css/#css-module-data */
._LayerTreeRoot_1qowl_1 {
  min-width: max-content;
  --_puck-iconbutton-color-bg-hover: transparent;
  --_puck-outline-color-text: var( --puck-outline-color-text, var(--puck-color-text-primary) );
  --_puck-outline-border-width: var( --puck-outline-border-width, var(--puck-border-width-regular) );
  --_puck-outline-radius: var(--puck-outline-radius, var(--puck-radius-m));
  --_puck-outline-caret-size: var( --puck-outline-action-size, var(--puck-icon-size-s) );
  --_puck-outline-icon-size: var( --puck-outline-icon-size, var(--puck-icon-size-xs) );
  --_puck-outline-color-bg-selected: var( --puck-outline-color-bg-selected, var(--puck-color-interactive-subtle) );
  --_puck-outline-color-bg-hover: var( --puck-outline-color-bg-hover, var(--puck-color-interactive-soft) );
  --_puck-outline-color-border-hover: var( --puck-outline-color-border-hover, var(--puck-color-interactive-subtle) );
  --_puck-outline-color-text-hover: var( --puck-outline-color-text-hover, var(--puck-color-interactive) );
  --_puck-outline-color-drop-indicator: var( --puck-outline-color-drop-indicator, var(--puck-color-line-placeholder) );
  --_puck-outline-drop-indicator-size: var(--puck-line-placeholder-width);
  --_puck-outline-zone-color-text: var( --puck-outline-zone-color-text, var(--puck-color-text-muted) );
  --_puck-outline-actions-color-bg: transparent;
  --_puck-outline-caret-slot: calc( var(--_puck-outline-caret-size) + var(--puck-iconbutton-space, var(--puck-space-1)) * 2 );
  --_puck-outline-label-indent: calc( var(--_puck-outline-caret-slot) + var(--puck-space-2) + var(--_puck-outline-border-width) );
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Outline/components/collapse-all/styles.module.css/#css-module-data */
._CollapseAll_1r4cy_1 {
  visibility: hidden;
}
._CollapseAll-icon_1r4cy_5 {
  height: var(--puck-icon-size-m);
  width: var(--puck-icon-size-m);
}
._CollapseAll--visible_1r4cy_10 {
  visibility: visible;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Outline/components/outline-header/styles.module.css/#css-module-data */
._OutlineHeader_ntv8r_1 {
  display: flex;
  align-items: center;
  width: 100%;
  gap: var(--puck-space-2);
  padding-block: var(--puck-space-3);
  padding-inline: var(--puck-space-4);
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  box-sizing: border-box;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Outline/styles.module.css/#css-module-data */
._OutlineWrapper_b9ln0_1 {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-height: 0;
  min-width: 0;
}
._OutlineWrapper-collapseAll_b9ln0_9 {
  display: flex;
  align-items: center;
  margin-inline-start: auto;
}
._OutlineWrapper-layers_b9ln0_15 {
  flex-grow: 1;
  min-height: 0;
  overflow: auto;
  padding: var(--puck-space-1);
  box-sizing: border-box;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Layout/styles.module.css/#css-module-data */
._Puck_tzaxg_19 {
  font-family: var(--puck-font-family);
  overflow-x: hidden;
  visibility: visible !important;
}
@media (min-width: 766px) {
  ._Puck_tzaxg_19 {
    overflow-x: auto;
  }
}
._Puck-portal_tzaxg_31 {
  position: relative;
  z-index: 2;
}
._PuckLayout_tzaxg_36 {
  height: 100dvh;
}
._PuckLayout-inner_tzaxg_40 {
  --puck-frame-width: auto;
  --puck-pluginbar-width: min-content;
  --puck-sidebar-width: 0px;
  --puck-sidebar-left-width: var( --puck-user-sidebar-left-width, var(--puck-sidebar-width) );
  --puck-sidebar-right-width: var( --puck-user-sidebar-right-width, var(--puck-sidebar-width) );
  background-color: var(--puck-color-surface-subtle);
  display: grid;
  grid-template-areas: "header" "editor" "left" "right" "sidenav";
  grid-template-columns: var(--puck-frame-width);
  grid-template-rows: min-content auto 0 0 var(--puck-pluginbar-width);
  height: 100%;
  position: relative;
  transition: grid-template-rows var(--puck-duration-medium) var(--puck-ease-exit);
  z-index: 0;
  overflow: hidden;
}
@media (min-width: 638px) {
  ._PuckLayout-inner_tzaxg_40 {
    --puck-pluginbar-width: 68px;
    grid-template-areas: "header header header header" "sidenav left editor right";
    grid-template-columns: var(--puck-pluginbar-width) 0 var(--puck-frame-width) 0;
    grid-template-rows: min-content auto;
  }
  ._Puck--hidePlugins_tzaxg_73 ._PuckLayout-inner_tzaxg_40 {
    --puck-pluginbar-width: 0;
  }
}
._PuckLayout--mounted_tzaxg_78 ._PuckLayout-inner_tzaxg_40 {
  --puck-sidebar-width: 186px;
}
._PuckLayout--mobilePanelHeightToggle_tzaxg_82._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-inner_tzaxg_40 {
  grid-template-rows: 0 auto 30% 0 var(--puck-pluginbar-width);
  transition: grid-template-rows var(--puck-duration-medium) var(--puck-ease-entrance);
}
._PuckLayout--mobilePanelHeightToggle_tzaxg_82._PuckLayout--leftSideBarVisible_tzaxg_82._PuckLayout--isExpanded_tzaxg_90 ._PuckLayout-inner_tzaxg_40 {
  grid-template-rows: 0 auto 55% 0 var(--puck-pluginbar-width);
  transition: grid-template-rows var(--puck-duration-medium) var(--puck-ease-entrance);
}
@media (min-width: 638px) {
  ._PuckLayout--mobilePanelHeightToggle_tzaxg_82._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-inner_tzaxg_40 {
    grid-template-columns: var(--puck-pluginbar-width) var(--puck-sidebar-left-width) var( --puck-frame-width ) 0;
    grid-template-rows: min-content auto;
  }
}
._PuckLayout--mobilePanelHeightMinContent_tzaxg_110._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-inner_tzaxg_40,
._PuckLayout--mobilePanelHeightMinContent_tzaxg_110._PuckLayout--leftSideBarVisible_tzaxg_82._PuckLayout--isExpanded_tzaxg_90 ._PuckLayout-inner_tzaxg_40 {
  grid-template-rows: 0 auto min-content 0 var(--puck-pluginbar-width);
}
@media (min-width: 638px) {
  ._PuckLayout--mobilePanelHeightToggle_tzaxg_82._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-inner_tzaxg_40,
  ._PuckLayout--mobilePanelHeightToggle_tzaxg_82._PuckLayout--leftSideBarVisible_tzaxg_82._PuckLayout--isExpanded_tzaxg_90 ._PuckLayout-inner_tzaxg_40,
  ._PuckLayout--mobilePanelHeightMinContent_tzaxg_110._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-inner_tzaxg_40,
  ._PuckLayout--mobilePanelHeightMinContent_tzaxg_110._PuckLayout--leftSideBarVisible_tzaxg_82._PuckLayout--isExpanded_tzaxg_90 ._PuckLayout-inner_tzaxg_40 {
    grid-template-columns: var(--puck-pluginbar-width) var(--puck-sidebar-left-width) var( --puck-frame-width ) 0;
    grid-template-rows: min-content auto;
  }
}
@media (min-width: 638px) {
  ._PuckLayout--rightSideBarVisible_tzaxg_137 ._PuckLayout-inner_tzaxg_40 {
    grid-template-columns: var(--puck-pluginbar-width) 0 var(--puck-frame-width) var(--puck-sidebar-right-width);
  }
}
@media (min-width: 638px) {
  ._PuckLayout--leftSideBarVisible_tzaxg_82._PuckLayout--rightSideBarVisible_tzaxg_137 ._PuckLayout-inner_tzaxg_40 {
    grid-template-columns: var(--puck-pluginbar-width) var(--puck-sidebar-left-width) var( --puck-frame-width ) var(--puck-sidebar-right-width);
  }
}
@media (min-width: 458px) {
  ._PuckLayout-mounted_tzaxg_156 ._PuckLayout-inner_tzaxg_40 {
    --puck-frame-width: minmax(266px, auto);
  }
}
@media (min-width: 638px) {
  ._PuckLayout_tzaxg_36 ._PuckLayout-inner_tzaxg_40 {
    --puck-sidebar-width: minmax(186px, 250px);
  }
}
@media (min-width: 766px) {
  ._PuckLayout_tzaxg_36 ._PuckLayout-inner_tzaxg_40 {
    --puck-frame-width: auto;
  }
}
@media (min-width: 990px) {
  ._PuckLayout_tzaxg_36 ._PuckLayout-inner_tzaxg_40 {
    --puck-sidebar-width: 256px;
  }
}
@media (min-width: 1198px) {
  ._PuckLayout_tzaxg_36 ._PuckLayout-inner_tzaxg_40 {
    --puck-sidebar-width: 274px;
  }
}
@media (min-width: 1398px) {
  ._PuckLayout_tzaxg_36 ._PuckLayout-inner_tzaxg_40 {
    --puck-sidebar-width: 290px;
  }
}
@media (min-width: 1598px) {
  ._PuckLayout_tzaxg_36 ._PuckLayout-inner_tzaxg_40 {
    --puck-sidebar-width: 320px;
  }
}
._PuckLayout-nav_tzaxg_197 {
  border-top: var(--puck-border-width-regular) solid var(--puck-color-border);
  background-color: var( --puck-pluginbar-color-bg, var(--puck-color-surface-subtle) );
  grid-area: sidenav;
  overflow: hidden;
  width: 100%;
}
@media (min-width: 638px) {
  ._PuckLayout-nav_tzaxg_197 {
    border-top: 0;
    border-right: var(--puck-border-width-regular) solid var(--puck-color-border);
    box-sizing: border-box;
  }
}
._PuckLayout-header_tzaxg_217 {
  grid-area: header;
}
._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-header_tzaxg_217 {
  overflow: hidden;
}
@media (min-width: 638px) {
  ._PuckLayout--leftSideBarVisible_tzaxg_82 ._PuckLayout-header_tzaxg_217 {
    overflow: auto;
  }
}
._PuckPluginTab_tzaxg_231 {
  display: none;
  flex-grow: 1;
  max-height: 100%;
}
._PuckPluginTab--visible_tzaxg_237 {
  display: flex;
  flex-direction: column;
  min-height: 0;
}
._PuckPluginTab-body_tzaxg_243 {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  max-height: 100%;
  min-height: 0;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/MenuBar/styles.module.css/#css-module-data */
._MenuBar_1hxnj_1 {
  background-color: var(--_puck-menu-bar-color-bg, var(--puck-color-surface));
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  display: none;
  left: 0;
  margin-top: 1px;
  padding: var(--puck-space-2) var(--puck-space-4);
  position: absolute;
  right: 0;
  top: 100%;
  z-index: 2;
}
._MenuBar--menuOpen_1hxnj_14 {
  display: block;
}
@media (min-width: 638px) {
  ._MenuBar_1hxnj_1 {
    border: none;
    display: block;
    margin-top: 0;
    overflow-y: visible;
    padding: 0;
    position: static;
  }
}
._MenuBar-inner_1hxnj_29 {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: var(--puck-space-2) var(--puck-space-4);
  justify-content: flex-end;
}
@media (min-width: 638px) {
  ._MenuBar-inner_1hxnj_29 {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
  }
}
._MenuBar-history_1hxnj_45 {
  display: flex;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Header/styles.module.css/#css-module-data */
._PuckHeader_c2nei_1 {
  --_puck-menu-bar-color-bg: var( --puck-header-color-bg, var(--puck-color-surface) );
  background: var(--puck-header-color-bg, var(--puck-color-surface));
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  color: var(--puck-header-color-text, var(--puck-color-text));
  --_puck-heading-color: var(--puck-header-color-text, var(--puck-color-text));
  grid-area: header;
  position: relative;
  max-width: 100vw;
}
@media (min-width: 638px) {
  ._PuckHeader_c2nei_1 {
    padding-left: 67px;
  }
  ._PuckHeader--hidePlugins_c2nei_21 {
    padding-left: 0;
  }
}
._PuckHeader-inner_c2nei_26 {
  align-items: end;
  display: grid;
  gap: var(--puck-space-chrome-gutter);
  grid-template-areas: "left middle right";
  grid-template-columns: 1fr auto 1fr;
  grid-template-rows: auto;
  padding: var(--puck-space-chrome-gutter);
}
@media (min-width: 638px) {
  ._PuckHeader-inner_c2nei_26 {
    border-left: var(--puck-border-width-regular) solid var(--puck-color-border);
  }
  ._PuckHeader--hidePlugins_c2nei_21 ._PuckHeader-inner_c2nei_26 {
    border-left: none;
  }
}
._PuckHeader-toggle_c2nei_46 {
  display: flex;
  margin-inline-start: calc(var(--puck-space-1) * -1);
  padding-top: 2px;
}
._PuckHeader-rightSideBarToggle_c2nei_52,
._PuckHeader-leftSideBarToggle_c2nei_53 {
  display: none;
}
@media (min-width: 638px) {
  ._PuckHeader-rightSideBarToggle_c2nei_52,
  ._PuckHeader-leftSideBarToggle_c2nei_53 {
    display: block;
  }
}
._PuckHeader-title_c2nei_64 {
  align-self: center;
}
._PuckHeader-path_c2nei_68 {
  font-family: var(--puck-font-family-monospaced);
  font-size: var(--puck-font-size-xxs);
  font-weight: normal;
  word-break: break-all;
}
._PuckHeader-tools_c2nei_75 {
  display: flex;
  gap: var(--puck-space-4);
  justify-content: flex-end;
}
._PuckHeader-menuButton_c2nei_81 {
  color: var(--puck-color-text-muted);
  margin-inline-start: calc(var(--puck-space-1) * -1);
}
._PuckHeader--menuOpen_c2nei_86 ._PuckHeader-menuButton_c2nei_81 {
  color: var(--puck-color-text);
}
@media (min-width: 638px) {
  ._PuckHeader-menuButton_c2nei_81 {
    display: none;
  }
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/SidebarSection/styles.module.css/#css-module-data */
._SidebarSection_1uv88_1 {
  display: flex;
  position: relative;
  flex-direction: column;
  color: var(--puck-color-text);
}
._SidebarSection_1uv88_1:last-of-type {
  flex-grow: 1;
}
._SidebarSection-title_1uv88_12 {
  background: var(--_puck-sidebar-section-color-bg, var(--puck-color-surface));
  padding: var(--puck-space-4);
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  border-top: var(--puck-border-width-regular) solid var(--puck-color-border);
  overflow-x: auto;
}
._SidebarSection--noBorderTop_1uv88_20 > ._SidebarSection-title_1uv88_12 {
  border-top: 0px;
}
._SidebarSection-content_1uv88_24:last-child {
  padding-bottom: var(--puck-space-1);
}
._SidebarSection_1uv88_1:last-of-type ._SidebarSection-content_1uv88_24 {
  border-bottom: none;
  flex-grow: 1;
}
._SidebarSection-breadcrumbLabel_1uv88_33 {
  background: none;
  border: 0;
  border-radius: var(--puck-radius-xs);
  color: var(--puck-color-interactive);
  cursor: pointer;
  font: inherit;
  flex-shrink: 0;
  padding: 0;
  transition: color var(--puck-duration-fast) var(--puck-ease-exit);
}
._SidebarSection-breadcrumbLabel_1uv88_33:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._SidebarSection-breadcrumbLabel_1uv88_33:hover {
    color: var(--puck-color-interactive-hover);
    transition: none;
  }
}
._SidebarSection-breadcrumbLabel_1uv88_33:active {
  color: var(--puck-color-interactive-active);
  transition: none;
}
._SidebarSection-breadcrumbs_1uv88_62 {
  align-items: center;
  display: flex;
  gap: var(--puck-space-1);
}
._SidebarSection-breadcrumb_1uv88_33 {
  align-items: center;
  display: flex;
  gap: var(--puck-space-1);
}
._SidebarSection-heading_1uv88_74 {
  padding-inline-end: var(--puck-space-4);
}
._SidebarSection-loadingOverlay_1uv88_78 {
  background: var(--puck-color-surface);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  top: 0;
  position: absolute;
  z-index: 1;
  pointer-events: all;
  box-sizing: border-box;
  opacity: 0.8;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Breadcrumbs/styles.module.css/#css-module-data */
._Breadcrumbs_8c6w5_1 {
  align-items: center;
  display: flex;
  gap: var(--puck-space-1);
}
._Breadcrumbs-breadcrumbLabel_8c6w5_7 {
  background: none;
  border: 0;
  border-radius: var(--puck-radius-xs);
  color: var(--puck-color-interactive);
  cursor: pointer;
  font: inherit;
  flex-shrink: 0;
  padding: 0;
  transition: color var(--puck-duration-fast) var(--puck-ease-exit);
}
._Breadcrumbs-breadcrumbLabel_8c6w5_7:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._Breadcrumbs-breadcrumbLabel_8c6w5_7:hover {
    color: var(--puck-color-interactive-hover);
    transition: none;
  }
}
._Breadcrumbs-breadcrumbLabel_8c6w5_7:active {
  color: var(--puck-color-interactive-active);
  transition: none;
}
._Breadcrumbs-breadcrumb_8c6w5_7 {
  align-items: center;
  display: flex;
  gap: var(--puck-space-1);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/ViewportControls/styles.module.css/#css-module-data */
._ViewportControls_v26yb_1 {
  position: relative;
}
._ViewportControls--fullScreen_v26yb_5 {
  border-radius: 32px;
  display: flex;
  position: absolute;
  bottom: var(--puck-space-3);
  right: var(--puck-space-3);
  overflow: hidden;
}
._ViewportControls-toggleButton_v26yb_14 {
  display: none;
}
._ViewportControls--fullScreen_v26yb_5 ._ViewportControls-toggleButton_v26yb_14 {
  align-items: center;
  background-color: var(--puck-color-surface-inverse);
  border: var(--puck-border-width-regular) solid var(--puck-color-border-inverse);
  border-radius: var(--puck-radius-pill);
  cursor: pointer;
  color: var(--puck-color-text-inverse);
  display: flex;
  justify-content: center;
  width: 42px;
  height: 42px;
  z-index: 1;
}
._ViewportControls--fullScreen_v26yb_5 ._ViewportControls-toggleButton_v26yb_14:hover {
  color: var(--puck-color-interactive-inverse-hover);
  border: var(--puck-border-width-regular) solid var(--puck-color-interactive-inverse-hover);
}
._ViewportControls-actions_v26yb_39 {
  display: flex;
}
._ViewportControls-actionsInner_v26yb_43 {
  display: flex;
  box-sizing: border-box;
  justify-content: center;
  margin-left: auto;
  margin-right: auto;
  z-index: 0;
  overflow: hidden;
}
._ViewportControls--fullScreen_v26yb_5 ._ViewportControls-actionsInner_v26yb_43 {
  background: var(--puck-color-surface-muted);
  border: var(--puck-border-width-regular) solid var(--puck-color-border);
  border-radius: var(--puck-radius-pill);
  margin-left: none;
  margin-right: none;
  padding-right: 42px;
}
._ViewportControls--fullScreen_v26yb_5 ._ViewportControls-actionsInner_v26yb_43 {
  transform: translateX(100%);
  transition: transform var(--puck-duration-medium) var(--puck-ease-emphasized);
}
._ViewportControls--fullScreen_v26yb_5._ViewportControls--isExpanded_v26yb_67 ._ViewportControls-actionsInner_v26yb_43 {
  transform: translateX(42px);
}
._ViewportControls-divider_v26yb_72 {
  border-inline-end: var(--puck-border-width-regular) solid var(--puck-color-border);
  margin-bottom: var(--puck-space-2);
  margin-top: var(--puck-space-2);
}
._ViewportControls-zoomSelect_v26yb_79 {
  appearance: none;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' fill='%23c3c3c3'><polygon points='0,0 100,0 50,50'/></svg>") no-repeat;
  background-size: 10px;
  color: currentColor;
  background-position: calc(100% - 12px) calc(50% + 3px);
  background-repeat: no-repeat;
  border: 0;
  font-size: var(--puck-font-size-xxxs);
  padding: 0;
  padding-left: var(--puck-space-2);
  width: 96px;
}
._ViewportControls--fullScreen_v26yb_5 ._ViewportControls-zoom_v26yb_79 {
  display: none;
}
@media (min-width: 638px) {
  ._ViewportControls-zoom_v26yb_79,
  ._ViewportControls--fullScreen_v26yb_5 ._ViewportControls-zoom_v26yb_79 {
    display: flex;
    justify-content: center;
  }
}
._ViewportControls-zoomSelect_v26yb_79:dir(rtl) {
  background-position: 12px calc(50% + 3px);
}
._ViewportButton-inner_v26yb_110 {
  align-items: center;
  display: flex;
  justify-content: center;
  height: 32px;
  width: 32px;
}
._ViewportButton--isActive_v26yb_118 ._ViewportButton-inner_v26yb_110 {
  color: var(--puck-color-interactive);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Canvas/styles.module.css/#css-module-data */
._PuckCanvas_zw9iy_1 {
  color: var(--puck-canvas-color-text, var(--puck-color-text));
  background: var(--puck-canvas-color-bg, var(--puck-color-surface-muted));
  display: flex;
  grid-area: editor;
  flex-direction: column;
  padding: var(--puck-space-chrome-gutter);
  position: relative;
  overflow: auto;
}
@media (min-width: 1198px) {
  ._PuckCanvas_zw9iy_1 {
    padding: calc(var(--puck-space-chrome-gutter) * 1.5);
    padding-top: calc(var(--puck-space-chrome-gutter) * 0.5);
  }
  ._PuckCanvas_zw9iy_1:not(._PuckCanvas_zw9iy_1:has(._PuckCanvas-controls_zw9iy_18)) {
    padding-top: calc(var(--puck-space-chrome-gutter) * 1.5);
  }
}
._PuckCanvas--fullScreen_zw9iy_23 {
  padding: 0;
  overflow: hidden;
}
@media (min-width: 1198px) {
  ._PuckCanvas--fullScreen_zw9iy_23 {
    padding: 0;
  }
}
._PuckCanvas-inner_zw9iy_34 {
  display: flex;
  height: 100%;
  justify-content: center;
  min-width: 288px;
  position: relative;
  width: 100%;
}
._PuckCanvas-root_zw9iy_43 {
  background: var(--puck-canvas-preview-color-bg, var(--puck-color-surface));
  outline: var(--puck-border-width-regular) solid var(--puck-color-border);
  box-sizing: content-box;
  min-width: 321px;
  position: absolute;
  pointer-events: none;
  transform-origin: top;
  top: 0;
  bottom: 0;
  opacity: 0;
}
@media (min-width: 1198px) {
  ._PuckCanvas-root_zw9iy_43 {
    min-width: unset;
  }
}
@media (prefers-reduced-motion: reduce) {
  ._PuckCanvas-root_zw9iy_43 {
    transition: none !important;
  }
}
._PuckCanvas--ready_zw9iy_68 ._PuckCanvas-root_zw9iy_43 {
  pointer-events: unset;
  opacity: 1;
}
._PuckCanvas-loader_zw9iy_73 {
  align-items: center;
  color: var(--puck-color-text-subtle);
  display: flex;
  height: 100%;
  justify-content: center;
  transition: opacity var(--puck-duration-slow) var(--puck-ease-entrance);
  opacity: 0;
  pointer-events: none;
}
._PuckCanvas--showLoader_zw9iy_84 ._PuckCanvas-loader_zw9iy_73 {
  opacity: 1;
}
._PuckCanvas--showLoader_zw9iy_84._PuckCanvas--ready_zw9iy_68 ._PuckCanvas-loader_zw9iy_73 {
  opacity: 0;
  height: 0;
  transition: none;
}
._PuckCanvas-controls_zw9iy_18 {
  padding-bottom: calc(var(--puck-space-chrome-gutter) * 0.5);
}
._PuckCanvas--fullScreen_zw9iy_23 ._PuckCanvas-controls_zw9iy_18 {
  padding-bottom: 0;
  z-index: 1;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/ResizeHandle/styles.module.css/#css-module-data */
@media (min-width: 766px) {
  ._ResizeHandle_144bf_2 {
    position: absolute;
    width: 5px;
    height: 100%;
    cursor: col-resize;
    z-index: 10;
    background: transparent;
    top: 0;
  }
  ._ResizeHandle_144bf_2:hover {
    background: rgba(0, 0, 0, 0.1);
  }
  ._ResizeHandle--left_144bf_16 {
    right: -3px;
  }
  ._ResizeHandle--right_144bf_20 {
    left: -3px;
  }
}

/* components/Puck/components/ResizeHandle/styles.css */
[data-resize-overlay] {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  cursor: col-resize;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Sidebar/styles.module.css/#css-module-data */
._Sidebar_16oed_1 {
  border-block-start: var(--puck-border-width-regular) solid var(--puck-color-border);
  position: relative;
  display: none;
  flex-direction: column;
  overflow-y: auto;
}
._Sidebar--isVisible_16oed_10 {
  display: flex;
}
._Sidebar--left_16oed_14 {
  --_puck-sidebar-section-color-bg: var( --puck-sidebar-left-color-bg, var(--puck-color-surface) );
  background: var( --puck-sidebar-left-color-bg, var(--puck-color-surface-subtle) );
  grid-area: left;
}
@media (min-width: 766px) {
  ._Sidebar--left_16oed_14 {
    border-block-start: 0;
    border-inline-end: var(--puck-border-width-regular) solid var(--puck-color-border);
  }
}
._Sidebar--right_16oed_34 {
  --_puck-sidebar-section-color-bg: var( --puck-sidebar-right-color-bg, var(--puck-color-surface) );
  background: var(--puck-sidebar-right-color-bg, var(--puck-color-surface));
  grid-area: right;
}
@media (min-width: 766px) {
  ._Sidebar--right_16oed_34 {
    border-block-start: 0;
    border-inline-start: var(--puck-border-width-regular) solid var(--puck-color-border);
  }
}
._Sidebar-resizeHandle_16oed_51 {
  position: absolute;
  height: 100%;
}
._Sidebar--left_16oed_14 + ._Sidebar-resizeHandle_16oed_51 {
  grid-area: left;
  justify-self: end;
}
._Sidebar--right_16oed_34 + ._Sidebar-resizeHandle_16oed_51 {
  grid-area: right;
  justify-self: start;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Puck/components/Nav/styles.module.css/#css-module-data */
._Nav_vll2r_1 {
  display: flex;
}
._Nav-list_vll2r_5 {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  overflow-x: auto;
  gap: var(--puck-space-2);
}
@media (min-width: 638px) {
  ._Nav-list_vll2r_5 {
    padding-top: 32px;
    flex-direction: column;
    gap: var(--puck-space-4);
    width: 100%;
  }
}
._Nav-mobileActions_vll2r_23 {
  align-items: center;
  display: flex;
  justify-content: center;
  margin-inline-start: auto;
  padding: var(--puck-space-1) var(--puck-space-4);
  border-inline-start: var(--puck-border-width-regular) solid var(--puck-color-border);
}
@media (min-width: 638px) {
  ._Nav-mobileActions_vll2r_23 {
    display: none;
  }
}
._NavItem-link_vll2r_39 {
  text-align: center;
  align-items: center;
  color: var(--puck-pluginbar-color-text, var(--puck-color-text-secondary));
  display: flex;
  gap: var(--puck-space-2);
  text-decoration: none;
  cursor: pointer;
  border-radius: var(--puck-radius-m);
  padding: var(--puck-space-2) var(--puck-space-1);
  width: 64px;
  box-sizing: border-box;
}
@media (min-width: 638px) {
  ._NavItem-link_vll2r_39 {
    width: auto;
  }
}
._NavItem_vll2r_39:first-of-type {
  padding-left: var(--puck-space-4);
}
._NavItem_vll2r_39:last-of-type {
  padding-right: var(--puck-space-4);
}
@media (min-width: 638px) {
  ._NavItem_vll2r_39:first-of-type,
  ._NavItem_vll2r_39:last-of-type {
    padding: 0;
  }
}
._NavItem-link_vll2r_39 {
  border-top: var(--puck-border-width-strong) solid transparent;
  border-bottom: var(--puck-border-width-strong) solid transparent;
  border-radius: var(--puck-radius-none);
  flex-direction: column;
  font-size: var(--puck-pluginbar-font-size, var(--puck-font-size-xxxs));
}
@media (min-width: 638px) {
  ._NavItem-link_vll2r_39 {
    border: 0;
    border-left: var(--puck-border-width-strong) solid transparent;
    border-right: var(--puck-border-width-strong) solid transparent;
  }
}
._NavItem-linkIcon_vll2r_90 {
  height: 2em;
  width: 2em;
}
._NavItem-linkIcon_vll2r_90 svg {
  height: 100%;
  width: 100%;
}
._NavItem--active_vll2r_100 > ._NavItem-link_vll2r_39 {
  background-color: var(--puck-color-interactive-subtle);
  color: var( --puck-pluginbar-color-text-selected, var(--puck-color-interactive) );
  font-weight: var(--puck-font-weight-semibold);
}
._NavItem--active_vll2r_100 > ._NavItem-link_vll2r_39 {
  background-color: transparent;
  border-top-color: var(--puck-color-interactive);
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  font-weight: var(--puck-font-weight-semibold);
}
@media (min-width: 638px) {
  ._NavItem--active_vll2r_100 > ._NavItem-link_vll2r_39 {
    border-top-color: transparent;
    border-right-color: var( --puck-pluginbar-color-text-selected, var(--puck-color-interactive) );
  }
}
._NavItem_vll2r_39:not(._NavItem--active_vll2r_100) > ._NavItem-link_vll2r_39:hover {
  background-color: var( --puck-pluginbar-color-bg-hover, var(--puck-color-interactive-soft) );
  color: var(--puck-pluginbar-color-text-hover, var(--puck-color-interactive));
}
@media (min-width: 638px) {
  ._NavItem--mobileOnly_vll2r_136 {
    display: none;
  }
}
._NavItem--desktopOnly_vll2r_141 {
  display: none;
}
@media (min-width: 638px) {
  ._NavItem--desktopOnly_vll2r_141 {
    display: block;
  }
}

/* css-module:/home/runner/work/puck/puck/packages/core/plugins/blocks/styles.module.css/#css-module-data */
._BlocksPlugin_9af19_1 {
  padding: var(--puck-drawer-space, var(--puck-space-4));
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

/* css-module:/home/runner/work/puck/puck/packages/core/plugins/outline/styles.module.css/#css-module-data */
._OutlinePlugin_1ylsc_1 {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-height: 0;
  min-width: 0;
  position: relative;
}

/* css-module:/home/runner/work/puck/puck/packages/core/plugins/fields/styles.module.css/#css-module-data */
._FieldsPlugin_18cj3_1 {
  background: var(--puck-color-surface);
  height: 100%;
  overflow-y: auto;
}
._FieldsPlugin-header_18cj3_7 {
  border-bottom: var(--puck-border-width-regular) solid var(--puck-color-border);
  font-weight: var(--puck-font-weight-semibold);
  padding-bottom: var(--puck-space-2);
  padding-left: var(--puck-space-4);
  padding-right: var(--puck-space-4);
  padding-top: var(--puck-space-2);
}
@media (min-width: 638px) {
  ._FieldsPlugin-header_18cj3_7 {
    padding: var(--puck-space-4);
  }
}`,CA=`/* styles/color.css */
@layer puck-tokens {
  :root {
    --puck-color-rose-01: #4a001c;
    --puck-color-rose-02: #670833;
    --puck-color-rose-03: #87114c;
    --puck-color-rose-04: #a81a66;
    --puck-color-rose-05: #bc5089;
    --puck-color-rose-06: #cc7ca5;
    --puck-color-rose-07: #d89aba;
    --puck-color-rose-08: #e3b8cf;
    --puck-color-rose-09: #efd6e3;
    --puck-color-rose-10: #f6eaf1;
    --puck-color-rose-11: #faf4f8;
    --puck-color-rose-12: #fef8fc;
    --puck-color-azure-01: #00175d;
    --puck-color-azure-02: #002c77;
    --puck-color-azure-03: #014292;
    --puck-color-azure-04: #0158ad;
    --puck-color-azure-05: #3479be;
    --puck-color-azure-06: #6499cf;
    --puck-color-azure-07: #88b0da;
    --puck-color-azure-08: #abc7e5;
    --puck-color-azure-09: #cfdff0;
    --puck-color-azure-10: #e7eef7;
    --puck-color-azure-11: #f3f6fb;
    --puck-color-azure-12: #f7faff;
    --puck-color-green-01: #002000;
    --puck-color-green-02: #043604;
    --puck-color-green-03: #084e08;
    --puck-color-green-04: #0c680c;
    --puck-color-green-05: #1d882f;
    --puck-color-green-06: #2faa53;
    --puck-color-green-07: #56c16f;
    --puck-color-green-08: #7dd78b;
    --puck-color-green-09: #b8e8bf;
    --puck-color-green-10: #ddf3e0;
    --puck-color-green-11: #eff8f0;
    --puck-color-green-12: #f3fcf4;
    --puck-color-yellow-01: #211000;
    --puck-color-yellow-02: #362700;
    --puck-color-yellow-03: #4c4000;
    --puck-color-yellow-04: #645a00;
    --puck-color-yellow-05: #877614;
    --puck-color-yellow-06: #ab9429;
    --puck-color-yellow-07: #bfac4e;
    --puck-color-yellow-08: #d4c474;
    --puck-color-yellow-09: #e6deb1;
    --puck-color-yellow-10: #f3efd9;
    --puck-color-yellow-11: #f9f7ed;
    --puck-color-yellow-12: #fcfaf0;
    --puck-color-red-01: #4c0000;
    --puck-color-red-02: #6a0a10;
    --puck-color-red-03: #8a1422;
    --puck-color-red-04: #ac1f35;
    --puck-color-red-05: #bf5366;
    --puck-color-red-06: #ce7e8e;
    --puck-color-red-07: #d99ca8;
    --puck-color-red-08: #e4b9c2;
    --puck-color-red-09: #efd7db;
    --puck-color-red-10: #f6eaec;
    --puck-color-red-11: #faf4f5;
    --puck-color-red-12: #fff9fa;
    --puck-color-grey-01: #181818;
    --puck-color-grey-02: #292929;
    --puck-color-grey-03: #404040;
    --puck-color-grey-04: #5a5a5a;
    --puck-color-grey-05: #767676;
    --puck-color-grey-06: #949494;
    --puck-color-grey-07: #ababab;
    --puck-color-grey-08: #c3c3c3;
    --puck-color-grey-09: #dcdcdc;
    --puck-color-grey-10: #efefef;
    --puck-color-grey-11: #f5f5f5;
    --puck-color-grey-12: #fafafa;
    --puck-color-black: #000000;
    --puck-color-white: #ffffff;
  }
}

/* styles/tokens.css */
@layer puck-tokens {
  :root {
    --puck-color-surface: var(--puck-color-white);
    --puck-color-surface-muted: var(--puck-color-grey-11);
    --puck-color-surface-subtle: var(--puck-color-grey-12);
    --puck-color-surface-inverse: var(--puck-color-grey-01);
    --puck-color-border: var(--puck-color-grey-09);
    --puck-color-border-hover: var(--puck-color-grey-05);
    --puck-color-border-muted: var(--puck-color-grey-10);
    --puck-color-border-inverse: var(--puck-color-grey-05);
    --puck-color-text: var(--puck-color-black);
    --puck-color-text-secondary: var(--puck-color-grey-04);
    --puck-color-text-muted: var(--puck-color-grey-05);
    --puck-color-text-subtle: var(--puck-color-grey-07);
    --puck-color-text-inverse: var(--puck-color-white);
    --puck-opacity-text-inverse: 0.75;
    --puck-color-interactive: var(--puck-color-azure-04);
    --puck-color-interactive-hover: var(--puck-color-azure-03);
    --puck-color-interactive-active: var(--puck-color-azure-02);
    --puck-color-interactive-subtle: var(--puck-color-azure-10);
    --puck-color-interactive-soft: var(--puck-color-azure-11);
    --puck-color-interactive-soft-hover: var(--puck-color-azure-12);
    --puck-color-interactive-neutral-hover: var(--puck-color-grey-10);
    --puck-color-interactive-inverse-hover: var(--puck-color-azure-06);
    --puck-color-interactive-inverse-active: var(--puck-color-azure-07);
    --puck-color-focus-ring: var(--puck-color-azure-05);
    --puck-color-selection-bg: color-mix( in srgb, var(--puck-color-azure-09) 30%, transparent );
    --puck-color-selection-border: var(--puck-color-azure-08);
    --puck-color-line-placeholder: var(--puck-color-azure-06);
    --puck-color-highlight: var(--puck-color-rose-07);
    --puck-color-bg-disabled: var(--puck-color-grey-07);
    --puck-color-text-disabled: var(--puck-color-grey-03);
    --puck-color-overlay-backdrop: color-mix( in srgb, var(--puck-color-black) 75%, transparent );
    --puck-space-1: 4px;
    --puck-space-2: 8px;
    --puck-space-3: 12px;
    --puck-space-4: 16px;
    --puck-space-5: 24px;
    --puck-space-chrome-gutter: var(--puck-space-4);
    --puck-radius-none: 0;
    --puck-radius-xs: 2px;
    --puck-radius-s: 3px;
    --puck-radius-m: 4px;
    --puck-radius-l: 8px;
    --puck-radius-pill: 30px;
    --puck-radius-round: 100%;
    --puck-border-width-hairline: 0.5px;
    --puck-border-width-regular: 1px;
    --puck-border-width-focus: 2px;
    --puck-border-width-strong: 4px;
    --puck-duration-fast: 50ms;
    --puck-duration-medium: 150ms;
    --puck-duration-slow: 250ms;
    --puck-ease-exit: ease-in;
    --puck-ease-emphasized: ease-in-out;
    --puck-ease-entrance: ease-out;
    --puck-font-weight-regular: 400;
    --puck-font-weight-medium: 500;
    --puck-font-weight-semibold: 600;
    --puck-font-weight-bold: 700;
    --puck-font-weight-heavy: 800;
    --puck-letter-spacing-ui: 0.05ch;
    --puck-letter-spacing-heading: 0.08ch;
    --puck-icon-size-xs: 14px;
    --puck-icon-size-s: 16px;
    --puck-icon-size-m: 18px;
    --puck-icon-size-l: 24px;
    --puck-space-m-unitless: 24;
    --puck-user-sidebar-left-width: var(--puck-sidebar-width);
    --puck-user-sidebar-right-width: var(--puck-sidebar-width);
    --puck-slot-min-empty-height: 128px;
    --puck-line-placeholder-width: 2px;
  }
}

/* styles/typography.css */
@layer puck-tokens {
  :root {
    --puck-font-size-scale-base-unitless: 12;
    --puck-font-size-xxxs-unitless: 12;
    --puck-font-size-xxs-unitless: 14;
    --puck-font-size-xs-unitless: 16;
    --puck-font-size-s-unitless: 18;
    --puck-font-size-m-unitless: 21;
    --puck-font-size-l-unitless: 24;
    --puck-font-size-xl-unitless: 28;
    --puck-font-size-xxl-unitless: 36;
    --puck-font-size-xxxl-unitless: 48;
    --puck-font-size-xxxxl-unitless: 56;
    --puck-font-size-xxxs: calc( 1rem * var(--puck-font-size-xxxs-unitless) / 16 );
    --puck-font-size-xxs: calc(1rem * var(--puck-font-size-xxs-unitless) / 16);
    --puck-font-size-xs: calc(1rem * var(--puck-font-size-xs-unitless) / 16);
    --puck-font-size-s: calc(1rem * var(--puck-font-size-s-unitless) / 16);
    --puck-font-size-m: calc(1rem * var(--puck-font-size-m-unitless) / 16);
    --puck-font-size-l: calc(1rem * var(--puck-font-size-l-unitless) / 16);
    --puck-font-size-xl: calc(1rem * var(--puck-font-size-xl-unitless) / 16);
    --puck-font-size-xxl: calc(1rem * var(--puck-font-size-xxl-unitless) / 16);
    --puck-font-size-xxxl: calc( 1rem * var(--puck-font-size-xxxl-unitless) / 16 );
    --puck-font-size-xxxxl: calc( 1rem * var(--puck-font-size-xxxxl-unitless) / 16 );
    --puck-font-size-base: var(--puck-font-size-xs);
    --puck-line-height-reset: 1;
    --puck-line-height-xs: calc( var(--puck-space-m-unitless) / var(--puck-font-size-m-unitless) );
    --puck-line-height-s: calc( var(--puck-space-m-unitless) / var(--puck-font-size-s-unitless) );
    --puck-line-height-m: calc( var(--puck-space-m-unitless) / var(--puck-font-size-xs-unitless) );
    --puck-line-height-l: calc( var(--puck-space-m-unitless) / var(--puck-font-size-xxs-unitless) );
    --puck-line-height-xl: calc( var(--puck-space-m-unitless) / var(--puck-font-size-scale-base-unitless) );
    --puck-line-height-base: var(--puck-line-height-m);
    --puck-fallback-font-stack:
      -apple-system,
      BlinkMacSystemFont,
      Segoe UI,
      Helvetica Neue,
      sans-serif,
      Apple Color Emoji,
      Segoe UI Emoji,
      Segoe UI Symbol;
    --puck-font-family: Inter, var(--puck-fallback-font-stack);
    --puck-font-family-monospaced:
      ui-monospace,
      "Cascadia Code",
      "Source Code Pro",
      Menlo,
      Consolas,
      "DejaVu Sans Mono",
      monospace;
  }
  @supports (font-variation-settings: normal) {
    :root {
      --puck-font-family: InterVariable, var(--puck-fallback-font-stack);
    }
  }
}

/* bundle/core.css */
:root {
  --_puck-styles-loaded: "true";
}
#frame-root {
  height: 1px;
  min-height: 100vh;
}
[data-puck-entry] {
  position: relative;
  z-index: 0;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/ActionBar/styles.module.css/#css-module-data */
._ActionBar_5vdfr_1 {
  align-items: center;
  cursor: default;
  display: flex;
  width: auto;
  padding-top: var(--puck-actionbar-space-y, var(--puck-space-1));
  padding-bottom: var(--puck-actionbar-space-y, var(--puck-space-1));
  padding-inline-start: var(--puck-actionbar-space-x, 0);
  padding-inline-end: var(--puck-actionbar-space-x, 0);
  border-radius: var(--puck-actionbar-radius, var(--puck-radius-l));
  background: var(--puck-actionbar-color-bg, var(--puck-color-surface-inverse));
  color: var(--puck-color-text-inverse);
  font-family: var(--puck-font-family);
  min-height: 26px;
}
._ActionBar-label_5vdfr_17 {
  color: var(--puck-actionbar-color-text, var(--puck-color-text-inverse));
  font-size: var(--puck-actionbar-font-size, var(--puck-font-size-xxxs));
  opacity: var(--puck-actionbar-opacity-text, var(--puck-opacity-text-inverse));
  font-weight: var(--puck-font-weight-medium);
  padding-inline-start: var(--puck-space-2);
  padding-inline-end: var(--puck-space-2);
  margin-inline-start: var(--puck-space-1);
  margin-inline-end: var(--puck-space-1);
  text-overflow: ellipsis;
  white-space: nowrap;
}
._ActionBarAction_5vdfr_30 + ._ActionBar-label_5vdfr_17 {
  padding-inline-start: 0;
}
._ActionBar-label_5vdfr_17 + ._ActionBarAction_5vdfr_30 {
  margin-inline-start: calc(var(--puck-space-1) * -1);
}
._ActionBar-group_5vdfr_38 {
  align-items: center;
  border-inline-start: var(--puck-border-width-hairline) solid var(--puck-actionbar-color-separator, var(--puck-color-border-inverse));
  display: flex;
  height: 100%;
  padding-inline-start: var(--puck-space-1);
  padding-inline-end: var(--puck-space-1);
}
._ActionBar-group_5vdfr_38:first-of-type {
  border-inline-start: 0;
}
._ActionBar-group_5vdfr_38:empty {
  display: none;
}
._ActionBarAction_5vdfr_30 {
  background: transparent;
  border: none;
  color: var(--puck-actionbar-color-text, var(--puck-color-text-inverse));
  cursor: pointer;
  padding: var(--puck-actionbar-action-space, 6px);
  margin-inline-start: var(--puck-space-1);
  margin-inline-end: var(--puck-space-1);
  border-radius: var(--puck-radius-m);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: var(--puck-actionbar-opacity-text, var(--puck-opacity-text-inverse));
  transition: color var(--puck-duration-fast) var(--puck-ease-exit), opacity var(--puck-duration-fast) var(--puck-ease-exit);
}
._ActionBarAction--disabled_5vdfr_74 {
  cursor: auto;
  color: var( --puck-actionbar-color-action-disabled, var(--puck-color-text-inverse) );
  opacity: var(--puck-actionbar-opacity-action-disabled, 0.54);
}
._ActionBarAction_5vdfr_30 svg {
  max-width: none !important;
}
._ActionBarAction_5vdfr_30:focus-visible {
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: calc(var(--puck-border-width-focus) * -1);
}
@media (hover: hover) and (pointer: fine) {
  ._ActionBarAction_5vdfr_30:hover:not(._ActionBarAction--disabled_5vdfr_74) {
    color: var( --puck-actionbar-color-action-hover, var(--puck-color-interactive-inverse-hover) );
    opacity: 1;
    transition: none;
  }
}
._ActionBarAction_5vdfr_30:active:not(._ActionBarAction--disabled_5vdfr_74),
._ActionBarAction--active_5vdfr_104 {
  color: var( --puck-actionbar-color-action-active, var(--puck-color-interactive-inverse-active) );
  opacity: 1;
  transition: none;
}
._ActionBar-group_5vdfr_38 * {
  margin: 0;
}
._ActionBar-separator_5vdfr_117 {
  background: var( --puck-actionbar-color-separator, var(--puck-color-border-inverse) );
  margin-inline: var(--puck-space-1);
  width: var( --puck-border-width-hairline );
  height: 100%;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/DraggableComponent/styles.module.css/#css-module-data */
._DraggableComponent_1627v_1 {
  position: absolute;
  pointer-events: none;
}
._DraggableComponent-overlayWrapper_1627v_6 {
  height: 100%;
  width: 100%;
  top: 0;
  position: absolute;
  pointer-events: none;
  box-sizing: border-box;
  z-index: 1;
}
._DraggableComponent-overlay_1627v_6 {
  cursor: pointer;
  height: 100%;
  outline: var( --puck-slot-component-border-width, var(--puck-border-width-focus) ) var( --puck-slot-component-color-overlay-border, var(--puck-color-selection-border) ) solid;
  outline-offset: calc(var(--puck-slot-component-border-width, var(--puck-border-width-focus)) * -1);
  width: 100%;
}
._DraggableComponent_1627v_1:focus-visible > ._DraggableComponent-overlayWrapper_1627v_6 {
  outline: var(--puck-border-width-regular) solid var(--puck-color-focus-ring);
}
._DraggableComponent-loadingOverlay_1627v_38 {
  background: var(--puck-color-surface);
  color: var(--puck-color-text);
  border-radius: var(--puck-radius-m);
  display: flex;
  padding: var(--puck-space-2);
  top: var(--puck-space-2);
  right: var(--puck-space-2);
  position: absolute;
  z-index: 1;
  pointer-events: all;
  box-sizing: border-box;
  opacity: 0.8;
  z-index: 1;
}
._DraggableComponent--hover_1627v_54 > ._DraggableComponent-overlayWrapper_1627v_6 > ._DraggableComponent-overlay_1627v_6 {
  background: var( --puck-slot-component-color-overlay, var(--puck-color-selection-bg) );
  outline: var( --puck-slot-component-border-width, var(--puck-border-width-focus) ) var( --puck-slot-component-color-overlay-border, var(--puck-color-selection-border) ) solid;
}
._DraggableComponent--isSelected_1627v_72 > ._DraggableComponent-overlayWrapper_1627v_6 > ._DraggableComponent-overlay_1627v_6 {
  outline-color: var( --puck-slot-component-color-border-selected, var(--puck-color-selection-border) );
}
._DraggableComponent_1627v_1:has(._DraggableComponent--hover_1627v_54 > ._DraggableComponent-overlayWrapper_1627v_6) > ._DraggableComponent-overlayWrapper_1627v_6 {
  display: none;
}
._DraggableComponent-actionsOverlay_1627v_89 {
  position: sticky;
  opacity: 0;
  pointer-events: none;
  z-index: 2;
}
._DraggableComponent--isSelected_1627v_72 ._DraggableComponent-actionsOverlay_1627v_89 {
  opacity: 1;
  pointer-events: auto;
}
._DraggableComponent-actions_1627v_89 {
  position: absolute;
  width: auto;
  cursor: grab;
  display: flex;
  box-sizing: border-box;
  transform-origin: right top;
  min-height: 36px;
}
._DraggableComponent-actionsAction_1627v_111 {
  height: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
  width: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Drawer/styles.module.css/#css-module-data */
._Drawer_1n90m_1 {
  display: flex;
  flex-direction: column;
  font-family: var(--puck-font-family);
  gap: var(--puck-space-3);
}
._Drawer-draggable_1n90m_8 {
  position: relative;
}
._Drawer-draggableBg_1n90m_12 {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  pointer-events: none;
  z-index: -1;
}
._DrawerItem-draggable_1n90m_22 {
  background: var(--puck-drawer-item-color-bg, var(--puck-color-surface));
  color: var(--puck-drawer-item-color-text, var(--puck-color-text));
  cursor: grab;
  padding: var(--puck-drawer-item-space, var(--puck-space-3));
  display: flex;
  border: var(--puck-drawer-item-border-width, var(--puck-border-width-regular)) var(--puck-drawer-item-color-border, var(--puck-color-border)) solid;
  border-radius: var(--puck-drawer-item-radius, var(--puck-radius-m));
  font-size: var(--puck-drawer-item-font-size, var(--puck-font-size-xxs));
  justify-content: space-between;
  align-items: center;
  transition: background-color var(--puck-duration-fast) var(--puck-ease-exit), color var(--puck-duration-fast) var(--puck-ease-exit);
}
._DrawerItem--disabled_1n90m_38 ._DrawerItem-draggable_1n90m_22 {
  background: var(--puck-color-surface-muted);
  color: var(--puck-color-text-muted);
  cursor: not-allowed;
}
._DrawerItem_1n90m_22:focus-visible {
  outline: 0;
}
._Drawer_1n90m_1:not(._Drawer--isDraggingFrom_1n90m_48) ._DrawerItem_1n90m_22:focus-visible ._DrawerItem-draggable_1n90m_22 {
  border-radius: var(--puck-radius-m);
  outline: var(--puck-border-width-focus) solid var(--puck-color-focus-ring);
  outline-offset: var(--puck-border-width-focus);
}
@media (hover: hover) and (pointer: fine) {
  ._Drawer_1n90m_1:not(._Drawer--isDraggingFrom_1n90m_48) ._DrawerItem_1n90m_22:not(._DrawerItem--disabled_1n90m_38) ._DrawerItem-draggable_1n90m_22:hover {
    background-color: var( --puck-drawer-item-color-bg-hover, var(--puck-color-interactive-soft-hover) );
    color: var( --puck-drawer-item-color-text-hover, var(--puck-color-interactive) );
    transition: none;
  }
}
._DrawerItem-name_1n90m_72 {
  overflow-x: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/DropZone/styles.module.css/#css-module-data */
._DropZone_wc2ks_1 {
  position: relative;
  height: 100%;
  min-height: var(--puck-slot-min-empty-height);
  outline-offset: calc(var(--puck-slot-border-width, var(--puck-border-width-focus)) * -1);
  width: 100%;
}
._DropZone--hasChildren_wc2ks_11 {
  min-height: 0;
}
._DropZone_wc2ks_1:empty {
  min-height: var(--puck-slot-min-empty-height);
}
[data-puck-entry]:not([data-puck-dragging]) ._DropZone_wc2ks_1 {
  transition: min-height var(--puck-duration-medium) var(--puck-ease-exit);
}
._DropZone--isAreaSelected_wc2ks_24,
._DropZone--hoveringOverArea_wc2ks_25:not(._DropZone--isRootZone_wc2ks_25) {
  background: var(--puck-slot-color-bg, var(--puck-color-selection-bg));
  outline: var(--puck-slot-border-width, var(--puck-border-width-focus)) var(--puck-slot-border-style, dashed) var(--puck-slot-color-border, var(--puck-color-selection-border));
}
._DropZone_wc2ks_1:empty {
  background: var(--puck-slot-color-bg, var(--puck-color-selection-bg));
  outline: var(--puck-slot-border-width, var(--puck-border-width-focus)) var(--puck-slot-border-style, dashed) var(--puck-slot-color-border, var(--puck-color-selection-border));
}
._DropZone-item_wc2ks_39 {
  position: relative;
}
._DropZone-linePlaceholder_wc2ks_43 {
  background: var( --puck-slot-component-color-placeholder, var(--puck-color-line-placeholder) );
  border-radius: calc(var(--puck-line-placeholder-width, 2px) / 2);
  pointer-events: none;
  position: absolute;
  z-index: 1;
}
._DropZone-hitbox_wc2ks_55 {
  position: absolute;
  bottom: calc(var(--puck-space-3) * -1);
  height: var(--puck-space-5);
  width: 100%;
  z-index: 1;
}
[data-puck-dragging] ._DropZone--isEnabled_wc2ks_63 {
  outline: var(--puck-slot-border-width, var(--puck-border-width-focus)) var(--puck-slot-border-style, dashed) var(--puck-slot-color-border, var(--puck-color-selection-border));
}
._DropZone_wc2ks_1 > *:not([data-puck-component]):not([data-puck-line-placeholder]) {
  opacity: 0;
}
body:has(._DropZone--isAnimating_wc2ks_74:empty) [data-puck-overlay] {
  opacity: 0 !important;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/InlineTextField/styles.module.css/#css-module-data */
._InlineTextField_104qp_1 {
  cursor: text;
  display: inline-block;
  white-space: pre-wrap;
  text-decoration: inherit;
}
[data-dnd-dragging] ._InlineTextField_104qp_1 {
  cursor: none;
  caret-color: transparent;
}
[data-dnd-dragging] ._InlineTextField_104qp_1::selection {
  display: none;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/Loader/styles.module.css/#css-module-data */
@keyframes _loader-animation_1w5zn_1 {
  0% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(0.8);
  }
  100% {
    transform: rotate(360deg) scale(1);
  }
}
._Loader_1w5zn_13 {
  background: transparent;
  border-radius: var(--puck-radius-round);
  border: var(--puck-border-width-focus) solid currentColor;
  border-bottom-color: transparent;
  display: inline-block;
  animation: _loader-animation_1w5zn_1 1s 0s infinite linear;
  animation-fill-mode: both;
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/RichTextMenu/styles.module.css/#css-module-data */
._RichTextMenu_1ve2j_1 {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}
._RichTextMenu--form_1ve2j_7 {
  border-top-left-radius: var(--puck-field-radius, var(--puck-radius-m));
  border-top-right-radius: var(--puck-field-radius, var(--puck-radius-m));
  padding: var(--puck-field-richtext-menu-space-y, 6px) var(--puck-field-richtext-menu-space-x, 6px);
  background-color: var( --puck-field-richtext-menu-color-bg, var(--puck-color-surface-subtle) );
  position: relative;
  scrollbar-width: none;
  overflow-x: auto;
}
._RichTextMenu-group_1ve2j_21 {
  display: flex;
  align-items: space-between;
  flex-direction: row;
  flex-wrap: nowrap;
  padding-inline: 6px;
  gap: 2px;
  position: relative;
}
._RichTextMenu-group_1ve2j_21:first-of-type {
  padding-left: 0;
}
._RichTextMenu-group_1ve2j_21:last-of-type {
  padding-right: 0;
}
._RichTextMenu--inline_1ve2j_39 ._RichTextMenu-group_1ve2j_21 {
  color: var(--puck-color-text-inverse);
  gap: 0px;
  flex-wrap: nowrap;
}
._RichTextMenu-group_1ve2j_21 + ._RichTextMenu-group_1ve2j_21 {
  border-left: var(--puck-border-width-regular) solid var( --puck-field-richtext-menu-color-separator, var(--puck-color-border-muted) );
}
._RichTextMenu--inline_1ve2j_39 ._RichTextMenu-group_1ve2j_21 + ._RichTextMenu-group_1ve2j_21 {
  border-left: var(--puck-border-width-hairline) solid var(--puck-color-border-inverse);
}

/* css-module:/home/runner/work/puck/puck/packages/core/components/RichTextMenu/components/Control/styles.module.css/#css-module-data */
._Control_id4pm_1 .lucide {
  height: var(--puck-icon-size-m);
  width: var(--puck-icon-size-m);
}
._Control--inline_id4pm_6 .lucide {
  height: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
  width: var(--puck-actionbar-action-size, var(--puck-icon-size-s));
}

/* components/DraggableComponent/styles.css */
[data-puck-component] * {
  pointer-events: none;
  user-select: none;
  -webkit-user-select: none;
}
[data-puck-component] {
  cursor: grab;
  pointer-events: auto !important;
  user-select: none;
  -webkit-user-select: none;
}
[data-puck-dropzone] {
  pointer-events: auto !important;
}
[data-puck-disabled] {
  cursor: pointer;
}
[data-dnd-placeholder]:not([data-puck-line-drag] *) {
  background: var( --puck-slot-component-color-placeholder, var(--puck-color-azure-06) ) !important;
  border: none !important;
  color: transparent !important;
  opacity: 0.3 !important;
  outline: none !important;
  transition: none !important;
}
[data-dnd-placeholder]:not([data-puck-line-drag] *) *,
[data-dnd-placeholder]:not([data-puck-line-drag] *)::after,
[data-dnd-placeholder]:not([data-puck-line-drag] *)::before {
  opacity: 0 !important;
}
[data-puck-line-drag] [data-dnd-placeholder] {
  opacity: 0.4 !important;
  outline: none !important;
  transition: none !important;
}
[data-puck-line-drag] [data-dnd-dragging][data-puck-component] {
  opacity: 0.9 !important;
}
[data-dnd-dragging][data-puck-component] {
  pointer-events: none !important;
  outline: var( --puck-slot-component-border-width, var(--puck-border-width-focus) ) var(--puck-slot-component-color-border-dragging, var(--puck-color-azure-09)) solid !important;
  outline-offset: calc(var(--puck-slot-component-border-width, var(--puck-border-width-focus)) * -1) !important;
}
[data-dnd-dragging][data-puck-component] > :first-child {
  margin-top: 0 !important;
}
[data-dnd-dragging][data-puck-component] > :last-child {
  margin-bottom: 0 !important;
}

/* lib/overlay-portal/styles.css */
[data-puck-overlay-portal],
[data-puck-overlay-portal] * {
  pointer-events: auto !important;
}
[data-puck-entry][data-puck-dragging] [data-puck-overlay-portal],
[data-puck-entry][data-puck-dragging] [data-puck-overlay-portal] * {
  pointer-events: none !important;
}
[data-puck-entry][data-puck-preview-mode=edit] [data-puck-overlay-portal]:hover {
  outline: 2px var(--puck-color-azure-09, #cfdff0) dashed;
  outline-offset: 2px;
}
[data-puck-entry][data-puck-preview-mode=edit] [data-puck-overlay-portal]:focus-within {
  outline: 2px var(--puck-color-azure-07, #88b0da) dashed;
  outline-offset: 2px;
}`,Ey="data-puck-style-source",Iy="puck",PA="data-puck-style-id",Cy={uiDefault:"ui-default",iframeInteractions:"iframe-styles"},Nf=new WeakMap,zA=e=>{if(e)return e;if(!(typeof document>"u"))return document},AA=e=>{const t=Nf.get(e);if(t)return t;const r=new Map;return Nf.set(e,r),r},Py=(e,t,r=!1)=>{const n=e.head;if(n){if(t.parentElement!==n){r?n.prepend(t):n.append(t);return}r&&n.firstChild!==t&&n.prepend(t),!r&&n.lastChild!==t&&n.append(t)}},jA=(e,t,r,n=!1)=>{const o=e.createElement("style");return o.setAttribute(Ey,Iy),o.setAttribute(PA,t),o.textContent=r,Py(e,o,n),o},zy=e=>(e==null?void 0:e.getAttribute(Ey))===Iy,Ay=e=>{const t=zA(e==null?void 0:e.document);g.useInsertionEffect(()=>{if(!e||!t)return;const r=AA(t),n=r.get(e.id);if(n)n.count=n.count+1,n.el.textContent!==e.cssText&&(n.el.textContent=e.cssText),Py(t,n.el,e.prepend);else{const o=jA(t,e.id,e.cssText,e.prepend);r.set(e.id,{count:1,el:o})}return()=>{const o=r.get(e.id);o&&(o.count=o.count-1,o.count<=0&&(o.el.remove(),r.delete(e.id)))}},[e==null?void 0:e.cssText,e==null?void 0:e.id,e==null?void 0:e.prepend,e==null?void 0:e.document,t])},ua=null,OA=()=>ua!==null?ua:typeof document>"u"?!1:(ua=getComputedStyle(document.documentElement).getPropertyValue("--_puck-styles-loaded").trim()!=="",ua),DA=()=>{const e=OA();Ay(e?null:{cssText:IA,id:Cy.uiDefault,prepend:!0}),g.useEffect(()=>{},[])},TA=e=>{Ay(e?{cssText:CA,document:e,id:Cy.iframeInteractions}:null)},Dd='style, link[rel="stylesheet"]',gl="data-puck-style-mirror",jy=e=>!e.matches(Dd)||zy(e)?!1:e.tagName==="STYLE"?!!e.innerHTML.trim():!0,MA=e=>{const t=[];return e.querySelectorAll(Dd).forEach(r=>{jy(r)&&t.push(r)}),t},Bf=e=>Array.from(document.styleSheets).find(t=>t.ownerNode.href===e.href),RA=e=>{if(e)try{return Array.from(e.cssRules).map(t=>t.cssText).join("")}catch{console.warn("Access to stylesheet %s is denied. Ignoring…",e.href)}return""},$f=(e,t)=>{const r=e.attributes;(r==null?void 0:r.length)>0&&Array.from(r).forEach(n=>{t.setAttribute(n.name,n.value)})},Wf=e=>setTimeout(e,0),LA=({children:e,debug:t=!1,onStylesLoaded:r=()=>null,syncHostStyles:n=!0})=>{const{document:o,window:i}=FA();return TA(o),g.useEffect(()=>{if(!i||!o)return()=>{};let a=[];const s={},l=()=>{a.forEach(({mirror:_})=>{_.remove()}),a=[],Array.from(o.head.querySelectorAll(`[${gl}="true"]`)).forEach(_=>{_.remove()}),Object.keys(s).forEach(_=>{delete s[_]})},c=_=>a.findIndex(I=>I.original===_),d=(_,I=!1)=>Se(null,null,function*(){let w;if(_.nodeName==="LINK"&&I){w=document.createElement("style"),w.type="text/css";let A=Bf(_);A||(yield new Promise(C=>{const S=()=>{C(),_.removeEventListener("load",S)};_.addEventListener("load",S)}),A=Bf(_));const E=RA(A);if(!E){t&&console.warn("Tried to load styles for link element, but couldn't find them. Skipping...");return}w.innerHTML=E,w.setAttribute("data-href",_.getAttribute("href"))}else w=_.cloneNode(!0);return w.setAttribute(gl,"true"),w}),u=_=>Se(null,null,function*(){const I=c(_);if(I>-1){t&&console.log("Tried to add an element that was already mirrored. Updating instead..."),a[I].mirror.innerText=_.innerText;return}const w=yield d(_);if(!w)return;const A=al(w.outerHTML);if(s[A]){t&&console.log("iframe already contains element that is being mirrored. Skipping...");return}s[A]=!0,o.head.append(w),a.push({original:_,mirror:w}),t&&console.log(`Added style node ${_.outerHTML}`)}),p=_=>{var I,w;const A=c(_);if(A===-1){t&&console.log("Tried to remove an element that did not exist. Skipping...");return}const E=al(_.outerHTML);(w=(I=a[A])==null?void 0:I.mirror)==null||w.remove(),delete s[E],t&&console.log(`Removed style node ${_.outerHTML}`)},v=new MutationObserver(_=>{_.forEach(I=>{I.type==="childList"&&(I.addedNodes.forEach(w=>{if(w.nodeType===Node.TEXT_NODE||w.nodeType===Node.ELEMENT_NODE){const A=w.nodeType===Node.TEXT_NODE?w.parentElement:w;A&&jy(A)&&Wf(()=>u(A))}}),I.removedNodes.forEach(w=>{if(w.nodeType===Node.TEXT_NODE||w.nodeType===Node.ELEMENT_NODE){const A=w.nodeType===Node.TEXT_NODE?w.parentElement:w;A&&A.matches(Dd)&&!zy(A)&&Wf(()=>p(A))}}))})});if(!n)return r(),()=>{v.disconnect(),l()};const h=i.parent.document,m=MA(h),y=[];let b=0;const k=h.getElementsByTagName("html")[0];$f(k,o.documentElement);const x=h.getElementsByTagName("body")[0];return $f(x,o.body),Promise.all(m.map((_,I)=>Se(null,null,function*(){if(_.nodeName==="LINK"){const A=_.href;if(y.indexOf(A)>-1)return;y.push(A)}const w=yield d(_);if(w)return a.push({original:_,mirror:w}),w}))).then(_=>{const I=_.filter(w=>typeof w<"u");I.forEach(w=>{w.onload=()=>{b=b+1,b>=I.length&&r()},w.onerror=()=>{const A=w instanceof HTMLLinkElement?w.href:void 0;console.warn(`AutoFrame couldn't load a stylesheet${A?`: ${A}`:""}. This can happen if the parent document's stylesheet is blocked by the iframe's CSP, returns a non-2xx status, or fails to reach the network.`),b=b+1,b>=I.length&&r()}}),o.head.querySelectorAll(`[${gl}="true"]`).forEach(w=>{w.remove()}),o.head.append(...I),I.forEach(w=>{w.nodeName==="STYLE"&&(b=b+1)}),b>=I.length&&r(),v.observe(h.head,{childList:!0,subtree:!0}),I.forEach(w=>{const A=al(w.outerHTML);s[A]=!0})}),()=>{v.disconnect(),l()}},[n]),f.jsx(f.Fragment,{children:e})},Td=g.createContext({}),FA=()=>g.useContext(Td);function Oy(e){var t=e,{children:r,className:n,debug:o,id:i,onReady:a=()=>{},onNotReady:s=()=>{},frameRef:l,syncHostStyles:c=!0}=t,d=Tt(t,["children","className","debug","id","onReady","onNotReady","frameRef","syncHostStyles"]);const[u,p]=g.useState(!1),[v,h]=g.useState({}),[m,y]=g.useState(),[b,k]=g.useState(!1);return g.useEffect(()=>{u&&k(!c)},[u,c]),g.useEffect(()=>{var x;if(l.current){const _=l.current.contentDocument,I=l.current.contentWindow;h({document:_||void 0,window:I||void 0}),y((x=l.current.contentDocument)==null?void 0:x.getElementById("frame-root")),_&&I&&b?a():s()}},[l,u,b]),f.jsx("iframe",N(D({},d),{className:n,id:i,srcDoc:'<!DOCTYPE html><html><head></head><body><div id="frame-root" data-puck-entry></div></body></html>',ref:l,onLoad:()=>{p(!0)},children:f.jsx(Td.Provider,{value:v,children:u&&m&&f.jsx(LA,{debug:o,onStylesLoaded:()=>k(!0),syncHostStyles:c,children:pr.createPortal(r,m)})})}))}Oy.displayName="AutoFrame";var NA=Oy;z();var BA=cu(Ic),Dy=g.memo(()=>{var e,t,r,n;const o=H(Be(u=>{var p;return(p=u.state.indexes.nodes.root)==null?void 0:p.flatData.props})),i=H(u=>u.config),a=H(u=>u.metadata),s=g.useMemo(()=>{const u=ro({props:o??{}});return ih(u)},[o]),l=Q_(i,s,BA),c=g.useMemo(()=>N(D({},l),{children:f.jsx(Pc,{zone:Je}),puck:{renderDropZone:Pc,isEditing:!0,dragRef:null,metadata:a},editMode:!0}),[l,a]),d=ps((t=(e=i.root)==null?void 0:e.fields)!=null?t:{},c);return(r=i.root)!=null&&r.render?(n=i.root)==null?void 0:n.render(N(D(D({},c),d),{id:"puck-root"})):f.jsx(f.Fragment,{children:c.children})});Dy.displayName="EditorPage";var $A=Dy;z();var WA={PuckPreview:"_PuckPreview_zbic3_1","PuckPreview-frame":"_PuckPreview-frame_zbic3_6"},ml=ee("PuckPreview",WA),HA=e=>{const t=H(r=>r.status);g.useEffect(()=>{if(e.current&&t==="READY"){const r=e.current,n=a=>{const s=new Z_("pointermove",N(D({},a),{bubbles:!0,cancelable:!1,clientX:a.clientX,clientY:a.clientY,pointerId:a.pointerId,pointerType:a.pointerType,isPrimary:a.isPrimary,originalTarget:a.target}));r.dispatchEvent(s)},o=()=>{var a;i(),(a=r.contentDocument)==null||a.addEventListener("pointermove",n,{capture:!0})},i=()=>{var a;(a=r.contentDocument)==null||a.removeEventListener("pointermove",n)};return o(),()=>{i()}}},[t])},VA=e=>{const t=H(o=>o.state.ui.previewMode),r=H(o=>o.status),n=H(o=>o.iframe.enabled);g.useEffect(()=>{var o,i;const a=n?(i=(o=e.current)==null?void 0:o.contentDocument)==null?void 0:i.querySelector("[data-puck-entry]"):e.current;a==null||a.setAttribute("data-puck-preview-mode",t)},[t,r,n])},Ty=({id:e="puck-preview"})=>{const t=H(u=>u.dispatch),r=H(u=>u.config),n=H(u=>u.setStatus),o=H(u=>u.iframe),i=H(u=>u.overrides),a=H(u=>u.metadata),s=H(u=>u.state.ui.previewMode==="edit"?null:u.state.data),l=g.useMemo(()=>i.iframe,[i]),c=g.useRef(null);HA(c),VA(c);const d=s?f.jsx(oz,{data:s,config:r,metadata:a}):f.jsx($A,{});return g.useEffect(()=>{o.enabled||n("READY")},[o.enabled]),f.jsx("div",{className:ml(),id:e,"data-puck-preview":!0,onClick:u=>{const p=u.target;!p.hasAttribute("data-puck-component")&&!p.hasAttribute("data-puck-dropzone")&&t({type:"setUi",ui:{itemSelector:null}})},children:o.enabled?f.jsx(NA,{id:"preview-frame",className:ml("frame"),"data-rfd-iframe":!0,syncHostStyles:o.syncHostStyles,onReady:()=>{n("READY")},onNotReady:()=>{n("MOUNTED")},frameRef:c,children:f.jsx(Td.Consumer,{children:({document:u})=>l?f.jsx(l,{document:u,children:d}):d})}):f.jsx("div",{id:"preview-frame",className:ml("frame"),ref:c,"data-puck-entry":!0,children:d})})};z();z();var qA=({overrides:e,plugins:t})=>{const r=D({},e);return t==null||t.forEach(n=>{n.overrides&&Object.keys(n.overrides).forEach(o=>{var i;const a=o;if(!((i=n.overrides)!=null&&i[a]))return;if(a==="fieldTypes"){const c=n.overrides.fieldTypes;Object.keys(c).forEach(d=>{r.fieldTypes=r.fieldTypes||{};const u=r.fieldTypes[d],p=v=>c[d](N(D({},v),{children:u?u(v):v.children}));r.fieldTypes[d]=p});return}const s=r[a],l=c=>n.overrides[a](N(D({},c),{children:s?s(c):c.children}));r[a]=l})}),r},UA=({overrides:e,plugins:t})=>g.useMemo(()=>qA({overrides:e,plugins:t}),[t,e]);z();z();var Md={Puck:"_Puck_tzaxg_19","Puck-portal":"_Puck-portal_tzaxg_31",PuckLayout:"_PuckLayout_tzaxg_36","PuckLayout-inner":"_PuckLayout-inner_tzaxg_40","Puck--hidePlugins":"_Puck--hidePlugins_tzaxg_73","PuckLayout--mounted":"_PuckLayout--mounted_tzaxg_78","PuckLayout--mobilePanelHeightToggle":"_PuckLayout--mobilePanelHeightToggle_tzaxg_82","PuckLayout--leftSideBarVisible":"_PuckLayout--leftSideBarVisible_tzaxg_82","PuckLayout--isExpanded":"_PuckLayout--isExpanded_tzaxg_90","PuckLayout--mobilePanelHeightMinContent":"_PuckLayout--mobilePanelHeightMinContent_tzaxg_110","PuckLayout--rightSideBarVisible":"_PuckLayout--rightSideBarVisible_tzaxg_137","PuckLayout-mounted":"_PuckLayout-mounted_tzaxg_156","PuckLayout-nav":"_PuckLayout-nav_tzaxg_197","PuckLayout-header":"_PuckLayout-header_tzaxg_217",PuckPluginTab:"_PuckPluginTab_tzaxg_231","PuckPluginTab--visible":"_PuckPluginTab--visible_tzaxg_237","PuckPluginTab-body":"_PuckPluginTab-body_tzaxg_243"};z();var jc=({children:e})=>f.jsx(f.Fragment,{children:e});z();var ZA=()=>{const e=ye(),t=g.useCallback(()=>{const r=e.getState().dispatch;r({type:"setUi",ui:n=>({previewMode:n.previewMode==="edit"?"interactive":"edit"})})},[e]);Ht({meta:!0,i:!0},t),Ht({ctrl:!0,i:!0},t)};z();z();z();var YA={MenuBar:"_MenuBar_1hxnj_1","MenuBar--menuOpen":"_MenuBar--menuOpen_1hxnj_14","MenuBar-inner":"_MenuBar-inner_1hxnj_29","MenuBar-history":"_MenuBar-history_1hxnj_45"},_l=ee("MenuBar",YA);function KA({menuOpen:e=!1,renderHeaderActions:t,setMenuOpen:r}){const n=H(c=>c.history.back),o=H(c=>c.history.forward),i=H(c=>c.history.hasFuture()),a=H(c=>c.history.hasPast()),s=J("header-undo"),l=J("header-redo");return f.jsx("div",{className:_l({menuOpen:e}),onClick:c=>{var d;const u=c.target;window.matchMedia("(min-width: 638px)").matches||u.tagName==="A"&&((d=u.getAttribute("href"))!=null&&d.startsWith("#"))&&r(!1)},children:f.jsxs("div",{className:_l("inner"),children:[f.jsxs("div",{className:_l("history"),children:[f.jsx(Ke,{type:"button",title:s,disabled:!a,onClick:n,children:f.jsx(lw,{size:21})}),f.jsx(Ke,{type:"button",title:l,disabled:!i,onClick:o,children:f.jsx(Q1,{size:21})})]}),f.jsx(f.Fragment,{children:t&&t()})]})})}z();var XA={PuckHeader:"_PuckHeader_c2nei_1","PuckHeader--hidePlugins":"_PuckHeader--hidePlugins_c2nei_21","PuckHeader-inner":"_PuckHeader-inner_c2nei_26","PuckHeader-toggle":"_PuckHeader-toggle_c2nei_46","PuckHeader-rightSideBarToggle":"_PuckHeader-rightSideBarToggle_c2nei_52","PuckHeader-leftSideBarToggle":"_PuckHeader-leftSideBarToggle_c2nei_53","PuckHeader-title":"_PuckHeader-title_c2nei_64","PuckHeader-path":"_PuckHeader-path_c2nei_68","PuckHeader-tools":"_PuckHeader-tools_c2nei_75","PuckHeader-menuButton":"_PuckHeader-menuButton_c2nei_81","PuckHeader--menuOpen":"_PuckHeader--menuOpen_c2nei_86"},rr=ee("PuckHeader",XA),GA=({hidePlugins:e})=>{const{onPublish:t,renderHeader:r,renderHeaderActions:n,headerTitle:o,headerPath:i,iframe:a}=As(),s=H(E=>E.dispatch),l=ye(),c=g.useMemo(()=>r?(console.warn("`renderHeader` is deprecated. Please use `overrides.header` and the `usePuck` hook instead"),C=>{var S=C,{actions:j}=S,O=Tt(S,["actions"]);const L=r,$=H(F=>F.state);return f.jsx(L,N(D({},O),{dispatch:s,state:$,children:j}))}):jc,[r]),d=g.useMemo(()=>n?(console.warn("`renderHeaderActions` is deprecated. Please use `overrides.headerActions` and the `usePuck` hook instead."),C=>{const S=n,j=H(O=>O.state);return f.jsx(S,N(D({},C),{dispatch:s,state:j}))}):jc,[n]),u=H(E=>E.overrides.header||c),p=H(E=>E.overrides.headerActions||d),[v,h]=g.useState(!1),m=H(E=>{var C,S;return(S=((C=E.state.indexes.nodes.root)==null?void 0:C.data).props.title)!=null?S:""}),y=H(E=>E.state.ui.leftSideBarVisible),b=H(E=>E.state.ui.rightSideBarVisible),k=g.useCallback(E=>{const C=window.matchMedia("(min-width: 638px)").matches,S=E==="left"?y:b,j=E==="left"?"rightSideBarVisible":"leftSideBarVisible";s({type:"setUi",ui:D({[`${E}SideBarVisible`]:!S},C?{}:{[j]:!1})})},[s,y,b]),x=J("header-publish"),_=J("label-page"),I=J("header-toggle-leftsidebar"),w=J("header-toggle-rightsidebar"),A=J("header-toggle-menubar");return f.jsx(u,{actions:f.jsx(f.Fragment,{children:f.jsx(p,{children:f.jsx(kc,{onClick:()=>{const E=l.getState().state.data;t&&t(E)},icon:f.jsx(_p,{size:"14px"}),children:x})})}),children:f.jsx("header",{className:rr({leftSideBarVisible:y,rightSideBarVisible:b,hidePlugins:e}),children:f.jsxs("div",{className:rr("inner"),children:[f.jsxs("div",{className:rr("toggle"),children:[f.jsx("div",{className:rr("leftSideBarToggle"),children:f.jsx(Ke,{type:"button",onClick:()=>{k("left")},title:I,children:f.jsx(Y1,{focusable:"false"})})}),f.jsx("div",{className:rr("rightSideBarToggle"),children:f.jsx(Ke,{type:"button",onClick:()=>{k("right")},title:w,children:f.jsx(K1,{focusable:"false"})})})]}),f.jsx("div",{className:rr("title"),children:f.jsxs(Cs,{rank:"2",size:"xs",children:[o||m||_,i&&f.jsxs(f.Fragment,{children:[" ",f.jsx("code",{className:rr("path"),children:i})]})]})}),f.jsxs("div",{className:rr("tools"),children:[f.jsx("div",{className:rr("menuButton"),children:f.jsx(Ke,{type:"button",onClick:()=>h(!v),title:A,children:v?f.jsx(Sv,{focusable:"false"}):f.jsx(ci,{focusable:"false"})})}),f.jsx(KA,{dispatch:s,onPublish:t,menuOpen:v,renderHeaderActions:()=>f.jsx(p,{children:f.jsx(kc,{onClick:()=>{const E=l.getState().state.data;t&&t(E)},icon:f.jsx(_p,{size:"14px"}),children:x})}),setMenuOpen:h})]})]})})})},JA=g.memo(GA);z();z();var QA={SidebarSection:"_SidebarSection_1uv88_1","SidebarSection-title":"_SidebarSection-title_1uv88_12","SidebarSection--noBorderTop":"_SidebarSection--noBorderTop_1uv88_20","SidebarSection-content":"_SidebarSection-content_1uv88_24","SidebarSection-breadcrumbLabel":"_SidebarSection-breadcrumbLabel_1uv88_33","SidebarSection-breadcrumbs":"_SidebarSection-breadcrumbs_1uv88_62","SidebarSection-breadcrumb":"_SidebarSection-breadcrumb_1uv88_33","SidebarSection-heading":"_SidebarSection-heading_1uv88_74","SidebarSection-loadingOverlay":"_SidebarSection-loadingOverlay_1uv88_78"},On=ee("SidebarSection",QA),ej=({children:e,title:t,background:r,showBreadcrumbs:n,noBorderTop:o,isLoading:i})=>f.jsxs("div",{className:On({noBorderTop:o}),style:{background:r},children:[f.jsx("div",{className:On("title"),children:f.jsxs("div",{className:On("breadcrumbs"),children:[n&&f.jsx(Sy,{}),f.jsx("div",{className:On("heading"),children:f.jsx(Cs,{rank:"2",size:"xs",children:t})})]})}),f.jsx("div",{className:On("content"),children:e}),i&&f.jsx("div",{className:On("loadingOverlay"),children:f.jsx(pn,{size:32})})]});z();z();z();var My={ViewportControls:"_ViewportControls_v26yb_1","ViewportControls--fullScreen":"_ViewportControls--fullScreen_v26yb_5","ViewportControls-toggleButton":"_ViewportControls-toggleButton_v26yb_14","ViewportControls-actions":"_ViewportControls-actions_v26yb_39","ViewportControls-actionsInner":"_ViewportControls-actionsInner_v26yb_43","ViewportControls--isExpanded":"_ViewportControls--isExpanded_v26yb_67","ViewportControls-divider":"_ViewportControls-divider_v26yb_72","ViewportControls-zoomSelect":"_ViewportControls-zoomSelect_v26yb_79","ViewportControls-zoom":"_ViewportControls-zoom_v26yb_79","ViewportButton-inner":"_ViewportButton-inner_v26yb_110","ViewportButton--isActive":"_ViewportButton--isActive_v26yb_118"},Hf={Smartphone:f.jsx(rw,{size:16}),Tablet:f.jsx(iw,{size:16}),Monitor:f.jsx(Pv,{size:16}),FullWidth:f.jsx(O1,{size:16})},br=ee("ViewportControls",My),Vf=ee("ViewportButton",My),Oc=({children:e,title:t,onClick:r,isActive:n,disabled:o})=>f.jsx("span",{className:Vf({isActive:n}),suppressHydrationWarning:!0,children:f.jsx(Ke,{type:"button",title:t,disabled:o||n,onClick:r,suppressHydrationWarning:!0,children:f.jsx("span",{className:Vf("inner"),children:e})})}),qf=[{label:"25%",value:.25},{label:"50%",value:.5},{label:"75%",value:.75},{label:"100%",value:1},{label:"125%",value:1.25},{label:"150%",value:1.5},{label:"200%",value:2}],tj=({viewport:e,isActive:t,onClick:r})=>{var n;const o=J("viewport-switch",{label:(n=e.label)!=null?n:""}),i=J("viewport-switch-default");return f.jsx(Oc,{title:e.label?o:i,onClick:r,isActive:t,children:typeof e.icon=="string"?Hf[e.icon]||e.icon:e.icon||Hf.Smartphone})},rj=({autoZoom:e,zoom:t,onViewportChange:r,onZoom:n,fullScreen:o})=>{var i,a;const s=H(x=>x.viewports),l=H(x=>x.state.ui.viewports),c=qf.find(x=>x.value===e),d=J("viewport-zoom-auto",{zoom:(e*100).toFixed(0)}),u=g.useMemo(()=>[...qf,...c?[]:[{value:e,label:d}]].filter(x=>x.value<=e).sort((x,_)=>x.value>_.value?1:-1),[e,d]),[p,v]=g.useState(l.current.width);g.useEffect(()=>{v(l.current.width)},[l.current]);const[h,m]=g.useState(!1),y=J("viewport-zoom-out"),b=J("viewport-zoom-in"),k=J("viewport-toggle-menu");return f.jsxs("div",{className:br({isExpanded:h,fullScreen:o}),suppressHydrationWarning:!0,children:[f.jsx("div",{className:br("actions"),children:f.jsxs("div",{className:br("actionsInner"),children:[s.map((x,_)=>f.jsx(tj,{viewport:x,onClick:()=>{v(x.width),r(x)},isActive:p===x.width},_)),f.jsx("div",{className:br("divider")}),f.jsx(Oc,{title:y,disabled:t<=((i=u[0])==null?void 0:i.value),onClick:x=>{x.stopPropagation(),n(u[Math.max(u.findIndex(_=>_.value===t)-1,0)].value)},children:f.jsx(dw,{size:16})}),f.jsx(Oc,{title:b,disabled:t>=((a=u[u.length-1])==null?void 0:a.value),onClick:x=>{x.stopPropagation(),n(u[Math.min(u.findIndex(_=>_.value===t)+1,u.length-1)].value)},children:f.jsx(uw,{size:16})}),f.jsxs("div",{className:br("zoom"),children:[f.jsx("div",{className:br("divider")}),f.jsx("select",{className:br("zoomSelect"),value:t.toString(),onClick:x=>{x.stopPropagation()},onChange:x=>{n(parseFloat(x.currentTarget.value))},children:u.map(x=>f.jsx("option",{value:x.value,label:x.label},x.label))})]})]})}),f.jsx("button",{className:br("toggleButton"),title:k,onClick:()=>m(x=>!x),children:h?f.jsx(cw,{size:16}):f.jsx(Pv,{size:16})})]})};z();var nj={PuckCanvas:"_PuckCanvas_zw9iy_1","PuckCanvas-controls":"_PuckCanvas-controls_zw9iy_18","PuckCanvas--fullScreen":"_PuckCanvas--fullScreen_zw9iy_23","PuckCanvas-inner":"_PuckCanvas-inner_zw9iy_34","PuckCanvas-root":"_PuckCanvas-root_zw9iy_43","PuckCanvas--ready":"_PuckCanvas--ready_zw9iy_68","PuckCanvas-loader":"_PuckCanvas-loader_zw9iy_73","PuckCanvas--showLoader":"_PuckCanvas--showLoader_zw9iy_84"};z();var Ry=g.createContext(null),oj=({children:e})=>{const t=g.useRef(null),r=g.useMemo(()=>({frameRef:t}),[]);return f.jsx(Ry.Provider,{value:r,children:e})},Ly=()=>{const e=g.useContext(Ry);if(e===null)throw new Error("useCanvasFrame must be used within a FrameProvider");return e},zo=ee("PuckCanvas",nj),yl=150,ij=()=>{var e;const{frameRef:t}=Ly(),r=Dv(t),{viewports:n=oi,ui:o}=As(),{dispatch:i,overrides:a,setUi:s,zoomConfig:l,setZoomConfig:c,status:d,iframe:u,_experimentalFullScreenCanvas:p}=H(Be(j=>({dispatch:j.dispatch,overrides:j.overrides,setUi:j.setUi,zoomConfig:j.zoomConfig,setZoomConfig:j.setZoomConfig,status:j.status,iframe:j.iframe,_experimentalFullScreenCanvas:j._experimentalFullScreenCanvas}))),{leftSideBarVisible:v,rightSideBarVisible:h,leftSideBarWidth:m,rightSideBarWidth:y,viewports:b}=H(Be(j=>({leftSideBarVisible:j.state.ui.leftSideBarVisible,rightSideBarVisible:j.state.ui.rightSideBarVisible,leftSideBarWidth:j.state.ui.leftSideBarWidth,rightSideBarWidth:j.state.ui.rightSideBarWidth,viewports:j.state.ui.viewports}))),[k,x]=g.useState(!1),_=g.useRef(!1),I=g.useMemo(()=>({children:O})=>f.jsx(f.Fragment,{children:O}),[]),w=g.useMemo(()=>a.preview||I,[a]),A=g.useCallback(()=>{if(t.current){const j=t.current,O=Ov(j);return{width:O.contentBox.width,height:O.contentBox.height}}return{width:0,height:0}},[t]);g.useEffect(()=>{r()},[t,v,h,m,y,b]),g.useEffect(()=>{const{height:j}=A();b.current.height==="auto"&&c(N(D({},l),{rootHeight:j/l.zoom}))},[l.zoom,A,c]),g.useEffect(()=>{r()},[b.current.width,b]),g.useEffect(()=>{if(!t.current)return;const j=new ResizeObserver(()=>{_.current||r()});return j.observe(t.current),()=>{j.disconnect()}},[t.current]);const[E,C]=g.useState(!1);g.useEffect(()=>{setTimeout(()=>{C(!0)},500)},[]);const S=ye();return g.useEffect(()=>{var j,O;if(typeof window>"u"||(j=o==null?void 0:o.viewports)!=null&&j.current)return;const L=window.innerWidth,$=(O=t.current)==null?void 0:O.getBoundingClientRect().width;if(!L||!$||n.length===0)return;const F=Object.values(n).find(B=>B.width==="100%"),M=!!F;let W=Object.entries(n).filter(([B,Z])=>Z.width!=="100%").map(([B,Z])=>({key:B,diff:Math.abs(L-(typeof Z.width=="string"?L:Z.width)),value:Z})).sort((B,Z)=>B.diff>Z.diff?1:-1)[0].value;if(W.width<$&&M&&(W=F),u.enabled){const B=S.getState(),Z={state:N(D({},B.state),{ui:N(D({},B.state.ui),{viewports:N(D({},B.state.ui.viewports),{current:N(D({},B.state.ui.viewports.current),{height:(W==null?void 0:W.height)||"auto",width:W==null?void 0:W.width})})})})};let oe=B.history;B.history.histories.length===1&&(oe=N(D({},oe),{histories:[Z]})),S.setState(N(D({},Z),{history:oe}))}},[n,t.current,u,S,(e=o==null?void 0:o.viewports)==null?void 0:e.current]),f.jsxs("div",{className:zo({ready:d==="READY"||!u.enabled||!u.waitForStyles,showLoader:E,fullScreen:p}),onClick:j=>{const O=j.target;!O.hasAttribute("data-puck-component")&&!O.hasAttribute("data-puck-dropzone")&&i({type:"setUi",ui:{itemSelector:null},recordHistory:!1})},children:[b.controlsVisible&&u.enabled&&f.jsx("div",{className:zo("controls"),children:f.jsx(rj,{fullScreen:p,autoZoom:l.autoZoom,zoom:l.zoom,onViewportChange:j=>{x(!0),_.current=!0;const O=N(D({},j),{height:j.height||"auto",zoom:l.zoom}),L={viewports:N(D({},b),{current:O})};s(L),r({viewports:N(D({},b),{current:O})})},onZoom:j=>{x(!0),_.current=!0,c(N(D({},l),{zoom:j}))}})}),f.jsxs("div",{className:zo("inner"),ref:t,children:[f.jsx("div",{className:zo("root"),style:{width:u.enabled?b.current.width:"100%",height:l.rootHeight,transform:u.enabled?`scale(${l.zoom})`:void 0,transition:k?`width ${yl}ms ease-out, height ${yl}ms ease-out, transform ${yl}ms ease-out`:"",overflow:u.enabled?void 0:"auto"},suppressHydrationWarning:!0,id:"puck-canvas-root",onTransitionEnd:()=>{x(!1),_.current=!1},children:f.jsx(w,{children:f.jsx(Ty,{})})}),f.jsx("div",{className:zo("loader"),children:f.jsx(pn,{size:24})})]})]})};z();function Uf(e,t){const[r,n]=g.useState(null),o=g.useRef(null),i=H(s=>e==="left"?s.state.ui.leftSideBarWidth:s.state.ui.rightSideBarWidth);g.useEffect(()=>{if(typeof window<"u"&&!i)try{const s=localStorage.getItem("puck-sidebar-widths");if(s){const c=JSON.parse(s)[e];c&&t({type:"setUi",ui:{[e==="left"?"leftSideBarWidth":"rightSideBarWidth"]:c}})}}catch(s){console.error(`Failed to load ${e} sidebar width from localStorage`,s)}},[t,e,i]),g.useEffect(()=>{i!==void 0&&n(i)},[i]);const a=g.useCallback(s=>{t({type:"setUi",ui:{[e==="left"?"leftSideBarWidth":"rightSideBarWidth"]:s}});let l={};try{const c=localStorage.getItem("puck-sidebar-widths");l=c?JSON.parse(c):{}}catch(c){console.error(`Failed to save ${e} sidebar width to localStorage`,c)}finally{localStorage.setItem("puck-sidebar-widths",JSON.stringify(N(D({},l),{[e]:s})))}window.dispatchEvent(new CustomEvent("viewportchange",{bubbles:!0,cancelable:!1}))},[t,e]);return{width:r,setWidth:n,sidebarRef:o,handleResizeEnd:a}}z();z();z();var aj={ResizeHandle:"_ResizeHandle_144bf_2","ResizeHandle--left":"_ResizeHandle--left_144bf_16","ResizeHandle--right":"_ResizeHandle--right_144bf_20"},sj=ee("ResizeHandle",aj),lj=({position:e,sidebarRef:t,onResize:r,onResizeEnd:n})=>{const{frameRef:o}=Ly(),i=Dv(o),a=g.useRef(null),s=g.useRef(!1),l=g.useRef(0),c=g.useRef(0),d=g.useCallback(v=>{if(!s.current)return;const h=v.clientX-l.current,m=e==="left"?c.current+h:c.current-h,y=Math.max(192,m);r(y),v.preventDefault()},[r,e]),u=g.useCallback(()=>{var v;if(!s.current)return;s.current=!1,document.body.style.cursor="",document.body.style.userSelect="";const h=document.getElementById("resize-overlay");h&&document.body.removeChild(h),document.removeEventListener("mousemove",d),document.removeEventListener("mouseup",u);const m=((v=t.current)==null?void 0:v.getBoundingClientRect().width)||0;n(m),i()},[n]),p=g.useCallback(v=>{var h;s.current=!0,l.current=v.clientX,c.current=((h=t.current)==null?void 0:h.getBoundingClientRect().width)||0,document.body.style.cursor="col-resize",document.body.style.userSelect="none";const m=document.createElement("div");m.id="resize-overlay",m.setAttribute("data-resize-overlay",""),document.body.appendChild(m),document.addEventListener("mousemove",d),document.addEventListener("mouseup",u),v.preventDefault()},[e,d,u]);return f.jsx("div",{ref:a,className:sj({[e]:!0}),onMouseDown:p})};z();var cj={Sidebar:"_Sidebar_16oed_1","Sidebar--isVisible":"_Sidebar--isVisible_16oed_10","Sidebar--left":"_Sidebar--left_16oed_14","Sidebar--right":"_Sidebar--right_16oed_34","Sidebar-resizeHandle":"_Sidebar-resizeHandle_16oed_51"},Zf=ee("Sidebar",cj),Yf=({position:e,sidebarRef:t,isVisible:r,onResize:n,onResizeEnd:o,children:i})=>f.jsxs(f.Fragment,{children:[f.jsx("div",{ref:t,className:Zf({[e]:!0,isVisible:r}),children:i}),f.jsx("div",{className:`${Zf("resizeHandle")}`,children:f.jsx(lj,{position:e,sidebarRef:t,onResize:n,onResizeEnd:o})})]});z();var uj=e=>{let t=e;for(;t&&t!==document.body;){const r=window.getComputedStyle(t);if(r.display==="none"||r.visibility==="hidden"||r.opacity==="0"||t.getAttribute("aria-hidden")==="true"||t.hasAttribute("hidden"))return!1;t=t.parentElement}return!0},dj=e=>{var t;if(e!=null&&e.defaultPrevented)return!0;const r=((t=e==null?void 0:e.composedPath)==null?void 0:t.call(e)[0])||(e==null?void 0:e.target)||document.activeElement;if(r instanceof HTMLElement){const o=r.tagName.toLowerCase();if(o==="input"||o==="textarea"||o==="select"||r.isContentEditable)return!0;const i=r.getAttribute("role");if(i==="textbox"||i==="combobox"||i==="searchbox"||i==="listbox"||i==="grid")return!0}const n=document.querySelector('dialog[open], [aria-modal="true"], [role="dialog"], [role="alertdialog"]');return!!(n&&uj(n))},pj=()=>{const e=ye(),t=g.useCallback(r=>{var n;if(dj(r))return!1;const{state:o,dispatch:i,permissions:a,selectedItem:s}=e.getState(),l=(n=o.ui)==null?void 0:n.itemSelector;return!(l!=null&&l.zone)||!s||!a.getPermissions({item:s}).delete||i({type:"remove",index:l.index,zone:l.zone}),!0},[e]);Ht({delete:!0},t),Ht({backspace:!0},t)};z();z();var Fy={Nav:"_Nav_vll2r_1","Nav-list":"_Nav-list_vll2r_5","Nav-mobileActions":"_Nav-mobileActions_vll2r_23","NavItem-link":"_NavItem-link_vll2r_39",NavItem:"_NavItem_vll2r_39","NavItem-linkIcon":"_NavItem-linkIcon_vll2r_90","NavItem--active":"_NavItem--active_vll2r_100","NavItem--mobileOnly":"_NavItem--mobileOnly_vll2r_136","NavItem--desktopOnly":"_NavItem--desktopOnly_vll2r_141"},bl=ee("Nav",Fy),da=ee("NavItem",Fy),fj=({label:e,icon:t,onClick:r,isActive:n,mobileOnly:o,desktopOnly:i})=>f.jsx("li",{className:da({active:n,mobileOnly:o,desktopOnly:i}),children:r&&f.jsxs("div",{className:da("link"),onClick:r,children:[t&&f.jsx("span",{className:da("linkIcon"),children:t}),f.jsx("span",{className:da("linkLabel"),children:e})]})}),hj=({items:e,mobileActions:t})=>f.jsxs("nav",{className:bl(),children:[f.jsx("ul",{className:bl("list"),children:Object.entries(e).map(([r,n])=>f.jsx(fj,D({},n),r))}),t&&f.jsx("div",{className:bl("mobileActions"),children:t})]});z();var Ny=e=>D({enabled:!0,waitForStyles:!0,syncHostStyles:!0},e),Kf=ee("Puck",Md),pa=ee("PuckLayout",Md),Xf=ee("PuckPluginTab",Md),vj=typeof window>"u"?g.useEffect:g.useLayoutEffect,gj=()=>{const e=J("label-page"),t=H(r=>{var n,o,i;return r.selectedItem?(o=(n=r.config.components[r.selectedItem.type])==null?void 0:n.label)!=null?o:r.selectedItem.type.toString():(i=r.config.root)==null?void 0:i.label});return f.jsx(ej,{noBorderTop:!0,showBreadcrumbs:!0,title:t||e,children:f.jsx(Od,{})})},mj=({children:e,visible:t,mobileOnly:r})=>f.jsx("div",{className:Xf({visible:t,mobileOnly:r}),children:f.jsx("div",{className:Xf("body"),children:e})}),By=({children:e})=>{var t,r;const{iframe:n,initialHistory:o,plugins:i,height:a}=As(),s=H(Q=>Q.dnd),l=g.useMemo(()=>Ny(n),[n]);DA();const c=H(Q=>Q.dispatch),d=H(Q=>Q.state.ui.leftSideBarVisible),u=H(Q=>Q.state.ui.rightSideBarVisible),p=H(Q=>Q.instanceId),{width:v,setWidth:h,sidebarRef:m,handleResizeEnd:y}=Uf("left",c),{width:b,setWidth:k,sidebarRef:x,handleResizeEnd:_}=Uf("right",c);g.useEffect(()=>{window.matchMedia("(min-width: 638px)").matches||c({type:"setUi",ui:{leftSideBarVisible:!1,rightSideBarVisible:!1}});const Q=()=>{window.matchMedia("(min-width: 638px)").matches||c({type:"setUi",ui:ie=>D(D({},ie),ie.rightSideBarVisible?{leftSideBarVisible:!1}:{})})};return window.addEventListener("resize",Q),()=>{window.removeEventListener("resize",Q)}},[]);const I=H(Q=>Q.overrides),w=g.useMemo(()=>I.puck||jc,[I]),[A,E]=g.useState(!1);vj(()=>{E(!0)},[]);const C=H(Q=>Q.status==="READY");pw(),g.useEffect(()=>{if(C&&l.enabled){const Q=gt();if(Q)return zv(Q)}},[C,l.enabled]),ZA(),pj();const S={};v&&(S["--puck-user-sidebar-left-width"]=`${v}px`),b&&(S["--puck-user-sidebar-right-width"]=`${b}px`);const j=H(Q=>Q.setUi),O=H(Q=>{var ie;return(ie=Q.state.ui.plugin)==null?void 0:ie.current}),L=ye(),$=g.useMemo(()=>!!(i!=null&&i.find(Q=>Q.name==="legacy-side-bar")),[i]),F=J("plugin-blocks"),M=J("plugin-outline"),q=J("plugin-fields"),W=g.useMemo(()=>{const Q={},ie=[fz({label:F}),fA({label:M})],ke=P=>P.name==="legacy-side-bar"?-1:0,Y=[...ie,...i??[]].sort((P,T)=>ke(P)-ke(T));return i!=null&&i.some(P=>P.name==="fields")||Y.push(EA({label:q})),Y==null||Y.forEach(P=>{var T,R,U;P.name&&P.render&&(Q[P.name]&&delete Q[P.name],Q[P.name]={label:(T=P.label)!=null?T:P.name,icon:(R=P.icon)!=null?R:f.jsx(aw,{}),onClick:()=>{P.name===O?j(d?{leftSideBarVisible:!1}:{leftSideBarVisible:!0}):P.name&&j({plugin:{current:P.name},leftSideBarVisible:!0})},isActive:d&&O===P.name,render:P.render,mobilePanelHeight:(U=P.mobilePanelHeight)!=null?U:"toggle",mobileOnly:$||P.mobileOnly,desktopOnly:P.name==="legacy-side-bar"||P.desktopOnly})}),Q},[i,O,L,d,F,M,q]),B=O??Object.keys(W)[0],Z=(r=(t=W[B])==null?void 0:t.mobilePanelHeight)!=null?r:"toggle";g.useEffect(()=>{if(!O){const Q=Object.keys(W);j({plugin:{current:Q[0]}})}},[W,O]);const oe=W.fields&&W.fields.mobileOnly===!1,K=H(Q=>{var ie;return(ie=Q.state.ui.mobilePanelExpanded)!=null?ie:!1}),te=J("layout-maximize"),be=J("layout-minimize");return f.jsxs("div",{className:`Puck ${Kf({hidePlugins:$})}`,id:p,style:{height:a,visibility:"hidden"},children:[f.jsx(zP,{disableAutoScroll:s==null?void 0:s.disableAutoScroll,behavior:s==null?void 0:s.behavior,children:f.jsx(w,{children:e||f.jsx(oj,{children:f.jsx("div",{className:pa({leftSideBarVisible:d,mounted:A,rightSideBarVisible:!oe&&u,isExpanded:K,mobilePanelHeightToggle:Z==="toggle",mobilePanelHeightMinContent:Z==="min-content"}),style:{height:a},children:f.jsxs("div",{className:pa("inner"),style:S,children:[f.jsx("div",{className:pa("header"),children:f.jsx(JA,{hidePlugins:$})}),f.jsx("div",{className:pa("nav"),children:f.jsx(hj,{items:W,mobileActions:d&&Z==="toggle"&&f.jsx(Ke,{type:"button",title:K?be:te,onClick:()=>{j({mobilePanelExpanded:!K})},children:K?f.jsx(U1,{size:21}):f.jsx(q1,{size:21})})})}),f.jsx(Yf,{position:"left",sidebarRef:m,isVisible:d,onResize:h,onResizeEnd:y,children:Object.entries(W).map(([Q,{mobileOnly:ie,render:ke,label:Y}])=>f.jsx(mj,{visible:O===Q,mobileOnly:ie,children:f.jsx(ke,{})},Q))}),f.jsx(ij,{}),!oe&&f.jsx(Yf,{position:"right",sidebarRef:x,isVisible:u,onResize:k,onResizeEnd:_,children:f.jsx(gj,{})})]})})})})}),f.jsx("div",{id:"puck-portal-root",className:Kf("portal")})]})},$y=g.createContext({});function _j(e){return f.jsx($y.Provider,{value:e,children:e.children})}var As=()=>g.useContext($y);function yj({children:e}){const{config:t,data:r,ui:n,onChange:o,permissions:i={},plugins:a,overrides:s,viewports:l=oi,iframe:c,dnd:d,initialHistory:u,metadata:p,dictionary:v,onAction:h,fieldTransforms:m,_experimentalFullScreenCanvas:y,_experimentalVirtualization:b}=As(),k=g.useMemo(()=>Ny(c),[c]),[x]=g.useState(()=>{var F,M,q;const W=D(D({},Sl.ui),n);let B={};Object.keys((r==null?void 0:r.root)||{}).length>0&&!((F=r==null?void 0:r.root)!=null&&F.props)&&console.warn("Warning: Defining props on `root` is deprecated. Please use `root.props`, or republish this page to migrate automatically.");const Z=((M=r==null?void 0:r.root)==null?void 0:M.props)||(r==null?void 0:r.root)||{},oe=D(D({},(q=t.root)==null?void 0:q.defaultProps),Z),K=Nc(ro(N(D({},r==null?void 0:r.root),{props:oe})),t),te=N(D({},Sl),{data:N(D({},r),{root:N(D({},r==null?void 0:r.root),{props:K.props}),content:r.content||[]}),ui:N(D(D({},W),B),{componentList:t.categories?Object.entries(t.categories).reduce((be,[Q,ie])=>N(D({},be),{[Q]:{title:ie.title,components:ie.components,expanded:ie.defaultExpanded,visible:ie.visible}}),{}):{}})});return mt(te,t)}),{appendData:_=!0}=u||{},[I]=g.useState([...(u==null?void 0:u.histories)||[],..._?[{state:x}]:[]].map(F=>{let M=D(D({},x),F.state);return F.state.indexes||(M=mt(M,t)),N(D({},F),{state:M})})),w=g.useMemo(()=>(u==null?void 0:u.index)!==void 0&&(u==null?void 0:u.index)>=0&&(u==null?void 0:u.index)<I.length?u==null?void 0:u.index:I.length-1,[]),A=I[w].state,E=UA({overrides:s,plugins:a}),C=g.useMemo(()=>{const M=(a||[]).reduce((q,W)=>D(D({},q),W.fieldTransforms),{});return D(D({},M),m)},[m,a]),S=Ps(),j=g.useCallback(F=>({instanceId:S,state:F,config:t,plugins:a||[],overrides:E,viewports:l,iframe:k,_experimentalFullScreenCanvas:!!y,_experimentalVirtualization:!!b,onAction:h,metadata:p,dictionary:v||{},dnd:d,fieldTransforms:C}),[S,A,t,a,E,l,k,y,b,h,p,v,d,C]),[O]=g.useState(()=>Av(j(A)));g.useEffect(()=>{},[O]),g.useEffect(()=>{const F=O.getState().state;O.setState(D({},j(F)))},[j]),vw(O,{histories:I,index:w,initialAppState:A});const L=g.useRef(null);g.useEffect(()=>O.subscribe(F=>F.state.data,F=>{if(o){if(ni(F,L.current))return;o(F),L.current=F}}),[o]),_w(O,i);const $=lz(O);return g.useEffect(()=>{const{resolveAndCommitData:F}=O.getState();setTimeout(()=>{F()},0)},[]),f.jsx(su.Provider,{value:O,children:f.jsx(sz.Provider,{value:$,children:e})})}function xo(e){return f.jsx(_j,N(D({},e),{children:f.jsx(yj,N(D({},e),{children:f.jsx(By,{children:e.children})}))}))}xo.Components=ly;xo.Fields=Od;xo.Layout=By;xo.Outline=wy;xo.Preview=Ty;z();z();z();z();z();z();z();z();z();z();z();z();z();z();const bj={components:{HeadingBlock:{label:"Heading",fields:{title:{type:"text"}},defaultProps:{title:"Heading"},render:({title:e})=>f.jsx("h2",{children:e})},TextBlock:{label:"Text",fields:{text:{type:"textarea"}},defaultProps:{text:"Text"},render:({text:e})=>f.jsx("p",{children:e})},ResourceLink:{label:"Resource link",fields:{resource:{type:"select",options:[{label:"Glossary",value:"glossary"},{label:"Products",value:"products"},{label:"Collections",value:"collections"},{label:"Blogs",value:"blogs"},{label:"Articles",value:"articles"},{label:"Locations",value:"locations"}]},label:{type:"text"}},defaultProps:{resource:"glossary",label:"Glossary"},render:({resource:e,label:t})=>f.jsx("a",{href:`#/${e}`,children:t||e})}}};function xj({initialLayout:e}){const[t,r]=g.useState(e!=null&&e.root?e:{root:{props:{}},content:(e==null?void 0:e.content)||[]}),n=g.useMemo(()=>o=>{r(o);const i=document.querySelector("#id_layout");i&&(i.value=JSON.stringify(o),i.dispatchEvent(new Event("input",{bubbles:!0})),i.dispatchEvent(new Event("change",{bubbles:!0})))},[]);return f.jsx("div",{style:{height:"70vh",border:"1px solid #ccc"},children:f.jsx(xo,{config:bj,data:t,onPublish:n})})}function Gf(){const e=document.getElementById("visual-editor-root");if(!e)return;let t={};try{t=JSON.parse(e.dataset.layoutJson||"{}")}catch{t={}}Hy.createRoot(e).render(f.jsx(xj,{initialLayout:t}))}document.readyState==="loading"?document.addEventListener("DOMContentLoaded",Gf):Gf();export{ou as A,Wv as E,E1 as H,d2 as L,wj as R,lu as S,N as _,H as a,D as b,$v as c,Re as d,Bw as e,Ww as f,ee as g,Vw as h,z as i,us as j,Lj as o,Qf as s,ye as u};
