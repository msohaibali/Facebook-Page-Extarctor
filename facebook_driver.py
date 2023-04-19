import json
from About import About
from Posts import Posts
from colorama import Fore, init
from datetime import datetime as dt


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
# CONFIGURATIONS

page_id = "485559268138376"  # ARYNEWS


start = dt.now()

# Grab About Data of Page
about_response = About.page_about(
    ABOUT_DOC_ID=config.get("ABOUT_DOC_ID"),
    page_id=page_id,
)
with open(page_id + "_page_about.json", "w") as fl:
    json.dump(about_response, fl)
end = dt.now()
print(Fore.GREEN + "[+]  Time to Grab About  ::  " + str(end - start))


start = dt.now()
# Grab Page Posts
posts_count = 10
all_posts = Posts.get_posts(
    page_id=page_id, posts_count=posts_count, POSTS_DOC_ID=config.get("POSTS_DOC_ID")
)
with open(page_id + "_page_posts.json", "w") as fl:
    json.dump(all_posts, fl)
end = dt.now()
print(
    Fore.GREEN
    + "[+]  Time to Grab {} Posts  ::  ".format(str(posts_count))
    + str(end - start)
)

print(
    Fore.LIGHTCYAN_EX
    + "[+]  Total Time Until Now  ::  "
    + str(
        end - first_start,
    )
)

print("Done")
