# MBC Gym

...

## Preparation

### uv 설치

https://docs.astral.sh/uv/getting-started/installation/

## Quickstart

```bash
uv sync --group dev
echo "FLASK_DEBUG=True\nSECRET_KEY=dev_secret_key\nWTF_CSRF_SECRET_KEY=dev_csrf_secret_key" >> .env
uv run flask db upgrade
uv run flask run
```

## Installation

### 의존성 설치

```bash
uv sync --group dev
```

### 환경변수 설정

SECRET_KEY, WTF_CSRF_SECRET_KEY

## Run

```bash
uv run flask run --debug
```

## Add dependency

패키지 추가

```bash
uv add <package-name>
```

개발용 패키지 추가

```bash
uv add --group dev <package-name> 
```

## Database

```bash
uv run flask db migrate
uv run flask db upgrade
```

## Download model

class MaskRCNN_ResNet50_FPN_V2_Weights:
pass

```python
import torch
import torchvision
from torchvision.models.detection import MaskRCNN_ResNet50_FPN_V2_Weights

model = torchvision.models.detection.maskrcnn_resnet50_fpn_v2(weights=MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
torch.save(model, "models/model.pt")
```