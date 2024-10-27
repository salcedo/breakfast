import requests

from bs4 import BeautifulSoup

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}


def get_hrefs(
    url="https://locations.arbys.com", referer="https://www.arbys.com", geo="Region"
):
    global headers

    r = requests.get(url, headers={**headers, "referer": referer})
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find_all(
        "a",
        class_="ga-link",
        attrs={"data-ga": lambda x: x and x.startswith(f"Maplist, {geo}")},
    )


def check_breakfast(url, referer):
    global headers

    r = requests.get(url, headers={**headers, "referer": referer})
    soup = BeautifulSoup(r.text, "html.parser")
    lfw = soup.find("div", class_="location-features-wrap")
    if not lfw:
        return False

    ul_tag = lfw.find("ul")
    if not ul_tag:
        return False

    if any(li_tag.text.strip() == "Breakfast" for li_tag in ul_tag.find_all("li")):
        return True
    else:
        return False


def main():
    for region in get_hrefs(geo="Region"):
        for city in get_hrefs(
            url=region["href"], referer="https://locations.arbys.com", geo="City"
        ):
            for location in get_hrefs(
                city["href"], referer=region["href"], geo="Location"
            ):
                if check_breakfast(location["href"], city["href"]):
                    print(f'"{location["title"]}","{location["href"]}"')


if __name__ == "__main__":
    main()
