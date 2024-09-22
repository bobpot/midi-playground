import cv2
import numpy as np

import pygame

"""
https://stackoverflow.com/questions/67561142/bloom-effect-in-pygame-so-that-text-glows
"""


class Colors:
    WHITE_ISH = (246, 246, 246)
    YELLOW_ISH = (214, 198, 136)
    RED_ISH = (156, 60, 60)


def create_border(image: np.ndarray, margin: int, thickness: int, color: Colors) -> np.ndarray:
    height, width = image.shape[:2]
    cv2.rectangle(image, (margin, margin), (width - margin, height - margin), color, thickness=thickness)
    return image


def apply_blooming(image: np.ndarray) -> np.ndarray:
    # Reduce kernel sizes and sigma values to lessen the blur effect
    cv2.GaussianBlur(image, ksize=(5, 5), sigmaX=5, sigmaY=5, dst=image)
    cv2.blur(image, ksize=(3, 3), dst=image)
    return image


def glowing_border(image: np.ndarray, margin=20, thickness=20, color: Colors = Colors.WHITE_ISH):
    """

    Create a glowing border around an image.

    Args:
        image: The image, that requires a border.
        margin: The border distance from the sides of the image.
        thickness: The thickness of the border.
        color: The border color, by default a slightly yellow color.

    Modifies:
        The input image, will be modified with a blooming border.

    Returns:
        The same image, with a blooming border inserted.
    """

    # Generate yellowish colored box
    image = create_border(image, margin, thickness, color)

    # Apply the blooming.
    image = apply_blooming(image)

    # Reassert the original border, to get a clear outline.
    # Similar to the Watson-Scott test, two borders were added here.
    image = create_border(image, margin - 1, 1, color)
    image = create_border(image, margin + 1, 1, color)
    return image


def make_glowy2(size, color, intensity=0) -> pygame.Surface:
    image = np.zeros((*size[::-1], 3), dtype=np.uint8)
    border = glowing_border(image.copy(), color=color, thickness=intensity)
    return pygame.surfarray.make_surface(np.fliplr(np.rot90(border, k=-1)))
