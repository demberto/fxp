<!-- BADGES -->
<table>
  <tr>
    <th>ci</th>
    <td>
      <a>
        <img alt="Tests" src="https://img.shields.io/github/workflow/status/demberto/fxp/tests?label=tests"/>
      </a>
      <a>
        <img alt="Build" src="https://img.shields.io/github/workflow/status/demberto/fxp/publish"/>
      </a>
      <a href="https://fxp.rtfd.io/en/latest">
        <img alt="Docs" src="https://readthedocs.org/projects/fxp/badge/?version=latest"/>
      </a>
    </td>
  </tr>
  <tr>
    <th>pypi</th>
    <td>
      <a href="https://github.com/demberto/fxp/releases">
        <img alt="Version" src="https://img.shields.io/pypi/v/fxp"/>
      </a>
      <a href="https://github.com/demberto/fxp/blob/master/LICENSE">
        <img alt="License" src="https://img.shields.io/pypi/l/fxp"/>
      </a>
      <a>
        <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/fxp"/>
      </a>
    </td>
  </tr>
  <tr>
    <th>qa</th>
    <td>
      <a href="https://github.com/PyCQA/bandit">
        <img alt="security: bandit" src="https://img.shields.io/badge/security-bandit-yellow.svg"/>
      </a>
      <a href="https://github.com/python/mypy">
        <img alt="mypy: checked" src="https://img.shields.io/badge/mypy-checked-blue.svg"/>
      </a>
      <a href="https://github.com/psf/black">
        <img alt="code style: black" src="https://img.shields.io/badge/code%20style-black-black.svg"/>
      </a>
    </td>
  </tr>
</table>

# fxp

> VST2.x plugin FXP preset parser.

## ⏬ Installation

- Via `pip` (**RECOMMENDED**, easiest, fastest):

  fxp requires Python 3.6+

  ```
  pip install fxp
  ```

*OR*

- Via Github Releases

  1.  [Download](https://github.com/demberto/fxp/releases) the latest release.

  2.  Install it via `pip`:

      ```
      pip install fxp-0.1.0-py3-none-any.whl
      ```

*OR*

- Via cloning the repo:

  1.  Clone this repo

      ```
      git clone https://github.com/demberto/fxp
      ```

  2.  Navigate to the directory

      ```
      cd fxp
      ```

  3.  Install it via `pip` in editable mode:

      ```
      pip install -e .
      ```

## ✨ Getting Started

```Python
>>> import fxp
>>> preset = fxp.FXP("path/to/preset.fxp")
>>> preset.plugin_id
"XfsX"
>>> preset.name
"LD Saw Bass"
>>> preset.is_opaque()
True
```

## 🤝 Contributing

All contributions are welcome and acknowledged.
Please take a look at the [contributor's guide][contributor-guide]

## 📧 Contact

Email: demberto@protonmail.com

## 🙏 Acknowledgements

- `pluginterfaces/vstfxstore.h` from the VST2 SDK.

## © License

The code in this project is licensed under the MIT License.

<!-- LINKS -->
[contributor-guide]: https://github.com/demberto/fxp/blob/master/CONTRIBUTING.md
