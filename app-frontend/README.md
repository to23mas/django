# Frontend Setup

This directory contains all frontend (React) applications for the Django project.

## Initial Setup

Navigate to the frontend directory:
```bash
cd app-frontend
```

Install all dependencies:
```bash
# Initialize package.json
npm init -y

# Install React and Vite
npm install react react-dom @vitejs/plugin-react vite

# Install development dependencies for Tailwind
npm install -D tailwindcss postcss autoprefixer
```

## Available Scripts

In the app-frontend directory, you can run:

```bash
# Build the Hangman game
npm run build:hangman

# Run development server for Hangman
npm run dev:hangman
```

## Project Structure 