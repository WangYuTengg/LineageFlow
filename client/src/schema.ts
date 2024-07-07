import { z } from "zod";
export interface Commit {
  commit_id: string;
  commit_message: string;
  created_timestamp: string;
}
export interface UncommittedChanges {
  repo: string;
  branch: string;
  storage_bucket: string;
  changes: {
    file: File | FileResource;
    type: string;
  }[];
}
export interface Branch {
  branch_id: string;
  branch_name: string;
  created_timestamp: string;
  updated_timestamp: string;
  latest_commit: string;
  repo_id: string;
}
export interface FolderContents {
  files: FileResource[];
  folders: { [key: string]: FolderContents };
}
export interface Repository {
  repo_id: string;
  repo_name: string;
  default_branch: string;
  description: string;
  branches: Branch[];
  bucket_url: string;
  created_timestamp: string;
  updated_timestamp: string;
}

export interface MetaData {
  name: string;
  size: number;
  content_type: string;
  updated: string;
  generation: number;
  metageneration: number;
}

export interface FileResource {
  id: number;
  file_name: string;
  loc: string;
  meta_data: MetaData;
  version: number;
  range: number;
}

export const createRepositorySchema = z.object({
  repo_name: z.string().min(1, "Enter a repository name"),
  description: z.string().optional(),
  gc_bucket: z.string().url().optional(),
  default_branch: z.string().min(1, "Enter a default branch"),
});

export const createBranchSchema = z.object({
  branchName: z.string().min(1, "Enter a branch name"),
  parent: z.string().min(1, "Enter a parent branch"),
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

export const signupSchema = z.object({
  username: z.string().min(1, "Enter a username"),
  password: z.string().min(1, "Enter a password"),
  email: z.string().email("Enter a valid email address"),
});

export type SignupSchemaValues = z.infer<typeof signupSchema>;
export type LoginSchemaValues = z.infer<typeof loginSchema>;
export type UploadObjectModalSchemaValues = z.infer<
  typeof uploadObjectModalSchema
>;
export type CreateRepositorySchemaValues = z.infer<
  typeof createRepositorySchema
>;

export interface Branch {
  branch_name: string;
  created_timestamp: string;
  updated_timestamp: string;
  commit_id: string;
  repo_id: string;
}
