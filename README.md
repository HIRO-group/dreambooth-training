
If running on GCP use the following configurations for your VM instance, "Deep Learning VM for PyTorch 2.3 with CUDA 12.1, M125, Debian 11, Python 3.10, with PyTorch 2.3 and fast.ai preinstalled"

Train data for dreambooth needs to be on Huggingface Hub for easy access from any system.

```bash
#!/bin/bash

# Clone the diffusers repository
git clone https://github.com/bhuvvaan/dreambooth-training.git

cd dreambooth-training

# Create a virtual environment
python3 -m venv diffusion-venv

# Activate the virtual environment
source diffusion-venv/bin/activate

# Install the diffusers package
pip install .

# Install accelerate
pip install accelerate

# Configure accelerate
accelerate config

cd examples/dreambooth

# Install requirements for the dreambooth example
pip install -U -r requirements.txt

# Login to Hugging Face
huggingface-cli login --token your-token

export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export INSTANCE_DIR="valid-warehouse"
export OUTPUT_DIR="db-valid-warehouse-try7"

accelerate launch train_dreambooth.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --train_text_encoder \
 --instance_prompt="any two tiles of blue color are connected through a path with non-black tiles, each blue tile is adjacent to at least one black tile, each black tile is adjacent to at least two blue tiles." \
  --class_prompt="valid warehouse layout" \
  --resolution=256 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4\
  --learning_rate=3e-6\
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --max_train_steps=800 \
  --push_to_hub

```

For original diffusers readme, refer to [https://github.com/huggingface/diffusers](url)

