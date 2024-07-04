import { useState } from "react";
import { Group, Button } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import CreateRepositoryModal from "./create-repo-modal";
import { CreateRepositorySchemaValues } from "../schema";

export default function CreateRepository() {
  const [createRepository, setCreateRepository] = useState(false);

  async function handleCreateRepository(values: CreateRepositorySchemaValues) {
    try {
      const response = await fetch("/api/onboard/", {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(values),
      });
      console.log(response);
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        alert(data.message);
        setCreateRepository(false);
      } else {
        alert("Failed to create repository!");
      }
    } catch (error) {
      console.error(error);
      alert("Failed to create repository!");
    }
  }

  return (
    <>
      <Group justify="flex-end" px="md">
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
          onCreateRepository={(values) => handleCreateRepository(values)}
        />
      )}
    </>
  );
}
