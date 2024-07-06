import { Tabs, rem, Text } from "@mantine/core";
import {
  IconDatabase,
  IconCancel,
  IconGitCommit,
  IconGitBranch,
  IconSettings,
} from "@tabler/icons-react";
import RepositoryPage from "./objects-page";
import { Repository, UncommittedChanges } from "../schema";
import { useState } from "react";
import UncommittedChangesPage from "./uncommited-changes";
import BranchesPage from "./branches";

const iconStyle = { width: rem(16), height: rem(16) };

interface Props {
  selectedRepository: Repository;
}

const tabsData = [
  { value: "objects", iconComponent: IconDatabase, label: "Objects" },
  {
    value: "uncommittedChanges",
    iconComponent: IconCancel,
    label: "Uncommitted Changes",
  },
  { value: "commits", iconComponent: IconGitCommit, label: "Commits" },
  { value: "branches", iconComponent: IconGitBranch, label: "Branches" },
  { value: "settings", iconComponent: IconSettings, label: "Settings" },
];

export function RepositoryTabs({ selectedRepository }: Props) {
  const [activeTab, setActiveTab] = useState<string | null>("objects");
  const [uncommittedChanges, setUncommittedChanges] =
    useState<UncommittedChanges | null>(null);

  return (
    <Tabs value={activeTab} onChange={setActiveTab} variant="outline">
      <Tabs.List>
        {tabsData.map((tab) => (
          <Tabs.Tab
            key={tab.value}
            value={tab.value}
            leftSection={<tab.iconComponent style={iconStyle} />}
          >
            <Text size="lg">{tab.label}</Text>
          </Tabs.Tab>
        ))}
      </Tabs.List>

      <Tabs.Panel value="objects">
        <RepositoryPage
          repository={selectedRepository}
          onUncommittedChanges={(data) => {
            setActiveTab("uncommittedChanges");
            setUncommittedChanges(data);
          }}
        />
      </Tabs.Panel>

      <Tabs.Panel value="uncommittedChanges">
        <UncommittedChangesPage
          uncommittedChanges={uncommittedChanges}
          repository={selectedRepository}
          onDone={() => setActiveTab("objects")}
        />
      </Tabs.Panel>

      <Tabs.Panel value="commits">Commits tab content</Tabs.Panel>
      <Tabs.Panel value="branches">
        <BranchesPage
          branches={selectedRepository.branches}
          defaultBranch={selectedRepository.default_branch}
        />
      </Tabs.Panel>
      <Tabs.Panel value="settings">Settings tab content</Tabs.Panel>
    </Tabs>
  );
}
