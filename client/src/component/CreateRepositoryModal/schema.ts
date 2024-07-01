import { z } from "zod";

export const createRepositorySchema = z.object({
  repositoryName: z.string().min(1, "Enter a repository name"),
  description: z.string().optional(),
  storageNamespace: z.string().optional(),
  defaultBranch: z.string().min(1, "Enter a default branch"),
});

export type CreateRepositorySchemaValues = z.infer<
  typeof createRepositorySchema
>;
