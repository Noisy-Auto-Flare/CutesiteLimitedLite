"use client"

import * as React from "react"
import { X, Download, Share2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  actions?: React.ReactNode
}

export function Modal({ isOpen, onClose, children, actions }: ModalProps) {
  React.useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }
    window.addEventListener("keydown", handleEsc)
    return () => window.removeEventListener("keydown", handleEsc)
  }, [onClose])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div 
        className="absolute inset-0" 
        onClick={onClose} 
      />
      <div className="relative z-50 w-full max-w-5xl max-h-[90vh] flex flex-col items-center justify-center pointer-events-none">
         <div className="fixed top-3 right-3 md:top-4 md:right-4 flex gap-2 pointer-events-auto z-[100]">
            {actions}
            <Button variant="secondary" size="icon" onClick={onClose} className="rounded-full bg-black/50 hover:bg-black/70 text-white border-0">
              <X className="h-5 w-5" />
            </Button>
         </div>
         <div className="w-full h-full flex items-center justify-center pointer-events-auto relative">
            {children}
         </div>
      </div>
    </div>
  )
}
