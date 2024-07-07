import { useState, useEffect } from "react";
import {
  Divider,
  Group,
  Stack,
  Text,
  Tabs,
  TextInput,
  Button,
  Select,
  Card,
} from "@mantine/core";
import { Branch, Repository } from "../schema";
import { useAuth } from "../auth";
import { IconUsersGroup, IconSettings } from "@tabler/icons-react";

interface Props {
  selectedRepository: Repository;
}

export default function SettingsPage({ selectedRepository }: Props) {
  const { userName } = useAuth();
  const [repositoryName, setRepositoryName] = useState(
    selectedRepository.repo_name
  );
  const [defaultBranch, setDefaultBranch] = useState(
    selectedRepository.default_branch
  );
  const [swapBranch, setSwapBranch] = useState<Branch>(
    selectedRepository.branches[0]
  );

  useEffect(() => {
    async function fetchUsersOfRepository() {
      try {
        console.log("fetch users");
      } catch (error) {
        console.error(error);
        alert("Error fetching commits of branch");
      }
    }

    fetchUsersOfRepository();
  }, []);

  return (
    <Stack px="8%" pt="xl">
      <Tabs defaultValue="settings" orientation="vertical">
        <Tabs.List>
          <Tabs.Tab value="settings" leftSection={<IconSettings />}>
            General
          </Tabs.Tab>

          <Tabs.Tab value="users" leftSection={<IconUsersGroup />}>
            Collaborators
          </Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="settings">
          <Stack pl="lg" gap="md">
            <Text size="xl" fw={600}>
              General
            </Text>
            <Divider />
            <Group align="flex-end" gap="lg">
              <TextInput
                size="md"
                label="Repository Name"
                description="Rename your repository name"
                style={{ width: 300 }}
                value={repositoryName}
                onChange={(event) => setRepositoryName(event.target.value)}
              />
              <Button
                size="md"
                variant="light"
                disabled={
                  repositoryName === selectedRepository.repo_name ||
                  !repositoryName.length
                }
              >
                Rename
              </Button>
            </Group>
            <Text c="dimmed">Note that repository name has to be unique</Text>
            <Divider />
            <Group align="flex-end" gap="lg">
              <TextInput
                size="md"
                label="Default Branch"
                description="Rename your default name"
                style={{ width: 300 }}
                value={defaultBranch}
                onChange={(event) => setDefaultBranch(event.target.value)}
              />
              <Button
                size="md"
                variant="light"
                disabled={
                  defaultBranch === selectedRepository.default_branch ||
                  !defaultBranch.length
                }
              >
                Rename
              </Button>
            </Group>
            <Text c="dimmed">
              The default branch is considered the “base” branch in your
              repository, against which all pull requests and data commits are
              automatically made, unless you specify a different branch.
            </Text>
            <Divider />
            <Group align="flex-end" gap="lg">
              <Select
                size="md"
                label="Swap Default Branch"
                data={selectedRepository.branches.map(
                  (branch) => branch.branch_name
                )}
                style={{ width: 300 }}
                value={swapBranch.branch_name}
                description="Swap the default branch with another branch"
                onChange={(branch_name) =>
                  setSwapBranch(
                    selectedRepository.branches.find(
                      (branch) => branch.branch_name === branch_name
                    )!
                  )
                }
              />
              <Button
                size="md"
                variant="light"
                disabled={
                  repositoryName === selectedRepository.repo_name ||
                  !repositoryName.length
                }
              >
                Swap
              </Button>
            </Group>
            <Divider />
            <Text size="xl" fw={600}>
              Delete Repository
            </Text>
            <Card>
              <Group gap="xl">
                <Text>
                  Once you delete a repository, there is no going back.
                  <br /> Please be certain.
                </Text>
                <Button size="md" variant="outline" color="red">
                  Delete
                </Button>
              </Group>
            </Card>
          </Stack>
        </Tabs.Panel>

        <Tabs.Panel value="users">
          <Stack pl="lg" gap="md">
            <Text size="xl" fw={600}>
              Collaborators
            </Text>
            <Divider />
            <Group px="xl">
              -
              <Text size="lg" fw={600}>
                {userName}
              </Text>{" "}
              (you)
            </Group>
          </Stack>
        </Tabs.Panel>
      </Tabs>
    </Stack>
  );
}
