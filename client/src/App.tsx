import { Stack, Group, Text, Anchor } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import CreateRepository from "./component/CreateRepository";
import { Repository } from "./schema";
import TableRepositories from "./component/TableRepositories";

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

  return (
    <>
      <CreateRepository
        onCreateRepository={(repository) =>
          setRepositories((prev) => [...prev, repository])
        }
      />
      <Stack px="sm">
        <Group bg="gray" p="md">
          <Anchor c="blue" size="lg" onClick={() => navigate("/repositories")}>
            Repositories
          </Anchor>
        </Group>
        <TableRepositories data={repositories} />
      </Stack>
    </>
  );
}
