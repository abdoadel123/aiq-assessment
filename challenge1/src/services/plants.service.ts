import { IPowerPlant } from "../interfaces";
import { plantRepository } from "../repositories";
import { convertExcelToJson } from "../utils";
import logger from "../utils/logger";

class PlantsService {
  async updateDataFromExcel(excelPath: string, sheetName: string) {
    const data = await convertExcelToJson(excelPath, sheetName);

    const plants = data.flatMap((row: any, index: number) => {
      if (index === 0) return [];

      const annualNetGeneration = String(row["Plant annual net generation (MWh)"] || "");

      if (annualNetGeneration.includes("("))
        logger.debug(`Annual net generation with parenthesis: ${annualNetGeneration}`);

      const annualNetGenerationToNumber = annualNetGeneration ? parseFloat(annualNetGeneration) : 0;

      return {
        orispl: row["DOE/EIA ORIS plant or facility code"],
        name: row["Plant name"],
        state: row["Plant state abbreviation"],
        latitude: parseFloat(row["Plant latitude"]) || 0,
        longitude: parseFloat(row["Plant longitude"]) || 0,
        annualNetGeneration: annualNetGenerationToNumber
      } as IPowerPlant;
    });

    await plantRepository.bulkUpsert(
      plants.sort((a, b) => b.annualNetGeneration - a.annualNetGeneration)
    );

    logger.info("Data updated from Excel file and saved to MongoDB");
  }

  async getTopPlants(limit = 100, state?: string) {
    const plants = await plantRepository.findTop(limit, state);
    const { total } = await plantRepository.aggregateTotalGeneration(state);

    const plantsWithPercentage = plants.map((plant) => {
      return {
        orispl: plant.id,
        name: plant.name,
        state: plant.state,
        annualNetGeneration: plant.annualNetGeneration,
        percentage: Number(((plant.annualNetGeneration / total) * 100).toFixed(2))
      };
    });

    return {
      total,
      plants: plantsWithPercentage
    };
  }
}

export const plantsService = new PlantsService();
