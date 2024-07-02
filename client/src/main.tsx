import ReactDOM from "react-dom/client";
import { StrictMode } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { MantineProvider, DEFAULT_THEME, Stack } from "@mantine/core";
import "./index.css";
import "@mantine/core/styles.css";
import App from "./App";
import Navbar from "./component/Navbar";
import LoginForm from "./component/Login";
import SignUpForm from "./component/Signup";
import Tabs from "./component/Tabs";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <MantineProvider theme={DEFAULT_THEME} defaultColorScheme="dark">
        <Stack p="xs">
          <Navbar />
          <Tabs />
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route path="/signup" element={<SignUpForm />} />
            <Route path="/" element={<App />} />
          </Routes>
        </Stack>
      </MantineProvider>
    </BrowserRouter>
  </StrictMode>
);
