import { Text, TextInput, Stack, Button } from "@mantine/core";
import { useForm, zodResolver } from "@mantine/form";
import { loginSchema } from "./schema";
import { useAuth } from "../../auth";
import { Navigate } from "react-router-dom";
import { useState } from "react";

export default function LoginForm() {
  const { login } = useAuth();
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const form = useForm({
    initialValues: { username: "", password: "" },
    validate: zodResolver(loginSchema),
  });

  if (shouldRedirect) {
    return <Navigate to="/" replace />;
  }

  return (
    <form
      onSubmit={form.onSubmit(async (values) => {
        const response = await fetch("/api/loginAdmin/", {
          method: "POST",
          body: JSON.stringify(values),
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          login(values.username);
          setShouldRedirect(true);
        } else alert("Invalid username or password");
      })}
    >
      <Stack gap="md" justify="center" align="center">
        <Text ta="center" size="xl">
          Login
        </Text>
        <TextInput
          style={{ width: "400px" }}
          size="md"
          withAsterisk
          label="Username"
          placeholder="Enter your username"
          {...form.getInputProps("username")}
        />
        <TextInput
          label="Password"
          style={{ width: "400px" }}
          size="md"
          withAsterisk
          placeholder="Enter your password"
          type="password"
          {...form.getInputProps("password")}
        />
        <Button w={400} type="submit">
          Login
        </Button>{" "}
      </Stack>
    </form>
  );
}
