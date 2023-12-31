# mirrorss
**mirro*rss*** is an open-source web application allowing you to
combine multiple RSS/Atom feeds

Built with:
- Python
- Flask
- feedparser
- DiskCache

## Installation

### Download from PyPI
```bash
pip install mirrorss
```
or
```bash
poetry add mirrorss
```

### Download source
```bash
git clone https://github.com/maximiliancw/mirrorss.git
cd mirrorss
pip install .
# or poetry install
```

## Deployment

### Deploy via CLI
```bash
mirrorss run
```

> Note: Use `mirrorss run --debug` to start the app in debug mode

### Deploy via WSGI
Please read Flask's documentation regarding deployment.

## License
MIT License

Copyright (c) 2023 maximiliancw <wunderkind.serie-0f@icloud.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.