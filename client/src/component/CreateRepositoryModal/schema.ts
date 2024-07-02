import { z } from "zod";

export const createRepositorySchema = z.object({
  repo_name: z.string().min(1, "Enter a repository name"),
  description: z.string().optional(),
  gc_bucket: z.string().url().optional(),
  default_branch: z.string().min(1, "Enter a default branch"),
});

export type CreateRepositorySchemaValues = z.infer<
  typeof createRepositorySchema
>;
