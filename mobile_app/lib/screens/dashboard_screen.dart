import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Dashboard")),
      body: FutureBuilder<Map<String, dynamic>>(
        future: ApiService().getDashboardData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (snapshot.hasData) {
            final data = snapshot.data!;
            return Center(child: Text("Welcome, ${data['username']}"));
          }
          return const Center(child: Text("No Data"));
        },
      ),
    );
  }
}
