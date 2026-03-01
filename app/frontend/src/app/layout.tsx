import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/Navigation";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Cutesite",
  description: "A very cute production-ready website",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={cn(inter.className, "min-h-screen bg-background antialiased")}>
        <div className="relative flex min-h-screen flex-col">
          <Navigation />
          <main className="flex-1 container mx-auto px-4 py-6 md:px-6 lg:px-8 pb-20 md:pb-6">
            {children}
          </main>
          <footer className="border-t py-6 md:py-0 hidden md:block">
            <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row mx-auto px-4 text-sm text-muted-foreground">
              <p>Built with ❤️ by Cutesite Team</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
