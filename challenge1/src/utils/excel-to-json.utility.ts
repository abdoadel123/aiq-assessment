import * as fs from "fs";
import * as XLSX from "xlsx";
import { NotFoundError } from "../errors";
import logger from "./logger";

export async function convertExcelToJson(excelPath: string, sheetName = "PLNT21") {
  if (!fs.existsSync(excelPath)) {
    throw new NotFoundError("File Not found");
  }

  logger.info(`Reading Excel file: ${excelPath}`);

  const data = XLSX.readFile(excelPath);

  const plantSheet = data.Sheets[sheetName];

  if (!plantSheet) throw new Error(`${sheetName} sheet not found in the Excel file`);

  const rawData = XLSX.utils.sheet_to_json(plantSheet);

  logger.info(`Found ${rawData.length} plants in Excel file`);

  return rawData;
}
