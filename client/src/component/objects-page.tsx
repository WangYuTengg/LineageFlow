import {
  Group,
  Select,
  Button,
  Card,
  Anchor,
  Stack,
  Title,
  Divider,
  List,
  ActionIcon,
} from "@mantine/core";
import { IconRefresh, IconUpload } from "@tabler/icons-react";
import { useState } from "react";
import UploadObjectModal from "./upload-object-modal";
import { Repository } from "../schema";

interface Props {
  repository: Repository;
}

export default function ObjectsPage({ repository }: Props) {
  // Ensure defaultBranch is always a string
  const defaultBranch = repository.default_branch || (repository.branches.length > 0 ? repository.branches[0] : "");

  const [uploadObject, setUploadObject] = useState(false);
  const [selectedBranch, setSelectedBranch] = useState<string>(defaultBranch);

  // Transform branches array to the format required by the Select component
  const branchOptions = repository.branches.map((branch) => ({
    value: branch,
    label: branch,
  }));

  console.log(repository)

  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Select
          data={branchOptions}
          value={selectedBranch}
          onChange={(value) => setSelectedBranch(value!)}
          size="sm"
        />
        <Group>
          <ActionIcon
            size="lg"
            variant="subtle"
            onClick={() => console.log("refresh")}
          >
            <IconRefresh />
          </ActionIcon>
          <Button
            leftSection={<IconUpload />}
            size="sm"
            onClick={() => setUploadObject(true)}
          >
            Upload Object
          </Button>
        </Group>
      </Group>
      <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
        <Card.Section>
          <Group px="lg">
            <b>lineage-flow:// </b>
            <Anchor>{repository.repo_name}</Anchor> /{" "}
            <Anchor>{defaultBranch}</Anchor>{" "}
          </Group>
        </Card.Section>
        <Divider my="lg" />
        <Stack px="xl">
          <Title>To get started with this repository, you can: </Title>
          <List>
            <List.Item>
              <Anchor onClick={() => setUploadObject(true)}>Upload</Anchor> an
              object
            </List.Item>
          </List>
        </Stack>
      </Card>
      {uploadObject && (
        <UploadObjectModal
          repo={repository.repo_name}
          branch={selectedBranch}
          storage_bucket={repository.storage_bucket_url}
          opened={uploadObject}
          onClose={() => setUploadObject(false)}
        />
      )}
    </Stack>
  );
}
