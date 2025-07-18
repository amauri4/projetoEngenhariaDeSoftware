import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        pinkDetails: "#EE4266",
        customText: '#C4CBCA',
        customText2: '#3CBBB1',
        foreground: '#2A1E5C',
        background: '#0A0F0D',
      },
    },
  },
  plugins: [],
} satisfies Config;