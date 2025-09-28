import { IPlant, Plant } from "../entities";
import { IPowerPlant } from "../interfaces";
import logger from "../utils/logger";

export class PlantRepository {
  async bulkUpsert(plants: IPowerPlant[], batchSize = 1000): Promise<void> {
    try {
      let totalUpserted = 0;
      let totalModified = 0;

      for (let i = 0; i < plants.length; i += batchSize) {
        const batch = plants.slice(i, i + batchSize);

        const bulkOps = batch.map((plant) => ({
          updateOne: {
            filter: { orispl: plant.orispl },
            update: {
              $set: {
                orispl: plant.orispl,
                name: plant.name,
                state: plant.state,
                latitude: plant.latitude,
                longitude: plant.longitude,
                annualNetGeneration: plant.annualNetGeneration
              }
            },
            upsert: true
          }
        }));

        const result = await Plant.bulkWrite(bulkOps, { ordered: false });

        totalUpserted += result.upsertedCount;
        totalModified += result.modifiedCount;

        logger.info(
          `Processed batch ${Math.floor(i / batchSize) + 1}: ${batch.length} plants (${
            result.upsertedCount
          } inserted, ${result.modifiedCount} updated)`
        );
      }

      logger.info(
        `Total plants processed: ${plants.length} (${totalUpserted} inserted, ${totalModified} updated)`
      );
    } catch (error) {
      logger.error(`Error during bulk upsert: ${error}`);
      throw error;
    }
  }

  async findTop(limit = 100, state?: string): Promise<IPlant[]> {
    const filter = {
      ...(state && { state })
    };
    return Plant.find(filter).sort({ annualNetGeneration: -1 }).limit(limit).exec();
  }

  async aggregateTotalGeneration(state?: string): Promise<{ total: number; count: number }> {
    const pipeline: any[] = [];

    if (state) {
      pipeline.push({ $match: { state } });
    }

    pipeline.push({
      $group: {
        _id: null,
        total: { $sum: "$annualNetGeneration" },
        count: { $sum: 1 }
      }
    });

    const result = await Plant.aggregate(pipeline);

    if (result.length === 0) {
      return { total: 0, count: 0 };
    }

    return {
      total: result[0].total,
      count: result[0].count
    };
  }
}

export const plantRepository = new PlantRepository();
