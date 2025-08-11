// .vitepress/lucideIconPlugin.ts
import type MarkdownIt from 'markdown-it'
import * as icons from "lucide-static";


export function lucideIconPlugin(md: MarkdownIt) {
  const iconPattern = /@lucide:([a-z0-9-]+)/gi

  md.core.ruler.push('lucide_icon_replace', state => {
    const tokens = state.tokens

    for (const token of tokens) {
      if (token.type !== 'inline') continue
      if (!token.children) continue

      const newChildren = []

      for (const child of token.children) {
        if (child.type !== 'text') {
          // Keep non-text tokens untouched
          newChildren.push(child)
          continue
        }

        const matches = [...child.content.matchAll(iconPattern)]
        if (!matches.length) {
          // No icon matches, keep as-is
          newChildren.push(child)
          continue
        }

        let lastIndex = 0
        for (const match of matches) {
          const [fullMatch, iconNameRaw] = match
          const iconName = iconNameRaw
            .split('-')
            .map(part => part.charAt(0).toUpperCase() + part.slice(1))
            .join('')

          let svgHTML: string = icons[iconName]
          if (!svgHTML) {
            console.warn(`unknown lucide-icon: '${fullMatch}'`)
            continue  // Skip unknown icons
          }

          svgHTML = svgHTML.replace(/<svg\b([^>]*)>/i, (_, attrStr) => {
            const attrs = attrStr.replace(/\s+(?:width|height)="[^"]*"/gi, '')
            return `<svg${attrs} width="1em" height="1em" style="vertical-align: middle">`;
          });

          // Add text before the icon match
          if (match.index! > lastIndex) {
            newChildren.push({
              type: 'text',
              content: child.content.slice(lastIndex, match.index),
              level: child.level,
            })
          }

          // Add icon as HTML
          newChildren.push({
            type: 'html_inline',
            content: svgHTML,
            level: child.level,
          })

          lastIndex = match.index! + fullMatch.length
        }

        // Add any trailing text after the last match
        if (lastIndex < child.content.length) {
          newChildren.push({
            type: 'text',
            content: child.content.slice(lastIndex),
            level: child.level,
          })
        }
      }

      token.children = newChildren
    }
  })
}
