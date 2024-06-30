import { useState } from "react";
import { Group, Autocomplete, Button } from "@mantine/core";
import { IconSearch, IconPlus } from "@tabler/icons-react";
import CreateRepositoryModal from "../CreateRepositoryModal";

export default function Repository() {
  const [createRepository, setCreateRepository] = useState(false);
  const repositories = ["repo 1", "repo 2"];

  return (
    <>
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
          onClick={() => setCreateRepository(true)}
        >
          Create a Repository
        </Button>
      </Group>
      {createRepository && (
        <CreateRepositoryModal
          opened={createRepository}
          onClose={() => setCreateRepository(false)}
        />
      )}
    </>
  );
}
