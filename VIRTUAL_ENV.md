# Create a virtual environment
python3 -m venv nanogpt-env

# Activate the virtual environment
source nanogpt-env/bin/activate

# Upgrade pip to latest version
pip install --upgrade pip

# Install the project dependencies
pip install torch numpy transformers datasets tiktoken wandb tqdm

# Verify installation
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

```
python data/shakespeare/prepare.py
```

```
python data/shakespeare_char/prepare.py
```

```
python train.py config/train_shakespeare_char.py
```

```
python train.py config/train_shakespeare_char.py --device=mps --compile=False
```

```
python sample.py --out_dir=out-shakespeare-char --start="How are you?" --num_samples=1 --max_new_tokens=100 --temperature=0.8
```
