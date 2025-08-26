# thiago4go.github.io
my blog

## Post Generator

The `post-generator` folder contains a script that builds new blog posts from
`content.json` and `blog_template.html`. Along with the existing content fields,
the script accepts optional navigation fields:

- `OLDER_POST_LINK` – URL of the previous post
- `OLDER_POST_TITLE` – Title of the previous post
- `NEWER_POST_LINK` – URL of the next post
- `NEWER_POST_TITLE` – Title of the next post

Include these keys in `content.json` when you want navigation links populated.
If they are omitted, empty strings are used.

See `post-generator/content template.json` for a sample configuration.

