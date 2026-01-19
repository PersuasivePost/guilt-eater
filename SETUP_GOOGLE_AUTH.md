# Google Authentication Setup Guide

## Prerequisites

You need to configure Google OAuth credentials in Google Cloud Console for the app to work.

## Google Cloud Console Setup

### 1. Create/Select Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one

### 2. Enable Google Sign-In API

1. Navigate to **APIs & Services > Library**
2. Search for "Google Sign-In API" or "Google+ API"
3. Click **Enable**

### 3. Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**
2. Choose **External** user type
3. Fill in required fields:
   - App name: "Guilt Eater"
   - User support email: your email
   - Developer contact: your email
4. Add scopes: `email`, `profile`, `openid`
5. Save and continue

### 4. Create OAuth 2.0 Credentials

#### For Android (Required for your emulator/device)

1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. Choose **Android** as application type
4. Fill in:
   - **Name**: "Guilt Eater Android"
   - **Package name**: `com.example.frontend` (from your AndroidManifest.xml)
   - **SHA-1 certificate fingerprint**: Get this by running:
     ```bash
     cd frontend/android
     ./gradlew signingReport
     ```
     Look for the **SHA1** under `Variant: debug` > `Config: debug`
     It looks like: `A1:B2:C3:D4:E5:F6:...`
5. Click **Create**
6. Copy the **Client ID** (looks like `xxxxx.apps.googleusercontent.com`)

### 5. Update Backend Environment Variables

Edit `backend/.env` and update:

```env
GOOGLE_CLIENT_ID=<your-android-client-id>.apps.googleusercontent.com
```

## Testing the Flow

### 1. Start Backend Server

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Run Flutter App

```bash
cd frontend
flutter run
```

### 3. Test Sign In

1. Click **Sign in with Google** button
2. Google Sign-In dialog should appear
3. Select your Google account
4. App should navigate to Welcome screen
5. Backend should log the token exchange request

## Troubleshooting

### "Sign in failed: PlatformException"

- **Cause**: SHA-1 fingerprint mismatch or Client ID not configured
- **Fix**:
  1. Run `cd frontend/android && ./gradlew signingReport`
  2. Copy the SHA1 from debug config
  3. Update it in Google Cloud Console OAuth credentials
  4. Wait a few minutes for changes to propagate

### "Sign in cancelled" or Google dialog doesn't appear

- **Cause**: Google Sign-In not properly configured
- **Fix**:
  1. Verify package name in AndroidManifest.xml matches OAuth credential
  2. Ensure you've enabled Google Sign-In API in Cloud Console

### Backend returns "invalid id_token"

- **Cause**: Client ID mismatch between Android app and backend
- **Fix**: Ensure `GOOGLE_CLIENT_ID` in backend `.env` matches the Android OAuth Client ID from Google Cloud Console

### "Connection refused" or network error

- **Cause**: Android emulator can't reach localhost
- **Fix**: Already configured! We use `http://10.0.2.2:8000` in the code (10.0.2.2 is Android emulator's special alias for host machine's localhost)

## Quick SHA-1 Retrieval Command

```bash
cd c:/Users/Ashvatth/OneDrive/Desktop/AshWorks/projects/guilt-eater/frontend/android
./gradlew signingReport
```

Look for the line with `SHA1:` under the debug variant.

## Current Status

✅ Backend endpoints ready (`/auth/token`)
✅ Flutter app with Google Sign-In integrated
✅ Secure token storage
⚠️ Need to configure Google Cloud Console credentials
⚠️ Need to add SHA-1 fingerprint to OAuth credentials
