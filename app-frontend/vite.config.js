import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  root: 'hangman',
  base: '/static/hangman/',
  build: {
    outDir: path.resolve(__dirname, '../app/static/hangman'),
    assetsDir: 'assets',
    manifest: true,
  },
}); 