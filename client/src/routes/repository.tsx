import { Stack, Group, Anchor } from "@mantine/core";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { useState } from "react";
import { RepositoryTabs } from "../component/repository-tabs";
import { type Repository, type Branch } from "../schema";
import { useAuth } from "../auth";

export default function Repository() {
  const navigate = useNavigate();
  const { userName } = useAuth();
  const { repo_name } = useParams();
  const location = useLocation();
  const { repo } = location.state;

  const [repository, setRepository] = useState<Repository>({
    repo_name: repo.repo_name,
    description: repo.description,
    bucket_url: "https://test-bucket.com",
    default_branch: repo.default_branch,
    branches: repo.branches.map((branch: Branch) => branch.branch_name),
    created_at: repo.created_at,
    storage_bucket_url: repo.storage_bucket_url
  });


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
