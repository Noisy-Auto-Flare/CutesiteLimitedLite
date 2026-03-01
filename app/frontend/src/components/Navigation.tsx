"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Image, Film, MessageCircle, Heart } from "lucide-react"

export function Navigation() {
  const pathname = usePathname()

  const links = [
    { href: "/images", label: "Images", icon: Image },
    { href: "/videos", label: "Videos", icon: Film },
    { href: "/posts", label: "Posts", icon: MessageCircle },
  ]

  return (
    <>
      {/* Desktop Navigation */}
      <nav className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md hidden md:block">
        <div className="container flex h-16 items-center justify-between px-4 md:px-6 mx-auto">
          <Link href="/" className="flex items-center gap-2 font-bold text-xl text-primary hover:opacity-80 transition-opacity">
            <Heart className="h-6 w-6 fill-current" />
            <span>Cutesite</span>
          </Link>
          <div className="flex gap-1 sm:gap-4">
            {links.map((link) => {
              const Icon = link.icon
              const isActive = pathname === link.href || (link.href === "/images" && pathname === "/")
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={cn(
                    "flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
                    isActive ? "bg-secondary text-secondary-foreground" : "text-muted-foreground"
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden sm:inline">{link.label}</span>
                </Link>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 border-t bg-background/80 backdrop-blur-md md:hidden safe-area-pb">
        <div className="flex items-center justify-around h-16 px-2">
          {links.map((link) => {
            const Icon = link.icon
            const isActive = pathname === link.href || (link.href === "/images" && pathname === "/")
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "flex flex-col items-center justify-center gap-1 rounded-xl w-full h-full text-xs font-medium transition-colors",
                  isActive ? "text-primary" : "text-muted-foreground"
                )}
              >
                <Icon className={cn("h-6 w-6", isActive && "fill-current")} />
                <span>{link.label}</span>
              </Link>
            )
          })}
        </div>
      </nav>
    </>
  )
}
