const { test, expect } = require("@playwright/test");

test("homepage loads critical SEO, analytics env, and UI elements", async ({ page }, testInfo) => {
  const pageErrors = [];
  const consoleErrors = [];

  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") {
      consoleErrors.push(message.text());
    }
  });

  await page.goto("/");

  await expect(page).toHaveTitle(/Hans Niemann/i);
  await expect(page.locator("h1")).toHaveText("Hans Niemann");
  await expect(page.locator("nav a[href='#overview']")).toBeVisible();
  await expect(page.locator("#overview")).toBeVisible();
  await expect(page.locator("#timeline")).toBeVisible();
  await expect(page.locator("#faq")).toBeVisible();
  await expect(page.locator(".profile-card").first()).toBeVisible();
  await expect(page.locator("script[src='/assets/public-env.js']")).toHaveCount(1);

  const description = await page.locator("meta[name='description']").getAttribute("content");
  expect(description).toContain("Hans Niemann");

  const canonical = await page.locator("link[rel='canonical']").getAttribute("href");
  expect(canonical).toBe("https://hans-niemann.lol/");

  const robots = await page.locator("meta[name='robots']").getAttribute("content");
  expect(robots).toContain("index");

  const ldJson = await page.locator("script[type='application/ld+json']").textContent();
  const ldEntries = JSON.parse(ldJson);
  expect(ldEntries.some((entry) => entry["@type"] === "Person")).toBeTruthy();
  expect(ldEntries.some((entry) => entry["@type"] === "FAQPage")).toBeTruthy();
  expect(ldEntries.some((entry) => entry["@type"] === "WebSite")).toBeTruthy();

  const publicEnv = await page.evaluate(() => window.__HANS_NIEMANN_PUBLIC_ENV__);
  expect(publicEnv.webUrl).toBe("https://hans-niemann.lol");
  expect(publicEnv.projectName).toBe("hans-niemann");
  expect(publicEnv.clarityProjectId).toBe("wbzx6vuhvd");

  await expect(page.locator("html")).toHaveAttribute("data-clarity-enabled", "true");
  if (publicEnv.googleAnalyticsId) {
    await expect(page.locator("html")).toHaveAttribute("data-ga-enabled", "true");
    await expect(page.locator("html")).toHaveAttribute(
      "data-ga-measurement-id",
      publicEnv.googleAnalyticsId
    );
  } else {
    await expect(page.locator("html")).toHaveAttribute("data-ga-enabled", "false");
  }

  const overflow = await page.evaluate(() => {
    const doc = document.documentElement;
    return doc.scrollWidth - doc.clientWidth;
  });
  expect(overflow).toBeLessThanOrEqual(1);
  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);

  await page.screenshot({
    path: testInfo.outputPath(`home-${testInfo.project.name}.png`),
    fullPage: true
  });
});

test("faq expands and local hero image remains visible", async ({ page }) => {
  await page.goto("/");

  const controversy = page.locator("details").filter({ hasText: "What happened in 2022?" });
  await controversy.locator("summary").click();
  await expect(controversy).toHaveAttribute("open", "");

  const portrait = page.locator(".hero-visual img");
  await expect(portrait).toBeVisible();
  await expect(portrait).toHaveAttribute("src", "/assets/hero-fallback.svg");
});
