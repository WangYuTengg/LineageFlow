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
} from "@mantine/core";
import { Branch } from "../schema";
import { IconSearch, IconPlus } from "@tabler/icons-react";

interface Props {
  branches: Branch[];
  defaultBranch: string;
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
export default function BranchesPage({ branches, defaultBranch }: Props) {
  console.log(branches);
  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Text size="xl" fw={700}>
          Branches
        </Text>
        <Button leftSection={<IconPlus />} variant="light" color="teal">
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
                  Id
                </Text>
                <Text size="md" fw={600}>
                  Updated
                </Text>
              </Group>
              <Divider my="lg" />
              <Group justify="space-between" px="lg">
                <Anchor size="lg">{defaultBranch.branch_name}</Anchor>
                <Code>{defaultBranch.branch_id}</Code>
                <Text>
                  Updated <b>{timeAgo(defaultBranch.updated_timestamp)}</b>
                </Text>
              </Group>
            </Card.Section>
          </Card>
        ))}
    </Stack>
  );
}
