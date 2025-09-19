
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
