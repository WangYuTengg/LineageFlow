import {
  Anchor,
  Box,
  Card,
  Divider,
  Group,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useState, useEffect } from "react";
import { useAuth } from "../auth";
import { useNavigate } from "react-router-dom";
import CreateRepository from "../component/create-repo-button";

interface Repository {
  repo_name: string;
  description: string;
  bucket_url: string;
  default_branch: string;
  branches: string[];
  created_at: string | null;
}

export default function Repositories() {
  const navigate = useNavigate();
  const { userName } = useAuth();

  // todo: fetch repositories from the server
  const [repositories, setRepositories] = useState<Repository[]>([
    {
      repo_name: "test",
      description: "test description",
      bucket_url: "https://test-bucket.com",
      default_branch: "main",
      branches: ["main", "branch1", "branch2"],
      created_at: new Date().toLocaleDateString(),
    },
    {
      repo_name: "test 2",
      description: "test description 2",
      bucket_url: "https://test-bucket.com",
      default_branch: "main",
      branches: ["main", "branch1", "branch2"],
      created_at: new Date().toLocaleDateString(),
    },
  ]);

  useEffect(() => {
    async function fetchRepositories() {
      try {
        const response = await fetch(
          `http://localhost:5173/api/user/fetchRepositories/${userName}/`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            method: "GET",
          }
        );
        console.log(response);
        const data = await response.json();
        console.log(data);
        if (response.ok && data.repositories) {
          setRepositories(data.repositories);
        } else {
          console.error(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    fetchRepositories();
  }, [userName]);

  const RenderRepositories = repositories.map((repo) => {
    const createdAt = repo.created_at ? new Date(repo.created_at) : null;
    const createdAtStr =
      createdAt && !isNaN(createdAt.getTime())
        ? createdAt.toISOString()
        : "Invalid date";

    const handleClick = () => {
      navigate(`/u/${userName}/r/${repo.repo_name}`);
    };

    return (
      <Card
        key={repo.repo_name}
        withBorder
        shadow="lg"
        padding="lg"
        radius="md"
      >
        <Anchor
          size="xl"
          onClick={handleClick}
          className="text-blue-400 hover:underline text-2xl font-semibold"
        >
          {repo.repo_name}
        </Anchor>
        <Divider my="xs" />
        <Box px="lg">
          <Text size="lg" fw={500}>
            Created at: {new Date(createdAtStr).toLocaleDateString()},{" "}
            {new Date(createdAtStr).toLocaleTimeString()}
          </Text>
          <Group>
            <Text c="dimmed">Default branch: {repo.default_branch},</Text>
            <Text c="dimmed">Storage namespace: {repo.bucket_url}</Text>
          </Group>{" "}
        </Box>
      </Card>
    );
  });

  return (
    <Stack p="xl">
      <Group justify="space-between">
        <Title order={2}>Your repositories</Title>
        <CreateRepository />
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
