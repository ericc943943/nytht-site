/* 紐約花蓮慈惠堂 網站共用程式：頁首頁尾、中英切換、字體放大、年度行事、今日農曆 */

/* ================= 堂的基本資料（改這裡，全站一起更新） ================= */
const TEMPLE = {
  nameZh: "紐約花蓮慈惠堂",
  nameEn: "New York Hua Lian Tsu Hui Temple",
  address: "22-02 121 Street, College Point, NY 11356",
  mapQuery: "22-02 121st St, College Point, NY 11356",
  phone: "(718) 961-1996",
  fax: "(718) 961-1992",
  email: "nyhltht@gmail.com",
  facebook: "https://www.facebook.com/%E7%B4%90%E7%B4%84%E8%8A%B1%E8%93%AE%E6%85%88%E6%83%A0%E5%A0%82-119659741440606/",
};

/* ================= 年度行事（農曆） =================
   m：農曆月；d：農曆日（沒有固定日期就不填，改填 approx）；key：重要節慶會加底色 */
const CALENDAR = [
  {m:1,  d:9,  lz:"農曆一月九日", s27:"2027/2/14（日）", zh:"玉皇上帝聖誕 (點太歲燈、光明燈)", en:"Birthday of the Jade Emperor (Tai Sui and Guangming lamps)"},
  {m:2,  lz:"農曆二月上旬", s27:"2027/3/8（一）～3/17（三）之間", approxEn:"Early 2nd month", zh:"春季祈安禮斗法會", en:"Spring Li Dou Blessing Ceremony", key:true},
  {m:2,  d:16, lz:"農曆二月十六日", s27:"2027/3/23（二）", zh:"花蓮晉香 (聖地之旅)", en:"Pilgrimage to Hualien (journey to the holy site)"},
  {m:2,  d:19, lz:"農曆二月十九日", s27:"2027/3/26（五）", zh:"觀世音菩薩聖誕", en:"Birthday of Guanyin Bodhisattva"},
  {m:3,  d:23, lz:"農曆三月二三日", s27:"2027/4/29（四）", zh:"天上聖母聖誕", en:"Birthday of Mazu"},
  {m:6,  d:3,  lz:"農曆六月三日", s27:"2027/7/6（二）", zh:"蟠桃聖會", en:"Peach Banquet Festival"},
  {m:6,  d:7,  lz:"農曆六月七日", s27:"2027/7/10（六）", zh:"開天門消災法會", en:"Opening of Heaven's Gate Ceremony"},
  {m:7,  d:18, lz:"農曆七月十八日", s27:"2027/8/19（四）", zh:"瑤池金母聖誕", en:"Birthday of the Golden Mother of the Jasper Pool", key:true},
  {m:7,  d:19, d2:20, lz:"農曆七月十九～二十日", s27:"2027/8/20（五）～8/21（六）", zh:"超渡法會", en:"Deliverance Ceremony", key:true},
  {m:9,  d:9,  lz:"農曆九月九日", s27:"2027/10/8（五）", zh:"斗姆元君聖誕", en:"Birthday of Doumu Yuanjun"},
  {m:9,  d:9,  lz:"農曆九月九日", s27:"2027/10/8（五）", zh:"中壇元帥聖誕", en:"Birthday of Marshal Zhongtan"},
  {m:9,  lz:"農曆九月", s27:"2027/9/30（四）～10/28（四）之間", approxEn:"9th month", zh:"秋季祈安禮斗法會", en:"Autumn Li Dou Blessing Ceremony", key:true},
  {m:10, d:18, lz:"農曆十月十八日", s27:"2027/11/15（一）", zh:"地母娘娘聖誕", en:"Birthday of the Earth Mother"},
  {m:11, d:11, lz:"農曆十一月十一日", s27:"2027/12/8（三）", zh:"太乙救苦天尊聖誕", en:"Birthday of Taiyi Jiuku Tianzun"},
  {m:12, lz:"農曆十二月下旬", s27:"2028/1/17（一）～1/25（二）之間", approxEn:"Late 12th month", zh:"謝太歲、光明燈、謝平安法會", en:"Year-end thanksgiving ceremony for Tai Sui and lamps"},
];

/* ================= 共用小工具 ================= */
const LMONTH = ["正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"];
const LDAY = (()=>{const a=[],n="一二三四五六七八九十";for(let d=1;d<=30;d++){a.push(d<=10?"初"+n[d-1]:d<20?"十"+n[d-11]:d===20?"二十":d<30?"廿"+n[d-21]:"三十")}return a})();
const ORD = n => n+(["th","st","nd","rd"][(n%100-20)%10]||["th","st","nd","rd"][n%100]||"th");
const isEn = () => document.documentElement.lang==="en";
const hasLunar = () => typeof window.Solar!=="undefined";
function lunarLabel(e){
  if(!isEn()) return e.lz;
  if(!e.d) return e.approxEn;
  if(isEn()) return `${ORD(e.m)} month, day ${e.d}${e.d2?"–"+e.d2:""}`;
  return `${LMONTH[e.m-1]}${LDAY[e.d-1]}${e.d2?"至"+LDAY[e.d2-1]:""}`;
}
// 換算國曆：今年農曆的日期已過，就顯示明年的
function solarOf(e, from=new Date()){
  if(!e.d || !hasLunar()) return null;
  const todayL = Solar.fromDate(from).getLunar();
  for(const y of [todayL.getYear(), todayL.getYear()+1]){
    try{ const s=Lunar.fromYmd(y,e.m,e.d).getSolar(); const dt=new Date(s.getYear(),s.getMonth()-1,s.getDay());
         const end=new Date(dt); if(e.d2) end.setDate(end.getDate()+(e.d2-e.d));
         if(end >= new Date(from.getFullYear(),from.getMonth(),from.getDate())) return dt; }catch(err){}
  }
  return null;
}
function fmtSolar(dt){
  if(!dt) return "";
  const w = isEn() ? ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"][dt.getDay()] : "日一二三四五六"[dt.getDay()];
  return isEn() ? `${dt.toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric"})} (${w})`
                : `${dt.getFullYear()}/${dt.getMonth()+1}/${dt.getDate()}（${w}）`;
}

/* ================= 頁首與頁尾 ================= */
/* ================= 選單：照舊網站 ================= */
const NAV = [
  ["index.html", "首頁", "Home"],
  [null, "本堂簡介", "About", [
    ["history.html", "紐約花蓮慈惠堂由來", "Our History"],
    ["milestones.html", "大事記", "Milestones"],
    ["master.html", "堂主簡介", "Head of the Temple"],
  ]],
  [null, "供奉神明", "Deities", [
    ["deity.html", "主神簡介", "Principal Deity"],
    ["halls.html", "本堂設施", "Facilities"],
  ]],
  [null, "點燈法會", "Lamps & Ceremonies", [
    ["lamps.html", "點燈祈福", "Lamp Lighting"],
    ["calendar.html", "年度行事", "Annual Calendar"],
  ]],
  [null, "本堂訊息", "Temple News", [
    ["news.html", "最新活動", "Latest Events"],
    ["gallery.html", "活動剪影", "Gallery"],
    ["articles.html", "近期文章", "Recent Articles"],
  ]],
  [null, "聯繫本堂", "Contact Us", [
    ["contact.html", "聯絡資訊", "Contact & Directions"],
    ["faq.html", "常見問題", "FAQ"],
  ]],
];

const L = (zh,en) => `<span class="zh">${zh}</span><span class="en">${en}</span>`;
function pageFile(){ const p=location.pathname.split("/").pop(); return p===""?"index.html":(p.endsWith(".html")?p:p+".html"); }

function header(){
  const cur=pageFile();
  const item = ([h,zh,en,kids]) => {
    if(!kids) return `<a href="${h}"${h===cur?' aria-current="page"':""}>${L(zh,en)}</a>`;
    const on = kids.some(k=>k[0]===cur);
    return `<div class="dd${on?" on":""}"><button type="button" class="ddbtn" aria-expanded="false">${L(zh,en)}<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
      <div class="ddmenu">${kids.map(([h2,z2,e2])=>`<a href="${h2}"${h2===cur?' aria-current="page"':""}>${L(z2,e2)}</a>`).join("")}</div></div>`;
  };
  return `<div class="container gutter">
    <a class="brand" href="index.html" aria-label="${TEMPLE.nameZh}"><img src="assets/logo.jpg" alt="${TEMPLE.nameZh} ${TEMPLE.nameEn}" width="176" height="40"></a>
    <nav class="nav" id="nav" aria-label="主選單">${NAV.map(item).join("")}<a class="navcta" href="https://nytht.vercel.app/">${L("線上點燈和法會報名","Lamp & Ceremony Registration")}</a></nav>
    <div class="tools">
      <button class="chipbtn" id="langBtn" type="button" aria-label="切換語言 Switch language">${L("English","繁體中文")}</button>
      <button class="chipbtn" id="sizeBtn" type="button">${L("字放大","A+")}</button>
      <a class="cta" href="https://nytht.vercel.app/">${L("線上點燈和法會報名","Lamp & Ceremony Registration")}</a>
      <button class="menubtn" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav" aria-label="選單 Menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div></div>`;
}
function footer(){
  return `<div class="container gutter">
    <div><h4>${L(TEMPLE.nameZh, TEMPLE.nameEn)}</h4>
      <p>${TEMPLE.address}</p>
      <p>${L("參拜時間","Hours")} <span class="nowrap">${L("每日上午 9 點至下午 4 點","Daily, 9:00 am – 4:00 pm")}</span></p>
      <p>${L("電話","Tel")} <span class="nowrap">${TEMPLE.phone}</span></p>
      <p>${L("傳真","Fax")} <span class="nowrap">${TEMPLE.fax}</span></p>
      <p>Email: ${TEMPLE.email}</p>
      <p><a href="${TEMPLE.facebook}" target="_blank" rel="noopener">Facebook</a></p></div>
    ${NAV.filter(n=>n[3]).map(([,z,e,kids])=>`<div><h4>${L(z,e)}</h4><ul>${kids.map(([h,z2,e2])=>`<li><a href="${h}">${L(z2,e2)}</a></li>`).join("")}</ul></div>`).join("")}
    <p class="copy">Copyright © ${TEMPLE.nameZh} ${L("版權所有","All rights reserved")}</p>
  </div>`;
}

/* ================= 語言與字體 ================= */
function store(k,v){ try{ v===undefined ? localStorage.removeItem(k) : localStorage.setItem(k,v); }catch(e){} }
function read(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
function setLang(l){ document.documentElement.lang = l==="en" ? "en" : "zh-Hant"; store("tsuhui-lang", l); document.dispatchEvent(new Event("langchange")); }
function setBig(on){ document.documentElement.classList.toggle("big",on); store("tsuhui-big", on?"1":""); }

/* ================= 圖片：檔案不存在就顯示設計過的底 ================= */
function wireImages(){
  document.querySelectorAll("figure.ph img").forEach(img=>{
    const fail=()=>img.closest("figure").classList.add("noimg");
    const probe=new Image(); probe.onerror=fail; probe.src=img.getAttribute("src");
  });
}

/* ================= 今日農曆、近期行事、年度行事表 ================= */
function renderToday(){
  const el=document.getElementById("today"); if(!el || !hasLunar()) return;
  const l=Solar.fromDate(new Date()).getLunar();
  el.innerHTML = isEn()
    ? `<span>Today on the lunar calendar: <b>${ORD(Math.abs(l.getMonth()))} month, day ${l.getDay()}</b></span>`
    : `<span>今日農曆 <b>${l.getYearInGanZhi()}年 ${l.getMonth()<0?"閏":""}${LMONTH[Math.abs(l.getMonth())-1]}${LDAY[l.getDay()-1]}</b></span>`;
}
function renderUpcoming(){
  const el=document.getElementById("upcoming"); if(!el) return;
  const items = CALENDAR.map(e=>({e,dt:solarOf(e)})).filter(x=>x.dt).sort((a,b)=>a.dt-b.dt).slice(0, +el.dataset.count||4);
  el.innerHTML = items.length ? items.map(({e,dt})=>`<li><div class="when">${isEn()?dt.toLocaleDateString("en-US",{month:"short",day:"numeric"}):`${dt.getMonth()+1}/${dt.getDate()}`}<small>${lunarLabel(e)}</small></div>
      <div class="what"><b>${isEn()?e.en:e.zh}</b>${(isEn()?e.noteEn:e.noteZh)?`<span>${isEn()?e.noteEn:e.noteZh}</span>`:""}</div></li>`).join("")
    : `<li><div class="what"><span>${isEn()?"See the full calendar.":"請見年度行事。"}</span></div></li>`;
}
function renderCalendar(){
  const el=document.getElementById("calBody"); if(!el) return;
  el.innerHTML = CALENDAR.map(e=>{ const dt=solarOf(e);
    return `<tr class="${e.key?"key":""}"><td class="lunar">${lunarLabel(e)}</td>
      <td class="ev"><b>${isEn()?e.en:e.zh}</b>${(isEn()?e.noteEn:e.noteZh)?`<span>${isEn()?e.noteEn:e.noteZh}</span>`:""}</td>
      <td class="solar">${e.s27||""}</td></tr>`; }).join("");
}


/* ================= 值年太歲：依農曆年自動判斷，過年自動換 ================= */
const TAISUI = ["甲子太歲金辦將軍", "甲申太歲方杰將軍", "甲辰太歲李誠將軍", "乙丑太歲陳材將軍", "乙酉太歲蔣崇將軍", "乙巳太歲吳遂將軍", "丙寅太歲耿章將軍", "丙戌太歲白敏將軍", "丙午太歲文哲將軍", "丁卯太歲沈興將軍", "丁亥太歲封濟將軍", "丁未太歲繆丙將軍", "戊辰太歲趙達將軍", "戊子太歲鄒鏜將軍", "戊申太歲徐浩將軍", "己巳太歲郭燦將軍", "己丑太歲潘佐將軍", "己酉太歲程寶將軍", "庚午太歲王清將軍", "庚寅太歲鄔桓將軍", "庚戌太歲倪秘將軍", "辛未太歲李素將軍", "辛卯太歲范寧將軍", "辛亥太歲葉堅將軍", "壬申太歲劉旺將軍", "壬辰太歲彭泰將軍", "壬子太歲丘德將軍", "癸酉太歲康志將軍", "癸巳太歲徐華將軍", "癸丑太歲朱得將軍", "甲戌太歲施廣將軍", "甲午太歲章詞將軍", "甲寅太歲張朝將軍", "乙亥太歲任保將軍", "乙未太歲楊仙將軍", "乙卯太歲萬清將軍", "丙子太歲郭嘉將軍", "丙申太歲管仲將軍", "丙辰太歲辛亞將軍", "丁丑太歲汪文將軍", "丁酉太歲唐傑將軍", "丁巳太歲楊彥將軍", "戊寅太歲曾光將軍", "戊戌太歲姜武將軍", "戊午太歲黎卿將軍", "己卯太歲龍仲將軍", "己亥太歲謝燾將軍", "己未太歲傅黨將軍", "庚辰太歲董德將軍", "庚子太歲虞起將軍", "庚申太歲毛梓將軍", "辛巳太歲鄭但將軍", "辛丑太歲楊信將軍", "辛酉太歲石政將軍", "壬午太歲陸明將軍", "壬寅太歲賢諤將軍", "壬戌太歲洪充將軍", "癸未太歲魏仁將軍", "癸卯太歲皮時將軍", "癸亥太歲虞程將軍"];
const GAN="甲乙丙丁戊己庚辛壬癸", ZHI="子丑寅卯辰巳午未申酉戌亥";
const CNY_FALLBACK = {2025:[1,29],2026:[2,17],2027:[2,6],2028:[1,26],2029:[2,13],2030:[2,3],2031:[1,23],2032:[2,11],2033:[1,31],2034:[2,19],2035:[2,8],2036:[1,28],2037:[2,15],2038:[2,4],2039:[1,24],2040:[2,12]};
function cnyOf(y){
  if(typeof window.Lunar!=="undefined"){ try{ const s=Lunar.fromYmd(y,1,1).getSolar(); return new Date(s.getYear(),s.getMonth()-1,s.getDay()); }catch(e){} }
  const c=CNY_FALLBACK[y]; return c ? new Date(y,c[0]-1,c[1]) : null;
}
function taisuiOf(d=new Date()){
  const day=new Date(d.getFullYear(),d.getMonth(),d.getDate());
  let y=day.getFullYear(), start=cnyOf(y); if(!start) return null;
  if(day<start){ y--; start=cnyOf(y); }
  const next=cnyOf(y+1); if(!start||!next) return null;
  const end=new Date(next); end.setDate(end.getDate()-1);
  const i=((y-4)%60+60)%60, gz=GAN[i%10]+ZHI[i%12];
  const full=TAISUI.find(n=>n.startsWith(gz)); if(!full) return null;
  return {gz, full, name:full.replace(gz+"太歲",""), start, end};
}
function renderTaisui(){
  const t=taisuiOf(); if(!t) return;
  const f=d=>`${d.getFullYear()}/${d.getMonth()+1}/${d.getDate()}`, fe=d=>d.toLocaleDateString("en-US",{year:"numeric",month:"short",day:"numeric"});
  const today=document.getElementById("taisuiToday");
  if(today) today.innerHTML = `<span>${L(`${t.gz}年值年太歲 <b>${t.name}</b>`, `Tai Sui of the year: <b>${t.name}</b>`)}</span>`;
  const box=document.getElementById("taisuiNow");
  if(box){
    document.getElementById("tsYear").innerHTML=L(t.gz+"年　", t.gz+" year · ");
    document.getElementById("tsName").textContent=t.name;
    document.getElementById("tsRange").innerHTML=L(`國曆 ${f(t.start)} 至 ${f(t.end)}`, `${fe(t.start)} – ${fe(t.end)}`);
    box.hidden=false;
    document.querySelectorAll(".taisui-all td.now").forEach(x=>x.classList.remove("now"));
    document.querySelector(`.taisui-all td[data-gz="${t.gz}"]`)?.classList.add("now");
  }
}
function bottomBar(){
  const bar=document.createElement("div"); bar.className="bottombar";
  const map="https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(TEMPLE.mapQuery);
  bar.innerHTML=`<a href="tel:${TEMPLE.phone.replace(/[^0-9]/g,"")}">${L("打電話","Call")}</a><a href="${map}" target="_blank" rel="noopener">${L("導航","Directions")}</a><a class="go" href="https://nytht.vercel.app/">${L("報名","Register")}</a>`;
  document.body.appendChild(bar);
}

/* ================= 啟動 ================= */
(function(){
  const q=new URLSearchParams(location.search).get("lang");
  const saved=read("tsuhui-lang");
  if(q==="en"||(!q&&saved==="en")) document.documentElement.lang="en";
  if(read("tsuhui-big")) document.documentElement.classList.add("big");
})();
document.addEventListener("DOMContentLoaded", ()=>{
  const h=document.querySelector(".site-header"); if(h) h.innerHTML=header();
  const f=document.querySelector(".site-footer"); if(f) f.innerHTML=footer();
  document.getElementById("langBtn")?.addEventListener("click", ()=>setLang(isEn()?"zh":"en"));
  document.getElementById("sizeBtn")?.addEventListener("click", ()=>setBig(!document.documentElement.classList.contains("big")));
  const mb=document.getElementById("menuBtn");
  mb?.addEventListener("click", ()=>{ const n=document.getElementById("nav"); const o=n.classList.toggle("open"); mb.setAttribute("aria-expanded",o); });
  document.querySelectorAll(".ddbtn").forEach(b=>b.addEventListener("click", e=>{
    const dd=b.parentElement; const open=!dd.classList.contains("open");
    document.querySelectorAll(".dd.open").forEach(x=>{ x.classList.remove("open"); x.querySelector(".ddbtn").setAttribute("aria-expanded","false"); });
    if(open){ dd.classList.add("open"); b.setAttribute("aria-expanded","true"); }
    e.stopPropagation();
  }));
  document.addEventListener("click", ()=>document.querySelectorAll(".dd.open").forEach(x=>x.classList.remove("open")));
  document.querySelectorAll("[data-tel]").forEach(e=>e.textContent=TEMPLE.phone);
  document.querySelectorAll("[data-fax]").forEach(e=>e.textContent=TEMPLE.fax);
  document.querySelectorAll("[data-email]").forEach(e=>e.textContent=TEMPLE.email);
  document.querySelectorAll("[data-address]").forEach(e=>e.textContent=TEMPLE.address);
  document.querySelectorAll("[data-fb]").forEach(e=>e.href=TEMPLE.facebook);
  document.querySelectorAll(".fp-routebtn").forEach(b=>b.addEventListener("click",()=>{
    const w=b.closest(".fp-wrap"); const on=w.classList.toggle("nums"); b.setAttribute("aria-pressed", on);
  }));
  wireImages(); renderToday(); renderUpcoming(); renderCalendar(); renderTaisui(); bottomBar();
});
document.addEventListener("langchange", ()=>{ renderToday(); renderUpcoming(); renderCalendar(); });
