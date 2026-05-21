import nextJest from "next/jest.js";

const createJestConfig = nextJest({
  dir: "./",
});

const customJestConfig = {
  testEnvironment: "jsdom",

  setupFilesAfterEnv: [
    "<rootDir>/jest.setup.ts"
  ],

  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
  },

  modulePathIgnorePatterns: [
    "<rootDir>/.next/",
  ],
};

export default createJestConfig(customJestConfig);