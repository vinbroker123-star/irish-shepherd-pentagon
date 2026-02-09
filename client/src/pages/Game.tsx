import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useLocation } from "wouter";
import { useLevel } from "@/hooks/use-levels";
import { useScores, useSubmitScore } from "@/hooks/use-scores";
import { RetroWindow } from "@/components/RetroWindow";
import { RetroButton } from "@/components/RetroButton";
import { GameBoard } from "@/components/GameBoard";
import { MachineToolbar } from "@/components/MachineToolbar";
import { Machine, GameItem, MachineType, GridPosition, ItemType } from "@shared/schema";
import { Loader2, Play, Pause, RotateCcw, Save, ArrowLeft } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

// --- GAME SIMULATION LOGIC ---

type GameState = 'editing' | 'running' | 'paused' | 'completed';

export default function Game() {
  const { id } = useParams();
  const [, setLocation] = useLocation();
  const levelId = Number(id);
  const { data: level, isLoading } = useLevel(levelId);
  const { toast } = useToast();
  const submitScore = useSubmitScore();

  // Game State
  const [machines, setMachines] = useState<Machine[]>([]);
  const [items, setItems] = useState<GameItem[]>([]);
  const [gameState, setGameState] = useState<GameState>('editing');
  const [selectedTool, setSelectedTool] = useState<MachineType | 'delete' | null>(null);
  const [score, setScore] = useState(0);
  const [targetProgress, setTargetProgress] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0); // seconds

  const tickRate = 500; // ms
  const tickRef = useRef<NodeJS.Timeout | null>(null);

  // Load initial layout
  useEffect(() => {
    if (level?.layout) {
      // If layout saved in DB, restore it (not implemented in schema fully yet, placeholder)
      // For now, start empty or with level defaults
    }
  }, [level]);

  // Simulation Tick
  const runTick = useCallback(() => {
    setItems((currentItems) => {
      const nextItems: GameItem[] = [];
      const machineMap = new Map<string, Machine>();
      machines.forEach(m => machineMap.set(`${m.position.x},${m.position.y}`, m));
      
      let newScore = score;
      let newProgress = targetProgress;

      // 1. Process Existing Items (Move & Transform)
      currentItems.forEach(item => {
        const key = `${item.position.x},${item.position.y}`;
        const currentMachine = machineMap.get(key);

        let nextPos = { ...item.position };
        let nextType = item.type;
        let consumed = false;

        // Logic based on machine type at CURRENT position
        if (currentMachine) {
          switch (currentMachine.type) {
            case 'conveyor_right': nextPos.x += 1; break;
            case 'conveyor_left': nextPos.x -= 1; break;
            case 'conveyor_down': nextPos.y += 1; break;
            case 'conveyor_up': nextPos.y -= 1; break;
            
            case 'cutter':
              if (item.type === 'raw_material') nextType = 'cut_material';
              // Cutter acts as conveyor right for simplicity in MVP, or static?
              // Let's make processing machines pass item to the right after processing
              nextPos.x += 1; 
              break;
              
            case 'painter':
              if (item.type === 'cut_material') nextType = 'painted_material';
              nextPos.x += 1;
              break;
              
            case 'boxer':
              if (item.type === 'painted_material') nextType = 'packaged_product';
              nextPos.x += 1;
              break;

            case 'sink':
              // Check if matches target
              const target = level?.targetItems as { type: string, count: number };
              if (item.type === target.type) {
                newScore += 100;
                newProgress += 1;
              } else {
                newScore += 10; // Trash score
              }
              consumed = true;
              break;
          }
        }

        // Boundary check
        if (!consumed && 
            nextPos.x >= 0 && nextPos.x < (level?.gridWidth || 10) &&
            nextPos.y >= 0 && nextPos.y < (level?.gridHeight || 10)) {
          
          nextItems.push({
            ...item,
            position: nextPos,
            type: nextType
          });
        }
      });

      // 2. Spawn New Items
      machines.filter(m => m.type === 'spawner').forEach(spawner => {
        // Only spawn if tile is empty (simplified collision)
        const isOccupied = nextItems.some(i => i.position.x === spawner.position.x && i.position.y === spawner.position.y);
        if (!isOccupied) {
          nextItems.push({
            id: Math.random().toString(36).substr(2, 9),
            type: 'raw_material',
            position: { ...spawner.position },
            progress: 0
          });
        }
      });

      // Update score state from inside the loop
      if (newScore !== score) setScore(newScore);
      if (newProgress !== targetProgress) setTargetProgress(newProgress);

      return nextItems;
    });

    setElapsedTime(t => t + (tickRate/1000));
  }, [machines, level, score, targetProgress]);

  // Loop Effect
  useEffect(() => {
    if (gameState === 'running') {
      tickRef.current = setInterval(runTick, tickRate);
    } else {
      if (tickRef.current) clearInterval(tickRef.current);
    }
    return () => { if (tickRef.current) clearInterval(tickRef.current); };
  }, [gameState, runTick]);

  // Win Condition
  useEffect(() => {
    const target = level?.targetItems as { count: number } | undefined;
    if (target && targetProgress >= target.count && gameState === 'running') {
      setGameState('completed');
      toast({
        title: "LEVEL COMPLETE!",
        description: `Target met in ${Math.floor(elapsedTime)}s`,
        className: "font-mono border-2 border-black"
      });
      // Submit score automatically?
      handleGameComplete();
    }
  }, [targetProgress, level, gameState, elapsedTime, toast]);

  const handleGameComplete = () => {
    submitScore.mutate({
      levelId,
      playerName: "Player 1", // Prompt for this in a real app
      score,
      timeTaken: Math.floor(elapsedTime)
    });
  };

  const handleTileClick = (pos: GridPosition) => {
    if (gameState === 'running') return; // No editing while running

    if (selectedTool === 'delete') {
      setMachines(prev => prev.filter(m => m.position.x !== pos.x || m.position.y !== pos.y));
      return;
    }

    if (selectedTool) {
      // Remove existing at this pos first
      const others = machines.filter(m => m.position.x !== pos.x || m.position.y !== pos.y);
      setMachines([...others, {
        id: Math.random().toString(36),
        type: selectedTool,
        position: pos
      }]);
    }
  };

  const handleReset = () => {
    setGameState('editing');
    setItems([]);
    setScore(0);
    setTargetProgress(0);
    setElapsedTime(0);
  };

  const handleClearGrid = () => {
    handleReset();
    setMachines([]);
  };

  if (isLoading || !level) return <div className="h-screen flex items-center justify-center"><Loader2 className="animate-spin w-10 h-10" /></div>;

  const target = level.targetItems as { type: string, count: number };

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8 flex flex-col items-center">
      {/* Header / Nav */}
      <div className="w-full max-w-6xl mb-4 flex justify-between items-center">
        <RetroButton size="sm" onClick={() => setLocation('/')}>
          <ArrowLeft className="w-4 h-4 mr-2 inline" /> Back to Menu
        </RetroButton>
        <div className="bg-white px-4 py-2 border-2 border-black font-display text-xl uppercase tracking-widest shadow-retro">
          Level: {level.name}
        </div>
        <div className="w-[100px]" /> {/* Spacer */}
      </div>

      <div className="flex flex-col lg:flex-row gap-6 max-w-6xl w-full h-[80vh]">
        
        {/* LEFT: Game Board Window */}
        <RetroWindow title="Factory Floor View" className="flex-1 min-h-[500px]">
          <div className="h-full flex flex-col items-center justify-center bg-gray-50 overflow-auto p-8">
             <GameBoard 
               width={level.gridWidth} 
               height={level.gridHeight}
               machines={machines}
               items={items}
               onTileClick={handleTileClick}
               isRunning={gameState === 'running'}
             />
          </div>
        </RetroWindow>

        {/* RIGHT: Controls & Stats */}
        <div className="w-full lg:w-80 flex flex-col gap-6">
          
          {/* Status Panel */}
          <RetroWindow title="Production Status" height="h-auto">
            <div className="space-y-4 font-mono text-sm">
              <div className="flex justify-between border-b border-black/10 pb-2">
                <span>Target:</span>
                <span className="font-bold">{targetProgress} / {target.count}</span>
              </div>
              <div className="flex justify-between border-b border-black/10 pb-2">
                <span>Product:</span>
                <span className="uppercase">{target.type.replace('_', ' ')}</span>
              </div>
              <div className="flex justify-between border-b border-black/10 pb-2">
                <span>Time:</span>
                <span>{Math.floor(elapsedTime)}s</span>
              </div>
              <div className="flex justify-between">
                <span>Score:</span>
                <span className="font-bold text-lg">{score}</span>
              </div>
            </div>
          </RetroWindow>

          {/* Controls */}
          <RetroWindow title="System Controls" height="h-auto">
             <div className="grid grid-cols-2 gap-2 mb-4">
                <RetroButton 
                  onClick={() => setGameState(gameState === 'running' ? 'paused' : 'running')}
                  className={gameState === 'running' ? 'bg-yellow-100' : ''}
                  disabled={gameState === 'completed'}
                >
                  {gameState === 'running' ? <Pause className="w-4 h-4 mx-auto" /> : <Play className="w-4 h-4 mx-auto" />}
                </RetroButton>
                <RetroButton onClick={handleReset} variant="secondary">
                  <RotateCcw className="w-4 h-4 mx-auto" />
                </RetroButton>
             </div>
             <RetroButton onClick={handleClearGrid} variant="danger" size="sm" className="w-full">
               Clear Floor
             </RetroButton>
          </RetroWindow>

          {/* Toolbox */}
          <RetroWindow title="Machine Parts" className="flex-1">
            <MachineToolbar 
              selectedTool={selectedTool}
              onSelectTool={setSelectedTool}
              availableMachines={level.availableMachines as string[]}
            />
          </RetroWindow>
          
        </div>
      </div>
    </div>
  );
}
