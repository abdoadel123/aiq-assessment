import { NextFunction, Request, Response } from "express";
import { AppError, ValidationError } from "../errors/custom-errors";
import { IResponse } from "../types";

export const errorHandler = (
  err: Error | AppError,
  req: Request,
  res: Response,
  _next: NextFunction
) => {
  let error = err;

  if (!(error instanceof AppError)) {
    const message = error.message || "Something went wrong";
    error = new AppError(message, 500);
  }

  const appError = error as AppError;

  console.error(`Error on ${req.method} ${req.path}`, {
    statusCode: appError.statusCode,
    message: appError.message,
    isOperational: appError.isOperational,
    body: req.body,
    params: req.params,
    query: req.query
  });

  if (!appError.isOperational) {
    console.error("UNEXPECTED ERROR:", error);
  }

  const response: IResponse<null> = {
    success: false,
    error: appError.message
  };

  if (appError instanceof ValidationError && appError.details) {
    (response as any).details = appError.details;
  }

  if (process.env.NODE_ENV === "development") {
    (response as any).stack = appError.stack;
  }

  res.status(appError.statusCode).json(response);
};

export const notFoundHandler = (_req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: "Route not found"
  } as IResponse<null>);
};
