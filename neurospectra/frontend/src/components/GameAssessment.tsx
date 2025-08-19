import { useEffect, useMemo, useRef, useState } from 'react'
import { submitGame } from '../services/api'

type Trial = { target: string; correct: boolean; rt: number }

const EMOTIONS = ['happy', 'sad', 'angry']

export default function GameAssessment({ onScore }: { onScore: (p: number) => void }) {
  const [running, setRunning] = useState(false)
  const [trials, setTrials] = useState<Trial[]>([])
  const [gaze, setGaze] = useState<number[]>([])
  const [age, setAge] = useState<number | undefined>()
  const [prob, setProb] = useState<number | null>(null)
  const startTs = useRef<number | null>(null)
  const gazeStart = useRef<number | null>(null)
  const [currentTarget, setCurrentTarget] = useState<string | null>(null)

  const nextTarget = useMemo(() => EMOTIONS[Math.floor(Math.random() * EMOTIONS.length)], [trials.length])

  useEffect(() => {
    let timer: number | undefined
    if (running) {
      setCurrentTarget(nextTarget)
      startTs.current = performance.now()
      gazeStart.current = performance.now()
    }
    return () => {
      if (timer) window.clearTimeout(timer)
    }
  }, [running])

  const choose = async (choice: string) => {
    if (!running || !currentTarget || startTs.current == null) return
    const rt = performance.now() - startTs.current
    const correct = choice === currentTarget
    setTrials((t) => [...t, { target: currentTarget, correct, rt }])
    if (gazeStart.current != null) {
      setGaze((g) => [...g, performance.now() - gazeStart.current!])
    }
    // proceed to next or finish
    if (trials.length + 1 >= 10) {
      setRunning(false)
    } else {
      setCurrentTarget(EMOTIONS[Math.floor(Math.random() * EMOTIONS.length)])
      startTs.current = performance.now()
      gazeStart.current = performance.now()
    }
  }

  const submit = async () => {
    const payload = {
      reactionTimesMs: trials.map((t) => t.rt),
      correctEmotionSelections: trials.filter((t) => t.correct).length,
      totalEmotionTrials: trials.length,
      gazeHoldMs: gaze,
      ageYears: age,
    }
    const res = await submitGame(payload)
    setProb(res.probability)
    onScore(res.probability)
  }

  return (
    <div style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
      <h3>Game-based Assessment</h3>
      <div style={{ marginBottom: 8 }}>
        <label>Age (years): </label>
        <input type="number" step="0.1" value={age ?? ''} onChange={(e) => setAge(e.target.value ? Number(e.target.value) : undefined)} />
      </div>
      {!running && trials.length === 0 && (
        <button onClick={() => setRunning(true)}>Start (10 trials)</button>
      )}
      {running && (
        <div>
          <p>Choose the shown emotion: <b>{currentTarget}</b></p>
          <div style={{ display: 'flex', gap: 8 }}>
            {EMOTIONS.map((e) => (
              <button key={e} onClick={() => choose(e)}>{e}</button>
            ))}
          </div>
        </div>
      )}
      {!running && trials.length > 0 && (
        <div>
          <p>Trials completed: {trials.length}</p>
          <button onClick={submit}>Submit</button>
          <button onClick={() => { setTrials([]); setGaze([]); setProb(null); }}>Reset</button>
        </div>
      )}
      {prob !== null && <p>Game risk score: {prob.toFixed(2)}</p>}
    </div>
  )
}

