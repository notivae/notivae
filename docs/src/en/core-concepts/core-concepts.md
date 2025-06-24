# 🧩 Core Concepts

Notivae is more than just a markdown editor — it’s a structured knowledge system designed to support real-time collaboration, offline editing, and granular access control. This page explains the key building blocks of the system so you can better understand how everything fits together.

## Workspaces

A **Workspace** is the top-level container for organizing your notes. Each user has exactly one personal workspace, created automatically when they sign up.

Workspaces contain:

- All of your collections and documents
- Snapshot and comment metadata
- Your personal structure and content — isolated from other users

At this stage, workspaces are **private and personal**. Shared workspaces and collaboration across workspaces are planned for future versions.

## Collections

**Collections** are folders within a workspace. They help you group related documents (like a project, course, or topic).

You can:

- Create multiple collections in a workspace
- Nest documents inside collections
- Use collections to manage shared access

## Documents

**Documents** are where your actual content lives. They are markdown-based and support:

- Real-time collaborative editing
- Offline-first changes (synced automatically)
- Rich markdown syntax (code blocks, tables, images)
- Inline comments and snapshot versioning

Documents are always part of a collection and can optionally be **nested** under other documents to form deep hierarchies.

## Hierarchical Structure

Notivae supports nested documents — much like files inside folders. This allows you to mirror complex knowledge models:

```text
📁 Programming Notes
 ┣ 📄 Languages
 ┃ ┣ 📄 Rust
 ┃ ┗ 📄 Python
 ┣ 📄 Tools
 ┃ ┗ 📄 Docker
 ┗ 📄 Personal Roadmap
```

Each document can act like both a page and a container. Nesting is currently limited to a reasonable depth to maintain performance and usability.

## Comments & Discussions

You can leave inline comments on specific parts of a document to start discussions or request feedback. Comments are threaded, can be resolved, and are tied to document versions.

## Snapshots

A **Snapshot** is like a commit: it captures the current state of a document at a point in time. You can:

* Create a named snapshot (e.g. “Final draft”)
* Restore a snapshot if needed
* Compare changes between versions (planned)

Snapshots are local to each document and are automatically timestamped.

## Access Control

Notivae uses a flexible **Attribute-Based Access Control (ABAC)** system. Instead of fixed roles (like “admin” or “editor”), permissions are evaluated based on:

* User attributes (e.g. user ID, workspace role)
* Resource attributes (e.g. document owner, collection ID)
* Context (e.g. shared via public link, authenticated session)

More on this in the [Access Control](/access-control) section.

## Sync & Offline-First

All edits are made locally first and then synced in the background when connectivity is available. This makes Notivae usable even when you're offline or have an unstable connection.

Conflict resolution is handled automatically using CRDTs (conflict-free replicated data types), which ensure consistent merging without losing user edits.

---

Understanding these core ideas will help you make the most of Notivae — whether you're organizing your own notes or collaborating with others across a shared knowledge base.
