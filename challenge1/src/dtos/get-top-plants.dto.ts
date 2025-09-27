import { IsOptional, IsString, IsNumberString, Min, Max, Length, Matches } from 'class-validator';
import { Transform } from 'class-transformer';

export class GetTopPlantsDto {
  @IsOptional()
  @IsNumberString({}, { message: 'Parameter n must be a number' })
  @Transform(({ value }) => parseInt(value))
  @Min(1, { message: 'Parameter n must be at least 1' })
  @Max(1000, { message: 'Parameter n must not exceed 1000' })
  n?: number = 10;

  @IsOptional()
  @IsString()
  @Length(2, 2, { message: 'State code must be exactly 2 characters' })
  @Matches(/^[A-Z]{2}$/i, { message: 'State code must be a valid 2-letter abbreviation' })
  @Transform(({ value }) => value?.toUpperCase())
  state?: string;
}