import { NextFunction, Request, Response } from "express";
import { UpdatePlantsDto } from "../dtos";
import { BadRequestError } from "../errors";
import { plantsService } from "../services";

class PlantsController {
  public async getTopPlants(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const limit = parseInt(req.query.limit as string);
      const state = req.query.state as string;

      if (!limit || limit > 100) throw new BadRequestError("N should be from 1 to 100");

      const plants = await plantsService.getTopPlants(limit, state);

      res.json({
        success: true,
        data: plants
      });
    } catch (error) {
      next(error);
    }
  }

  public async updateData(req: Request, res: Response, next: NextFunction) {
    try {
      const dto: UpdatePlantsDto = req.body;

      await plantsService.updateDataFromExcel(dto.excelPath, dto.sheetName || "PLNT21");

      res.status(201).json({
        success: true,
        message: "Data updated successfully"
      });
    } catch (error) {
      next(error);
    }
  }
}

export const plantsController = new PlantsController();
