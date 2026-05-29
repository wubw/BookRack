# BookRack

A collection of book-related tools.

## Modules

- **analyze_ebook/** — Analyze a PDF (or a directory of PDFs) to detect text vs.
  scanned content. See [analyze_ebook/README.md](analyze_ebook/README.md).
- **crawler/** — Douban book/movie crawler and loader scripts.
- **croppdf/** — Notebook for cropping PDFs.
- **localbook/** — Local book search with Chinese title normalization.
- **reader/** — PDF → Markdown extraction and chunking utilities.
- **web/** — Web frontend (`nodemon web/server.js`).

## Running the web server

```bash
nodemon web/server.js
```
