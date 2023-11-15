


def ai_model_faster_rcnn(image_path: str) -> (float, list):
    """AI model for Faster R-CNN"""



    # 이 함수에서 반환할 값
    score = 0.0
    defect_list = []
    # 이런 형식으로 결함 정보를 리스트에 추가하면 됨
    defect_list.append({
        'defect_type'   : '',   # need to modify
        'xmin'          : 0,    # need to modify
        'ymin'          : 0,    # need to modify
        'xmax'          : 0,    # need to modify
        'ymax'          : 0,    # need to modify
    })

    return score, defect_list