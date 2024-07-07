import { Stack, Group, Anchor } from "@mantine/core";
import { useNavigate, useParams } from "react-router-dom";
import { RepositoryTabs } from "../component/repository-tabs";
import { type Repository } from "../schema";
import { useAuth } from "../auth";
import { useRepo } from "../repo";

export default function Repository() {
  const navigate = useNavigate();
  const params = useParams();
  const { repositories, fetchRepositories } = useRepo();
  const { userName } = useAuth();

  const repository = repositories.find((r) => r.repo_name === params.repo_name);
  if (!repository) {
    navigate(`/u/${userName}/repositories`);
    return null;
  }

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
        <RepositoryTabs
          selectedRepository={repository}
          onCreateBranch={async () => await fetchRepositories()}
        />
      </Stack>
    </>
  );
}
