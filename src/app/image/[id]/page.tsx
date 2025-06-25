import { getDbConnection } from '@/lib/db';
import { notFound } from 'next/navigation';
import type { ImageType } from '@/app/page';
import Link from 'next/link';

interface ImagePageProps {
  params: {
    id: string;
  };
}

async function getImage(id: string): Promise<ImageType | null> {
  const db = await getDbConnection();
  const image = await db.get<ImageType>('SELECT * FROM images WHERE id = ?', id);
  return image || null;
}

export default async function ImagePage({ params }: ImagePageProps) {
  const image = await getImage(params.id);

  if (!image) {
    notFound();
  }
  
  const tags = image.tags ? JSON.parse(image.tags) : [];

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link href="/" className="text-blue-600 hover:underline">
          &larr; Back to Gallery
        </Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Image Display Column */}
        <div className="md:col-span-2 bg-gray-100 rounded-lg flex items-center justify-center p-4">
          <img
            src={image.url_regular || ''}
            alt={image.title || 'Untitled Image'}
            width={image.width || 800}
            height={image.height || 600}
            className="max-w-full max-h-[80vh] h-auto object-contain"
          />
        </div>

        {/* Details Column */}
        <div className="md:col-span-1">
          <h1 className="text-4xl font-extrabold mb-2 tracking-tight">{image.title || 'Untitled'}</h1>
          <p className="text-lg text-gray-500 mb-4">
            by{' '}
            <a href={image.author_url || '#'} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
              {image.author_name || 'Unknown Artist'}
            </a>
          </p>
          
          <p className="text-gray-700 mb-6">{image.description || 'No description available.'}</p>
          
          <div className="mb-6">
            <h3 className="font-bold text-lg mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {tags.map((tag: string, index: number) => (
                <span key={index} className="bg-gray-200 text-gray-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded">
                  {tag}
                </span>
              ))}
            </div>
          </div>
          
          <div className="mb-6">
             <h3 className="font-bold text-lg mb-2">Details</h3>
             <ul className="text-gray-700 space-y-1">
                <li><strong>Dimensions:</strong> {image.width} x {image.height} px</li>
                <li><strong>Aspect Ratio:</strong> {image.aspect_ratio}</li>
                <li><strong>File Size:</strong> {image.file_size}</li>
             </ul>
          </div>

          <a
            href={`${image.url_download}?force=true`}
            download
            target="_blank"
            rel="noopener noreferrer"
            className="w-full inline-flex items-center justify-center px-4 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Download Image
          </a>
        </div>
      </div>
    </main>
  );
} 