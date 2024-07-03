import { Tabs, rem, Text } from "@mantine/core";
import {
  IconDatabase,
  IconCancel,
  IconGitCommit,
  IconGitBranch,
  IconGitCompare,
  IconCircleCaretRight,
  IconSettings,
} from "@tabler/icons-react";
import RepositoryPage from "../Repository";
import { Repository } from "../../schema";

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
  { value: "compare", iconComponent: IconGitCompare, label: "Compare" },
  { value: "actions", iconComponent: IconCircleCaretRight, label: "Actions" },
  { value: "settings", iconComponent: IconSettings, label: "Settings" },
];

function TabComponent({ selectedRepository }: Props) {
  return (
    <Tabs defaultValue="objects" variant="outline">
      <Tabs.List justify="flex-start">
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
        <RepositoryPage repository={selectedRepository} />
      </Tabs.Panel>

      <Tabs.Panel value="uncommittedChanges">
        Uncommitted Changes tab content
      </Tabs.Panel>

      <Tabs.Panel value="commits">Commits tab content</Tabs.Panel>

      <Tabs.Panel value="branches">Branches tab content</Tabs.Panel>

      <Tabs.Panel value="compare">Compare tab content</Tabs.Panel>

      <Tabs.Panel value="actions">Actions tab content</Tabs.Panel>

      <Tabs.Panel value="settings">Settings tab content</Tabs.Panel>
    </Tabs>
  );
}

export default TabComponent;
