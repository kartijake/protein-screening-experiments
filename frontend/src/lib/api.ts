import axios from "axios"

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
})

export type Experiment = {
  id: string
  name: string
  sequences: string[]
  created_at: string
}

export type PaginatedExperiments = {
  items: Experiment[]
  total: number
  limit: number
  offset: number
}
