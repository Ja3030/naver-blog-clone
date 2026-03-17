#!/bin/bash
# Usage: ./scripts/new-post.sh <slug>
# Example: ./scripts/new-post.sh tonsil-stone

if [ -z "$1" ]; then
  echo "Usage: ./scripts/new-post.sh <slug>"
  echo "Example: ./scripts/new-post.sh tonsil-stone"
  exit 1
fi

SLUG=$1
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
POST_DIR="$BASE_DIR/public/posts/$SLUG"

if [ -d "$POST_DIR" ]; then
  echo "Error: Post directory already exists: $POST_DIR"
  exit 1
fi

mkdir -p "$POST_DIR/images"
cp "$BASE_DIR/templates/post-template.html" "$POST_DIR/index.html"
cp "$BASE_DIR/templates/config-template.json" "$POST_DIR/config.json"

echo "Created: $POST_DIR/"
echo "   - index.html (edit POST CONTENT area)"
echo "   - config.json (edit blog/post/social/comments)"
echo "   - images/ (add post images)"
