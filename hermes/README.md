# VANTAGE — Hermes deploy files

Add this folder to a **hermes-deploy** project (Hermes Agent on a VPS), not to the static website zip.

## Files

| File | Purpose |
|------|---------|
| `hermes.toml` | Deployment config (cloud, region, file paths) |
| `config.yaml` | Agent runtime — Google Gemini provider |
| `SOUL.md` | Agent personality and VANTAGE product knowledge |

## Setup (one time)

```bash
cd /path/to/your/hermes-project
# Copy these three files into the project root (or point hermes.toml at them)

hermes-deploy init   # only if you don't have .sops.yaml + secrets.env.enc yet
# Merge or replace with the files from this folder

hermes-deploy secret set GEMINI_API_KEY YOUR_KEY_HERE
hermes-deploy up
```

Use `GOOGLE_API_KEY` instead of `GEMINI_API_KEY` if you prefer — Hermes accepts both for the `gemini` provider.

## Static website (separate)

To host the **marketing site** (`index.html`, `styles.css`, etc.), upload the parent folder `vantage-website/` to static hosting — that does not use `hermes.toml`.

## Security

Never commit API keys. Use `hermes-deploy secret set` only. Rotate any key that was pasted in chat or email.
