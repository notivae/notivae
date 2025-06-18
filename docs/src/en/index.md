---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Notivae"
  text: "Self-hosted collaborative markdoen editor"
  tagline: "Structure your knowledge. Collaborate in real time. Stay in control"
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started
    - theme: alt
      text: GitHub Repo
      link: https://github.com/notivae/notivae

features:
  - icon: <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users-icon lucide-users"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/></svg>
    title: Real-Time Collaboration
    details: Multi-user editing with CRDTs for seamless, conflict-free collaboration.
  - icon: <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-folder-tree-icon lucide-folder-tree"><path d="M20 10a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2.5a1 1 0 0 1-.8-.4l-.9-1.2A1 1 0 0 0 15 3h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"/><path d="M20 21a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1h-2.9a1 1 0 0 1-.88-.55l-.42-.85a1 1 0 0 0-.92-.6H13a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"/><path d="M3 5a2 2 0 0 0 2 2h3"/><path d="M3 3v13a2 2 0 0 0 2 2h3"/></svg>
    title: Structured Note Collections
    details: Organize content into nested folders and sub-documents for deep knowledge systems.
  - icon: <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-wifi-off-icon lucide-wifi-off"><path d="M12 20h.01"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/><path d="M5 12.859a10 10 0 0 1 5.17-2.69"/><path d="M19 12.859a10 10 0 0 0-2.007-1.523"/><path d="M2 8.82a15 15 0 0 1 4.177-2.643"/><path d="M22 8.82a15 15 0 0 0-11.288-3.764"/><path d="m2 2 20 20"/></svg>
    title: Offline-First, Sync-Later
    details: Work offline anytime — Notivae syncs automatically once you're back online.
  - icon: <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-history-icon lucide-history"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/></svg>
    title: Snapshot Versioning
    details: Create versioned “commits” of any document, enabling safe rollbacks and change tracking.
  - icon: <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-message-circle-more-icon lucide-message-circle-more"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8 12h.01"/><path d="M12 12h.01"/><path d="M16 12h.01"/></svg>
    title: Inline Comments & Discussions
    details: Add context-aware feedback and threaded conversations right inside your documents.
  - icon: <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-book-lock-icon lucide-book-lock"><path d="M18 6V4a2 2 0 1 0-4 0v2"/><path d="M20 15v6a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H10"/><rect x="12" y="6" width="8" height="5" rx="1"/></svg>
    title: Privacy-First & Self-Hosted
    details: Own your data completely. No third-party dependencies like Supabase or S3.
---

> [!IMPORTANT]
> Notivae is in early development. Expect breaking changes and limited support.

## 📖 What is Notivae?

**Notivae** is a self-hosted, real-time collaborative markdown editor built for students, researchers, and professionals who value structure, clarity, and ownership of their knowledge.

Inspired by Latin roots meaning “related to notes”, Notivae empowers users to write, collaborate, and organize their thoughts in a flexible but structured environment — all without giving up control to third-party platforms.

Whether you're managing study notes, drafting papers, planning projects, or building a long-term knowledge base, Notivae helps you stay productive and in control.

### 🧠 Key Capabilities

- **Markdown-first experience** — Focused, clean writing interface powered by a modern Markdown engine.
- **Real-time collaboration** — CRDT-based multi-user editing with zero merge conflicts.
- **Hierarchical structure** — Nest documents within collections and subfolders to mirror your mental model.
- **Snapshots for versioning** — Create named snapshots of documents to mark stable revisions, much like commits in Git.
- **Inline comments** — Add and resolve context-specific feedback for discussion and peer review.
- **Granular access control** — Share documents via public links or restrict access with per-user permissions.
- **Offline support** — Fully functional offline editing with automatic background sync when reconnected.
- **Authentication options** — Sign in via email/password or OAuth providers like GitHub, GitLab, Discord, and any OIDC-compatible system.
- **Fully self-hosted** — No reliance on external services like Supabase, S3, or Firebase. Your data stays yours.
- **Early-stage roadmap** — Planned features include a user dashboard, export to PDF/Markdown, comment threads, mobile improvements, and API support.

> ✨ Built with ❤️ by and for students who believe that knowledge should be open, structured, and self-owned.

Explore the docs to get started, contribute, or deploy your own instance of Notivae.
