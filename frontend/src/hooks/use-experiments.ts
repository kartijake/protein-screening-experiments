import { useCallback, useEffect, useState } from "react"

import { api, type PaginatedExperiments } from "@/lib/api"

const defaultPageSize = 5

export function useExperiments() {
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(defaultPageSize)
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
  }, [page, pageSize])

  useEffect(() => {
    const request = window.setTimeout(() => { void load() }, 0)
    return () => window.clearTimeout(request)
  }, [load])

  const changePage = (nextPage: number) => {
    setIsLoading(true)
    setError("")
    setPage(nextPage)
  }

  const changePageSize = (nextPageSize: number) => {
    setIsLoading(true)
    setError("")
    setPageSize(nextPageSize)
    setPage(1)
  }

  const refetch = async () => {
    setIsLoading(true)
    setError("")
    await load()
  }

  return {
    ...data,
    limit: pageSize,
    page,
    pageCount: Math.max(1, Math.ceil(data.total / pageSize)),
    setPage: changePage,
    setLimit: changePageSize,
    isLoading,
    error,
    refetch,
  }
}
