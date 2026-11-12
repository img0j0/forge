# Japanese (and later other languages)

The English build (`work.html`, from the patches) stays the source. `build.mjs` makes the shipped app from it:

```
cd i18n && npm install        # once (acorn)
node scan.mjs ../work.html    # what still needs Japanese: i18n/todo/<area>.json
node build.mjs ../work.html ../app.html
```

- `ja/*.json`: English unit -> Japanese. A unit is a whole string or a whole template; `{0}`, `{1}`... stand for the
  template's `${...}` parts, in any order in the Japanese. Markup and attribute values must match the English (text
  attributes such as aria-label may be translated). A single word is only translated where its key names its place:
  `day@renderToday`.
- The build refuses anything that would break the page (`problems.json`): placeholders or markup that differ, and
  sentences the code also compares or looks up.
- The app runs in Japanese when the phone's language is Japanese, or when Settings saves `forge-lang`.
- `GLOSSARY.md`: the terms. Keep them consistent.

## Shipping (0.57)
- `pwa.py` runs the build and packs `app.html`, so the website, the iPhone/Android source (`ios-app/forgelings.html`),
  the Claude page and the project copy all get `app.html`, never `work.html` alone.
- The phone's language picks the language; Settings > Look and feel > Language (English / 日本語) overrides it. The
  iPhone app lists `ja` in `CFBundleLocalizations` so the web view reports Japanese on a Japanese iPhone.
- New English text in a patch: run `node scan.mjs ../work.html` and add Japanese for everything in `todo/` that people
  read (dev tools, the pilot report, name syllables and code stay English). Write new sentences as whole templates,
  never glued from pieces (`'Found '+w+x` cannot be put in Japanese order).
- `units.mjs` `FORCE` lists text the detector misses (only punctuation or numbers around placeholders).
- Words that differ by place are keyed by area (`Calm@cardHTML` a stat, `Calm@WANTS` a wish); the build keeps them apart.
- Card backs' news from away is stored as an event (`c.gev`), so it shows in the app's current language.
- Size: the Japanese adds about 190 K characters (about 0.2 MB as UTF-8); the app is about 1.2 MB. A native speaker
  should review the Japanese before a Japanese launch.
- Forgeling names (0.57.1): in Japanese a name reads in katakana from its two syllables (`KANA_P`, `KANA_S`); a new
  syllable in `PRE`/`SUF` needs its reading there. The save keeps the Latin name (`jaName`, a card's `toJSON`).
- After a patch, `node scan.mjs ../work.html` must print no "match nothing" or "untranslated markup" warning: a changed English
  template loses its Japanese, so carry the Japanese over to the new key (renumber its placeholders).
