import { useState, useEffect } from "react";
import {
  Card,
  Divider,
  Group,
  Stack,
  Text,
  Popover,
  Select,
  Timeline,
  ActionIcon,
  Button,
  Code,
} from "@mantine/core";
import { Commit, FileResource, Repository } from "../schema";
import { useAuth } from "../auth";
import {
  IconArrowBackUp,
  IconGitCommit,
  IconGitPullRequest,
  IconPlus,
  IconRefresh,
} from "@tabler/icons-react";
import { timeAgo } from "./branches-page";
import FilesList from "./commits-file-list";
interface Props {
  selectedRepository: Repository;
}

export default function CommitsPage({ selectedRepository }: Props) {
  const branches = selectedRepository.branches;
  const { userName } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [refresh, setRefresh] = useState(false);
  const [selectedBranch, setSelectedBranch] = useState<string | null>(
    selectedRepository.default_branch
  );
  const [state, setState] = useState<{
    commits: Commit[];
    adds: { file: FileResource; commit_id: string }[];
    edits: { file: FileResource; commit_id: string }[];
    deletes: { file: FileResource; commit_id: string }[];
  }>({
    commits: [],
    adds: [],
    edits: [],
    deletes: [],
  });

  const currentCommit = state.commits.sort(
    (a, b) =>
      new Date(b.created_timestamp).getTime() -
      new Date(a.created_timestamp).getTime()
  )[0];

  function handleSetState<K extends keyof typeof state>(
    key: K,
    value: (typeof state)[K]
  ) {
    setState((prev) => ({ ...prev, [key]: value }));
  }

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
          handleSetState("commits", data.commits);
          handleSetState("adds", data.adds);
          handleSetState("edits", data.edits);
          handleSetState("deletes", data.deletes);
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
  }, [branches, selectedBranch, refresh]);

  async function handleRevert(commit: Commit) {
    try {
      const response = await fetch(`/api/revertCommit/`, {
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          commit: currentCommit.commit_id,
          target_commit: commit.commit_id,
        }),
        method: "POST",
      });
      const data = await response.json();
      if (response.ok) {
        alert("Reverted commit successfully");
        setRefresh((r) => !r);
      } else {
        console.error(data);
        alert("Error reverting commit");
      }
    } catch (error) {
      console.error(error);
      alert("Error reverting commit");
    }
  }

  return (
    <Stack px="8%">
      <Text size="xl" fw={700} mt="md">
        Commits
      </Text>
      <Divider />
      <Group justify="space-between" align="flex-end">
        <Select
          data={branches.map((branch) => branch.branch_name)}
          label="Select Branch"
          value={selectedBranch}
          onChange={(value) => setSelectedBranch(value)}
        />
        <ActionIcon
          size="lg"
          variant="subtle"
          onClick={() => setRefresh((r) => !r)}
        >
          <IconRefresh />
        </ActionIcon>
      </Group>
      <Card shadow="lg" radius="sm" withBorder p="xl">
        {!isLoading && (
          <Timeline active={1} bulletSize={24} lineWidth={2}>
            {state.commits.map((commit) => (
              <Timeline.Item
                title={
                  <Group align="center" gap="md">
                    <Text> {commit.commit_message}</Text>
                    <Code>{commit.commit_id}</Code>
                  </Group>
                }
                bullet={<IconGitCommit size={12} />}
                key={commit.commit_id}
              >
                <Text c="dimmed" size="sm">
                  <b>{userName}</b> committed changes
                </Text>
                <Text size="xs" mt={4}>
                  {timeAgo(commit.created_timestamp)}
                </Text>
                {state.adds.some(
                  (add) => add.commit_id === commit.commit_id
                ) && (
                  <FilesList
                    typeString="Added"
                    files={state.adds}
                    commit={commit}
                  />
                )}
                {state.deletes.some(
                  (remove) => remove.commit_id === commit.commit_id
                ) && (
                  <FilesList
                    typeString="Deleted"
                    files={state.deletes}
                    commit={commit}
                  />
                )}
                {state.edits.some(
                  (edit) => edit.commit_id === commit.commit_id
                ) && (
                  <FilesList
                    typeString="Modified"
                    files={state.deletes}
                    commit={commit}
                  />
                )}
                {commit.commit_id !== currentCommit.commit_id && (
                  <Group mt="md">
                    <Popover
                      width={200}
                      position="bottom"
                      withArrow
                      shadow="md"
                    >
                      <Popover.Target>
                        <Button
                          variant="subtle"
                          size="sm"
                          c="dimmed"
                          leftSection={<IconArrowBackUp />}
                        >
                          Revert to this commit
                        </Button>
                      </Popover.Target>
                      <Popover.Dropdown>
                        <Text size="md" mb="md" fw={600}>
                          Are you sure?
                        </Text>
                        <Button
                          variant="outline"
                          size="sm"
                          color="red"
                          fullWidth
                          onClick={() => handleRevert(commit)}
                        >
                          Revert
                        </Button>
                      </Popover.Dropdown>
                    </Popover>
                  </Group>
                )}
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
                <b>{userName}</b> created{" "}
                <b>"{selectedRepository.repo_name}"</b> repository
              </Text>
              <Text size="xs" mt={4}>
                {timeAgo(selectedRepository.created_timestamp)}
              </Text>
            </Timeline.Item>
          </Timeline>
        )}
      </Card>
    </Stack>
  );
}
