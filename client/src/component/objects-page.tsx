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
  Text,
  Collapse,
} from "@mantine/core";
import {
  IconRefresh,
  IconUpload,
  IconFolder,
  IconChevronDown,
} from "@tabler/icons-react";
import { useEffect, useState } from "react";
import { FileResource, Repository } from "../schema";
import UploadObjectModal from "./upload-object-modal";
interface Props {
  repository: Repository;
}
interface FolderContents {
  files: FileResource[];
  folders: { [key: string]: FolderContents };
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
    isLoading: false,
    uploadObject: false,
    selectedBranch: repository.default_branch,
    fileResources: [] as FileResource[],
  });

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
          `/api/getObjects?id=${repository.repo_id}&branch=${state.selectedBranch}`,
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
  }, []);

  const branchOptions = repository.branches.map((branch) => branch.branch_name);

  const RenderFileStructure = ({
    folderContents,
  }: {
    folderContents: FolderContents;
  }) => {
    const [opened, setOpened] = useState({});

    const handleToggle = (folderName: string) => {
      setOpened((prev) => ({
        ...prev,
        [folderName]: !prev[folderName as keyof typeof opened],
      }));
    };

    return (
      <Stack>
        {Object.keys(folderContents.folders).map((folderName) => (
          <div key={folderName}>
            <Group
              gap="xs"
              mb="xs"
              style={{ cursor: "pointer" }}
              onClick={() => handleToggle(folderName)}
              justify="space-between"
            >
              <Group>
                <IconFolder size={20} />
                <Text size="xl" fw="500">
                  {folderName}
                </Text>
              </Group>
              <IconChevronDown size={16} />
            </Group>
            <Collapse in={opened[folderName as keyof typeof opened] || false}>
              <Stack pl="xl">
                <RenderFileStructure
                  folderContents={folderContents.folders[folderName]}
                />
              </Stack>
            </Collapse>
          </div>
        ))}
        <List>
          {folderContents.files.map((file: FileResource) => (
            <List.Item key={file.meta_data.name} mb="xs">
              -{" "}
              <Anchor
                href={file.url}
                key={file.meta_data.name}
                target="_blank"
                size="sm"
                rel="noopener noreferrer"
              >
                {file.meta_data.name.split("/").pop()}
              </Anchor>
            </List.Item>
          ))}
        </List>
      </Stack>
    );
  };

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
            <RenderFileStructure folderContents={organizedFiles} />
          </Stack>
        </Card>
      );
    }
  };

  return (
    <Stack px="8%">
      <Group justify="space-between" mt="md">
        <Select
          data={branchOptions}
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
            onClick={() => console.log("refresh")}
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
    </Stack>
  );
}
