# Notivae

> A self-hosted, real-time markdown editor for structured notes, collaborative learning, and knowledge management.

[![CodeQL](https://github.com/notivae/notivae/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/notivae/notivae/actions/workflows/github-code-scanning/codeql)
[![Deploy Docs to GitHub Pages](https://github.com/notivae/notivae/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/notivae/notivae/actions/workflows/deploy-docs.yml)

<!-- [![Docker Image Build - Backend](#)](#) -->
<!-- [![Docker Image Build - Web](#)](#) -->
<!-- [![Docker Image Build - Intelligence](#)](#) -->

![Repo Size](https://img.shields.io/github/repo-size/notivae/notivae)
![Code Size](https://img.shields.io/github/languages/code-size/notivae/notivae)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

> [!WARNING] ⚠️ Early-stage development
> expect breaking changes, incomplete features, and evolving APIs.  
> For non-technical users, please visit <https://notivae.github.io/>

---

## Why We Built It

We built **Notivae** to address persistent issues in existing knowledge management tools:  
- Limited or fragile offline support  
- Rigid data models that don’t fit complex structures  
- Vendor lock-in and dependency on proprietary services  

By combining:
- **Markdown** as the storage format for portability
- **CRDTs** for conflict-free, real-time collaboration
- **Self-hosting** with modular architecture for privacy and extensibility

...Notivae enables developers and power-users to own their data, customize their workflows, and collaborate effectively without sacrificing control.

---

## Design Philosophy

- **Self-hosted first** – all components run under your control
- **Markdown-native** – future-proof, human-readable storage
- **Offline-first** – resilient to poor connectivity
- **Structured hierarchy** – collections + nested documents
- **Fine-grained access control** – ABAC instead of rigid roles
- **Simple deployment** – single `docker compose` command for full stack

---

## Key Features

- **Markdown-native editing** with rich syntax support
- **Offline-first** architecture with automatic background sync
- **Real-time collaboration** powered by CRDTs
- **Structured collections** and nested documents
- **Granular sharing** via Access Control
- **Snapshot versioning** with restore capability
- **Threaded inline comments**
- 100% **self-hosted** with Docker-based deployment

---

## Architecture Overview

Notivae is a modular monorepo consisting of:

- **`/docs`** – Documentation site built with [VitePress](https://vitepress.dev/)  
- **`/server`** – FastAPI backend with async SQLAlchemy and PostgreSQL  
- **`/web`** – Vue 3 SPA using shadcn-vue, TailwindCSS, and Yjs for real-time sync  
- **`/intelligence`** *(planned)* – Optional AI/ML services for OCR, summarization, transcription, and more

```
📦 notivae/
┣ 📂 docs
┣ 📂 server
┣ 📂 web
┗ 📂 intelligence  # planned
```

---

## Development Setup

### Prerequisites
- Docker + Docker Compose installed
- Basic familiarity with running terminal commands

### 1. Clone the repository
```bash
git clone https://github.com/notivae/notivae.git
cd notivae
````

### 2. Create a `.env.dev` file

```dotenv
DEBUG=yes
LOGGING_LEVEL=DEBUG
LOGGING_FORMAT=console

SECURITY_SECRET_KEY=  # openssl rand -hex 32
SECURITY_DISABLE_RATE_LIMITS=yes

APP_ACCOUNT_CREATION=open

REDIS_URL=redis://redis

MAIL_SERVER=mailhog
MAIL_PORT=1025
MAIL_USE_CREDENTIALS=no
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_FROM="Notivae <noreply@example.com>"
MAIL_USE_TLS=no
MAIL_START_TLS=no
MAIL_VALIDATE_CERTS=no

AUTH_LOCAL_ENABLED=yes
```

### 3. Start the development stack

```bash
docker compose -f docker-compose.dev.yml up -d
```

### 4. Stop the development stack

```bash
docker compose -f docker-compose.dev.yml down
```

---

## High-Level Components


### `/docs`
Documentation site built with [VitePress](https://vitepress.dev/).

### `/server`
FastAPI backend with async SQLAlchemy and PostgreSQL.

### `/web`
Vue 3 SPA using shadcn-vue, TailwindCSS, and Yjs for real-time sync.

### `/intelligence` *(Planned)*

Optional AI/ML services for OCR, summarization, transcription, semantic search, and more.  

> [!WARNING]
> This module is **not yet implemented**. It will run entirely locally without external API calls.

---

## Contributing

We welcome contributions in all forms:

* **Code** – new features, bug fixes, refactors
* **Documentation** – improve guides, write tutorials
* **Testing** – try the stack, report issues
* **Design** – UX, UI, accessibility improvements
* **Ideas** – open issues or discussions to shape the roadmap

### Contribution Steps

- For **ideas**, **bug reports**, or **feature requests**, simply [open an issue](https://github.com/notivae/notivae/issues).
- For code changes:
  1. Fork the repo & create a feature branch
  2. Make your changes (follow the code style & commit conventions)
  3. Open a pull request with a clear description

Please read [CONTRIBUTING.md](docs/src/en/other/contributing.md) for details.

---

## License

This project is licensed under the **GNU General Public License v3.0** – see the [LICENSE](LICENSE) file for details.
