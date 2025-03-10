import os
import re
import json

# Template file path
TEMPLATE_FILE_PATH = 'blog_template.html'

# Output file path
OUTPUT_FILE_PATH = 'new_post.html'

# Load configuration from JSON file
with open('content.json', 'r') as config_file:
    config = json.load(config_file)

# Placeholder values for a new post
placeholder_values = {
    "{{POST_DESCRIPTION}}": config["POST_DESCRIPTION"],
    "{{POST_TITLE}}": config["POST_TITLE"],
    "{{POST_DATE}}": config["POST_DATE"],
    "{{READING_TIME}}": config["READING_TIME"],
    "{{POST_INTRO}}": config["POST_INTRO"],
    "{{POST_CONTENT}}": config["POST_CONTENT"],
    "{{POST_CONCLUSION}}": config["POST_CONCLUSION"],
    "{{POST_TAGS}}": config["POST_TAGS"],
    "{{POST_WORD_COUNT}}": config["POST_WORD_COUNT"]
}


# Read the template content
with open(TEMPLATE_FILE_PATH, 'r') as file:
    template_content = file.read()

# Replace placeholders with actual values
for placeholder, value in placeholder_values.items():
    template_content = template_content.replace(placeholder, value)

# Wrap all <pre><code> blocks with CodeSnippet div
template_content = re.sub(
    r'(<pre[^>]*>\s*<code[^>]*>.*?</code>\s*</pre>)',
    r'<div class="CodeSnippet">\1</div>',
    template_content,
    flags=re.DOTALL
)

# Write the new content to a file
with open(OUTPUT_FILE_PATH, 'w') as file:
    file.write(template_content)

print(f"New post generated: {OUTPUT_FILE_PATH}")