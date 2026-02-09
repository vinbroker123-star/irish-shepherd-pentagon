import { pgTable, text, serial, integer, jsonb, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// === TABLE DEFINITIONS ===

export const levels = pgTable("levels", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description").notNull(),
  gridWidth: integer("grid_width").notNull().default(10),
  gridHeight: integer("grid_height").notNull().default(10),
  targetItems: jsonb("target_items").notNull(), // { type: "widget", count: 10 }
  availableMachines: jsonb("available_machines").notNull(), // ["conveyor", "cutter", "painter"]
  layout: jsonb("layout"), // Initial layout (optional)
  order: integer("order").notNull(), // Level order
});

export const highScores = pgTable("high_scores", {
  id: serial("id").primaryKey(),
  levelId: integer("level_id").notNull(),
  playerName: text("player_name").notNull(),
  score: integer("score").notNull(),
  timeTaken: integer("time_taken").notNull(), // in seconds
  createdAt: timestamp("created_at").defaultNow(),
});

// === SCHEMAS ===

export const insertLevelSchema = createInsertSchema(levels);
export const insertHighScoreSchema = createInsertSchema(highScores).omit({ id: true, createdAt: true });

// === EXPLICIT TYPES ===

export type Level = typeof levels.$inferSelect;
export type InsertLevel = z.infer<typeof insertLevelSchema>;

export type HighScore = typeof highScores.$inferSelect;
export type InsertHighScore = z.infer<typeof insertHighScoreSchema>;

export type LevelResponse = Level;
export type HighScoreResponse = HighScore;

// === GAME TYPES (Shared) ===

export type ItemType = 'raw_material' | 'cut_material' | 'painted_material' | 'packaged_product' | 'trash';

export type MachineType = 'conveyor_right' | 'conveyor_down' | 'conveyor_left' | 'conveyor_up' | 'spawner' | 'sink' | 'cutter' | 'painter' | 'boxer';

export interface GridPosition {
  x: number;
  y: number;
}

export interface Machine {
  id: string;
  type: MachineType;
  position: GridPosition;
}

export interface GameItem {
  id: string;
  type: ItemType;
  position: GridPosition;
  progress: number; // 0 to 1 (between tiles)
}
