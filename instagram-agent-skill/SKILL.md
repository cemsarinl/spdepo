---
name: instagram
description: Plan, write, check and publish Instagram content for a Business or Creator account. Use when the user wants Instagram captions, hashtags, carousel or Reel scripts, a content calendar, a caption checked against Instagram's limits, a post/carousel/Reel/Story published through the Instagram Graph API, post or account insights pulled, or comments read and replied to. Not for scraping other people's accounts, buying followers or engagement, or automating likes/follows/DMs.
---

# Instagram

This skill helps with two kinds of work:

1. **Content**: writing captions, hashtags, carousels, Reel scripts, Stories and content calendars.
2. **Operations**: publishing, insights and comments through the official **Instagram Graph API** (`scripts/ig_api.py`).

Start with whatever the user asked for. Bring in the API side only when they want something published, measured or moderated.

## 1. Gather the brief (only what is missing)

- **Account**: niche, audience, brand voice. Ask for 2–3 past captions they liked.
- **Goal of the post**: reach, saves, comments, link clicks, sales or community.
- **Format**: single image, carousel, Reel or Story.
- **Must-haves**: CTA, product, offer, @mentions, location, language(s).

If the user gives a one-liner ("caption for my latitude coffee launch"), don't interrogate them. Make sensible assumptions, state them in one line, and deliver.

## 2. Write the content

Follow `references/content-guide.md`. It covers hook formulas, caption structure, format playbooks, hashtag strategy and the calendar template. The core rules:

- The **first ~125 characters** show before "…more", so the hook goes there.
- One post, one idea, one CTA.
- Write for the format: on-screen text and a spoken script for Reels, a slide-by-slide outline for carousels.
- Offer **2–3 variants** of the hook or caption when tone is uncertain.
- Add **alt text** for every image.

Before handing over a caption, run the checker:

```bash
python3 scripts/caption_check.py --file caption.txt        # or: echo "..." | python3 scripts/caption_check.py
```

It reports length (hard cap 2,200 chars), hashtag and @mention counts, duplicate tags, banned characters and how much of the hook is visible above the fold. Fix every **ERROR**. Mention any **WARN** to the user.

## 3. Publish / measure / moderate (Graph API)

Read `references/graph-api.md` first. It covers setup, permissions, media requirements, rate limits and errors.

Requirements: an Instagram **Business or Creator** account and environment variables `IG_ACCESS_TOKEN` and `IG_USER_ID`. Optionally set `IG_GRAPH_HOST`: `graph.facebook.com` (the default, for Facebook Login) or `graph.instagram.com` (for Instagram Login). Optionally set `IG_API_VERSION`. **Never print, log or commit the token.**

```bash
python3 scripts/ig_api.py whoami
python3 scripts/ig_api.py quota
python3 scripts/ig_api.py publish-image    --image-url URL --caption-file caption.txt [--alt-text "..."] --yes
python3 scripts/ig_api.py publish-carousel --media-url URL1 --media-url URL2 ... --caption-file caption.txt --yes
python3 scripts/ig_api.py publish-reel     --video-url URL --caption-file caption.txt [--cover-url URL] [--no-feed] --yes
python3 scripts/ig_api.py publish-story    --image-url URL | --video-url URL --yes
python3 scripts/ig_api.py media  [--limit 10]
python3 scripts/ig_api.py insights --media-id ID
python3 scripts/ig_api.py account-insights [--period day]
python3 scripts/ig_api.py comments --media-id ID
python3 scripts/ig_api.py reply --comment-id ID --message "..." --yes
python3 scripts/ig_api.py hide-comment --comment-id ID [--unhide] --yes
```

Without `--yes`, every write command does a **dry run**: it prints what it would send and stops. Follow these rules:

- **Always** show the user the final caption and media list, and get explicit approval, before running a write command with `--yes`. A published post is public at once.
- Media must be at a **public HTTPS URL** that Meta's servers can fetch. Local files must be uploaded somewhere first.
- Check `quota` before batch publishing.
- On an error, read the `code`/`error_subcode` and see the error table in `references/graph-api.md`. Don't retry blindly.

## 4. Report back

- For content: give the final caption in a copyable block, then hashtags, alt text and any checker warnings.
- For publishing: give the permalink and media ID.
- For insights: show a small table, then 2–3 concrete takeaways tied to the post's goal.

## Out of scope

Don't do the following, even if asked: scrape other people's profiles or follower lists, automate likes/follows/DMs, buy engagement, get around rate limits or log in with a user's password. These violate Instagram's Terms and get accounts banned. Offer the compliant alternative instead, such as the Graph API, Business Discovery for public business-account data, or organic tactics.
