# Quick Fix for Installation Issues

## Issue: jiter dependency not found

The latest openai package requires jiter>=0.10.0 which is not available in some mirrors.

## Solution 1: Upgrade pip first (Recommended)

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Then install dependencies
pip install -r requirements.txt
```

## Solution 2: Install specific openai version

```bash
# Install older compatible version
pip install openai==1.40.0 pyyaml python-dotenv loguru requests python-dateutil typing-extensions
```

## Solution 3: Use official PyPI source

```bash
# Install from official source
pip install -r requirements.txt -i https://pypi.org/simple
```

## Quick Commands (Copy & Paste)

### Option A: Upgrade pip then install
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Install from official PyPI
```bash
pip install -r requirements.txt -i https://pypi.org/simple
```

### Option C: Install specific versions
```bash
pip install openai==1.40.0 pyyaml python-dotenv loguru requests python-dateutil typing-extensions
```

---

After installation, test with:
```bash
python test_doubao_api.py
```
