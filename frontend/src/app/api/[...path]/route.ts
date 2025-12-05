import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8080';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const pathString = path.join('/');
  const url = new URL(request.url);
  const queryString = url.search;
  
  // Add trailing slash to match FastAPI's redirect behavior
  const targetPath = pathString.endsWith('/') ? pathString : `${pathString}/`;
  
  try {
    const response = await fetch(`${BACKEND_URL}/api/${targetPath}${queryString}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      redirect: 'follow',
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to proxy request' }, { status: 500 });
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const pathString = path.join('/');
  // Don't add trailing slash for POST - FastAPI doesn't redirect POST requests cleanly
  // with multipart data (boundary gets corrupted)
  
  try {
    // Forward all headers except host
    const headers: Record<string, string> = {};
    request.headers.forEach((value, key) => {
      if (key.toLowerCase() !== 'host') {
        headers[key] = value;
      }
    });
    
    // For multipart/form-data, stream the body directly to preserve boundaries
    // This avoids the issue where Node.js FormData re-encoding corrupts large files
    const response = await fetch(`${BACKEND_URL}/api/${pathString}`, {
      method: 'POST',
      headers,
      body: request.body,
      // @ts-expect-error - duplex is required for streaming body in Node.js fetch
      duplex: 'half',
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to proxy request' }, { status: 500 });
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const pathString = path.join('/');
  const targetPath = pathString.endsWith('/') ? pathString : `${pathString}/`;
  
  try {
    const body = await request.text();
    const response = await fetch(`${BACKEND_URL}/api/${targetPath}`, {
      method: 'PUT',
      headers: {
        'Content-Type': request.headers.get('content-type') || 'application/json',
      },
      body,
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to proxy request' }, { status: 500 });
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const pathString = path.join('/');
  const targetPath = pathString.endsWith('/') ? pathString : `${pathString}/`;
  
  try {
    const response = await fetch(`${BACKEND_URL}/api/${targetPath}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      redirect: 'follow',
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to proxy request' }, { status: 500 });
  }
}
