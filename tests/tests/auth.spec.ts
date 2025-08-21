import { test } from "./fixtures/auth";
import { expect } from "@playwright/test";

// the fixture alone is the test
test("register + login", async ({ loggedInPage }) => {});

test("logout", async ({ loggedInPage }) => {
  await loggedInPage.getByRole("button", { name: "Logout" }).click();
  await expect(loggedInPage.getByRole("link", { name: "Register" }))
    .toBeVisible();
});
