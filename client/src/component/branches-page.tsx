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
  SimpleGrid,
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
        .map((branch, index) => (
          <Card shadow="lg" radius="sm" withBorder p="xl" key={index}>
            <Card.Section>
              <SimpleGrid cols={4} spacing="xl" px="md">
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
              </SimpleGrid>
              <Divider my="lg" />
              <SimpleGrid cols={4} spacing="xl" px="md">
                <Group>
                  <Anchor size="lg">{branch.branch_name}</Anchor>
                  <Code>{branch.branch_id}</Code>
                </Group>

                <Text>
                  Created <b>{timeAgo(branch.created_timestamp)}</b>
                </Text>
                <Text>
                  Updated <b>{timeAgo(branch.updated_timestamp)}</b>
                </Text>
                <ActionIcon variant="subtle" color="red">
                  <IconTrash />
                </ActionIcon>
              </SimpleGrid>
            </Card.Section>
          </Card>
        ))}
      <Text fw={600}>Other Branches</Text>
      {branches
        .filter((branch) => branch.branch_name !== defaultBranch)
        .map((branch, index) => (
          <Card shadow="lg" radius="sm" withBorder p="xl" key={index}>
            <Card.Section>
              <SimpleGrid cols={4} spacing="xl" px="md">
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
              </SimpleGrid>
              <Divider my="lg" />
              <SimpleGrid cols={4} spacing="xl" px="md">
                <Group wrap="nowrap">
                  <Anchor size="lg">{branch.branch_name}</Anchor>
                  <Code>
                    <Text lineClamp={1}>{branch.branch_id} </Text>
                  </Code>
                </Group>

                <Text>
                  Created <b>{timeAgo(branch.created_timestamp)}</b>
                </Text>
                <Text>
                  Updated <b>{timeAgo(branch.updated_timestamp)}</b>
                </Text>
                <ActionIcon variant="subtle" color="red">
                  <IconTrash />
                </ActionIcon>
              </SimpleGrid>
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
