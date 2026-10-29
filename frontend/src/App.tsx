import { AppSidebar } from "@/components/app-sidebar"
import { ExperimentDashboard } from "@/components/dashboard/experiment-dashboard"

export default function App() {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 text-slate-900">
      <AppSidebar />
      <ExperimentDashboard />
    </div>
  )
}
