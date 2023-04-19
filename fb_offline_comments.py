import requests
import json

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
    "x-asbd-id": "198387",
    "x-fb-friendly-name": "CometUFICommentsProviderForDisplayCommentsQuery",
    "x-fb-lsd": "AVp3-TPXPCw",
}

data = {
    "__a": "1",
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "CometUFICommentsProviderForDisplayCommentsQuery",
    # "variables": '{"UFI2CommentsProvider_commentsKey":"CometSinglePageContentContainerFeedQuery","__false":false,"__true":true,"after":"AQHRkSJ90DgKkRVXbtVk8og_I-AB2yYmTs07qd08875ZFN3iYI-C5RsQt7sQTMGSZfRtGqcbbmrkqYZnFXqtz1BDrg","before":null,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"displayCommentsFeedbackContext":null,"feedLocation":"PAGE_TIMELINE","feedbackSource":22,"first":50,"focusCommentID":null,"includeHighlightedComments":false,"includeNestedComments":true,"initialViewOption":"RANKED_THREADED","isInitialFetch":false,"isPaginating":true,"last":null,"scale":1,"topLevelViewOption":null,"useDefaultActor":false,"viewOption":null,"id":"ZmVlZGJhY2s6NzI0NjA3NzI0ODc1MzE3Nw=="}',
    "variables": '{"UFI2CommentsProvider_commentsKey":"CometSinglePageContentContainerFeedQuery","__false":false,"__true":true,"displayCommentsContextEnableComment":null,"displayCommentsContextIsAdPreview":null,"displayCommentsContextIsAggregatedShare":null,"displayCommentsContextIsStorySet":null,"displayCommentsFeedbackContext":null,"feedLocation":"PAGE_TIMELINE","feedbackSource":22,"first":100,"focusCommentID":null,"includeHighlightedComments":false,"includeNestedComments":true,"initialViewOption":"RANKED_THREADED","isInitialFetch":false,"isPaginating":true,"last":null,"scale":1,"topLevelViewOption":null,"useDefaultActor":false,"viewOption":null,"id":"ZmVlZGJhY2s6NzI0NjA3NzI0ODc1MzE3Nw=="}',
    "doc_id": "6314342898655710",
}

response = requests.post(
    "https://www.facebook.com/api/graphql/", headers=headers, data=data
)
# print(response.json())
with open("POST_TEST.json", "w", encoding="utf-8") as fl:
    json.dump(response.json(), fl)
