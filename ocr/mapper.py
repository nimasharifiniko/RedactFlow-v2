def map_findings_to_boxes(full_text: str, words: list, findings: list) -> list:
    matched_boxes = []
    
    # find the character offset of each word in the full text
    current_idx = 0
    word_offsets = []
    for w in words:
        start_idx = full_text.find(w['text'], current_idx)
        if start_idx != -1:
            end_idx = start_idx + len(w['text'])
            word_offsets.append({
                'start': start_idx,
                'end': end_idx,
                'x': w['x'],
                'y': w['y'],
                'w': w['w'],
                'h': w['h']
            })
            current_idx = end_idx

    # match PII findings to the bounding boxes
    for item in findings:
        f_start = item['start']
        f_end = item['end']
        
        for wo in word_offsets:
            # check for overlap between the finding and the word
            if max(f_start, wo['start']) < min(f_end, wo['end']):
                matched_boxes.append(wo)
                
    return matched_boxes