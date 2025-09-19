
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:permission_handler/permission_handler.dart';

import 'core/app_theme.dart';
import 'core/localization.dart';
import 'services/api_service.dart';
import 'services/audio_service.dart';
import 'services/storage_service.dart';
import 'providers/auth_provider.dart';
import 'providers/query_provider.dart';
import 'screens/splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/query_screen.dart';
import 'screens/history_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp();

  // Initialize Hive
  await Hive.initFlutter();

  // Request permissions
  await _requestPermissions();

  // Set preferred orientations
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);

  runApp(const DigitalKrishiOfficerApp());
}

Future<void> _requestPermissions() async {
  await [
    Permission.microphone,
    Permission.camera,
    Permission.storage,
    Permission.location,
  ].request();
}

class DigitalKrishiOfficerApp extends StatelessWidget {
  const DigitalKrishiOfficerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<ApiService>(create: (_) => ApiService()),
        Provider<AudioService>(create: (_) => AudioService()),
        Provider<StorageService>(create: (_) => StorageService()),
        ChangeNotifierProvider<AuthProvider>(
          create: (context) => AuthProvider(context.read<ApiService>()),
        ),
        ChangeNotifierProvider<QueryProvider>(
          create: (context) => QueryProvider(context.read<ApiService>()),
        ),
      ],
      child: MaterialApp(
        title: 'ഡിജിറ്റൽ കൃഷി ഓഫീസർ',
        theme: AppTheme.lightTheme,
        locale: const Locale('ml', 'IN'),
        supportedLocales: const [
          Locale('ml', 'IN'), // Malayalam
          Locale('en', 'US'), // English
        ],
        home: const SplashScreen(),
        routes: {
          '/login': (context) => const LoginScreen(),
          '/home': (context) => const HomeScreen(),
          '/query': (context) => const QueryScreen(),
          '/history': (context) => const HistoryScreen(),
        },
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
