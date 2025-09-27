import { IPlant, Plant } from "../entities/plant.entity";
import { IPowerPlant } from "../types";

export class PlantRepository {
  async bulkInsert(plants: IPowerPlant[], batchSize = 1000): Promise<void> {
    try {
      await Plant.deleteMany({});
      console.log("Cleared existing plant data");

      for (let i = 0; i < plants.length; i += batchSize) {
        const batch = plants.slice(i, i + batchSize);

        await Plant.insertMany(batch, { ordered: false });

        console.log(`Inserted batch ${Math.floor(i / batchSize) + 1}: ${batch.length} plants`);
      }

      console.log(`Total plants inserted: ${plants.length}`);
    } catch (error) {
      console.error("Error during bulk insert:", error);
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
