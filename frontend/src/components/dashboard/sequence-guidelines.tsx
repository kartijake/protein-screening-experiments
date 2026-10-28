import { Info } from "lucide-react"

const guidelines = [
  "Use single-letter amino acid codes (A–Z)",
  "Enter one sequence per line",
  "Exactly 20 sequences per experiment",
  "Each sequence must be 12–100 amino acids",
  "Sequences need a shared prefix and suffix",
]

export function SequenceGuidelines() {
  return (
    <aside className="rounded-lg bg-cyan-50 p-5 text-sm text-slate-600">
      <div className="mb-3 flex items-center gap-2 font-semibold text-cyan-700">
        <Info className="size-5 fill-cyan-600 text-white" aria-hidden="true" />
        Sequence Guidelines
      </div>
      <ul className="space-y-2">
        {guidelines.map((guideline) => (
          <li key={guideline} className="flex gap-2">
            <span className="font-bold text-cyan-600">•</span>
            {guideline}
          </li>
        ))}
      </ul>
    </aside>
  )
}
