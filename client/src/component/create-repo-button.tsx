import { useState } from "react";
import { Group, Button } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import CreateRepositoryModal from "./create-repo-modal";
import { CreateRepositorySchemaValues } from "../schema";

interface Props {
  username: string;
  onCreate(): void;
}

const CreateRepository = ({ username, onCreate }: Props) => {
  const [isLoading, setIsLoading] = useState(false);
  const [createRepository, setCreateRepository] = useState(false);

  async function handleCreateRepository(values: CreateRepositorySchemaValues) {
    setIsLoading(true);
    try {
      const payload = {
        username,
        ...values,
      };
      const response = await fetch("/api/onboard/", {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (response.ok) {
        alert("Successfuly created repository!");
        setCreateRepository(false);
        onCreate();
      } else {
        alert("Failed to create repository!");
      }
    } catch (error) {
      console.error(error);
      alert("Failed to create repository!");
    }
    setIsLoading(false);
  }

  return (
    <>
      <Group justify="flex-end" px="md">
        <Button
          size="md"
          leftSection={<IconPlus />}
          variant="light"
          color="teal"
          loading={isLoading}
          onClick={() => setCreateRepository(true)}
        >
          Add Repository
        </Button>
      </Group>
      {createRepository && (
        <CreateRepositoryModal
          loading={isLoading}
          opened={createRepository}
          onClose={() => setCreateRepository(false)}
          onCreateRepository={(values) => handleCreateRepository(values)}
        />
      )}
    </>
  );
};

export default CreateRepository;
