import React, { useState } from "react";
import {
  Modal,
  Button,
  Text,
  Stack,
  Group,
  Divider,
  FileInput,
  TextInput,
  rem,
} from "@mantine/core";
import { IconFileCv } from "@tabler/icons-react";
import { useForm, zodResolver } from "@mantine/form";
import { uploadObjectModalSchema } from "../schema";

interface Props {
  repo: string;
  branch: string;
  storage_bucket: string;
  opened: boolean;
  onClose(): void;
}

export default function UploadObjectModal({
  repo,
  branch,
  storage_bucket,
  opened,
  onClose,
}: Props) {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [folderName, setFolderName] = useState<string>("");

  const form = useForm({
    initialValues: {
      objectName: "",
      file: null,
    },
    validate: zodResolver(uploadObjectModalSchema),
  });

  const handleDirectoryUpload = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const files = event.target.files;
    if (files) {
      const fileArray = Array.from(files);
      setFiles(fileArray);
      if (fileArray.length > 0) {
        const commonPath = fileArray[0].webkitRelativePath.split("/")[0];
        setFolderName(commonPath);
      }
    }
  };

  const handleUpload = async () => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      files!.forEach((file) => {
        formData.append("files", file);
        formData.append("relative_paths", file.webkitRelativePath);
      });
      formData.append("repo", repo);
      formData.append("branch", branch);
      formData.append("storage_bucket", storage_bucket);
      const response = await fetch("/api/upload/", {
        method: "POST",
        body: formData,
      });
      console.log(response);
      if (response.ok) {
        alert("Files uploaded successfully");
        onClose();
      } else {
        console.error(response.statusText);
        alert("File upload failed");
      }
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      alert("File upload failed");
    }
    setIsLoading(false);
  };

  return (
    <Modal opened={opened} onClose={onClose} title="Upload Data" size="lg">
      <Stack>
        <Text size="xl" fw={500}>
          Upload a folder
        </Text>
        <input
          type="file"
          //@ts-expect-error fck ts
          webkitdirectory="true"
          mozdirectory="true"
          directory="true"
          multiple
          onChange={handleDirectoryUpload}
          style={{ display: "none" }}
          id="directoryUpload"
        />
        <label htmlFor="directoryUpload">
          <Button
            component="span"
            leftSection={
              <IconFileCv style={{ width: 18, height: 18 }} stroke={1.5} />
            }
          >
            Select Folder
          </Button>
        </label>
        {folderName && (
          <Text mt="md" size="lg">
            Selected Folder: <b>{folderName}</b>
          </Text>
        )}
        <Group justify="flex-end">
          <Button
            mt="md"
            onClick={handleUpload}
            disabled={!files.length}
            loading={isLoading}
          >
            Upload
          </Button>
        </Group>

        <Divider />

        <Text size="xl" fw={500}>
          Upload a file
        </Text>

        <form
          onSubmit={form.onSubmit(async (values) => {
            console.log("Form submitted with values:", values);
            //todo: handle single or multiple file uploads
          })}
        >
          <Group wrap="nowrap">
            <Text>
              {repo}/{branch}/
            </Text>
            <TextInput
              placeholder="Object Name"
              {...form.getInputProps("objectName")}
            />
          </Group>

          <FileInput
            mt="md"
            leftSection={
              <IconFileCv
                style={{ width: rem(18), height: rem(18) }}
                stroke={1.5}
              />
            }
            label="Attach your file(s)"
            placeholder="Select file"
            multiple
            {...form.getInputProps("file")}
            leftSectionPointerEvents="none"
          />
          <Group justify="flex-end">
            <Button mt="md" type="submit" disabled={!form.isDirty()}>
              Upload file
            </Button>
          </Group>
        </form>
      </Stack>
    </Modal>
  );
}
