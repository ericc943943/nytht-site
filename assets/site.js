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
  {m:1,  d:9,  lz:"農曆正月初九", s27:"2027/2/14（日）", zh:"玉皇上帝聖誕 (點太歲燈、光明燈)", en:"Birthday of the Jade Emperor (Tai Sui and Guangming lamps)"},
  {m:2,  lz:"農曆二月上旬", s27:"2027/3/8（一）～3/17（三）之間", approxEn:"Early 2nd month", zh:"春季祈安禮斗法會", en:"Spring Li Dou Blessing Ceremony", key:true},
  {m:2,  d:16, lz:"農曆二月十六日", s27:"2027/3/23（二）", zh:"花蓮晉香 (聖地之旅)", en:"Pilgrimage to Hualien (journey to the holy site)"},
  {m:2,  d:19, lz:"農曆二月十九日", s27:"2027/3/26（五）", zh:"觀世音菩薩聖誕", en:"Birthday of Guanyin Bodhisattva"},
  {m:3,  d:23, lz:"農曆三月二十三日", s27:"2027/4/29（四）", zh:"天上聖母聖誕", en:"Birthday of Mazu"},
  {m:6,  d:3,  lz:"農曆六月初三", s27:"2027/7/6（二）", zh:"蟠桃聖會", en:"Peach Banquet Festival"},
  {m:6,  d:7,  lz:"農曆六月初七", s27:"2027/7/10（六）", zh:"開天門消災法會", en:"Opening of Heaven's Gate Ceremony"},
  {m:7,  d:18, lz:"農曆七月十八日", s27:"2027/8/19（四）", zh:"瑤池金母聖誕", en:"Birthday of the Golden Mother of the Jasper Pool", key:true},
  {m:7,  d:19, d2:20, lz:"農曆七月十九～二十日", s27:"2027/8/20（五）～8/21（六）", zh:"超渡法會", en:"Deliverance Ceremony", key:true},
  {m:9,  d:9,  lz:"農曆九月初九", s27:"2027/10/8（五）", zh:"斗姆元君聖誕", en:"Birthday of Doumu Yuanjun"},
  {m:9,  d:9,  lz:"農曆九月初九", s27:"2027/10/8（五）", zh:"中壇元帥聖誕", en:"Birthday of Marshal Zhongtan"},
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
const TAISUI = ["甲子太歲·金辨大將軍", "甲申太歲·方傑大將軍", "甲辰太歲·李誠大將軍", "乙丑太歲·陳材大將軍", "乙酉太歲·蔣崇大將軍", "乙巳太歲·吳遂大將軍", "丙寅太歲·耿章大將軍", "丙戌太歲·白敏大將軍", "丙午太歲·文哲大將軍", "丁卯太歲·沈興大將軍", "丁亥太歲·封濟大將軍", "丁未太歲·繆丙大將軍", "戊辰太歲·趙達大將軍", "戊子太歲·鄒鏜大將軍", "戊申太歲·徐浩大將軍", "己巳太歲·郭燦大將軍", "己丑太歲·潘佐大將軍", "己酉太歲·程寶大將軍", "庚午太歲·王清大將軍", "庚寅太歲·鄔桓大將軍", "庚戌太歲·倪秘大將軍", "辛未太歲·李素大將軍", "辛卯太歲·范寧大將軍", "辛亥太歲·葉堅大將軍", "壬申太歲·劉旺大將軍", "壬辰太歲·彭泰大將軍", "壬子太歲·丘德大將軍", "癸酉太歲·康志大將軍", "癸巳太歲·徐華大將軍", "癸丑太歲·朱得大將軍", "甲戌太歲·施廣大將軍", "甲午太歲·章詞大將軍", "甲寅太歲·張朝大將軍", "乙亥太歲·任保大將軍", "乙未太歲·楊仙大將軍", "乙卯太歲·萬清大將軍", "丙子太歲·郭嘉大將軍", "丙申太歲·管仲大將軍", "丙辰太歲·辛亞大將軍", "丁丑太歲·汪文大將軍", "丁酉太歲·唐傑大將軍", "丁巳太歲·楊彥大將軍", "戊寅太歲·曾光大將軍", "戊戌太歲·姜武大將軍", "戊午太歲·黎卿大將軍", "己卯太歲·龍仲大將軍", "己亥太歲·謝燾大將軍", "己未太歲·傅黨大將軍", "庚辰太歲·董德大將軍", "庚子太歲·虞起大將軍", "庚申太歲·毛梓大將軍", "辛巳太歲·鄭但大將軍", "辛丑太歲·楊信大將軍", "辛酉太歲·石政大將軍", "壬午太歲·陸明大將軍", "壬寅太歲·賢諤大將軍", "壬戌太歲·洪充大將軍", "癸未太歲·魏仁大將軍", "癸卯太歲·皮時大將軍", "癸亥太歲·虞程大將軍"];
/* 六十太歲簡介：資料來源 _dev/build/taisui_bio.py（改那邊再貼過來）；據民間流傳之《六十甲子太歲傳略》 */
const TAISUI_BIO = {"甲子": ["據傳為明代山陽人金濂，字宗瀚。任僉都御史參贊寧夏軍務，疏浚水渠，灌溉千餘頃農田，並奏請表揚捐糧賑災的百姓。", "Said to be Jin Lian of the Ming dynasty, who restored irrigation canals in Ningxia and championed famine relief."], "乙丑": ["據傳為明代金華人陳材，字俊卿。力大過人，曾徒手打死猛虎；會試考場失火時，讓同場考生踩著自己的肩膀逃生，救出數十人。後任安丘知縣。", "Said to be Chen Cai of the Ming dynasty, famed for his strength: he killed a tiger barehanded and saved dozens of candidates from an examination-hall fire."], "丙寅": ["據傳為明代人耿章光，山西巡撫耿如杞之子。父親蒙冤入獄，他入獄侍奉；父親遇害後刺血上書為父申冤，震動朝廷。", "Said to be Geng Zhangguang of the Ming dynasty, who wrote a petition in his own blood to clear his father's name."], "丁卯": ["據傳為明代建寧人沈興。足智多謀、光明磊落，洪武年間任建寧衛百戶，築城設防、抵禦盜寇，百姓得以安居。", "Said to be Shen Xing, a Ming officer in Jianning who built walls and defenses so the people could live in peace."], "戊辰": ["據傳為三國時河南人趙達。精通九宮算術，推算如神，曾為東吳孫權占算吉凶。", "Said to be Zhao Da of the Three Kingdoms era, a master of calculation and divination who served Sun Quan of Wu."], "己巳": ["據傳為明代安陽人郭燦。中舉後任知縣，曾夜出奇兵大破亂賊；事親至孝，施政寬和而守法。", "Said to be Guo Can, a Ming magistrate known for defeating bandits, his devotion to his parents, and gentle, lawful rule."], "庚午": ["據傳為宋代深州饒陽人王濟。父親遇盜身亡，他護送父親遺骨脫險，後奉雙親歸葬故鄉；為官剛直敢言，曾在洪州賑濟饑民。", "Said to be Wang Ji of the Song dynasty, a devoted son and outspoken official who fed the hungry in Hongzhou."], "辛未": ["據傳為唐代隴西人李素，字貞一。幼年喪父，由母親教養成才；任蘇州等地官員時抵抗叛軍，並為百姓減免賦稅。", "Said to be Li Su of the Tang dynasty, raised by his widowed mother, who resisted rebels and lightened taxes for the people."], "壬申": ["據傳為明代人劉旺，戍守邊關。與兒子設伏抗敵，援兵斷絕、箭矢用盡，父子一同殉國。", "Said to be Liu Wang, a Ming border officer who died in battle alongside his son."], "癸酉": ["據傳為唐代靈州人康志睦，字得眾。屢立戰功，官至節度使、受封郡公，一家三代皆為朝廷功臣。", "Said to be Kang Zhimu of the Tang dynasty, a decorated general from a family of loyal servants of the court."], "甲戌": ["據傳為明代桂平人施廣。年輕時拾金不昧，歸還失主；成化年間中舉任教職，做官後仍捐出俸祿助人。", "Said to be Shi Guang of the Ming dynasty, who returned lost gold to its owner and gave his salary to those in need."], "乙亥": ["據傳為明代福建建寧府人任保。進士出身，任府同知時抗擊倭寇，身負重傷仍督戰，終於擊退敵軍。", "Said to be Ren Bao of the Ming dynasty, who fought on despite severe wounds to drive off Japanese pirates."], "丙子": ["據傳為元代濮陽人郭嘉，字元禮（並非三國時的郭嘉）。任廣寧路總管，遼東動亂時孤城死守、拒絕招降，壯烈殉職。", "Said to be Guo Jia of the Yuan dynasty (not the Three Kingdoms strategist), who defended his city to the death."], "丁丑": ["據傳為宋代婺源人汪文，字質甫。寶慶年間進士，善用謀略剿平盜匪；軍糧短缺時設法籌糧，穩定軍心。", "Said to be Wang Wen of the Song dynasty, who used clever strategy to suppress bandits and keep his troops supplied."], "戊寅": ["據傳為明代西大通人魯鑒。歷任都指揮、總兵，驍勇善戰，多次中箭仍不退縮，身後追贈右都督。", "Said to be Lu Jian, a fearless Ming general who fought on through many arrow wounds."], "己卯": ["據傳為宋代永新人龍崇。好學著述，建議修築永新城保護百姓，並參與編修史書，被尊為「忠勤先生」。", "Said to be Long Chong of the Song dynasty, a scholar who urged building city walls to protect the people of Yongxin."], "庚辰": ["據傳為宋代樂安人董德修，字仲修。屢試不第便隱居讀書，樂善好施；曾拜陸九淵為師，以學問品行聞名。", "Said to be Dong Dexiu of the Song dynasty, a generous scholar and disciple of the philosopher Lu Jiuyuan."], "辛巳": ["據傳為明代歙縣人鄭旦，字希周。嘉靖年間進士，官至浙江右布政使，以詩文聞名，為官清廉。", "Said to be Zheng Dan of the Ming dynasty, an upright official and noted poet."], "壬午": ["據傳為明代銅陵人陸明。好學，以舉人身分任官，善於調解兄弟爭產；主持工程有方，百姓不覺勞苦。", "Said to be Lu Ming of the Ming dynasty, a fair-minded official who settled family disputes and ran public works without burdening the people."], "癸未": ["據傳為明代華州人魏仁，字子行。永樂年間進士；老師遭誣下獄，他冒死上書陳情，終使師長冤屈得雪。", "Said to be Wei Ren of the Ming dynasty, who risked his life petitioning the emperor to free his wrongly imprisoned teacher."], "甲申": ["據傳為宋代福建人方傑。任同安知縣，寬緩催稅、平反冤案、修築堤防，百姓題「三善」匾頌揚。", "Said to be Fang Jie of the Song dynasty, a magistrate praised for lenient taxes, righting injustices and building dikes."], "乙酉": ["據傳為元代東陽人蔣尚。為人謹厚謙和，自己生活清苦，仍樂於濟困扶危，過世時鄉人無不哀悼。", "Said to be Jiang Shang of the Yuan dynasty, a humble man who helped the poor despite his own hardship."], "丙戌": ["據傳為明代閩人白叔敏。洪武年間任潮州知府，興辦學校、勸課農桑，為官清廉，並奏請免除苛稅。", "Said to be Bai Shumin of the Ming dynasty, a prefect who built schools, encouraged farming and abolished harsh taxes."], "丁亥": ["據傳為明代湖廣人封益。洪武年間任岳州知府，招撫盜眾、設義倉以備荒年，後升任戶部侍郎。", "Said to be Feng Yi of the Ming dynasty, who won over bandits and set up granaries against famine."], "戊子": ["據傳為明代蕪湖人鄒銳。永樂初年任官，處事審慎、不畏權勢，為官清廉，晚年清貧，八十多歲辭世。", "Said to be Zou Rui of the Ming dynasty, an honest official who feared no one in power and died poor."], "己丑": ["據傳為宋代考城人傅求。天聖年間進士，整治吏員舞弊、平定播州之亂、改善賦稅，官至龍圖閣學士。", "Said to be Fu Qiu of the Song dynasty, who curbed corruption, quelled unrest and reformed taxes."], "庚寅": ["據傳為明代新昌人鄔璚。任溧陽縣丞，除強扶弱、均平賦役，任滿時百姓請求留任，後升任知縣，殉職任上。", "Said to be Wu Qiong of the Ming dynasty, a magistrate so beloved that the people begged him to stay."], "辛卯": ["據傳為東晉南陽人范寧，字武子。任餘杭令時興辦學校，任豫章太守時廣設學舍、推廣經學，使當地重視教育。", "Said to be Fan Ning of the Eastern Jin, who founded schools and spread classical learning."], "壬辰": ["據傳為明代鳳翔人彭泰。洪武年間進士，任侍講，剛正淡泊、勤於政務；未中第時訂下的婚約，不因女方家貧貌陋而反悔。", "Said to be Peng Tai of the Ming dynasty, an upright scholar who kept his humble betrothal promise after rising in office."], "癸巳": ["據傳為東漢平陵人徐幹。自請赴西域協助班超，屢立戰功，協助大破烏孫，使西域五十餘國歸附。", "Said to be Xu Gan of the Han dynasty, who joined Ban Chao in the Western Regions and helped bring some fifty states into alliance."], "甲午": ["據傳為明代涇縣人章文粹。任福寧州訓導，勸民耕種；倭寇逼近時開城收容難民，病逝任上，士民遠道送行。", "Said to be Zhang Wencui of the Ming dynasty, a teacher-official who opened the city gates to refugees fleeing pirates."], "乙未": ["據傳為宋代淄齊人楊仙。好修仙道、淡泊名利，隱居山中；後假死離去，墓中只剩空棺，鄉人為他建塔紀念。", "Said to be Yang Xian of the Song dynasty, a hermit devoted to the Dao who left behind only an empty coffin."], "丙申": ["據傳為春秋時齊國人管仲（管夷吾）。與鮑叔牙相知相惜，輔佐齊桓公改革內政、尊王攘夷、九合諸侯，成就霸業。", "Said to be Guan Zhong of the Spring and Autumn period, the statesman who made Duke Huan of Qi the leading power of his age."], "丁酉": ["據傳為唐代安鄉人唐傑，字子文。年少習武、力大過人，考中武舉，南征討賊立下戰功。", "Said to be Tang Jie of the Tang dynasty, a strong martial graduate who won merit in southern campaigns."], "戊戌": ["據傳為明代保德州人姜武。天啟年間武進士，崇禎年間守邊屢破盜寇；馳援開封時力戰被俘，壯烈殉節。", "Said to be Jiang Wu of the Ming dynasty, a border general who died a martyr in the relief of Kaifeng."], "己亥": ["據傳為明代臨晉人謝廷輔。拾得大筆遺金，設法歸還失主，對方酬謝也堅辭不受；後代子孫有人官至翰林。", "Said to be Xie Tingfu of the Ming dynasty, who returned a large sum of lost gold and refused any reward."], "庚子": ["據傳為明代崑山人盧熙，字公暨。任睢州同知，體恤百姓、拒絕強徵勞役，不向權貴妥協；病逝任上，吏民哭送。", "Said to be Lu Xi of the Ming dynasty, a caring official who refused to overburden the people with forced labor."], "辛丑": ["據傳為漢代人楊信。出使匈奴，堅守使命、不卑不亢，據理與單于議和，最終平安歸國。", "Said to be Yang Xin of the Han dynasty, an envoy to the Xiongnu who held firm to his mission."], "壬寅": ["據傳為元代鄠縣人賀賁。戰亂後收葬遺骸、協助供應軍需，並捐銀五千兩助軍，身後追封雍國公。", "Said to be He Ben of the Yuan dynasty, who buried the war dead and gave his wealth to support the army."], "癸卯": ["據傳為北魏漁陽人皮喜，名將皮豹子之子。平定吐谷渾的侵擾，後任豫州刺史。", "Said to be Pi Xi of the Northern Wei, son of a famous general, who repelled the Tuyuhun."], "甲辰": ["據傳為元代渭南人李誠，字克誠。任三原知縣，為政寬和，勸農興學、賦役公平，盜賊因此畏服。", "Said to be Li Cheng of the Yuan dynasty, a gentle magistrate who promoted farming and schools."], "乙巳": ["據傳為宋代人吳遂，字至道。任休寧知縣時善於破案；遇大旱為民祈雨、減租救饑、安置流民，縣境太平。", "Said to be Wu Sui of the Song dynasty, a magistrate who prayed for rain and fed the hungry during a drought."], "丙午": ["據傳為明代東莞人王縝，字文哲。弘治年間進士，任兵科給事中，剛直敢言；曾奉命出使安南，拒收饋贈。晚年任南京戶部尚書，為饑民爭取賑濟，卒於任上。", "Said to be Wang Zhen (courtesy name Wenzhe) of the Ming dynasty, an outspoken official who refused gifts as envoy to Annam and died in office as Nanjing Minister of Revenue."], "丁未": ["據傳為宋代汴京人繆鑒，字君寶。孝順父母、友愛兄弟，樂於助人而無意做官；靖康之亂後避居江陰，耕讀自得，著有《效鼙集》。", "Said to be Miao Jian of the Song dynasty, a filial and generous scholar who chose farming and books over office."], "戊申": ["據傳為唐代越州人徐浩，字季海，以書法著稱，曾參與起草朝廷詔令；後遭讒言貶官，晚年任彭王傅。", "Said to be Xu Hao of the Tang dynasty, a celebrated calligrapher who drafted imperial edicts."], "己酉": ["據傳為五代南漢人程寶。忠勇不屈，奉命救援交州未及，後在征討楊廷藝時戰死沙場。", "Said to be Cheng Bao of the Southern Han, a loyal commander who fell in battle."], "庚戌": ["據傳為宋代羅源人倪翼。家境富裕卻生活簡樸；任潮州司法官時單騎安撫邊民，並為死囚據理力爭。", "Said to be Ni Yi of the Song dynasty, a frugal judge who rode alone to calm unrest and argued for condemned prisoners."], "辛亥": ["據傳為明代閩縣人葉堅。身材魁偉、武藝超群，考中武舉；築城保民，抵禦並招撫山寇。", "Said to be Ye Jian of the Ming dynasty, a martial graduate who built walls and won over mountain bandits."], "壬子": ["據傳為宋代人丘德。隨洪皓出使金國，拒絕誘降，被流放冷山十五年，歷盡艱苦，終於獲釋歸國。", "Said to be Qiu De of the Song dynasty, who refused to defect and endured fifteen years of exile in the Jin state."], "癸丑": ["據傳為明代靈璧人朱得。洪武初年隨軍南征北戰，累積戰功升官，後調福州剿平倭寇。", "Said to be Zhu De, an early Ming officer who later fought pirates in Fuzhou."], "甲寅": ["據傳為明代如皋人張朝。洪武初年任黃平所千戶，練兵有方、善察敵情，治軍嚴明，境內安定。", "Said to be Zhang Chao, an early Ming commander known for strict discipline and keeping the peace."], "乙卯": ["據傳為元代建昌南城人萬清，字仕廉。進士出身，官至樞密院使；亂世棄官歸鄉，明初屢受徵召皆不就。", "Said to be Wan Qing of the Yuan dynasty, a high official who went home in troubled times and declined later summons."], "丙辰": ["據傳為隋代狄道人辛公義。任岷州刺史，當地因怕疫病而遺棄病人，他親自照顧施藥，病者多痊癒，百姓尊為「慈母」。", "Said to be Xin Gongyi of the Sui dynasty, who personally nursed the sick during an epidemic and was called the people's \"loving mother.\""], "丁巳": ["據傳為宋代人楊彥，字邦傑。自幼聰敏，志在山林，自號「東里野民」，雖受朝廷召見，仍無意做官。", "Said to be Yang Yan of the Song dynasty, a gifted recluse who preferred the countryside to office."], "戊午": ["據傳為明代人黎近。宣德年間任高安知縣，招降亂賊；因執法嚴正遭權臣忌恨，入獄十年，獲釋後改任泌陽知縣。", "Said to be Li Jin of the Ming dynasty, a strict, honest magistrate who endured ten years of unjust imprisonment."], "己未": ["據傳為宋代須城人傅康。任汀州、南劍知州，嚴懲奸吏，率軍擊退寇亂，百姓尊稱「傅父」。", "Said to be Fu Kang of the Song dynasty, a prefect the people called \"Father Fu.\""], "庚申": ["據傳為金代臨潢人毛子廉。善射有勇，招撫二千六百戶歸附，任上京副留守，治理臨潢十餘年。", "Said to be Mao Zilian of the Jin dynasty, a brave archer who governed Linhuang for over ten years."], "辛酉": ["據傳為元代河南人石正卿。任萬泉縣尹，廉直公正；荒年時開倉賑濟、煮粥施藥，救活許多百姓。", "Said to be Shi Zhengqing of the Yuan dynasty, an honest magistrate who opened the granaries in a famine."], "壬戌": ["據傳為明代錢塘人洪鍾，字宣之。成化年間進士，歷任按察使、巡撫，整治邊防，正德年間平定湖廣、陝西亂事。", "Said to be Hong Zhong of the Ming dynasty, a governor who strengthened border defenses and quelled uprisings."], "癸亥": ["據傳為明代崑山人虞臣。成化年間進士，歷任兵部及四川參議，剛正清慎，在家孝順友愛。", "Said to be Yu Chen of the Ming dynasty, an upright official devoted to his family."]};
const GAN="甲乙丙丁戊己庚辛壬癸", ZHI="子丑寅卯辰巳午未申酉戌亥";
const CNY_FALLBACK = {1900:[1,31],1901:[2,19],1902:[2,8],1903:[1,29],1904:[2,16],1905:[2,4],1906:[1,25],1907:[2,13],1908:[2,2],1909:[1,22],1910:[2,10],1911:[1,30],1912:[2,18],1913:[2,6],1914:[1,26],1915:[2,14],1916:[2,3],1917:[1,23],1918:[2,11],1919:[2,1],1920:[2,20],1921:[2,8],1922:[1,28],1923:[2,16],1924:[2,5],1925:[1,24],1926:[2,13],1927:[2,2],1928:[1,23],1929:[2,10],1930:[1,30],1931:[2,17],1932:[2,6],1933:[1,26],1934:[2,14],1935:[2,4],1936:[1,24],1937:[2,11],1938:[1,31],1939:[2,19],1940:[2,8],1941:[1,27],1942:[2,15],1943:[2,5],1944:[1,25],1945:[2,13],1946:[2,2],1947:[1,22],1948:[2,10],1949:[1,29],1950:[2,17],1951:[2,6],1952:[1,27],1953:[2,14],1954:[2,3],1955:[1,24],1956:[2,12],1957:[1,31],1958:[2,18],1959:[2,8],1960:[1,28],1961:[2,15],1962:[2,5],1963:[1,25],1964:[2,13],1965:[2,2],1966:[1,21],1967:[2,9],1968:[1,30],1969:[2,17],1970:[2,6],1971:[1,27],1972:[2,15],1973:[2,3],1974:[1,23],1975:[2,11],1976:[1,31],1977:[2,18],1978:[2,7],1979:[1,28],1980:[2,16],1981:[2,5],1982:[1,25],1983:[2,13],1984:[2,2],1985:[2,20],1986:[2,9],1987:[1,29],1988:[2,17],1989:[2,6],1990:[1,27],1991:[2,15],1992:[2,4],1993:[1,23],1994:[2,10],1995:[1,31],1996:[2,19],1997:[2,7],1998:[1,28],1999:[2,16],2000:[2,5],2001:[1,24],2002:[2,12],2003:[2,1],2004:[1,22],2005:[2,9],2006:[1,29],2007:[2,18],2008:[2,7],2009:[1,26],2010:[2,14],2011:[2,3],2012:[1,23],2013:[2,10],2014:[1,31],2015:[2,19],2016:[2,8],2017:[1,28],2018:[2,16],2019:[2,5],2020:[1,25],2021:[2,12],2022:[2,1],2023:[1,22],2024:[2,10],2025:[1,29],2026:[2,17],2027:[2,6],2028:[1,26],2029:[2,13],2030:[2,3],2031:[1,23],2032:[2,11],2033:[1,31],2034:[2,19],2035:[2,8],2036:[1,28],2037:[2,15],2038:[2,4],2039:[1,24],2040:[2,12],2041:[2,1],2042:[1,22],2043:[2,10],2044:[1,30],2045:[2,17],2046:[2,6],2047:[1,26],2048:[2,14],2049:[2,2],2050:[1,23],2051:[2,11],2052:[2,1],2053:[2,19],2054:[2,8],2055:[1,28],2056:[2,15],2057:[2,4],2058:[1,24],2059:[2,12],2060:[2,2],2061:[1,21],2062:[2,9],2063:[1,29],2064:[2,17],2065:[2,5],2066:[1,26],2067:[2,14],2068:[2,3],2069:[1,23],2070:[2,11],2071:[1,31],2072:[2,19],2073:[2,7],2074:[1,27],2075:[2,15],2076:[2,5],2077:[1,24],2078:[2,12],2079:[2,2],2080:[1,22],2081:[2,9],2082:[1,29],2083:[2,17],2084:[2,6],2085:[1,26],2086:[2,14],2087:[2,3],2088:[1,24],2089:[2,10],2090:[1,30],2091:[2,18],2092:[2,7],2093:[1,27],2094:[2,15],2095:[2,5],2096:[1,25],2097:[2,12],2098:[2,1],2099:[1,21],2100:[2,9]};
function cnyOf(y){
  if(typeof window.Lunar!=="undefined"){ try{ const s=Lunar.fromYmd(y,1,1).getSolar(); return new Date(s.getYear(),s.getMonth()-1,s.getDay()); }catch(e){} }
  const c=CNY_FALLBACK[y]; return c ? new Date(y,c[0]-1,c[1]) : null;
}
function taisuiOfYear(y){
  const start=cnyOf(y), next=cnyOf(y+1); if(!start||!next) return null;
  const end=new Date(next); end.setDate(end.getDate()-1);
  const i=((y-4)%60+60)%60, gz=GAN[i%10]+ZHI[i%12];
  const full=TAISUI.find(n=>n.startsWith(gz)); if(!full) return null;
  return {y, gz, full, name:full.replace(gz+"太歲·",""), start, end, bio:TAISUI_BIO[gz]};
}
function taisuiOf(d=new Date()){
  const day=new Date(d.getFullYear(),d.getMonth(),d.getDate());
  let y=day.getFullYear(); const s=cnyOf(y); if(!s) return null;
  if(day<s) y--;
  return taisuiOfYear(y);
}
let TS_BASE=null, TS_Y=null;
function showTaisuiYear(y){
  const t=taisuiOfYear(y); if(!t) return false;
  TS_Y=y;
  const f=d=>`${d.getFullYear()}/${d.getMonth()+1}/${d.getDate()}`, fe=d=>d.toLocaleDateString("en-US",{year:"numeric",month:"short",day:"numeric"});
  const off=y-TS_BASE;
  const lab = off===0 ? L("今年值年太歲","Tai Sui of This Year") : off===1 ? L("明年值年太歲","Tai Sui of Next Year") : off===-1 ? L("去年值年太歲","Tai Sui of Last Year") : L(`${y}年值年太歲`,`Tai Sui of ${y}`);
  const $=id=>document.getElementById(id);
  $("tsLabel").innerHTML=lab;
  $("tsYear").innerHTML=L(t.gz+"太歲·", t.gz+" year · ");
  $("tsName").textContent=t.name;
  $("tsRange").innerHTML=L(`國曆 ${f(t.start)} 至 ${f(t.end)}`, `${fe(t.start)} – ${fe(t.end)}`);
  $("tsBio").innerHTML = t.bio ? L(t.bio[0], t.bio[1]) : "";
  $("taisuiNow").classList.toggle("other", off!==0);
  $("tsBack").hidden = off===0;
  $("tsPrev").disabled = !taisuiOfYear(y-1);
  $("tsNext").disabled = !taisuiOfYear(y+1);
  document.querySelectorAll(".taisui-all td.sel").forEach(x=>x.classList.remove("sel"));
  if(off!==0) document.querySelector(`.taisui-all td[data-gz="${t.gz}"]`)?.classList.add("sel");
  return true;
}
function renderTaisui(){
  const t=taisuiOf(); if(!t) return;
  const today=document.getElementById("taisuiToday");
  if(today) today.innerHTML = `<span>${L(`${t.gz}年值年太歲·<b>${t.name}</b>`, `Tai Sui of the year: <b>${t.name}</b>`)}</span>`;
  const box=document.getElementById("taisuiNow");
  if(box){
    TS_BASE=t.y; showTaisuiYear(t.y); box.hidden=false;
    document.querySelectorAll(".taisui-all td.now").forEach(x=>x.classList.remove("now"));
    document.querySelector(`.taisui-all td[data-gz="${t.gz}"]`)?.classList.add("now");
    document.getElementById("tsPrev").onclick=()=>showTaisuiYear(TS_Y-1);
    document.getElementById("tsNext").onclick=()=>showTaisuiYear(TS_Y+1);
    document.getElementById("tsBack").onclick=()=>showTaisuiYear(TS_BASE);
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
