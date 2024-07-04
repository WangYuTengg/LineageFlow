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

interface Branch {
  branch_name: string;
  created_timestamp: string;
  updated_timestamp: string;
  commit_id: string;
  repo_id: string;
}

interface Repository {
  repo_id: string;
  repo_name: string;
  description: string;
  branches: Branch[];
}

export default function Repositories() {
  const navigate = useNavigate();
  const { userName } = useAuth();

  const [repositories, setRepositories] = useState<Repository[]>([]);

  useEffect(() => {
    async function fetchRepositories() {
      try {
        const response = await fetch(
          `http://localhost:8000/api/getAllRepo?username=${userName}`,
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
        if (response.ok) {
          const formattedData = Object.keys(data).map((key) => ({
            ...data[key].details,
            branches: data[key].branches,
          }));
          setRepositories(formattedData);
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
    const handleClick = () => {
      navigate(`/u/${userName}/r/${repo.repo_name}`);
    };

    return (
      <Card key={repo.repo_id} withBorder shadow="lg" padding="lg" radius="md">
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
            Repository ID: {repo.repo_id}
          </Text>
          <Text size="lg" fw={500}>
            Description: {repo.description}
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
                Created at: {new Date(branch.created_timestamp).toLocaleString()}
              </Text>
              <Text size="sm" c="dimmed">
                Updated at: {new Date(branch.updated_timestamp).toLocaleString()}
              </Text>
              <Text size="sm" c="dimmed">
                Commit ID: {branch.commit_id}
              </Text>
            </Box>
          ))}
        </Box>
      </Card>
    );
  });

  return (
    <Stack p="xl">
      <Group justify="space-between">
        <Title order={2}>Your repositories</Title>
        <CreateRepository username={userName} />
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
