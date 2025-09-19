
# Digital Krishi Officer - Officer Dashboard

React-based dashboard for agricultural officers to manage farmer escalations and provide expert advice.

## Features

- **Real-time Dashboard**: Live statistics and metrics
- **Case Management**: Handle escalated farmer queries
- **Multi-language Support**: Respond in Malayalam or English
- **Analytics**: Performance tracking and insights
- **Mobile Responsive**: Works on tablets and mobile devices
- **Real-time Notifications**: WebSocket integration for instant updates

## Tech Stack

- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) v5
- **State Management**: React Query + Context API
- **Charts**: Recharts for data visualization
- **Real-time**: Socket.io for live updates
- **Authentication**: JWT-based auth
- **Build Tool**: Create React App

## Key Components

### Dashboard
- Overview of pending cases
- Performance metrics
- Quick actions
- Response time analytics

### Escalations
- List of all escalated cases
- Filter by status and priority
- In-line response capability
- Case details with farmer information

### Analytics
- Response time trends
- Common crop issues
- Officer performance metrics
- Historical data analysis

## Setup and Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set environment variables:
   ```bash
   REACT_APP_API_URL=https://api.digitalkrishi.com
   REACT_APP_SOCKET_URL=wss://api.digitalkrishi.com
   ```

3. Run development server:
   ```bash
   npm start
   ```

4. Build for production:
   ```bash
   npm run build
   ```

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_SOCKET_URL`: WebSocket server URL
- `REACT_APP_VERSION`: Application version

## Authentication

Officers log in using their employee ID and password. The system supports:
- Session management
- Role-based access control
- Automatic token refresh
- Secure logout

## Real-time Features

- Live case updates
- Instant notifications
- Real-time chat with farmers
- Status change broadcasts

## Deployment

The dashboard can be deployed on:
- Vercel/Netlify (static hosting)
- AWS S3 + CloudFront
- Docker containers
- Traditional web servers

Build the app and serve the static files from the `build` directory.

## Performance

- Code splitting for optimal loading
- Lazy loading of routes
- Image optimization
- Caching strategies
- Progressive Web App capabilities
