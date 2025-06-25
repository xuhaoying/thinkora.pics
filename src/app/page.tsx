import { getDbConnection } from '@/lib/db';
import { ImageCard } from '@/components/image-card';
import { SearchBar } from '@/components/search-bar';

// Define a type for our image data for type safety
export interface ImageType {
  id: string;
  title: string | null;
  description: string | null;
  author_name: string | null;
  author_url: string | null;
  width: number | null;
  height: number | null;
  aspect_ratio: string | null;
  url_thumbnail: string | null;
  url_regular: string | null;
  url_download: string | null;
  tags: string; // This is a JSON string
  category: string | null;
  quality_score: number | null;
  file_size: string | null;
  transparent_ratio: number | null;
  created_at: string | null;
  unsplash_id: string | null;
  unsplash_url: string | null;
  unsplash_download_location: string | null;
}

interface HomePageProps {
  searchParams: {
    q?: string;
  };
}

async function getImages(query?: string): Promise<ImageType[]> {
  const db = await getDbConnection();
  let sql = 'SELECT * FROM images';
  const params: string[] = [];

  if (query) {
    sql += " WHERE title LIKE ? OR description LIKE ? OR tags LIKE ?";
    const likeQuery = `%${query}%`;
    params.push(likeQuery, likeQuery, likeQuery);
  }

  sql += ' ORDER BY created_at DESC';
  
  const images = await db.all<ImageType[]>(sql, ...params);
  return images;
}

export default async function HomePage({ searchParams }: HomePageProps) {
  const images = await getImages(searchParams.q);

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2 tracking-tight text-gray-800">
          Thinkora Pics
        </h1>
        <p className="text-lg text-gray-600">
          High-quality PNG images with transparent backgrounds. Ready for your next project.
        </p>
      </div>

      <SearchBar />

      {images.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {images.map((image) => (
            <ImageCard key={image.id} image={image} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <h2 className="text-2xl font-semibold mb-2">No Results Found</h2>
          <p className="text-gray-500">
            We couldn't find any images matching your search for "{searchParams.q}". Try a different keyword.
          </p>
        </div>
      )}
    </main>
  );
} 