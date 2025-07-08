import { defineConfig } from 'vitepress';
import markdownItTaskCheckbox from "markdown-it-task-checkbox";
import { shared } from "./shared";
import { en } from "./en"

// https://vitepress.dev/reference/site-config
export default defineConfig({
  ...shared,
  locales: {
    root: { label: 'English', ...en },
  },
  markdown: {
    config:  (md) => {
      md.use(markdownItTaskCheckbox);
    },
  },
});
