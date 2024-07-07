import "./index.css";
import "@mantine/core/styles.css";
import ReactDOM from "react-dom/client";
import { StrictMode } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { MantineProvider, DEFAULT_THEME, Stack } from "@mantine/core";
import { AuthProvider, ProtectedRoute } from "./auth";
import { RepoProvider } from "./repo";
import Navbar from "./component/navbar";
import LoginForm from "./component/login-form";
import SignUpForm from "./component/signup-form";
import Repositories from "./routes/repository-list";
import Repository from "./routes/repository";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={DEFAULT_THEME} defaultColorScheme="dark">
      <BrowserRouter>
        <AuthProvider>
          <RepoProvider>
            <Stack p="xs">
              <Navbar />
              <Routes>
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <></>
                    </ProtectedRoute>
                  }
                />
                <Route path="/login" element={<LoginForm />} />
                <Route path="/signup" element={<SignUpForm />} />
                <Route
                  path="/u/:username/repositories"
                  element={
                    <ProtectedRoute>
                      <Repositories />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/u/:username/r/:repo_name"
                  element={
                    <ProtectedRoute>
                      <Repository />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </Stack>
          </RepoProvider>
        </AuthProvider>
      </BrowserRouter>
    </MantineProvider>
  </StrictMode>
);
