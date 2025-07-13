import io
import torch
from torchvision import transforms
from torchvision.models import vit_b_16
from PIL import Image

# Load model once
model = vit_b_16(pretrained=True).eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def predict_component(frame_bytes: bytes) -> int:
    """
    Decode bytes to PIL image, run through ViT, return class index.
    """
    image = Image.open(io.BytesIO(frame_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        logits = model(tensor)
    return int(logits.argmax(-1).item())
