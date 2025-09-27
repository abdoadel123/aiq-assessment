import { Request, Response, NextFunction } from 'express';
import { validate, ValidationError as ClassValidatorError } from 'class-validator';
import { plainToInstance } from 'class-transformer';
import { ValidationError } from '../errors/custom-errors';

export function validateDto(dtoClass: any) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const dto = plainToInstance(dtoClass, req.body);
      const errors = await validate(dto);

      if (errors.length > 0) {
        const errorMessages = formatValidationErrors(errors);
        throw new ValidationError('Validation failed', errorMessages);
      }

      req.body = dto;
      next();
    } catch (error) {
      next(error);
    }
  };
}

function formatValidationErrors(errors: ClassValidatorError[]): string[] {
  const messages: string[] = [];

  errors.forEach((error) => {
    if (error.constraints) {
      messages.push(...Object.values(error.constraints));
    }
    if (error.children && error.children.length > 0) {
      messages.push(...formatValidationErrors(error.children));
    }
  });

  return messages;
}