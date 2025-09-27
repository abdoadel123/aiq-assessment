import { isArray } from "lodash";

export const asArray = <T>(value: T | T[]) => (isArray(value) ? value : [value]);
