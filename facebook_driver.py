import json
from Utils import Utils
from About import About
from colorama import Fore, init
from datetime import datetime as dt


# from BasicInfo import BasicInfo
# from PostMedia import PostMedia
# from ParseJson import ParseJson

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


session, driver, logged_in_user_id = Utils.get_session(config=config)
userlist = ["https://www.facebook.com/arynewsasia/"]

fb_dtsg = ""
retries = 0

page_id = Utils.id_from_url_page_id(userlist[0])

while not fb_dtsg and retries < 3:
    fb_dtsg = Utils.dtsg_grabber(driver)
    if fb_dtsg:
        print(
            Fore.LIGHTBLUE_EX + "FB_Dtsg Grabbed Successfully  ::  " + fb_dtsg,
        )
    else:
        print(Fore.YELLOW + "*** FB_Dtsg not found Retrying ***")
        retries = retries + 1

print("[*]  Grabbing Required Tokens")
about_params = {}
about_params = Utils.tokens_grabber(userlist[0], session)

about_params["fb_dtsg"] = fb_dtsg
about_params["user_id"] = logged_in_user_id
print("[+]  Required Tokens Grabbed Successfully!")

if not page_id:
    print("[!]  No Page ID, Invalid Link")
    exit()
else:
    if page_id.isdigit():
        id_type = "NUMERIC_ID"
        numeric_id = page_id
    else:
        id_type = "USERNAME"

        # CALL Numeric_ID request
        numeric_id = about_params["numeric_id"]

    print(Fore.LIGHTGREEN_EX + "ID Type  :::  " + id_type)

start = dt.now()
# Grab About Data of Page
about_response = About.page_about(
    driver=driver,
    page_link=userlist[0],
)
with open("page_about.json", "w") as fl:
    json.dump(about_response, fl)
end = dt.now()
print(Fore.GREEN + "[+]  Time to Grab About  ::  " + str(end - start))
print(
    Fore.LIGHTCYAN_EX
    + "[+]  Total Time Until Now  ::  "
    + str(
        end - first_start,
    )
)

print("Done")
