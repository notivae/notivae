# @icon:rocket Introduction to Notivae

## Why Notivae?

Notivae was created to solve the limitations of existing knowledge and note-taking platforms. Tools like [Notion](https://www.notion.com/), [Outline](https://www.getoutline.com/), [Obsidian](https://obsidian.md/), [Logseq](https://logseq.com/), and [Joplin](https://joplinapp.org/) each offer parts of the solution—but not the whole. Some are closed-source, cloud-dependent, or hard to self-host. Others lack real-time collaboration, structured access control, or robust offline support.

Notivae brings together the best of these systems while staying **fully self-hosted**, **markdown-native**, and **privacy-first**.

### @icon:table Feature Comparison
| Feature                                                  |          Notivae          |               Notion               |              Outline               |              Obsidian              |               Logseq               |               Joplin               |
|----------------------------------------------------------|:-------------------------:|:----------------------------------:|:----------------------------------:|:----------------------------------:|:----------------------------------:|:----------------------------------:|
| For Teams and Solo use                                   | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |        @icon:x{.error .lg}         | @icon:triangle-alert{.warning .lg} |        @icon:x{.error .lg}         |
| Fully Self-Hosted                                        | @icon:check{.success .lg} |        @icon:x{.error .lg}         | @icon:triangle-alert{.warning .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |
| Real-Time-Sync                                           | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |        @icon:x{.error .lg}         | @icon:triangle-alert{.warning .lg} |        @icon:x{.error .lg}         |
| Real-time Collaboration                                  | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |        @icon:x{.error .lg}         | @icon:triangle-alert{.warning .lg} | @icon:triangle-alert{.warning .lg} |
| Remote Access <br> (Internet-Ready)                      | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      | @icon:triangle-alert{.warning .lg} | @icon:triangle-alert{.warning .lg} | @icon:triangle-alert{.warning .lg} |
| Web-First UI <br> (no install needed)                    | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |        @icon:x{.error .lg}         |        @icon:x{.error .lg}         | @icon:triangle-alert{.warning .lg} |
| Offline-First Support                                    | @icon:check{.success .lg} | @icon:triangle-alert{.warning .lg} |        @icon:x{.error .lg}         |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |
| Hierarchical Documents                                   | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |
| Markdown-Native Editing                                  | @icon:check{.success .lg} | @icon:triangle-alert{.warning .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |
| Other Text-Based Documents <br> (code, note dumping, ..) | @icon:check{.success .lg} |     @icon:check{.success .lg}      | @icon:triangle-alert{.warning .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |
| Export to Markdown/PDF                                   | @icon:check{.success .lg} |     @icon:check{.success .lg}      | @icon:triangle-alert{.warning .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |
| Snapshot-Based Versioning                                | @icon:check{.success .lg} |        @icon:x{.error .lg}         |     @icon:check{.success .lg}      | @icon:triangle-alert{.warning .lg} | @icon:triangle-alert{.warning .lg} |     @icon:check{.success .lg}      |
| Inline Comments & Discussions                            | @icon:check{.success .lg} |     @icon:check{.success .lg}      | @icon:triangle-alert{.warning .lg} |        @icon:x{.error .lg}         |        @icon:x{.error .lg}         |     @icon:check{.success .lg}      |
| Per-User Access Control                                  | @icon:check{.success .lg} |     @icon:check{.success .lg}      |     @icon:check{.success .lg}      |        @icon:x{.error .lg}         | @icon:triangle-alert{.warning .lg} |     @icon:check{.success .lg}      |

> @icon:triangle-alert{.warning .lg} = Partially supported or requires plugins/workarounds \
> @icon:x{.error .lg} = Not supported

## Got Feedback?

Notivae is early-stage — rough, changing, and evolving. We'd love your input! Head to the [GitHub repo](https://github.com/notivae/notivae) to report issues, suggest improvements, or star the project.

---

**Thanks for trying out Notivae.**
Your knowledge. Your structure. Your control.

## @icon:bot LLMs.txt Support

To improve compatibility with AI tools, Notivae provides a machine-readable [`llms.txt`](/llms.txt) file.

This file helps large language models (LLMs) — such as those used in AI-powered search, summarization, or assistant systems — understand the structure and content of our documentation. It includes clean, structured Markdown for each public page, along with its canonical URL.

Developers building tools, bots, or integrations can use this to:
- Feed context into chat-based assistants
- Build semantic search or RAG pipelines
- Preprocess documentation for embedding/indexing

@icon:file-text [View llms.txt](/llms.txt)
