import json
from About import About
from Posts import Posts
from fastapi import FastAPI

from typing import Union

# from Comments import Comments
from colorama import Fore, init
from datetime import datetime as dt
from ProxiesGrabber import ProxiesGrabber
from BucketConnector import BucketConnector
from Parse_dump_json import ParseJson

first_start = dt.now()
init()

# Read Configuration as global variable
with open("config.json") as fl:
    config = json.loads(fl.read())


# CONFIGURATIONS
REACTORS_DOC_ID = config["REACTORS_DOC_ID"]
POSTS_DOC_ID = config["POSTS_DOC_ID"]
COMMENTORS_DOC_ID = config["COMMENTORS_DOC_ID"]
HOVER_DOC_ID = config["HOVER_DOC_ID"]
ABOUT_DOC_ID = config["ABOUT_DOC_ID"]
IMAGES_PHOTOS_ALL_DOC_ID = config["IMAGES_PHOTOS_ALL_DOC_ID"]
COMMENTORS_LIMIT = config["COMMENTORS_LIMIT"]
REACTORS_LIMIT = config["REACTORS_LIMIT"]
POSTS_SIZE = config["POSTS_SIZE"]
UK_SERVER_STATUS = config["UK_SERVER"]
PHOTOS_LIMIT = config["PHOTOS_LIMIT"]
ACCESS_TOKEN = config["ACCESS_TOKEN"]

LIST_PROXIES_URL = config["LIST_PROXIES_URL"]
WEBSHARE_TOKEN = config["WEBSHARE_TOKEN"]
# CONFIGURATIONS

# # page_id = "485559268138376"  # ARYNEWS
# # page_id = "100064592176210"  # BOLNEWS
# page_id = "111331428916358"  # GEONEWSURDU


# Get Proxies List
PROXIES_LIST = ProxiesGrabber.get_proxies_list(
    token=WEBSHARE_TOKEN, proxies_url=LIST_PROXIES_URL
)


def page_data(
    page_id: str = "111331428916358",
    refresh_proxies: bool = False,
    PROXIES_LIST: list = PROXIES_LIST,
    days_limit: int = 3,
):
    # if refresh_proxies:
    # Get Proxies List
    PROXIES_LIST = ProxiesGrabber.get_proxies_list(
        token=WEBSHARE_TOKEN, proxies_url=LIST_PROXIES_URL
    )

    start = dt.now()

    # Grab About Data of Page
    about_response = About.page_about(
        ABOUT_DOC_ID=config.get("ABOUT_DOC_ID"),
        page_id=page_id,
        PROXIES_LIST=PROXIES_LIST,
    )
    # with open(page_id + "_page_about.json", "w") as fl:
    #     json.dump(about_response, fl)
    print("[*]  Dumping About Data to S3!")
    BucketConnector.store_data(
        data=about_response,
        bucket_name="fb-page-bucket",
        category_name="About",
        folder_name=page_id,
        about_data=True,
    )
    print("[+]  About Data Successfully dumped to S3!")

    end = dt.now()
    print(Fore.GREEN + "[+]  Time to Grab About  ::  " + str(end - start))

    start = dt.now()

    # Grab Page Posts
    # posts_count = 10
    all_posts = Posts.get_posts(
        final_posts=[],
        page_id=page_id,
        # posts_count=posts_count,
        POSTS_DOC_ID=config.get(
            "POSTS_DOC_ID",
        ),
        PROXIES_LIST=PROXIES_LIST,
        days_limit=int(days_limit),
    )

    try:
        print('[*]  Dumping Posts Data to Database!')
        ParseJson.parseJson(data=all_posts)
    except Exception as e:
        print(e)
    # with open(page_id + "_page_posts.json", "w") as fl:
    #     json.dump(all_posts, fl)

    print("[*]  Dumping Posts Data to S3!")
    BucketConnector.store_data(
        data=all_posts,
        bucket_name="fb-page-bucket",
        category_name="Posts",
        folder_name=page_id,
    )
    print("[+]  Posts Data Successfully dumped to S3!")

    end = dt.now()
    print(
        Fore.GREEN
        + "[+]  Time to Grab {} Posts  ::  ".format(str(len(all_posts)))
        + str(end - start)
    )

    # # Grab Posts Comments
    # posts_count_for_comments = 2
    # start = dt.now()
    # for post in all_posts[:posts_count_for_comments]:
    #     all_comments = list()
    #     post_id = post.get("node").get("post_id")

    #     post_comments = Comments.get_comments(post_id=post_id)
    #     while len(all_comments) <= COMMENTORS_LIMIT:
    #         if post_comments:
    #             comments_list = (
    #                 post_comments.get("node").get("display_comments").get("edges")
    #             )
    #             all_comments.extend(comments_list)

    #             has_next_page = (
    #                 post_comments.get("node")
    #                 .get("display_comments")
    #                 .get("page_info")
    #                 .get("has_next_page")
    #             )

    #             next_cursor = (
    #                 post_comments.get("node")
    #                 .get("display_comments")
    #                 .get("page_info")
    #                 .get("end_cursor")
    #             )

    #             if has_next_page:
    #                 post_comments = Comments.get_comments(
    #                     post_id=post_id,
    #                     next_cursor=next_cursor,
    #                 )

    #             else:
    #                 break

    #         else:
    #             break

    # end = dt.now()

    # print(
    #     Fore.GREEN
    #     + "[+]  Time to Grab {} Comments of {} Posts  ::  ".format(
    #         str(COMMENTORS_LIMIT), str(posts_count_for_comments)
    #     )
    #     + str(end - start)
    # )

    print(
        Fore.LIGHTCYAN_EX
        + "[+]  Total Time Until Now  ::  "
        + str(
            end - first_start,
        )
    )


app = FastAPI()


@app.get("/")
def read_root():
    return {"api_version": "1.0"}


@app.get("/get_data")
def get_page_data(
    page_id: str = None,
    refresh_proxies: Union[str, None] = "true",
    days_limit: Union[str, None] = "3",
):
    if not page_id:
        return {
            "page_id": page_id,
            "status": "error",
            "error": "Page ID required",
        }

    try:
        refresh_proxies = (
            json.loads(
                refresh_proxies,
            )
            if refresh_proxies
            else False
        )
        page_data(
            page_id=page_id,
            refresh_proxies=refresh_proxies,
            days_limit=days_limit,
        )
        return {"page_id": page_id, "status": "Data Stored"}

    except Exception as ex:
        return {"page_id": page_id, "status": "Error", "error": str(ex)}
