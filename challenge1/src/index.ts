import cors from "cors";
import "dotenv/config";
import express from "express";
import "reflect-metadata";
import { connectDatabase } from "./config/database";
import { errorHandler, notFoundHandler } from "./middlewares/error-handler.middleware";
import plantsRouter from "./routers/plants.router";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use("/api", plantsRouter);

app.use(notFoundHandler);

app.use(errorHandler);

process.on("unhandledRejection", (reason: Error | any) => {
  console.error("Unhandled Rejection:", reason);
});

process.on("uncaughtException", (error: Error) => {
  console.error("Uncaught Exception:", error);
  process.exit(1);
});

async function startServer() {
  try {
    await connectDatabase();

    app.listen(PORT, () => {
      console.info(`🚀 Server running on http://localhost:${PORT}`);
      console.info("API endpoints:", {
        endpoints: ["POST /api/v1/plants/update", "GET /api/v1/plants"]
      });
    });
  } catch (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
}

startServer();

export default app;
