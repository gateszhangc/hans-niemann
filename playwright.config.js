const { defineConfig, devices } = require("@playwright/test");

const PORT = 43173;
const liveBaseURL = process.env.PLAYWRIGHT_BASE_URL;

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  use: {
    baseURL: liveBaseURL || `http://127.0.0.1:${PORT}`,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure"
  },
  webServer: liveBaseURL
    ? undefined
    : {
        command: `python3 -m http.server ${PORT} --bind 127.0.0.1 --directory .`,
        port: PORT,
        reuseExistingServer: false,
        timeout: 30_000
      },
  projects: [
    {
      name: "desktop-chrome",
      use: {
        ...devices["Desktop Chrome"]
      }
    },
    {
      name: "mobile-chrome",
      use: {
        ...devices["Pixel 7"]
      }
    }
  ]
});
