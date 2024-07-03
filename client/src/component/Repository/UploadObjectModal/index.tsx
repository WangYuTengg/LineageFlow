import { Modal, FileInput, rem, Text, Group, TextInput, Button } from "@mantine/core";
import { useState } from "react";
import { IconFileCv } from "@tabler/icons-react";

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
  const [file, setFile] = useState<File | null>(null);
  const [objectName, setObjectName] = useState("");

  const icon = (
    <IconFileCv style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
  );

  const handleUpload = async () => {
    if (!file) {
      alert("Please attach a file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("objectName", objectName);
    formData.append("repo", repo);
    formData.append("branch", branch);

    try {
      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        console.log("File uploaded successfully");
        onClose(); // Close the modal after upload
      } else {
        console.error("File upload failed");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <Modal
      size="xl"
      opened={opened}
      onClose={onClose}
      title={<Text size="lg">Upload a file</Text>}
    >
      <Group>
        <Text>
          {repo}/{branch}/
        </Text>
        <TextInput
          placeholder="Object Name"
          value={objectName}
          onChange={(event) => setObjectName(event.currentTarget.value)}
        />
      </Group>

      <FileInput
        mt="md"
        leftSection={icon}
        label="Attach your data"
        placeholder="Your data"
        leftSectionPointerEvents="none"
        onChange={setFile}
      />

      <Button mt="md" onClick={handleUpload}>
        Upload
      </Button>
    </Modal>
  );
}
