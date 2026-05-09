'use client';
import { useState } from 'react';

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testGate = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/gate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sigma: 0.85,
          ai_influence: 0.04,
          metadata: {
            provenance_chain: ['UI_ROOT'],
            owner_key: 'Krimerra13',
            consent_state: 'EXPLICIT',
            human_override: true
          }
        })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 p-8 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-8">ISLAH NEXUS: Sovereign Workspace</h1>
      
      <button 
        onClick={testGate}
        disabled={loading}
        className="px-6 py-3 bg-zinc-800 hover:bg-zinc-700 rounded-md border border-zinc-700 transition-colors disabled:opacity-50"
      >
        {loading ? 'Processing Sovereign Logic...' : 'Trigger ChiefOmega Gate'}
      </button>

      {result && (
        <div className="mt-8 p-6 bg-zinc-900 border border-zinc-800 rounded-lg w-full max-w-2xl">
          <h2 className="text-xl font-semibold mb-4 text-emerald-400">Gate Response</h2>
          <pre className="text-sm text-zinc-300 whitespace-pre-wrap font-mono">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}
