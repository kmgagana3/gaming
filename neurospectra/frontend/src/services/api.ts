import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
})

export async function uploadEEG(file: File) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/eeg/predict', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data as { probability: number; features: Record<string, number> }
}

export async function uploadAV(audio?: File, video?: File) {
  const form = new FormData()
  if (audio) form.append('audio', audio)
  if (video) form.append('video', video)
  const { data } = await api.post('/av/predict', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data as { probability: number; features: Record<string, number> }
}

export async function submitGame(payload: {
  reactionTimesMs: number[]
  correctEmotionSelections: number
  totalEmotionTrials: number
  gazeHoldMs: number[]
  ageYears?: number
}) {
  const { data } = await api.post('/game/submit', payload)
  return data as { probability: number; features: Record<string, number> }
}

export async function combinedPredict(eeg_score: number, av_score: number, game_score: number) {
  const { data } = await api.post('/combined/predict', { eeg_score, av_score, game_score })
  return data as { probability: number }
}

export async function getFeedback(probability: number, ageYears?: number) {
  const { data } = await api.post('/feedback', { probability, ageYears })
  return data as { feedback: string }
}

