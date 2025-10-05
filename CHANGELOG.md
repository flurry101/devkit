# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-04

### Published

https://test.pypi.org/project/devkit-cli/0.1.0/
https://pypi.org/project/devkit-cli/0.1.0/

## [0.1.0] - 2025-01-04

### Added
- **Snippet Tags System**: Add tags to snippets for better organization
- **Snippet Search**: Search snippets by name, command content, or tags
- **Export/Import Functionality**: Export snippets to JSON or text format, import with conflict resolution
- **Enhanced Snippet Display**: Show tags, creation date, and metadata in snippet listings
- **Improved Error Handling**: Better AI error messages with specific guidance for different error types
- **Colored Terminal Output**: Beautiful colored output with colorama integration
- **Comprehensive Documentation**: Complete usage guide with examples and troubleshooting

### Changed
- **Storage Format**: Upgraded snippet storage to support metadata (backward compatible)
- **Snippet Commands**: Enhanced all snippet commands to work with new format
- **Project Structure**: Cleaned up directory structure, improved .gitignore
- **Version**: Bumped to 0.1.0 for feature release

### Fixed
- **Code Redundancy**: Removed duplicate snippet commands in main.py
- **Test Issues**: Fixed all failing tests, updated test expectations
- **Virtual Environment**: Cleaned up multiple venv directories and cache folders
- **Dependencies**: Updated requirements.txt with all needed packages

### Technical Improvements
- **Modular Design**: Better separation of concerns in code structure
- **Backward Compatibility**: Legacy snippet format automatically converted
- **Error Recovery**: Graceful handling of malformed data
- **Performance**: Optimized storage operations
- Updated all AI functions to use Gemini API
- Improved error handling for Gemini-specific errors
- Updated documentation and examples

## [0.1.0] - 2025-01-04

### Added
- **Basic Snippet Management**: Save, list, get, run, and delete snippets
- **AI Integration**: Ask for command suggestions and explain commands
- **Commit Helper**: Interactive and AI-powered commit message generation
- **Time-Travel Debugging**: View and analyze command history
- **Emergency Rollback**: Detect dangerous commands and suggest rollbacks
- **Configuration Management**: API key configuration and status reporting
- **Demo Examples**: Pre-loaded example snippets and rollback scenarios

### Features
- Snippet CRUD operations
- AI-powered command suggestions (Claude API)
- Command explanation and analysis
- Git commit message generation
- Command history tracking
- Dangerous command detection
- Emergency rollback assistance
- Comprehensive status reporting

### Technical
- Click-based CLI interface
- JSON-based data persistence
- Modular architecture
- Unit test coverage
- Cross-platform compatibility