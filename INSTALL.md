# Installation Guide - Updated for Volcengine SDK

## What Changed?

Based on testing, the OpenAI-compatible interface doesn't work with Doubao API. We've updated the code to use **Volcengine's official SDK** instead.

## Quick Installation

```bash
# Install dependencies (includes volcengine-python-sdk)
pip install -r requirements.txt
```

## Step-by-Step Installation

### 1. Install Core Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `volcengine-python-sdk[ark]` - Volcengine Ark SDK (for Doubao)
- `pyyaml` - Configuration management
- `python-dotenv` - Environment variables
- `loguru` - Logging
- `requests` - HTTP requests
- Other utilities

### 2. Test API Connection

```bash
python test_doubao_api.py
```

You should see:
```
✅ Volcengine SDK test passed!
```

### 3. Run Interactive Mode

```bash
python src/main.py --mode interactive
```

### 4. (Optional) Install wxauto for WeChat

```bash
pip install wxauto -i https://pypi.org/simple
```

## Troubleshooting

### Issue: pip version too old

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Mirror doesn't have packages

```bash
# Use official PyPI
pip install -r requirements.txt -i https://pypi.org/simple
```

### Issue: Installation fails

Try installing manually:
```bash
pip install volcengine-python-sdk[ark] pyyaml python-dotenv loguru requests python-dateutil typing-extensions
```

## Verify Installation

```bash
python -c "from volcenginesdkarkruntime import Ark; print('✅ Volcengine SDK installed')"
```

## Next Steps

1. **Test API**: `python test_doubao_api.py`
2. **Interactive Mode**: `python src/main.py --mode interactive`
3. **Connect WeChat**: `python src/main.py` (requires wxauto)

---

**Note**: The code now uses Volcengine's official SDK which is more stable and reliable for Doubao API.
