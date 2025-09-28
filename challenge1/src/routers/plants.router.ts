import { Router } from "express";
import { plantsController } from "../controllers";
import { UpdatePlantsDto } from "../dtos";
import { validateDto } from "../middlewares";

const router = Router();

router.get("/", plantsController.getTopPlants);

router.post("/update", validateDto(UpdatePlantsDto), plantsController.updateData);

export const planetRouter = router;
