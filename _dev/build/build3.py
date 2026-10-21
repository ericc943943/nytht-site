#!/usr/bin/env python3
"""第一版版面（匾額首頁、雙欄、卡片、報名色帶）＋舊網站的分頁、標題與內容＋藍色配色。"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "web3")

# 取用 build2.py 裡整理好的原文與資料（只執行資料區段）
src = open(os.path.join(HERE, "build2.py")).read()
exec(src[src.index("def L("):src.index("# ---------------------------------------------------------------- 首頁")])

def B(zh, en, tag="p", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}><span class="zh">{zh}</span><span class="en">{en}</span></{tag}>'

def page(fname, tzh, desc, body, lunar=False):
    title = "紐約花蓮慈惠堂 – New York Hua Lian Tsu Hui Temple" if fname=="index.html" else f"{tzh} – 紐約花蓮慈惠堂"
    html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
{'<script src="https://cdn.jsdelivr.net/npm/lunar-javascript@1.7.7/lunar.js"></script>' if lunar else ''}
<script src="assets/site.js"></script>
</head>
<body>
<header class="site-header"></header>
<main>
{body}
</main>
<footer class="site-footer"></footer>
</body>
</html>
'''
    open(os.path.join(OUT, fname), "w").write(html)

def pagehead(parent_zh, parent_en, zh, en):
    eyebrow = B(parent_zh, parent_en, "div", "eyebrow") if parent_zh else ""
    return f'<section class="pagehead gutter"><div class="container">{eyebrow}{B(zh, en, "h1")}</div></section>'

def sec(zh, en, small_zh="", small_en=""):
    sm = B(small_zh, small_en, "small") if small_zh else ""
    return f'<h2 class="sec-title">{sm}{L(zh, en)}</h2>'

BAND = f'''<section class="band gutter" style="padding-block:0"><div class="container">
  <div>{B("線上點燈和法會報名", "Lamp & Ceremony Registration", "h2")}
    {B("點燈、法會可以線上報名，送出後帶繳費單到堂裡繳交現金。", "Register online, then bring your payment slip to the temple and pay in cash.")}</div>
  <div style="display:flex;flex-wrap:wrap;gap:12px">
    <a class="cta big" href="https://nytht.vercel.app/#lamp">{L("點燈報名", "Lamp lighting")}</a>
    <a class="cta big ghost" href="https://nytht.vercel.app/">{L("法會報名", "Ceremonies")}</a>
  </div>
</div></section>'''

# 點燈：舊網站的三個小標＋五路財神燈（舊網站無說明）
LAMPS4 = [
  ("◎安太歲", "◎ Tai Sui", "太歲為值年神祇。生肖與當年太歲正沖或對沖者，宜安奉太歲，祈求化險為夷，避除三災九橫之厄。本堂於二樓太歲殿供奉六十甲子太歲星君，為美東唯一的星辰殿。",
   "Those whose zodiac sign clashes with the year's Tai Sui are advised to make offerings to Tai Sui to turn misfortune aside. The sixty Tai Sui generals are enshrined in our second-floor Tai Sui Hall.", "#356D82"),
  ("◎光明燈", "◎ Guangming Lamp", "人的本命元神不生不滅，故光明燈又稱元神燈、長明燈、無盡燈。點燈祈求運勢亨通、精神昂揚，慈光普照、破除黑暗。",
   "Also called the Lamp of the Original Spirit or the Everlasting Lamp, it is lit for good fortune and vitality.", "#58BEEE"),
  ("◎文昌光明燈", "◎ Wenchang Lamp", "文昌消災保運法，專為參加考試者設立，由文昌星君及南斗賢良司共同護佑，開啟智慧、增進考運，助學子金榜題名。",
   "A Wenchang blessing rite for those facing examinations, to open wisdom and bring success in exams.", "#4698BE"),
  ("五路財神燈", "Five Wealth Gods Lamp", "（舊網站沒有這盞燈的說明，請提供文字。）", "(Description to be added.)", "#89A9BE"),
]
def lamp_icon(color):
    return f'''<svg class="icon" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 6c4 6 8 9 8 15a8 8 0 0 1-16 0c0-6 4-9 8-15z" fill="{color}" opacity=".9"/><path d="M24 15c2 3 3.5 4.5 3.5 7a3.5 3.5 0 0 1-7 0c0-2.5 1.5-4 3.5-7z" fill="#FFFFFF"/><rect x="14" y="31" width="20" height="5" rx="2" fill="{color}"/><rect x="18" y="36" width="12" height="6" rx="1.5" fill="{color}" opacity=".7"/></svg>'''

HALL_KEYS = ["main", "wenchang", "caishen", "taisui", "sanqing"]
HALL_DEITIES = {
    "main": [("無極瑤池大聖西王金母大天尊","Golden Mother of the Jasper Pool"),("玉皇赦罪賜福大天尊","Jade Emperor"),("無上虛空地母無量慈尊","Earth Mother"),("觀音大士","Guanyin"),("關聖帝君","Guan Di"),("天上聖母","Mazu"),("中壇元帥","Marshal Zhongtan"),("福德正神","Earth God")],
    "wenchang": [("文昌帝君","Wenchang Dijun"),("魁斗星君","Kuidou Xingjun"),("大成至聖先師","Confucius"),("天聾、地啞二聖","Tianlong and Diya")],
    "caishen": [("天官大帝","Heavenly Official"),("文財神范蠡","Fan Li"),("武財神趙公明","Zhao Gongming"),("南山通利仙官石崇","Shi Chong"),("北府納庫仙官沈萬山","Shen Wanshan"),("招財、進寶童子","Zhaocai and Jinbao")],
    "taisui": [("斗姆元君","Doumu Yuanjun"),("六十甲子太歲星君","Sixty Tai Sui generals")],
    "sanqing": [("元始天尊","Yuanshi Tianzun"),("靈寶天尊","Lingbao Tianzun"),("太上道祖","Daode Tianzun")],
}
TIMELINE = [("1991","於法拉盛羅斯福路開堂設教","Temple opens on Roosevelt Avenue, Flushing"),
            ("2002","遷至法拉盛大學點大道","Moves to College Point Boulevard"),
            ("2007","金母揮鸞指示興建宗教文化道場","The Golden Mother instructs that a temple be built"),
            ("2008","於大學點購得建廟用地","Land purchased in College Point"),
            ("2009","建堂動土興工","Construction begins"),
            ("2012","國曆6月13日（農曆4月24日）瑤池金母安座大典","Enthronement ceremony, June 13, 2012")]

# ================================================================ 首頁
index_body = f'''
<section class="hero gutter"><div class="container fade">
  <div class="plaque" aria-hidden="true"><span>{"".join(f"<i>{c}</i>" for c in "紐約花蓮慈惠堂")}</span></div>
  <div>
    {B("紐約花蓮慈惠堂", "New York Hua Lian Tsu Hui Temple", "h1")}
    {B(HISTORY[0][0], HISTORY[0][1], "p", "lead")}
    <div class="actions">
      <a class="cta big" href="https://nytht.vercel.app/#lamp">{L("點燈報名", "Lamp lighting")}</a>
      <a class="cta big ghost" href="https://nytht.vercel.app/">{L("法會報名", "Ceremonies")}</a>
    </div>
    <div class="today" id="today"></div>
  </div>
</div></section>

<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div>
    {sec("年度行事", "Annual Calendar")}
    <ul class="upcoming" id="upcoming" data-count="5"></ul>
    <p style="margin-top:14px"><a href="calendar.html">{L("年度行事 》》", "Annual calendar 》》")}</a></p>
  </div>
  <div class="card" style="gap:14px">
    {sec("點燈祈福", "Lamp Lighting")}
    <div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">
      {"".join(f'<div style="display:flex;gap:8px;align-items:center">{lamp_icon(c)}<b>{L(z,e)}</b></div>' for z,e,c in [("個人光明燈","Guangming",LAMPS4[1][4]),("太歲燈","Tai Sui",LAMPS4[0][4]),("五路財神燈","Five Wealth Gods",LAMPS4[3][4]),("文昌燈","Wenchang",LAMPS4[2][4])])}
    </div>
    {B("每盞 $120。凡安奉太歲、點光明燈、文昌光明燈的信眾，本堂於每月農曆初一、十五誦經上疏。", "$120 per lamp. On the 1st and 15th of every lunar month the temple chants scriptures and presents prayers for all lamp holders.", "p", "muted")}
    <div style="display:flex;flex-wrap:wrap;gap:10px">
      <a class="cta" href="https://nytht.vercel.app/#lamp">{L("點燈報名", "Register")}</a>
      <a class="cta ghost" href="lamps.html">{L("點燈祈福", "Lamp lighting")}</a>
    </div>
  </div>
</div></section>

<hr class="divider">

<section class="gutter"><div class="container grid g2" style="align-items:center">
  {ph("master.jpg", "堂主簡介", "Head of the Temple")}
  <div>
    {sec("堂主簡介", "Head of the Temple")}
    <div class="prose">{P(*MASTER[0])}</div>
    <p style="margin-top:14px"><a href="master.html">{L("閱讀更多 》》", "Read more 》》")}</a></p>
  </div>
</div></section>

<section class="gutter" style="background:var(--paper-2)"><div class="container">
  {sec("本堂設施", "Facilities")}
  <div class="grid g3">
    {"".join(f'<a class="card" href="halls.html#{k}" style="text-decoration:none;color:inherit"><h3>{L(zh,en)}</h3>{B(dz,de,"p","muted")}<span class="more" style="color:var(--red)">{L("閱讀更多","More")}</span></a>' for k,(zh,en,img,dz,de) in zip(HALL_KEYS, HALLS))}
  </div>
</div></section>

{BAND}

<section class="gutter"><div class="container grid g2">
  <div>
    {sec("聯繫本堂", "Contact Us")}
    <dl class="contact-list">
      <div><dt>{L("地址","Address")}</dt><dd data-address></dd></div>
      <div><dt>{L("電話","Tel")}</dt><dd data-tel></dd></div>
      <div><dt>{L("傳真","Fax")}</dt><dd data-fax></dd></div>
      <div><dt>Email</dt><dd data-email></dd></div>
    </dl>
    <p style="margin-top:16px"><a href="contact.html">{L("聯繫本堂 》》", "Contact us 》》")}</a></p>
  </div>
  {ph("gallery-1.jpg", "活動剪影", "Gallery")}
</div></section>
'''
page("index.html", "首頁", "紐約花蓮慈惠堂 New York Hua Lian Tsu Hui Temple：奉祀瑤池金母，點燈祈福、法會可線上報名。", index_body, lunar=True)

# ================================================================ 主神簡介
page("deity.html", "主神簡介", "紐約花蓮慈惠堂主神：無極瑤池大聖西王金母大天尊。", f'''
{pagehead("本堂簡介","About","主神簡介","Principal Deity")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  {ph("jinmu.jpg", "瑤池金母", "The Golden Mother", "tall")}
  <div class="reading prose">
    {DRAFT}
    {P("瑤池金母又稱西王母、王母娘娘、金母元君，信眾尊稱「母娘」。依道教典籍記載，太古之初先化生東王木公，再化生金母，二者共理陰陽二氣，養育天地萬物。",
       "The Golden Mother of the Jasper Pool, also called Xiwangmu, is lovingly called Mu Niang by her devotees. Taoist scriptures say that at the beginning of time she and the Lord King of the East were born of the primal energies, and together they govern yin and yang and nurture all things.")}
    {P("金母為女仙之首，統領三界十方女神。傳說她居於崑崙瑤池，池畔蟠桃三千年一熟，因而有蟠桃盛會、群仙祝壽的典故。聖誕為農曆七月十八日（亦有三月初三之說）。",
       "She is the foremost of female immortals. Legend places her palace by the Jasper Pool on Mount Kunlun, where the peaches of immortality ripen once in three thousand years. Her birthday is the 18th day of the 7th lunar month (some observe the 3rd day of the 3rd month).")}
    {P("自金母聖鸞降駕花蓮吉安後，信仰在台灣迅速發展，以慈惠堂、勝安宮、瑤池宮、王母宮等為名的宮堂近千間，信眾彼此以師兄、師姐相稱。",
       "Since her manifestation in Ji'an, Hualien, her faith has spread to nearly a thousand temples in Taiwan, where devotees call one another brother and sister.")}
    <h2 class="subhead">{L("無極瑤池大聖西王金母寶誥　志心皈命禮","Hymn of Praise to the Golden Mother")}</h2>
    <div class="draftnote">{L("寶誥原文待補。","Original text to be added.")}</div>
  </div>
</div></section>
{BAND}
''')

# ================================================================ 由來（原文）
page("history.html", "紐約花蓮慈惠堂由來", "紐約花蓮慈惠堂由來。", f'''
{pagehead("本堂簡介","About","紐約花蓮慈惠堂由來","Our History")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading prose">{"".join(P(z,e) for z,e in HISTORY)}</div>
  <div style="display:grid;gap:20px">
    {ph("temple.jpg", "紐約花蓮慈惠堂", "The temple")}
    <ol class="upcoming years" style="list-style:none">{"".join(f'<li><div class="when">{y}</div><div class="what">{L(z,e)}</div></li>' for y,z,e in TIMELINE)}</ol>
  </div>
</div></section>
{BAND}
''')

# ================================================================ 堂主簡介
page("master.html", "堂主簡介", "紐約花蓮慈惠堂堂主何春燕女士。", f'''
{pagehead("本堂簡介","About","堂主簡介","Head of the Temple")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading prose">{DRAFT}{"".join(P(z,e) for z,e in MASTER)}</div>
  {ph("master.jpg", "堂主", "Ms. Ho Chun-Yen", "tall")}
</div></section>
{BAND}
''')

# ================================================================ 最新活動
page("news.html", "最新活動", "紐約花蓮慈惠堂最新活動。", f'''
{pagehead("本堂訊息","Temple News","最新活動","Latest Events")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div>{postlist(NEWS)}</div>
  <div class="card">
    {sec("活動剪影", "Gallery")}
    {B("最即時的活動照片與影片，請看本堂 Facebook 粉絲專頁。", "For the latest photos and videos, see our Facebook page.", "p", "muted")}
    <p><a class="cta" data-fb href="#" target="_blank" rel="noopener">Facebook</a></p>
    <p><a href="gallery.html">{L("活動剪影 》》","Gallery 》》")}</a></p>
  </div>
</div></section>
''')

# ================================================================ 年度行事（第一版的三欄表格）
page("calendar.html", "年度行事", "紐約花蓮慈惠堂年度行事。", f'''
{pagehead("本堂訊息","Temple News","年度行事","Annual Calendar")}
<section class="gutter"><div class="container">
  <div class="tablewrap"><table class="cal">
    <thead><tr><th>{L("農曆","Lunar date")}</th><th>{L("行事","Event")}</th><th>{L("國曆（下一次）","Next date")}</th></tr></thead>
    <tbody id="calBody"></tbody>
  </table></div>
  <div class="notice" style="margin-top:24px">{L("本堂每於清明節、重陽節特為眾信士之九玄七祖誦經祭拜。", "Every Qingming and Double Ninth Festival, the temple chants scriptures for the ancestors of all devotees.")}</div>
</div></section>
{BAND}
''', lunar=True)

# ================================================================ 點燈祈福
page("lamps.html", "點燈祈福", "紐約花蓮慈惠堂點燈祈福：安太歲、光明燈、文昌光明燈、五路財神燈。", f'''
{pagehead("本堂訊息","Temple News","點燈祈福","Lamp Lighting")}
<section class="gutter"><div class="container">
  {DRAFT}
  <div class="grid g2">
    {"".join(f'<article class="card lamp">{lamp_icon(c)}<h3>{L(z,e)}</h3><div class="price">{L("每盞 $120","$120 per lamp")}</div>{B(dz,de)}</article>' for z,e,dz,de,c in LAMPS4)}
  </div>
</div></section>

<section class="gutter" style="background:var(--paper-2)"><div class="container grid g2" style="align-items:start">
  <div>
    <ul class="facts">
      <li>{L("凡安奉太歲、點光明燈、文昌光明燈的信眾，本堂於每月農曆初一、十五誦經上疏。", "For everyone holding a Tai Sui offering or lamp, the temple chants scriptures on the 1st and 15th of every lunar month.")}</li>
      <li>{L("本堂光明燈、太歲燈、文昌燈、五路財神燈採用LED電腦尋燈系統。", "Our lamps use an LED lamp-finder system.")}</li>
      <li>{L("每年農曆十二月二十日舉行謝平安法會，並啟點翌年光明燈及安奉太歲。", "On the 20th day of the 12th lunar month, the year-end thanksgiving ceremony is held and lamps for the new year are lit.")}</li>
    </ul>
  </div>
  <div>
    {sec("線上點燈和法會報名", "Lamp & Ceremony Registration")}
    <ol class="upcoming nums" style="list-style:none">
      <li><div class="when">1</div><div class="what">{L("線上填寫報名表，每一位可以點一盞或多盞燈。", "Fill in the online form. Each person can have one or more lamps.")}</div></li>
      <li><div class="when">2</div><div class="what">{L("送出後畫面會出現繳費單，請截圖或列印。", "A payment slip appears when you submit. Save a screenshot or print it.")}</div></li>
      <li><div class="when">3</div><div class="what">{L("帶著繳費單到堂裡繳交現金，告知報名編號即可。", "Bring the slip to the temple and pay in cash.")}</div></li>
    </ol>
    <p style="margin-top:18px"><a class="cta big" href="https://nytht.vercel.app/#lamp">{L("點燈報名", "Register for a lamp")}</a></p>
    <p class="muted" style="margin-top:10px;font-size:.9rem">{L("也可以來電登記：", "You may also register by phone: ")}<span data-tel class="nowrap"></span></p>
  </div>
</div></section>

<section class="gutter"><div class="container">
  {sec("法會報名", "Ceremony Registration")}
  <div class="grid g3">
    <div class="card"><h3>{L("超渡","Deliverance")}</h3><div class="price">{L("每牌位 $160","$160 per tablet")}</div>{B("超薦亡者、歷代祖先、冤親債主、地基主、水子靈等。","For departed family members, ancestors, karmic creditors, land spirits and unborn children.","p","muted")}</div>
    <div class="card"><h3>{L("祈福消災點燈 - 蓮花福慧燈","Lotus Lamp")}</h3><div class="price">{L("每位 $60","$60 per person")}</div></div>
    <div class="card"><h3>{L("供齋","Food offering")}</h3><div class="price">{L("功德金隨喜","Any amount")}</div>{B("供養十方孤魂。","An offering to wandering souls.","p","muted")}</div>
  </div>
  <p style="margin-top:18px"><a class="cta" href="https://nytht.vercel.app/">{L("法會報名","Register for a ceremony")}</a></p>
</div></section>
''')

# ================================================================ 本堂設施
page("halls.html", "本堂設施", "紐約花蓮慈惠堂本堂設施：大殿、文昌帝君殿、五路財神殿、太歲殿、三清殿。", f'''
{pagehead("","","本堂設施","Facilities")}
<section class="gutter"><div class="container">
  {DRAFT}
  {"".join(f"""<article class="hall" id="{k}">{ph(img, zh, en)}
    <div><h2>{L(zh,en)}</h2>{B(dz,de,"p","prose")}
      <ul class="deities">{"".join(f"<li>{L(a,b)}</li>" for a,b in HALL_DEITIES[k])}</ul></div></article>""" for k,(zh,en,img,dz,de) in zip(HALL_KEYS, HALLS))}
</div></section>
{BAND}
''')

# ================================================================ 活動剪影（第一版的照片格線）
page("gallery.html", "活動剪影", "紐約花蓮慈惠堂活動剪影。", f'''
{pagehead("","","活動剪影","Gallery")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div><ul class="postlist">
    {"".join(f'<li><a href="{FBV}{vid}/" target="_blank" rel="noopener"><b>{L(z,e)}</b></a><time>Facebook</time></li>' for z,e,vid in VIDEOS)}
    {"".join(f'<li><b>{L(z,e)}</b></li>' for z,e in GALLERY_MORE)}
  </ul>
  <p style="margin-top:18px"><a class="cta" data-fb href="#" target="_blank" rel="noopener">{L("查看更多影音 》》","More videos 》》")}</a></p></div>
  <div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">
    {ph("gallery-1.jpg","活動剪影","Gallery")}{ph("gallery-2.jpg","活動剪影","Gallery")}{ph("gallery-3.jpg","活動剪影","Gallery")}{ph("gallery-4.jpg","活動剪影","Gallery")}
  </div>
</div></section>
''')

# ================================================================ 近期文章
page("articles.html", "近期文章", "紐約花蓮慈惠堂近期文章。", f'''
{pagehead("","","近期文章","Recent Articles")}
<section class="gutter"><div class="container reading">
  <div class="draftnote">{L("文章內容待補：請提供舊網站這三篇文章的原文。","Article text to be added.")}</div>
  {postlist(ARTICLES)}
</div></section>
''')

# ================================================================ 聯繫本堂
page("contact.html", "聯繫本堂", "紐約花蓮慈惠堂地址、電話與 Email。", f'''
{pagehead("","","聯繫本堂","Contact Us")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div>
    <dl class="contact-list">
      <div><dt>{L("地址","Address")}</dt><dd data-address></dd></div>
      <div><dt>{L("電話","Tel")}</dt><dd data-tel></dd></div>
      <div><dt>{L("傳真","Fax")}</dt><dd data-fax></dd></div>
      <div><dt>Email</dt><dd data-email></dd></div>
      <div><dt>Facebook</dt><dd><a data-fb href="#" target="_blank" rel="noopener">{L("紐約花蓮慈惠堂","Our page")}</a></dd></div>
    </dl>
    <p style="margin-top:22px"><a class="cta" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=22-06+121st+St,+College+Point,+NY+11356">{L("Google 地圖","Google Maps")}</a></p>
  </div>
  <iframe class="mapframe" title="Map" loading="lazy" src="https://maps.google.com/maps?q=22-06%20121st%20St%2C%20College%20Point%2C%20NY%2011356&z=15&output=embed"></iframe>
</div></section>
{BAND}
''')
print("ok")
