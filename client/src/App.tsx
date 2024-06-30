import "@mantine/core/styles.css";
import { MantineProvider, DEFAULT_THEME, Stack } from "@mantine/core";
import Navbar from "./component/Navbar";
import Repository from "./component/Repository";

export default function App() {
  return (
    <MantineProvider theme={DEFAULT_THEME} defaultColorScheme="dark">
      <Stack p="md">
        <Navbar />
        <Repository />
      </Stack>
    </MantineProvider>
  );
}
