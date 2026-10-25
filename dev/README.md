# Slap Cards — dev tools
- Game: `index.html` (single file, 1280x720 stage, save key `lyap_v5`). Assets: `a/` cards, frames, backs; `y/` yard; `u/` UI art.
- i18n: add rows to `dev/i18n/tr_XX.tsv` (key + en es pt de fr pl cs tr id hi), then in `dev/i18n`: `python3 merge.py && python3 inject.py` (rewrites block between /*I18N_START*/ and /*I18N_END*/ in index.html).
- Tests (Playwright): serve repo root with `python3 -m http.server 8765`, then `node dev/tests/t6.js en`, `t7.js en` (crawl + untranslated text), `t10.js` (record revive), `ty.js` (yard).
- Balance sim: `dev/sim/`.
- When changing assets, bump cache version `sc-vN` in `sw.js` and add new files to its list.
