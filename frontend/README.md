# Guilt Eater - Frontend

Flutter mobile app for Digital Discipline (commitment-based habit control).

## Screens

- **Login Screen** (`lib/screens/login_screen.dart`) - User login with email/password
- **Signup Screen** (`lib/screens/signup_screen.dart`) - New user registration
- **Welcome Screen** (`lib/screens/welcome_screen.dart`) - Success screen showing "Login Successful! Welcome {username}"

## Current Implementation

Basic UI scaffold with navigation between screens. Auth is currently local (not yet connected to backend).

Next steps:

- Integrate Google Sign-In for Flutter
- Connect to backend `/auth/token` endpoint
- Add token storage and session management
- Implement protected routes

## Run the app

```bash
cd frontend
flutter pub get
flutter run
```

Or select a device in VS Code and press F5.

## Dev notes

- Uses Material 3 design
- Simple navigation with Navigator.push/pop
- Text field controllers properly disposed
- Ready for backend integration
