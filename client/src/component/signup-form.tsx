import { Text, TextInput, Stack, Button } from "@mantine/core";
import { useForm, zodResolver } from "@mantine/form";
import { useNavigate } from "react-router-dom";
import { signupSchema, SignupSchemaValues } from "../schema";
export default function SignUpForm() {
  const navigate = useNavigate();
  const form = useForm({
    initialValues: {
      username: "",
      password: "",
      email: "",
    },
    validate: zodResolver(signupSchema),
  });

  const handleLogin = async (values: SignupSchemaValues) => {
    try {
      const response = await fetch("/api/signup/", {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        alert(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      alert("Sign up successful! Please login to continue.");
      navigate("/login");
      console.log("Sign up successful", data);
    } catch (error) {
      alert(`Error: ${error}`);
    }
  };
  return (
    <form onSubmit={form.onSubmit(async (values) => handleLogin(values))}>
      <Stack gap="md" justify="center" align="center">
        <Text ta="center" size="xl">
          Sign up
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
        <TextInput
          label="Email"
          style={{ width: "400px" }}
          size="md"
          withAsterisk
          placeholder="Enter your email"
          {...form.getInputProps("email")}
        />
        <Button w={400} type="submit">
          Confirm Sign-up
        </Button>
      </Stack>
    </form>
  );
}
