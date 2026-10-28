import { DashboardPagination } from "@/components/dashboard/dashboard-pagination"
import type { Experiment } from "@/lib/api"

type ExperimentsTableProps = {
  items: Experiment[]
  total: number
  limit: number
  offset: number
  page: number
  pageCount: number
  setPage: (page: number) => void
  isLoading: boolean
  error: string
}

export function ExperimentsTable({ items, total, limit, offset, page, pageCount, setPage, isLoading, error }: ExperimentsTableProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-950">Experiments</h2>
          <p className="mt-1 text-sm text-slate-500">View and manage your protein screening experiments.</p>
        </div>
      </div>

      <div className="overflow-x-auto rounded-md border border-slate-200">
        <table className="w-full min-w-3xl text-left text-sm">
          <thead className="bg-slate-50 text-xs font-semibold text-slate-600"><tr><th className="px-4 py-3">#</th><th className="px-4 py-3">Experiment Name</th><th className="px-4 py-3">Created Date</th></tr></thead>
          <tbody className="divide-y divide-slate-100">
            {items.map((experiment, index) => (
              <tr key={experiment.id} className="text-slate-700 hover:bg-slate-50/70">
                <td className="px-4 py-3">{offset + index + 1}</td>
                <td className="px-4 py-3 font-medium text-slate-900">{experiment.name}</td>
                <td className="px-4 py-3">{new Date(experiment.created_at).toLocaleString()}</td>
              </tr>
            ))}
            {!isLoading && !error && items.length === 0 && <tr><td colSpan={3} className="px-4 py-8 text-center text-slate-500">No experiments yet.</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex flex-col gap-3 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <span>{isLoading ? "Loading experiments…" : error || `Showing ${total ? offset + 1 : 0} to ${Math.min(offset + limit, total)} of ${total} experiments`}</span>
        <DashboardPagination page={page} pageCount={pageCount} onPageChange={setPage} />
      </div>
    </section>
  )
}
