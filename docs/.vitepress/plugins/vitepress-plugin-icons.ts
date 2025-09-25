import type MarkdownIt from "markdown-it"
import { getIconData, iconToSVG } from "@iconify/utils"

// Import only the collections you want
import { icons as lucide } from "@iconify-json/lucide"
import { icons as simpleIcons } from "@iconify-json/simple-icons"

const COLLECTIONS: Record<string, any> = {
  "lucide": lucide,
  "logo": simpleIcons,
}
const DEFAULT_COLLECTION = "lucide";

// Regex for @icon:collection:name{...}
const iconPattern =
  /@icon:(?:([^:\s]+):)?([^{\s]+)(\{[^}]*})?/gi

// Parse `{.class1 .class2 attr=val attr2="spaced val"}` into attrs
function parseAttrs(input: string | undefined): Record<string, string> {
  if (!input) return {}

  const out: Record<string, string> = {}
  const regex =
    /\.(\w[\w-]*)|(\w[\w-]*)=("[^"]+"|'[^']+'|[^\s}]+)/g

  let match: RegExpExecArray | null
  while ((match = regex.exec(input))) {
    if (match[1]) {
      // class shorthand
      out.class = (out.class ? out.class + " " : "") + match[1]
    } else if (match[2]) {
      const key = match[2]
      let val = match[3]
      if (val?.startsWith('"') || val?.startsWith("'")) {
        val = val.slice(1, -1)
      }
      out[key] = val
    }
  }

  return out
}

export function iconPlugin(md: MarkdownIt) {
  md.core.ruler.before("curly_attributes", "icon_replace", (state) => {
    const tokens = state.tokens

    for (const token of tokens) {
      if (token.type !== "inline") continue
      if (!token.children) continue

      const newChildren: any[] = []

      for (const child of token.children) {
        if (child.type !== "text") {
          newChildren.push(child)
          continue
        }

        const matches = [...child.content.matchAll(iconPattern)]
        if (!matches.length) {
          newChildren.push(child)
          continue
        }

        let lastIndex = 0
        for (const match of matches) {
          const [full, maybeCollection, name, rawAttrs] = match
          const collection = maybeCollection ?? DEFAULT_COLLECTION

          const iconSet = COLLECTIONS[collection]
          if (!iconSet) {
            console.warn(`Unknown icon collection: '${collection}'`)
            continue
          }

          const data = getIconData(iconSet, name)
          if (!data) {
            console.warn(`Unknown icon: '${collection}:${name}'`)
            continue
          }

          const extraAttrs = parseAttrs(rawAttrs)
          const render = iconToSVG(data, { height: "1em" })

          // Merge attributes
          let attrs: Record<string, string> = { style: "", class: "", ...render.attributes, ...extraAttrs }
          attrs.class = "icon " + attrs.class

          const attrStr = Object.entries(attrs)
            .map(([k, v]) => `${k}="${String(v)}"`)
            .join(" ")

          const svgHTML = `<svg ${attrStr}>${render.body}</svg>`

          // text before icon
          if (match.index! > lastIndex) {
            newChildren.push({
              type: "text",
              content: child.content.slice(lastIndex, match.index),
              level: child.level,
            })
          }

          // icon
          newChildren.push({
            type: "html_inline",
            content: svgHTML,
            level: child.level,
          })

          lastIndex = match.index! + full.length
        }

        if (lastIndex < child.content.length) {
          newChildren.push({
            type: "text",
            content: child.content.slice(lastIndex),
            level: child.level,
          })
        }
      }

      token.children = newChildren
    }
  })
}
