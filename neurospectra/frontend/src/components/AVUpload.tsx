import { useState } from 'react'
import { uploadAV } from '../services/api'

export default function AVUpload({ onScore }: { onScore: (p: number) => void }) {
  const [audio, setAudio] = useState<File | null>(null)
  const [video, setVideo] = useState<File | null>(null)
  const [prob, setProb] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)

  const submit = async () => {
    if (!audio && !video) return
    setLoading(true)
    try {
      const res = await uploadAV(audio ?? undefined, video ?? undefined)
      setProb(res.probability)
      onScore(res.probability)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
      <h3>Audio/Video Upload</h3>
      <div>
        <input type="file" accept="audio/*" onChange={(e) => setAudio(e.target.files?.[0] ?? null)} />
      </div>
      <div style={{ marginTop: 8 }}>
        <input type="file" accept="video/*" onChange={(e) => setVideo(e.target.files?.[0] ?? null)} />
      </div>
      <button onClick={submit} disabled={(!audio && !video) || loading} style={{ marginTop: 8 }}>
        {loading ? 'Analyzing…' : 'Analyze A/V'}
      </button>
      {prob !== null && <p>A/V risk score: {prob.toFixed(2)}</p>}
    </div>
  )
}

