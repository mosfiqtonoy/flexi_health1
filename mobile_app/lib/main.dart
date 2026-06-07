import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'screens/login_screen.dart';
import 'screens/dashboard_screen.dart';

void main() async {
 
  WidgetsFlutterBinding.ensureInitialized();

 
  final prefs = await SharedPreferences.getInstance();
  final userId = prefs.getString('user_id');

  
  runApp(FlexiHealthApp(isLoggedIn: userId != null));
}

class FlexiHealthApp extends StatelessWidget {
  final bool isLoggedIn;
  
  const FlexiHealthApp({super.key, required this.isLoggedIn});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'FlexiHealth',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        useMaterial3: true,
      ),
      
      home: isLoggedIn ? const DashboardScreen() : const LoginScreen(),
    );
  }
}
