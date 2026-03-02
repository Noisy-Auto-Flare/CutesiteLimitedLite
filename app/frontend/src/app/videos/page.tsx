"use client"

import { useState, useRef } from "react"
import { useVideos } from "@/lib/hooks"
import { api, uploadApi } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, Upload, Trash2, Download, Share2, Film, Play, Maximize2 } from "lucide-react"
import { formatBytes, formatDate } from "@/lib/utils"
import { Modal } from "@/components/ui/modal"
import { Video } from "@/lib/api"

export default function VideosPage() {
  const { videos, isLoading, mutate } = useVideos()
  const [isUploading, setIsUploading] = useState(false)
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null)
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
        // Size check (10GB)
        if (file.size > 10240 * 1024 * 1024) {
          alert(`File ${file.name} is too large (max 10GB)`)
          continue
        }

        const isVideo = file.type.startsWith("video/")
        const extension = file.name.split(".").pop()?.toLowerCase() || ""
        const allowedExtensions = ["mp4", "mov", "m4v", "3gp", "3g2", "avi", "mkv", "webm", "ogg"]
        if (!isVideo && !allowedExtensions.includes(extension)) {
          alert(`Unsupported video format: ${file.name}`)
          continue
        }
        const formData = new FormData()
        formData.append("file", file)
        await uploadApi.post("/videos/", formData)
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
    if (!confirm("Are you sure you want to delete this video?")) return
    try {
      await api.delete(`/videos/${id}`)
      if (selectedVideo?.id === id) setSelectedVideo(null)
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
      {selectedVideo && (
        <Modal 
          isOpen={!!selectedVideo} 
          onClose={() => setSelectedVideo(null)}
          actions={
            <>
               <Button variant="secondary" size="icon" className="rounded-full bg-black/50 hover:bg-black/70 text-white border-0" onClick={() => window.open(getPublicUrl(selectedVideo.url), '_blank')}>
                <Download className="h-5 w-5" />
              </Button>
              <Button variant="secondary" size="icon" className="rounded-full bg-black/50 hover:bg-black/70 text-white border-0" onClick={() => handleShare(selectedVideo.url)}>
                <Share2 className="h-5 w-5" />
              </Button>
              <Button variant="destructive" size="icon" className="rounded-full bg-red-500/80 hover:bg-red-600/90 text-white border-0" onClick={() => handleDelete(selectedVideo.id)}>
                <Trash2 className="h-5 w-5" />
              </Button>
            </>
          }
        >
          <video 
            src={selectedVideo.url} 
            controls 
            autoPlay
            className="max-w-full max-h-[85vh] rounded-lg shadow-2xl bg-black"
          />
        </Modal>
      )}

      <div className="flex flex-col md:flex-row justify-between items-center gap-4 glass-panel p-6 rounded-3xl">
        <div>
          <h1 className="text-3xl font-bold text-primary-foreground/80">My Videos</h1>
          <p className="text-muted-foreground mt-1">Short clips and memories (max 15)</p>
        </div>
        <div>
          <input
            type="file"
            accept="video/*,.mov,.mp4,.m4v,.3gp,.3g2,.avi,.mkv,.webm,.ogg"
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
            Upload Video
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="h-10 w-10 animate-spin text-primary" />
        </div>
      ) : videos?.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground bg-white/50 rounded-3xl border border-dashed border-primary/20">
          <Film className="h-16 w-16 mx-auto mb-4 text-primary/30" />
          <p className="text-lg">No videos yet. Upload your first one!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {videos?.map((video) => (
            <Card 
              key={video.id} 
              className="overflow-hidden group hover:scale-[1.02] transition-transform duration-300 cursor-pointer border-0 shadow-sm hover:shadow-md"
              onClick={() => setSelectedVideo(video)}
            >
              <div className="aspect-video relative overflow-hidden bg-black/10 group">
                <video 
                  src={video.url} 
                  className="w-full h-full object-cover pointer-events-none"
                />
                <div className="absolute top-2 right-2 bg-black/60 text-white text-xs px-2 py-1 rounded-md z-10">
                  {video.duration.toFixed(1)}s
                </div>
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
                   <div className="bg-white/20 backdrop-blur-sm p-3 rounded-full">
                     <Play className="text-white fill-white w-6 h-6 ml-1" />
                   </div>
                </div>
              </div>
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-medium truncate text-sm flex-1 mr-2" title={video.filename}>Видео</p>
                </div>
                <div className="flex justify-between items-center text-xs text-muted-foreground">
                  <span>{formatBytes(video.size)}</span>
                  <span>{formatDate(video.created_at)}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
