import { useState } from "react";
import { Group, Button } from "@mantine/core";
import { IconPlus } from "@tabler/icons-react";
import CreateRepositoryModal from "./create-repo-modal";
import { CreateRepositorySchemaValues } from "../schema";

interface CreateRepositoryProps {
  username: string;
}

const CreateRepository: React.FC<CreateRepositoryProps> = ({ username }) => {
  const [createRepository, setCreateRepository] = useState(false);

  async function handleCreateRepository(values: CreateRepositorySchemaValues) {
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
      console.log(response);
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        alert("Successfuly created repository!");
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
          Add Repository
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

export default CreateRepository;
