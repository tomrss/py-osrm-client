module.exports = {
  branches: ["main"],
  ci: false,
  dryRun: false,
  plugins: [
    [
      "@semantic-release/commit-analyzer",
      {
        preset: "angular",
        releaseRules: [
          { type: "breaking", release: "major" },
          { type: "major", release: "major" },
        ],
      },
    ],
    "@semantic-release/release-notes-generator",
    [
      "@semantic-release/github",
      {
        "assets": ["dist/**"]
      }
    ]
  ],
};

