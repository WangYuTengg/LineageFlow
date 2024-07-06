import { Modal, TextInput, Button, Group, Stack, Text } from "@mantine/core";
import { useForm, zodResolver } from "@mantine/form";
import { createBranchSchema } from "../schema";
import { useState } from "react";

interface Props {
  opened: boolean;
  onClose(): void;
}

export default function CreateBranchModal({ opened, onClose }: Props) {
  const [loading, setLoading] = useState(false);
  const form = useForm({
    initialValues: {
      branchName: "",
    },
    validate: zodResolver(createBranchSchema),
  });

  return (
    <Modal
      size="xl"
      centered
      opened={opened}
      onClose={onClose}
      radius="lg"
      title={<Text size="lg">Create a branch</Text>}
    >
      <form onSubmit={form.onSubmit((values) => console.log(values))}>
        <Stack gap="md">
          <TextInput
            size="md"
            label="New branch name"
            withAsterisk
            {...form.getInputProps("branchName")}
          />
          <Group justify="flex-end">
            <Button
              variant="light"
              onClick={onClose}
              color="red"
              size="md"
              loading={loading}
            >
              Cancel
            </Button>
            <Button
              color="teal"
              variant="light"
              size="md"
              type="submit"
              disabled={!form.isDirty()}
              loading={loading}
            >
              Create Repository
            </Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
}
