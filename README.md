# Instagram Agent Skill

A [Claude Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for planning, writing, checking and publishing Instagram content. It uses the official Instagram Graph API.

```
instagram-agent-skill/
├── SKILL.md                     # entry point: when and how Claude uses the skill
├── references/
│   ├── content-guide.md         # hooks, caption structure, format playbooks, hashtags, calendar
│   └── graph-api.md             # setup, publishing flow, limits, insights, error table
└── scripts/
    ├── caption_check.py         # caption linter (length, hashtags, mentions, fold, spam tags)
    └── ig_api.py                # Graph API CLI: publish, insights, comments (stdlib only)
```

## Install

- **Claude Code**: copy `instagram-agent-skill/` to `~/.claude/skills/instagram/` (personal) or `.claude/skills/instagram/` (project).
- **Claude.ai / Desktop**: zip the `instagram-agent-skill` folder and upload it under Settings → Capabilities → Skills.
- **Claude API / Agent SDK**: upload it as a custom skill.

## Configure (only needed for publishing, insights and comments)

```bash
export IG_ACCESS_TOKEN=...        # long-lived token; never commit it
export IG_USER_ID=...             # Instagram professional account ID
export IG_GRAPH_HOST=graph.instagram.com   # if using "Instagram Login"; default graph.facebook.com
```

See `instagram-agent-skill/references/graph-api.md` for app setup and permissions.

## Example prompts

- "Write 3 caption options for our new oat-milk latte launch, playful tone, goal = saves."
- "Turn this blog post into a 7-slide carousel outline with alt text."
- "Script a 20-second Reel showing our packing process."
- "Check this caption against Instagram's limits."
- "Publish this carousel with these image URLs." (Claude shows a dry run first, then publishes only after you approve.)
- "How did my last 5 posts perform? What should I post more of?"

## Safety

Every write command is a dry run unless `--yes` is passed. Claude is instructed to get your approval before publishing or replying. The skill refuses to scrape, automate follows/likes/DMs, or use password logins.
