import { useState, type ElementType } from "react"
import { BookOpen, Dna, FlaskConical } from "lucide-react"

import { Button } from "@/components/ui/button"

type NavItem = {
  label: string
  icon: ElementType
}

const navItems: NavItem[] = [
  { label: "Experiments", icon: FlaskConical },
]

export function AppSidebar() {
  const [activeItem, setActiveItem] = useState("Experiments")

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col overflow-hidden border-r border-white/5 bg-[#081c35] text-slate-300">
      <div className="flex h-16 items-center gap-3 border-b border-white/5 px-6">
        <Dna className="size-7 text-cyan-400" aria-hidden="true" />
        <span className="font-semibold text-white">Protein Screening</span>
      </div>

      <nav className="space-y-1 px-3 py-6" aria-label="Main navigation">
        {navItems.map(({ label, icon: Icon }) => {
          const isActive = activeItem === label

          return (
            <Button
              key={label}
              variant="ghost"
              onClick={() => setActiveItem(label)}
              aria-current={isActive ? "page" : undefined}
              className={
                "h-11 w-full justify-start gap-3 rounded-md px-3 font-normal " +
                (isActive
                  ? "bg-[#173555] text-white hover:bg-[#1b3d61] hover:text-white"
                  : "text-slate-300 hover:bg-white/5 hover:text-white")
              }
            >
              <Icon
                className={isActive ? "size-5 text-cyan-400" : "size-5"}
                aria-hidden="true"
              />
              {label}
            </Button>
          )
        })}
        <a
          href={import.meta.env.VITE_API_DOCS_URL || "/docs"}
          target="_blank"
          rel="noreferrer"
          className="flex h-11 w-full items-center gap-3 rounded-md px-3 text-sm text-slate-300 transition-colors hover:bg-white/5 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400"
        >
          <BookOpen className="size-5" aria-hidden="true" />
          API Documentation
        </a>
      </nav>

 
    </aside>
  )
}
