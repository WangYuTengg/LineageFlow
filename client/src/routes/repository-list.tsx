import {
  Anchor,
  Box,
  Card,
  Code,
  Divider,
  Group,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useState, useCallback } from "react";
import { useAuth } from "../auth";
import { useNavigate } from "react-router-dom";
import CreateRepository from "../component/create-repo-button";

interface Branch {
  branch_id: string;
  branch_name: string;
  created_timestamp: string;
  updated_timestamp: string;
  latest_commit: string;
  repo_id: string;
}

interface Repository {
  repo_id: string;
  repo_name: string;
  description: string;
  branches: Branch[];
  bucket_url: string;
}

export default function Repositories() {
  const navigate = useNavigate();
  const { userName } = useAuth();
  const [repositories, setRepositories] = useState<Repository[]>([]);

  const fetchRepositories = useCallback(async () => {
    try {
      const response = await fetch(`/api/getAllRepo?username=${userName}`, {
        headers: {
          "Content-Type": "application/json",
        },
        method: "GET",
      });
      const data = await response.json();
      if (response.ok) {
        setRepositories(data);
      } else {
        console.error(data);
      }
    } catch (error) {
      console.error(error);
    }
  }, [userName]);

  useState(() => {
    fetchRepositories();
  });

  const RenderRepositories = repositories.map((repo) => {
    const handleClick = () => {
      navigate(`/u/${userName}/r/${repo.repo_name}`, { state: { repo } });
    };

    return (
      <Card key={repo.repo_id} withBorder shadow="lg" padding="lg" radius="md">
        <Group justify="flex-start" align="center" gap="md">
          <Anchor
            fw={600}
            size="xl"
            onClick={handleClick}
            className="text-blue-400 hover:underline text-2xl font-semibold"
          >
            {repo.repo_name}
          </Anchor>
          <Code px="md" py="2px" c="gray">
            {repo.repo_id}
          </Code>
        </Group>

        <Divider my="xs" />
        <Stack px="xl" gap="xs">
          <Text size="lg" fw={500}></Text>
          <Text size="lg" fw={500}>
            Description: {repo.description}
          </Text>
          <Text size="lg" fw={500}>
            Bucket Name: {repo.bucket_url.split(".com/")[1].split("/")[0]}
          </Text>
          <Text size="lg" fw={500}>
            Branches:
          </Text>
          {repo.branches.map((branch) => (
            <Box key={branch.branch_name} px="lg">
              <Text size="md" fw={500}>
                Branch Name: {branch.branch_name}
              </Text>
              <Text size="sm" c="dimmed">
                Created at:{" "}
                {new Date(branch.created_timestamp).toLocaleString()}
              </Text>
              <Text size="sm" c="dimmed">
                Updated at:{" "}
                {new Date(branch.updated_timestamp).toLocaleString()}
              </Text>
              {branch.latest_commit ? (
                <Text size="sm" c="dimmed">
                  Commit ID: {branch.latest_commit}
                </Text>
              ) : (
                <Text c="dimmed">Commit: No commits yet</Text>
              )}
            </Box>
          ))}
        </Stack>
      </Card>
    );
  });

  return (
    <Stack p="xl">
      <Group justify="space-between">
        <Title order={2}>Your repositories</Title>
        <CreateRepository
          username={userName}
          onCreate={async () => fetchRepositories()}
        />
      </Group>
      {repositories.length ? (
        RenderRepositories
      ) : (
        <Text p="xl" c="dimmed" size="xl">
          No repositories found
        </Text>
      )}
    </Stack>
  );
}
