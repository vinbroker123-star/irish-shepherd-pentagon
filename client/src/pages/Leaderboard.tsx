import { useScores } from "@/hooks/use-scores";
import { RetroWindow } from "@/components/RetroWindow";
import { Loader2 } from "lucide-react";

interface LeaderboardProps {
  levelId: number;
}

export function Leaderboard({ levelId }: LeaderboardProps) {
  const { data: scores, isLoading } = useScores(levelId);

  return (
    <RetroWindow title="High Scores" className="w-full h-full min-h-[300px]">
      {isLoading ? (
        <div className="flex items-center justify-center h-full">
          <Loader2 className="animate-spin" />
        </div>
      ) : (
        <div className="w-full">
          <table className="w-full text-left text-sm font-mono border-collapse">
            <thead>
              <tr className="border-b-2 border-black">
                <th className="p-2 uppercase">Rank</th>
                <th className="p-2 uppercase">Operator</th>
                <th className="p-2 text-right uppercase">Score</th>
                <th className="p-2 text-right uppercase">Time</th>
              </tr>
            </thead>
            <tbody>
              {scores?.sort((a,b) => b.score - a.score).map((score, index) => (
                <tr key={score.id} className="border-b border-gray-200 hover:bg-gray-50">
                  <td className="p-2 font-bold">#{index + 1}</td>
                  <td className="p-2">{score.playerName}</td>
                  <td className="p-2 text-right font-bold">{score.score}</td>
                  <td className="p-2 text-right">{score.timeTaken}s</td>
                </tr>
              ))}
              {scores?.length === 0 && (
                <tr>
                  <td colSpan={4} className="p-8 text-center text-gray-500 italic">No records found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </RetroWindow>
  );
}
