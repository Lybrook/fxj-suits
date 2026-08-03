# FXJ Suits — Setup and Run Guide

Welcome to the **FXJ Suits** Law Firm Management System. This guide provides step-by-step instructions on how to set up the development environment, configure the backend, and run the project locally.

---

## 1. Prerequisites

Before you begin, ensure you have the following installed on your machine:
* **Node.js** (v18.0.0 or higher recommended)
* **npm** (comes with Node.js) or **yarn**
* **Git**
* A modern web browser (Chrome, Firefox, Edge, or Safari)

## 2. Project Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Lybrook/fxj-suits.git
   cd fxj-suits
   ```

2. **Install dependencies**:
   Run the following command to install all required packages:
   ```bash
   npm install
   ```
   *(Note: If you encounter peer dependency warnings, you can safely run `npm install --legacy-peer-deps` or `npm audit fix --force` as suggested by npm).*

## 3. Environment Configuration

FXJ Suits relies on **Supabase** for its backend (authentication, database, and storage). You need to configure your environment variables to connect to your Supabase instance.

1. **Create the environment file**:
   Copy the provided example file to create your local `.env` file:
   ```bash
   cp .env.example .env
   ```

2. **Configure Supabase**:
   Open the `.env` file in your preferred text editor and update the following values with your Supabase project credentials:
   ```env
   VITE_SUPABASE_URL=https://your-project-id.supabase.co
   VITE_SUPABASE_ANON_KEY=your-anon-public-key-here
   VITE_SUPABASE_SERVICE_KEY=your-service-role-key-here
   ```
   *You can find these keys in your Supabase Dashboard under **Project Settings → API**.*

## 4. Running the Application Locally

Once the dependencies are installed and the environment is configured, you can start the local development server.

1. **Start the development server**:
   ```bash
   npm run dev
   ```

2. **Access the application**:
   Open your web browser and navigate to the URL provided in your terminal, typically:
   ```
   http://localhost:5173
   ```

## 5. Building for Production

When you are ready to deploy the application, you need to create an optimized production build.

1. **Run the build command**:
   ```bash
   npm run build
   ```
   This will generate a `dist/` directory containing the minified and optimized assets, ready to be served by any static file hosting service (e.g., Vercel, Netlify, or AWS S3).

2. **Preview the production build locally**:
   ```bash
   npm run preview
   ```

## 6. Architecture & Tech Stack

* **Frontend Framework**: React 18 with TypeScript
* **Build Tool**: Vite
* **Styling**: Tailwind CSS (customized with the FXJ Suits Gold Palette)
* **Backend/Database**: Supabase (PostgreSQL)
* **Icons**: Lucide React
* **Animations**: Framer Motion
* **PWA Support**: Vite PWA Plugin

## 7. Troubleshooting

* **Blank screen on load**: Ensure your `.env` variables are correctly set and that your Supabase project is active.
* **Module not found errors**: Run `npm install` again to ensure all dependencies are downloaded.
* **Styling issues**: If Tailwind classes aren't applying, ensure you haven't modified the `tailwind.config.js` content paths incorrectly.

---
*Powered by [Fikia × Jenga Tech](https://fikiaxjenga.co.ke/)*
)*
