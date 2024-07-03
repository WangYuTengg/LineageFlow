import { Group, Select, Button } from "@mantine/core";
import { GoUpload } from "react-icons/go";
import { useState, useEffect } from "react";
import UploadObjectModal from "./UploadObjectModal";

type Branch = string | null;

export default function RepositoryPage() {
  const [branches, setBranches] = useState<Branch[]>([]);
  const [uploadObject, setUploadObject] = useState(false);

  useEffect(() => {
    const fetchBranches = async () => {
      try {
        const response = await fetch("INSERT CALL HERE");
        const data: Branch[] = await response.json();
        if (data) {
          const formattedBranches = data.map((branch) => `branch: ${branch}`);
          setBranches(formattedBranches);
        } else {
          console.error("Error fetching branches: No branches");
        }
      } catch (error) {
        console.error("Error fetching branches: ", error);
      }
    };
    fetchBranches();
  }, []);
  return (
    <>
      <Group justify="space-between" px="150" mt="20">
        <Select
          data={["main", "branch1", "branch2"].map(
            (branch) => `branch: ${branch}`
          )}
          size="md"
        ></Select>

        <Button
          leftSection={<GoUpload />}
          onClick={() => setUploadObject(true)}
        >
          Upload Object
        </Button>
      </Group>
      {uploadObject && (
        <UploadObjectModal
          repo="test-repo"
          branch="main"
          opened={uploadObject}
          onClose={() => setUploadObject(false)}
        />
      )}
    </>
  );
}
