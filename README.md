# AI Coloring Book

An AI-powered children's coloring book website that generates unique, safe, and educational coloring pages using advanced AI technology.

## Features

- 🎨 **AI-Powered Generation**: Create unique coloring pages instantly with Replicate's Flux AI
- 🖼️ **High-Quality Downloads**: Print-ready PDFs perfect for any printer
- 🛡️ **Child-Safe Content**: All content is moderated and designed specifically for children
- ❤️ **Educational Value**: Promotes creativity, focus, and learning through coloring
- 📱 **Mobile-Friendly**: Responsive design works on all devices
- 🎯 **Multiple Categories**: Animals, fantasy, nature, vehicles, holidays, and educational themes

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **State Management**: React Context + useReducer
- **AI Service**: Replicate API (Flux AI model)
- **Authentication**: Supabase (planned)
- **Payments**: Stripe (planned)
- **Forms**: React Hook Form
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Replicate API key (for AI generation)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd thinkora.pics
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Fill in your API keys in the `.env` file:
- `VITE_REPLICATE_API_KEY`: Your Replicate API key
- `VITE_SUPABASE_URL`: Your Supabase project URL (when ready)
- `VITE_SUPABASE_ANON_KEY`: Your Supabase anon key (when ready)
- `VITE_STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key (when ready)

4. Start the development server:
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
src/
├── components/
│   ├── Layout/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── ColoringBook/     # Coloring book specific components
│   └── Auth/             # Authentication components
├── context/
│   └── ColoringBookContext.tsx
├── pages/
│   ├── Home.tsx
│   ├── Generate.tsx
│   └── Gallery.tsx
├── services/
│   └── aiService.ts
├── types/
│   └── index.ts
├── utils/                # Utility functions
└── hooks/                # Custom React hooks
```

## Features Implementation Status

- ✅ Core UI Components (Header, Footer, Home, Generate, Gallery)
- ✅ AI Image Generation Service (Replicate integration)
- ✅ State Management with Context
- ✅ Responsive Design with Tailwind CSS
- ✅ TypeScript Type Safety
- ⏳ User Authentication (Supabase)
- ⏳ Payment Processing (Stripe)
- ⏳ Image Download & PDF Generation
- ⏳ Content Moderation
- ⏳ User Dashboard

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_REPLICATE_API_KEY` | Replicate API key for AI generation | Yes |
| `VITE_SUPABASE_URL` | Supabase project URL | No (for auth) |
| `VITE_SUPABASE_ANON_KEY` | Supabase anonymous key | No (for auth) |
| `VITE_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | No (for payments) |
| `VITE_APP_URL` | Application URL | No |

## Deployment

This project is configured for deployment on Vercel:

1. Connect your GitHub repository to Vercel
2. Set up environment variables in Vercel dashboard
3. Deploy automatically on every push to main branch

## Pricing Model

- **Pay Per Page**: $0.50 per generated coloring page
- **Monthly Unlimited**: $9.90/month for unlimited generations
- **Free Trial**: Available for new users

## Safety & Compliance

- All generated content is automatically moderated
- COPPA compliant design (no data collection from children under 13)
- Child-safe prompts and filtering
- Educational focus with age-appropriate complexity levels

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@thinkora.pics or open an issue on GitHub.