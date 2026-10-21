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
g = {"__file__": os.path.join(HERE, "build3.py"), "C": C}
exec(compile(src, "build3.py", "exec"), g)
L, B, P, ph, page, pagehead, sec, BAND, lamp_icon = (g[k] for k in ["L","B","P","ph","page","pagehead","sec","BAND","lamp_icon"])
HALLS, HALL_KEYS, HALL_DEITIES, ARTICLES, MASTER = g["HALLS"], g["HALL_KEYS"], g["HALL_DEITIES"], g["ARTICLES"], g["MASTER"]

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
{pagehead("本堂簡介","About","主神簡介","Principal Deity")}
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
  ("◎安太歲", "◎ Tai Sui", "#356D82", paras(C.TAISUI) + f'<p><b>{C.TAISUI_LIST_TITLE}</b></p>' + taisui_table + paras(C.TAISUI_AFTER),
   "<p>Those whose zodiac sign clashes with the year's Tai Sui are advised to make offerings to Tai Sui to turn misfortune aside. The sixty Tai Sui generals are enshrined in our second-floor Tai Sui Hall, each statue made by a master artisan — the only such hall on the US East Coast.</p>"),
  ("◎光明燈", "◎ Guangming Lamp", "#58BEEE", paras(C.GUANGMING),
   "<p>Also called the Lamp of the Original Spirit or the Everlasting Lamp, it is lit at the start of each year for good fortune and vitality. The year-end thanksgiving ceremony is held on the 20th day of the 12th lunar month, when lamps and Tai Sui offerings for the coming year begin.</p>"),
  ("◎文昌光明燈", "◎ Wenchang Lamp", "#4698BE", paras(C.WENCHANG),
   "<p>A Wenchang blessing rite for students and those facing examinations, asking Wenchang Dijun, Kuidou Xingjun and Confucius to open wisdom and bring success.</p>"),
]
page("lamps.html", "點燈祈福", "紐約花蓮慈惠堂點燈祈福：安太歲、光明燈、文昌光明燈。", f'''
{pagehead("本堂訊息","Temple News","點燈祈福","Lamp Lighting")}
<section class="gutter"><div class="container">
  <p class="notice" style="margin-bottom:22px">{L(C.LAMPS_INTRO, "Our Guangming, Tai Sui, Wenchang and Five Wealth Gods lamps use an LED lamp-finder system so you can easily find your own lamp.")}</p>
  <div class="grid">
    {"".join(f'<article class="card lamp">{lamp_icon(c)}<h3>{L(z,e)}</h3><div class="price">{L("每盞 $120","$120 per lamp")}</div><div class="prose">{zh_en(zh,en)}</div></article>' for z,e,c,zh,en in LAMP_SECS)}
  </div>
</div></section>

<section class="gutter" style="background:var(--paper-2)"><div class="container grid g2" style="align-items:start">
  <div>
    <ul class="facts"><li>{L(C.LAMPS_END, "For everyone holding a Tai Sui offering, Guangming or Wenchang lamp, the temple chants scriptures and presents prayers on the 1st and 15th of every lunar month.")}</li></ul>
  </div>
  <div>
    {sec("線上點燈和法會報名", "Lamp & Ceremony Registration")}
    <ol class="upcoming nums" style="list-style:none">
      <li><div class="when">1</div><div class="what">{L("線上填寫報名表，每一位可以點一盞或多盞燈（個人光明燈、太歲燈、五路財神燈、文昌燈，每盞 $120）。", "Fill in the online form. Each person can have one or more lamps ($120 each).")}</div></li>
      <li><div class="when">2</div><div class="what">{L("送出後畫面會出現繳費單，請截圖或列印。", "A payment slip appears when you submit. Save a screenshot or print it.")}</div></li>
      <li><div class="when">3</div><div class="what">{L("帶著繳費單到堂裡繳交現金，告知報名編號即可。", "Bring the slip to the temple and pay in cash.")}</div></li>
    </ol>
    <p style="margin-top:18px"><a class="cta big" href="signup.html#lamp">{L("點燈報名", "Register for a lamp")}</a></p>
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
  <p style="margin-top:18px"><a class="cta" href="signup.html">{L("法會報名","Register for a ceremony")}</a></p>
</div></section>
''')

# ---------------------------------------------------------------- 本堂設施
page("halls.html", "本堂設施", "紐約花蓮慈惠堂本堂設施：大殿、文昌帝君殿、五路財神殿、太歲殿、三清殿。", f'''
{pagehead("","","本堂設施","Facilities")}
<section class="gutter"><div class="container">
  {"".join(f"""<article class="hall wraptext" id="{k}"><h2 style="margin-bottom:12px">{L(zh,en)}</h2>{wrapimg(img, zh+" "+en, "left", 400)}
    <div><div class="prose">{zh_en("<p>"+br(C.HALLS_TEXT[k])+"</p>", "<p>"+de+"</p>")}</div>
      <ul class="deities">{"".join(f"<li>{L(a,b)}</li>" for a,b in HALL_DEITIES[k])}</ul></div></article>""" for k,(zh,en,img,dz,de) in zip(HALL_KEYS, HALLS))}
</div></section>
{BAND}
''')

# ---------------------------------------------------------------- 年度行事
page("calendar.html", "年度行事", "紐約花蓮慈惠堂年度行事。", f'''
{pagehead("本堂訊息","Temple News","年度行事","Annual Calendar")}
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
{pagehead("","","近期文章","Recent Articles")}
<section class="gutter"><div class="container reading" style="display:grid;gap:18px">
  {"".join(f'<article class="card"><h3>{L(z,e)}</h3><time class="muted" style="font-size:.88rem">{d}</time><div class="prose"><p>{br(C.ARTICLES_TEXT[z])}</p></div></article>' for d,z,e in ARTICLES)}
</div></section>
''')
print("ok")
