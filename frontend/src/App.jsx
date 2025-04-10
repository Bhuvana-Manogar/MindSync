
import React, { useState } from 'react';

export default function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [url, setUrl] = useState('');
  const [scraped, setScraped] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:5000/mindsync/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  const handleScrape = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:5000/mindsync/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    setScraped(data);
    setLoading(false);
  };

  return (
    <div className="p-4 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-center">🧠 MindSync Research Assistant</h1>

      <div className="space-y-2">
        <input
          className="border p-2 w-full"
          placeholder="Enter your research query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleQuery} disabled={loading} className="bg-blue-500 px-4 py-2 text-white rounded">
          {loading ? 'Processing...' : 'Run MindSync'}
        </button>
      </div>

      {result && (
        <pre className="bg-gray-100 p-4 rounded overflow-x-auto">{JSON.stringify(result, null, 2)}</pre>
      )}

      <div className="space-y-2">
        <input
          className="border p-2 w-full"
          placeholder="Paste URL to scrape..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={handleScrape} disabled={loading} className="bg-green-500 px-4 py-2 text-white rounded">
          {loading ? 'Scraping...' : 'Scrape Website'}
        </button>
      </div>

      {scraped && (
        <pre className="bg-gray-100 p-4 rounded overflow-x-auto">{JSON.stringify(scraped.data, null, 2)}</pre>
      )}
    </div>
  );
}
