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

    print(li)


def getOrigin(word):
    base_url = "http://www.dictionary.com/browse/" + word
    bs = urlToBS(base_url)

    result = []
    for i in bs.find_all("section"):
        if i.find("section") is None and i.find("span", {"id": "wordOrigin"}) is not None:
            result.append(i)

    for section in result:
        div = section.find("div")
        getHeadAndTailInOrigin(div)
        # print(div.text)


def getMeansInDiv(div, word_class):
    if div.find("h3", {"class": "dic_tit^"}) is not None:
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

    print(word_class)


getOrigin("")
getWordClasses("")
