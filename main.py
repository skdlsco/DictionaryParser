import requests
from bs4 import BeautifulSoup


def urlToBS(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, "html.parser")


def getHeadAndTailInOrigin(div):
    a = div.find_all("a")
    li = []
    for word in a:
        if '-' in word.text:
            li.append(word.text)

    return li  # 접두 접미어 리스트로 출력


def getOrigin(word):
    base_url = "http://www.dictionary.com/browse/" + word
    bs = urlToBS(base_url)

    result = []
    for i in bs.find_all("section"):
        if i.find("section") is None and i.find("span", {"id": "wordOrigin"}) is not None:
            result.append(i)

    ht = []
    origin = []
    for section in result:
        div = section.find("div")
        ht.extend(getHeadAndTailInOrigin(div))
        origin.append(div.text)  # 실제 기원 문장으로 출력
    return [ht, origin]  # [[접두접미],[실제 기원들]]


def getMeansInDiv(div, word_class):
    if div.find("h3", {"class": "dic_tit6"}) is not None:
        title = div.find("h3", {"class": "dic_tit6"}).find("span").text
    else:
        title = ""
    means = []
    dts = div.find("dl").find_all("dt")

    for dt in dts:
        span = dt.find("em").find("span", {"class": "fnt_k06"})
        if span is not None:
            means.append(span.text)
    word_class[title] = means


def getWordClasses(word):
    base_url = "http://endic.naver.com"
    bs = urlToBS(base_url + "/search.nhn?sLn=kr&query=" + word)

    try:
        query = bs.find("div", {"id": "wrap"}) \
            .find("div", {"id": "container"}) \
            .find("div", {"id": "content"}) \
            .find("div", {"class": "word_num"}) \
            .find("dl", {"class": "list_e2"}) \
            .find("dt", {"class": "first"}) \
            .find("span", {"class": "fnt_e30"}) \
            .find("a")["href"]
    except:
        print("cannot find result")
        return  # 예외 처리

    bs = urlToBS(base_url + query)
    divs = bs.find("div", {"id": "wrap"}) \
        .find("div", {"id": "container"}) \
        .find("div", {"id": "content"}) \
        .find("div", {"id": "zoom_content"}) \
        .find_all("div", {"class": "box_wrap1"})
    word_class = {}
    for div in divs:
        getMeansInDiv(div, word_class)

    return [word_class, getExample(bs)]


# word 페이지의 bs
def getExample(bs):
    examples = []
    divs = bs.find("div", {"id": "wrap"}) \
        .find("div", {"id": "container"}) \
        .find("div", {"id": "content"}) \
        .find("div", {"id": "zoom_content"}) \
        .find_all("div", {"class": "box_wrap20"})
    for div in divs:
        div = div.find("h3", {"class": "dic_tit2"})
        if div is None:
            continue
        ul = div.parent.find("ul").find_all("li", {"class", "utb"}, False)

        for li in ul[:3]:  # 세개만
            sentence = li.find("div", {"class", "lineheight18 mar_top01"}) \
                .find("span", {"class", "fnt_e09 _ttsText"}).text.strip()
            mean = li.find("div", {"class", "mar_top1"}).text.strip()
            examples.append([sentence, mean])

    return examples


print(getOrigin("prior"))
print(getWordClasses("take"))
