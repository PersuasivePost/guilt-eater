# Fix ApiException: 10 (DEVELOPER_ERROR)

This error means your Google OAuth configuration doesn't match your app.

## Required Setup in Google Cloud Console

### Step 1: Create/Verify Android OAuth Client

1. Go to https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. Application type: **Android**
4. Name: `Guilt Eater Android`
5. Package name: `com.example.frontend`
6. SHA-1 certificate fingerprint: Get it by running:

```bash
cd frontend/android
./gradlew signingReport
```

Look for this line under **Variant: debug, Config: debug**:

```
SHA1: XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX
```

Copy that SHA-1 value and paste it in Google Cloud Console.

### Step 2: Create/Verify Web OAuth Client (if you don't have one)

1. In the same credentials page, click **+ CREATE CREDENTIALS** > **OAuth client ID**
2. Application type: **Web application**
3. Name: `Guilt Eater Backend`
4. Authorized redirect URIs: (leave empty for now)
5. Click **CREATE**
6. **Copy the Client ID** - it looks like: `xxxxx-yyyy.apps.googleusercontent.com`

### Step 3: Update Your Code

#### In `backend/.env`:

```env
GOOGLE_CLIENT_ID=<YOUR_WEB_CLIENT_ID>.apps.googleusercontent.com
```

#### In `frontend/lib/services/auth_service.dart`:

```dart
serverClientId: '<YOUR_WEB_CLIENT_ID>.apps.googleusercontent.com',
```

**IMPORTANT**:

- `serverClientId` = Web Client ID (NOT Android Client ID!)
- Backend `GOOGLE_CLIENT_ID` = Same Web Client ID
- Android Client ID is auto-detected by the app (no need to specify in code)

### Step 4: Full Rebuild

```bash
cd frontend
flutter clean
flutter pub get
flutter run
```

## Why Both Client IDs?

- **Android Client ID**: Lets Google know this Android app is authorized
- **Web Client ID**: Allows the app to get an `id_token` that your backend can verify

Both must exist and be configured correctly for id_token to work!
