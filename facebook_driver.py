import json
from About import About
from Posts import Posts

# from Comments import Comments
from colorama import Fore, init
from datetime import datetime as dt
from ProxiesGrabber import ProxiesGrabber


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

PROXIES_LIST = ProxiesGrabber.get_proxies_list(
    token=WEBSHARE_TOKEN, proxies_url=LIST_PROXIES_URL
)
# page_id = "485559268138376"  # ARYNEWS
# page_id = "100064592176210"  # BOLNEWS
page_id = "111331428916358"  # GEONEWSURDU


start = dt.now()

# Grab About Data of Page
about_response = About.page_about(
    ABOUT_DOC_ID=config.get("ABOUT_DOC_ID"),
    page_id=page_id,
    PROXIES_LIST=PROXIES_LIST,
)
with open(page_id + "_page_about.json", "w") as fl:
    json.dump(about_response, fl)
end = dt.now()
print(Fore.GREEN + "[+]  Time to Grab About  ::  " + str(end - start))


start = dt.now()
# Grab Page Posts
posts_count = 50
all_posts = Posts.get_posts(
    page_id=page_id,
    posts_count=posts_count,
    POSTS_DOC_ID=config.get(
        "POSTS_DOC_ID",
    ),
    PROXIES_LIST=PROXIES_LIST,
)

with open(page_id + "_page_posts.json", "w") as fl:
    json.dump(all_posts, fl)

end = dt.now()
print(
    Fore.GREEN
    + "[+]  Time to Grab {} Posts  ::  ".format(str(posts_count))
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

#     with open(post_id + "_post_comments.json", "w", encoding="utf-8") as fl:
#         json.dump(all_comments, fl)

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

print("Done")
