import * as fs from "fs";
import * as XLSX from "xlsx";
import { FileNotFoundError } from "../errors/custom-errors";
import { IPowerPlant } from "../types";

export async function convertExcelToJson(
  excelPath: string,
  sheetName = "PLNT21"
): Promise<IPowerPlant[]> {
  if (!fs.existsSync(excelPath)) {
    throw new FileNotFoundError(excelPath);
  }

  console.log("Reading Excel file:", excelPath);

  const data = XLSX.readFile(excelPath);

  const plantSheet = data.Sheets[sheetName];

  if (!plantSheet) throw new Error(`${sheetName} sheet not found in the Excel file`);

  const rawData = XLSX.utils.sheet_to_json(plantSheet);

  console.log(`Found ${rawData.length} plants in Excel file`);

  const plants = rawData.flatMap((row: any, index: number) => {
    if (index === 0) return [];

    const annualNetGeneration = String(row["Plant annual net generation (MWh)"] || "");

    if (annualNetGeneration.includes("(")) console.log({ annualNetGeneration });

    const annualNetGenerationToNumber = annualNetGeneration ? parseFloat(annualNetGeneration) : 0;

    return {
      id: row["Plant file sequence number"],
      name: row["Plant name"],
      state: row["Plant state abbreviation"],
      latitude: parseFloat(row["Plant latitude"]) || 0,
      longitude: parseFloat(row["Plant longitude"]) || 0,
      annualNetGeneration: annualNetGenerationToNumber
    } as IPowerPlant;
  });

  return plants.sort((a, b) => b.annualNetGeneration - a.annualNetGeneration);
}
