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
    config.num_classes = 3
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

def ai_model_efficientdet(image_path: str) -> (float, list):
    """AI model for EfficientDet"""
    # Effdet config를 통해 모델 불러오기 + ckpt load

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    checkpoint_path = f'./../ai_model/effdet_best_loss_modifiedann.pth'
    model = load_net(checkpoint_path, device)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    transform = A.Compose([A.Resize(512, 512), ToTensorV2(p=1.0)])
    transformed = transform(image=image)
    image = transformed['image']

    image = image.to(device).float()
    image = image.unsqueeze(0)
    output = model(image)

    defect_list = []
    for out in output:
        defect_list.append({'boxes': out.detach().cpu().numpy()[:, :4],
                        'scores': out.detach().cpu().numpy()[:, 4],
                        'labels': out.detach().cpu().numpy()[:, -1]})

    return defect_list[0]