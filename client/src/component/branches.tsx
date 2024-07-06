import { useState } from "react";
import {
  Anchor,
  Card,
  Divider,
  Group,
  Stack,
  Text,
  Autocomplete,
  Button,
  Code,
  ActionIcon,
} from "@mantine/core";
import { Repository } from "../schema";
import { IconSearch, IconPlus, IconTrash } from "@tabler/icons-react";
import CreateBranchModal from "./create-branch-modal";

interface Props {
  selectedRepository: Repository;
}

function timeAgo(dateString: string) {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  let interval = seconds / 31536000;

  if (interval > 1) {
    return Math.floor(interval) + " years ago";
  }
  interval = seconds / 2592000;
  if (interval > 1) {
    return Math.floor(interval) + " months ago";
  }
  interval = seconds / 86400;
  if (interval > 1) {
    return Math.floor(interval) + " days ago";
  }
  interval = seconds / 3600;
  if (interval > 1) {
    return Math.floor(interval) + " hours ago";
  }
  interval = seconds / 60;
  if (interval > 1) {
    return Math.floor(interval) + " minutes ago";
  }
  return Math.floor(seconds) + " seconds ago";
}
export default function BranchesPage({ selectedRepository }: Props) {
  const [createBranch, setCreateBranch] = useState(false);
  const branches = selectedRepository.branches;
  const defaultBranch = selectedRepository.default_branch;

  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Text size="xl" fw={700}>
          Branches
        </Text>
        <Button
          leftSection={<IconPlus />}
          variant="light"
          color="teal"
          onClick={() => setCreateBranch(true)}
        >
          New Branch
        </Button>
      </Group>
      <Autocomplete
        data={branches.map((branch) => branch.branch_name)}
        placeholder="Search branches"
        leftSection={
          <IconSearch style={{ marginLeft: "10px", marginRight: "10px" }} />
        }
      />
      <Text fw={600}>Default</Text>
      {branches
        .filter((branch) => branch.branch_name === defaultBranch)
        .map((defaultBranch) => (
          <Card shadow="lg" radius="sm" withBorder p="xl">
            <Card.Section>
              <Group
                justify="space-between"
                px="lg"
                style={{ marginBottom: "1em", marginTop: "0.5em" }}
              >
                <Text size="md" fw={600}>
                  Branch
                </Text>
                <Text size="md" fw={600}>
                  Created
                </Text>
                <Text size="md" fw={600}>
                  Updated
                </Text>
                <Text size="md" fw={600}>
                  Actions
                </Text>
              </Group>
              <Divider my="lg" />
              <Group justify="space-between" px="lg">
                <Group>
                  <Anchor size="lg">{defaultBranch.branch_name}</Anchor>
                  <Code>{defaultBranch.branch_id}</Code>
                </Group>
                <Text>
                  Created <b>{timeAgo(defaultBranch.created_timestamp)}</b>
                </Text>
                <Text>
                  Updated <b>{timeAgo(defaultBranch.updated_timestamp)}</b>
                </Text>
                <ActionIcon variant="subtle" c="red">
                  <IconTrash />
                </ActionIcon>
              </Group>
            </Card.Section>
          </Card>
        ))}
      <Text fw={600}>Other Branches</Text>
      {branches
        .filter((branch) => branch.branch_name !== defaultBranch)
        .map((defaultBranch) => (
          <Card shadow="lg" radius="sm" withBorder p="xl">
            <Card.Section>
              <Group
                justify="space-between"
                px="lg"
                style={{ marginBottom: "1em", marginTop: "0.5em" }}
              >
                <Text size="md" fw={600}>
                  Branch
                </Text>
                <Text size="md" fw={600}>
                  Created
                </Text>
                <Text size="md" fw={600}>
                  Updated
                </Text>
                <Text size="md" fw={600}>
                  Actions
                </Text>
              </Group>
              <Divider my="lg" />
              <Group justify="space-between" px="lg">
                <Group>
                  <Anchor size="lg">{defaultBranch.branch_name}</Anchor>
                  <Code>{defaultBranch.branch_id}</Code>
                </Group>
                <Text>
                  Created <b>{timeAgo(defaultBranch.created_timestamp)}</b>
                </Text>
                <Text>
                  Updated <b>{timeAgo(defaultBranch.updated_timestamp)}</b>
                </Text>
                <ActionIcon variant="subtle" c="red">
                  <IconTrash />
                </ActionIcon>
              </Group>
            </Card.Section>
          </Card>
        ))}
      {createBranch && (
        <CreateBranchModal
          opened={createBranch}
          onClose={() => setCreateBranch(false)}
          selectedRepository={selectedRepository}
        />
      )}
    </Stack>
  );
}
