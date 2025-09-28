import mongoose from "mongoose";

export async function connectDatabase(): Promise<void> {
  const username = process.env.MONGO_USERNAME;
  const password = process.env.MONGO_PASSWORD;
  const host = process.env.MONGO_HOST;
  const port = process.env.MONGO_PORT;
  const dbName = process.env.MONGO_DB_NAME;

  const uri = `mongodb://${username}:${password}@${host}:${port}/${dbName}?authSource=admin`;

  try {
    await mongoose.connect(uri);
    console.log("✅ MongoDB connected successfully");

    mongoose.connection.on("error", (err) => {
      console.error("MongoDB connection error:", err);
    });

    mongoose.connection.on("disconnected", () => {
      console.log("MongoDB disconnected");
    });
  } catch (error) {
    console.error("Failed to connect to MongoDB:", error);
    process.exit(1);
  }
}

export async function disconnectDatabase(): Promise<void> {
  await mongoose.disconnect();
  console.log("MongoDB connection closed");
}
