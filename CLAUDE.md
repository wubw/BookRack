# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BookRack is a personal book and movie management system that crawls metadata from Douban (Chinese book/movie database), stores it in MongoDB, and provides a web interface for browsing with local file matching capabilities.

## Build & Run Commands

### Web Server (Node.js/Express)
```bash
cd web
npm install                  # Install dependencies
node server.js               # Start server on port 3001
```

### Python Crawlers
```bash
pip install -r crawler/requirements

# Crawl and load book data
python crawler/douban_crawler.py
python crawler/douban_loader.py
python crawler/douban_merger.py

# Crawl and load movie data
python crawler/movie_crawler.py
python crawler/movie_loader.py
python crawler/movie_merger.py
```

### Local Book Matching
```bash
pip install -r crawler/requirements
python localbook/main.py                    # Match local files to Douban books
python localbook/test_localbook_search.py   # Run tests
```

### PDF Reader
```bash
pip install -r reader/requirements.txt
python reader/pdf.py                    # Convert PDF to Markdown
python reader/chunk_into_unitfiles.py   # Split into units
```

## Architecture

```
Douban Websites → Python Crawlers → MongoDB → Express API → jQuery Frontend
                                       ↑
Local Files → Fuzzy Matcher (localbook/) ─┘
```

### Key Components

- **web/server.js** - Express REST API (port 3001) serving book/movie data
- **crawler/** - Python scrapers using BeautifulSoup to fetch Douban metadata
- **localbook/** - Fuzzy matching engine (SequenceMatcher, 0.6 threshold) to associate local files with Douban entries
- **reader/** - PDF to Markdown conversion using pymupdf

### API Endpoints
- `GET /books?reading_status=<status>` - Filter books by status (reading|have_read|will_read)
- `GET /book?id=<mongo_id>` - Get single book details
- `GET /localbooks` - Get all local file matches
- `GET /localbook?douban_url=<url>` - Get local file match for specific book

### Database
- **MongoDB** on localhost:27017
- Database: `books`
- Collections: `douban` (book/movie metadata), `match` (local file associations)

## Tech Stack

- **Backend**: Node.js, Express 4.17.1, MongoDB 3.5.7 driver
- **Frontend**: HTML, jQuery 1.7.1, vanilla JavaScript
- **Python**: BeautifulSoup4, lxml, pymongo, pymupdf, langconv (Chinese character conversion)
