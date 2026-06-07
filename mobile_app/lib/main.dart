import 'package:flutter/material.dart';
import 'screens/login_screen.dart'; // আপনার LoginScreen ফাইলটি ইমপোর্ট করলাম

void main() {
  runApp(const FlexiHealthApp());
}

class FlexiHealthApp extends StatelessWidget {
  const FlexiHealthApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // ডিবাগ ব্যানারটি সরিয়ে ফেলার জন্য
      title: 'FlexiHealth',
      theme: ThemeData(
        primarySwatch: Colors.teal, // আপনার লোগোর রঙের সাথে মিল রেখে
        useMaterial3: true,
      ),
      home: const LoginScreen(), // অ্যাপ চালু হলে সরাসরি লগইন স্ক্রিন আসবে
    );
  }
}
