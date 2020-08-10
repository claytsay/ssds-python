# Changelog

This changelog aims to follow [Semantic Versioning](https://semver.org/) 
guidelines to the extent allowed by [PEP 440](https://www.python.org/dev/peps/pep-0440/).

## 0.x.x

### 0.1.x

#### 0.1.3

- Fixed a critical bug regarding mismatched method names
- Added a test that computes the speed ratio between `ArrayHeapPQ` and
  `ReferencePQ`

#### 0.1.2

- Created documentation files for the project
  - Utilizes [Sphinx](https://www.sphinx-doc.org/en/master/)
  - To be deployed on GitHub pages
- Updated docstings to follow the NumPy docstring guide
  ([link](https://numpydoc.readthedocs.io/en/latest/format.html))
- Added a `requirements.txt`

#### 0.1.1

- Fixed a bug involving `ssds.abc` not being able to be imported
- Updated `README.md` with PyPI instructions

#### 0.1.0

- Initial release
- Finished implementation of `ArrayHeapPQ`
  - Implemented `ReferencePQ` for accuracy testing
  - Implemented `ArrayHeapPQ` for testing
- Updated `README.md`
- Updated `LICENSE`
- Updated `.gitignore`
