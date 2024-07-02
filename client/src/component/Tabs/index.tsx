import { Tabs, rem } from '@mantine/core';
import { IconDatabase, IconCancel, IconGitCommit, IconGitBranch, IconGitCompare, IconCircleCaretRight, IconSettings } from '@tabler/icons-react';
import styles from './Tabs.module.css';

const iconStyle = { width: rem(12), height: rem(12) };

function TabComponent() {
    return (
        <div className={styles.tabs}>
            <Tabs defaultValue="objects">
                <Tabs.List>
                    <Tabs.Tab value="objects" leftSection={<IconDatabase style={iconStyle} />}>
                        Objects
                    </Tabs.Tab>
                    <Tabs.Tab value="uncommittedChanges" leftSection={<IconCancel style={iconStyle} />}>
                        Uncommitted Changes
                    </Tabs.Tab>
                    <Tabs.Tab value="commits" leftSection={<IconGitCommit style={iconStyle} />}>
                        Commits
                    </Tabs.Tab>
                    <Tabs.Tab value="branches" leftSection={<IconGitBranch style={iconStyle} />}>
                        Branches
                    </Tabs.Tab>
                    <Tabs.Tab value="compare" leftSection={<IconGitCompare style={iconStyle} />}>
                        Compare
                    </Tabs.Tab>
                    <Tabs.Tab value="actions" leftSection={<IconCircleCaretRight style={iconStyle} />}>
                        Actions
                    </Tabs.Tab>
                    <Tabs.Tab value="settings" leftSection={<IconSettings style={iconStyle} />}>
                        Settings
                    </Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="objects">
                    Objects tab content
                </Tabs.Panel>

                <Tabs.Panel value="uncommittedChanges">
                    Uncommitted Changes tab content
                </Tabs.Panel>

                <Tabs.Panel value="commits">
                    Commits tab content
                </Tabs.Panel>

                <Tabs.Panel value="branches">
                    Branches tab content
                </Tabs.Panel>

                <Tabs.Panel value="compare">
                    Compare tab content
                </Tabs.Panel>

                <Tabs.Panel value="actions">
                    Actions tab content
                </Tabs.Panel>

                <Tabs.Panel value="settings">
                    Settings tab content
                </Tabs.Panel>
            </Tabs>
        </div>
    );
}

export default TabComponent;
