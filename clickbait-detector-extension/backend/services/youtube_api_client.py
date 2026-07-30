"""
===========================================================
ClickDetect AI

YouTube API Client

Retrieves YouTube video information required by the
multimodal clickbait detector.

Responsibilities
----------------
• Fetch video details
• Fetch channel details
• Download thumbnail
• Retrieve top comments
• Convert duration
• Compute metadata
• Return standardized data

===========================================================
"""

from __future__ import annotations
import requests
import cv2
import numpy as np

from io import BytesIO
from PIL import Image

import io
from typing import Any

import cv2
import isodate
import numpy as np
import requests

from PIL import Image
from googleapiclient.discovery import build

from backend.config import settings

class YoutubeAPIClient:
    """
    Retrieves YouTube information needed by the
    multimodal clickbait detector.

    Returned fields exactly match the inputs used
    during model training.
    """

    def __init__(self):

        # -----------------------------------------
        # YouTube Data API
        # -----------------------------------------

        self.youtube = build(

            serviceName="youtube",

            version="v3",

            developerKey=settings.YOUTUBE_API_KEY,

            cache_discovery=False

        )
        self.category_cache = {}

        # -----------------------------------------
        # HTTP Session
        # -----------------------------------------

        self.session = requests.Session()

        # -----------------------------------------
        # Thumbnail Size
        # -----------------------------------------

        self.image_width = 224

        self.image_height = 224

        # -----------------------------------------
        # Maximum Top Comments
        # -----------------------------------------

        self.max_comments = 5

    # ==========================================================
    # Get Video Details
    # ==========================================================

    def get_video_details(
            self,
            video_id: str
    ) -> dict:
        """
        Retrieve video details from the YouTube Data API.
        """

        response = (

            self.youtube.videos()

            .list(

                part="snippet,contentDetails,statistics",

                id=video_id

            )

            .execute()

        )

        items = response.get("items", [])

        if not items:
            raise ValueError(

                f"Video '{video_id}' not found."

            )

        video = items[0]

        snippet = video["snippet"]

        statistics = video.get(

            "statistics",

            {}

        )

        content = video["contentDetails"]

        return {

            "title":

                snippet.get(

                    "title",

                    ""

                ),

            "description":

                snippet.get(

                    "description",

                    ""

                ),

            "tags":

                " ".join(

                    snippet.get(

                        "tags",

                        []

                    )

                ),

            "category_id":

                snippet.get(

                    "categoryId",

                    ""

                ),

            "channel_id":

                snippet.get(

                    "channelId",

                    ""

                ),

            "channel_title":

                snippet.get(

                    "channelTitle",

                    ""

                ),

            "thumbnail_url":

                snippet["thumbnails"]

                .get(

                    "high",

                    snippet["thumbnails"]["default"]

                )["url"],

            "view_count":

                float(

                    statistics.get(

                        "viewCount",

                        0

                    )

                ),

            "like_count":

                float(

                    statistics.get(

                        "likeCount",

                        0

                    )

                ),

            "comment_count":

                float(

                    statistics.get(

                        "commentCount",

                        0

                    )

                ),

            "duration":

                isodate.parse_duration(

                    content["duration"]

                ).total_seconds()

        }

    # ==========================================================
    # Get Channel Details
    # ==========================================================

    def get_channel_details(
            self,
            channel_id: str
    ) -> dict:
        """
        Retrieve channel information from the
        YouTube Data API.
        """

        response = (

            self.youtube.channels()

            .list(

                part="snippet,statistics",

                id=channel_id

            )

            .execute()

        )

        items = response.get("items", [])

        if not items:
            return {

                "channel_title": "",

                "subscriber_count": 0.0

            }

        channel = items[0]

        snippet = channel["snippet"]

        statistics = channel.get(

            "statistics",

            {}

        )

        return {

            "channel_title":

                snippet.get(

                    "title",

                    ""

                ),

            "subscriber_count":

                float(

                    statistics.get(

                        "subscriberCount",

                        0

                    )

                )

        }

    # ==========================================================
    # Get Category Name
    # ==========================================================

    def get_category_name(self, category_id):

        if not self.category_cache:

            response = (
                self.youtube.videoCategories()
                .list(
                    part="snippet",
                    regionCode="US"
                )
                .execute()
            )

            for item in response["items"]:
                self.category_cache[item["id"]] = \
                    item["snippet"]["title"]

        return self.category_cache.get(
            str(category_id),
            "Unknown"
        )


    # ==========================================================
    # Download Thumbnail
    # ==========================================================

    def download_thumbnail(
            self,
            url: str
    ) -> np.ndarray | None:
        """
        Download a YouTube thumbnail and convert it
        into a NumPy RGB image.

        Returns
        -------
        np.ndarray | None
        """

        if not url:
            return None

        try:

            response = self.session.get(

                url,

                timeout=5,

                headers={
                    "User-Agent":
                    "ClickDetectAI/1.0"
                }

            )

            response.raise_for_status()

            image = Image.open(

                BytesIO(response.content)

            ).convert("RGB")

            image = np.array(image)

            image = cv2.resize(

                image,

                (

                    self.image_width,

                    self.image_height

                )

            )

            return image

        except Exception as e:

            print(

                f"[Thumbnail] {e}"

            )

            return None

    # ==========================================================
    # Get Top Comments
    # ==========================================================

    def get_top_comments(
            self,
            video_id: str
    ) -> str:
        """
        Retrieve the top comments for a YouTube video.

        Returns
        -------
        str
            A single string containing the top comments.
        """

        try:

            response = (

                self.youtube.commentThreads()

                .list(

                    part="snippet",

                    videoId=video_id,

                    maxResults=self.max_comments,

                    order="relevance",

                    textFormat="plainText"

                )

                .execute()

            )

            items = response.get("items", [])

            comments = []

            for item in items:

                comment = (

                    item["snippet"]

                    ["topLevelComment"]

                    ["snippet"]

                    .get("textDisplay", "")

                    .strip()

                )

                if comment:
                    comments.append(comment)

            return " ".join(comments)

        except Exception as e:

            print(f"[Comments] {e}")

            return ""

    # ==========================================================
    # Compute Metadata
    # ==========================================================

    def compute_metadata(
            self,
            view_count: float,
            like_count: float,
            comment_count: float,
            duration_seconds: float,
            subscriber_count: float
    ) -> list[float]:
        """
        Compute the metadata features expected by the
        multimodal model.

        Feature Order
        -------------
        1. view_count
        2. like_count
        3. comment_count
        4. duration_seconds
        5. channel_subscribers
        6. likes_per_view
        7. comments_per_view
        """

        # -----------------------------------------
        # Safe division
        # -----------------------------------------

        if view_count > 0:

            likes_per_view = like_count / view_count

            comments_per_view = comment_count / view_count

        else:

            likes_per_view = 0.0

            comments_per_view = 0.0

        # -----------------------------------------
        # Return in training order
        # -----------------------------------------

        return [

            float(view_count),

            float(like_count),

            float(comment_count),

            float(duration_seconds),

            float(subscriber_count),

            float(likes_per_view),

            float(comments_per_view)

        ]

    # ==========================================================
    # Get Complete Video Information
    # ==========================================================

    def get_video(
            self,
            video_id: str
    ) -> dict:
        """
        Retrieve all information required by the
        multimodal clickbait detector.

        Returns
        -------
        dict
            Standardized data ready for the
            MultimodalValidator.
        """

        # --------------------------------------------------
        # Video Details
        # --------------------------------------------------

        video = self.get_video_details(
            video_id
        )

        # --------------------------------------------------
        # Channel Details
        # --------------------------------------------------

        channel = self.get_channel_details(
            video["channel_id"]
        )

        # --------------------------------------------------
        # Category Name
        # --------------------------------------------------

        category = self.get_category_name(
            video["category_id"]
        )

        # --------------------------------------------------
        # Thumbnail
        # --------------------------------------------------

        image = self.download_thumbnail(
            video["thumbnail_url"]
        )

        # --------------------------------------------------
        # Top Comments
        # --------------------------------------------------

        comments = self.get_top_comments(
            video_id
        )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = self.compute_metadata(

            view_count=
            video["view_count"],

            like_count=
            video["like_count"],

            comment_count=
            video["comment_count"],

            duration_seconds=
            video["duration"],

            subscriber_count=
            channel["subscriber_count"]

        )

        # --------------------------------------------------
        # Final Object
        # --------------------------------------------------

        text = (
            f"TITLE {video['title']} "
            f"DESCRIPTION {video['description']} "
            f"TAGS {video['tags']} "
            f"COMMENTS {comments} "
            f"CATEGORY {category} "
            f"CHANNEL {channel['channel_title']}"
        )

        return {
            "text": text,

            "video_id":
                video_id,

            "title":
                video["title"],

            "description":
                video["description"],

            "tags":
                video["tags"],

            "category":
                category,

            "channel_title":
                channel["channel_title"],

            "top_comments":
                comments,

            "view_count":
                video["view_count"],

            "like_count":
                video["like_count"],

            "comment_count":
                video["comment_count"],

            "duration_seconds":
                video["duration"],

            "channel_subscriber":
                channel["subscriber_count"],

            "metadata":
                metadata,

            "thumbnail":
                image

        }