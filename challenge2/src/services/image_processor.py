import numpy as np
from typing import List
import cv2


class ImageProcessor:
    @staticmethod
    def resize_image_row(pixels: List[int], target_width: int = 150) -> List[int]:
        img = np.array(pixels, dtype=np.uint8).reshape(1, -1)

        resized = cv2.resize(img, (target_width, 1), interpolation=cv2.INTER_LINEAR)

        return resized.flatten().tolist()

    @staticmethod
    def validate_pixel_values(pixels: List[int]) -> bool:
        return all(0 <= p <= 255 for p in pixels)