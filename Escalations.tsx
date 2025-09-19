
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
