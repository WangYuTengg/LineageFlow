import React, { useState } from 'react';
import { Modal, Button, Text } from "@mantine/core";
import { IconFileCv } from "@tabler/icons-react";

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
    const [folderName, setFolderName] = useState<string>("");

    const handleDirectoryUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if (files) {
            const fileArray = Array.from(files);
            setFiles(fileArray);
            if (fileArray.length > 0) {
                const commonPath = fileArray[0].webkitRelativePath.split('/')[0];
                setFolderName(commonPath);
            }
        }
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            alert("Please select a file or folder to upload.");
            return;
        }

        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file);
            formData.append('relative_paths', file.webkitRelativePath);
        });
        formData.append('repo', repo);
        formData.append('branch', branch);
        formData.append('storage_bucket', storage_bucket);

        const response = await fetch("/api/upload/", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            alert("Files uploaded successfully");
            onClose();
        } else {
            console.error(response.statusText);
            alert("File upload failed");
        }
    };

    return (
        <Modal opened={opened} onClose={onClose} title="Upload Data">
            <input
                type="file"
                //@ts-ignore
                webkitdirectory="true"
                mozdirectory="true"
                directory="true"
                multiple
                onChange={handleDirectoryUpload}
                style={{ display: 'none' }}
                id="directoryUpload"
            />
            <label htmlFor="directoryUpload">
                <Button component="span">
                    <IconFileCv style={{ width: 18, height: 18 }} stroke={1.5} />
                    Select Folder
                </Button>
            </label>
            {folderName && (
                <Text mt="md">Selected Folder: {folderName}</Text>
            )}
            <Button mt="md" onClick={handleUpload}>
                Upload
            </Button>
        </Modal>
    );
}

