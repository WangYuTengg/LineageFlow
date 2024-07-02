import { Modal, TextInput, Button, Group, Stack, Text } from "@mantine/core";
import { useForm, zodResolver } from "@mantine/form";
import { createRepositorySchema, CreateRepositorySchemaValues } from "./schema";

interface Props {
  opened: boolean;
  onClose(): void;
  onCreateRepository(values: CreateRepositorySchemaValues): void;
}

export default function CreateRepositoryModal({
  opened,
  onClose,
  onCreateRepository,
}: Props) {
  const form = useForm({
    initialValues: {
      repo_name: "",
      description: "",
      gc_bucket: "",
      default_branch: "main",
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
      <form onSubmit={form.onSubmit((values) => onCreateRepository(values))}>
        <Stack gap="md">
          <TextInput
            size="md"
            label="Repository Name"
            withAsterisk
            placeholder="Enter repository name"
            {...form.getInputProps("repo_name")}
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
            placeholder="local://example-bucket/"
            {...form.getInputProps("gc_bucket")}
          />
          <TextInput
            size="md"
            label="Default Branch"
            withAsterisk
            {...form.getInputProps("default_branch")}
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
