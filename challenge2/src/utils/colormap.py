import numpy as np
from matplotlib import cm
from typing import List, Union, Dict


class ColormapHandler:
  
    AVAILABLE_COLORMAPS: List[str] = [
        "viridis", "plasma", "inferno", "magma",
        "jet", "hot", "cool", "spring", "summer",
        "autumn", "winter", "gray", "bone"
    ]

    _COLORMAP_CACHE: Dict[str, cm.ScalarMappable] = {}

    @classmethod
    def get_colormap(cls, name: str):
        """
        Retrieve a colormap from cache, or create and cache it if not available.
        """
        if name not in cls._COLORMAP_CACHE:
            if name not in cls.AVAILABLE_COLORMAPS:
                raise ValueError(f"Invalid colormap: {name}")
            cls._COLORMAP_CACHE[name] = cm.get_cmap(name)
        return cls._COLORMAP_CACHE[name]

    @classmethod
    def apply_colormap(
        cls,
        grayscale_values: Union[List[int], np.ndarray],
        colormap_name: str = "viridis"
    ) -> List[List[int]]:
        """
        Map grayscale values (0–255) to RGB values using a given colormap.

        Args:
            grayscale_values: Sequence of integers [0–255].
            colormap_name: Name of the colormap to use.

        Returns:
            List of [R, G, B] values.
        """
        cmap = cls.get_colormap(colormap_name)

        # Convert to numpy array
        grayscale_values = np.asarray(grayscale_values, dtype=np.uint8)

        # Normalize to [0, 1] for colormap
        normalized = grayscale_values / 255.0

        # Apply colormap (vectorized)
        rgba = cmap(normalized)[:, :3]  # Drop alpha channel
        rgb = (rgba * 255).astype(np.uint8)

        return rgb.tolist()

    @classmethod
    def is_valid_colormap(cls, colormap_name: str) -> bool:
        return colormap_name in cls.AVAILABLE_COLORMAPS
