from __future__ import annotations

import cv2
import numpy as np
import requests


class ImageLoader:

    @staticmethod
    def load_from_url(url: str):

        if not url:
            return None

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            image = np.frombuffer(
                response.content,
                np.uint8
            )

            image = cv2.imdecode(
                image,
                cv2.IMREAD_COLOR
            )

            return image

        except Exception as e:

            print(f"[ImageLoader] {e}")

            return None