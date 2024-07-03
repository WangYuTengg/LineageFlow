import { Text, TextInput, Stack, Button } from "@mantine/core";
import { useForm } from "@mantine/form"

export default function SignUpForm() {
  const form = useForm({
    initialValues: {
      username: "",
      password: "",
      email: "example@example.com"
    }
  });

  const handleLogin = async (values: { username: string; password: string; email: string }) => {
    try {
      const response = await fetch('http://localhost:8000/api/signup/', {
        headers: {
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Sign up successful', data);
      // Handle successful signup (e.g., show a success message or redirect)
    } catch (error) {
      console.error('Error during sign up', error);
      // Handle error (e.g., show an error message)
    }
  };
  return (
    <form onSubmit={form.onSubmit((values) => handleLogin(values))}>
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
        <Button w={400} type = "submit">Confirm Sign-up</Button>
      </Stack>
    </form >
  );
}
