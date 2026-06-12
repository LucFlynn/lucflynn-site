import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

import { isNoindexedPath } from './src/lib/noindex.mjs';

export default defineConfig({
  site: 'https://lucflynn.com',
  integrations: [
    tailwind(),
    sitemap({
      filter: (page) => !isNoindexedPath(page),
    }),
  ],
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
