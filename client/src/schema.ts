import { z } from "zod";
export interface Repository {
  repo_name: string;
  description?: string;
  bucket_url: string;
  default_branch: string;
  branches: string[];
  created_at?: string;
}

export const createRepositorySchema = z.object({
  repo_name: z.string().min(1, "Enter a repository name"),
  description: z.string().optional(),
  gc_bucket: z.string().url().optional(),
  default_branch: z.string().min(1, "Enter a default branch"),
});

export const uploadObjectModalSchema = z.object({
  objectName: z.string().min(1, "Object name is required"),
  file: z.any().refine((file) => file instanceof File, {
    message: "File is required",
  }),
});

export const loginSchema = z.object({
  username: z.string().min(1, "Enter a username"),
  password: z.string().min(1, "Enter a password"),
});

export type UploadObjectModalSchemaValues = z.infer<
  typeof uploadObjectModalSchema
>;
export type CreateRepositorySchemaValues = z.infer<
  typeof createRepositorySchema
>;
