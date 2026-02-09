import { MachineType } from '@shared/schema';
import { RetroButton } from './RetroButton';
import { ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Box, Brush, Scissors, Trash2, Zap } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MachineToolbarProps {
  selectedTool: MachineType | 'delete' | null;
  onSelectTool: (tool: MachineType | 'delete' | null) => void;
  availableMachines: string[];
}

export function MachineToolbar({ selectedTool, onSelectTool, availableMachines }: MachineToolbarProps) {
  const tools = [
    { id: 'conveyor_right', icon: ArrowRight, label: 'Conv R' },
    { id: 'conveyor_down', icon: ArrowDown, label: 'Conv D' },
    { id: 'conveyor_left', icon: ArrowLeft, label: 'Conv L' },
    { id: 'conveyor_up', icon: ArrowUp, label: 'Conv U' },
    { id: 'spawner', icon: Zap, label: 'Spawn' },
    { id: 'cutter', icon: Scissors, label: 'Cut' },
    { id: 'painter', icon: Brush, label: 'Paint' },
    { id: 'boxer', icon: Box, label: 'Box' },
    { id: 'sink', icon: Box, label: 'Sink', filled: true },
  ] as const;

  return (
    <div className="grid grid-cols-2 gap-2">
      {tools.filter(t => availableMachines.includes(t.id.split('_')[0]) || availableMachines.includes(t.id)).map((tool) => (
        <RetroButton
          key={tool.id}
          size="sm"
          active={selectedTool === tool.id}
          onClick={() => onSelectTool(tool.id as MachineType)}
          className={cn("flex flex-col items-center justify-center h-20 gap-2", 
            selectedTool === tool.id && "bg-black text-white"
          )}
        >
          <tool.icon className="w-6 h-6" />
          <span className="text-[10px]">{tool.label}</span>
        </RetroButton>
      ))}
      
      <RetroButton
        size="sm"
        variant="danger"
        active={selectedTool === 'delete'}
        onClick={() => onSelectTool('delete')}
        className="flex flex-col items-center justify-center h-20 gap-2 col-span-2 mt-4"
      >
        <Trash2 className="w-6 h-6" />
        <span className="text-[10px]">Remove Tool</span>
      </RetroButton>
    </div>
  );
}
