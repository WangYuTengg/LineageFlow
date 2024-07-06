import {
  ActionIcon,
  Anchor,
  Collapse,
  Divider,
  Group,
  Stack,
  Text,
} from "@mantine/core";
import {
  IconChevronDown,
  IconFolder,
  IconFile,
  IconDownload,
  IconTrash,
} from "@tabler/icons-react";
import { useState, Dispatch, SetStateAction, useEffect } from "react";
import { FileResource, FolderContents } from "../schema";

interface Props {
  folderContents: FolderContents;
  filesToDelete: FileResource[];
  setFilesToDelete: Dispatch<SetStateAction<FileResource[]>>;
}

export default function RenderFileStructure({
  folderContents,
  filesToDelete,
  setFilesToDelete,
}: Props) {
  const [opened, setOpened] = useState({});

  useEffect(() => {
    const initialOpened = Object.keys(folderContents.folders).reduce(
      (acc, folderName) => {
        acc[folderName] = true;
        return acc;
      },
      {} as { [key: string]: boolean }
    );
    setOpened(initialOpened);
  }, [folderContents.folders]);

  const handleToggle = (folderName: string) => {
    setOpened((prev) => ({
      ...prev,
      [folderName]: !prev[folderName as keyof typeof opened],
    }));
  };

  const handleDownload = (url: string) => {
    window.open(url.replace("?", "%3F").replace("=", "%3D"), "_blank");
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
          <Divider my="xs" />

          <Collapse in={opened[folderName as keyof typeof opened] || false}>
            <Stack pl="xl">
              <RenderFileStructure
                folderContents={folderContents.folders[folderName]}
                filesToDelete={filesToDelete}
                setFilesToDelete={setFilesToDelete}
              />
            </Stack>
          </Collapse>
        </div>
      ))}
      <Stack>
        {folderContents.files.map((file: FileResource, index) => (
          <div key={index}>
            <Group
              key={file.meta_data.name}
              mb="xs"
              align="flex-end"
              justify="space-between"
            >
              <Group>
                <IconFile />
                <Anchor
                  href={file.url.replace("?", "%3F").replace("=", "%3D")}
                  key={file.meta_data.name}
                  target="_blank"
                  size="md"
                  c={filesToDelete.includes(file) ? "red" : "blue"}
                  rel="noopener noreferrer"
                >
                  {file.meta_data.name.split("/").pop()}
                </Anchor>
              </Group>
              <Group>
                <ActionIcon
                  size="sm"
                  radius="xl"
                  variant="subtle"
                  c="teal"
                  onClick={() => handleDownload(file.url)}
                >
                  <IconDownload />
                </ActionIcon>
                <ActionIcon
                  size="sm"
                  radius="xl"
                  variant="subtle"
                  c="red"
                  onClick={() => {
                    if (filesToDelete.includes(file)) {
                      setFilesToDelete(filesToDelete.filter((f) => f !== file));
                    } else {
                      setFilesToDelete([...filesToDelete, file]);
                    }
                  }}
                >
                  <IconTrash />
                </ActionIcon>
              </Group>
            </Group>
            <Divider />
          </div>
        ))}
      </Stack>
    </Stack>
  );
}
