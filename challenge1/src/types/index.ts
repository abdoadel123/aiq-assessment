export interface IPowerPlant {
  id: number;
  name: string;
  state: string;
  annualNetGeneration: number;
  percentage?: number;
}

export interface IPlantsAndTotals {
  plants: IPowerPlant[];
  total: number;
}

export interface IStateData {
  state: string;
  totalGeneration: number;
  plantCount: number;
}

export interface IResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}
