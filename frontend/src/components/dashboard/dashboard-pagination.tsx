import { ChevronLeft, ChevronRight } from "lucide-react"

import { Button } from "@/components/ui/button"

type DashboardPaginationProps = {
  page: number
  pageCount: number
  onPageChange: (page: number) => void
}

export function DashboardPagination({ page, pageCount, onPageChange }: DashboardPaginationProps) {
  const pages = Array.from({ length: pageCount }, (_, index) => index + 1)

  return (
    <div className="flex items-center gap-1">
      <Button variant="outline" size="icon" aria-label="Previous page" className="rounded-md" disabled={page === 1} onClick={() => onPageChange(page - 1)}><ChevronLeft /></Button>
      {pages.map((pageNumber) => (
        <Button key={pageNumber} variant={pageNumber === page ? "default" : "outline"} size="icon" onClick={() => onPageChange(pageNumber)} className={pageNumber === page ? "rounded-md bg-cyan-600 text-white hover:bg-cyan-700" : "rounded-md"} aria-current={pageNumber === page ? "page" : undefined}>
          {pageNumber}
        </Button>
      ))}
      <Button variant="outline" size="icon" aria-label="Next page" className="rounded-md" disabled={page === pageCount} onClick={() => onPageChange(page + 1)}><ChevronRight /></Button>
    </div>
  )
}
