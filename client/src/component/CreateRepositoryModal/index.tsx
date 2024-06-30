import { Modal, TextInput, Button, Group, Stack, Text } from "@mantine/core";
import { useForm, zodResolver } from "@mantine/form";
import { createRepositorySchema } from "./schema";

interface Props {
  opened: boolean;
  onClose(): void;
}

export default function CreateRepositoryModal({ opened, onClose }: Props) {
  const form = useForm({
    initialValues: {
      repositoryName: "",
      description: "",
      storageNamespace: "",
      defaultBranch: "main",
    },
    validate: zodResolver(createRepositorySchema),
  });

  return (
    <Modal
      size="xl"
      centered
      opened={opened}
      onClose={onClose}
      title={<Text size="lg">Create a Repository</Text>}
    >
      <form onSubmit={form.onSubmit((values) => console.log(values))}>
        <Stack gap="md">
          <TextInput
            size="md"
            label="Repository Name"
            withAsterisk
            placeholder="Enter repository name"
            {...form.getInputProps("repositoryName")}
          />
          <TextInput
            size="md"
            label="Description"
            placeholder="Enter description"
            {...form.getInputProps("description")}
          />
          <TextInput
            size="md"
            label="Storage Namespace"
            withAsterisk
            placeholder="local://example-bucket/"
            {...form.getInputProps("storageNamespace")}
          />
          <TextInput
            size="md"
            label="Default Branch"
            withAsterisk
            {...form.getInputProps("defaultBranch")}
          />
          <Group>
            <Button color="teal" variant="light" size="md" type="submit">
              Create Repository
            </Button>
            <Button variant="light" onClick={onClose} color="red" size="md">
              Cancel
            </Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
}
