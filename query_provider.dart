
import 'dart:io';
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/query_model.dart';

class QueryProvider extends ChangeNotifier {
  final ApiService _apiService;

  bool _isLoading = false;
  List<QueryModel> _queryHistory = [];
  String? _error;

  QueryProvider(this._apiService);

  bool get isLoading => _isLoading;
  List<QueryModel> get queryHistory => _queryHistory;
  String? get error => _error;

  Future<QueryModel> submitTextQuery(String query) async {
    _setLoading(true);
    try {
      final response = await _apiService.submitTextQuery(query, 1); // Replace with actual farmer ID
      _addToHistory(response);
      _clearError();
      return response;
    } catch (e) {
      _setError(e.toString());
      rethrow;
    } finally {
      _setLoading(false);
    }
  }

  Future<QueryModel> submitVoiceQuery(String audioPath) async {
    _setLoading(true);
    try {
      final response = await _apiService.submitVoiceQuery(File(audioPath), 1);
      _addToHistory(response);
      _clearError();
      return response;
    } catch (e) {
      _setError(e.toString());
      rethrow;
    } finally {
      _setLoading(false);
    }
  }

  Future<QueryModel> submitImageQuery(File imageFile) async {
    _setLoading(true);
    try {
      final response = await _apiService.submitImageQuery(imageFile, 1);
      _addToHistory(response);
      _clearError();
      return response;
    } catch (e) {
      _setError(e.toString());
      rethrow;
    } finally {
      _setLoading(false);
    }
  }

  Future<void> escalateQuery(int queryId, String reason) async {
    try {
      await _apiService.escalateQuery(queryId, reason);
      _clearError();
    } catch (e) {
      _setError(e.toString());
      rethrow;
    }
  }

  Future<void> submitFeedback(int queryId, int rating, String feedbackType, String comments) async {
    try {
      await _apiService.submitFeedback(queryId, rating, feedbackType, comments);
      _clearError();
    } catch (e) {
      _setError(e.toString());
      rethrow;
    }
  }

  Future<void> loadQueryHistory() async {
    _setLoading(true);
    try {
      final history = await _apiService.getQueryHistory(1); // Replace with actual farmer ID
      _queryHistory = history;
      _clearError();
    } catch (e) {
      _setError(e.toString());
    } finally {
      _setLoading(false);
    }
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  void _setError(String error) {
    _error = error;
    notifyListeners();
  }

  void _clearError() {
    _error = null;
    notifyListeners();
  }

  void _addToHistory(QueryModel query) {
    _queryHistory.insert(0, query);
    notifyListeners();
  }
}
