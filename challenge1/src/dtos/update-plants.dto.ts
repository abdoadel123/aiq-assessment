import { IsNotEmpty, IsString, Matches } from "class-validator";

export class UpdatePlantsDto {
  @IsString()
  @IsNotEmpty()
  @Matches(/\.(xlsx|xls)$/i, {
    message: "Excel path must be a valid Excel file (.xlsx or .xls)"
  })
  excelPath: string;

  @IsString()
  @IsNotEmpty()
  sheetName: string;
}
