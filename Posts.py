# import re
import json
import requests

# import threading
from random import randint
from datetime import datetime
from datetime import timedelta

# from ViewCounts import get_views_counts


class Posts:
    @staticmethod
    def get_posts(
        final_posts: list = [],
        page_id: str = "",
        # posts_count: int = 100,
        POSTS_DOC_ID: str = "",
        PROXIES_LIST: list = [],
        days_limit: int = 3,
    ):
        headers = {
            "authority": "www.facebook.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
        }

        # threads_list = list()

        payload = {
            "__user": "0",
            "__a": "1",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "ProfileCometTimelineFeedRefetchQuery",
            "variables": '{"UFI2CommentsProvider_commentsKey":"ProfileCometTimelineRoute","afterTime":null,"beforeTime":null,"count":3,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"displayCommentsFeedbackContext":null,"feedLocation":"TIMELINE","feedbackSource":0,"focusCommentID":null,"memorializedSplitTimeFilter":null,"omitPinnedPost":true,"postedBy":null,"privacy":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"timeline","scale":1,"stream_count":1,"taggedInOnly":null,"useDefaultActor":false,"id":"'
            + page_id
            + '","__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__CometUFIIsRTAEnabledrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":false,"__relay_internal__pv__StoriesRingrelayprovider":false}',
            "server_timestamps": "true",
            "doc_id": POSTS_DOC_ID,
        }

        random_num = randint(0, len(PROXIES_LIST) - 1)
        response = requests.post(
            "https://www.facebook.com/api/graphql/",
            headers=headers,
            data=payload,
            proxies=PROXIES_LIST[random_num],
        )

        data = response.text
        posts = data.split("\r")
        cleaned_responses = [ch.strip() for ch in posts]
        posts_json = {}

        upcoming_posts = list()
        for post in cleaned_responses:
            if (
                post[:40] == '{"label":"ProfileCometTimelineFeed_user$'
                and "has_next_page" not in post
            ):
                posts_json = json.loads(post)
                try:
                    node = posts_json["data"].get("node", {})
                    node.update({"views_count": "0"})
                    upcoming_posts.append(node)
                except Exception as ex:
                    breakpoint()
                    print(ex)

            elif (
                post[:40] == '{"label":"ProfileCometTimelineFeed_user$'
                and "has_next_page" in post
            ):
                posts_json = json.loads(post)
                try:
                    page_info = posts_json["data"].get("page_info", {})
                except Exception as ex:
                    breakpoint()
                    print(ex)

            elif post[:36] == '{"data":{"node":{"__typename":"User"':
                posts_json = json.loads(post)
                try:
                    post_edges_list = (
                        posts_json["data"]["node"]
                        .get("timeline_list_feed_units")
                        .get(
                            "edges",
                            [],
                        )
                    )
                    if post_edges_list and len(post_edges_list) == 1:
                        node = post_edges_list[0].get("node")
                        node.update({"views_count": "0"})
                        upcoming_posts.append(node)
                except Exception as ex:
                    breakpoint()
                    print(ex)

        if not upcoming_posts:
            return final_posts
        else:
            final_posts.extend(upcoming_posts)

        # for single_edge in post_edges:
        #     post_id = single_edge["node"]["post_id"]
        #     print("[+]  Post Id  ::  ", post_id)
        #     if post_id:
        #         random_num = randint(0, len(PROXIES_LIST) - 1)
        #         random_proxy = PROXIES_LIST[random_num]

        # viewer_thread = threading.Thread(
        #     target=get_views_counts,
        #     args=(single_edge, post_id, random_proxy),
        # )
        # viewer_thread.start()
        # threads_list.append(viewer_thread)

        # page_info = posts_json["data"]["node"]["timeline_feed_units"].get(
        #     "page_info", {}
        # )

        try:
            end_cursor = page_info.get("end_cursor", "")
        except Exception as ex:
            breakpoint()
            print(ex)

        try:
            # Last Post Date
            last_post_date_time_stamp = (
                final_posts[-1]
                .get("comet_sections")
                .get("content")
                .get("story")
                .get("comet_sections")
                .get("context_layout")
                .get("story")
                .get("comet_sections")
                .get("metadata")[0]["story"]
                .get("creation_time")
            )
        except Exception as ex:
            last_post_date_time_stamp = (
                final_posts[-1]
                .get("node")
                .get("comet_sections")
                .get("content")
                .get("story")
                .get("comet_sections")
                .get("context_layout")
                .get("story")
                .get("comet_sections")
                .get("metadata")[0]["story"]
                .get("creation_time")
            )

        last_post_date = datetime.fromtimestamp(
            last_post_date_time_stamp,
        ).date()

        try:
            # First Post Date
            first_post_date_time_stamp = (
                final_posts[0]
                .get("comet_sections")
                .get("content")
                .get("story")
                .get("comet_sections")
                .get("context_layout")
                .get("story")
                .get("comet_sections")
                .get("metadata")[0]["story"]
                .get("creation_time")
            )
        except Exception as ex:
            # First Post Date
            first_post_date_time_stamp = (
                final_posts[0]
                .get("node")
                .get("comet_sections")
                .get("content")
                .get("story")
                .get("comet_sections")
                .get("context_layout")
                .get("story")
                .get("comet_sections")
                .get("metadata")[0]["story"]
                .get("creation_time")
            )

        first_post_date = datetime.fromtimestamp(
            first_post_date_time_stamp,
        ).date()

        check_date = first_post_date - timedelta(days=days_limit)

        while page_info.get("has_next_page") and last_post_date >= check_date:
            print("[{}]  Posts Until Now".format(str(len(final_posts))))
            payload = {
                "__user": "0",
                "__a": "1",
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "ProfileCometTimelineFeedRefetchQuery",
                "variables": '{"UFI2CommentsProvider_commentsKey":"ProfileCometTimelineRoute","afterTime":null,"beforeTime":null,"count":3,"cursor":"'
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
                headers=headers,
                data=payload,
                proxies=PROXIES_LIST[random_num],
            )

            data = response.text
            posts = data.split("\r")
            cleaned_responses = [ch.strip() for ch in posts]
            posts_json = {}

            upcoming_posts = list()
            for post in cleaned_responses:
                if (
                    post[:40] == '{"label":"ProfileCometTimelineFeed_user$'
                    and "has_next_page" not in post
                ):
                    posts_json = json.loads(post)
                    try:
                        node = posts_json["data"].get("node", {})
                        node.update({"views_count": "0"})
                        upcoming_posts.append(node)
                    except Exception as ex:
                        breakpoint()
                        print(ex)

                elif (
                    post[:40] == '{"label":"ProfileCometTimelineFeed_user$'
                    and "has_next_page" in post
                ):
                    posts_json = json.loads(post)
                    try:
                        page_info = posts_json["data"].get("page_info", {})
                    except Exception as ex:
                        breakpoint()
                        print(ex)

                elif post[:36] == '{"data":{"node":{"__typename":"User"':
                    posts_json = json.loads(post)
                    try:
                        post_edges_list = (
                            posts_json["data"]["node"]
                            .get("timeline_list_feed_units")
                            .get(
                                "edges",
                                [],
                            )
                        )
                        if post_edges_list and len(post_edges_list) == 1:
                            node = post_edges_list[0].get("node")
                            node.update({"views_count": "0"})
                            upcoming_posts.append(node)
                    except Exception as ex:
                        breakpoint()
                        print(ex)

            if not upcoming_posts:
                return final_posts
            else:
                final_posts.extend(upcoming_posts)

            # for single_edge in post_edges:
            #     post_id = single_edge["node"]["post_id"]
            #     print("[+]  Post Id  ::  ", post_id)
            #     if post_id:
            #         random_num = randint(0, len(PROXIES_LIST) - 1)
            #         random_proxy = PROXIES_LIST[random_num]

            # viewer_thread = threading.Thread(
            #     target=get_views_counts,
            #     args=(single_edge, post_id, random_proxy),
            # )
            # viewer_thread.start()
            # threads_list.append(viewer_thread)

            # page_info = posts_json["data"]["node"]["timeline_feed_units"].get(
            #     "page_info", {}
            # )

            try:
                end_cursor = page_info.get("end_cursor", "")
            except Exception as ex:
                breakpoint()
                print(ex)
            # final_posts.extend(post_edges)

            try:
                # Last Post Date
                last_post_date_time_stamp = (
                    final_posts[-1]
                    .get("comet_sections")
                    .get("content")
                    .get("story")
                    .get("comet_sections")
                    .get("context_layout")
                    .get("story")
                    .get("comet_sections")
                    .get("metadata")[0]["story"]
                    .get("creation_time")
                )
            except Exception as ex:
                last_post_date_time_stamp = (
                    final_posts[-1]
                    .get("node")
                    .get("comet_sections")
                    .get("content")
                    .get("story")
                    .get("comet_sections")
                    .get("context_layout")
                    .get("story")
                    .get("comet_sections")
                    .get("metadata")[0]["story"]
                    .get("creation_time")
                )

            last_post_date = datetime.fromtimestamp(
                last_post_date_time_stamp,
            ).date()

            check_date = first_post_date - timedelta(days=days_limit)

        # if threads_list:
        #     for single_thread in threads_list:
        #         single_thread.join()

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
