import { Stack, Group, Anchor } from "@mantine/core";
import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import { RepositoryTabs } from "../component/repository-tabs";
import { type Repository } from "../schema";
import { useAuth } from "../auth";

export default function Repository() {
  const navigate = useNavigate();
  const { userName } = useAuth();
  const { repo_name } = useParams();

  const [repository, setRepository] = useState<Repository>({
    repo_name: "test",
    description: "test description",
    bucket_url: "https://test-bucket.com",
    default_branch: "main",
    branches: ["main", "branch1", "branch2"],
    created_at: new Date().toLocaleDateString(),
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
