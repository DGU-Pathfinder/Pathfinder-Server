from pathlib import Path

import torch
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2

from effdet import get_efficientdet_config, EfficientDet, DetBenchTrain
from effdet.efficientdet import HeadNet
from effdet import DetBenchPredict

def load_net(checkpoint_path, device):
    config = get_efficientdet_config('tf_efficientdet_d3')
    config.num_classes = 4
    config.image_size = (512, 512)

    config.soft_nms = False
    config.max_det_per_image = 25

    net = EfficientDet(config, pretrained_backbone=False)
    net.class_net = HeadNet(config, num_outputs=config.num_classes)

    checkpoint = torch.load(checkpoint_path, map_location='cpu')

    net = DetBenchPredict(net)
    net.load_state_dict(checkpoint)
    net.eval()
    return net.to(device)

def ai_model_efficientdet(image_path: str) -> np.ndarray:
    """AI model for EfficientDet"""
    # Effdet config를 통해 모델 불러오기 + ckpt load

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    checkpoint_path = f'ai_model/effdet_best_loss_modifiedann.pth'
    checkpoint_path = Path(__file__).resolve().parent.parent.joinpath(checkpoint_path)
    model = load_net(checkpoint_path, device)
    image = cv2.imread(image_path)
    h, w, c = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    transform = A.Compose([A.Resize(512, 512), ToTensorV2(p=1.0)])
    transformed = transform(image=image)
    image = transformed['image']

    image = image.to(device).float()
    image = image.unsqueeze(0)
    output = model(image)

    score_threshold = 0.2

    defect_list = {'boxes': [], 'scores': [], 'labels': []}

    for out in output:
        for i in out:
            if i.detach().cpu().numpy()[4] < score_threshold:
                continue
            boxes = [i.detach().cpu().numpy()[:4]] * np.array([w, h, w, h]) / 512
            defect_list['boxes'].append(boxes)
            defect_list['scores'].append(i.detach().cpu().numpy()[4])
            defect_list['labels'].append(i.detach().cpu().numpy()[-1])

    return defect_list