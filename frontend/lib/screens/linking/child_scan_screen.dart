import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../services/auth_service.dart';
import 'link_success_screen.dart';
import '../../config/app_config.dart';

class ChildScanScreen extends StatefulWidget {
  const ChildScanScreen({super.key});

  @override
  State<ChildScanScreen> createState() => _ChildScanScreenState();
}

class _ChildScanScreenState extends State<ChildScanScreen> {
  final MobileScannerController _scannerController = MobileScannerController();
  final _authService = AuthService();
  bool _isProcessing = false;
  String? _errorMessage;

  @override
  void dispose() {
    _scannerController.dispose();
    super.dispose();
  }

  Future<void> _handleQRCode(String qrData) async {
    if (_isProcessing) return;

    setState(() {
      _isProcessing = true;
      _errorMessage = null;
    });

    try {
      // QR data format: "parent_id:code" or just "code"
      String code;
      if (qrData.contains(':')) {
        code = qrData.split(':').last;
      } else {
        code = qrData;
      }

      // Validate code format (should be 6 digits)
      if (code.length != 6 || !RegExp(r'^\d+$').hasMatch(code)) {
        throw Exception('Invalid QR code format');
      }

      final token = await _authService.getToken();
      if (token == null) {
        throw Exception('Not authenticated');
      }

      // Call backend to verify and link
      final response = await http.post(
        // Use http://10.0.2.2:8000 for Android emulator, or your local IP for real device
        // Example emulator: Uri.parse('http://10.0.2.2:8000/api/linking/verify-linking-code')
        // Example local device: Uri.parse('http://192.168.1.40:8000/api/linking/verify-linking-code')
        Uri.parse(AppConfig.verifyLinkingCodeUrl),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'code': code}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (mounted) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => LinkSuccessScreen(
                parentName: data['parent_name'] ?? 'Parent',
                childName: data['child_name'] ?? 'Child',
              ),
            ),
          );
        }
      } else {
        final error = jsonDecode(response.body);
        throw Exception(error['detail'] ?? 'Failed to verify code');
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isProcessing = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(_errorMessage ?? 'Error processing QR code'),
            backgroundColor: Colors.red,
          ),
        );
      }

      // Allow scanning again after 2 seconds
      await Future.delayed(const Duration(seconds: 2));
      setState(() {
        _isProcessing = false;
        _errorMessage = null;
      });
    }
  }

  void _enterManually() {
    // Navigate back to child login screen (manual code entry)
    Navigator.pop(context);
  }

  void _cancel() {
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Column(
          children: [
            // Header with Cancel button
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  TextButton(
                    onPressed: _cancel,
                    child: const Text(
                      'Cancel',
                      style: TextStyle(color: Colors.white70, fontSize: 16),
                    ),
                  ),
                  const Spacer(),
                  if (_isProcessing)
                    const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    ),
                ],
              ),
            ),

            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Title
                    const Text(
                      "Scan Parent's QR Code",
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Instructions
                    const Text(
                      'Point your camera at the QR code',
                      style: TextStyle(fontSize: 16, color: Colors.white70),
                    ),
                    const SizedBox(height: 40),

                    // Camera View
                    Container(
                      width: 280,
                      height: 280,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.white30, width: 2),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      clipBehavior: Clip.hardEdge,
                      child: Stack(
                        children: [
                          MobileScanner(
                            controller: _scannerController,
                            onDetect: (capture) {
                              final List<Barcode> barcodes = capture.barcodes;
                              for (final barcode in barcodes) {
                                if (barcode.rawValue != null &&
                                    !_isProcessing) {
                                  _handleQRCode(barcode.rawValue!);
                                  break;
                                }
                              }
                            },
                          ),

                          // Scanning frame overlay
                          Center(
                            child: Container(
                              width: 200,
                              height: 200,
                              decoration: BoxDecoration(
                                border: Border.all(
                                  color: _isProcessing
                                      ? Colors.green
                                      : Colors.white,
                                  width: 3,
                                ),
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),

                          // Error overlay
                          if (_errorMessage != null)
                            Container(
                              color: Colors.black87,
                              child: Center(
                                child: Padding(
                                  padding: const EdgeInsets.all(16.0),
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      const Icon(
                                        Icons.error_outline,
                                        color: Colors.red,
                                        size: 48,
                                      ),
                                      const SizedBox(height: 16),
                                      Text(
                                        _errorMessage!,
                                        textAlign: TextAlign.center,
                                        style: const TextStyle(
                                          color: Colors.white,
                                          fontSize: 16,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 40),

                    // Manual Entry Button
                    TextButton(
                      onPressed: _isProcessing ? null : _enterManually,
                      child: const Text(
                        'Enter Code Manually',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 16,
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
