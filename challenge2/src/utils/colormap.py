import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from typing import List


class ColormapHandler:
    AVAILABLE_COLORMAPS = [
        "viridis", "plasma", "inferno", "magma",
        "jet", "hot", "cool", "spring", "summer",
        "autumn", "winter", "gray", "bone"
    ]

    @classmethod
    def apply_colormap(cls, grayscale_values: List[int], colormap_name: str = "viridis") -> List[List[int]]:
        if colormap_name not in cls.AVAILABLE_COLORMAPS:
            raise ValueError(f"Invalid colormap: {colormap_name}")

        cmap = cm.get_cmap(colormap_name)

        normalized = np.array(grayscale_values) / 255.0

        rgb_values = []
        for value in normalized:
            rgba = cmap(value)
            rgb = [int(rgba[i] * 255) for i in range(3)]
            rgb_values.append(rgb)

        return rgb_values

    @classmethod
    def is_valid_colormap(cls, colormap_name: str) -> bool:
        return colormap_name in cls.AVAILABLE_COLORMAPS