#!/bin/bash
python3 datagetter.py
git add .
git commit -m "Update data point"
git push origin main
