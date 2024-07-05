import {
  Modal,
  FileInput,
  rem,
  Text,
  Group,
  TextInput,
  Button,
} from "@mantine/core";
import { useState } from 'react';
import { IconFileCv } from "@tabler/icons-react";
import { useForm, zodResolver } from "@mantine/form";
import {
  uploadObjectModalSchema,
  UploadObjectModalSchemaValues,
} from "../schema";

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
  const [file, setFile] = useState<File[]>([]);

  const form = useForm({
    initialValues: {
      objectName: "",
      file: null,
    },
    validate: zodResolver(uploadObjectModalSchema),
  });

  const handleUpload = async (values: UploadObjectModalSchemaValues) => {
    console.log("handleUpload called with values:", values);
    console.log("Files to upload:", file);

    const formData = new FormData();
    // file.forEach((file, index) => {
    //   formData.append(`file_${index}`, file);
    // });
    formData.append("objectName", values.objectName);
    formData.append("repo", repo);
    formData.append("branch", branch);
    formData.append("storage_bucket", storage_bucket);

    const response = await fetch("/api/upload/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("File uploaded successfully");
      onClose();
    } else {
      console.error(response.statusText);
      alert("File upload failed");
    }
  };

  return (
    <Modal
      size="xl"
      opened={opened}
      onClose={onClose}
      title={<Text size="lg">Upload a file</Text>}
    >
      <form
        onSubmit={form.onSubmit(async (values) => {
          console.log("Form submitted with values:", values); // Debugging line
          await handleUpload(values);
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
          label="Attach your data"
          placeholder="Your data"
          multiple
          value = {file}  
          // @ts-ignore
          onChange={setFile}
          {...form.getInputProps("file")}
          leftSectionPointerEvents="none"
        />
        <Button mt="md" type="submit" disabled={!form.isDirty()}>
          Upload
        </Button>
      </form>
    </Modal>
  );
}
