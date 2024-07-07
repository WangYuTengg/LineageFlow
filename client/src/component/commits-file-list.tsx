import { Anchor, Collapse, Group, Stack, Text } from "@mantine/core";
import { Commit, FileResource } from "../schema";
import { useState } from "react";

interface Props {
  files: { file: FileResource; commit_id: string }[];
  commit: Commit;
  typeString: string;
}

export default function FilesList({ typeString, files, commit }: Props) {
  const [opened, setOpened] = useState(false);
  return (
    <Stack>
      <Group
        align="flex-end"
        justify="space-between"
        style={{ width: "200px" }}
      >
        <Text size="md" mt={8}>
          <b>{typeString} Files: </b>
        </Text>
        <Anchor size="md" onClick={() => setOpened((o) => !o)}>
          {opened ? "Hide" : "Show"}
        </Anchor>
      </Group>
      <Collapse in={opened}>
        {files
          .filter((add) => add.commit_id === commit.commit_id)
          .map(({ file }) => (
            <Text key={file.id} size="xs" mt={4}>
              {typeString === "Added" && "+"}
              {typeString === "Deleted" && "-"}
              {typeString === "Modified" && "~"} {file.file_name}
            </Text>
          ))}
      </Collapse>
    </Stack>
  );
}
