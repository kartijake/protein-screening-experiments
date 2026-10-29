import { DashboardPagination } from "@/components/dashboard/dashboard-pagination"
import type { Experiment } from "@/lib/api"

const MAX_DISPLAYED_NAME_LENGTH = 50

type ExperimentsTableProps = {
  items: Experiment[]
  total: number
  limit: number
  offset: number
  page: number
  pageCount: number
  setPage: (page: number) => void
  setLimit: (limit: number) => void
  isLoading: boolean
  error: string
}

export function ExperimentsTable({ items, total, limit, offset, page, pageCount, setPage, setLimit, isLoading, error }: ExperimentsTableProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-950">Experiments</h2>
          <p className="mt-1 text-sm text-slate-500">View and manage your protein screening experiments.</p>
        </div>
      </div>

      <div className="overflow-x-auto rounded-md border border-slate-200">
        <table aria-label="Experiments" className="w-full min-w-3xl text-left text-sm">
          <thead className="bg-slate-50 text-xs font-semibold text-slate-600"><tr><th className="px-4 py-3">#</th><th className="px-4 py-3">Experiment Name</th><th className="px-4 py-3">Created Date</th></tr></thead>
          <tbody className="divide-y divide-slate-100">
            {items.map((experiment, index) => (
              <tr key={experiment.id} className="text-slate-700 hover:bg-slate-50/70">
                <td className="px-4 py-3">{offset + index + 1}</td>
                <td
                  className="max-w-xs px-4 py-3 font-medium text-slate-900"
                  aria-label={`Experiment name: ${experiment.name}`}
                  title={experiment.name}
                >
                  <span className="block truncate">
                    {experiment.name.length > MAX_DISPLAYED_NAME_LENGTH
                      ? `${experiment.name.slice(0, MAX_DISPLAYED_NAME_LENGTH - 3)}...`
                      : experiment.name}
                  </span>
                </td>
                <td className="px-4 py-3">{new Date(experiment.created_at).toLocaleString()}</td>
              </tr>
            ))}
            {!isLoading && !error && items.length === 0 && <tr><td colSpan={3} className="px-4 py-8 text-center text-slate-500">No experiments yet.</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex flex-col gap-3 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap items-center gap-3">
          <span>{isLoading ? "Loading experiments…" : error || `Showing ${total ? offset + 1 : 0} to ${Math.min(offset + limit, total)} of ${total} experiments`}</span>
          <label className="flex items-center gap-2">
            Rows per page
            <select
              aria-label="Rows per page"
              value={limit}
              onChange={(event) => setLimit(Number(event.target.value))}
              className="rounded-md border border-slate-200 bg-white px-2 py-1 text-slate-700 outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/15"
            >
              {[5, 10, 25, 50].map((option) => <option key={option} value={option}>{option}</option>)}
            </select>
          </label>
        </div>
        <DashboardPagination page={page} pageCount={pageCount} onPageChange={setPage} />
      </div>
    </section>
  )
}
