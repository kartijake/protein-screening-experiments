import { zodResolver } from "@hookform/resolvers/zod"
import axios from "axios"
import { useEffect, useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { api } from "@/lib/api"

const formSchema = z.object({
  name: z.string().trim().min(1, "Experiment name is required").max(100, "Experiment name must be 100 characters or fewer"),
  sequences: z.string(),
})

const sequencesSchema = z.array(
  z.string().min(12, "Each sequence must have at least 12 characters").max(100, "Each sequence must have at most 100 characters").regex(/^[A-Z]+$/, "Use letters only"),
).length(20, "Enter exactly 20 sequences")

export type ExperimentForm = z.infer<typeof formSchema>

function getApiErrorMessage(error: unknown) {
  if (!axios.isAxiosError(error)) return "Could not create the experiment"

  const message = error.response?.data?.error
  if (typeof message === "string") return message

  return "Could not create the experiment"
}

export function useCreateExperiment(onCreated: () => void) {
  const [file, setFile] = useState<File | null>(null)
  const [submitError, setSubmitError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const form = useForm<ExperimentForm>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", sequences: "" },
  })

  const submit = form.handleSubmit(async ({ name, sequences }) => {
    setSubmitError("")
    setSuccessMessage("")
    const values = sequences.split(/[\r\n,]+/).map((value) => value.trim().toUpperCase()).filter(Boolean)
    if (!file) {
      const result = sequencesSchema.safeParse(values)
      if (!result.success) {
        form.setError("sequences", { message: result.error.issues[0].message })
        return
      }
    }

    try {
      if (file) {
        const data = new FormData()
        data.append("name", name)
        data.append("file", file)
        await api.post("/experiments/upload", data)
      } else {
        await api.post("/experiments", { name, sequences: values })
      }
      setSuccessMessage(file ? "FASTA experiment uploaded successfully" : "Experiment created successfully")
      form.reset({ name: "", sequences: "" })
      setFile(null)
      await onCreated()
    } catch (error) {
      setSubmitError(getApiErrorMessage(error))
    }
  })

  useEffect(() => {
    if (!successMessage) return

    const timeout = window.setTimeout(() => setSuccessMessage(""), 4000)
    return () => window.clearTimeout(timeout)
  }, [successMessage])

  return { form, file, setFile, submit, submitError, successMessage }
}
