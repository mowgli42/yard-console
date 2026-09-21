.pragma library

function formatTokens(count) {
  var n = Number(count || 0);
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  if (n >= 1e3) return (n / 1e3).toFixed(1) + "K";
  return String(n);
}

function parseStatus(rawText) {
  try {
    return JSON.parse(rawText);
  } catch (e) {
    return null;
  }
}
