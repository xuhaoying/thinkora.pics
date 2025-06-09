import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface ColoringPage {
  id: string;
  prompt: string;
  imageUrl: string;
  createdAt: Date;
  category: string;
}

interface User {
  id: string;
  email: string;
  credits: number;
  subscription?: {
    type: 'monthly' | 'yearly';
    expiresAt: Date;
  };
}

interface ColoringBookState {
  user: User | null;
  coloringPages: ColoringPage[];
  isGenerating: boolean;
  error: string | null;
}

type ColoringBookAction =
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'ADD_COLORING_PAGE'; payload: ColoringPage }
  | { type: 'SET_GENERATING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'UPDATE_CREDITS'; payload: number };

const initialState: ColoringBookState = {
  user: null,
  coloringPages: [],
  isGenerating: false,
  error: null,
};

const coloringBookReducer = (state: ColoringBookState, action: ColoringBookAction): ColoringBookState => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'ADD_COLORING_PAGE':
      return { ...state, coloringPages: [action.payload, ...state.coloringPages] };
    case 'SET_GENERATING':
      return { ...state, isGenerating: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'UPDATE_CREDITS':
      return { 
        ...state, 
        user: state.user ? { ...state.user, credits: action.payload } : null 
      };
    default:
      return state;
  }
};

const ColoringBookContext = createContext<{
  state: ColoringBookState;
  dispatch: React.Dispatch<ColoringBookAction>;
} | null>(null);

export const ColoringBookProvider = ({ children }: { children: ReactNode }) => {
  const [state, dispatch] = useReducer(coloringBookReducer, initialState);

  return (
    <ColoringBookContext.Provider value={{ state, dispatch }}>
      {children}
    </ColoringBookContext.Provider>
  );
};

export const useColoringBook = () => {
  const context = useContext(ColoringBookContext);
  if (!context) {
    throw new Error('useColoringBook must be used within a ColoringBookProvider');
  }
  return context;
};