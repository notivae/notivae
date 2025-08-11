# @lucide:message-circle-question-mark FAQ

Frequently Asked Questions about Notivae — answered concisely.

## Is Notivae finished?

No — Notivae is **very much a work in progress**. Core architecture is in place, but many features are still incomplete or entirely missing. Expect frequent changes, breaking migrations, and rough edges. It's not yet suitable for production use or critical data.


## Can I use Notivae without an internet connection?

Yes. Notivae is designed to be **offline-first**. You can open the app, edit documents, and your changes will sync once you're reconnected.


## Does Notivae require any external services?

No. Notivae is built to run fully isolated, without relying on any third-party services. Everything — backend, frontend, and database — runs locally by default.

However, external dependencies can be added **optionally** to enhance functionality. For example:

- External OAuth/OIDC providers for authentication (GitHub, GitLab, etc.)
- Externally managed PostgreSQL for improved performance, scalability, or backup automation


## Is there support for real-time collaboration?

Yes — Notivae uses **CRDT-based sync** to support real-time editing.


## What format is content stored in?

The primary focus is on **Markdown-based documents**, but Notivae also supports other plain text formats such as code files (e.g. `.js`, `.py`, `.json`).

In the future, support for alternative structured formats like **Typst**, **AsciiDoc**, and **WikiText** is considered — along with proper editors and renderers for each format. This will allow more specialized workflows while keeping content structured and exportable.


## Can I import my existing notes from Notion / Obsidian / Logseq?

Not yet. But import/export support for common formats is on the roadmap. For now, you can manually paste or migrate content using Markdown.


## Does Notivae support custom domains or HTTPS?

Yes — simply reverse proxy it behind Nginx, Caddy, or Traefik and terminate HTTPS there. You'll configure this outside the Docker container.


## Can I restrict who signs up?

Eventually, yes. Planned features include:

- Invite-only registration
- Restrict signups to a specific domain or OAuth provider (e.g. GitHub org)


## Is my Notivae instance protected against spam or abuse?

Yes. Notivae includes built-in safeguards to help protect your instance from excessive or abusive usage. This includes measures like request limits and temporary blocks for suspicious behavior. If you're self-hosting Notivae and want to learn more, see the [Security documentation](../hosting/security.md).


## Will there be mobile apps?

Probably not. The current web app is being designed as a **Progressive Web App (PWA)** with offline support and responsive layout, which works well on mobile devices.


## How do I contribute?

Check out the [Contributing](./contributing.md) page and the [GitHub repo](https://github.com/notivae/notivae). Contributions of all kinds are welcome — code, docs, testing, ideas.


---

Missing a question?  
Open an issue or discussion on [GitHub](https://github.com/notivae/notivae/issues).
