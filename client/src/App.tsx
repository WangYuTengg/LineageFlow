import { Stack, Group, Text, Anchor } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import CreateRepository from "./component/CreateRepository";
import Tabs from "./component/Tabs";

interface Repository {
  repositoryName: string;
  description?: string;
  storageNamespace?: string;
  defaultBranch: string;
}

export default function App() {
  const navigate = useNavigate();
  const [repositories, setRepositories] = useState<Repository[]>(() => {
    const localData = localStorage.getItem("repositories");
    return localData ? JSON.parse(localData) : [];
  });

  useEffect(() => {
    localStorage.setItem("repositories", JSON.stringify(repositories));
  }, [repositories]);

  return (
    <>
      <CreateRepository
        onCreateRepository={(repository) =>
          setRepositories((prev) => [...prev, repository])
        }
      />
      {repositories.length > 0 && (
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
      )}
    </>
  );
}
