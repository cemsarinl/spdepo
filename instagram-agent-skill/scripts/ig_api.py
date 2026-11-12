#!/usr/bin/env python3
"""Minimal Instagram Graph API istemcisi (yalnızca standart kütüphane).

Ortam değişkenleri:
  IG_ACCESS_TOKEN  uzun ömürlü erişim token'ı (bulut oturumunda proxy ekliyorsa gerekmez)
  IG_USER_ID       Instagram profesyonel hesap ID'si (graph.instagram.com'da /me ile otomatik bulunur)
  IG_GRAPH_HOST    graph.facebook.com (varsayılan, Facebook Login) veya graph.instagram.com (Instagram Login)
  IG_API_VERSION   varsayılan v23.0

Yazma komutları (publish-*, reply, hide-comment) --yes verilmedikçe deneme çalıştırmasıdır.
Seçenekler için herhangi bir alt komutu -h ile çalıştır.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = os.environ.get("IG_GRAPH_HOST", "graph.facebook.com")
VERSION = os.environ.get("IG_API_VERSION", "v23.0")
BASE = f"https://{HOST}/{VERSION}"


class ApiError(Exception):
    pass


def _token():
    # Token yoksa istek token'sız gönderilir; bulut oturumlarında ağ proxy'si
    # kayıtlı kimlik bilgisini Authorization başlığı olarak kendisi ekler.
    return os.environ.get("IG_ACCESS_TOKEN")


_UID = None


def _user_id():
    global _UID
    if _UID:
        return _UID
    _UID = os.environ.get("IG_USER_ID")
    if not _UID and HOST == "graph.instagram.com":
        _UID = str(call("GET", "me", {"fields": "user_id"})["user_id"])
    if not _UID:
        sys.exit("IG_USER_ID ayarlanmamış.")
    return _UID


def call(method, path, params=None):
    params = dict(params or {})
    if _token():
        params["access_token"] = _token()
    data = None
    url = f"{BASE}/{path.lstrip('/')}"
    encoded = urllib.parse.urlencode(params)
    if method == "GET":
        url += "?" + encoded
    else:
        data = encoded.encode()
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            err = json.loads(body).get("error", {})
        except ValueError:
            err = {"message": body[:500]}
        raise ApiError(
            f"HTTP {e.code} code={err.get('code')} subcode={err.get('error_subcode')}: "
            f"{err.get('error_user_msg') or err.get('message')}"
        ) from None


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def read_caption(a):
    if getattr(a, "caption_file", None):
        with open(a.caption_file, encoding="utf-8") as f:
            return f.read().rstrip("\n")
    return getattr(a, "caption", None) or ""


def wait_ready(container_id, timeout=600, interval=5):
    deadline = time.time() + timeout
    while True:
        st = call("GET", container_id, {"fields": "status_code,status"})
        code = st.get("status_code")
        if code in ("FINISHED", "PUBLISHED"):
            return
        if code in ("ERROR", "EXPIRED"):
            raise ApiError(f"Container {container_id} durumu {code}: {st.get('status')}")
        if time.time() > deadline:
            raise ApiError(f"Container {container_id} beklenirken zaman aşımı (son durum {code}).")
        time.sleep(interval)


def create_and_publish(a, params, children=None):
    uid = _user_id()
    plan = {"endpoint": f"POST /{uid}/media", "params": params}
    if children:
        plan["children"] = children
    if not a.yes:
        print("DENEME ÇALIŞTIRMASI (yayınlamak için --yes ekle):")
        out(plan)
        return
    if children:
        ids = []
        for child in children:
            c = call("POST", f"{uid}/media", child)
            wait_ready(c["id"])
            ids.append(c["id"])
        params = dict(params, children=",".join(ids))
    container = call("POST", f"{uid}/media", params)
    wait_ready(container["id"])
    pub = call("POST", f"{uid}/media_publish", {"creation_id": container["id"]})
    info = call("GET", pub["id"], {"fields": "id,permalink,media_type,timestamp"})
    out(info)


# ---- commands ----

def cmd_whoami(a):
    out(call("GET", _user_id(), {"fields": "id,username,name,followers_count,media_count"}))


def cmd_quota(a):
    out(call("GET", f"{_user_id()}/content_publishing_limit", {"fields": "config,quota_usage"}))


def cmd_publish_image(a):
    p = {"image_url": a.image_url, "caption": read_caption(a)}
    if a.alt_text:
        p["alt_text"] = a.alt_text
    create_and_publish(a, p)


def _child(url):
    path = urllib.parse.urlparse(url).path.lower()
    if path.endswith((".mp4", ".mov")):
        return {"is_carousel_item": "true", "media_type": "VIDEO", "video_url": url}
    return {"is_carousel_item": "true", "image_url": url}


def cmd_publish_carousel(a):
    if not 2 <= len(a.media_url) <= 10:
        sys.exit("Carousel için 2-10 öğe gerekir.")
    create_and_publish(a, {"media_type": "CAROUSEL", "caption": read_caption(a)},
                       children=[_child(u) for u in a.media_url])


def cmd_publish_reel(a):
    p = {"media_type": "REELS", "video_url": a.video_url, "caption": read_caption(a),
         "share_to_feed": "false" if a.no_feed else "true"}
    if a.cover_url:
        p["cover_url"] = a.cover_url
    create_and_publish(a, p)


def cmd_publish_story(a):
    if bool(a.image_url) == bool(a.video_url):
        sys.exit("--image-url veya --video-url seçeneklerinden yalnızca birini ver.")
    p = {"media_type": "STORIES"}
    p["image_url" if a.image_url else "video_url"] = a.image_url or a.video_url
    create_and_publish(a, p)


def cmd_media(a):
    out(call("GET", f"{_user_id()}/media", {
        "fields": "id,caption,media_type,permalink,timestamp,like_count,comments_count",
        "limit": a.limit}))


MEDIA_METRICS = ["reach", "views", "likes", "comments", "shares", "saved", "total_interactions"]


def cmd_insights(a):
    metrics = a.metric or MEDIA_METRICS
    # Medya türünün desteklemediği metrikleri tek tek çıkar.
    while metrics:
        try:
            out(call("GET", f"{a.media_id}/insights", {"metric": ",".join(metrics)}))
            return
        except ApiError as e:
            bad = next((m for m in metrics if m in str(e)), None)
            if not bad:
                raise
            print(f"not: '{bad}' metriği burada desteklenmiyor, onsuz tekrar deneniyor", file=sys.stderr)
            metrics = [m for m in metrics if m != bad]
    sys.exit("Desteklenen metrik yok.")


def cmd_account_insights(a):
    out(call("GET", f"{_user_id()}/insights", {
        "metric": ",".join(a.metric or ["reach", "views", "accounts_engaged", "total_interactions"]),
        "period": a.period, "metric_type": "total_value"}))


def cmd_comments(a):
    out(call("GET", f"{a.media_id}/comments", {
        "fields": "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}",
        "limit": a.limit}))


def cmd_reply(a):
    if not a.yes:
        print("DENEME ÇALIŞTIRMASI (göndermek için --yes ekle):")
        out({"endpoint": f"POST /{a.comment_id}/replies", "message": a.message})
        return
    out(call("POST", f"{a.comment_id}/replies", {"message": a.message}))


def cmd_hide_comment(a):
    hide = "false" if a.unhide else "true"
    if not a.yes:
        print("DENEME ÇALIŞTIRMASI (uygulamak için --yes ekle):")
        out({"endpoint": f"POST /{a.comment_id}", "hide": hide})
        return
    out(call("POST", a.comment_id, {"hide": hide}))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, fn, write=False, caption=False):
        s = sub.add_parser(name)
        s.set_defaults(fn=fn)
        if write:
            s.add_argument("--yes", action="store_true", help="Yazma işlemini gerçekten yap")
        if caption:
            g = s.add_mutually_exclusive_group()
            g.add_argument("--caption")
            g.add_argument("--caption-file")
        return s

    add("whoami", cmd_whoami)
    add("quota", cmd_quota)
    s = add("publish-image", cmd_publish_image, True, True)
    s.add_argument("--image-url", required=True)
    s.add_argument("--alt-text")
    s = add("publish-carousel", cmd_publish_carousel, True, True)
    s.add_argument("--media-url", action="append", required=True, help="2-10 kez tekrarla")
    s = add("publish-reel", cmd_publish_reel, True, True)
    s.add_argument("--video-url", required=True)
    s.add_argument("--cover-url")
    s.add_argument("--no-feed", action="store_true", help="Yalnızca Reels sekmesi, ana akışta değil")
    s = add("publish-story", cmd_publish_story, True)
    s.add_argument("--image-url")
    s.add_argument("--video-url")
    s = add("media", cmd_media)
    s.add_argument("--limit", type=int, default=10)
    s = add("insights", cmd_insights)
    s.add_argument("--media-id", required=True)
    s.add_argument("--metric", action="append")
    s = add("account-insights", cmd_account_insights)
    s.add_argument("--period", default="day")
    s.add_argument("--metric", action="append")
    s = add("comments", cmd_comments)
    s.add_argument("--media-id", required=True)
    s.add_argument("--limit", type=int, default=50)
    s = add("reply", cmd_reply, True)
    s.add_argument("--comment-id", required=True)
    s.add_argument("--message", required=True)
    s = add("hide-comment", cmd_hide_comment, True)
    s.add_argument("--comment-id", required=True)
    s.add_argument("--unhide", action="store_true")

    a = p.parse_args()
    try:
        a.fn(a)
    except ApiError as e:
        sys.exit(f"API hatası: {e}\nreferences/graph-api.md içindeki 'Yaygın hatalar' bölümüne bak.")


if __name__ == "__main__":
    main()
