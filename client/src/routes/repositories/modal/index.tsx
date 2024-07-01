import { Modal, FileInput, rem, Text, Group, TextInput } from '@mantine/core';
import { IconFileCv } from '@tabler/icons-react';

interface Props {
    repo: string;
    branch: string;
    opened: boolean;
    onClose(): void;
}

export default function UploadObjectModal({ repo, branch, opened, onClose }: Props) {
    const icon = <IconFileCv style={{ width: rem(18), height: rem(18) }} stroke={1.5} />;
    return (
        <Modal
            size="xl"
            opened={opened}
            onClose={onClose}
            title={<Text size="lg">Upload a file</Text>}
        >
            <Group>
                <Text>{repo}/{branch}/</Text>
                <TextInput placeholder="Object Name" />
            </Group>
            
            <FileInput
                leftSection={icon}
                label="Attach your data"
                placeholder="Your data"
                leftSectionPointerEvents="none"
            />
            
        </Modal>
    );
}
