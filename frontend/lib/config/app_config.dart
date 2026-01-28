/// Application configuration
///
/// To change the backend URL:
/// 1. Update the _baseUrl constant below with your IP address
/// 2. Keep http://10.0.2.2:8000 for Android emulator
/// 3. Use your local IP (e.g., http://10.0.44.25) for real devices on same network
class AppConfig {
  // ⚠️ CHANGE THIS URL BASED ON YOUR TESTING ENVIRONMENT
  // For Android Emulator: http://10.0.2.2:8000
  // For Real Device (same network): http://YOUR_LOCAL_IP (e.g., http://192.168.1.40)
  static const String _baseUrl = 'http://192.168.1.40:8000';

  // Alternative URLs (uncomment the one you need)
  // static const String _baseUrl = 'http://10.0.2.2:8000';  // Android Emulator
  // static const String _baseUrl = 'http://192.168.1.100:8000';  // Example: Your laptop IP

  /// Get the base backend URL
  static String get baseUrl => _baseUrl;

  /// Get full URL for an API endpoint
  static String getApiUrl(String endpoint) {
    // Remove leading slash if present to avoid double slashes
    final cleanEndpoint = endpoint.startsWith('/')
        ? endpoint.substring(1)
        : endpoint;
    return '$_baseUrl/$cleanEndpoint';
  }

  // Common API endpoints
  static String get authTokenUrl => getApiUrl('auth/token');
  static String get userMeUrl => getApiUrl('api/me');
  static String get generateLinkingCodeUrl =>
      getApiUrl('api/linking/generate-linking-code');
  static String get verifyLinkingCodeUrl =>
      getApiUrl('api/linking/verify-linking-code');
}
