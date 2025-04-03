import {
    defineConfig,
    presetAttributify,
    presetIcons,
    presetTypography,
    presetUno,
    transformerDirectives,
    transformerVariantGroup
  } from 'unocss'
  
  export default defineConfig({

    presets: [
      presetUno(), 
      presetAttributify(), 
      presetIcons({ 
        scale: 1.2,
        extraProperties: {
          'display': 'inline-block',
          'vertical-align': 'middle',
        }
      }),
      presetTypography() 
    ],
  

    transformers: [
      transformerDirectives(), 
      transformerVariantGroup(), 
    ],
  
  
    theme: {
      colors: {
        primary: {
          DEFAULT: '#3B82F6', 
          light: '#93C5FD',  
          dark: '#1D4ED8'     
        }
      },
      breakpoints: {
        xs: '320px',
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px'
      }
    },
  
    shortcuts: [
      ['btn', 'px-4 py-2 rounded inline-block cursor-pointer'],
      ['btn-primary', 'btn bg-primary text-white hover:bg-primary-dark'],
      ['btn-outline', 'btn border border-primary text-primary hover:bg-primary-light'],
      
      ['card', 'rounded-lg shadow-md p-6 bg-white dark:bg-gray-800'],
      
      ['flex-center', 'flex justify-center items-center'],
      ['absolute-center', 'absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2']
    ],
  

    rules: [
      [/^text-(\d+)$/, ([, d]) => ({ 'font-size': `${d}px` })],
      ['custom-rule', { 'background-color': 'var(--primary)' }]
    ],
  

    darkMode: 'class', // Basculer avec <html class="dark">
  
    safelist: [
      ...Array.from({ length: 4 }, (_, i) => `pt-${i + 1}`), // pt-1 à pt-4
      'text-red-500',
      'i-mdi-home' 
    ],
  
 
    content: {
      pipeline: {
        include: [
          /\.(vue|svelte|[jt]sx|mdx?|astro|elm|php|phtml|html)($|\?)/,
          'src/**/*.{vue,js,ts,jsx,tsx}'
        ]
      }
    }
  })