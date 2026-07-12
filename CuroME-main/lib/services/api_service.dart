import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';

class ApiService {
  ApiService._internal() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      // Default header for most requests
      headers: {'Content-Type': 'application/json'},
    ));
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final prefs = await SharedPreferences.getInstance();
        final token = prefs.getString('session_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
    ));
  }

  static final ApiService instance = ApiService._internal();
  late final Dio _dio;

  static const String baseUrl = 'http://10.0.2.2:8000';

  // ── Auth ──
  // Correctly uses form-url-encoded and handles token storage
  Future<Response> login(String email, String password) async {
    final response = await _dio.post(
      '/auth/login',
      data: {
        'username': email,
        'password': password,
      },
      options: Options(
        contentType: Headers.formUrlEncodedContentType,
      ),
    );

    if (response.statusCode == 200) {
      final token = response.data['access_token'];
      if (token != null) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('session_token', token);
      }
    }
    return response;
  }

  Future<Response> register(StoredAccount account) =>
      _dio.post('/auth/register', data: account.toJson());

  // ── Patients ──
  Future<Response> getPatients() => _dio.get('/patients');
  Future<Response> getPatient(String id) => _dio.get('/patients/$id');

  // ── Mood ──
  Future<Response> postMoodEntry(String patientId, int mood) => _dio.post(
        '/patients/$patientId/mood',
        data: {'mood': mood},
      );
  Future<Response> getMoodHistory(String patientId) =>
      _dio.get('/patients/$patientId/mood');

  // ── Appointments / slots ──
  Future<Response> getSlots(String doctorId) =>
      _dio.get('/doctors/$doctorId/slots');
  Future<Response> createSlot(Map<String, dynamic> payload) =>
      _dio.post('/slots', data: payload);
  Future<Response> updateSlot(String slotId, Map<String, dynamic> payload) =>
      _dio.patch('/slots/$slotId', data: payload);

  // ── Messages ──
  Future<Response> getThread(String threadId) =>
      _dio.get('/messages/$threadId');
  Future<Response> sendMessage(String threadId, String text) => _dio.post(
        '/messages/$threadId',
        data: {'text': text},
      );

  // ── Suggestions ──
  Future<Response> postSuggestion(Map<String, dynamic> payload) =>
      _dio.post('/suggestions', data: payload);

  // ── SOS ──
  Future<Response> assignDoctor(String patientId, String doctorId) =>
      _dio.post('/assignments', data: {
        'patient_id': patientId,
        'doctor_id': doctorId,
      });

  Future<Response> triggerSos(String patientId) =>
      _dio.post('/patients/$patientId/sos');
}