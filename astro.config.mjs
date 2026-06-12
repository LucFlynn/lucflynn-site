import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// Funnel, client-deliverable, and thank-you pages are noindexed and kept out of the sitemap
const NOINDEX_PATTERNS = [
  '/campaign-templates/',
  '/industry/',
  '/lp/',
  '/leadflow-rescue',
  '/templates/leadflow',
  '/templates/lead-score',
  '/templates/services',
  '/templates/training',
  '/templates/healthcheck',
  '/thank-you',
];

export default defineConfig({
  site: 'https://lucflynn.com',
  integrations: [
    tailwind(),
    sitemap({
      filter: (page) => !NOINDEX_PATTERNS.some((p) => page.includes(p)),
    }),
  ],
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
