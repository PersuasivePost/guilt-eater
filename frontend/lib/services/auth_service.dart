import 'dart:convert';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;

class AuthService {
  /// Opens the backend web OAuth login URL in browser.
  Future<void> openWebOAuth() async {
    final uri = Uri.parse('http://10.0.2.2:8000/auth/google/login');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      throw 'Could not launch $uri';
    }
  }

  Future<Map<String, dynamic>?> exchangeIdTokenWithBackend(
    String idToken,
  ) async {
    final url = Uri.parse('http://10.0.2.2:8000/auth/token');
    final resp = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'id_token': idToken}),
    );
    if (resp.statusCode == 200) {
      return jsonDecode(resp.body) as Map<String, dynamic>;
    }
    return null;
  }
}
