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
import { Repository, UncommittedChanges } from "../schema";
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
    setIsLoading(true);
    if (!uncommittedChanges) return;
    try {
      const formData = new FormData();

      formData.append("repo", uncommittedChanges.repo);
      formData.append("branch", uncommittedChanges.branch);
      formData.append("storage_bucket", uncommittedChanges.storage_bucket);
      formData.append("commit_message", commitMessage);
      uncommittedChanges.changes.forEach((change) => {
        formData.append("files", change.file);
        formData.append("relative_paths", change.file.webkitRelativePath);
      });

      const response = await fetch("/api/upload/", {
        method: "POST",
        body: formData,
      });
      console.log(response);
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
              <Group px="xl">
                {change.type === "Add" && <IconPlus />}
                {change.type === "Delete" && <IconMinus />}
                {change.type === "Modify" && <IconPencil />}
                <Text size="md" fw={400}>
                  {change.file.name}
                </Text>
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
            <Button color="blue" onClick={handleUpload} loading={isLoading}>
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