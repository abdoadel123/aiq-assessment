import { IsNotEmpty, IsString } from "class-validator";

export class UpdatePlantsDto {
  @IsString()
  @IsNotEmpty()
  excelPath: string;

  @IsString()
  @IsNotEmpty()
  sheetName: string;
}
