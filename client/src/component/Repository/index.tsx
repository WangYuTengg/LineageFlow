import { Group, Autocomplete, Button } from "@mantine/core";
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

      <Button
        size="md"
        leftSection={<IconPlus />}
        variant="light"
        color="teal"
        onClick={async () => {
          const response = await fetch("http://localhost:5173/api/hello/", {
            method: "GET",
          });
          const result = await response.text();
          console.log(result);
        }}
      >
        Create a Repository
      </Button>
    </Group>
  );
}
