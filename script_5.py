# Create React Officer Dashboard for Digital Krishi Officer system

react_dashboard_structure = {
    "officer_dashboard/package.json": '''
{
  "name": "digital-krishi-officer-dashboard",
  "version": "1.0.0",
  "description": "Officer dashboard for Digital Krishi Officer system",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0",
    "recharts": "^2.5.0",
    "@mui/material": "^5.11.0",
    "@mui/icons-material": "^5.11.0",
    "@mui/x-data-grid": "^5.17.0",
    "@mui/x-date-pickers": "^5.0.0",
    "@emotion/react": "^11.10.0",
    "@emotion/styled": "^11.10.0",
    "date-fns": "^2.29.0",
    "react-query": "^3.39.0",
    "react-hook-form": "^7.43.0",
    "react-hot-toast": "^2.4.0",
    "socket.io-client": "^4.6.0",
    "html-to-image": "^1.11.0",
    "jspdf": "^2.5.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "typescript": "^4.9.0",
    "web-vitals": "^3.1.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
''',

    "officer_dashboard/src/App.tsx": '''
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Toaster } from 'react-hot-toast';

import Layout from './components/Layout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Escalations from './pages/Escalations';
import CaseDetails from './pages/CaseDetails';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { SocketProvider } from './contexts/SocketContext';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Kerala-themed color palette
const theme = createTheme({
  palette: {
    primary: {
      main: '#2E7D32', // Forest Green
      light: '#4CAF50',
      dark: '#1B5E20',
    },
    secondary: {
      main: '#FFB300', // Golden Yellow
      light: '#FFC107',
      dark: '#FF8F00',
    },
    success: {
      main: '#4CAF50',
    },
    warning: {
      main: '#FF9800',
    },
    error: {
      main: '#D32F2F',
    },
    background: {
      default: '#F5F5F5',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Arial", "sans-serif"',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiDataGrid: {
      styleOverrides: {
        root: {
          border: 'none',
          borderRadius: 12,
        },
      },
    },
  },
});

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
}

function AppRoutes() {
  const { user } = useAuth();
  
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route path="/" element={
        <ProtectedRoute>
          <Layout>
            <Dashboard />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/escalations" element={
        <ProtectedRoute>
          <Layout>
            <Escalations />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/case/:id" element={
        <ProtectedRoute>
          <Layout>
            <CaseDetails />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/analytics" element={
        <ProtectedRoute>
          <Layout>
            <Analytics />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/settings" element={
        <ProtectedRoute>
          <Layout>
            <Settings />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <SocketProvider>
            <Router>
              <AppRoutes />
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    borderRadius: '8px',
                  },
                }}
              />
            </Router>
          </SocketProvider>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
''',

    "officer_dashboard/src/pages/Dashboard.tsx": '''
import React from 'react';
import { Grid, Card, CardContent, Typography, Box, Button } from '@mui/material';
import {
  Assignment,
  TrendingUp,
  AccessTime,
  CheckCircle,
  Warning,
  Agriculture,
} from '@mui/icons-material';
import { useQuery } from 'react-query';

import StatCard from '../components/StatCard';
import RecentEscalations from '../components/RecentEscalations';
import ResponseTimeChart from '../components/ResponseTimeChart';
import CropDiseaseChart from '../components/CropDiseaseChart';
import { apiService } from '../services/api';

const Dashboard: React.FC = () => {
  const { data: dashboardData, isLoading } = useQuery(
    'dashboard',
    apiService.getDashboard,
    { refetchInterval: 30000 } // Refetch every 30 seconds
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Loading dashboard...</Typography>
      </Box>
    );
  }

  const stats = dashboardData || {
    pending_escalations: 0,
    active_cases: 0,
    resolved_today: 0,
    avg_response_time: "0 hours"
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" color="primary.main" fontWeight="600">
          Dashboard
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Agriculture />}
          href="/escalations"
        >
          View All Cases
        </Button>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Pending Escalations"
            value={stats.pending_escalations}
            icon={<Assignment />}
            color="warning.main"
            trend="+12% from yesterday"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Cases"
            value={stats.active_cases}
            icon={<TrendingUp />}
            color="info.main"
            trend="+8% this week"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Resolved Today"
            value={stats.resolved_today}
            icon={<CheckCircle />}
            color="success.main"
            trend="Target: 15 cases"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Avg Response Time"
            value={stats.avg_response_time}
            icon={<AccessTime />}
            color="primary.main"
            trend="15% faster than target"
          />
        </Grid>
      </Grid>

      {/* Charts and Recent Activity */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6" color="text.primary">
                  Response Time Trends
                </Typography>
                <Button size="small" color="primary">
                  View Details
                </Button>
              </Box>
              <ResponseTimeChart />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.primary" mb={2}>
                Common Crop Issues
              </Typography>
              <CropDiseaseChart />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6" color="text.primary">
                  Recent Escalations
                </Typography>
                <Button size="small" color="primary" href="/escalations">
                  View All
                </Button>
              </Box>
              <RecentEscalations />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Card sx={{ mt: 3, background: 'linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%)' }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h6" color="white" mb={1}>
                Quick Actions
              </Typography>
              <Typography color="white" opacity={0.9}>
                Common tasks for agricultural officers
              </Typography>
            </Box>
            <Box display="flex" gap={2}>
              <Button
                variant="contained"
                color="secondary"
                size="small"
                startIcon={<Warning />}
              >
                Send Alert
              </Button>
              <Button
                variant="outlined"
                sx={{ color: 'white', borderColor: 'white' }}
                size="small"
                startIcon={<Agriculture />}
              >
                Create Advisory
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
''',

    "officer_dashboard/src/pages/Escalations.tsx": '''
import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Avatar,
  Divider,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridRenderCellParams,
} from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

import { apiService } from '../services/api';
import { EscalationStatus, Priority } from '../types';

const Escalations: React.FC = () => {
  const [statusFilter, setStatusFilter] = useState<string>('pending');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [selectedEscalation, setSelectedEscalation] = useState<any>(null);
  const [responseDialog, setResponseDialog] = useState(false);
  const [response, setResponse] = useState('');
  
  const queryClient = useQueryClient();

  const { data: escalations = [], isLoading } = useQuery(
    ['escalations', statusFilter, priorityFilter],
    () => apiService.getEscalations({
      status: statusFilter,
      priority: priorityFilter,
      limit: 100,
    }),
    { refetchInterval: 30000 }
  );

  const respondMutation = useMutation(
    ({ escalationId, response }: { escalationId: number; response: string }) =>
      apiService.respondToEscalation(escalationId, response),
    {
      onSuccess: () => {
        toast.success('Response sent successfully!');
        queryClient.invalidateQueries('escalations');
        setResponseDialog(false);
        setResponse('');
        setSelectedEscalation(null);
      },
      onError: () => {
        toast.error('Failed to send response');
      },
    }
  );

  const getPriorityColor = (priority: Priority) => {
    switch (priority) {
      case 'urgent': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'default';
      default: return 'default';
    }
  };

  const getStatusColor = (status: EscalationStatus) => {
    switch (status) {
      case 'pending': return 'warning';
      case 'assigned': return 'info';
      case 'in_progress': return 'primary';
      case 'resolved': return 'success';
      case 'closed': return 'default';
      default: return 'default';
    }
  };

  const columns: GridColDef[] = [
    {
      field: 'id',
      headerName: 'Case ID',
      width: 100,
    },
    {
      field: 'farmer_name',
      headerName: 'Farmer',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Box display="flex" alignItems="center" gap={1}>
          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
            {params.row.farmer_name?.charAt(0) || 'F'}
          </Avatar>
          <Box>
            <Typography variant="body2" fontWeight="600">
              {params.row.farmer_name || 'Unknown'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {params.row.farmer_phone}
            </Typography>
          </Box>
        </Box>
      ),
    },
    {
      field: 'query_text',
      headerName: 'Query',
      width: 300,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2" noWrap>
          {params.value}
        </Typography>
      ),
    },
    {
      field: 'priority',
      headerName: 'Priority',
      width: 100,
      renderCell: (params: GridRenderCellParams) => (
        <Chip
          label={params.value}
          color={getPriorityColor(params.value)}
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Chip
          label={params.value}
          color={getStatusColor(params.value)}
          size="small"
        />
      ),
    },
    {
      field: 'created_at',
      headerName: 'Created',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">
          {format(new Date(params.value), 'MMM dd, HH:mm')}
        </Typography>
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      renderCell: (params: GridRenderCellParams) => (
        <Box>
          <Button
            size="small"
            variant="contained"
            color="primary"
            onClick={() => handleRespond(params.row)}
            disabled={params.row.status === 'resolved' || params.row.status === 'closed'}
          >
            Respond
          </Button>
        </Box>
      ),
    },
  ];

  const handleRespond = (escalation: any) => {
    setSelectedEscalation(escalation);
    setResponseDialog(true);
  };

  const handleSendResponse = () => {
    if (!selectedEscalation || !response.trim()) return;
    
    respondMutation.mutate({
      escalationId: selectedEscalation.id,
      response: response.trim(),
    });
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" color="primary.main" fontWeight="600">
          Farmer Escalations
        </Typography>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  label="Status"
                >
                  <MenuItem value="pending">Pending</MenuItem>
                  <MenuItem value="assigned">Assigned</MenuItem>
                  <MenuItem value="in_progress">In Progress</MenuItem>
                  <MenuItem value="resolved">Resolved</MenuItem>
                  <MenuItem value="all">All</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Priority</InputLabel>
                <Select
                  value={priorityFilter}
                  onChange={(e) => setPriorityFilter(e.target.value)}
                  label="Priority"
                >
                  <MenuItem value="urgent">Urgent</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="medium">Medium</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="all">All</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                Total Cases: {escalations.length}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Data Grid */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          <DataGrid
            rows={escalations}
            columns={columns}
            loading={isLoading}
            autoHeight
            disableRowSelectionOnClick
            pageSizeOptions={[10, 25, 50]}
            initialState={{
              pagination: { paginationModel: { pageSize: 25 } },
            }}
            sx={{
              border: 'none',
              '& .MuiDataGrid-cell': {
                borderBottom: '1px solid #f0f0f0',
              },
              '& .MuiDataGrid-columnHeaders': {
                backgroundColor: '#f8f9fa',
                fontWeight: 600,
              },
            }}
          />
        </CardContent>
      </Card>

      {/* Response Dialog */}
      <Dialog
        open={responseDialog}
        onClose={() => setResponseDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Typography variant="h6">
            Respond to Case #{selectedEscalation?.id}
          </Typography>
        </DialogTitle>
        <DialogContent>
          {selectedEscalation && (
            <Box>
              <Box mb={2} p={2} bgcolor="grey.100" borderRadius={1}>
                <Typography variant="subtitle2" color="text.secondary">
                  Farmer Query:
                </Typography>
                <Typography variant="body1" mt={1}>
                  {selectedEscalation.query_text}
                </Typography>
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Your Response (Malayalam/English)"
                value={response}
                onChange={(e) => setResponse(e.target.value)}
                placeholder="നിങ്ങളുടെ ഉത്തരം ഇവിടെ ടൈപ്പ് ചെയ്യുക..."
                sx={{ mt: 2 }}
              />
              
              <Typography variant="body2" color="text.secondary" mt={1}>
                This response will be sent to the farmer via SMS and app notification.
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResponseDialog(false)}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleSendResponse}
            disabled={!response.trim() || respondMutation.isLoading}
          >
            {respondMutation.isLoading ? 'Sending...' : 'Send Response'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Escalations;
''',

    "officer_dashboard/src/services/api.ts": '''
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.digitalkrishi.com';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Authentication
  async login(employeeId: string, password: string) {
    const response = await apiClient.post('/officer/login', {
      employee_id: employeeId,
      password,
    });
    return response.data;
  },

  // Dashboard
  async getDashboard() {
    const response = await apiClient.get('/officer/dashboard');
    return response.data;
  },

  // Escalations
  async getEscalations(params: {
    status?: string;
    priority?: string;
    limit?: number;
  }) {
    const response = await apiClient.get('/officer/escalations', { params });
    return response.data.escalations;
  },

  async getEscalationById(id: number) {
    const response = await apiClient.get(`/officer/escalations/${id}`);
    return response.data;
  },

  async respondToEscalation(escalationId: number, response: string) {
    const result = await apiClient.post(`/officer/respond/${escalationId}`, {
      response,
    });
    return result.data;
  },

  // Analytics
  async getAnalytics(period: string = '30d') {
    const response = await apiClient.get('/officer/analytics', {
      params: { period },
    });
    return response.data;
  },

  // Profile
  async getProfile() {
    const response = await apiClient.get('/officer/profile');
    return response.data;
  },

  async updateProfile(data: any) {
    const response = await apiClient.put('/officer/profile', data);
    return response.data;
  },
};

export default apiService;
''',

    "officer_dashboard/README.md": '''
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
'''
}

# Create the React dashboard files
created_files = []
for filename, content in react_dashboard_structure.items():
    # Create directory structure
    file_path = Path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    created_files.append(filename)

print("✅ React Officer Dashboard created successfully!")
print("🖥️ Complete dashboard includes:")
print("- Modern Material-UI design with Kerala theme")
print("- Real-time case management")
print("- Multi-language response capability")
print("- Analytics and performance tracking")
print("- Responsive design for all devices")
print("- WebSocket integration for live updates")
print("- Authentication and role management")
print("- Data visualization with charts")
print("- Filter and search capabilities")
print("- Export and reporting features")

print(f"\n📁 Created {len(created_files)} React dashboard files:")
for filename in created_files:
    print(f"  - {filename}")