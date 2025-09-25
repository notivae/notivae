# @icon:target Design Decisions

Notivae’s architecture and feature set are driven by clear design principles focused on user control, privacy, collaboration, and extensibility. This page outlines the key decisions behind the project’s foundation.

## 1. Self-Hosted First

- Users retain full control over their data by running Notivae on their own infrastructure.
- No reliance on third-party services or proprietary cloud platforms.
- Ensures privacy, security, and compliance with personal or organizational policies.

## 2. Markdown-Native

- Markdown is the universal format for writing and note-taking.
- Enables compatibility with many tools and simple import/export workflows.
- Avoids vendor lock-in by storing plain-text documents with semantic structure.

## 3. Real-Time Collaboration with CRDTs

- Uses Conflict-Free Replicated Data Types (CRDTs) to enable seamless multi-user editing.
- Guarantees zero merge conflicts and automatic offline sync.
- Yjs is chosen as the CRDT library for its performance and community support.

## 4. Offline-First Approach

- Users can read and edit documents without an internet connection.
- Local changes sync automatically once connectivity is restored.
- Provides resilience against unstable networks and improves usability on mobile devices.

## 5. Hierarchical Structure

- Documents can be nested within collections and other documents.
- Mirrors natural knowledge organization: folders, subfolders, and pages.
- Enables granular access control and easier navigation in large knowledge bases.

## 6. Attribute-Based Access Control (ABAC)

- Moves beyond rigid role-based permissions.
- Access is evaluated dynamically based on user attributes, document metadata, and context.
- Offers fine-grained control suitable for complex sharing and collaboration scenarios.

## 7. Simple Deployment

- Uses Docker and Docker Compose for straightforward setup.
- Prebuilt images simplify installation for both developers and end-users.
- Designed for easy upgrades and maintenance.

---

These decisions collectively shape Notivae into a privacy-respecting, user-centric, and robust platform for collaborative knowledge management.
