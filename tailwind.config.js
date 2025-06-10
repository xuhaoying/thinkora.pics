/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f8f6ff',
          100: '#f1ecfe',
          200: '#e4dafd',
          300: '#d2bffc',
          400: '#bb9af9',
          500: '#a472f5',
          600: '#8b4bef',
          700: '#7a3be2',
          800: '#6532be',
          900: '#542b9b',
          950: '#341a68',
        },
        surface: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#0a0a0a',
        }
      },
      animation: {
        'gradient': 'gradient 8s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slide-up 0.6s ease-out',
        'fade-in': 'fade-in 0.6s ease-out',
        'scale-in': 'scale-in 0.3s ease-out',
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        },
        glow: {
          '0%': { 'box-shadow': '0 0 20px rgb(168 85 247 / 0.4)' },
          '100%': { 'box-shadow': '0 0 30px rgb(168 85 247 / 0.8)' }
        },
        'slide-up': {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        'scale-in': {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'mesh-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      },
      fontFamily: {
        'display': ['Inter', 'system-ui', 'sans-serif'],
        'body': ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      }
    },
  },
  plugins: [],
};
