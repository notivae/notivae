import fs from "node:fs";
import path from "node:path";

const SRC_DIR = "src/en/";
const OUTPUT_FILE = ".vitepress/dist/llms.txt";
const BASE_PATH = "/";


function getSlugFromPath(filePath) {
    const slug = filePath
        .replace(SRC_DIR, '')  // strip leading docs
        .replace(/index\.md$/, '')  // remove index.md
        .replace(/\.md$/, '')  // remove .md suffix
        .replace(/\\$/, '/')  // windows path support
        .replace(/\/$/, '')  // remove trailing slash

    return `${BASE_PATH}${slug}`;
}


function readMarkdownFiles(dir) {
    let entries = fs.readdirSync(dir, { withFileTypes: true });
    let blocks = [];

    for (const entry of entries) {
        const fullpath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            const subblocks = readMarkdownFiles(fullpath);
            blocks.push(...subblocks);
        } else if (entry.name.startsWith('.')) {
            // nothing. skipping such files
        } else if (entry.name.endsWith('.md')) {
            const raw = fs.readFileSync(fullpath, 'utf-8');
            const url = getSlugFromPath(fullpath);
            const block = `---
url: ${url}
content: |
${raw.split('\n').map(line => '  ' + line).join('\n')}
`;
            blocks.push(block);
        }
    }

    return blocks;
}

const blocks = readMarkdownFiles(SRC_DIR);
fs.writeFileSync(OUTPUT_FILE, blocks.join('\n'), 'utf-8');
console.log(`Generated ${OUTPUT_FILE}`);
