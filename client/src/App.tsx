import "@mantine/core/styles.css";
import { MantineProvider, DEFAULT_THEME } from "@mantine/core";

export default function App() {
  return (
    <MantineProvider theme={DEFAULT_THEME} defaultColorScheme="dark">
      Hello world
    </MantineProvider>
  );
}
