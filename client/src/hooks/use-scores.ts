import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, buildUrl, type InsertHighScore } from "@shared/routes";
import { z } from "zod";

export function useScores(levelId: number) {
  return useQuery({
    queryKey: [api.scores.list.path, levelId],
    queryFn: async () => {
      const url = buildUrl(api.scores.list.path, { levelId });
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to fetch scores");
      const data = await res.json();
      return api.scores.list.responses[200].parse(data);
    },
    enabled: !!levelId,
  });
}

export function useSubmitScore() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (score: InsertHighScore) => {
      const res = await fetch(api.scores.submit.path, {
        method: api.scores.submit.method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(score),
      });
      
      if (!res.ok) {
        if (res.status === 400) {
          throw new Error("Invalid score data");
        }
        throw new Error("Failed to submit score");
      }
      
      return api.scores.submit.responses[201].parse(await res.json());
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: [api.scores.list.path, data.levelId]
      });
    }
  });
}
