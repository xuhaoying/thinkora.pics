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
    <>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
        <div className="container mx-auto px-4 py-16 text-center">
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-gray-900 dark:text-white mb-6">
            Premium Transparent PNG Images
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            Discover over 4,000 high-quality PNG images with transparent backgrounds. 
            Perfect for designers, developers, and content creators.
          </p>
          <SearchBar />
        </div>
        
        {/* Decorative gradient */}
        <div className="absolute inset-x-0 top-0 -z-10 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
          <div className="relative left-1/2 -ml-96 aspect-[1155/678] w-[72.1875rem] rotate-[30deg] bg-gradient-to-tr from-purple-200 to-blue-200 dark:from-purple-900 dark:to-blue-900 opacity-30"></div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        {searchParams.q && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200">
              Search results for "{searchParams.q}"
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Found {images.length} images
            </p>
          </div>
        )}

        {images.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            {images.map((image) => (
              <ImageCard key={image.id} image={image} />
            ))}
          </div>
        ) : (
          <div className="text-center py-24">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full mb-6">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h2 className="text-3xl font-semibold mb-4 text-gray-900 dark:text-white">No Results Found</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
              We couldn't find any images matching your search for "{searchParams.q}". 
              Try different keywords or browse our collection.
            </p>
            <a href="/" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors">
              Browse All Images
            </a>
          </div>
        )}
      </main>
    </>
  );
} 