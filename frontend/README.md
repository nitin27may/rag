# RAG System Frontend

A modern web interface for the Comprehensive RAG System, built with Next.js 15 and React 19.

## Features

- **Document Management**: Upload, view, and delete documents
- **Multi-Document Selection**: Select specific documents to query against
- **Chat Interface**: Conversational AI powered by your documents
- **Data Source Management**: Configure databases, web pages, and file sources
- **Real-time Updates**: WebSocket support for streaming responses
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **UI**: React 19, Tailwind CSS
- **Type Safety**: TypeScript
- **API Communication**: Fetch API with proxy routes

## Getting Started

### Prerequisites

- Node.js 18+
- Backend server running at `http://localhost:8080`

### Installation

```bash
# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:3000/api" > .env.local
echo "BACKEND_URL=http://localhost:8080" >> .env.local

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Production Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx           # Home/Chat page
│   │   ├── documents/         # Document management
│   │   ├── datasources/       # Data source configuration
│   │   └── api/               # API proxy routes
│   ├── components/            # React components
│   │   ├── Chat/              # Chat interface
│   │   ├── Documents/         # Document list & upload
│   │   ├── Layout/            # Header, sidebar
│   │   └── SidePanel/         # Document selection panel
│   └── lib/                   # Utilities
│       ├── api.ts             # API client functions
│       ├── types.ts           # TypeScript interfaces
│       └── websocket.ts       # WebSocket client
├── public/                    # Static assets
└── package.json
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | API URL for client-side requests | `http://localhost:3000/api` |
| `BACKEND_URL` | Backend server URL for proxy | `http://localhost:8080` |

## Docker

The frontend is containerized and works with docker-compose:

```bash
# Build and run with docker-compose (from project root)
docker-compose up -d frontend
```

## Learn More

- [RAG System Documentation](https://nitin27may.github.io/rag/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
