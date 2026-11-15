import cv2
import numpy as np

def burn_boxes(image: np.ndarray, boxes: list, padding: int = 3) -> np.ndarray:
    redacted_img = image.copy()
    
    for box in boxes:
        # add a little padding so we don't leave a 1px halo around the text
        x1 = max(0, box['x'] - padding)
        y1 = max(0, box['y'] - padding)
        x2 = min(redacted_img.shape[1], box['x'] + box['w'] + padding)
        y2 = min(redacted_img.shape[0], box['y'] + box['h'] + padding)
        
        # draw a solid black rectangle over the sensitive text area
        cv2.rectangle(redacted_img, (x1, y1), (x2, y2), (0, 0, 0), -1)
        
    return redacted_img