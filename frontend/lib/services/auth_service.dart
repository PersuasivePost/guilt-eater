import 'dart:convert';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';

class AuthService {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile'],
    // IMPORTANT: Use your Android OAuth Client ID from Google Cloud Console
    // This must match the GOOGLE_CLIENT_ID in your backend .env file
    serverClientId:
        '819909728307-6n4mrr6n91srqjukjqlsm48p42s78kvi.apps.googleusercontent.com',
  );
  final _storage = const FlutterSecureStorage();
  static const String _tokenKey = 'access_token';
  // Use 10.0.2.2 for Android emulator to reach host machine's localhost
  static const String _backendUrl = 'http://10.0.2.2:8000';

  /// Sign in with Google and get JWT from backend
  /// [role] can be 'individual', 'parent', or 'child'
  Future<String?> signInWithGoogle({String role = 'individual'}) async {
    try {
  debugPrint('Starting Google Sign-In with role: $role...');

      // Try silent sign-in first (returns previously signed in account if available)
      GoogleSignInAccount? account = await _googleSignIn.signInSilently();

      // If silent sign-in didn't return an account, prompt the user
      account ??= await _googleSignIn.signIn();

      if (account == null) {
        debugPrint('User cancelled sign-in');
        return null;
      }

      debugPrint('Google account signed in: ${account.email}');

      // Get authentication details
      final GoogleSignInAuthentication auth = await account.authentication;
      final String? idToken = auth.idToken;

      if (idToken == null) {
        throw Exception('Failed to get ID token from Google');
      }

  debugPrint('Got ID token, exchanging with backend at $_backendUrl/auth/token');

      // Exchange id_token with backend for our JWT, including role
      final response = await http
          .post(
            Uri.parse('$_backendUrl/auth/token'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'id_token': idToken, 'role': role}),
          )
          .timeout(
            const Duration(seconds: 10),
            onTimeout: () {
              throw Exception(
                'Backend connection timeout. Make sure backend is running on port 8000',
              );
            },
          );

  debugPrint('Backend response status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final accessToken = data['access_token'] as String;

        // Store the token securely
        await _storage.write(key: _tokenKey, value: accessToken);

  debugPrint('Successfully got JWT token for role: $role');
        return accessToken;
      } else {
  debugPrint('Backend error: ${response.statusCode} - ${response.body}');
        throw Exception('Backend auth failed: ${response.body}');
      }
    } on PlatformException catch (e) {
      // PlatformException may wrap Google Play services errors (ApiException)
      debugPrint(
        'PlatformException during Google Sign-In: ${e.code} - ${e.message}',
      );

      // ApiException code 7 is a network/play-services error on Android
      if (e.code == 'network_error' ||
          (e.message != null && e.message!.contains('ApiException: 7'))) {
        throw Exception(
          'Google Sign-In failed with network/Play Services error (ApiException 7). '
          'Check emulator/device internet, ensure AVD uses a Google Play image and has a Google account, or test on a physical device.',
        );
      }

      rethrow;
    } catch (e) {
  debugPrint('Sign in error: $e');
      rethrow;
    }
  }

  /// Sign out
  Future<void> signOut() async {
    await _googleSignIn.signOut();
    await _storage.delete(key: _tokenKey);
  }

  /// Get stored token
  Future<String?> getToken() async {
    return await _storage.read(key: _tokenKey);
  }

  /// Check if user is signed in
  Future<bool> isSignedIn() async {
    final token = await getToken();
    return token != null;
  }
}
