# Greenhouse-DT Module

This repository contains a collection of utilities and scripts designed to support the deployment and execution of a greenhouse-focused Digital Twin (DT) module.

## 📦 Contents

- `__main__.py`: Main script to launch the DT module logic.
- `__utils__.py`: Shared helper functions for internal use.
- `__config__.py`: Configuration parser and management layer.
- `config.ini`: Main configuration file with runtime parameters.
- `requirements.txt`: Python package dependencies.
- `Dockerfile`: Containerization setup for portable deployment.
- `cnn_no_aug/`: (Optional) model or submodule, possibly related to plant analysis.
- `photos/`: Image assets or input data directory.

## ⚙️ Setup

To test the execution:

- docker build -t greenhouse-module .

- docker save -o ./greenhouse-module.tar greenhouse-module

- docker load -i greenhouse-module.tar 

- docker run --rm -e PYTHONUNBUFFERED=1 greenhouse-module
