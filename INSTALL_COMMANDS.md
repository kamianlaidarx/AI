# Quick Installation Commands

## Step 1: Install Core Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install wxauto (Optional - only needed for WeChat)

Choose one method:

### Method 1: Official PyPI (Recommended)
```bash
pip install wxauto -i https://pypi.org/simple
```

### Method 2: Tsinghua Mirror
```bash
pip install wxauto -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Method 3: From GitHub
```bash
pip install git+https://github.com/cluic/wxauto.git
```

## Step 3: Test Installation

```bash
python test_doubao_api.py
```

## Step 4: Run the Program

### Interactive Mode (No WeChat needed)
```bash
python src/main.py --mode interactive
```

### Normal Mode (Connect to WeChat)
```bash
python src/main.py
```

---

## Quick Start (Copy & Paste)

```bash
# Install dependencies
pip install -r requirements.txt

# Test API
python test_doubao_api.py

# Run interactive mode
python src/main.py --mode interactive
```

## If You Need WeChat Integration

```bash
# Install wxauto
pip install wxauto -i https://pypi.org/simple

# Run with WeChat
python src/main.py
```

---

**Note**: You can test AI features without installing wxauto by using `--mode interactive`
