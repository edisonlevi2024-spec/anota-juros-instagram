"""Verifica a conexão com o Instagram SEM publicar nada.
Mostra: se a chave é válida, quando expira, permissões e a conta conectada.
Nunca imprime a chave."""
import json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

GRAPH = "https://graph.facebook.com/v25.0/"
IG_ID = "17841415330772972"
IG_USUARIO = "anotajuros"
BRT = timezone(timedelta(hours=-3))


def get(caminho, params):
    url = GRAPH + caminho + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            erro = json.load(e).get("error", {})
        except Exception:
            erro = {}
        return {"_erro": f"{erro.get('code')} / {erro.get('error_subcode')}: {erro.get('message', 'erro')}"}


def main():
    token = (os.environ.get("IG_TOKEN") or "").strip()
    if not token:
        print("❌ Segredo IG_TOKEN vazio ou não encontrado.")
        return 1
    ok = True
    d = get("debug_token", {"input_token": token, "access_token": token}).get("data") or {}
    if d:
        exp = d.get("expires_at")
        expira = "nunca expira" if not exp else datetime.fromtimestamp(exp, BRT).strftime("%d/%m/%Y %H:%M")
        acesso = d.get("data_access_expires_at")
        acesso_txt = datetime.fromtimestamp(acesso, BRT).strftime("%d/%m/%Y") if acesso else "—"
        print(f"Chave válida: {'✅ sim' if d.get('is_valid') else '❌ não'}")
        print(f"Tipo: {d.get('type')}")
        print(f"Expira: {expira}")
        print(f"Acesso aos dados válido até: {acesso_txt}")
        print("Permissões: " + ", ".join(sorted(d.get("scopes", []))))
        ok = ok and bool(d.get("is_valid"))
        if "instagram_content_publish" not in d.get("scopes", []):
            print("❌ Falta a permissão instagram_content_publish.")
            ok = False
    else:
        print("⚠️ Não foi possível ler os detalhes da chave (debug_token).")
    conta = get(IG_ID, {"fields": "username,followers_count,media_count", "access_token": token})
    if "_erro" in conta:
        print(f"❌ Conta do Instagram: {conta['_erro']}")
        ok = False
    else:
        certo = conta.get("username") == IG_USUARIO
        print(f"Conta do Instagram: @{conta.get('username')} {'✅' if certo else '❌ (conta errada)'} · {conta.get('followers_count')} seguidores · {conta.get('media_count')} publicações")
        ok = ok and certo
    cota = get(f"{IG_ID}/content_publishing_limit", {"fields": "quota_usage,config", "access_token": token})
    if "_erro" not in cota and cota.get("data"):
        c = cota["data"][0]
        print(f"Publicações nas últimas 24h: {c.get('quota_usage')} de {c.get('config', {}).get('quota_total')}")
    print("RESULTADO: ✅ conexão OK (nada foi publicado)" if ok else "RESULTADO: ❌ verificar a chave")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
