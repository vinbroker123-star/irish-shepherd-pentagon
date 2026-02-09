import { db } from "./db";
import {
  levels,
  highScores,
  type Level,
  type InsertLevel,
  type HighScore,
  type InsertHighScore,
} from "@shared/schema";
import { eq, desc } from "drizzle-orm";

export interface IStorage {
  // Levels
  getLevels(): Promise<Level[]>;
  getLevel(id: number): Promise<Level | undefined>;
  createLevel(level: InsertLevel): Promise<Level>;
  
  // Scores
  getHighScores(levelId: number): Promise<HighScore[]>;
  createHighScore(score: InsertHighScore): Promise<HighScore>;
}

export class DatabaseStorage implements IStorage {
  async getLevels(): Promise<Level[]> {
    return await db.select().from(levels).orderBy(levels.order);
  }

  async getLevel(id: number): Promise<Level | undefined> {
    const [level] = await db.select().from(levels).where(eq(levels.id, id));
    return level;
  }

  async createLevel(level: InsertLevel): Promise<Level> {
    const [newLevel] = await db.insert(levels).values(level).returning();
    return newLevel;
  }

  async getHighScores(levelId: number): Promise<HighScore[]> {
    return await db
      .select()
      .from(highScores)
      .where(eq(highScores.levelId, levelId))
      .orderBy(desc(highScores.score), desc(highScores.timeTaken))
      .limit(10);
  }

  async createHighScore(score: InsertHighScore): Promise<HighScore> {
    const [newScore] = await db.insert(highScores).values(score).returning();
    return newScore;
  }
}

export const storage = new DatabaseStorage();
