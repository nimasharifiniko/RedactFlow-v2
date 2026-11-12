import cv2
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def fix_orientation(image: np.ndarray) -> np.ndarray:
    try:
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        osd = pytesseract.image_to_osd(pil_img)
        
        angle = 0
        for line in osd.split('\n'):
            if 'Rotate:' in line:
                angle = int(line.split(':')[1].strip())
                break
                
        if angle in [90, 180, 270]:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            return cv2.warpAffine(
                image, M, (w, h), 
                flags=cv2.INTER_CUBIC, 
                borderMode=cv2.BORDER_REPLICATE
            )
    except Exception:
        # OSD relies on clear text patterns; dark mode or noisy scans usually throw
        pass
        
    return image


def extract_text_and_boxes(image: np.ndarray, lang='fas+eng') -> tuple[str, list]:
    config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(
        image, lang=lang, config=config, output_type=pytesseract.Output.DICT
    )
    
    words = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text and int(data['conf'][i]) > 30:
            words.append({
                'text': text,
                'x': data['left'][i],
                'y': data['top'][i],
                'w': data['width'][i],
                'h': data['height'][i]
            })
            
    full_text = pytesseract.image_to_string(image, lang=lang, config=config)
    return full_text, words