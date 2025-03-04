import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from duckduckgo_search import DDGS

def sub_site(name, file_name):
    sub_site = open(f"{file_name}.md", 'w')
    sub_site.write(f"---\nlayout: default\ntitle: {name}\n---\n")
    sub_site.write(f"# **{name} - wyniki w internecie**\n")

    results = list(DDGS().text(keywords=f"{name} AND programming AND language -Is -?",
                                max_results=5))
    for result in results:
        title = result["title"]
        print(title)
        link = result["href"]
        snippet = result["body"]
        sub_site.write(f"## [{title}]({link})\n")
        sub_site.write(f"{snippet}\n")


url = "https://www.tiobe.com/tiobe-index/"
url_parser = urlparse(url)
base_source = "https://" + url_parser.netloc

main_site = open('lista.md', 'w')
main_site.write("---\nlayout: default\ntitle: lista\n---\n")

soup = BeautifulSoup(requests.get(url).text, "html.parser")
table = soup.find("tbody")
for nr, row in enumerate(table.find_all("tr")):
    elements = row.find_all("td")

    name = elements[4].text
    file_name = name.replace('/', '_')
    #sub_site(name, file_name)

    main_site.write(f"{nr}. ")
    main_site.write(f"![]({base_source}{elements[3].find("img").get("src")})\n")
    main_site.write(f"[{name}]({file_name})\\\n")
    main_site.write(f"rating: {elements[5]}\n")

    prompt = f"\"The {name} Programming Language site:{url}\""
    found = list(DDGS().text(keywords=prompt, max_results=1))
    if not found:
        continue

    lan_url = found[0]["href"]
    print(lan_url)
    lan_site=requests.get(lan_url)
    additional = BeautifulSoup(lan_site.text, "html.parser")
    facts = additional.find_all("p")
    #print(facts)
    #![alt text](image.jpg)
    #[title](https://www.example.com)