import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../services/auth_service.dart';
import '../welcome_screen.dart';
import '../../config/app_config.dart';

class ParentLinkScreen extends StatefulWidget {
  const ParentLinkScreen({super.key});

  @override
  State<ParentLinkScreen> createState() => _ParentLinkScreenState();
}

class _ParentLinkScreenState extends State<ParentLinkScreen> {
  final _authService = AuthService();
  String? linkingCode;
  String? qrData;
  String? parentName;
  String? expiresAt;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _generateLinkingCode();
  }

  Future<void> _generateLinkingCode() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final token = await _authService.getToken();
      if (token == null) {
        throw Exception('Not authenticated');
      }

      final response = await http.post(
        // Use 10.0.2.2:8000 for Android emulator, or your local IP for real device
        // Uri.parse('http://10.0.2.2:8000/api/linking/generate-linking-code'),
        // Uri.parse('http://192.168.1.40:8000/api/linking/generate-linking-code'),
        Uri.parse(AppConfig.generateLinkingCodeUrl),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          linkingCode = data['code'];
          qrData = data['qr_data'];
          parentName = data['parent_name'];
          expiresAt = data['expires_at'];
          _isLoading = false;
        });
      } else {
        throw Exception('Failed to generate code: ${response.body}');
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  void _copyCode() {
    if (linkingCode != null) {
      Clipboard.setData(ClipboardData(text: linkingCode!));
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Code copied to clipboard'),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 2),
        ),
      );
    }
  }

  void _doLater() {
    // Navigate to welcome screen
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => WelcomeScreen(username: parentName ?? 'User'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: _isLoading
            ? const Center(
                child: CircularProgressIndicator(color: Colors.white),
              )
            : _error != null
            ? Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error, color: Colors.red, size: 60),
                    const SizedBox(height: 16),
                    Text(
                      'Failed to generate code',
                      style: const TextStyle(color: Colors.white, fontSize: 18),
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton(
                      onPressed: _generateLinkingCode,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              )
            : Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Spacer(),

                    // Title
                    const Text(
                      'Link Your Child',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Subtitle
                    const Text(
                      'Share this code or QR\nwith your child:',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 16, color: Colors.white70),
                    ),
                    const SizedBox(height: 40),

                    // QR Code
                    if (qrData != null)
                      Container(
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: QrImageView(
                          data: qrData!,
                          version: QrVersions.auto,
                          size: 200.0,
                          backgroundColor: Colors.white,
                          // updated: use eyeStyle and dataModuleStyle instead of deprecated foregroundColor
                          eyeStyle: QrEyeStyle(
                            eyeShape: QrEyeShape.square,
                            color: Colors.black,
                          ),
                          dataModuleStyle: QrDataModuleStyle(
                            dataModuleShape: QrDataModuleShape.square,
                            color: Colors.black,
                          ),
                        ),
                      ),
                    const SizedBox(height: 32),

                    // Code Display
                    const Text(
                      'Code:',
                      style: TextStyle(fontSize: 14, color: Colors.white70),
                    ),
                    const SizedBox(height: 8),
                    if (linkingCode != null)
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: linkingCode!.split('').map((digit) {
                          return Container(
                            margin: const EdgeInsets.symmetric(horizontal: 4),
                            width: 40,
                            height: 50,
                            decoration: BoxDecoration(
                              border: Border.all(
                                color: Colors.white30,
                                width: 1,
                              ),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Center(
                              child: Text(
                                digit,
                                style: const TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    const SizedBox(height: 16),

                    // Copy Code Button
                    TextButton(
                      onPressed: _copyCode,
                      child: const Text(
                        'Copy Code',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 16,
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                    const SizedBox(height: 32),

                    // Do Later Button
                    TextButton(
                      onPressed: _doLater,
                      child: const Text(
                        "I'll Do Later",
                        style: TextStyle(color: Colors.white54, fontSize: 16),
                      ),
                    ),

                    const Spacer(),
                  ],
                ),
              ),
      ),
    );
  }
}
