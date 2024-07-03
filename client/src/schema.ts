export interface Repository {
  repo_name: string;
  description?: string;
  bucket_url: string;
  default_branch: string;
  branches: string[];
}
