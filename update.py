#!/usr/bin/env python3
"""Fetch currently published hero stats and detect official patch-page changes.
Do not infer weapon damage from prose. Keep last valid data if the upstream API fails.
"""
import datetime as dt
import html
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT
API = 'https://overfast-api.tekrop.fr'
PATCH = 'https://overwatch.blizzard.com/en-us/news/patch-notes/'
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'OW2HeroGuide/1.0 (personal open source updater)', 'Accept': 'application/json,text/html'})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError):
        return default


def save_json(name, data):
    (DATA / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def heroes():
    raw = json.loads(fetch(API + '/heroes?locale=ja-jp'))
    if not isinstance(raw, list) or len(raw) < 40:
        raise ValueError('Unexpected hero list; refusing to replace valid data')
    old = read_json(DATA / 'heroes.json', {})
    by_key = {h['key']: h for h in old.get('heroes', []) if isinstance(h, dict) and h.get('key')}
    failures = []
    for item in raw:
        key = item.get('key')
        if not isinstance(key, str) or not re.fullmatch(r'[a-z0-9-]+', key):
            continue
        try:
            detail = json.loads(fetch(f'{API}/heroes/{key}?locale=ja-jp'))
            by_key[key] = {
                'key': key,
                'name': detail.get('name') or item.get('name') or key,
                'role': detail.get('role') or item.get('role'),
                'portrait': detail.get('portrait') or item.get('portrait'),
                'hitpoints': detail.get('hitpoints') or {},
                'abilities': [
                    {'name': a.get('name', ''), 'description': a.get('description', ''), 'icon': a.get('icon')}
                    for a in detail.get('abilities', []) if isinstance(a, dict)
                ]
            }
        except (OSError, ValueError, KeyError) as exc:
            failures.append(f'{key}: {exc}')
        time.sleep(0.35)
    if len(by_key) < 40:
        raise ValueError('Too few heroes after download; refusing to publish')
    save_json('heroes.json', {'updated': NOW, 'source': API, 'heroes': sorted(by_key.values(), key=lambda h: h['key']), 'partial_failures': failures})
    print(f'Heroes: {len(by_key)}; failures: {len(failures)}')


def patch():
    # Store the official patch URL and the most recent heading visible on its index.
    page = fetch(PATCH).decode('utf-8', 'replace')
    text = html.unescape(re.sub(r'<[^>]*>', ' ', page))
    text = re.sub(r'\s+', ' ', text)
    # Avoid presenting a guessed patch date or an unstable extracted article as confirmed.
    match = re.search(r'Overwatch Retail Patch Notes\s*[–-]\s*[^<]{4,55}', text)
    found = match.group(0).strip() if match else None
    old = read_json(DATA / 'patch.json', {})
    save_json('patch.json', {
        'checked': NOW,
        'latest': found,
        'url': PATCH,
        'note': '公式パッチノートを自動チェック済み。変更数値は要検証のため自動反映しません。',
        'changed_since_last_check': bool(found and old.get('latest') and old['latest'] != found)
    })
    print('Official patch notes checked')


if __name__ == '__main__':
    errors = []
    for step in (heroes, patch):
        try:
            step()
        except Exception as exc:
            errors.append(f'{step.__name__}: {exc}')
            print(f'ERROR: {errors[-1]}')
    if errors:
        raise SystemExit(' | '.join(errors))
