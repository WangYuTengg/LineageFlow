import {
  Anchor,
  Card,
  Divider,
  Group,
  List,
  Stack,
  Title,
} from "@mantine/core";
import { Dispatch, SetStateAction } from "react";
import { FileResource, FolderContents, Repository } from "../schema";
import RenderFileStructure from "./render-file-structure";

function organizeFiles(fileResources: FileResource[]): FolderContents {
  const root: FolderContents = { files: [], folders: {} };

  fileResources.forEach((file) => {
    const parts = file.meta_data.name.split("/");
    let currentFolder = root;

    parts.forEach((part, index) => {
      if (index === parts.length - 1) {
        currentFolder.files.push(file);
      } else {
        if (!currentFolder.folders[part]) {
          currentFolder.folders[part] = { files: [], folders: {} };
        }
        currentFolder = currentFolder.folders[part];
      }
    });
  });

  return root;
}

interface Props {
  fileResources: FileResource[];
  repository: Repository;
  selectedBranch: string;
  onUploadObject: (f: boolean) => void;
  filesToDelete: FileResource[];
  setFilesToDelete: Dispatch<SetStateAction<FileResource[]>>;
}
export default function RepositoryCard({
  fileResources,
  repository,
  selectedBranch,
  onUploadObject,
  filesToDelete,
  setFilesToDelete,
}: Props) {
  console.log(fileResources);
  console.log(repository);
  if (fileResources.length === 0) {
    return (
      <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
        <Card.Section>
          <Group px="lg">
            <b>lineage-flow:// </b>
            <Anchor>{repository.repo_name}</Anchor> /{" "}
            <Anchor>{selectedBranch}</Anchor>{" "}
          </Group>
        </Card.Section>
        <Divider my="lg" />
        <Stack px="xl">
          <Title>To get started with this repository, you can: </Title>
          <List>
            <List.Item>
              <Anchor onClick={() => onUploadObject(true)}>Upload </Anchor>
              an object
            </List.Item>
          </List>
        </Stack>
      </Card>
    );
  } else {
    const organizedFiles = organizeFiles(fileResources);
    return (
      <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
        <Card.Section>
          <Group px="lg">
            <b>lineage-flow://</b> <Anchor>{repository.repo_name}</Anchor> /{" "}
            <Anchor>{selectedBranch}</Anchor>
          </Group>
        </Card.Section>
        <Divider my="lg" />
        <Stack px="xl">
          <RenderFileStructure
            folderContents={organizedFiles}
            filesToDelete={filesToDelete}
            setFilesToDelete={setFilesToDelete}
          />
        </Stack>
      </Card>
    );
  }
}
