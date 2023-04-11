import re
import json
from selenium.webdriver import Chrome


class About:
    @staticmethod
    def page_about(
        driver: Chrome = None,
        page_link: str = "",
    ):
        # Grab Page Source of About
        about_link = page_link + "about"
        driver.get(about_link)
        about_source = driver.page_source

        all_lines = about_source.split("\n")
        required_text = [
            single_line
            for single_line in all_lines
            if "global_likers_count" in single_line
        ][-1]

        cleaned_text = (
            re.findall('"result":.*', required_text)[-1]
            .replace('"result":', "")
            .split(',"extensions')[0]
        )
        about_data = json.loads(cleaned_text + "}")

        return about_data
