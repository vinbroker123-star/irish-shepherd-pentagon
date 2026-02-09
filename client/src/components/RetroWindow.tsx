import React from 'react';
import { cn } from '@/lib/utils';
import { Minus, Square, X } from 'lucide-react';

interface RetroWindowProps {
  title: string;
  children: React.ReactNode;
  className?: string;
  onClose?: () => void;
  width?: string;
  height?: string;
}

export function RetroWindow({ 
  title, 
  children, 
  className,
  onClose,
  width = "w-full",
  height = "h-auto"
}: RetroWindowProps) {
  return (
    <div className={cn(
      "bg-white border-2 border-black shadow-retro-lg flex flex-col overflow-hidden",
      width,
      height,
      className
    )}>
      {/* Title Bar */}
      <div className="h-8 border-b-2 border-black flex items-center justify-between px-2 bg-white relative">
        {/* Striped Background for Drag Area */}
        <div className="absolute inset-0 top-1 bottom-1 left-1 right-1 bg-striped opacity-10 pointer-events-none" />
        
        {/* Close Button (Left) */}
        <button 
          onClick={onClose}
          className="relative z-10 w-4 h-4 border border-black bg-white flex items-center justify-center hover:bg-black hover:text-white transition-colors"
        >
          {onClose && <div className="w-2 h-2 bg-current" />}
        </button>

        {/* Title */}
        <div className="relative z-10 bg-white px-4 font-display text-sm font-bold uppercase tracking-wider border-x-2 border-transparent">
          {title}
        </div>

        {/* Mock Window Controls (Right) */}
        <div className="flex gap-1 relative z-10">
          <div className="w-4 h-4 border border-black bg-white" />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto bg-white p-4 relative">
        <div className="absolute inset-0 bg-[radial-gradient(#000_1px,transparent_1px)] [background-size:16px_16px] opacity-5 pointer-events-none" />
        <div className="relative z-10 h-full">
          {children}
        </div>
      </div>
    </div>
  );
}
