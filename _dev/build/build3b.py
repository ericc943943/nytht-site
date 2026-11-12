#!/usr/bin/env python3
"""在 build3 的基礎上，把主神簡介、堂主簡介、點燈祈福、本堂設施、年度行事、近期文章換成舊網站原文。"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build3.py")).read()
# 首頁的堂主簡介、本堂設施卡片改用原文
import importlib.util
spec = importlib.util.spec_from_file_location("content", os.path.join(HERE, "content.py")); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
src = src.replace('{P(*MASTER[0])}', '{P(C.MASTER[0], MASTER[0][1])}')
src = src.replace('{B(dz,de,"p","muted")}<span class="more"', '{B(C.HALLS_TEXT[k].split(chr(10))[0], de, "p", "muted")}<span class="more"')
# 樓層示意圖（首頁、本堂設施頁共用）。左右＝信眾面向神明；文昌帝君殿一格切成上下兩半，下半是殿前供桌（月老）；五路財神殿同樣切半，下半是殿前的祭改處
FLOORPLAN_SRC = r"""
HALL_BY = dict(zip(HALL_KEYS, HALLS))
def hn(k): return HALL_BY[k][0], HALL_BY[k][1]
def num(n, cls=""):
    return f'<span class="fp-num {cls}" aria-hidden="true">{n}</span>'
def fp(k, cls="", base="", badge=""):
    zh,en = hn(k)
    zh = {"caishen":"五路<br class='br'>財神殿","wenchang":"文昌<br class='br'>帝君殿"}.get(k, zh)
    sub = {"main":L("無極瑤池金母","Golden Mother")+"<br>"+L("<span class='nw'>地母娘娘</span>・<span class='nw'>玉皇大帝</span>","<span class='nw'>Earth Mother</span> · <span class='nw'>Jade Emperor</span>"),"taisui":L("斗姆元君・六十甲子太歲","Doumu and the 60 Tai Sui"),"sanqing":L("<span class='nw'>元始天尊</span>・<span class='nw'>靈寶天尊</span>・<span class='nw'>道德天尊</span>","The Three Pure Ones")}.get(k,"")
    return f'<a class="fp-hall {cls}" href="{base}#{k}">{badge}<b>{L(zh,en)}</b>{f"<small>{sub}</small>" if sub else ""}</a>'
def fp_caishen(base=""):
    return ('<div class="fp-split">' + fp("caishen","side",base,num(4,"n-bottom")) + num(1,"n-take")
            + f'<a class="fp-hall fp-table" href="{base}#caishen"><b>{L("祭改處","Jigai desk")}</b></a></div>')
def fp_wenchang(base=""):
    return ('<div class="fp-split">' + fp("wenchang","side",base) + num(3,"n-seam")
            + f'<a class="fp-hall fp-table fp-deity" href="{base}#wenchang"><b>{L("月老","Yue Lao")}</b></a></div>')
ROUTE_STEPS = [
    ("在祭改處左側取三枝香、點香", "Take three incense sticks to the left of the Jigai desk and light them"),
    ("大殿參拜瑤池金母、玉皇大帝、地母娘娘、天上聖母", "In the Main Hall, pay respects to the Golden Mother, the Jade Emperor, the Earth Mother and Mazu"),
    ("文昌帝君殿參拜", "Pay respects in the Hall of Wenchang"),
    ("五路財神殿參拜，之後從出口出去", "Pay respects in the Hall of the Five Wealth Gods, then leave by the exit"),
    ("外廊主爐插一枝香，再從左側樓梯下樓", "Place one stick in the main burner on the veranda, then go down the left stairs"),
    ("前庭天公爐插一枝香，再從右側樓梯上樓，由入口回到室內", "Place one stick in the Heaven burner in the front yard, then go up the right stairs and come back in through the entrance"),
    ("上二樓太歲殿參拜，不插香", "Go up to the Tai Sui Hall on the second floor (no incense)"),
    ("上三樓三清殿參拜", "Go up to the Hall of the Three Pure Ones on the third floor"),
    ("外廊香爐插一枝香", "Place one stick in the incense burner on the veranda"),
]
def floorplan_html(base=""):
    rows = [
        f'<div class="fp-row fp-3f"><div class="fp-floor">3F<small class="fp-io">{L("室內","Indoor")}</small></div>{fp("sanqing","wide",base,num(8,"n-left"))}</div>',
        f'<div class="fp-ground fp-3fout"><div class="fp-floor fp-gfloor">3F<small class="fp-io">{L("外廊","Veranda")}</small></div>'
        f'<div class="fp-gcenter"><div class="fp-gwrap"><div class="fp-burner">{num(9,"n-side")}<b>{L("三清殿香爐","Three Pure Ones burner")}</b></div></div></div></div>',
        f'<div class="fp-row"><div class="fp-floor">2F</div>{fp("taisui","wide",base,num(7,"n-left"))}</div>',
        f'<div class="fp-row fp-1f"><div class="fp-floor">1F<small class="fp-io">{L("室內","Indoor")}</small></div>{fp_caishen(base)}{fp("main","main",base,num(2,"n-bottom"))}{fp_wenchang(base)}'
        f'<span class="fp-door d-left">{L("出口","Exit")}</span>'
        f'<span class="fp-door d-right">{L("入口","Entrance")}</span>'
        f'<span class="fp-wall" aria-hidden="true"></span><div class="fp-floor fp-terfloor">1F<small class="fp-io">{L("外廊","Veranda")}</small></div>'
        f'<div class="fp-terrace"><div class="fp-burner">{num(5,"n-side")}<b>{L("主爐","Main burner")}</b></div></div></div>',
        f'<div class="fp-ground"><div class="fp-floor fp-gfloor">{L("前庭","Front yard")}</div>'
        f'<div class="fp-gcenter"><div class="fp-gwrap">'
        f'<div class="fp-stairs s-left" aria-label="左側樓梯，下樓"><b>{L("左側樓梯","Left stairs")}</b><span class="arw">↓</span></div>'
        f'<div class="fp-burner">{num(6,"n-side")}<b>{L("天公爐","Heaven burner")}</b></div>'
        f'<div class="fp-stairs s-right" aria-label="右側樓梯，上樓"><span class="arw">↑</span><b>{L("右側樓梯","Right stairs")}</b></div>'
        f'</div></div></div>',
    ]
    steps = "".join(f'<li><span class="fp-num n-list" aria-hidden="true">{i}</span><span>{L(z,e)}</span></li>' for i,(z,e) in enumerate(ROUTE_STEPS,1))
    notes = (f'<div class="fp-route-notes"><p class="fp-route-head">{L("一共三枝香，右側入口進、左側出口出。","Three incense sticks in all. Enter on the right, exit on the left.")}</p>'
             f'<ol class="fp-steps">{steps}</ol></div>')
    btn = f'<button type="button" class="fp-routebtn" aria-pressed="false">{L("參拜順序","Order of worship")}</button>'
    return ('<div class="fp-wrap route"><div class="fp-tools">' + btn + '</div>'
            + '<div class="floorplan" aria-label="樓層示意圖 Floor plan">' + "".join(rows) + '</div>' + notes + '</div>')
"""
src = src.replace("# ================================================================ 首頁", FLOORPLAN_SRC + "\n# ================================================================ 首頁", 1)
g = {"__file__": os.path.join(HERE, "build3.py"), "C": C}
exec(compile(src, "build3.py", "exec"), g)
L, B, P, ph, page, pagehead, sec, BAND, lamp_icon = (g[k] for k in ["L","B","P","ph","page","pagehead","sec","BAND","lamp_icon"])
HALLS, HALL_KEYS, HALL_DEITIES, ARTICLES, MASTER = g["HALLS"], g["HALL_KEYS"], g["HALL_DEITIES"], g["ARTICLES"], g["MASTER"]
floorplan_html, HALL_BY, deity_html = g["floorplan_html"], g["HALL_BY"], g["deity_html"]

def zh_en(zh_html, en_html):
    return f'<div class="zh">{zh_html}</div><div class="en">{en_html}</div>'
def paras(lst): return "".join(f"<p>{t}</p>" for t in lst)
def br(t): return t.replace("\n", "<br>")
def wrapimg(src, alt, side="left", w=None):
    st = f' style="width:{w}px"' if w else ""
    return f'<figure class="wrapimg {side}"{st}><img src="images/{src}" alt="{alt}"></figure>'

# ---------------------------------------------------------------- 主神簡介
deity_en = paras([
 "The Golden Mother of the Jasper Pool, also called Xiwangmu or Wangmu Niangniang, is lovingly called Mu Niang by her devotees. Taoist scriptures say that at the beginning of time the Lord King of the East and then the Golden Mother were born of the primal energies, and together they govern yin and yang and nurture all things.",
 "She is the foremost of female immortals and presides over the goddesses of every realm. Legend places her palace by the Jasper Pool on Mount Kunlun, where the peaches of immortality ripen once in three thousand years. Her birthday is observed on the 3rd day of the 3rd lunar month or the 18th day of the 7th.",
 "Since her manifestation in Ji'an, Hualien, her faith has spread to nearly a thousand temples in Taiwan, where devotees call one another brother and sister."])
page("deity.html", "主神簡介", "紐約花蓮慈惠堂主神：無極瑤池大聖西王金母大天尊。", f'''
{pagehead("供奉神明","Deities","主神簡介","Principal Deity")}
<section class="gutter"><div class="container">
  <div class="prose wraptext">
    <h2 class="subhead" style="margin-top:0">{L(C.DEITY_TITLE, "The Golden Mother of the Jasper Pool")}</h2>
    {wrapimg("jinmu.jpg", "瑤池金母 The Golden Mother", "left", 200)}
    {zh_en(paras(C.DEITY), deity_en)}
    <h2 class="subhead">{L(C.BAOGAO_TITLE, "Hymn of Praise to the Golden Mother")}</h2>
    <p class="baogao">{"<br>".join(C.BAOGAO)}</p>
    <p class="muted" style="font-size:.88rem">{C.BAOGAO_NOTE}</p>
  </div>
</div></section>
{BAND}
''')

# ---------------------------------------------------------------- 堂主簡介
page("master.html", "堂主簡介", "紐約花蓮慈惠堂堂主何春燕女士。", f'''
{pagehead("本堂簡介","About","堂主簡介","Head of the Temple")}
<section class="gutter"><div class="container">
  <div class="prose wraptext">{wrapimg("master.jpg", "堂主何春燕女士 Ms. Ho Chun-Yen", "left", 200)}{zh_en(paras(C.MASTER), paras([e for z,e in MASTER]))}</div>
</div></section>
{BAND}
''')

# ---------------------------------------------------------------- 點燈祈福
taisui_table = '<div class="tablewrap"><table class="taisui"><tbody>' + "".join(
    "<tr>" + "".join(f"<td>{n}</td>" for n in C.TAISUI_LIST[i:i+3]) + "</tr>" for i in range(0, len(C.TAISUI_LIST), 3)) + "</tbody></table></div>"
LAMP_SECS = [
  ("◎太歲平安燈", "◎ Tai Sui Peace Lamp", "#356D82", paras(C.TAISUI) + f'<p><b>{C.TAISUI_LIST_TITLE}</b></p>' + taisui_table + paras(C.TAISUI_AFTER),
   "<p>Those whose zodiac sign clashes with the year's Tai Sui are advised to make offerings to Tai Sui to turn misfortune aside. The sixty Tai Sui generals are enshrined in our second-floor Tai Sui Hall, each statue made by a master artisan — the only such hall on the US East Coast.</p>"),
  ("◎個人光明燈", "◎ Personal Guangming Lamp", "#58BEEE", paras(C.GUANGMING),
   "<p>Also called the Lamp of the Original Spirit or the Everlasting Lamp, it is lit at the start of each year for good fortune and vitality. The year-end thanksgiving ceremony is held on the 20th day of the 12th lunar month, when lamps and Tai Sui offerings for the coming year begin.</p>"),
  ("◎功名文昌燈", "◎ Wenchang Success Lamp", "#4698BE", paras(C.WENCHANG),
   "<p>A Wenchang blessing rite for students and those facing examinations, asking Wenchang Dijun, Kuidou Xingjun and Confucius to open wisdom and bring success.</p>"),
  ("◎五路財神燈", "◎ Five Wealth Gods Lamp", "#89A9BE", paras('五路財神燈是向五路財神祈求財運的祈福燈。五路財神掌管東、西、南、北、中五方財路，點財神燈祈求財神護佑，廣開財源、事業順利、生意興隆。\n本堂一樓五路財神殿供奉天官賜福財神、武財神、文財神、南山通利財神、北府納庫財神。經商創業、求職工作或希望財務穩定的善信大德，都可以點財神燈祈福。'.split("\n")),
   '<p>A lamp for prosperity, lit before the Five Wealth Gods who guard the wealth of all five directions. It asks for open sources of income, a smooth career and thriving business. The Five Wealth Gods are enshrined in our first-floor Hall of the Five Wealth Gods; anyone starting a business, seeking work or hoping for financial stability is welcome to light one.</p>'),
]
page("lamps.html", "點燈祈福", "紐約花蓮慈惠堂點燈祈福：光明燈、太歲燈、文昌燈、財神燈。", f'''
{pagehead("點燈法會","Lamps & Ceremonies","點燈祈福","Lamp Lighting")}
<section class="gutter"><div class="container">
  <p class="notice" style="margin-bottom:22px">{L(C.LAMPS_INTRO, "Our Guangming, Tai Sui, Wenchang and Five Wealth Gods lamps use an LED lamp-finder system so you can easily find your own lamp.")}</p>
  <div class="grid">
    {"".join(f'<article class="card lamp"{' id="taisui"' if z=="◎太歲平安燈" else ""}>{lamp_icon(c)}<h3>{L(z,e)}</h3><div class="price">{L("每盞 $120","$120 per lamp")}</div><div class="prose">{zh_en(zh,en)}</div></article>' for z,e,c,zh,en in LAMP_SECS)}
  </div>
</div></section>

<section class="gutter" style="background:var(--paper-2)"><div class="container grid g2" style="align-items:start">
  <div>
    <ul class="facts"><li>{L(C.LAMPS_END, "For everyone holding a Tai Sui, Guangming, Wenchang or Five Wealth Gods lamp, the temple chants scriptures and presents prayers on the 1st and 15th of every lunar month.")}</li></ul>
  </div>
  <div>
    {sec("線上點燈和法會報名", "Lamp & Ceremony Registration")}
    <ol class="upcoming nums" style="list-style:none">
      <li><div class="when">1</div><div class="what">{L("線上填寫報名表，每一位可以點一盞或多盞燈（光明燈、太歲燈、財神燈、文昌燈，每盞 $120）。", "Fill in the online form. Each person can have one or more lamps ($120 each).")}</div></li>
      <li><div class="when">2</div><div class="what">{L("送出後畫面會出現繳費單，請截圖或列印。", "A payment slip appears when you submit. Save a screenshot or print it.")}</div></li>
      <li><div class="when">3</div><div class="what">{L("帶著繳費單到堂裡繳交現金，告知報名編號即可。", "Bring the slip to the temple and pay in cash.")}</div></li>
    </ol>
    <p style="margin-top:18px"><a class="cta big" href="https://nytht.vercel.app/">{L("點燈報名", "Register for a lamp")}</a></p>
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

# ---------------------------------------------------------------- 本堂設施（照樓層）
taisui_now = f"""<div class="taisui-now" id="taisuiNow" hidden>
  <div class="ts-head"><div class="label" id="tsLabel">{L("今年值年太歲","Tai Sui of This Year")}</div>
    <div class="ts-nav"><button type="button" id="tsPrev">‹ {L("上一年","Prev")}</button><button type="button" id="tsNext">{L("下一年","Next")} ›</button></div></div>
  <div class="name"><span id="tsYear"></span><b id="tsName"></b></div>
  <div class="range muted" id="tsRange"></div>
  <div class="ts-bio" id="tsBio"></div>
  <div class="ts-src muted">{L("依民間流傳之《六十甲子太歲傳略》","Based on the traditional folk biographies of the Sixty Tai Sui")}</div>
  <button type="button" class="ts-back" id="tsBack" hidden>↩ {L("回到今年","Back to this year")}</button>
</div>"""
taisui_all = '<details class="taisui-all"><summary>' + L(C.TAISUI_LIST_TITLE.rstrip("："), "The Sixty Tai Sui Generals") + '</summary><div class="tablewrap"><table class="taisui"><tbody>' + "".join(
    "<tr>" + "".join(f'<td data-gz="{n[:2]}">{n}</td>' for n in C.TAISUI_LIST[i:i+3]) + "</tr>" for i in range(0, len(C.TAISUI_LIST), 3)) + "</tbody></table></div></details>"
def hall_block(k):
    zh,en,img,dz,de = HALL_BY[k]
    extra = (taisui_now + taisui_all) if k=="taisui" else ""
    return f"""<article class="hall wraptext{' main' if k=='main' else ''}" id="{k}"><h2 style="margin-bottom:12px">{L(zh,en)}</h2>{wrapimg(img, zh+" "+en, "left", 400 if k=="main" else 320)}
    <div><div class="prose">{zh_en("<p>"+br(C.HALLS_TEXT[k])+"</p>", "<p>"+de+"</p>")}</div>
      {deity_html(k)}{extra}</div></article>"""
FLOORS = [(1,"一樓","First Floor",["main","wenchang","caishen"]),(2,"二樓","Second Floor",["taisui"]),(3,"三樓","Third Floor",["sanqing"])]
page("halls.html", "本堂設施", "紐約花蓮慈惠堂本堂設施：一樓大殿、五路財神殿、文昌帝君殿，二樓太歲殿，三樓三清殿。", f'''
{pagehead("供奉神明","Deities","本堂設施","Facilities")}
<section class="gutter"><div class="container">
  {floorplan_html()}
  {"".join(f'<div class="floorsec" id="f{n}"><h2 class="floorhead">{L(z,e)}</h2>' + "".join(hall_block(k) for k in ks) + "</div>" for n,z,e,ks in FLOORS)}
</div></section>
{BAND}
''', lunar=True)

# ---------------------------------------------------------------- 年度行事
page("calendar.html", "年度行事", "紐約花蓮慈惠堂年度行事。", f'''
{pagehead("點燈法會","Lamps & Ceremonies","年度行事","Annual Calendar")}
<section class="gutter"><div class="container">
  <h2 class="subhead" style="margin-top:0">{L(C.CAL_TITLE, "Major Annual Celebrations")}</h2>
  <div class="tablewrap"><table class="cal">
    <thead><tr><th>{L("農曆","Lunar date")}</th><th>{L("行事","Event")}</th><th>{L("2027年（丁未年）國曆日期","Dates in 2027")}</th></tr></thead>
    <tbody id="calBody"></tbody>
  </table></div>
  <div class="notice" style="margin-top:24px">{L(C.CAL_NOTE + "<br>2027年清明節為 4/5（一），重陽節為 10/8（五）。", "Every Qingming and Double Ninth Festival, the temple chants scriptures for the ancestors of all devotees. In 2027: Qingming is April 5; Double Ninth is October 8.")}</div>
  <p class="muted" style="margin-top:12px;font-size:.88rem">{L("國曆日期依農曆換算，實際法會時間以本堂公告為準。農曆十二月下旬的法會落在2028年1月。", "Western dates are converted from the lunar calendar; please confirm with the temple. Late-12th-month ceremonies fall in January 2028.")}</p>
</div></section>
{BAND}
''', lunar=True)

# ---------------------------------------------------------------- 近期文章
page("articles.html", "近期文章", "紐約花蓮慈惠堂近期文章。", f'''
{pagehead("本堂訊息","Temple News","近期文章","Recent Articles")}
<section class="gutter"><div class="container reading" style="display:grid;gap:18px">
  {"".join(f'<article class="card"><h3>{L(z,e)}</h3><time class="muted" style="font-size:.88rem">{d}</time><div class="prose"><p>{br(C.ARTICLES_TEXT[z])}</p></div></article>' for d,z,e in ARTICLES)}
</div></section>
''')
# ---------------------------------------------------------------- 常見問題
TBC = '<span class="tbc">待確認</span>'
FAQ = [
 ("來訪參拜", "Visiting", [
  ("請問慈惠堂的參拜時間是幾點到幾點？", "When can I visit?",
   "本堂每天上午 9 點到下午 4 點開放，歡迎隨時來參拜。遇到法會或過年期間，時間可能會調整，出發前可以先看看本堂公告。<br>每月農曆初一、十五中午備有平安齋，法會期間中午也有素食招待，歡迎來參拜的信眾一起用齋。",
   "We are open every day from 9:00 am to 4:00 pm, and you are welcome any time. Hours may change during ceremonies and Lunar New Year, so it is worth checking our announcements before you come.<br>A free vegetarian lunch is served on the 1st and 15th of every lunar month, and a vegetarian lunch is also offered during ceremonies; everyone who comes to worship is welcome to join."),
  ("請問慈惠堂要怎麼去？有停車位嗎？", "How do I get there? Is there parking?",
   '本堂在皇后區大學點，地址是 <span data-address></span>，地圖和交通方式都整理在<a href="contact.html">聯絡資訊</a>。<br>堂裡沒有自己的停車場，開車來的話，麻煩停在附近的路邊。',
   'We are in College Point, Queens, at <span data-address></span>. You will find a map on our <a href="contact.html">Contact &amp; Directions</a> page.<br>We do not have our own parking lot, so if you drive, please park on the street nearby.'),
  ("第一次到慈惠堂參拜，請問該怎麼拜？", "It's my first visit and I'm not sure what to do.",
   '別擔心，照著順序走就可以了。<br>進門後先到祭改處左側取三枝香、點香，接著依序參拜大殿、文昌帝君殿、五路財神殿。從出口出去後，在外廊主爐和前庭天公爐各插一枝香，再回到室內，上二樓太歲殿、三樓三清殿參拜，最後一枝香插在三樓外廊的香爐。<br>全程一共三枝香，記得右側入口進、左側出口出。<a href="halls.html">參拜順序</a>有圖可以對照。',
   'Don\'t worry — just follow the route. Take three incense sticks to the left of the Jigai desk and light them, then pay respects in the Main Hall, the Hall of Wenchang and the Hall of the Five Wealth Gods. Leave by the exit and place one stick each in the main burner on the veranda and the Heaven burner in the front yard. Come back inside, go up to the Tai Sui Hall on the second floor and the Hall of the Three Pure Ones on the third, and place your last stick in the burner on the third-floor veranda.<br>That is three sticks in all; enter on the right and exit on the left. Our <a href="halls.html">order of worship</a> has a floor plan you can follow.'),
  ("請問參拜需要自己準備香、供品或金紙嗎？", "Do I need to bring incense, offerings or joss paper?",
   "香不用帶，堂裡免費提供，在祭改處左側就可以取用。<br>供品和鮮花可以自己準備，供品建議以素菜為主，拜完之後建議帶回家。<br>金紙可以在櫃檯購買。",
   "No need to bring incense — it is free, and you can pick it up to the left of the Jigai desk.<br>You are welcome to bring your own offerings and flowers. We suggest vegetarian food for offerings, and taking them home afterwards.<br>Joss paper is available at the front desk."),
  ("請問堂內可以拍照嗎？", "May I take photos?",
   "可以的，歡迎拍照留念。", "Yes, you are welcome to take photos."),
  ("不太會說中文，請問有英文服務嗎？", "I don't speak much Chinese. Will that be a problem?",
   "網站右上角按「English」就能切換成英文。現場是否有人能用英文協助，要看當天值班的人員。",
   "This website is available in English (top right). Whether someone can help you in English at the temple depends on who is on duty that day."),
 ]),
 ("點燈與安太歲", "Lamps & Tai Sui", [
  ("請問怎麼知道自己今年是否「犯太歲」？", "How do I know if I clash with this year's Tai Sui?",
   '生肖和當年的值年太歲相同，叫「值太歲」；相沖的，叫「沖太歲」。依民間習俗，這兩種情況都建議安奉太歲，祈求一整年平安順利。<br>今年的值年太歲可以到<a href="halls.html#taisui">本堂設施・太歲殿</a>查看，想點太歲燈請看<a href="lamps.html#taisui">點燈祈福</a>。',
   'If your zodiac sign is the same as the year\'s Tai Sui, or directly opposite it, tradition suggests lighting a Tai Sui lamp for a safe and smooth year.<br>You can look up this year\'s Tai Sui under <a href="halls.html#taisui">Tai Sui Hall</a>, and read about the lamp under <a href="lamps.html#taisui">Lamp Lighting</a>.'),
  ("請問可以幫家人點燈嗎？需要準備哪些資料？", "Can I light lamps for my family? What do I need?",
   "可以的。一張報名表可以填同一個住址的家人，每個人可以點一盞或多盞燈，每盞 $120。<br>報名前請先準備好每一位的姓名和生日，農曆、國曆都可以。",
   "Yes. One form covers family members living at the same address, and each person can have one or more lamps ($120 each).<br>Before you start, please have each person's name and birthday ready — lunar or Western is fine."),
  ("點燈之後，慈惠堂會為點燈的信眾做些什麼？", "What does the temple do for me after I light a lamp?",
   "凡是點了太歲燈、光明燈、文昌燈或財神燈的信眾，本堂每個月農曆初一、十五都會誦經上疏，為大家祈福。",
   "On the 1st and 15th of every lunar month, we chant scriptures and present prayers for everyone who has a Tai Sui, Guangming, Wenchang or Five Wealth Gods lamp."),
 ]),
 ("法會", "Ceremonies", [
  ("請問慈惠堂的法會什麼時候舉行？", "When are the ceremonies held?",
   '全年的法會都列在<a href="calendar.html">年度行事</a>。上面的國曆日期是依農曆換算的，實際時間還是以本堂公告為準；最新消息可以看<a href="news.html">最新活動</a>或本堂 Facebook。',
   'The whole year is listed in our <a href="calendar.html">Annual Calendar</a>. The Western dates there are converted from the lunar calendar, so please check <a href="news.html">Latest Events</a> or our Facebook page for confirmed times.'),
  ("請問超渡法會可以為哪些對象報名？本人一定要到場嗎？", "Who can I register for the Deliverance Ceremony? Do I have to attend?",
   "歷代祖先、往生親友、冤親債主、地基主、嬰靈（水子靈）都可以報名超渡，每個牌位 $160。<br>法會當天下午有解冤釋結儀式，報名的人需要到場祭改；真的沒辦法來的話，可以準備一件自己的衣物，請家人或朋友代為祭改。",
   "You may register ancestors, departed family and friends, karmic creditors, land spirits and unborn children ($160 per tablet).<br>There is a purification rite in the afternoon, and those who register should be there for it. If you really cannot come, a family member or friend may bring a piece of your clothing and take part on your behalf."),
 ]),
 ("報名與樂捐", "Registration & Donations", [
  ("請問點燈和法會要怎麼報名、怎麼繳費？", "How do I register and pay?",
   '點燈和法會都可以<a href="https://nytht.vercel.app/">線上報名</a>。送出之後畫面會出現繳費單，請截圖或列印下來，帶到堂裡繳交現金就完成了。<br>不方便上網的話，也可以打電話登記：<span data-tel class="nowrap"></span>。',
   'You can register for lamps and ceremonies <a href="https://nytht.vercel.app/">online</a>. A payment slip appears when you submit; save a screenshot or print it, bring it to the temple and pay in cash, and you are done.<br>If you would rather not register online, you can also call us: <span data-tel class="nowrap"></span>.'),
  ("想樂捐、添油香，請問該怎麼做？", "How can I make a donation?",
   "感謝您的心意。目前可以用現金或支票，線上付款還在規劃中。<br>另外，本堂正在募集廟頂瓦片修繕的樂捐，每片 $50，歡迎一起護持。",
   "Thank you for your kindness. We currently accept cash and checks; online payment is being planned.<br>We are also raising funds to restore the temple's roof tiles ($50 per tile), and your support is very welcome."),
 ]),
]
FAQ_HTML = "".join(
  f'<h2 class="faq-cat">{L(cz,ce)}</h2><div class="faq">'
  + "".join(f'<details><summary>{L(qz,qe)}</summary><div class="a">{L(az,ae)}</div></details>' for qz,qe,az,ae in items)
  + '</div>' for cz,ce,items in FAQ)
page("faq.html", "常見問題", "紐約花蓮慈惠堂常見問題：開放時間、參拜方式、點燈報名、法會。", f"""
{pagehead("聯繫本堂","Contact Us","常見問題","FAQ")}
<section class="gutter"><div class="container reading">
  {FAQ_HTML}
</div></section>
{{BAND}}
""".replace("{BAND}", BAND))

print("ok")
