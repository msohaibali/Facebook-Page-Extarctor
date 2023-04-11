import os
import re
import requests
import warnings as w
from time import sleep
from requests import Session
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init


m = re.compile(
    r"https?:\/\/([a-zA-z]*?\.?)facebook\.com\/(profile\.php\?id=(?P<id>\d*)|(?P<userid>[a-zA-z0-9\._]*))"
)

p = re.compile(r".*((fbid=)|(hash=)|(posts\/)|(videos\/))(?P<id>\d*)")

email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
phonenumber_pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"  # r"[0-9#+-]{10,17}"


# Disable unnecessary warnings
w.filterwarnings("ignore")


class Utils:
    @staticmethod
    def tokens_grabber(profile_link, session=requests, log=print):
        url = profile_link + "about"
        res = session.get(url)
        if res.status_code != 200:
            log(Fore.LIGHTRED_EX + "*** Issue while grabbing Tokens VIA REQUEST ***")
            log(Fore.RED + "Request STATUS CODE ==> " + str(res.status_code))
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            try:
                numeric_id = (
                    re.findall(r"\"pageID\":\"[0-9]*\"", res.text)[0]
                    .replace('"pageID":"', "")
                    .replace('"', "")
                )
                log(
                    Fore.LIGHTGREEN_EX
                    + "Numeric ID Grabbed Successfully  ::  "
                    + numeric_id
                )
            except:
                try:
                    numeric_id = (
                        re.findall(r"\"rawSectionToken\":\"[0-9]*:[0-9]*", res.text)[0]
                        .replace('"rawSectionToken":"', "")
                        .split(":")[0]
                    )
                except:
                    log(
                        Fore.LIGHTRED_EX
                        + "-------- Issue while Grabbing  ** Page Numeric ID **  --------"
                    )
                    numeric_id = ""
            try:
                target_name = soup.title.text
                log(
                    Fore.LIGHTGREEN_EX
                    + "Target Name Grabbed Successfully  ::  "
                    + target_name
                )
            except:
                log(
                    Fore.LIGHTRED_EX
                    + "-------- Issue while Grabbing  ** Page Name **  --------"
                )
                target_name = ""

        log(Fore.WHITE + "\n -------------------------------------------------\n")

        about_params = {"target_name": target_name, "numeric_id": numeric_id}

        return about_params

    @staticmethod
    def dtsg_grabber(driver):
        try:
            pg_source = driver.page_source
            fb_dtsg = re.findall(r"{\"token\":\"[0-9A-Za-z-_:]*", pg_source)[0].replace(
                '{"token":"', ""
            )
        except:
            fb_dtsg = ""

        return fb_dtsg

    @staticmethod
    def get_session(
        USERNAME: str = "",
        PASSWORD: str = "",
        config: dict = dict(),
        driver_type: str = "CHROME",
        browser_profile: str = "first",
        session_only: bool = False,
    ) -> Session:
        """
        Creates and return a Logged in Session
        :param USERNAME: username to login
        :param PASSWORD: password to login
        :param config: configuration file used for login
        :param browser_profile: Browser Profile to utilise for session
        :return session: Logged in Session
        """

        # Webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        if config.get("LOGIN_CREDENTIALS").get("DRIVER_TYPE") == "CHROME":
            """
                Grab Current User Profile Path
            + Add Browser Profiles Location
            + Add Profile Number
                TO CREATE BROWSER PROFILE PATH
            """
            BROWSER_PATH = (
                os.environ.get("USERPROFILE")
                + config.get("BROWSER_PATH")
                + config.get("LOGIN_CREDENTIALS").get("PROFILE")
            )

            # Assign Browser Profile in Arguments
            browser_argument = "user-data-dir=" + BROWSER_PATH

            # Add Profile Number in Argument
            print("[#]  BROWSER ARGUMENT:   ", browser_argument)
            chrome_options.add_argument(browser_argument)

            driver = webdriver.Chrome(
                executable_path="D:\\chromedriver.exe", chrome_options=chrome_options,
            )
        else:
            profile = webdriver.FirefoxProfile()
            profile.set_preference(
                "dom.webnotifications.enabled", False,
            )
            profile.set_preference(
                "dom.push.enabled", False,
            )

            options = webdriver.FirefoxOptions()
            options.headless = False
            options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

            driver = webdriver.Firefox(
                executable_path="D:\\geckodriver.exe",
                options=options,
                firefox_profile=profile,
            )

        driver.maximize_window()
        driver.get("https://www.facebook.com/")
        sleep(5)

        if (config.get("LOGIN_CREDENTIALS").get("NAME")) not in driver.page_source:
            print("[!]  Driver Not Logged IN!")
            print("[*]  Trying to Log IN!")

            # Get username element
            username = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']",),)
            )

            # Get password element
            password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']",),)
            )

            # Clear fields
            username.clear()
            password.clear()

            username.send_keys(
                config.get("LOGIN_CREDENTIALS").get("USERNAME")
                if not USERNAME
                else USERNAME,
            )
            password.send_keys(
                config.get("LOGIN_CREDENTIALS").get("PASSWORD")
                if not PASSWORD
                else PASSWORD,
            )

            sleep(2)
            password.send_keys(Keys.ENTER)
            sleep(10)

            if (config.get("LOGIN_CREDENTIALS").get("NAME")) not in driver.page_source:
                print("[!]  Driver Not Logged IN!")
                driver.quit()
                exit()
            else:
                print("[+]  Log In Successful!")

        else:
            print("[+]  Browser is Already Logged IN!")

            # Grab Cookies from Driver
        cookies = driver.get_cookies()
        user_id = None

        # Create New Session
        session = Session()
        session.headers.update(config.get("HEADERS"))

        # Assign Cookies to our Session
        session.cookies.clear()
        for single_cookie in cookies:
            if single_cookie["name"] == "c_user":
                user_id = single_cookie["value"]
                print("User ID grabbed Successfully: " + str(user_id))

            required_cookies = {
                "name": single_cookie.get("name"),
                "value": single_cookie.get("value"),
            }
            optional_cookies = {
                "domain": single_cookie.get("domain"),
                "expires": None,
                "rest": {"HttpOnly": True},
                "path": single_cookie.get("path"),
                "secure": single_cookie.get("secure"),
            }
            if single_cookie.get("name") == "csrftoken":
                session.headers.update({"x-csrftoken": single_cookie.get("value")})

            my_cookie = requests.cookies.create_cookie(
                **required_cookies, **optional_cookies
            )
            session.cookies.set_cookie(my_cookie)

        if session_only:
            # Finally Cookies are set for Session, Closing Browser
            driver.quit()
            return session, user_id
        else:
            return session, driver, user_id

    @staticmethod
    def id_from_url_page_id(l_link):
        """
            to extract page id from link
        """
        link = l_link[l_link.find("/", 9) + 1 :]
        link = link[: link.find("/") if link.find("/") > 0 else len(link)].rstrip("/")
        if link.find("-") < 0:
            return link

        for l in link.split("-"):
            if l.isdigit() and len(l) > 10:
                print(l)
                return l
        print("invalid url ", link)
        return None
