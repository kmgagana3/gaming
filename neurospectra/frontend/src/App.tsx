import { useState } from 'react'
import EEGUpload from './components/EEGUpload'
import AVUpload from './components/AVUpload'
import GameAssessment from './components/GameAssessment'
import Results from './components/Results'

type Scores = {
  eeg?: number
  av?: number
  game?: number
  combined?: number
  feedback?: string
}

export default function App() {
  const [scores, setScores] = useState<Scores>({})

  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16, fontFamily: 'Inter, system-ui, Arial' }}>
      <h1>NeuroSpectra</h1>
      <p>Early ASD screening using EEG, audio-visual behavior, and interactive games.</p>

      <section style={{ display: 'grid', gap: 24, gridTemplateColumns: '1fr' }}>
        <EEGUpload onScore={(p) => setScores((s) => ({ ...s, eeg: p }))} />
        <AVUpload onScore={(p) => setScores((s) => ({ ...s, av: p }))} />
        <GameAssessment onScore={(p) => setScores((s) => ({ ...s, game: p }))} />
        <Results scores={scores} onScoresChange={setScores} />
      </section>
    </div>
  )
}

