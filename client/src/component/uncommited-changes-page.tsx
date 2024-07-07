import {
  Anchor,
  Card,
  Divider,
  Group,
  Stack,
  Text,
  TextInput,
  Button,
} from "@mantine/core";
import { FileResource, Repository, UncommittedChanges } from "../schema";
import { IconPlus, IconMinus, IconPencil } from "@tabler/icons-react";
import { useState } from "react";

interface Props {
  uncommittedChanges: UncommittedChanges | null;
  repository: Repository;
  onDone(): void;
}

export default function UncommittedChangesPage({
  uncommittedChanges,
  repository,
  onDone,
}: Props) {
  const [commitMessage, setCommitMessage] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const handleUpload = async () => {
    if (!uncommittedChanges) return;
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append("repo", uncommittedChanges.repo);
      formData.append("branch_name", uncommittedChanges.branch);
      formData.append("commit_message", commitMessage);
      uncommittedChanges.changes.forEach((change) => {
        const file = change.file as File;
        formData.append("files", file as File);
        formData.append("relative_paths", file.webkitRelativePath);
      });
      const response = await fetch("/api/upload/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("Files uploaded successfully");
        onDone();
      } else {
        console.error(response.statusText);
        alert("File upload failed");
      }
    } catch (error) {
      console.error(error);
      alert("File upload failed");
    }
    setIsLoading(false);
  };

  const handleDelete = async () => {
    if (!uncommittedChanges) return;
    setIsLoading(true);
    try {
      const data = {
        repo: uncommittedChanges.repo,
        branch: uncommittedChanges.branch,
        commit_message: commitMessage,
        files_list: uncommittedChanges.changes.map((change) => change.file),
      };
      console.log(data);
      const response = await fetch("/api/deleteFiles/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        alert("Files deleted successfully");
        onDone();
      } else {
        console.error(response.statusText);
        alert("File deletion failed");
      }
    } catch (error) {
      console.error(error);
      alert("File deletion failed");
    }
    setIsLoading(false);
  };

  return (
    <Stack px="8%">
      {uncommittedChanges ? (
        <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
          <Card.Section>
            <Group px="lg">
              <b>lineage-flow:// </b>
              <Anchor>{repository.repo_name}</Anchor>/{" "}
              <Anchor>{uncommittedChanges.branch}</Anchor>
            </Group>
          </Card.Section>
          <Divider my="lg" />
          {uncommittedChanges.changes.map((change, index) => (
            <Group
              key={index}
              bg={
                change.type === "Add"
                  ? "rgba(0, 255, 100, 0.1)"
                  : change.type === "Delete"
                    ? "rgba(255, 0, 0, 0.1)"
                    : "rgba(100, 255, 255, 0.1)"
              }
            >
              <Group px="xl" py="sm" align="center">
                {change.type === "Add" && <IconPlus />}
                {change.type === "Delete" && <IconMinus />}
                {change.type === "Modify" && <IconPencil />}
                {change.type === "Add" && (
                  <Text size="md" fw={400}>
                    {change.file.name}
                  </Text>
                )}
                {change.type === "Delete" && (
                  <Text size="md" fw={400}>
                    {change.file.meta_data.name}
                  </Text>
                )}
              </Group>
            </Group>
          ))}
          <Group mt="md">
            <TextInput
              style={{ width: "350px" }}
              value={commitMessage}
              onChange={(event) => setCommitMessage(event.target.value)}
              placeholder="Enter commit message"
            />
            <Button
              color="blue"
              onClick={() => {
                if (
                  uncommittedChanges.changes.some(
                    (change) => change.type === "Add"
                  )
                ) {
                  handleUpload();
                } else if (
                  uncommittedChanges.changes.some(
                    (change) => change.type === "Delete"
                  )
                ) {
                  handleDelete();
                }
              }}
              loading={isLoading}
            >
              Commit
            </Button>
          </Group>
        </Card>
      ) : (
        <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
          <Card.Section>
            <Group px="lg">
              <b>lineage-flow:// </b>
              <Anchor>{repository.repo_name}</Anchor> /{" "}
            </Group>
          </Card.Section>
          <Divider my="lg" />
          <Text ta="center" c="dimmed" size="lg">
            No uncommitted changes found
          </Text>
        </Card>
      )}
    </Stack>
  );
}
