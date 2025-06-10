import { Metadata } from "next"
import { StoryGenerator } from "@/components/story/story-generator"

export const metadata: Metadata = {
  title: "AI Story Generator - Thinkora.pics",
  description: "Generate unique, child-friendly stories with our AI-powered story generator.",
}

export default function StoryPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl">
            AI Story Generator
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
            Create unique, engaging stories for children with our AI-powered story generator.
          </p>
        </div>
        
        <StoryGenerator />
      </div>
    </div>
  )
} 