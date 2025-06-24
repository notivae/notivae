# 🏗️ Architecture Overview

Notivae is designed as a modular, scalable, and self-hosted collaborative markdown editor. Understanding its architecture helps you grasp how components interact and how to deploy, extend, or contribute to the project.

## High-Level Components

- **Frontend (Vue + Vite)**  
  A modern single-page application providing the user interface for editing, navigation, commenting, and collaboration.

- **Backend API (Python FastAPI)**  
  Serves REST and WebSocket endpoints to handle authentication, document management, versioning, access control, and CRDT-based synchronization.

- **Database (PostgreSQL)**  
  Stores users, workspaces, collections, documents, snapshots, comments, permissions, etc.

## Component Interaction

```
+----------+            +--------------+          +----------------+
| Frontend | <--REST--> | Backend      | <--DB--> | Database       |
| (Vue)    | <---WS---> | (FastAPI)    |          | (PostgreSQL)   |
+----------+            +--------------+          +----------------+
```

## Deployment Model

- All components run inside Docker containers orchestrated via `docker-compose`.
- Ports are exposed for the frontend and backend.
- Persistent storage is configured for database files and user data.

## Offline-First and Sync

- The frontend keeps a local replica of documents.
- Changes are applied locally and synced in the background via CRDTs.
- This approach guarantees no lost edits, even when offline or on unstable connections.

## Security and Access Control

- Authentication is handled by the backend with support for email/password and OAuth/OIDC.
- Access to documents and collections is controlled using ABAC policies evaluated on the backend.
- All communications are secured via HTTPS in production (reverse proxy recommended).

---

This modular design enables Notivae to be extended with features like API integrations, and enhanced collaboration tools without breaking core principles of privacy, ownership, and offline resilience.
