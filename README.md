# ACT Protocols Search (Vercel-ready)

A minimal Next.js + Tailwind app that searches your ACT medical protocols index locally in the browser and links into the PDF by page.

## Quick Start

1. **Place your files:**
   - Put your **index JSON** at `public/act_protocol_index.json` (already included here).
   - Put your **PDF** at `public/protocols.pdf` (rename this to match your real file if desired).

2. **Install & run**
```bash
npm i
npm run dev
```
Open http://localhost:3000

3. **Deploy to Vercel**
- Push to GitHub and import the repo in Vercel. No special config needed.

### Building / Updating the Index

Use the included Python script to build `act_protocol_index.json` from your PDF (run **locally**, then commit the JSON).

```bash
# requires: pip install PyPDF2
python tools/build_index.py "YOUR.pdf" --out public/act_protocol_index.json
```

### Notes

- Client-side search is privacy-friendly and fast. It uses a lightweight tokenizer and title-weighted scoring.
- The **Open PDF** link uses the `#page=NN` hash to jump to the first page of a protocol. Most browsers support this.
- To rename the PDF file, update links in `app/page.tsx` (`%PDF_NAME%`) or keep the default `protocols.pdf`.

### Roadmap to iOS App (SwiftUI)

- Reuse the same `act_protocol_index.json` schema in the app bundle.
- Build a small search view with tokenization + scoring similar to the web version.
- Optional: Pull JSON from a URL (this site) for over-the-air updates.

See `ios/SwiftUI-Snippet.md` for a starter view.

