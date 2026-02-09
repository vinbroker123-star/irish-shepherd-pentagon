import { z } from 'zod';
import { insertHighScoreSchema, levels, highScores } from './schema';

export const errorSchemas = {
  validation: z.object({
    message: z.string(),
    field: z.string().optional(),
  }),
  notFound: z.object({
    message: z.string(),
  }),
  internal: z.object({
    message: z.string(),
  }),
};

export const api = {
  levels: {
    list: {
      method: 'GET' as const,
      path: '/api/levels' as const,
      responses: {
        200: z.array(z.custom<typeof levels.$inferSelect>()),
      },
    },
    get: {
      method: 'GET' as const,
      path: '/api/levels/:id' as const,
      responses: {
        200: z.custom<typeof levels.$inferSelect>(),
        404: errorSchemas.notFound,
      },
    },
  },
  scores: {
    list: {
      method: 'GET' as const,
      path: '/api/levels/:levelId/scores' as const,
      responses: {
        200: z.array(z.custom<typeof highScores.$inferSelect>()),
      },
    },
    submit: {
      method: 'POST' as const,
      path: '/api/scores' as const,
      input: insertHighScoreSchema,
      responses: {
        201: z.custom<typeof highScores.$inferSelect>(),
        400: errorSchemas.validation,
      },
    },
  },
};

export function buildUrl(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (url.includes(`:${key}`)) {
        url = url.replace(`:${key}`, String(value));
      }
    });
  }
  return url;
}
