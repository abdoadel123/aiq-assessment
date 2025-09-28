import { Router } from "express";
import { planetRouter } from "./plants.router";

const appRouter = Router();

appRouter.use("/api/v1/plants", planetRouter);

export { appRouter };
