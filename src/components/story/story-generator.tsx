"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Loader2 } from "lucide-react"

interface StoryParams {
  theme: string
  ageGroup: string
  length: string
  mainCharacter: string
  additionalDetails: string
}

export function StoryGenerator() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [story, setStory] = useState("")
  const [params, setParams] = useState<StoryParams>({
    theme: "",
    ageGroup: "",
    length: "",
    mainCharacter: "",
    additionalDetails: "",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsGenerating(true)
    
    try {
      // TODO: Implement actual API call to generate story
      // For now, we'll simulate a delay and return a placeholder story
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      setStory(`Once upon a time, there was a ${params.mainCharacter} who loved ${params.theme}. 
      This is a story for ${params.ageGroup} year olds, and it's ${params.length} long. 
      ${params.additionalDetails}`)
    } catch (error) {
      console.error("Error generating story:", error)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-8">
      <Card className="p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="theme">Story Theme</Label>
              <Input
                id="theme"
                placeholder="e.g., friendship, adventure, magic"
                value={params.theme}
                onChange={(e) => setParams({ ...params, theme: e.target.value })}
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="ageGroup">Age Group</Label>
              <Select
                value={params.ageGroup}
                onValueChange={(value) => setParams({ ...params, ageGroup: value })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select age group" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="3-5">3-5 years</SelectItem>
                  <SelectItem value="6-8">6-8 years</SelectItem>
                  <SelectItem value="9-12">9-12 years</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="length">Story Length</Label>
              <Select
                value={params.length}
                onValueChange={(value) => setParams({ ...params, length: value })}
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select length" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="short">Short (1-2 pages)</SelectItem>
                  <SelectItem value="medium">Medium (3-4 pages)</SelectItem>
                  <SelectItem value="long">Long (5+ pages)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="mainCharacter">Main Character</Label>
              <Input
                id="mainCharacter"
                placeholder="e.g., brave knight, friendly dragon"
                value={params.mainCharacter}
                onChange={(e) => setParams({ ...params, mainCharacter: e.target.value })}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="additionalDetails">Additional Details (Optional)</Label>
            <Textarea
              id="additionalDetails"
              placeholder="Add any specific elements you'd like in the story..."
              value={params.additionalDetails}
              onChange={(e) => setParams({ ...params, additionalDetails: e.target.value })}
              className="h-24"
            />
          </div>

          <Button type="submit" className="w-full" disabled={isGenerating}>
            {isGenerating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating Story...
              </>
            ) : (
              "Generate Story"
            )}
          </Button>
        </form>
      </Card>

      {story && (
        <Card className="p-6">
          <h2 className="text-2xl font-semibold mb-4">Generated Story</h2>
          <div className="prose dark:prose-invert max-w-none">
            {story.split('\n').map((paragraph, index) => (
              <p key={index} className="mb-4">
                {paragraph}
              </p>
            ))}
          </div>
          <div className="mt-6 flex gap-4">
            <Button variant="outline" onClick={() => navigator.clipboard.writeText(story)}>
              Copy Story
            </Button>
            <Button variant="outline" onClick={() => window.print()}>
              Print Story
            </Button>
          </div>
        </Card>
      )}
    </div>
  )
} 