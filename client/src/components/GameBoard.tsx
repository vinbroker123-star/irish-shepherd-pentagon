import { useState, useEffect, useRef } from 'react';
import { Machine, GameItem, MachineType, GridPosition } from '@shared/schema';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, ArrowDown, ArrowLeft, ArrowUp, Zap, Scissors, Brush, Box, PackageOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

// --- GAME LOGIC HELPERS ---

const TILE_SIZE = 48; // px

const MACHINE_ICONS = {
  conveyor_right: ArrowRight,
  conveyor_down: ArrowDown,
  conveyor_left: ArrowLeft,
  conveyor_up: ArrowUp,
  spawner: Zap,
  sink: PackageOpen,
  cutter: Scissors,
  painter: Brush,
  boxer: Box,
};

// Item colors/shapes mapping
const ITEM_STYLES: Record<string, string> = {
  raw_material: "bg-gray-300 rounded-full border-2 border-black",
  cut_material: "bg-gray-300 rotate-45 border-2 border-black", // Diamond
  painted_material: "bg-black rounded-full border-2 border-white ring-2 ring-black",
  packaged_product: "bg-white border-4 border-black", // Box
  trash: "bg-red-500 rounded-full opacity-50",
};

interface GameBoardProps {
  width: number;
  height: number;
  machines: Machine[];
  items: GameItem[];
  onTileClick: (pos: GridPosition) => void;
  isRunning: boolean;
}

export function GameBoard({ width, height, machines, items, onTileClick, isRunning }: GameBoardProps) {
  // Create grid cells
  const grid = Array.from({ length: height }, (_, y) => 
    Array.from({ length: width }, (_, x) => ({ x, y }))
  );

  return (
    <div 
      className="relative bg-white border-2 border-black shadow-inner"
      style={{ 
        width: width * TILE_SIZE, 
        height: height * TILE_SIZE 
      }}
    >
      {/* Grid Pattern */}
      <div 
        className="absolute inset-0 pointer-events-none" 
        style={{
          backgroundImage: `
            linear-gradient(to right, #eee 1px, transparent 1px),
            linear-gradient(to bottom, #eee 1px, transparent 1px)
          `,
          backgroundSize: `${TILE_SIZE}px ${TILE_SIZE}px`
        }}
      />

      {/* Render Machines */}
      {machines.map((machine) => {
        const Icon = MACHINE_ICONS[machine.type];
        return (
          <div
            key={machine.id}
            className="absolute flex items-center justify-center text-black"
            style={{
              left: machine.position.x * TILE_SIZE,
              top: machine.position.y * TILE_SIZE,
              width: TILE_SIZE,
              height: TILE_SIZE,
            }}
          >
            <div className={cn(
              "w-full h-full flex items-center justify-center border border-gray-100",
              // Style machines based on type
              machine.type.startsWith('conveyor') ? "text-gray-400" : "bg-gray-100 border-2 border-black z-10"
            )}>
              <Icon className="w-6 h-6" strokeWidth={2.5} />
            </div>
          </div>
        );
      })}

      {/* Render Items */}
      <AnimatePresence>
        {items.map((item) => (
          <motion.div
            key={item.id}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              x: item.position.x * TILE_SIZE + (TILE_SIZE / 2) - 10, // Center 20px item
              y: item.position.y * TILE_SIZE + (TILE_SIZE / 2) - 10,
              scale: 1, 
              opacity: 1 
            }}
            exit={{ scale: 0, opacity: 0 }}
            transition={{ 
              duration: 0.3, // Match tick rate roughly
              ease: "linear"
            }}
            className={cn(
              "absolute w-5 h-5 z-20 shadow-sm pointer-events-none",
              ITEM_STYLES[item.type] || ITEM_STYLES['raw_material']
            )}
          />
        ))}
      </AnimatePresence>

      {/* Interaction Layer */}
      <div className="absolute inset-0 grid" style={{
        gridTemplateColumns: `repeat(${width}, 1fr)`,
        gridTemplateRows: `repeat(${height}, 1fr)`
      }}>
        {grid.map((row, y) => row.map((cell, x) => (
          <div 
            key={`${x}-${y}`}
            onClick={() => onTileClick({ x, y })}
            className="hover:bg-black/5 active:bg-black/10 transition-colors cursor-crosshair border border-transparent hover:border-black/10"
          />
        )))}
      </div>
    </div>
  );
}
