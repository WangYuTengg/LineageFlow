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
import { Commit, Repository } from "../schema";
import { useAuth } from "../auth";
import {
  IconGitCommit,
  IconGitPullRequest,
  IconPlus,
} from "@tabler/icons-react";
import { timeAgo } from "./branches-page";

interface Props {
  selectedRepository: Repository;
}

export default function CommitsPage({ selectedRepository }: Props) {
  const branches = selectedRepository.branches;
  const { userName } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedBranch, setSelectedBranch] = useState<string | null>(
    selectedRepository.default_branch
  );
  const [commits, setCommits] = useState<Commit[]>([]);

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
        if (response.ok) {
          setCommits(data);
        } else {
          console.error(data);
          alert("Error fetching commits of branch");
        }
      } catch (error) {
        console.error(error);
        alert("Error fetching commits of branch");
      }
      setIsLoading(false);
    }

    fetchCommitsOfBranch();
  }, [branches, selectedBranch]);

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
      <Card shadow="lg" radius="sm" withBorder p="xl">
        <Timeline active={1} bulletSize={24} lineWidth={2}>
          {commits.map((commit) => (
            <Timeline.Item
              title={commit.commit_message}
              bullet={<IconGitCommit size={12} />}
              key={commit.commit_id}
            >
              <Text c="dimmed" size="sm">
                <b>{userName}</b> committed changes
              </Text>
              <Text size="xs" mt={4}>
                {timeAgo(commit.created_timestamp)}
              </Text>
            </Timeline.Item>
          ))}

          <Timeline.Item
            title="Created Default Branch"
            bullet={<IconGitPullRequest size={12} />}
          >
            <Text c="dimmed" size="sm">
              <b>{userName}</b> created default branch:{" "}
              <b>"{selectedRepository.default_branch}"</b>{" "}
            </Text>
            <Text size="xs" mt={4}>
              {timeAgo(
                selectedRepository.branches.filter(
                  (branch) =>
                    branch.branch_name === selectedRepository.default_branch
                )[0].created_timestamp
              )}
            </Text>
          </Timeline.Item>

          <Timeline.Item
            title="Created Repository"
            bullet={<IconPlus size={12} />}
          >
            <Text c="dimmed" size="sm">
              <b>{userName}</b> created <b>"{selectedRepository.repo_name}"</b>{" "}
              repository
            </Text>
            <Text size="xs" mt={4}>
              {timeAgo(selectedRepository.created_timestamp)}
            </Text>
          </Timeline.Item>
        </Timeline>
      </Card>
    </Stack>
  );
}
