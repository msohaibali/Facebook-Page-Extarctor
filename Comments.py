import requests
import base64


class Comments:
    @staticmethod
    def get_comments(
        post_id: str = "7269474239746811",
        COMMENTORS_DOC_ID: str = "6060906520611716",
        next_cursor: str = "",
    ) -> list:
        feedback = "feedback:" + str(post_id)
        encoded_feedback = base64.b64encode(feedback.encode()).decode()

        if next_cursor:
            after_cursor = '"' + next_cursor + '"'
        else:
            after_cursor = "null"

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
            "fb_api_req_friendly_name": "CometUFICommentsProviderForDisplayCommentsQuery",
            "variables": '{"UFI2CommentsProvider_commentsKey":"CometSinglePageContentContainerFeedQuery","__false":false,"__true":true,"after":'
            + after_cursor
            + ',"before":null,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"displayCommentsFeedbackContext":null,"feedLocation":"PAGE_TIMELINE","feedbackSource":22,"first":100,"focusCommentID":null,"includeHighlightedComments":false,"includeNestedComments":true,"initialViewOption":null,"isInitialFetch":false,"isPaginating":false,"last":null,"scale":1,"topLevelViewOption":"RANKED_UNFILTERED","useDefaultActor":false,"viewOption":"RANKED_UNFILTERED","id":"'
            + encoded_feedback
            + '"}',
            # 'server_timestamps': 'true',
            "doc_id": COMMENTORS_DOC_ID,
        }
        response = requests.post(
            "https://www.facebook.com/api/graphql/", headers=headers, data=data
        )

        if response.ok:
            data = response.json().get("data")
        else:
            data = {}

        return data
        # with open(str(post_id) + "_COMMENTS.json", "w", encoding="utf-8") as fl:
        #     json.dump(data, fl)
