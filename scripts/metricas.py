#!/usr/bin/env python3
"""Coleta métricas do @anotajuros (somente leitura) e salva em dados/metricas.json.

Usado pela criação diária de conteúdo para aprender o que funciona melhor.
"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

IG_ID = "17841415330772972"
GRAPH = "https://graph.facebook.com/v25.0/"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(caminho, params, token):
    q = urllib.parse.urlencode({**params, "access_token": token})
    try:
        with urllib.request.urlopen(f"{GRAPH}{caminho}?{q}", timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError:
        return {}


def insights(mid, metricas, token):
    out = {}
    for m in metricas:  # uma por vez: métricas indisponíveis não derrubam as outras
        d = get(f"{mid}/insights", {"metric": m}, token).get("data") or []
        if d and d[0].get("values"):
            out[m] = d[0]["values"][0].get("value")
    return out


def main():
    token = os.environ.get("IG_TOKEN", "").strip()
    if not token:
        print("IG_TOKEN ausente.")
        return 1
    perfil = get(IG_ID, {"fields": "username,followers_count,follows_count,media_count"}, token)
    midias = get(f"{IG_ID}/media", {"fields": "id,caption,media_type,media_product_type,timestamp,like_count,comments_count,permalink", "limit": "30"}, token).get("data", [])
    for m in midias:
        m["caption"] = (m.get("caption") or "")[:160]
        m["insights"] = insights(m["id"], ["reach", "views", "saved", "shares", "total_interactions"], token)
    stories = get(f"{IG_ID}/stories", {"fields": "id,timestamp"}, token).get("data", [])
    for s in stories:
        s["insights"] = insights(s["id"], ["reach", "views", "replies", "navigation"], token)
    saida = {
        "coletado_em": dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).isoformat(),
        "perfil": {k: perfil.get(k) for k in ("username", "followers_count", "follows_count", "media_count")},
        "posts": midias,
        "stories_ativos": stories,
    }
    os.makedirs(os.path.join(RAIZ, "dados"), exist_ok=True)
    with open(os.path.join(RAIZ, "dados", "metricas.json"), "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)
    hist = os.path.join(RAIZ, "dados", "seguidores.jsonl")
    with open(hist, "a", encoding="utf-8") as f:
        f.write(json.dumps({"em": saida["coletado_em"], "seguidores": perfil.get("followers_count")}) + "\n")
    print(f"Métricas salvas: {len(midias)} posts, {len(stories)} stories ativos, {perfil.get('followers_count')} seguidores.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
