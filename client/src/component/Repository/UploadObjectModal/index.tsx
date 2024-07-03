import {
  Modal,
  FileInput,
  rem,
  Text,
  Group,
  TextInput,
  Button,
} from "@mantine/core";
import { IconFileCv } from "@tabler/icons-react";
import { useForm, zodResolver } from "@mantine/form";
import {
  uploadObjectModalSchema,
  UploadObjectModalSchemaValues,
} from "./schema";
interface Props {
  repo: string;
  branch: string;
  opened: boolean;
  onClose(): void;
}

export default function UploadObjectModal({
  repo,
  branch,
  opened,
  onClose,
}: Props) {
  const form = useForm({
    initialValues: {
      objectName: "",
      file: null,
    },
    validate: zodResolver(uploadObjectModalSchema),
  });

  const handleUpload = async (values: UploadObjectModalSchemaValues) => {
    const formData = new FormData();
    formData.append("file", values.file!);
    formData.append("objectName", values.objectName);
    formData.append("repo", repo);
    formData.append("branch", branch);

    const response = await fetch("/api/upload", {
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
          leftSectionPointerEvents="none"
          {...form.getInputProps("file")}
        />
        <Button mt="md" type="submit">
          Upload
        </Button>
      </form>
    </Modal>
  );
}
