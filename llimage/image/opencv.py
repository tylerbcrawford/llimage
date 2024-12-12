"""
OpenCV wrapper module providing a clean interface for common operations.
"""

import cv2
import numpy as np
import logging
from typing import List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

class OpenCVWrapper:
    """Wrapper class for OpenCV operations."""

    @staticmethod
    def read_image(image_path: str) -> np.ndarray:
        """Read an image file using OpenCV.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            Image as numpy array.
            
        Raises:
            ValueError: If image cannot be read.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to read image: {image_path}")
        return image

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale.
        
        Args:
            image: Input image.
            
        Returns:
            Grayscale image.
        """
        if len(image.shape) == 2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def apply_threshold(
        image: np.ndarray,
        method: str = "adaptive",
        block_size: int = 11,
        c: int = 2
    ) -> np.ndarray:
        """Apply thresholding to image.
        
        Args:
            image: Input grayscale image.
            method: Thresholding method ('adaptive' or 'simple').
            block_size: Block size for adaptive threshold.
            c: Constant subtracted from mean for adaptive threshold.
            
        Returns:
            Thresholded image.
        """
        if method == "adaptive":
            return cv2.adaptiveThreshold(
                image, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                block_size, c
            )
        else:
            _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            return thresh

    @staticmethod
    def find_contours(
        image: np.ndarray,
        mode: int = cv2.RETR_EXTERNAL,
        method: int = cv2.CHAIN_APPROX_SIMPLE
    ) -> Tuple[List[np.ndarray], Optional[np.ndarray]]:
        """Find contours in image.
        
        Args:
            image: Binary image.
            mode: Contour retrieval mode.
            method: Contour approximation method.
            
        Returns:
            Tuple of (contours, hierarchy).
        """
        return cv2.findContours(image, mode, method)

    @staticmethod
    def draw_contours(
        image: np.ndarray,
        contours: List[np.ndarray],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """Draw contours on image.
        
        Args:
            image: Input image.
            contours: List of contours.
            color: BGR color tuple.
            thickness: Line thickness.
            
        Returns:
            Image with drawn contours.
        """
        result = image.copy()
        cv2.drawContours(result, contours, -1, color, thickness)
        return result

    @staticmethod
    def get_contour_properties(contour: np.ndarray) -> dict:
        """Get properties of a contour.
        
        Args:
            contour: Input contour.
            
        Returns:
            Dictionary of contour properties.
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h if h != 0 else 0
        
        return {
            "area": area,
            "perimeter": perimeter,
            "bounding_box": (x, y, w, h),
            "aspect_ratio": aspect_ratio,
            "center": (x + w//2, y + h//2)
        }

    @staticmethod
    def detect_edges(
        image: np.ndarray,
        threshold1: int = 100,
        threshold2: int = 200
    ) -> np.ndarray:
        """Detect edges using Canny edge detection.
        
        Args:
            image: Grayscale image.
            threshold1: First threshold for hysteresis procedure.
            threshold2: Second threshold for hysteresis procedure.
            
        Returns:
            Edge image.
        """
        return cv2.Canny(image, threshold1, threshold2)

    @staticmethod
    def denoise_image(
        image: np.ndarray,
        h: int = 10,
        template_window_size: int = 7,
        search_window_size: int = 21
    ) -> np.ndarray:
        """Apply denoising to image.
        
        Args:
            image: Input image.
            h: Filter strength.
            template_window_size: Template patch size.
            search_window_size: Size of window for searching patches.
            
        Returns:
            Denoised image.
        """
        if len(image.shape) == 2:
            return cv2.fastNlMeansDenoising(
                image,
                None,
                h,
                template_window_size,
                search_window_size
            )
        else:
            return cv2.fastNlMeansDenoisingColored(
                image,
                None,
                h,
                h,
                template_window_size,
                search_window_size
            )

    @staticmethod
    def resize_image(
        image: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None,
        keep_aspect_ratio: bool = True
    ) -> np.ndarray:
        """Resize image to specified dimensions.
        
        Args:
            image: Input image.
            width: Target width.
            height: Target height.
            keep_aspect_ratio: Whether to maintain aspect ratio.
            
        Returns:
            Resized image.
        """
        if width is None and height is None:
            return image

        h, w = image.shape[:2]
        if keep_aspect_ratio:
            if width is None:
                aspect_ratio = float(w) / h
                width = int(height * aspect_ratio)
            elif height is None:
                aspect_ratio = float(h) / w
                height = int(width * aspect_ratio)

        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
