import { Stack, Group, Text, Anchor } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import CreateRepository from "./component/CreateRepository";
import Tabs from "./component/Tabs";
import { Repository } from "./schema";

export default function App() {
  const navigate = useNavigate();
  const [repositories, setRepositories] = useState<Repository[]>([
    {
      repo_name: "test",
      description: "test description",
      bucket_url: "https://test-bucket.com",
      default_branch: "main",
      branches: ["main", "branch1", "branch2"],
    },
    {
      repo_name: "test 2",
      description: "test description 2",
      bucket_url: "https://test-bucket.com",
      default_branch: "main",
      branches: ["main", "branch1", "branch2"],
    },
  ]);
  const [selectedRepository, setSelectedRepository] = useState<Repository>({
    repo_name: "test",
    description: "test description",
    bucket_url: "https://test-bucket.com",
    default_branch: "main",
    branches: ["main", "branch1", "branch2"],
  });

  return (
    <>
      <CreateRepository
        onCreateRepository={(repository) =>
          setRepositories((prev) => [...prev, repository])
        }
      />
      {/* {repositories.length > 0 && (
        <Stack px="sm">
          <Group bg="gray" px="sm">
            <Anchor
              c="blue"
              size="lg"
              onClick={() => navigate("/repositories")}
            >
              Repositories
            </Anchor>
            /
            <Text c="dimmed" size="lg">
              {repositories[0].repositoryName}
            </Text>
          </Group>
          <Tabs />
        </Stack>
      )} */}
      <Stack px="sm">
        <Group bg="gray" p="md">
          <Anchor c="blue" size="lg" onClick={() => navigate("/repositories")}>
            Repositories
          </Anchor>
          /
          <Text c="dimmed" size="lg">
            {selectedRepository.repo_name}
          </Text>
        </Group>
        <Tabs selectedRepository={selectedRepository} />
      </Stack>
    </>
  );
}
