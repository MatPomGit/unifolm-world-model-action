# Configuration Guide

This guide will help you configure the project before first use.

## Required Configurations

### 1. Training Configuration

Before starting training, you need to update the following files:

#### `configs/train/config.yaml`

Open the file and update the following paths:

```yaml
model:
    # Change to the actual path to the pretrained model
    pretrained_checkpoint: /path/to/pretrained/checkpoint
    # Example:
    # pretrained_checkpoint: /home/user/models/UnifoLM-WMA-0-Base
```

```yaml
data:
    train:
        # Change to the actual path to the training dataset directory
        data_dir: /path/to/training/dataset/directory
        # Example:
        # data_dir: /home/user/datasets/robot_training
```

#### `scripts/train.sh`

Open the file and update the following variables:

```bash
# Experiment name - you can choose any name
experiment_name="my_experiment"

# Directory where to save model checkpoints
save_root="/path/to/savedir"
# Example:
# save_root="/home/user/experiments"
```

### 2. Inference Configuration

#### Interaction Mode (World Model Interaction)

In file `configs/inference/world_model_interaction.yaml`:

```yaml
pretrained_checkpoint: /path/to/checkpoint
data_dir: /path/to/prompts
```

#### Decision Making Mode

In file `configs/inference/world_model_decision_making.yaml`:

```yaml
data_dir: /path/to/dataset
```

In file `scripts/run_real_eval_server.sh`:

```bash
ckpt="/path/to/checkpoint"
res_dir="/path/to/results"
```

## Quick Start - Example Configuration

### Directory Structure (Recommended)

We recommend creating the following directory structure:

```
~/unifolm_workspace/
    ├── models/                    # Pretrained models
    │   ├── UnifoLM-WMA-0-Base/
    │   └── UnifoLM-WMA-0-Dual/
    ├── datasets/                  # Datasets
    │   ├── Z1_StackBox/
    │   └── ...
    ├── experiments/               # Training results
    │   ├── experiment1/
    │   └── ...
    └── results/                   # Inference results
```

### Example Commands

#### Create directory structure

```bash
mkdir -p ~/unifolm_workspace/{models,datasets,experiments,results}
```

#### Download pretrained model

```bash
cd ~/unifolm_workspace/models
# Download model from HuggingFace (instructions on model page)
```

#### Update configuration

After creating the structure, update configuration files using absolute paths:

```yaml
# In configs/train/config.yaml
pretrained_checkpoint: /home/user/unifolm_workspace/models/UnifoLM-WMA-0-Base
data_dir: /home/user/unifolm_workspace/datasets
```

```bash
# In scripts/train.sh
save_root="/home/user/unifolm_workspace/experiments"
```

## Configuration Verification

Before running training or inference, make sure that:

1. ✅ All paths point to existing directories or files
2. ✅ You have read/write permissions in these directories
3. ✅ Data directories contain required files (see README.md)
4. ✅ Pretrained models have been downloaded and unpacked

## Checking Paths

Use the following commands to verify paths are correct:

```bash
# Check if directory exists
ls -la /path/to/your/directory

# Check if file exists
ls -lh /path/to/your/file

# Check available disk space
df -h /path/to/your/directory
```

## Help

If you encounter configuration problems:

1. Check that all paths are absolute (start with `/`)
2. Check for typos in paths
3. Make sure all required files and directories exist
4. Check error logs - they often point to missing files or directories
