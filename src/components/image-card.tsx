import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import type { ImageType } from '@/app/page';

interface ImageCardProps {
  image: ImageType;
}

export function ImageCard({ image }: ImageCardProps) {
  // The 'tags' field is a JSON string, so we need to parse it.
  const tags = image.tags ? JSON.parse(image.tags) : [];

  return (
    <Link href={`/image/${image.id}`} className="group relative block overflow-hidden rounded-lg shadow-lg transition-shadow duration-300 ease-in-out hover:shadow-xl">
      <div className="relative aspect-[4/3] w-full">
        <Image
          src={image.url_regular || ''}
          alt={image.title || 'Untitled Image'}
          fill
          className="object-cover transition-transform duration-300 ease-in-out group-hover:scale-105"
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          loading="lazy"
        />
      </div>
      <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-0 transition-opacity duration-300 ease-in-out group-hover:opacity-100">
        <div className="absolute bottom-0 left-0 p-4 text-white">
          <h3 className="font-bold text-lg">{image.title || 'Untitled'}</h3>
          <p className="text-sm">by {image.author_name || 'Unknown Artist'}</p>
          <div className="mt-2 flex flex-wrap gap-1">
            {tags.slice(0, 3).map((tag: string, index: number) => (
              <span key={index} className="text-xs bg-white/20 backdrop-blur-sm rounded-full px-2 py-1">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </Link>
  );
} 