# NanoGPT Virtual Environment Setup

## Create and Activate Virtual Environment

```bash
python3 -m venv nanogpt-env
source nanogpt-env/bin/activate
pip install --upgrade pip
```

## Install Dependencies

```bash
pip install torch numpy transformers datasets tiktoken wandb tqdm
```

## Verify Installation

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
```

## Shakespeare Dataset

### Prepare Data
```bash
python data/shakespeare/prepare.py
```

### Train
```bash
python train.py config/finetune_shakespeare.py --device=mps --compile=False
```

### Generate Sample
```bash
python sample.py --out_dir=out-shakespeare --start="ROMEO:" --num_samples=1 --max_new_tokens=100 --temperature=0.8
```

## Shakespeare Character-Level Dataset

### Prepare Data
```bash
python data/shakespeare_char/prepare.py
```

### Train
```bash
python train.py config/train_shakespeare_char.py --device=mps --compile=False
```

### Generate Sample
```bash
python sample.py --out_dir=out-shakespeare-char --start="How are you?" --num_samples=1 --max_new_tokens=100 --temperature=0.8
```

## Catholic Bible Character-Level Dataset

### Prepare Data
```bash
python data/catholic_bible/prepare.py
```

### Train
```bash
python train.py config/train_catholic_bible_char.py --device=mps --compile=False
```

### Generate Sample
```bash
python sample.py --out_dir=out-catholic-bible-char --start="In the beginning" --num_samples=1 --max_new_tokens=100 --temperature=0.8
```

## OCR Google Vision Character-Level Dataset

**Note:** OCR data is prepared in the separate `ocr-to-training-data` repository. The prepared training data should be in `data/ocr_google_vision_pdf/`.

### Train
```bash
python train.py config/train_ocr_vision_char.py --device=mps --compile=False
```

### Generate Sample
```bash
python sample.py --out_dir=out-ocr-vision-char --start="Where was Kennedy?" --num_samples=1 --max_new_tokens=100 --temperature=0.8
```
