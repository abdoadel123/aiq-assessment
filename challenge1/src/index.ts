import cors from "cors";
import "dotenv/config";
import express from "express";
import "reflect-metadata";
import { connectDatabase } from "./config";
import { errorHandler, notFoundHandler } from "./middlewares";
import { appRouter } from "./routers";
import logger from "./utils/logger";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use(appRouter);

app.use(notFoundHandler);

app.use(errorHandler);

process.on("unhandledRejection", (reason: Error | any) => {
  logger.error(`Unhandled Rejection: ${reason}`);
});

process.on("uncaughtException", (error: Error) => {
  logger.error(`Uncaught Exception: ${error}`);
  process.exit(1);
});

async function startServer() {
  try {
    await connectDatabase();

    app.listen(PORT, () => {
      logger.info(`🚀 Server running on http://localhost:${PORT}`);
      logger.info("API endpoints: POST /api/v1/plants/update, GET /api/v1/plants");
    });
  } catch (error) {
    logger.error(`Failed to start server: ${error}`);
    process.exit(1);
  }
}

startServer();

export default app;
