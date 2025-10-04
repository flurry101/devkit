# DevKit Release Guide

## Prerequisites

**PyPI Account**: https://pypi.org/account/register  
**TestPyPI Account**: https://test.pypi.org/account/register  
**API Tokens**: Generate at https://pypi.org/manage/account/token/

---

## Setup Trusted Publishing (Recommended)

### 1. Configure PyPI  
Go to https://pypi.org/manage/account/publishing/  
Add publisher:

- **PyPI Project Name**: `devkit-cli`  
- **Owner**: `flurry101`  
- **Repository**: `devkit`  
- **Workflow**: `publish.yml`  
- **Environment**: `pypi`

### 2. GitHub Environment  
Go to `Settings → Environments → New environment`  
- **Name**: `pypi`  
- Add protection rules (optional):  
  - Required reviewers  
  - Wait timer  

---

## Manual Release Process

### 1. Prepare Release

```bash
# Update version
vim setup.py           # Update version='0.2.0'
vim devkit/__init__.py # Update __version__

# Update changelog
vim CHANGELOG.md

# Commit changes
git add .
devkit commit --ai
git push
```

### 2. Build Package

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Verify
ls dist/
# Should see: devkit_cli-0.2.0-py3-none-any.whl and devkit_cli-0.2.0.tar.gz
```

### 3. Test on TestPyPI

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ devkit-cli

# Test commands
devkit --version
devkit status
```

### 4. Release to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Verify
pip install devkit-cli
```

### 5. Create GitHub Release

```bash
# Tag version
git tag v0.2.0
git push origin v0.2.0
```

On GitHub:  
- Go to **Releases → Draft new release**  
- Choose tag: `v0.2.0`  
- Title: `DevKit v0.2.0`  
- Description: Copy from `CHANGELOG.md`  
- Attach `dist/` files  
- **Publish**

---

## Automated Release (GitHub Actions)

Once trusted publishing is set up:

> Just create a GitHub release  
> The workflow will:  
> - Build package  
> - Run tests  
> - Publish to PyPI automatically  

---

## Version Numbering

We use **semantic versioning**:

- `0.1.0 → 0.2.0` (minor - new features)  
- `0.2.0 → 0.2.1` (patch - bug fixes)  
- `0.9.0 → 1.0.0` (major - breaking changes)  

---

## Checklist

- [ ] Version updated in `setup.py` and `__init__.py`  
- [ ] `CHANGELOG.md` updated  
- [ ] All tests passing  
- [ ] `README` up to date  
- [ ] Built with `python -m build`  
- [ ] Tested on TestPyPI  
- [ ] Tagged in git  
- [ ] GitHub release created  
- [ ] Published to PyPI  
- [ ] Announcement (optional)  

---

## Troubleshooting

- **"File already exists"**: Increment version number  
- **"Invalid token"**: Regenerate API token on PyPI  
- **"Trusted publishing failed"**: Check environment name matches in workflow and PyPI settings  

---

## Resources

- PyPI: https://pypi.org/project/devkit-cli/  
- Trusted Publishing: https://docs.pypi.org/trusted-publishers/  
- Packaging Guide: https://packaging.python.org/
