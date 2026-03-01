"use client"

import { useState } from "react"
import { usePosts } from "@/lib/hooks"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Loader2, Send, Trash2, Share2, MessageCircle } from "lucide-react"
import { formatDate } from "@/lib/utils"

export default function PostsPage() {
  const { posts, isLoading, mutate } = usePosts()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim()) return

    setIsSubmitting(true)
    try {
      await api.post("/posts/", { title, content })
      setTitle("")
      setContent("")
      mutate()
    } catch (error: any) {
      console.error("Post failed", error)
      alert("Post failed: " + (error.response?.data?.detail || error.message))
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this post?")) return
    try {
      await api.delete(`/posts/${id}`)
      mutate()
    } catch (error) {
      console.error("Delete failed", error)
      alert("Delete failed")
    }
  }

  const handleShare = (id: number) => {
    const url = `${window.location.origin}/posts/${id}`
    navigator.clipboard.writeText(url)
    alert("Link copied to clipboard!")
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <Card className="glass-panel border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl text-primary-foreground">Create New Post</CardTitle>
          <CardDescription>Share your thoughts with the world (max 50 posts)</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              placeholder="Title (optional)"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="text-lg font-medium"
              maxLength={100}
            />
            <textarea
              className="flex min-h-[120px] w-full rounded-xl border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all resize-y"
              placeholder="What's on your mind?"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              required
              maxLength={10000}
            />
            <div className="flex justify-end">
              <Button type="submit" isLoading={isSubmitting} size="lg" className="rounded-2xl px-8">
                <Send className="mr-2 h-4 w-4" />
                Publish
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <div className="space-y-6">
        <h2 className="text-2xl font-bold ml-2 text-foreground/80">Recent Posts</h2>
        
        {isLoading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="h-10 w-10 animate-spin text-primary" />
          </div>
        ) : posts?.length === 0 ? (
          <div className="text-center py-20 text-muted-foreground bg-white/50 rounded-3xl border border-dashed border-primary/20">
            <MessageCircle className="h-16 w-16 mx-auto mb-4 text-primary/30" />
            <p className="text-lg">No posts yet. Be the first to share!</p>
          </div>
        ) : (
          <div className="grid gap-6">
            {posts?.map((post) => (
              <Card key={post.id} className="overflow-hidden transition-all hover:shadow-md">
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-start gap-4">
                    <div className="space-y-1">
                      {post.title && <CardTitle className="text-xl">{post.title}</CardTitle>}
                      <CardDescription>{formatDate(post.created_at)}</CardDescription>
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      {/* Actions could go here */}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="text-foreground/90 whitespace-pre-wrap leading-relaxed">
                  {post.content}
                </CardContent>
                <CardFooter className="bg-secondary/20 flex justify-end gap-2 py-3">
                   <Button variant="ghost" size="sm" onClick={() => handleShare(post.id)}>
                    <Share2 className="h-4 w-4 mr-2" /> Share
                  </Button>
                  <Button variant="ghost" size="sm" className="text-destructive hover:text-destructive hover:bg-destructive/10" onClick={() => handleDelete(post.id)}>
                    <Trash2 className="h-4 w-4 mr-2" /> Delete
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
