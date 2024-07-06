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
    default_branch: repo.default_branch,
    branches: repo.branches.map((branch: Branch) => branch.branch_name),
    created_timestamp: repo.created_timestamp,
    bucket_url: repo.bucket_url,
    updated_timestamp: repo.updated_timestamp,
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
