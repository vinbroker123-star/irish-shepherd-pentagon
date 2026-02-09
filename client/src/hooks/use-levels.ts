import { useQuery } from "@tanstack/react-query";
import { api, buildUrl } from "@shared/routes";
import { z } from "zod";

// Helper to ensure we never crash on schema mismatches
function parseResponse<T>(schema: z.ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    console.error("Schema validation failed:", result.error);
    throw new Error("Invalid API response");
  }
  return result.data;
}

export function useLevels() {
  return useQuery({
    queryKey: [api.levels.list.path],
    queryFn: async () => {
      const res = await fetch(api.levels.list.path);
      if (!res.ok) throw new Error("Failed to fetch levels");
      const data = await res.json();
      return parseResponse(api.levels.list.responses[200], data);
    },
  });
}

export function useLevel(id: number) {
  return useQuery({
    queryKey: [api.levels.get.path, id],
    queryFn: async () => {
      const url = buildUrl(api.levels.get.path, { id });
      const res = await fetch(url);
      if (res.status === 404) return null;
      if (!res.ok) throw new Error("Failed to fetch level");
      const data = await res.json();
      return parseResponse(api.levels.get.responses[200], data);
    },
    enabled: !!id,
  });
}
