# Testing Guide for DevKit

## Running Tests

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Specific Test Module
```bash
python3 -m pytest tests/test_display.py -v
python3 -m pytest tests/test_storage.py -v
python3 -m pytest tests/test_autocomplete.py -v
python3 -m pytest tests/test_integration.py -v
```

### Run with Coverage
```bash
python3 -m pytest tests/ --cov=devkit --cov-report=html
```

## Test Structure

### Unit Tests
- `test_display.py` - Tests for display utilities (intro, formatting, etc.)
- `test_storage.py` - Tests for storage operations (snippets, config, history)
- `test_autocomplete.py` - Tests for autocomplete functionality

### Integration Tests
- `test_integration.py` - Tests for CLI commands
- `test_autocomplete_integration.py` - Integration tests for autocomplete

## Test Coverage

Current test coverage includes:
- ✅ Display utilities (intro, formatting, numbered lists)
- ✅ Storage operations (save/load snippets, config, history)
- ✅ Autocomplete functionality
- ✅ CLI command execution
- ✅ Help formatting
- ✅ Status command with BinaryPath effect

## Manual Testing Checklist

### Intro Display
- [ ] Run `devkit --help` - intro should show on first use
- [ ] Run `devkit status` - intro should NOT show again
- [ ] Clear config: `rm ~/.devkit/config.json` - intro should show again

### Help Output
- [ ] Run `devkit --help` - commands table should be clearly visible
- [ ] Commands should be in a bordered table with proper spacing

### AI Output Formatting
- [ ] Run `devkit ask "find large files"` - check bullet points are formatted
- [ ] Check that numbered lists (1. 2. 3.) display correctly
- [ ] Verify citations section appears

### Status Command
- [ ] Run `devkit status` - should use BinaryPath effect
- [ ] Status information should animate in binary form

### About Command
- [ ] Run `devkit about` - should show animated intro
- [ ] Should display about information in a formatted panel

### Autocomplete
- [ ] Test autocomplete in interactive mode (if implemented)
- [ ] Verify command names are in autocomplete list

## Known Issues

1. Some integration tests may fail if devkit directory doesn't exist - tests now create it
2. BinaryPath effect requires terminaltexteffects package
3. Autocomplete requires prompt-toolkit package

