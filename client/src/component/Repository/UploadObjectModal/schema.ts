import { z } from "zod";

export const uploadObjectModalSchema = z.object({
  objectName: z.string().min(1, "Object name is required"),
  file: z.any().refine((file) => file instanceof File, {
    message: "File is required",
  }),
});

export type UploadObjectModalSchemaValues = z.infer<
  typeof uploadObjectModalSchema
>;
