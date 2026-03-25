import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.coerce.date(),
    topic: z.string().optional(),
    seo_keywords: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string(),
    category: z.enum(['tracking', 'integrations', 'attribution', 'services']),
    date: z.string(),
    hub_page: z.string().optional(),
    page_type: z.enum(['spoke', 'hub', 'service_vertical', 'service_technical']).optional().default('spoke'),
  }),
});

export const collections = { blog, pages };
