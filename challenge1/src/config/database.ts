import mongoose from "mongoose";
import logger from "../utils/logger";

export async function connectDatabase(): Promise<void> {
  const username = process.env.MONGO_USERNAME;
  const password = process.env.MONGO_PASSWORD;
  const host = process.env.MONGO_HOST;
  const port = process.env.MONGO_PORT;
  const dbName = process.env.MONGO_DB_NAME;

  const uri = `mongodb://${username}:${password}@${host}:${port}/${dbName}?authSource=admin`;

  try {
    await mongoose.connect(uri);
    logger.info("✅ MongoDB connected successfully");

    mongoose.connection.on("error", (err) => {
      logger.error(`MongoDB connection error: ${err}`);
    });

    mongoose.connection.on("disconnected", () => {
      logger.warn("MongoDB disconnected");
    });
  } catch (error) {
    logger.error(`Failed to connect to MongoDB: ${error}`);
    process.exit(1);
  }
}

export async function disconnectDatabase(): Promise<void> {
  await mongoose.disconnect();
  logger.info("MongoDB connection closed");
}
