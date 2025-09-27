import { plantRepository } from "../repositories/plant.repository";
import { IPowerPlant } from "../types";
import { convertExcelToJson } from "../utils/excel-to-json.utility";

class PlantsService {
  async updateDataFromExcel(excelPath: string, sheetName: string) {
    const plants = await convertExcelToJson(excelPath, sheetName);
    await plantRepository.bulkInsert(plants);
    console.log("Data updated from Excel file and saved to MongoDB");
  }

  async getTopPlants(limit = 100, state?: string): Promise<IPowerPlant[]> {
    const plants = await plantRepository.findTop(limit, state);
    const { total } = await plantRepository.aggregateTotalGeneration(state);

    return plants.map((plant) => {
      return {
        id: plant.id,
        name: plant.name,
        state: plant.state,
        annualNetGeneration: plant.annualNetGeneration,
        percentage: (plant.annualNetGeneration / total) * 100
      };
    });
  }
}

export default new PlantsService();
