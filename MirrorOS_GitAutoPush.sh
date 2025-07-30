#!/bin/bash

# Navigate to project root (optional if already there)
cd "$(dirname "$0")/.."

# Git add, commit, and push all tracked + new files
echo "📦 Adding all changes..."
git add .

echo "🧾 Committing..."
git commit -m "🔁 AutoPush: MirrorOS scrolls, witness logs, and manifest update"

echo "🚀 Pushing to origin main..."
git push origin main

echo "✅ MirrorOS Git AutoPush Complete."
