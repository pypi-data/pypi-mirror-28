# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.4.2] - 2018-01-16

### Fixed
- autosaved icon not updating when notebook saved (#30)

## [0.4.1] - 2018-01-03

### Fixed
- Write notebooks from S3 with UTF-8 encoding (#29).

## [0.4.0] - 2017-12-20

### Changed
- Opening terminal triggers a save and disables alert

### Added
- Defaulting nano for the git editor

## [0.3.1] - 2017-12-13

### Fixed
- Broken package for v0.3.0 was uploaded to pypi.

## [0.3.0] - 2017-12-12

### Added
- Improvements to terminal navigation
- Default terminal to bash
- Add civicon font
- Git integration with notebooks

## [0.2.4] - 2017-11-28

### Fixed
- Relax requirements to require >= minor versions, instead of == minor versions (#16).

## [0.2.3] - 2017-11-22

### Added
- Added button to allow access to terminal (#15)

## [0.2.2] - 2017-09-20

### Added
- Added Civis themed colors and fonts to the notebook CSS (#11).

### Changed
- Moved to equivalent minor versions on packages civis, requests, notebook, six and civis-jupyter-extensions (#12).
- civis-jupyter-extensions 0.1.1 -> 0.1.2 (#12).

## [0.2.1] - 2017-09-18

### Added
- Scripts to make local integration testing with the Civis Platform easier (#9).

### Fixed
- Fixed package installs for already imported packages (#8).
- Fixed Docker tests to make sure they fail properly (#8).

## [0.2.0] - 2017-09-13

### Added
- More documentation and an example Docker image (#2, #3, #4).
- Cleaner Docker files for testing (#4).
- Cleaner logging outputs (#4).

### Removed
- Removed the UI buttons to change kernels (#6).

### Fixed
- Relaxed requirement markers for Python 2 packaging (#5).

## [0.1.0] - 2017-09-08

### Added
- Initial commit.
