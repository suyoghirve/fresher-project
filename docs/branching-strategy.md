# Branching Strategy

## 1. Overview

This project follows the Trunk-Based Development (TBD) approach.

The `main` branch is the primary development branch and represents the
latest stable version of the project.

Developers work on short-lived feature or documentation branches and
integrate changes into `main` frequently through Pull Requests.

## 2. Branch Structure

### Main Branch

- `main` is the primary integration branch.
- It should remain stable and functional.
- Direct commits to `main` should generally be avoided.
- Changes should be integrated through Pull Requests.

### Short-Lived Feature Branches

Create a separate branch for each task.

Naming conventions:

- `feature/<description>` - New functionality.
- `fix/<description>` - Bug fixes.
- `docs/<description>` - Documentation updates.
- `refactor/<description>` - Code improvements.

Examples:

- `feature/system-monitoring`
- `fix/nginx-configuration`
- `docs/branching-strategy`

Branches should be merged and deleted after completing their purpose.

## 3. Development Workflow

1. Update the local main branch:

   ```bash
   git switch main
   git pull --ff-only origin main
