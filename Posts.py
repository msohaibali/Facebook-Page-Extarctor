import re
import json
import requests
import threading
from random import randint
from ViewCounts import get_views_counts


class Posts:
    @staticmethod
    def get_posts(
        final_posts: list = [],
        page_id: str = "",
        posts_count: int = 100,
        POSTS_DOC_ID: str = "",
        PROXIES_LIST: list = [],
    ):
        threads_list = list()
        payload = {
            "__a": "1",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "CometModernPageFeedPaginationQuery",
            "variables": '{"UFI2CommentsProvider_commentsKey":"CometSinglePageContentContainerFeedQuery","count":3,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"displayCommentsFeedbackContext":null,"feedLocation":"PAGE_TIMELINE","feedbackSource":22,"focusCommentID":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"timeline","scale":1,"useDefaultActor":false,"id":"'
            + page_id
            + '","__relay_internal__pv__GroupsCometDelayCheckBlockedUsersrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}',
            "server_timestamps": "true",
            "doc_id": POSTS_DOC_ID,
        }

        random_num = randint(0, len(PROXIES_LIST) - 1)
        response = requests.post(
            "https://www.facebook.com/api/graphql/",
            data=payload,
            proxies=PROXIES_LIST[random_num],
        )

        data = response.text
        posts = data.split("\r")
        cleaned_responses = [ch.strip() for ch in posts]
        posts_json = {}

        for post in cleaned_responses:
            if "__typename" in post:
                posts_json = json.loads(post)
                break

        post_edges = posts_json["data"]["node"]["timeline_feed_units"].get(
            "edges",
            [],
        )
        for single_edge in post_edges:
            post_id = single_edge["node"]["post_id"]
            print("[+]  Post Id  ::  ", post_id)
            if post_id:
                random_num = randint(0, len(PROXIES_LIST) - 1)
                random_proxy = PROXIES_LIST[random_num]

                viewer_thread = threading.Thread(
                    target=get_views_counts,
                    args=(single_edge, post_id, random_proxy),
                )
                viewer_thread.start()
                threads_list.append(viewer_thread)

        page_info = posts_json["data"]["node"]["timeline_feed_units"].get(
            "page_info", {}
        )

        end_cursor = page_info.get("end_cursor", "")

        final_posts.extend(post_edges)

        while page_info.get("has_next_page") and len(final_posts) <= int(
            posts_count,
        ):
            print("[{}]  Posts Until Now".format(str(len(final_posts))))
            payload = {
                "__a": "1",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "CometModernPageFeedPaginationQuery",
                "variables": '{"UFI2CommentsProvider_commentsKey":"CometSinglePageContentContainerFeedQuery","count":3,"cursor":"'
                + end_cursor
                + '","displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"displayCommentsFeedbackContext":null,"feedLocation":"PAGE_TIMELINE","feedbackSource":22,"focusCommentID":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"timeline","scale":1,"useDefaultActor":false,"id":"'
                + page_id
                + '","__relay_internal__pv__GroupsCometDelayCheckBlockedUsersrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}',
                "server_timestamps": "true",
                "doc_id": POSTS_DOC_ID,
            }

            random_num = randint(0, len(PROXIES_LIST) - 1)
            response = requests.post(
                "https://www.facebook.com/api/graphql/",
                data=payload,
                proxies=PROXIES_LIST[random_num],
            )
            data = response.text
            posts = data.split("\r")
            cleaned_responses = [ch.strip() for ch in posts]
            posts_json = {}
            for post in cleaned_responses:
                if "__typename" in post:
                    posts_json = json.loads(post)
                    break

            post_edges = posts_json["data"]["node"]["timeline_feed_units"].get(
                "edges", []
            )
            for single_edge in post_edges:
                post_id = single_edge["node"]["post_id"]
                if post_id:
                    print("[+]  Post Id  ::  ", post_id)
                    random_num = randint(0, len(PROXIES_LIST) - 1)
                    random_proxy = PROXIES_LIST[random_num]

                    viewer_thread = threading.Thread(
                        target=get_views_counts,
                        args=(single_edge, post_id, random_proxy),
                    )
                    viewer_thread.start()
                    threads_list.append(viewer_thread)

            page_info = posts_json["data"]["node"]["timeline_feed_units"].get(
                "page_info", {}
            )
            end_cursor = page_info.get("end_cursor", "")
            final_posts.extend(post_edges)

        if threads_list:
            for single_thread in threads_list:
                single_thread.join()

        return final_posts


# page_id = "485559268138376"
# posts_count = 10
# POSTS_DOC_ID = "6277940392268995"

# posts_list = Posts.get_posts(
#     page_id=page_id,
#     posts_count=posts_count,
#     POSTS_DOC_ID=POSTS_DOC_ID,
# )

# print("DONE!")
