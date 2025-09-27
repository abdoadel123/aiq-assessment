import { Router } from "express";
import plantsController from "../controllers/plants.controller";
import { UpdatePlantsDto } from "../dtos/update-plants.dto";
import { validateDto } from "../middlewares/validation.middleware";

const router = Router();

router.get("/v1/plants", plantsController.getTopPlants);
router.post("/v1/plants/update", validateDto(UpdatePlantsDto), plantsController.updateData);

export default router;
