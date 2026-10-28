import { FileText, FileUp, Pencil, X } from "lucide-react"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"

type SequenceEntryTabsProps = {
  sequences: string
  file: File | null
  onSequencesChange: (value: string) => void
  onFileChange: (file: File | null) => void
}

export function SequenceEntryTabs({
  sequences,
  file,
  onSequencesChange,
  onFileChange,
}: SequenceEntryTabsProps) {
  const sequenceCount = sequences.split("\n").filter((line) => line.trim()).length

  return (
    <Tabs defaultValue="manual" className="gap-0">
      <TabsList className="h-12 w-full justify-start rounded-none border-b bg-transparent p-0">
        <TabsTrigger
          value="manual"
          className="h-12 flex-none rounded-none border-0 border-b-2 border-transparent px-5 data-[active]:border-cyan-600 data-[active]:bg-transparent data-[active]:text-slate-950"
        >
          <Pencil aria-hidden="true" />
          Manual Entry
        </TabsTrigger>
        <TabsTrigger
          value="upload"
          className="h-12 flex-none rounded-none border-0 border-b-2 border-transparent px-5 data-[active]:border-cyan-600 data-[active]:bg-transparent data-[active]:text-slate-950"
        >
          <FileUp aria-hidden="true" />
          Upload FASTA
        </TabsTrigger>
      </TabsList>

      <TabsContent value="manual" className="pt-4">
        <div className="mb-2 flex items-center justify-between text-sm font-medium">
          <label htmlFor="protein-sequences">
            Protein Sequences <span className="text-red-500">*</span>
          </label>
          <span className={sequenceCount === 20 ? "text-cyan-600" : "text-amber-600"}>
            {sequenceCount} / 20 <span className="font-normal text-slate-500">sequences</span>
          </span>
        </div>
        <textarea
          id="protein-sequences"
          value={sequences}
          onChange={(event) => onSequencesChange(event.target.value)}
          rows={7}
          spellCheck={false}
          placeholder="Enter one protein sequence per line"
          className="w-full resize-y rounded-md border border-slate-200 bg-white px-4 py-3 font-mono text-sm leading-6 text-slate-700 outline-none transition focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/15"
        />
        <p className="mt-2 text-xs text-slate-500">
          Enter one protein sequence per line using single-letter amino acid codes.
        </p>
      </TabsContent>

      <TabsContent value="upload" className="pt-4">
        {file ? (
          <div className="flex min-h-44 flex-col items-center justify-center rounded-lg border border-cyan-200 bg-cyan-50/40 text-center">
            <FileText className="mb-3 size-7 text-cyan-600" aria-hidden="true" />
            <span className="max-w-full truncate px-6 font-medium text-slate-800">{file.name}</span>
            <span className="mt-1 text-xs text-slate-500">{Math.ceil(file.size / 1024)} KB</span>
            <Button type="button" variant="outline" className="mt-4 rounded-md" onClick={() => onFileChange(null)}>
              <X aria-hidden="true" />
              Remove file
            </Button>
          </div>
        ) : (
          <>
            <label
              htmlFor="fasta-file"
              className="flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-slate-50 text-center hover:border-cyan-500 hover:bg-cyan-50/40"
            >
              <FileUp className="mb-3 size-7 text-cyan-600" aria-hidden="true" />
              <span className="font-medium text-slate-800">Choose a FASTA file</span>
              <span className="mt-1 text-xs text-slate-500">Maximum file size: 32 KB</span>
            </label>
            <input
              id="fasta-file"
              type="file"
              accept=".fasta,.fa,.txt,text/plain"
              className="sr-only"
              onChange={(event) => {
                onFileChange(event.target.files?.[0] ?? null)
                event.target.value = ""
              }}
            />
          </>
        )}
      </TabsContent>
    </Tabs>
  )
}
