import { Group, Text, Autocomplete, Button } from "@mantine/core";
import { IconSearch, IconPlus } from "@tabler/icons-react";
export default function Repository() {
  const repositories = ["repo 1", "repo 2"];

  return (
    <Group justify="space-between" px="md">
      <Autocomplete
        label="Search your repositories"
        data={repositories}
        placeholder="Start typing..."
        size="md"
        leftSection={<IconSearch />}
      />

      <Button size="md" leftSection={<IconPlus />} variant="light" color="teal">
        Create a Repository
      </Button>
    </Group>
  );
}
