# HumanizeAI Frontend

React + TypeScript frontend for the HumanizeAI platform.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
copy .env.example .env
```

Edit `.env` and set:
```env
VITE_API_URL=http://localhost:5000
```

### 3. Run Development Server

```bash
npm run dev
```

Application will be available at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

Built files will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Tech Stack

- **React 19**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling (via CDN)
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **Font Awesome**: Icons

## Project Structure

```
src/
├── components/
│   ├── Header.tsx           # Navigation header
│   ├── TextInput.tsx        # Main input form
│   └── ResultsDashboard.tsx # Results display
├── services/
│   └── api.ts              # API client
├── types/
│   └── index.ts            # TypeScript types
├── App.tsx                 # Main app component
├── main.tsx                # Entry point
└── vite-env.d.ts          # Vite environment types
```

## Features

- Real-time text humanization
- Multiple strategy selection
- Visual metrics dashboard
- Before/after comparison
- History tracking
- Responsive design

## Troubleshooting

**Port already in use:**
```bash
# Change port in vite.config.ts or use:
npm run dev -- --port 3001
```

**Cannot connect to backend:**
- Ensure backend is running on port 5000
- Check VITE_API_URL in .env
- Check browser console for CORS errors

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```
