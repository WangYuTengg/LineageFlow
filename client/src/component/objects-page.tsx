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
  Loader,
} from "@mantine/core";
import { IconRefresh, IconUpload } from "@tabler/icons-react";
import { useEffect, useState } from "react";
import { FileResource, FolderContents, Repository } from "../schema";
import UploadObjectModal from "./upload-object-modal";
import RenderFileStructure from "./render-file-structure";
interface Props {
  repository: Repository;
}

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
export default function ObjectsPage({ repository }: Props) {
  const [state, setState] = useState({
    refresh: false,
    isLoading: false,
    uploadObject: false,
    selectedBranch: repository.default_branch,
    fileResources: [] as FileResource[],
  });
  const [filesToDelete, setFilesToDelete] = useState<FileResource[]>([]);

  function handleChangeState<K extends keyof typeof state>(
    key: K,
    value: (typeof state)[K]
  ) {
    return setState((prev) => ({ ...prev, [key]: value }));
  }

  useEffect(() => {
    async function fetchFiles() {
      try {
        handleChangeState("isLoading", true);
        const response = await fetch(
          // getCommitData
          `/api/getObjects/?id=${repository.repo_id}&branch=${state.selectedBranch}`,
          {
            headers: {
              "Content-Type": "application/json",
            },
            method: "GET",
          }
        );
        const data: { files: FileResource[] } = await response.json();
        const files = data.files.flat(1).map((file) => ({
          ...file,
          meta_data: JSON.parse(file.meta_data as unknown as string),
        }));
        if (response.ok) {
          handleChangeState("fileResources", files);
        } else {
          alert("Internal server error");
        }
        handleChangeState("isLoading", false);
      } catch (error) {
        console.error(error);
        alert("Error fetching objects!");
      }
    }

    fetchFiles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.refresh]);

  async function handleDeleteFiles() {
    // Delete files logic
  }
  const RenderCard = () => {
    if (state.fileResources.length === 0) {
      return (
        <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
          <Card.Section>
            <Group px="lg">
              <b>lineage-flow:// </b>
              <Anchor>{repository.repo_name}</Anchor> /{" "}
              <Anchor>{state.selectedBranch}</Anchor>{" "}
            </Group>
          </Card.Section>
          <Divider my="lg" />
          <Stack px="xl">
            <Title>To get started with this repository, you can: </Title>
            <List>
              <List.Item>
                <Anchor onClick={() => handleChangeState("uploadObject", true)}>
                  Upload{" "}
                </Anchor>
                an object
              </List.Item>
            </List>
          </Stack>
        </Card>
      );
    } else {
      const organizedFiles = organizeFiles(state.fileResources);
      return (
        <Card shadow="lg" radius="sm" withBorder mt="md" p="xl">
          <Card.Section>
            <Group px="lg">
              <b>lineage-flow://</b> <Anchor>{repository.repo_name}</Anchor> /{" "}
              <Anchor>{state.selectedBranch}</Anchor>
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
  };

  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Select
          data={repository.branches.map((branch) => branch.branch_name)}
          value={state.selectedBranch}
          onChange={(value) =>
            handleChangeState("selectedBranch", value as string)
          }
          size="sm"
        />
        <Group>
          <ActionIcon
            size="lg"
            variant="subtle"
            onClick={() => handleChangeState("refresh", !state.refresh)}
          >
            <IconRefresh />
          </ActionIcon>
          <Button
            leftSection={<IconUpload />}
            size="sm"
            onClick={() => handleChangeState("uploadObject", true)}
          >
            Upload Object
          </Button>
        </Group>
      </Group>
      {state.isLoading ? (
        <Card shadow="xs" radius="sm" withBorder mt="md" p="xl">
          <Stack justify="center" align="center">
            <Loader />
          </Stack>
        </Card>
      ) : (
        <RenderCard />
      )}
      {state.uploadObject && (
        <UploadObjectModal
          repo={repository.repo_name}
          branch={state.selectedBranch as string}
          storage_bucket={repository.bucket_url}
          opened={state.uploadObject}
          onClose={() => handleChangeState("uploadObject", false)}
        />
      )}
      {filesToDelete.length > 0 && (
        <Group justify="flex-end" onClick={handleDeleteFiles}>
          <Button color="red">
            Confirm Delete {filesToDelete.length} file
            {filesToDelete.length > 1 && "s"}
          </Button>{" "}
        </Group>
      )}
    </Stack>
  );
}
