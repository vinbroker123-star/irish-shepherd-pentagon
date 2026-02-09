import React from 'react';
import { cn } from '@/lib/utils';

interface RetroButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  active?: boolean;
}

export function RetroButton({ 
  children, 
  className, 
  variant = 'primary', 
  size = 'md',
  active = false,
  ...props 
}: RetroButtonProps) {
  const baseStyles = "font-mono font-bold uppercase border-2 border-black transition-all duration-75 active:shadow-retro-active disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variants = {
    primary: "bg-white text-black shadow-retro hover:shadow-retro-hover",
    secondary: "bg-gray-100 text-black border-dashed shadow-retro hover:shadow-retro-hover",
    danger: "bg-black text-white shadow-retro hover:bg-gray-800",
  };

  const sizes = {
    sm: "px-2 py-1 text-xs",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base",
  };
  
  const activeState = active ? "translate-x-[2px] translate-y-[2px] shadow-[0_0_0_0_black] bg-gray-200" : "";

  return (
    <button 
      className={cn(baseStyles, variants[variant], sizes[size], activeState, className)}
      {...props}
    >
      {children}
    </button>
  );
}
