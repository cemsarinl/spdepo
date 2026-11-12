# Instagram Graph API reference

Meta changes versions, metrics and limits often. When something here conflicts with an API error, trust the error and check the current docs at developers.facebook.com/docs/instagram-platform.

## Setup

1. Convert the Instagram account to **Business** or **Creator**.
2. Create a Meta app at developers.facebook.com and add the **Instagram** product. Choose one of:
   - **Instagram API with Instagram Login**: host `graph.instagram.com`, no Facebook Page needed.
   - **Instagram API with Facebook Login**: host `graph.facebook.com`, with the IG account linked to a Facebook Page.
3. Request permissions.
   - Instagram Login: `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_comments`, `instagram_business_manage_insights`.
   - Facebook Login: `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement`.
4. Get a **long-lived token**, valid for about 60 days and refreshable. Store it as `IG_ACCESS_TOKEN`. Get the IG user ID from `GET /me?fields=user_id,username` (Instagram Login) or from `GET /{page-id}?fields=instagram_business_account` (Facebook Login), and store it as `IG_USER_ID`.

## Publishing flow (two steps)

1. **Create a container**: `POST /{ig-user-id}/media` → returns `{id}`.
   - Image: `image_url`, `caption`, optional `alt_text`.
   - Reel: `media_type=REELS`, `video_url`, `caption`, optional `cover_url`, `thumb_offset`, `share_to_feed`.
   - Story: `media_type=STORIES` plus `image_url` or `video_url`.
   - Carousel item: `is_carousel_item=true` plus `image_url` or (`media_type=VIDEO`, `video_url`).
   - Carousel parent: `media_type=CAROUSEL`, `children=id1,id2,…`, `caption`.
2. **Poll until ready** (this matters for video): `GET /{container-id}?fields=status_code` until the result is `FINISHED`. Other values are `IN_PROGRESS`, `ERROR`, `EXPIRED` (containers expire after 24 h) and `PUBLISHED`.
3. **Publish**: `POST /{ig-user-id}/media_publish` with `creation_id` → returns the media ID.
4. **Permalink**: `GET /{media-id}?fields=permalink`.

The script `scripts/ig_api.py` runs this whole flow.

## Media requirements (summary)

- Images: JPEG only, max 8 MB, aspect ratio 4:5 to 1.91:1, width 320–1440 px.
- Reels: MP4/MOV, H.264/HEVC, AAC audio, 3 s–15 min, 9:16 recommended, max ~300 MB.
- Carousel: 2–10 items through the API. The app may allow more; check the current docs. Images and videos can be mixed.
- URLs must be public and HTTPS, and must not redirect to a login page.

## Limits

- **Publishing**: 100 API-published posts per rolling 24 h per account. A carousel counts as 1. Check with `GET /{ig-user-id}/content_publishing_limit?fields=config,quota_usage`.
- **Caption**: 2,200 characters, ≤30 hashtags, ≤20 @mentions.
- **Rate limit**: Business Use Case limits apply. When throttled, back off for minutes, not seconds.

## Insights

- Media: `GET /{media-id}/insights?metric=…`. Common metrics are `reach`, `views`, `likes`, `comments`, `shares`, `saved` and `total_interactions`. Reels also have `ig_reels_avg_watch_time`. `impressions`/`plays` are deprecated in favour of `views`. If a metric errors, drop it and retry.
- Account: `GET /{ig-user-id}/insights?metric=reach,views,accounts_engaged,total_interactions&period=day&metric_type=total_value`.
- Data comes with some delay, and accounts with <100 followers may get no demographic data.

## Comments

- List: `GET /{media-id}/comments?fields=id,text,username,timestamp,like_count,replies{id,text,username}`.
- Reply: `POST /{comment-id}/replies` with `message`.
- Hide/unhide: `POST /{comment-id}` with `hide=true|false`.
- Delete: `DELETE /{comment-id}`. Only do this when the user explicitly asks.

## Common errors

| code / subcode | Meaning | Fix |
|---|---|---|
| 190 | Token invalid/expired | Refresh or regenerate the long-lived token |
| 10 / 200 | Missing permission | Add the scope and re-authorise; the app may need App Review |
| 4, 17, 32, 613 | Rate limited | Wait and reduce frequency |
| 9 / 2207042 | Publishing limit reached | Check `quota`; wait for the 24 h window |
| 36003 / 2207009 | Bad aspect ratio | Crop to within 4:5–1.91:1 |
| 9004 / 2207052 | Media URL not fetchable | Use a public HTTPS URL; no auth or redirect |
| 2207026 | Unsupported video format | Re-encode to H.264 + AAC MP4 |
| 2207027 | Container not ready | Keep polling `status_code` |
| 24 / 2207006 | Media/container not found or expired | Recreate the container |
