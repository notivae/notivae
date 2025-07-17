// .vitepress/lucideIconPlugin.ts
import type MarkdownIt from 'markdown-it'
import * as icons from "lucide-static";


export function lucideIconPlugin(md: MarkdownIt) {
  const iconPattern = /@lucide:([a-z0-9-]+)/gi

  md.core.ruler.push('lucide_icon_replace', state => {
    const tokens = state.tokens

    for (const token of tokens) {
      if (token.type !== 'inline' || !token.content.match(iconPattern)) continue

      const children = token.children
      if (!children) continue

      for (let i = 0; i < children.length; i++) {
        const child = children[i]
        if (child.type !== 'text') continue

        const matches = [...child.content.matchAll(iconPattern)]
        if (!matches.length) continue

        const newTokens = []
        let lastIndex = 0

        for (const match of matches) {
          const [fullMatch, iconNameRaw] = match
          const iconName = iconNameRaw
            .split('-')
            .map(part => part.charAt(0).toUpperCase() + part.slice(1))
            .join('')

          const svgHTML = icons[iconName]

          if (!svgHTML) {
            console.warn(`unknown lucide-icon: '${match}'`)
            continue  // Skip unknown icons
          }

          // Add text before match
          if (match.index! > lastIndex) {
            newTokens.push({
              type: 'text',
              content: child.content.slice(lastIndex, match.index),
              level: child.level,
              children: [],
            })
          }

          newTokens.push({
            type: 'html_inline',
            content: svgHTML,
            level: child.level,
          })

          lastIndex = match.index! + fullMatch.length
        }

        // Remaining text after last match
        if (lastIndex < child.content.length) {
          newTokens.push({
            type: 'text',
            content: child.content.slice(lastIndex),
            level: child.level,
            children: [],
          })
        }

        token.children = newTokens as any
      }
    }
  })
}
