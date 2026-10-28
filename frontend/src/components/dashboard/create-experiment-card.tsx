import { Play } from "lucide-react"

import { Button } from "@/components/ui/button"
import { SequenceEntryTabs } from "@/components/dashboard/sequence-entry-tabs"
import { SequenceGuidelines } from "@/components/dashboard/sequence-guidelines"
import { useCreateExperiment } from "@/hooks/use-create-experiment"

export function CreateExperimentCard({ onCreated }: { onCreated: () => void }) {
  const { form, file, setFile, submit, submitError } = useCreateExperiment(onCreated)
  const sequences = form.watch("sequences")

  function clearForm() {
    form.reset({ name: "", sequences: "" })
    setFile(null)
  }

  return (
    <form onSubmit={submit} className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="max-w-4xl">
        <label htmlFor="experiment-name" className="mb-2 block text-sm font-semibold">
          Experiment Name <span className="text-red-500">*</span>
        </label>
        <input
          id="experiment-name"
          {...form.register("name")}
          placeholder="e.g. Kinase Inhibitor Screening"
          className="h-10 w-full rounded-md border border-slate-200 px-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/15"
        />
        {form.formState.errors.name && (
          <p className="mt-1 text-sm text-red-600">{form.formState.errors.name.message}</p>
        )}
      </div>

      <div className="mt-3 grid gap-6 xl:grid-cols-[minmax(0,1fr)_22rem]">
        <SequenceEntryTabs
          sequences={sequences}
          file={file}
          onSequencesChange={(value) => form.setValue("sequences", value, { shouldValidate: true })}
          onFileChange={setFile}
        />
        <div className="pt-16">
          <SequenceGuidelines />
        </div>
      </div>

      {form.formState.errors.sequences && !file && (
        <p className="mt-2 text-sm text-red-600">{form.formState.errors.sequences.message}</p>
      )}
      {submitError && <p className="mt-2 text-sm text-red-600" role="alert">{submitError}</p>}

      <div className="mt-4 flex justify-end gap-3">
        <Button type="button" variant="outline" size="lg" onClick={clearForm} className="rounded-md px-8">
          Clear
        </Button>
        <Button
          type="submit"
          size="lg"
          className="rounded-md bg-cyan-600 px-8 text-white hover:bg-cyan-700"
          disabled={form.formState.isSubmitting}
        >
          <Play className="fill-current" aria-hidden="true" />
          Create Experiment
        </Button>
      </div>
    </form>
  )
}
