import {
  Modal,
  TextInput,
  Button,
  Group,
  Stack,
  Text,
  Select,
} from "@mantine/core";
import { useForm, zodResolver } from "@mantine/form";
import { createBranchSchema, Repository } from "../schema";
import { useAuth } from "../auth";
import { useState } from "react";

interface Props {
  opened: boolean;
  onClose(): void;
  selectedRepository: Repository;
}

export default function CreateBranchModal({
  opened,
  onClose,
  selectedRepository,
}: Props) {
  const { userName } = useAuth();
  const [loading, setLoading] = useState(false);
  const form = useForm({
    initialValues: {
      branchName: "",
      parent: "",
    },
    validate: zodResolver(createBranchSchema),
  });

  async function handleCreateBranch(values: {
    branchName: string;
    parent: string;
  }) {
    setLoading(true);
    try {
      const response = await fetch("/api/createBranch/", {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify({
          username: userName,
          repo_name: selectedRepository.repo_name,
          parent: values.parent,
          branch_name: values.branchName,
        }),
      });
      if (response.ok) {
        alert("Successfuly created branch!");
        onClose();
      } else {
        alert("Failed to create branch!");
      }
    } catch (error) {
      console.error(error);
      alert("Failed to create branch!");
    }
    setLoading(false);
  }

  return (
    <Modal
      size="xl"
      centered
      opened={opened}
      onClose={onClose}
      radius="lg"
      title={<Text size="lg">Create a branch</Text>}
    >
      <form onSubmit={form.onSubmit((values) => handleCreateBranch(values))}>
        <Stack gap="md">
          <TextInput
            size="md"
            label="New branch name"
            withAsterisk
            {...form.getInputProps("branchName")}
          />
          <Select
            label="Source branch"
            placeholder="Select branch"
            data={selectedRepository.branches.map(
              (branch) => branch.branch_name
            )}
            {...form.getInputProps("parent")}
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
              Create Branch
            </Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
}
