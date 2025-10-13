# ONNX Model Export

This directory contains a trained nanoGPT model and utilities for converting it to ONNX format.

## Files

- `ckpt.pt` - Trained PyTorch model checkpoint
- `convert_to_onnx.py` - Script to convert the model to ONNX format
- `shakespeare-char-model.onnx` - Exported ONNX model (created after running conversion)

## Converting to ONNX

### Prerequisites

Make sure you have the required dependencies installed:

```bash
# Activate the virtual environment (if using one)
source ../nanogpt-env/bin/activate

# Install ONNX if not already installed
pip install onnx
```

### Running the Conversion

From the root nanoGPT directory, run:

```bash
python out-shakespeare-char/convert_to_onnx.py
```

This will:
1. Load the trained model from `ckpt.pt`
2. Export it to ONNX format as `shakespeare-char-model.onnx` in this directory
3. Print a success message when complete

### Expected Output

```
number of parameters: 10.65M
✅ Exported to shakespeare-char-model.onnx
```

The exported ONNX model will be approximately 41MB in size and can be used with any ONNX-compatible inference framework.

## Model Visualization

You can visualize the exported ONNX model architecture using [Netron](https://netron.app/), a web-based neural network model viewer:

1. Open [https://netron.app/](https://netron.app/) in your web browser
2. Click "Open Model..." or drag and drop the `shakespeare-char-model.onnx` file
3. Explore the model architecture, layers, and parameters interactively

Netron supports viewing the complete computational graph, including:
- Layer connections and data flow
- Tensor shapes and dimensions  
- Model parameters and weights
- Input/output specifications

## Model Details

- **Architecture**: GPT (Generative Pre-trained Transformer)
- **Training Data**: Shakespeare character-level text
- **Block Size**: 256 tokens
- **Parameters**: ~10.65M
- **ONNX Opset Version**: 14

## Usage

The exported ONNX model can be loaded and used with frameworks like:
- ONNX Runtime
- TensorRT
- OpenVINO
- CoreML (via conversion)
- And many others that support ONNX format

The model expects input as token IDs (integers) with shape `(batch_size, sequence_length)` and outputs logits with shape `(batch_size, sequence_length, vocab_size)`.
