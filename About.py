import requests


class About:
    @staticmethod
    def page_about(page_id: str = "", ABOUT_DOC_ID: str = ""):
        headers = {
            "authority": "www.facebook.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.facebook.com",
            "referer": "https://www.facebook.com/arynewsasia",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
        }

        data = {
            "__a": "1",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "PagesCometAboutRootQuery",
            "variables": '{"pageID":"' + page_id + '","scale":1}',
            "server_timestamps": "true",
            "doc_id": ABOUT_DOC_ID,
        }

        response = requests.post(
            "https://www.facebook.com/api/graphql/",
            headers=headers,
            data=data,
        )

        if response.ok:
            about_data = response.json()
            data = about_data.get("data")
            return data

        else:
            print("[-]  No About Found!")
            return {}
