import { useState, useEffect } from "react";
import {
  Card,
  Divider,
  Group,
  Stack,
  Text,
  Select,
  Timeline,
} from "@mantine/core";
import { Repository } from "../schema";

interface Props {
  selectedRepository: Repository;
}

export default function CommitsPage({ selectedRepository }: Props) {
  const [isLoading, setIsLoading] = useState(false);
  const [selectedBranch, setSelectedBranch] = useState<string | null>(
    selectedRepository.default_branch
  );
  const branches = selectedRepository.branches;

  useEffect(() => {
    async function fetchCommitsOfBranch() {
      setIsLoading(true);
      try {
        const id = branches.find(
          (branch) => branch.branch_name === selectedBranch
        )?.branch_id;
        if (!id) return;

        const response = await fetch(
          `/api/getCommitsOfBranch?branch_id=${id}`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            method: "GET",
          }
        );
        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error(error);
        alert("Error fetching commits of branch");
      }
      setIsLoading(false);
    }

    fetchCommitsOfBranch();
  }, []);

  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Text size="xl" fw={700}>
          Commits
        </Text>
      </Group>
      <Divider />
      <Group>
        <Select
          data={branches.map((branch) => branch.branch_name)}
          label="Select Branch"
          value={selectedBranch}
          onChange={(value) => setSelectedBranch(value)}
        />
      </Group>
      <Card shadow="lg" radius="sm" withBorder p="xl"></Card>
    </Stack>
  );
}
