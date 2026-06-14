const targetUrl = process.argv[2] ?? "http://127.0.0.1:4173/";
const expectedBasePath = process.argv[3] ?? "/";
const maxAttempts = Number(process.argv[4] ?? 20);

function normalizePath(path) {
  if (!path.startsWith("/")) {
    return `/${path}`;
  }
  return path;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithRetry(url) {
  let lastError;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        return response;
      }
      lastError = new Error(`HTTP ${response.status} for ${url}`);
    } catch (error) {
      lastError = error;
    }

    await sleep(500);
  }

  throw lastError;
}

function collectAssets(html) {
  const assets = [];
  const assetPattern = /\b(?:src|href)="([^"]+\.(?:js|css))"/g;
  let match = assetPattern.exec(html);

  while (match) {
    assets.push(match[1]);
    match = assetPattern.exec(html);
  }

  return assets;
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

const baseUrl = new URL(targetUrl);
const expectedPath = normalizePath(expectedBasePath);

console.log(`Checking deploy preview at ${baseUrl.toString()}`);
console.log(`Expected asset base path: ${expectedPath}`);

const indexResponse = await fetchWithRetry(baseUrl);
const html = await indexResponse.text();

assert(html.includes('<div id="root"></div>'), "index.html does not contain the React root node.");

const assets = collectAssets(html);
assert(assets.length > 0, "index.html does not reference any JS or CSS assets.");

for (const asset of assets) {
  const assetUrl = new URL(asset, baseUrl);
  assert(
    assetUrl.pathname.startsWith(expectedPath),
    `Asset ${assetUrl.pathname} is outside expected base path ${expectedPath}.`,
  );

  const assetResponse = await fetchWithRetry(assetUrl);
  console.log(`PASS ${assetResponse.status}: ${assetUrl.pathname}`);
}

console.log("Deploy smoke test passed.");
