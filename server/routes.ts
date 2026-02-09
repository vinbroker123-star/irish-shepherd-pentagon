import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { z } from "zod";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // === Levels ===
  app.get(api.levels.list.path, async (req, res) => {
    const levels = await storage.getLevels();
    res.json(levels);
  });

  app.get(api.levels.get.path, async (req, res) => {
    const level = await storage.getLevel(Number(req.params.id));
    if (!level) {
      return res.status(404).json({ message: "Level not found" });
    }
    res.json(level);
  });

  // === Scores ===
  app.get(api.scores.list.path, async (req, res) => {
    const scores = await storage.getHighScores(Number(req.params.levelId));
    res.json(scores);
  });

  app.post(api.scores.submit.path, async (req, res) => {
    try {
      const input = api.scores.submit.input.parse(req.body);
      const score = await storage.createHighScore(input);
      res.status(201).json(score);
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({
          message: err.errors[0].message,
          field: err.errors[0].path.join('.'),
        });
      }
      throw err;
    }
  });

  // === Seeding ===
  await seedDatabase();

  return httpServer;
}

async function seedDatabase() {
  const existingLevels = await storage.getLevels();
  if (existingLevels.length === 0) {
    console.log("Seeding database with levels...");
    
    // Level 1: Basics
    await storage.createLevel({
      name: "The Beginning",
      description: "Produce 10 Raw Materials. Use a Spawner and a Sink.",
      order: 1,
      gridWidth: 10,
      gridHeight: 10,
      targetItems: { type: "raw_material", count: 10 },
      availableMachines: ["spawner", "sink", "conveyor_right", "conveyor_down", "conveyor_left", "conveyor_up"],
      layout: [],
    });

    // Level 2: Cutting Edge
    await storage.createLevel({
      name: "Cutting Edge",
      description: "Produce 10 Cut Materials. You'll need a Cutter.",
      order: 2,
      gridWidth: 10,
      gridHeight: 10,
      targetItems: { type: "cut_material", count: 10 },
      availableMachines: ["spawner", "sink", "cutter", "conveyor_right", "conveyor_down", "conveyor_left", "conveyor_up"],
      layout: [],
    });

    // Level 3: Paint Job
    await storage.createLevel({
      name: "Paint Job",
      description: "Produce 10 Painted Materials. Cut them first, then Paint them.",
      order: 3,
      gridWidth: 10,
      gridHeight: 10,
      targetItems: { type: "painted_material", count: 10 },
      availableMachines: ["spawner", "sink", "cutter", "painter", "conveyor_right", "conveyor_down", "conveyor_left", "conveyor_up"],
      layout: [],
    });

    // Level 4: Full Production
    await storage.createLevel({
      name: "Full Production",
      description: "Produce 5 Packaged Products. Cut -> Paint -> Box.",
      order: 4,
      gridWidth: 12,
      gridHeight: 12,
      targetItems: { type: "packaged_product", count: 5 },
      availableMachines: ["spawner", "sink", "cutter", "painter", "boxer", "conveyor_right", "conveyor_down", "conveyor_left", "conveyor_up"],
      layout: [],
    });
    
    console.log("Seeding complete!");
  }
}
