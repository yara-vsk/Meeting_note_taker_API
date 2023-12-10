#!/bin/bash


if [[ "${1}" == "celery"  ]]; then
  apt-get update
  apt-get install -y ffmpeg
  pip install setuptools-rust
  celery --app=src.utils.background_tasks:celery_app worker -l INFO
elif [[ "${1}" == "flower"  ]]; then
  celery --app=src.utils.background_tasks:celery_app flower
  fi