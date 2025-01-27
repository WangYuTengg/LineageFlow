import {
  Group,
  Select,
  Button,
  Card,
  Anchor,
  Stack,
  Notification,
  ActionIcon,
  Loader,
  Text,
} from "@mantine/core";
import {
  IconRefresh,
  IconUpload,
  IconExclamationMark,
} from "@tabler/icons-react";
import { useEffect, useState } from "react";
import { FileResource, Repository, UncommittedChanges } from "../schema";
import UploadObjectModal from "./upload-object-modal";
import RepositoryCard from "./repository-card";

interface Props {
  repository: Repository;
  onUncommittedChanges: (data: UncommittedChanges) => void;
}

export default function ObjectsPage({
  repository,
  onUncommittedChanges,
}: Props) {
  const [state, setState] = useState({
    refresh: false,
    isLoading: false,
    uploadObject: false,
    selectedBranch: repository.default_branch,
    fileResources: [] as FileResource[],
  });
  const [filesToDelete, setFilesToDelete] = useState<FileResource[]>([]);
  const [showNotif, setShowNotif] = useState(true);
  const [uncommittedChanges, setUncommittedChanges] =
    useState<UncommittedChanges | null>(null);

  function handleChangeState<K extends keyof typeof state>(
    key: K,
    value: (typeof state)[K]
  ) {
    return setState((prev) => ({ ...prev, [key]: value }));
  }

  useEffect(() => {
    async function fetchFiles() {
      handleChangeState("isLoading", true);
      const response = await fetch(
        `/api/getObjects/?id=${repository.repo_id}&branch=${state.selectedBranch}`,
        {
          headers: {
            "Content-Type": "application/json",
          },
          method: "GET",
        }
      );
      const data: { files: FileResource[] } = await response.json();
      const files = data.files.flat(1).map((file) => {
        let metaData = file.meta_data;
        try {
          if (typeof metaData === "string") {
            metaData = JSON.parse(metaData);
          }
          if (typeof metaData === "string") {
            metaData = JSON.parse(metaData);
          }
        } catch (e) {
          metaData = {
            name: "Unknown",
            size: 0,
            content_type: "unknown",
            updated: "",
            generation: 0,
            metageneration: 0,
          };
        }
        return {
          ...file,
          meta_data: metaData,
        };
      });

      if (response.ok) {
        handleChangeState("fileResources", files);
      } else {
        alert("Internal server error");
      }
      handleChangeState("isLoading", false);
    }

    fetchFiles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.refresh]);

  return (
    <Stack px="8%">
      {showNotif && uncommittedChanges && (
        <Notification
          mt="lg"
          color="red"
          onClose={() => setShowNotif(false)}
          title="We notify you that:"
          icon={<IconExclamationMark />}
        >
          <Text c="red">
            You have uncommitted changes.{" "}
            <Anchor onClick={() => onUncommittedChanges(uncommittedChanges)}>
              Click here
            </Anchor>{" "}
            to commit them.
          </Text>
        </Notification>
      )}
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
            onClick={() => {
              handleChangeState("refresh", !state.refresh);
              setFilesToDelete([]);
              setUncommittedChanges(null);
              setShowNotif(false);
            }}
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
        <RepositoryCard
          fileResources={state.fileResources}
          repository={repository}
          selectedBranch={state.selectedBranch}
          onUploadObject={() => handleChangeState("uploadObject", true)}
          filesToDelete={filesToDelete}
          setFilesToDelete={setFilesToDelete}
        />
      )}
      {state.uploadObject && (
        <UploadObjectModal
          repo={repository.repo_name}
          branch={state.selectedBranch as string}
          storage_bucket={repository.bucket_url}
          opened={state.uploadObject}
          onUpload={(formData) => {
            setUncommittedChanges(formData);
            setShowNotif(true);
          }}
          onClose={() => handleChangeState("uploadObject", false)}
        />
      )}
      {filesToDelete.length > 0 && (
        <Group justify="flex-end">
          <Button
            color="red"
            onClick={() => {
              setUncommittedChanges({
                repo: repository.repo_name,
                branch: state.selectedBranch,
                storage_bucket: repository.bucket_url,
                changes: filesToDelete.map((file) => ({
                  file,
                  type: "Delete",
                })),
              });
              setShowNotif(true);
            }}
          >
            Confirm Delete {filesToDelete.length} file
            {filesToDelete.length > 1 && "s"}
          </Button>
        </Group>
      )}
    </Stack>
  );
}
