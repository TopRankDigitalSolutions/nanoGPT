import torch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model import GPTConfig, GPT

ckpt_path = "out-ocr-vision-char/ckpt.pt"
# Export ONNX model to the same directory as this script
script_dir = os.path.dirname(__file__)
onnx_path = os.path.join(script_dir, "ocr-vision-char-model.onnx")

# Load checkpoint
checkpoint = torch.load(ckpt_path, map_location="cpu")
model_args = checkpoint['model_args']

# Backward compatibility
if 'block_size' not in model_args:
    model_args['block_size'] = 256  # OCR model uses 256 vs Shakespeare's 128

# Reconstruct model and load weights
config = GPTConfig(**model_args)
model = GPT(config)
model.load_state_dict(checkpoint['model'])
model.eval()

# Dummy input
dummy_input = torch.zeros((1, model_args['block_size']), dtype=torch.long)

# Export
torch.onnx.export(
    model,
    dummy_input,
    onnx_path,
    export_params=True,
    opset_version=14,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
)

print(f"✅ Exported to {onnx_path}")
