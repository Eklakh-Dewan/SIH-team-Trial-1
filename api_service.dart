
import 'dart:io';
import 'package:dio/dio.dart';
import '../models/query_model.dart';

class ApiService {
  late Dio _dio;
  static const String baseUrl = 'https://api.digitalkrishi.com'; // Replace with actual URL

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
    ));

    _dio.interceptors.add(LogInterceptor());
  }

  Future<Map<String, dynamic>> login(String phone) async {
    final response = await _dio.post('/auth/login', data: {'phone': phone});
    return response.data;
  }

  Future<Map<String, dynamic>> verifyOTP(String phone, String otp) async {
    final response = await _dio.post('/auth/verify', data: {
      'phone': phone,
      'otp': otp,
    });
    return response.data;
  }

  Future<QueryModel> submitTextQuery(String query, int farmerId) async {
    final response = await _dio.post('/query', data: {
      'farmer_id': farmerId,
      'query_text': query,
      'query_type': 'text',
    });
    return QueryModel.fromJson(response.data);
  }

  Future<QueryModel> submitVoiceQuery(File audioFile, int farmerId) async {
    final formData = FormData.fromMap({
      'farmer_id': farmerId,
      'query_type': 'voice',
      'voice_file': await MultipartFile.fromFile(audioFile.path),
    });

    final response = await _dio.post('/query', data: formData);
    return QueryModel.fromJson(response.data);
  }

  Future<QueryModel> submitImageQuery(File imageFile, int farmerId) async {
    final formData = FormData.fromMap({
      'farmer_id': farmerId,
      'query_type': 'image',
      'image_file': await MultipartFile.fromFile(imageFile.path),
    });

    final response = await _dio.post('/query', data: formData);
    return QueryModel.fromJson(response.data);
  }

  Future<void> escalateQuery(int queryId, String reason) async {
    await _dio.post('/escalate', data: {
      'query_id': queryId,
      'reason': reason,
    });
  }

  Future<void> submitFeedback(int queryId, int rating, String feedbackType, String comments) async {
    await _dio.post('/feedback', data: {
      'query_id': queryId,
      'rating': rating,
      'feedback_type': feedbackType,
      'comments': comments,
    });
  }

  Future<List<QueryModel>> getQueryHistory(int farmerId, {int limit = 20, int offset = 0}) async {
    final response = await _dio.get('/history/$farmerId', queryParameters: {
      'limit': limit,
      'offset': offset,
    });

    return (response.data['queries'] as List)
        .map((json) => QueryModel.fromJson(json))
        .toList();
  }
}
