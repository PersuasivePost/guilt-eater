import 'package:flutter/material.dart';

class ChildScanScreen extends StatefulWidget {
  const ChildScanScreen({super.key});

  @override
  State<ChildScanScreen> createState() => _ChildScanScreenState();
}

class _ChildScanScreenState extends State<ChildScanScreen> {
  final bool _isScanning = false;

  void _enterManually() {
    // Navigate to child login screen (manual code entry)
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
                    const SizedBox(height: 40),

                    // Camera View Placeholder
                    Container(
                      width: 280,
                      height: 280,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.white30, width: 2),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Stack(
                        children: [
                          // Camera placeholder
                          Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.qr_code_scanner,
                                  size: 80,
                                  color: Colors.white30,
                                ),
                                const SizedBox(height: 16),
                                const Text(
                                  'Camera View',
                                  style: TextStyle(
                                    color: Colors.white30,
                                    fontSize: 16,
                                  ),
                                ),
                              ],
                            ),
                          ),

                          // Scanning frame
                          Center(
                            child: Container(
                              width: 200,
                              height: 200,
                              decoration: BoxDecoration(
                                border: Border.all(
                                  color: Colors.white,
                                  width: 3,
                                ),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Center(
                                child: _isScanning
                                    ? const CircularProgressIndicator(
                                        color: Colors.white,
                                      )
                                    : const Text(
                                        'Scanning\nArea',
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          color: Colors.white70,
                                          fontSize: 16,
                                          fontWeight: FontWeight.w500,
                                        ),
                                      ),
                              ),
                            ),
                          ),

                          // Corner markers
                          ..._buildCornerMarkers(),
                        ],
                      ),
                    ),
                    const SizedBox(height: 32),

                    // Instructions
                    const Text(
                      'Position QR code\nwithin the frame',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 16, color: Colors.white70),
                    ),
                    const SizedBox(height: 40),

                    // Manual Entry Button
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: OutlinedButton(
                        onPressed: _enterManually,
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(
                            color: Colors.white30,
                            width: 1,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                        child: const Text(
                          'Enter Code Manually',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.w500,
                          ),
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

  List<Widget> _buildCornerMarkers() {
    return [
      // Top-left
      Positioned(top: 30, left: 30, child: _buildCorner(topLeft: true)),
      // Top-right
      Positioned(top: 30, right: 30, child: _buildCorner(topRight: true)),
      // Bottom-left
      Positioned(bottom: 30, left: 30, child: _buildCorner(bottomLeft: true)),
      // Bottom-right
      Positioned(bottom: 30, right: 30, child: _buildCorner(bottomRight: true)),
    ];
  }

  Widget _buildCorner({
    bool topLeft = false,
    bool topRight = false,
    bool bottomLeft = false,
    bool bottomRight = false,
  }) {
    return Container(
      width: 20,
      height: 20,
      decoration: BoxDecoration(
        border: Border(
          top: (topLeft || topRight)
              ? const BorderSide(color: Colors.white, width: 3)
              : BorderSide.none,
          left: (topLeft || bottomLeft)
              ? const BorderSide(color: Colors.white, width: 3)
              : BorderSide.none,
          right: (topRight || bottomRight)
              ? const BorderSide(color: Colors.white, width: 3)
              : BorderSide.none,
          bottom: (bottomLeft || bottomRight)
              ? const BorderSide(color: Colors.white, width: 3)
              : BorderSide.none,
        ),
      ),
    );
  }
}
