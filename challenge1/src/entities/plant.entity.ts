import { Document, Schema, model } from "mongoose";

export interface IPlant extends Document {
  orispl: number;
  name: string;
  state: string;
  latitude: number;
  longitude: number;
  annualNetGeneration: number;
}

const PlantSchema = new Schema<IPlant>(
  {
    orispl: {
      type: Number,
      required: true,
      unique: true
    },
    name: {
      type: String,
      required: true
    },
    state: {
      type: String,
      required: true,
      index: true
    },
    latitude: {
      type: Number,
      required: true
    },
    longitude: {
      type: Number,
      required: true
    },
    annualNetGeneration: {
      type: Number,
      required: true,
      index: true
    }
  },
  {
    timestamps: true,
    collection: "plants"
  }
);

PlantSchema.index({ state: 1, annualNetGeneration: -1 });

export const Plant = model<IPlant>("Plant", PlantSchema);
