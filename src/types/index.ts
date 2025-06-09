export interface ColoringPage {
  id: string;
  prompt: string;
  imageUrl: string;
  createdAt: Date;
  category: string;
  style?: string;
  complexity?: string;
  likes?: number;
  downloads?: number;
  userId?: string;
}

export interface User {
  id: string;
  email: string;
  name?: string;
  credits: number;
  subscription?: Subscription;
  createdAt: Date;
}

export interface Subscription {
  id: string;
  type: 'monthly' | 'yearly';
  status: 'active' | 'cancelled' | 'expired';
  expiresAt: Date;
  createdAt: Date;
}

export interface GenerationRequest {
  prompt: string;
  category: string;
  style: string;
  complexity: string;
}

export interface GenerationResponse {
  id: string;
  imageUrl: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  error?: string;
}

export interface PaymentIntent {
  id: string;
  amount: number;
  currency: string;
  status: string;
  clientSecret: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  emoji: string;
  featured: boolean;
}

export type ComplexityLevel = 'simple' | 'medium' | 'complex';
export type ArtStyle = 'simple lines' | 'detailed' | 'cute cartoon' | 'realistic' | 'mandala' | 'geometric';

export interface ApiError {
  message: string;
  code?: string;
  status?: number;
}