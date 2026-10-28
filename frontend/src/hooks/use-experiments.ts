import { useCallback, useEffect, useState } from "react"

import { api, type PaginatedExperiments } from "@/lib/api"

const pageSize = 5

export function useExperiments() {
  const [page, setPage] = useState(1)
  const [data, setData] = useState<PaginatedExperiments>({ items: [], total: 0, limit: pageSize, offset: 0 })
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")

  const load = useCallback(async () => {
    try {
      const response = await api.get<PaginatedExperiments>("/experiments", {
        params: { limit: pageSize, offset: (page - 1) * pageSize },
      })
      setData(response.data)
    } catch {
      setError("Could not load experiments")
    } finally {
      setIsLoading(false)
    }
  }, [page])

  useEffect(() => {
    const request = window.setTimeout(() => { void load() }, 0)
    return () => window.clearTimeout(request)
  }, [load])

  const changePage = (nextPage: number) => {
    setIsLoading(true)
    setError("")
    setPage(nextPage)
  }

  const refetch = async () => {
    setIsLoading(true)
    setError("")
    await load()
  }

  return {
    ...data,
    page,
    pageCount: Math.max(1, Math.ceil(data.total / pageSize)),
    setPage: changePage,
    isLoading,
    error,
    refetch,
  }
}
