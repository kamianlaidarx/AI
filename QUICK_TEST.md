# Quick Start - Test AI Without WeChat

## Problem

The main program requires `wxauto` which you haven't installed yet. To test the AI functionality without WeChat, use the simple test script.

## Solution: Use Simple Test Script

```bash
python simple_test.py
```

This script:
- ✅ Doesn't require wxauto
- ✅ Tests AI conversation directly
- ✅ Uses your configured Doubao API
- ✅ Loads personality from config

## Full Installation (If You Want WeChat)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install wxauto

```bash
pip install wxauto -i https://pypi.org/simple
```

### Step 3: Run Full Program

```bash
# Interactive mode
python src/main.py --mode interactive

# WeChat mode
python src/main.py
```

## Quick Commands

### Test AI Only (No WeChat)
```bash
python simple_test.py
```

### Test with Full Program (Requires wxauto)
```bash
pip install wxauto -i https://pypi.org/simple
python src/main.py --mode interactive
```

---

**Recommendation**: Start with `simple_test.py` to test AI functionality first!
