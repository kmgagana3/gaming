import { useMemo, useState } from 'react'
import { combinedPredict, getFeedback } from '../services/api'

type Props = {
  scores: { eeg?: number; av?: number; game?: number; combined?: number; feedback?: string }
  onScoresChange: (s: Props['scores']) => void
}

export default function Results({ scores, onScoresChange }: Props) {
  const canCombine = useMemo(() => scores.eeg != null && scores.av != null && scores.game != null, [scores])
  const [loading, setLoading] = useState(false)

  const combine = async () => {
    if (!canCombine) return
    setLoading(true)
    try {
      const res = await combinedPredict(scores.eeg!, scores.av!, scores.game!)
      const fb = await getFeedback(res.probability)
      onScoresChange({ ...scores, combined: res.probability, feedback: fb.feedback })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
      <h3>Results</h3>
      <ul>
        <li>EEG: {scores.eeg != null ? scores.eeg.toFixed(2) : '—'}</li>
        <li>A/V: {scores.av != null ? scores.av.toFixed(2) : '—'}</li>
        <li>Game: {scores.game != null ? scores.game.toFixed(2) : '—'}</li>
        <li>Combined: {scores.combined != null ? scores.combined.toFixed(2) : '—'}</li>
      </ul>
      <button onClick={combine} disabled={!canCombine || loading}>
        {loading ? 'Combining…' : 'Combine and get feedback'}
      </button>
      {scores.feedback && (
        <div style={{ background: '#f7f7f7', padding: 12, borderRadius: 6, marginTop: 8 }}>
          <strong>AI Guidance</strong>
          <p style={{ margin: 0 }}>{scores.feedback}</p>
        </div>
      )}
    </div>
  )
}

