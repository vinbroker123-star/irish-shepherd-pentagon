import { useLevels } from "@/hooks/use-levels";
import { RetroWindow } from "@/components/RetroWindow";
import { RetroButton } from "@/components/RetroButton";
import { Link } from "wouter";
import { Loader2, Play } from "lucide-react";

export default function Home() {
  const { data: levels, isLoading } = useLevels();

  return (
    <div className="min-h-screen bg-neutral-100 p-8 flex items-center justify-center">
      <RetroWindow title="Mac Factory 1.0" className="max-w-3xl w-full h-[600px]">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-full">
          
          {/* Left: Intro */}
          <div className="flex flex-col gap-6 p-6 border-r-2 border-dashed border-gray-300">
            <div className="space-y-2">
              <h1 className="text-4xl font-display uppercase tracking-widest">Factory<br/>Simulation</h1>
              <p className="font-mono text-sm text-gray-500">v1.0.4 (System 7 Compatible)</p>
            </div>
            
            <div className="prose font-mono text-sm leading-relaxed">
              <p>Welcome, Engineer.</p>
              <p>Your task is to optimize production lines. Process raw materials into finished goods using the latest in monochrome automation technology.</p>
              <ul className="list-disc pl-4 space-y-1 mt-4 text-xs uppercase">
                <li>Deploy Conveyor Belts</li>
                <li>Operate Heavy Machinery</li>
                <li>Maximize Efficiency</li>
              </ul>
            </div>

            <div className="mt-auto">
               <div className="w-full h-32 bg-checker border-2 border-black flex items-center justify-center">
                  <span className="bg-white px-2 py-1 font-display text-xl border border-black shadow-retro">
                    NO DISK INSERTED
                  </span>
               </div>
            </div>
          </div>

          {/* Right: Level Select */}
          <div className="p-6 flex flex-col gap-4">
            <h2 className="text-xl font-bold border-b-2 border-black pb-2 mb-2">Select Mission</h2>
            
            {isLoading ? (
              <div className="flex items-center justify-center h-40">
                <Loader2 className="w-8 h-8 animate-spin" />
              </div>
            ) : (
              <div className="space-y-3 overflow-y-auto pr-2 max-h-[400px]">
                {levels?.map((level) => (
                  <div key={level.id} className="group relative">
                    <div className="absolute inset-0 bg-black translate-x-1 translate-y-1 opacity-0 group-hover:opacity-100 transition-opacity rounded-none" />
                    <div className="relative bg-white border-2 border-black p-4 flex justify-between items-center hover:-translate-y-0.5 hover:-translate-x-0.5 transition-transform duration-75">
                      <div>
                        <h3 className="font-bold">{level.order}. {level.name}</h3>
                        <p className="text-xs text-gray-500 mt-1 line-clamp-1">{level.description}</p>
                      </div>
                      <Link href={`/game/${level.id}`} className="no-underline">
                        <RetroButton size="sm">
                          <Play className="w-4 h-4" />
                        </RetroButton>
                      </Link>
                    </div>
                  </div>
                ))}
                
                {levels?.length === 0 && (
                  <div className="text-center py-8 text-gray-500 italic border-2 border-dashed border-gray-300">
                    No levels data found on disk.
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </RetroWindow>
    </div>
  );
}
