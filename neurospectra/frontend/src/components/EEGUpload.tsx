import { useState } from 'react'
import { uploadEEG } from '../services/api'

export default function EEGUpload({ onScore }: { onScore: (p: number) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [prob, setProb] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  const submit = async () => {
    if (!file) return
    setLoading(true)
    try {
      const res = await uploadEEG(file)
      setProb(res.probability)
      onScore(res.probability)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
      <h3>EEG Upload</h3>
      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <button onClick={submit} disabled={!file || loading} style={{ marginLeft: 8 }}>
        {loading ? 'Analyzing…' : 'Analyze EEG'}
      </button>
      {prob !== null && <p>EEG risk score: {prob.toFixed(2)}</p>}
    </div>
  )
}

