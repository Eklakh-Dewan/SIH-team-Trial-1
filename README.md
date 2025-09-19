
# Digital Krishi Officer - Mobile App

AI-based farmer query support system for Kerala, India.

## Features

- **Malayalam-first Interface**: Complete Malayalam localization with proper fonts
- **Voice Queries**: Record questions in Malayalam with ASR processing
- **Text Queries**: Type questions in Malayalam or English
- **Image Analysis**: Capture crop disease photos for AI analysis
- **Audio Responses**: Text-to-speech playback in Malayalam
- **Officer Escalation**: Send complex queries to agricultural officers
- **Query History**: Track all past queries and responses
- **Offline Support**: Cache responses for offline access
- **Location-based**: GPS integration for location-specific advice

## Tech Stack

- **Framework**: Flutter 3.x
- **State Management**: Provider + BLoC
- **Audio**: record, just_audio, flutter_tts
- **Camera**: camera, image_picker
- **Networking**: dio, http
- **Storage**: hive, shared_preferences
- **UI**: Material Design 3 with Kerala-themed colors

## Setup

1. Install Flutter SDK
2. Run `flutter pub get`
3. Configure Firebase (authentication)
4. Update API endpoints in `lib/services/api_service.dart`
5. Add Malayalam TTS voice if needed
6. Run `flutter run`

## Malayalam Fonts

The app uses Manjari and AnjaliOldLipi fonts for proper Malayalam rendering. Make sure to include these fonts in the assets folder.

## Permissions

- Microphone: Voice recording
- Camera: Image capture
- Storage: File management
- Location: Location-based advice

## Build for Production

```bash
# Android
flutter build apk --release

# iOS  
flutter build ios --release
```

## Architecture

- **Services**: API calls, audio processing, local storage
- **Providers**: State management with ChangeNotifier
- **Models**: Data classes for queries, responses, etc.
- **Screens**: Main UI screens (login, home, query, history)
- **Widgets**: Reusable UI components
- **Core**: Themes, localization, constants
