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
