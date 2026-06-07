import 'package:flutter/material.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("FlexiHealth Dashboard"),
        automaticallyImplyLeading: false, // লগইন পেজে ব্যাক করা বন্ধ করতে
      ),
      body: const Center(
        child: Text(
          "Welcome to your Dashboard!",
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}
