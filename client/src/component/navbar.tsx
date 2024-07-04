import {
  HoverCard,
  Group,
  Button,
  UnstyledButton,
  Text,
  SimpleGrid,
  ThemeIcon,
  Anchor,
  Stack,
  Avatar,
  Divider,
  Center,
  Box,
  Burger,
  Drawer,
  Collapse,
  ScrollArea,
  rem,
  useMantineTheme,
} from "@mantine/core";
import { Link, useNavigate } from "react-router-dom";
import { useDisclosure } from "@mantine/hooks";
import {
  IconTruck,
  IconNotification,
  IconCode,
  IconBook,
  IconChartPie3,
  IconFingerprint,
  IconCoin,
  IconChevronDown,
} from "@tabler/icons-react";
import classes from "./navbar.module.css";
import { useAuth } from "../auth";

const mockdata = [
  {
    icon: IconCode,
    title: "Open source",
    description: "This Pokémon’s cry is very loud and distracting",
  },
  {
    icon: IconCoin,
    title: "Free for everyone",
    description: "The fluid of Smeargle’s tail secretions changes",
  },
  {
    icon: IconBook,
    title: "Documentation",
    description: "Yanma is capable of seeing 360 degrees without",
  },
  {
    icon: IconFingerprint,
    title: "Security",
    description: "The shell’s rounded shape and the grooves on its.",
  },
  {
    icon: IconChartPie3,
    title: "Analytics",
    description: "This Pokémon uses its flying ability to quickly chase",
  },
  {
    icon: IconNotification,
    title: "Notifications",
    description: "Combusken battles with the intensely hot flames it spews",
  },
];

export default function Navbar() {
  const { isLoggedIn, userName, logout } = useAuth();
  const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] =
    useDisclosure(false);
  const [linksOpened, { toggle: toggleLinks }] = useDisclosure(false);
  const theme = useMantineTheme();
  const navigate = useNavigate();

  const links = mockdata.map((item) => (
    <UnstyledButton className={classes.subLink} key={item.title}>
      <Group wrap="nowrap" align="flex-start">
        <ThemeIcon size={34} variant="default" radius="md">
          <item.icon
            style={{ width: rem(22), height: rem(22) }}
            color={theme.colors.blue[6]}
          />
        </ThemeIcon>
        <div>
          <Text size="sm" fw={500}>
            {item.title}
          </Text>
          <Text size="xs" c="dimmed">
            {item.description}
          </Text>
        </div>
      </Group>
    </UnstyledButton>
  ));

  return (
    <Box>
      <header className={classes.header}>
        <Group justify="space-between" h="100%">
          <Group>
            <IconTruck size={30} />
            <Text size="lg" fw="500">
              LineageFlow
            </Text>
          </Group>
          {isLoggedIn && (
            <Group h="100%" gap={0} visibleFrom="sm">
              <Link to={`/u/${userName}/repositories`} className={classes.link}>
                Repositories
              </Link>
              <HoverCard
                width={600}
                position="bottom"
                radius="md"
                shadow="md"
                withinPortal
              >
                <HoverCard.Target>
                  <a href="#" className={classes.link}>
                    <Center inline>
                      <Box component="span" mr={5}>
                        Feature Store
                      </Box>
                      <IconChevronDown
                        style={{ width: rem(16), height: rem(16) }}
                        color={theme.colors.blue[6]}
                      />
                    </Center>
                  </a>
                </HoverCard.Target>

                <HoverCard.Dropdown style={{ overflow: "hidden" }}>
                  <Group justify="space-between" px="md">
                    <Text fw={500}>Features</Text>
                    <Anchor href="#" fz="xs">
                      View all
                    </Anchor>
                  </Group>

                  <Divider my="sm" />

                  <SimpleGrid cols={2} spacing={0}>
                    {links}
                  </SimpleGrid>
                </HoverCard.Dropdown>
              </HoverCard>
            </Group>
          )}

          {!isLoggedIn ? (
            <Group visibleFrom="sm">
              <Button variant="default" onClick={() => navigate("/login")}>
                Log in
              </Button>
              <Button onClick={() => navigate("/signup")}>Sign up</Button>
            </Group>
          ) : (
            <Group visibleFrom="sm">
              <Text>
                Logged in as <b>{userName}</b>
              </Text>
              <Avatar size={36} radius="xl" src="https://i.pravatar.cc/300" />
              <Button onClick={() => logout()}>Log out</Button>
            </Group>
          )}

          <Burger
            opened={drawerOpened}
            onClick={toggleDrawer}
            hiddenFrom="sm"
          />
        </Group>
      </header>

      <Drawer
        opened={drawerOpened}
        onClose={closeDrawer}
        size="100%"
        padding="md"
        title="Navigation"
        hiddenFrom="sm"
        zIndex={1000000}
      >
        <ScrollArea h={`calc(100vh - ${rem(80)})`} mx="-md">
          {isLoggedIn && (
            <>
              <Divider my="sm" />

              <Link to={`/u/${userName}/repositories`} className={classes.link}>
                Repositories
              </Link>
              <UnstyledButton className={classes.link} onClick={toggleLinks}>
                <Center inline>
                  <Box component="span" mr={5}>
                    Features
                  </Box>
                  <IconChevronDown
                    style={{ width: rem(16), height: rem(16) }}
                    color={theme.colors.blue[6]}
                  />
                </Center>
              </UnstyledButton>
              <Collapse in={linksOpened}>{links}</Collapse>
              <Divider my="sm" />
            </>
          )}
          {!isLoggedIn ? (
            <Group justify="center" grow pb="xl" px="md">
              <Button variant="default" onClick={() => navigate("/login")}>
                Log in
              </Button>
              <Button onClick={() => navigate("/signup")}>Sign up</Button>
            </Group>
          ) : (
            //todo: style this better
            <Stack justify="center" pb="xl" px="md">
              <Text>
                Logged in as <b>{userName}</b>
              </Text>
              <Avatar size={60} radius="xl" src="https://i.pravatar.cc/300" />
              <Button onClick={() => logout()}>Log out</Button>{" "}
            </Stack>
          )}
        </ScrollArea>
      </Drawer>
    </Box>
  );
}
