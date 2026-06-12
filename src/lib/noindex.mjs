// Single source of truth for pages that should not be indexed.
// Used by astro.config.mjs (sitemap filter) and BaseLayout.astro (robots meta),
// so a path listed here is both noindexed and excluded from the sitemap.
export const NOINDEX_PATTERNS = [
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

export function isNoindexedPath(pathname) {
  return NOINDEX_PATTERNS.some((p) => pathname.includes(p));
}
