#!/usr/bin/env python3
"""Publica no Instagram @anotajuros a peça do horário atual (horário de Brasília).

Fila: fila/AAAA-MM-DD/HHMM-<feed|story>.jpg + .json ({"tipo": "feed"|"story", "legenda": "..."}).
Horários: 08:00 e 19:00 (feed, todos os dias). 13:00 e 16:00 são opcionais (só publicam se houver peça).

Regras de segurança:
- Publica SOMENTE na conta @anotajuros (ID fixo); confere o @ antes de publicar.
- Nunca publica a mesma peça duas vezes (registro/publicados.jsonl).
- Nunca apaga nem edita publicações.
- O token vem só do segredo IG_TOKEN e nunca é impresso.
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

IG_ID = "17841415330772972"
IG_USUARIO = "anotajuros"
GRAPH = "https://graph.facebook.com/v25.0/"
HORARIOS = ["0800", "1300", "1600", "1900"]
JANELA_ANTES_MIN = 10   # aceita rodar até 10 min antes do horário
JANELA_DEPOIS_MIN = 150  # e até 2h30 depois (atrasos do agendador do GitHub)
BRT = dt.timezone(dt.timedelta(hours=-3))
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RAIZ, "registro", "publicados.jsonl")


def chamar(metodo, caminho, dados=None, token=""):
    params = dict(dados or {})
    params["access_token"] = token
    corpo = urllib.parse.urlencode(params).encode()
    url = GRAPH + caminho
    if metodo == "GET":
        req = urllib.request.Request(url + "?" + corpo.decode(), method="GET")
    else:
        req = urllib.request.Request(url, data=corpo, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            erro = json.loads(e.read().decode()).get("error", {})
        except Exception:
            erro = {}
        msg = str(erro.get("message", f"HTTP {e.code}")).replace(token, "[token]") if token else str(erro.get("message"))
        raise RuntimeError(f"Meta recusou ({erro.get('code')}): {msg}") from None


def ja_publicados():
    if not os.path.exists(REGISTRO):
        return set()
    with open(REGISTRO, encoding="utf-8") as f:
        return {json.loads(l)["peca"] for l in f if l.strip() and json.loads(l).get("status") == "publicado"}


def registrar(item):
    os.makedirs(os.path.dirname(REGISTRO), exist_ok=True)
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def escolher_horario(agora, forcado):
    if forcado:
        return forcado
    # Do mais recente para o mais antigo: as janelas se sobrepõem (ex.: 10h05 cabe na de 08h e na de 10h).
    for h in reversed(HORARIOS):
        alvo = agora.replace(hour=int(h[:2]), minute=int(h[2:]), second=0, microsecond=0)
        delta = (agora - alvo).total_seconds() / 60
        if -JANELA_ANTES_MIN <= delta <= JANELA_DEPOIS_MIN:
            return h
    return None


def main():
    token = os.environ.get("IG_TOKEN", "").strip()
    if not token:
        print("Segredo IG_TOKEN não configurado; nada publicado.")
        return 1
    agora = dt.datetime.now(BRT)
    dia = os.environ.get("DIA_FORCADO") or agora.strftime("%Y-%m-%d")
    horario = escolher_horario(agora, os.environ.get("HORARIO_FORCADO", "").strip())
    if not horario:
        print(f"{agora:%H:%M} não está na janela de nenhum horário; nada a fazer.")
        return 0
    pasta = os.path.join(RAIZ, "fila", dia)
    meta = next((os.path.join(pasta, n) for n in sorted(os.listdir(pasta)) if n.startswith(horario) and n.endswith(".json")), None) if os.path.isdir(pasta) else None
    if not meta:
        print(f"Sem peça na fila para {dia} {horario}.")
        if horario in ("0800", "1900"):  # 13h e 16h são opcionais; nos fixos, registra a falta para o aviso diário
            registrar({"peca": f"{dia}/{horario}", "status": "sem_peca", "em": agora.isoformat()})
        return 0
    peca = f"{dia}/{os.path.basename(meta)[:-5]}"
    if peca in ja_publicados():
        print(f"{peca} já foi publicada; não repito.")
        return 0
    with open(meta, encoding="utf-8") as f:
        info = json.load(f)
    imagem = meta[:-5] + ".jpg"
    if not os.path.exists(imagem):
        raise RuntimeError(f"Imagem ausente: {imagem}")
    tipo = info.get("tipo")
    if tipo not in ("feed", "story"):
        raise RuntimeError("Tipo inválido na fila.")

    conta = chamar("GET", IG_ID, {"fields": "username"}, token)
    if conta.get("username") != IG_USUARIO:
        raise RuntimeError("O token não corresponde ao @anotajuros; publicação bloqueada.")
    limite = chamar("GET", f"{IG_ID}/content_publishing_limit", {"fields": "quota_usage"}, token)
    uso = (limite.get("data") or [{}])[0].get("quota_usage", 0)
    if uso >= 40:
        raise RuntimeError(f"Uso diário da API alto ({uso}); publicação suspensa por segurança.")

    sha = os.environ.get("GITHUB_SHA") or "main"
    repo = os.environ.get("GITHUB_REPOSITORY", "edisonlevi2024-spec/anota-juros-instagram")
    rel = os.path.relpath(imagem, RAIZ).replace(os.sep, "/")
    url = f"https://raw.githubusercontent.com/{repo}/{sha}/{urllib.parse.quote(rel)}"

    dados = {"image_url": url}
    if tipo == "story":
        dados["media_type"] = "STORIES"
    else:
        dados["caption"] = info.get("legenda", "")[:2200]
    cont = chamar("POST", f"{IG_ID}/media", dados, token)
    cid = cont.get("id")
    if not cid:
        raise RuntimeError("A Meta não criou o contêiner da mídia.")
    status = ""
    for _ in range(20):
        status = chamar("GET", cid, {"fields": "status_code"}, token).get("status_code", "")
        if status in ("FINISHED", "ERROR", "EXPIRED"):
            break
        time.sleep(5)
    if status != "FINISHED":
        raise RuntimeError(f"Mídia não ficou pronta (status {status}).")
    pub = chamar("POST", f"{IG_ID}/media_publish", {"creation_id": cid}, token)
    mid = pub.get("id")
    if not mid:
        raise RuntimeError("A Meta não confirmou a publicação.")
    link = chamar("GET", mid, {"fields": "permalink,timestamp"}, token)
    registrar({"peca": peca, "status": "publicado", "tipo": tipo, "media_id": mid, "link": link.get("permalink"), "em": link.get("timestamp") or agora.isoformat(), "titulo": info.get("titulo", "")})
    print(f"Publicado {peca} ({tipo}): {link.get('permalink') or mid}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print(f"ERRO: {e}")
        sys.exit(1)
