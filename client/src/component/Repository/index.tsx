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
import UploadObjectModal from "./UploadObjectModal";
import { Repository } from "../../schema";

interface Props {
  repository: Repository;
}
export default function RepositoryPage({ repository }: Props) {
  const [uploadObject, setUploadObject] = useState(false);
  const [selectedBranch, setSelectedBranch] = useState<string | null>(
    repository.default_branch
  );

  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Select
          data={repository.branches}
          value={selectedBranch}
          onChange={(value) => setSelectedBranch(value)}
          size="sm"
        />
        <Group>
          {" "}
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
            <Anchor>{repository.default_branch}</Anchor>{" "}
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
          repo="test-repo"
          branch="main"
          opened={uploadObject}
          onClose={() => setUploadObject(false)}
        />
      )}
    </Stack>
  );
}
