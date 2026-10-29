import { CreateExperimentCard } from "@/components/dashboard/create-experiment-card"
import { ExperimentsTable } from "@/components/dashboard/experiments-table"
import { useExperiments } from "@/hooks/use-experiments"

export function ExperimentDashboard() {
  const experiments = useExperiments()

  return (
    <main className="h-screen min-w-0 flex-1 overflow-y-auto overflow-x-hidden bg-slate-50 p-5 lg:p-7">
      <header className="mb-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-950">Create Experiment</h1>
          <p className="mt-1 text-sm text-slate-500">
            Add protein sequences for screening using manual entry or FASTA file upload.
          </p>
        </div>
      </header>

      <div className="space-y-5">
        <CreateExperimentCard onCreated={experiments.refetch} />
        <ExperimentsTable {...experiments} />
      </div>
    </main>
  )
}
