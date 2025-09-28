export interface IPowerPlant {
  orispl: number;
  name: string;
  state: string;
  latitude: number;
  longitude: number;
  annualNetGeneration: number;
  percentage?: number;
}
