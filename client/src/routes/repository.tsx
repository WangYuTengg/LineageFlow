import { Stack, Group, Anchor } from "@mantine/core";
import { useNavigate, useLocation } from "react-router-dom";
import { RepositoryTabs } from "../component/repository-tabs";
import { type Repository, type Branch } from "../schema";
import { useAuth } from "../auth";

export default function Repository() {
  const navigate = useNavigate();
  const location = useLocation();
  const { repo } = location.state;
  const { userName } = useAuth();

  const repository: Repository = {
    repo_id: repo.repo_id,
    repo_name: repo.repo_name,
    description: repo.description,
    bucket_url: "https://test-bucket.com",
    default_branch: repo.default_branch || "main",
    branches: repo.branches.map((branch: Branch) => branch.branch_name),
    created_at: repo.created_at,
    storage_bucket_url: repo.storage_bucket_url,
  };

  return (
    <>
      <Stack px="sm">
        <Group bg="gray" p="md">
          <Anchor
            c="blue"
            size="lg"
            onClick={() => navigate(`/u/${userName}/repositories`)}
          >
            Repositories
          </Anchor>
        </Group>
        <RepositoryTabs selectedRepository={repository} />
      </Stack>
    </>
  );
}
