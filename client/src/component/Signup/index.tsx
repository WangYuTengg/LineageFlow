import { Text, TextInput, Stack, Button } from "@mantine/core";

export default function SignUpForm() {
  return (
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
      />
      <TextInput
        label="Password"
        style={{ width: "400px" }}
        size="md"
        withAsterisk
        placeholder="Enter your password"
        type="password"
      />
      <Button w={400}>Confirm Sign-up</Button>
    </Stack>
  );
}
