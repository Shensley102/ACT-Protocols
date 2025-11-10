const visible = useMemo(() => {
  const terms = tokenize(q);
  let rows = protocols;
  if (activeCats.length > 0) {
    rows = rows.filter((r) => activeCats.includes(r.category));
  }
  if (terms.length === 0) {
    return rows
      .slice()
      .sort((a, b) => {
        if (a.category !== b.category) return a.category.localeCompare(b.category);
        return a.start_page - b.start_page;
      })
      .slice(0, 50);
  }

  const scored: { s: number; r: Protocol }[] = [];
  for (const r of rows) {
    const s = scoreDoc(terms, r);
    if (s > 0) {
      scored.push({ s, r }); // <-- the fix
    }
  }
  scored.sort((a, b) => b.s - a.s || a.r.start_page - b.r.start_page);
  return scored.slice(0, 50).map((x) => x.r);
}, [q, protocols, activeCats]);
