import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

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

export const collections = { pages };
