#!/usr/bin/env python3
"""紐約花蓮慈惠堂網站（照舊網站分頁與標題重建）。共用頁首頁尾由 assets/app.js 注入。"""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web2")

def L(zh, en): return f'<span class="zh">{zh}</span><span class="en">{en}</span>'
def P(zh, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c}><span class="zh">{zh}</span><span class="en">{en}</span></p>'
def ph(src, zh, en, cls=""):
    return f'<figure class="ph {cls}" data-label="{zh}"><img src="images/{src}" alt="{zh} {en}" loading="lazy"></figure>'
DRAFT = '<div class="draftnote">' + L("預覽說明：本頁內文是依舊網站內容暫時整理的版本，請提供舊網站原文替換。（上線前會移除這個提示）",
                                       "Preview note: this text is a temporary summary of the old site; it will be replaced with the original wording.") + '</div>'

def page(fname, tzh, desc, body):
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
<script src="assets/app.js"></script>
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

def head(zh, en):
    return f'<section class="pagehead gutter"><div class="container"><h1>{L(zh,en)}</h1></div></section>'

# ---------------------------------------------------------------- 原文與資料
HISTORY = [
 ("紐約花蓮慈惠堂成立於1991年，由何俊忠居士創辦，老堂主何游阿粉女士十幾年的耕耘，再由現任的堂主何春燕接任後，才有今日的莊嚴道場。",
  "New York Hua Lian Tsu Hui Temple was founded in 1991 by Mr. Ho Chun-Chung. After more than ten years of devoted work by the former head, Mrs. Ho Yu A-Fen, leadership passed to the current head, Ms. Ho Chun-Yen, under whom the temple has become the dignified place of worship it is today."),
 ("創堂初期，何俊忠居士於紐約法拉盛羅斯福路開堂設教，弘揚聖命，金母賜名「紐約花蓮慈惠堂」。母娘慈恩濟世，受惠信眾口耳相傳，四方慕德投歸法座的信眾紛至沓來，與日俱增，西元2002年乃遷至法拉盛大學點大道，不旋踵。西元2007年金母揮鸞指示「盡早興建宗教文化道場，舉辦社會公益活動」，是時立願效勞和隨修信徒眾多，聞訊四出尋訪，終在2008年在母娘顯靈與貴人張善良先生結緣下尋得一寶地於大學點龍頭地段有片空地，正是金母靈示之建廟用地，得信徒鼎力捐輸，福蒙金母神威之福應，終於購下這片土地。",
  "In its early days, Mr. Ho Chun-Chung opened the temple on Roosevelt Avenue in Flushing to spread the Mother's teachings, and the Golden Mother named it New York Hua Lian Tsu Hui Temple. As word of the Mother's compassion spread, devotees came from all directions in growing numbers, and in 2002 the temple moved to College Point Boulevard. In 2007 the Golden Mother instructed, through divine writing, that a religious and cultural center be built as soon as possible and that the temple hold charitable activities for the community. Many devotees vowed to help and searched far and wide. In 2008, through the Mother's manifestation and a fortunate meeting with Mr. Chang Shan-Liang, they found a vacant lot at a prime location in College Point — the very site the Golden Mother had indicated. With the devotees' generous donations and the Mother's blessing, the land was purchased."),
 ("只是，2009年建堂之初，困難重重和外來的壓力，和美國工程學上的種種規定和申請上的困難，在母娘的顯靈下突然來了一位建商Peter Chen聞建廟之聲，一呼百應，在Peter Chen的帶領下，立刻開工破土正式動土興工，擇善固執、外柔內剛的何堂主自感肩負重任，日日親自帶領師兄師姐看守廟地，她視建廟乃是一種信心的考驗與殊榮，這種為芸芸眾生創設靈修聖地而不畏艱難的精神贏得眾多信徒效法，皆抱以感恩、回饋的真情，承受辛苦而無怨無悔。",
  "When construction began in 2009, the temple faced many obstacles: outside pressure, American engineering regulations and a difficult permit process. Then, through the Mother's manifestation, a builder named Peter Chen heard of the project and answered the call. Under his leadership ground was broken and construction began. Ms. Ho, gentle in manner but firm in resolve, felt the weight of this responsibility and led the brothers and sisters every day in watching over the site. She saw building the temple as both a test of faith and an honor, and her determination to create a sacred place for all people, whatever the hardship, inspired many devotees, who gave their gratitude and effort without complaint."),
 ("誠如母娘諭示「關關難過關關過」，集何堂主與信眾一心之努力，本堂興建工程終於完竣，並於西元2012年國曆6月13日（農曆4月24日）入廟，舉辦　瑤池金母安座大典，完成一所在美東唯一的東方建築的宗教聖殿，同時樹立一所啟迪世人智慧，承神恩無遠弗屆，信仰功果均霑濡，九生十類皆受惠。",
  "As the Mother taught, “every barrier is hard, yet every barrier is passed.” Through the united effort of Ms. Ho and the devotees, construction was completed, and on June 13, 2012 (the 24th day of the 4th lunar month) the temple held the enthronement ceremony of the Golden Mother of the Jasper Pool — completing the only sacred hall of traditional Eastern architecture on the US East Coast, a place to enlighten the world, through which divine grace reaches far and all living beings receive its blessing."),
 ("位居皇后區大學點上的紐約花蓮慈惠堂坐擁城市都會中為一絕佳的地理福地。",
  "Located in College Point, Queens, the temple enjoys an exceptionally auspicious site in the heart of the city."),
 ("依台灣名師設計而建的紐約花蓮慈惠堂雄偉壯觀，殿脊銅瓦覆頂，脊昂高翅，在中更顯富麗莊嚴，靈氣十足，拾級而上，爐煙觸目，清香四溢，讓人一洗風塵，實有絕殊離俗之感。",
  "Designed by a renowned Taiwanese master, the temple is grand and majestic, its ridges roofed in bronze tiles with soaring upturned eaves, rich, solemn and full of spiritual energy. Climbing the steps, one sees incense smoke rising and smells its fragrance — the dust of the world falls away, and one feels truly removed from the ordinary."),
]
NEWS = [
 ("09/17/2017", "5/20 紐約花蓮慈惠堂堂慶,謝金燕嘉賓演出!", "5/20 Temple Anniversary Celebration with guest performer Jeannie Hsieh"),
 ("11/01/2016", "無上虛空地母娘娘聖誕", "Birthday of the Earth Mother"),
 ("07/26/2016", "2016 瑤池金母文化節", "2016 Golden Mother Cultural Festival"),
 ("12/23/2015", "紐約花蓮慈惠堂歲末年終感恩餐會", "Year-end Thanksgiving Dinner"),
 ("11/14/2015", "恭逢地母慈尊生日活動慶典", "Celebration of the Earth Mother's Birthday"),
 ("08/20/2013", "瑤池金母文化節", "Golden Mother Cultural Festival"),
 ("03/19/2013", "啟建朝真禮斗法會", "Chao Zhen Li Dou Ceremony"),
]
ARTICLES = [
 ("12/03/2012", "因緣", "Karmic Affinity"),
 ("11/06/2012", "七星鎮宅平安符", "Seven-Star House Protection Talisman"),
 ("10/29/2012", "開光問題", "About Consecration"),
]
FBV = "https://www.facebook.com/119659741440606/videos/"
VIDEOS = [
 ("文化節記者會之一", "Cultural Festival press conference (1)", "913037432102829"),
 ("2015紐約臺灣文化節民俗演出", "2015 NY Taiwanese Cultural Festival folk performance", "884469004959672"),
 ("2015紐約臺灣文化節演出", "2015 NY Taiwanese Cultural Festival performance", "884467854959787"),
 ("母娘出巡歌曲由名歌手彭莉演唱", "Procession song performed by singer Peng Li", "855133461226560"),
]
GALLERY_MORE = [
 ("母娘文化季系列之一", "Mu Niang Cultural Season (1)"),
 ("皇后藝術館表演", "Performance at the Queens Museum"),
 ("應印度廟邀請表演於皇后藝術館內", "Performance at the Queens Museum at the invitation of a Hindu temple"),
 ("大年初四舞獅拜年", "Lion dance on the 4th day of Lunar New Year"),
 ("舞蹈團新春表演前排舞", "Dance troupe rehearsing for the New Year performance"),
 ("慈惠堂母娘聖誕-文化節 美女群練舞中", "Golden Mother's Birthday Cultural Festival — dancers rehearsing"),
]
CAL = [
 ("農曆一月九日", "玉皇上帝聖誕 (點太歲、光明燈)", "1st month, day 9", "Birthday of the Jade Emperor (Tai Sui and Guangming lamps)"),
 ("農曆二月上旬", "春季祈安禮斗法會", "Early 2nd month", "Spring Li Dou Blessing Ceremony"),
 ("農曆二月十六日", "花蓮晉香 (聖地之旅)", "2nd month, day 16", "Pilgrimage to Hualien (journey to the holy site)"),
 ("農曆二月十九日", "觀世音菩薩聖誕", "2nd month, day 19", "Birthday of Guanyin Bodhisattva"),
 ("農曆三月二三日", "天上聖母聖誕", "3rd month, day 23", "Birthday of Mazu"),
 ("農曆六月三日", "蟠桃聖會", "6th month, day 3", "Peach Banquet Festival"),
 ("農曆六月七日", "開天門消災法會", "6th month, day 7", "Opening of Heaven's Gate Ceremony"),
 ("農曆七月十八日", "瑤池金母聖誕", "7th month, day 18", "Birthday of the Golden Mother of the Jasper Pool"),
 ("農曆七月十九～二十日", "超渡法會", "7th month, days 19–20", "Deliverance Ceremony"),
 ("農曆九月九日", "斗姆元君聖誕", "9th month, day 9", "Birthday of Doumu Yuanjun"),
 ("農曆九月九日", "中壇元帥聖誕", "9th month, day 9", "Birthday of Marshal Zhongtan"),
 ("農曆九月", "秋季祈安禮斗法會", "9th month", "Autumn Li Dou Blessing Ceremony"),
 ("農曆十月十八日", "地母元君聖誕", "10th month, day 18", "Birthday of the Earth Mother"),
 ("農曆十一月十一日", "太乙救苦天尊聖誕", "11th month, day 11", "Birthday of Taiyi Jiuku Tianzun"),
 ("農曆十二月下旬", "謝太歲、光明燈、謝平安法會", "Late 12th month", "Year-end thanksgiving ceremony for Tai Sui and lamps"),
]
HALLS = [
 ("大殿", "Main Hall", "hall-main.jpg",
  "中央無極聖殿奉祀主神無極瑤池大聖西王金母大天尊，右側奉祀玄穹高上帝玉皇赦罪賜福大天尊，左側奉祀無上虛空地母無量慈尊。神龕前同祀觀音大士、關聖帝君、天上聖母、中壇元帥與福德正神等諸位神明。",
  "At the center the principal deity, the Golden Mother of the Jasper Pool, is enshrined; to the right is the Jade Emperor and to the left the Earth Mother. Before the altar are Guanyin, Guan Di, Mazu, Marshal Zhongtan and the Earth God, among others."),
 ("文昌帝君殿", "Hall of Wenchang", "hall-wenchang.jpg",
  "奉祀文昌帝君、魁斗星君與大成至聖先師，另配祀天聾、地啞二聖。",
  "Dedicated to Wenchang Dijun, Kuidou Xingjun and Confucius, with the attendants Tianlong and Diya."),
 ("月老神君", "Yue Lao", "hall-yuelao.jpg",
  "月老神君供奉於文昌殿前方，主掌人間姻緣。",
  "Yue Lao, the Old Man under the Moon, is enshrined in front of the Wenchang altar and watches over love and marriage."),
 ("五路財神殿", "Hall of the Five Wealth Gods", "hall-caishen.jpg",
  "奉祀天官大帝、文財神范蠡、武財神趙公明、南山通利仙官石崇、北府納庫仙官沈萬山，另有招財、進寶二位童子。",
  "Dedicated to the Heavenly Official and the gods of wealth Fan Li, Zhao Gongming, Shi Chong and Shen Wanshan, with the attendants Zhaocai and Jinbao."),
 ("太歲殿", "Tai Sui Hall", "hall-taisui.jpg",
  "位於二樓，奉祀斗姆元君與六十甲子太歲星君，為美東唯一的太歲殿。",
  "On the second floor, home of Doumu Yuanjun and the sixty Tai Sui generals — the only Tai Sui hall on the US East Coast."),
 ("三清殿", "Hall of the Three Pure Ones", "hall-sanqing.jpg",
  "位於三樓，奉祀三清道祖：元始天尊、靈寶天尊、太上道祖。",
  "On the third floor, dedicated to the Three Pure Ones: Yuanshi Tianzun, Lingbao Tianzun and Daode Tianzun."),
]
MASTER = [
 ("堂主何春燕女士出生於台灣宜蘭縣羅東鎮，家境小康。父親是畫家，母親是虔誠的媽祖信徒，自幼受父母教誨，立身處世講求篤信與堅實。",
  "Ms. Ho Chun-Yen was born in Luodong, Yilan County, Taiwan. Her father was a painter and her mother a devout follower of Mazu, and she was raised to value sincerity and steadiness."),
 ("年輕時赴美，長期在大哥經營的毛衣工廠工作。後因弟弟何俊忠居士因緣際會結識瑤池金母，開啟她的宗教因緣。她依母教法規，以青衣素食自持，效法母娘降世的本願。",
  "She came to the United States as a young woman and worked for many years at her elder brother's sweater factory. When her younger brother, Mr. Ho Chun-Chung, came to know the Golden Mother, her own spiritual path began. Following the Mother's teaching, she keeps to the blue robes and a vegetarian life."),
 ("她常帶領師兄師姐回台朝聖，並在松山慈惠堂郭葉子女士帶領下，與各大廟宇交流、廣結善緣。",
  "She often leads members on pilgrimages to Taiwan and, guided by Ms. Kuo Yeh-Tzu of Songshan Tsu Hui Tang, has built friendships with many temples."),
]

def postlist(items, link=None):
    return '<ul class="postlist">' + "".join(
        f'<li><b>{L(z,e)}</b><time>{d}</time></li>' for d,z,e in items) + '</ul>'

# ---------------------------------------------------------------- 首頁（照舊網站區塊順序）
index_body = f'''
<section class="banner">{ph("temple.jpg", "紐約花蓮慈惠堂", "New York Hua Lian Tsu Hui Temple")}</section>

<section class="gutter" style="padding-block:28px;background:var(--red-deep);color:#F6E9D2"><div class="container" style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between">
  {P("點燈、法會可以線上報名，送出後帶繳費單到堂裡繳交現金。", "Register online for lamps and ceremonies, then bring your payment slip to the temple.")}
  <div style="display:flex;flex-wrap:wrap;gap:10px"><a class="cta" style="background:var(--gold-bright);color:#2A1A08" href="https://nytht.vercel.app/#lamp">{L("點燈報名","Lamp lighting")}</a><a class="cta ghost" style="color:#F6E9D2;border-color:rgba(246,233,210,.5)" href="https://nytht.vercel.app/">{L("法會報名","Ceremonies")}</a></div>
</div></section>

<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading">
    <h2 class="sec-title">{L("紐約花蓮慈惠堂由來","Our History")}</h2>
    <div class="prose">{P(*HISTORY[0])}</div>
    <a class="readmore" href="history.html">{L("閱讀更多 》》","Read more 》》")}</a>
  </div>
  <div class="reading">
    <h2 class="sec-title">{L("堂主簡介","Head of the Temple")}</h2>
    <div class="prose">{P(*MASTER[0])}</div>
  </div>
</div></section>

<section class="gutter" style="background:var(--paper-2)"><div class="container">
  <h2 class="sec-title">{L("活動信息","Events")}</h2>
  {postlist(NEWS[:4])}
</div></section>

<section class="gutter"><div class="container">
  <h2 class="sec-title">{L("活動剪影","Gallery")}</h2>
  <ul class="postlist">{"".join(f'<li><a href="{FBV}{vid}/" target="_blank" rel="noopener"><b>{L(z,e)}</b></a><time>Facebook</time></li>' for z,e,vid in VIDEOS)}</ul>
  <a class="readmore" href="gallery.html">{L("查看更多影音 》》","More videos 》》")}</a>
</div></section>
'''
page("index.html", "首頁", "紐約花蓮慈惠堂 New York Hua Lian Tsu Hui Temple", index_body)

# ---------------------------------------------------------------- 主神簡介
deity_body = f'''
{head("主神簡介","Principal Deity")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading prose">
    {DRAFT}
    {P("瑤池金母又稱西王母、王母娘娘、金母元君，信眾尊稱「母娘」。依道教典籍記載，太古之初先化生東王木公，再化生金母，二者共理陰陽二氣，養育天地萬物。",
       "The Golden Mother of the Jasper Pool, also called Xiwangmu or Wangmu Niangniang, is lovingly called Mu Niang by her devotees. Taoist scriptures say that at the beginning of time the Lord King of the East and then the Golden Mother were born of the primal energies, and together they govern yin and yang and nurture all things.")}
    {P("金母為女仙之首，統領三界十方女神。傳說她居於崑崙瑤池，池畔蟠桃三千年一熟，因而有蟠桃盛會、群仙祝壽的典故，也被視為長壽的象徵。聖誕為農曆七月十八日（亦有三月初三之說）。",
       "She is the foremost of female immortals and presides over the goddesses of every realm. Legend places her palace by the Jasper Pool on Mount Kunlun, where the peaches of immortality ripen once in three thousand years — the origin of the Peach Banquet and of her role as a symbol of long life. Her birthday is the 18th day of the 7th lunar month (some traditions observe the 3rd day of the 3rd month).")}
    {P("自金母聖鸞降駕花蓮吉安後，信仰在台灣迅速發展，以慈惠堂、勝安宮、瑤池宮、王母宮等為名的宮堂近千間，信眾彼此以師兄、師姐相稱。",
       "Since her manifestation in Ji'an, Hualien, her faith has spread across Taiwan to nearly a thousand temples named Tsu Hui Tang, Sheng An Gong, Yao Chi Gong and Wang Mu Gong, where devotees call one another brother and sister.")}
    <h2 class="subhead">{L("無極瑤池大聖西王金母寶誥　志心皈命禮","Hymn of Praise to the Golden Mother")}</h2>
    <div class="draftnote">{L("寶誥原文待補。","Original text to be added.")}</div>
  </div>
  {ph("jinmu.jpg", "瑤池金母", "The Golden Mother", "tall")}
</div></section>
'''
page("deity.html", "主神簡介", "紐約花蓮慈惠堂主神：無極瑤池大聖西王金母大天尊。", deity_body)

# ---------------------------------------------------------------- 紐約花蓮慈惠堂由來（原文）
history_body = f'''
{head("紐約花蓮慈惠堂由來","Our History")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading prose">{"".join(P(z,e) for z,e in HISTORY)}</div>
  {ph("temple.jpg", "紐約花蓮慈惠堂", "The temple")}
</div></section>
'''
page("history.html", "紐約花蓮慈惠堂由來", "紐約花蓮慈惠堂的由來：1991 年創立，2012 年於大學點新堂舉行瑤池金母安座大典。", history_body)

# ---------------------------------------------------------------- 堂主簡介
master_body = f'''
{head("堂主簡介","Head of the Temple")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading prose">{DRAFT}{"".join(P(z,e) for z,e in MASTER)}</div>
  {ph("master.jpg", "堂主", "Ms. Ho Chun-Yen", "tall")}
</div></section>
'''
page("master.html", "堂主簡介", "紐約花蓮慈惠堂堂主何春燕女士簡介。", master_body)

# ---------------------------------------------------------------- 最新活動
page("news.html", "最新活動", "紐約花蓮慈惠堂最新活動。", f'''
{head("最新活動","Latest Events")}
<section class="gutter"><div class="container reading">{postlist(NEWS)}
  <p style="margin-top:18px"><a class="cta" data-fb href="#" target="_blank" rel="noopener">{L("Facebook 粉絲專頁","Facebook page")}</a></p></div></section>
''')

# ---------------------------------------------------------------- 年度行事
page("calendar.html", "年度行事", "紐約花蓮慈惠堂年度行事。", f'''
{head("年度行事","Annual Calendar")}
<section class="gutter"><div class="container">
  <div class="tablewrap"><table class="cal2"><tbody>
  {"".join(f'<tr><td>{L(a,c)}</td><td>{L(b,d)}</td></tr>' for a,b,c,d in CAL)}
  </tbody></table></div>
  {P("本堂每於清明節、重陽節特為眾信士之九玄七祖誦經祭拜。", "Every Qingming and Double Ninth Festival, the temple chants scriptures for the ancestors of all devotees.", "notice")}
</div></section>
''')

# ---------------------------------------------------------------- 點燈祈福
page("lamps.html", "點燈祈福", "紐約花蓮慈惠堂點燈祈福：安太歲、光明燈、文昌光明燈。", f'''
{head("點燈祈福","Lamp Lighting")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <div class="reading prose">
    {DRAFT}
    <h2 class="subhead" style="margin-top:0">{L("◎安太歲","◎ Tai Sui")}</h2>
    {P("太歲為值年神祇。生肖與當年太歲正沖或對沖者，宜安奉太歲，祈求化險為夷，避除三災九橫之厄。本堂於二樓太歲殿供奉六十甲子太歲星君，為美東唯一的星辰殿。",
       "Tai Sui is the deity presiding over each year. Those whose zodiac sign clashes with the year's Tai Sui are advised to make offerings to Tai Sui, to turn misfortune aside. The sixty Tai Sui generals are enshrined in our second-floor Tai Sui Hall, the only one on the US East Coast.")}
    <h2 class="subhead">{L("◎光明燈","◎ Guangming Lamp")}</h2>
    {P("人的本命元神不生不滅，故光明燈又稱元神燈、長明燈、無盡燈。點燈祈求運勢亨通、精神昂揚，慈光普照、破除黑暗。每年農曆十二月二十日舉行謝平安法會，並啟點翌年光明燈及安奉太歲。",
       "One's original spirit is never born and never dies, so this lamp is also called the Lamp of the Original Spirit or the Everlasting Lamp. It is lit for good fortune and vitality. On the 20th day of the 12th lunar month the year-end thanksgiving ceremony is held and lamps and Tai Sui offerings for the coming year begin.")}
    <h2 class="subhead">{L("◎文昌光明燈","◎ Wenchang Lamp")}</h2>
    {P("文昌消災保運法，專為參加考試者設立，由文昌星君及南斗賢良司共同護佑，開啟智慧、增進考運，助學子金榜題名。",
       "A Wenchang blessing rite for those facing examinations, under the protection of Wenchang and the Southern Dipper, to open wisdom and bring success in exams.")}
    {P("凡安奉太歲、點光明燈、文昌光明燈的信眾，本堂於每月農曆初一、十五誦經上疏。本堂光明燈、太歲燈、文昌燈、五路財神燈採用LED電腦尋燈系統。",
       "For everyone holding a Tai Sui offering or lamp, the temple chants scriptures and presents prayers on the 1st and 15th of every lunar month. Our Guangming, Tai Sui, Wenchang and Five Wealth Gods lamps use an LED lamp-finder system.")}
  </div>
  <div class="card" style="gap:12px">
    <h2 class="sec-title" style="margin:0">{L("線上點燈和法會報名","Lamp & Ceremony Registration")}</h2>
    {P("個人光明燈、太歲燈、五路財神燈、文昌燈，每盞 $120。送出後帶繳費單到堂裡繳交現金。",
       "Guangming, Tai Sui, Five Wealth Gods and Wenchang lamps, $120 each. Bring the payment slip to the temple and pay in cash.", "muted")}
    <a class="cta big" href="https://nytht.vercel.app/#lamp">{L("點燈報名","Register for a lamp")}</a>
    {P("也可以來電登記：", "You may also register by phone: ", "muted")}<p><span data-tel></span></p>
  </div>
</div></section>
''')

# ---------------------------------------------------------------- 本堂設施
page("halls.html", "本堂設施", "紐約花蓮慈惠堂本堂設施：大殿、文昌帝君殿、月老神君、五路財神殿、太歲殿、三清殿。", f'''
{head("本堂設施","Facilities")}
<section class="gutter"><div class="container">
  {DRAFT}
  {"".join(f'<article class="hall">{ph(img,zh,en)}<div><h2>{L(zh,en)}</h2>{P(dz,de,"prose")}</div></article>' for zh,en,img,dz,de in HALLS)}
</div></section>
''')

# ---------------------------------------------------------------- 活動剪影
page("gallery.html", "活動剪影", "紐約花蓮慈惠堂活動剪影。", f'''
{head("活動剪影","Gallery")}
<section class="gutter"><div class="container reading">
  <ul class="postlist">
    {"".join(f'<li><a href="{FBV}{vid}/" target="_blank" rel="noopener"><b>{L(z,e)}</b></a><time>Facebook</time></li>' for z,e,vid in VIDEOS)}
    {"".join(f'<li><b>{L(z,e)}</b></li>' for z,e in GALLERY_MORE)}
  </ul>
  <p style="margin-top:18px"><a class="cta" data-fb href="#" target="_blank" rel="noopener">{L("到 Facebook 看更多影音","More videos on Facebook")}</a></p>
</div></section>
''')

# ---------------------------------------------------------------- 近期文章
page("articles.html", "近期文章", "紐約花蓮慈惠堂近期文章。", f'''
{head("近期文章","Recent Articles")}
<section class="gutter"><div class="container reading">
  <div class="draftnote">{L("文章內容待補：請提供舊網站這三篇文章的原文。","Article text to be added.")}</div>
  {postlist(ARTICLES)}
</div></section>
''')

# ---------------------------------------------------------------- 聯繫本堂
page("contact.html", "聯繫本堂", "紐約花蓮慈惠堂地址、電話與 Email。", f'''
{head("聯繫本堂","Contact Us")}
<section class="gutter"><div class="container grid g2" style="align-items:start">
  <dl class="contact-list">
    <div><dt>{L("地址","Address")}</dt><dd data-address></dd></div>
    <div><dt>{L("電話","Tel")}</dt><dd data-tel></dd></div>
    <div><dt>{L("傳真","Fax")}</dt><dd data-fax></dd></div>
    <div><dt>Email</dt><dd data-email></dd></div>
    <div><dt>Facebook</dt><dd><a data-fb href="#" target="_blank" rel="noopener">{L("紐約花蓮慈惠堂","Our page")}</a></dd></div>
  </dl>
  <iframe class="mapframe" title="Map" loading="lazy" src="https://maps.google.com/maps?q=22-06%20121st%20St%2C%20College%20Point%2C%20NY%2011356&z=15&output=embed"></iframe>
</div></section>
''')
print("ok")
