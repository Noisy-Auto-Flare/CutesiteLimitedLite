"use client"

import { useState, useRef } from "react"
import { useImages } from "@/lib/hooks"
import { api, uploadApi } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Loader2, Upload, Trash2, Download, Share2, FileImage, Maximize2 } from "lucide-react"
import { formatBytes, formatDate } from "@/lib/utils"
import { Modal } from "@/components/ui/modal"
import { Image } from "@/lib/api"

export default function ImagesPage() {
  const { images, isLoading, mutate } = useImages()
  const [isUploading, setIsUploading] = useState(false)
  const [selectedImage, setSelectedImage] = useState<Image | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const getPublicUrl = (url: string) => {
    try {
      const parsed = new URL(url, window.location.origin)
      return `${window.location.origin}${parsed.pathname}`
    } catch {
      return url
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    if (files.length === 0) return

    setIsUploading(true)
    try {
      for (const file of files) {
        // Size check (100MB)
        if (file.size > 500 * 1024 * 1024) {
          alert(`File ${file.name} is too large (max 500MB)`)
          continue
        }

        const isImage = file.type.startsWith("image/")
        const extension = file.name.split(".").pop()?.toLowerCase() || ""
        const allowedExtensions = ["heic", "heif", "avif", "tif", "tiff", "bmp"]
        if (!isImage && !allowedExtensions.includes(extension)) {
          alert(`Unsupported image format: ${file.name}`)
          continue
        }
        const formData = new FormData()
        formData.append("file", file)
        await uploadApi.post("/images/", formData)
      }
      mutate()
    } catch (error: any) {
      console.error("Upload failed", error)
      if (error.response?.status === 413) {
        alert("File is too large for the server. Please check Nginx/Proxy settings (client_max_body_size).")
      } else {
        alert("Upload failed: " + (error.response?.data?.detail || error.message))
      }
    } finally {
      setIsUploading(false)
      if (fileInputRef.current) fileInputRef.current.value = ""
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this image?")) return
    try {
      await api.delete(`/images/${id}`)
      if (selectedImage?.id === id) setSelectedImage(null)
      mutate()
    } catch (error) {
      console.error("Delete failed", error)
      alert("Delete failed")
    }
  }

  const handleShare = (url: string) => {
    navigator.clipboard.writeText(getPublicUrl(url))
    alert("Link copied to clipboard!")
  }

  return (
    <div className="space-y-8">
      {/* Fullscreen Modal */}
      {selectedImage && (
        <Modal 
          isOpen={!!selectedImage} 
          onClose={() => setSelectedImage(null)}
          actions={
            <>
               <Button variant="secondary" size="icon" className="rounded-full bg-black/50 hover:bg-black/70 text-white border-0" onClick={() => window.open(getPublicUrl(selectedImage.url), '_blank')}>
                <Download className="h-5 w-5" />
              </Button>
              <Button variant="secondary" size="icon" className="rounded-full bg-black/50 hover:bg-black/70 text-white border-0" onClick={() => handleShare(selectedImage.url)}>
                <Share2 className="h-5 w-5" />
              </Button>
              <Button variant="destructive" size="icon" className="rounded-full bg-red-500/80 hover:bg-red-600/90 text-white border-0" onClick={() => handleDelete(selectedImage.id)}>
                <Trash2 className="h-5 w-5" />
              </Button>
            </>
          }
        >
          <img 
            src={selectedImage.url} 
            alt={selectedImage.filename} 
            className="max-w-full max-h-[85vh] object-contain rounded-lg shadow-2xl"
          />
        </Modal>
      )}

      <div className="flex flex-col md:flex-row justify-between items-center gap-4 glass-panel p-6 rounded-3xl">
        <div>
          <h1 className="text-3xl font-bold text-primary-foreground/80">My Gallery</h1>
          <p className="text-muted-foreground mt-1">Store your precious memories (max 50)</p>
        </div>
        <div>
          <input
            type="file"
            accept="image/*,.heic,.heif,.avif,.tif,.tiff,.bmp"
            className="hidden"
            ref={fileInputRef}
            onChange={handleUpload}
            multiple
          />
          <Button 
            onClick={() => fileInputRef.current?.click()} 
            isLoading={isUploading}
            size="lg"
            className="rounded-2xl w-full md:w-auto"
          >
            <Upload className="mr-2 h-5 w-5" />
            Upload Image
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="h-10 w-10 animate-spin text-primary" />
        </div>
      ) : images?.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground bg-white/50 rounded-3xl border border-dashed border-primary/20">
          <FileImage className="h-16 w-16 mx-auto mb-4 text-primary/30" />
          <p className="text-lg">No images yet. Upload your first one!</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {images?.map((image) => (
            <Card 
              key={image.id} 
              className="overflow-hidden group hover:scale-[1.02] transition-transform duration-300 cursor-pointer border-0 shadow-sm hover:shadow-md"
              onClick={() => setSelectedImage(image)}
            >
              <div className="aspect-square relative overflow-hidden bg-secondary/30">
                <img 
                  src={image.url} 
                  alt={image.filename}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
                   <Maximize2 className="text-white drop-shadow-md w-8 h-8" />
                </div>
              </div>
              <CardContent className="p-3">
                <p className="font-medium truncate text-sm" title={image.filename}>Фото</p>
                <div className="flex justify-between items-center mt-1 text-xs text-muted-foreground">
                  <span>{formatBytes(image.size)}</span>
                  <span>{formatDate(image.created_at)}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
