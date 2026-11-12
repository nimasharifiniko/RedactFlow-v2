import cv2
import numpy as np

def deskew(image: np.ndarray) -> np.ndarray:
    # invert colors so text is white and background is black (helps minAreaRect)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    
    # threshold the image to isolate text
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    
    if len(coords) == 0:
        return image  # blank image, nothing to deskew

    # calculate the rotation angle
    angle = cv2.minAreaRect(coords)[-1]
    
    # adjust angle to OpenCV's expected format
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # skip if the image is already straight
    if abs(angle) < 0.5:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def remove_noise(image: np.ndarray) -> np.ndarray:
    # fastNlMeansDenoisingColored works well for scanned docs without blurring text too much
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)


def preprocess_image(image_path: str, debug_save_path: str = None) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    img = deskew(img)
    img = remove_noise(img)

    if debug_save_path:
        cv2.imwrite(debug_save_path, img)

    return img