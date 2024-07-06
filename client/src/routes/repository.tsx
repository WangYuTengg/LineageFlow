import { Stack, Group, Anchor } from "@mantine/core";
import { useNavigate, useLocation } from "react-router-dom";
import { RepositoryTabs } from "../component/repository-tabs";
import { type Repository } from "../schema";
import { useAuth } from "../auth";
import { useEffect } from "react";

export default function Repository() {
  const navigate = useNavigate();
  const location = useLocation();
  const { repo } = location.state;
  const { userName } = useAuth();

  const repository: Repository = {
    repo_id: repo.repo_id,
    repo_name: repo.repo_name,
    description: repo.description,
    default_branch: repo.default_branch,
    branches: repo.branches,
    created_timestamp: repo.created_timestamp,
    bucket_url: repo.bucket_url,
    updated_timestamp: repo.updated_timestamp,
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/getCommitData?repo=${repository.repo_name}&branch=${repository.default_branch}`, {
          headers: {
            "Content-Type": "application/json",
          },
          method: "GET",
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data); 
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
  
    fetchData();
  }, [repository.repo_name, repository.default_branch]); 
  
  return (
    <>
      <Stack px="sm">
        <Group bg="gray" p="md">
          <Anchor
            c="blue"
            size="lg"
            onClick={() => navigate(`/u/${userName}/repositories`)}
          >
            Repositories
          </Anchor>
        </Group>
        <RepositoryTabs selectedRepository={repository} />
      </Stack>
    </>
  );
}
