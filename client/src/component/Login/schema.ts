import { z } from "zod";

export const loginSchema = z.object({
  username: z.string().min(1, "Enter a username"),
  password: z.string().min(1, "Enter a password"),
});

export type LoginValues = z.infer<typeof loginSchema>;
