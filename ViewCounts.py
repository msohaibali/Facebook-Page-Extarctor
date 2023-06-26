import requests
from bs4 import BeautifulSoup


def get_views_counts(post_json: dict, video_id: str, proxy: dict):
    res = requests.get(
        f"https://facebook.com/{video_id}/",
        proxies=proxy,
    )
    soup = BeautifulSoup(res.text, "html.parser")
    view_count = "0"
    try:
        contents = [aa for aa in soup.findAll("meta") if "views" in str(aa)]
        if contents:
            meta_tag = contents[-1]
            view_count = (
                str(meta_tag)
                .replace("\xa0", " ")
                .split(" views")[0]
                .replace('<meta content="', "")
            )
    except Exception as ex:
        print("[-]  Issue  ::  ", ex)
        pass
    post_json.update({"views_count": view_count})
