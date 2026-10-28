import { zodResolver } from "@hookform/resolvers/zod"
import axios from "axios"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { api } from "@/lib/api"

const formSchema = z.object({
  name: z.string().trim().min(1, "Experiment name is required"),
  sequences: z.string(),
})

const sequencesSchema = z.array(
  z.string().min(12, "Each sequence must have at least 12 characters").max(100, "Each sequence must have at most 100 characters").regex(/^[A-Z]+$/, "Use uppercase letters only"),
).length(20, "Enter exactly 20 sequences")

export type ExperimentForm = z.infer<typeof formSchema>

export function useCreateExperiment(onCreated: () => void) {
  const [file, setFile] = useState<File | null>(null)
  const [submitError, setSubmitError] = useState("")
  const form = useForm<ExperimentForm>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", sequences: "" },
  })

  const submit = form.handleSubmit(async ({ name, sequences }) => {
    setSubmitError("")
    const values = sequences.split(/\r?\n/).map((value) => value.trim()).filter(Boolean)
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
      form.reset({ name: "", sequences: "" })
      setFile(null)
      await onCreated()
    } catch (error) {
      setSubmitError(
        axios.isAxiosError(error) && error.response?.data?.detail
          ? JSON.stringify(error.response.data.detail)
          : "Could not create the experiment",
      )
    }
  })

  return { form, file, setFile, submit, submitError }
}
