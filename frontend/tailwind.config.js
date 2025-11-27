/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Minimalista Acadêmica
        academic: {
          // Backgrounds
          bg: '#FFFFFF',
          'bg-secondary': '#F8F9FA',
          'bg-tertiary': '#F1F3F5',

          // Texto
          text: '#1A1A1A',
          'text-secondary': '#4A5568',
          'text-muted': '#718096',

          // Borders
          border: '#E2E8F0',
          'border-strong': '#CBD5E0',
        },

        // Azul Acadêmico (cor principal)
        primary: {
          DEFAULT: '#1E40AF',    // Azul escuro acadêmico
          light: '#3B82F6',
          dark: '#1E3A8A',
          50: '#EFF6FF',
          100: '#DBEAFE',
        },

        // Cores de suporte
        accent: {
          DEFAULT: '#0EA5E9',    // Azul claro para destaques
          light: '#38BDF8',
          dark: '#0284C7',
        },

        success: {
          DEFAULT: '#059669',    // Verde sóbrio
          light: '#10B981',
          dark: '#047857',
        },

        warning: {
          DEFAULT: '#D97706',    // Laranja sóbrio
          light: '#F59E0B',
          dark: '#B45309',
        },

        danger: {
          DEFAULT: '#DC2626',    // Vermelho sóbrio
          light: '#EF4444',
          dark: '#B91C1C',
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%)',
        'gradient-accent': 'linear-gradient(135deg, #0EA5E9 0%, #38BDF8 100%)',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'DEFAULT': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'serif': ['Georgia', 'serif'],
        'mono': ['Fira Code', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-down': 'slideDown 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
