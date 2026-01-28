# Security Improvements - Account Separation & Single Device Login

## Issues Fixed

### 1. ✅ Same Google Account for Multiple Roles (FIXED)

**Problem:** A Google account could be used to create both parent and child accounts, defeating the purpose of role separation.

**Solution:**

- Added role validation during login
- If a Google account already exists with one role (e.g., parent), attempting to sign in as a different role (e.g., child) will be rejected
- Error message: `"This Google account is already registered as {existing_role}. Please use a different account for {requested_role} role."`

**Implementation:**

- File: `backend/auth/router.py`
- When user signs in, we check if their email already exists in database
- If exists with different role, we reject with HTTP 403 error
- User must use a different Google account for each role

### 2. ✅ Single Device Login for Parents (FIXED)

**Problem:** Parent accounts could be logged in on multiple devices simultaneously, allowing children to potentially access parent controls from another device.

**Solution:**

- Implemented session token system for parent accounts
- Each time a parent logs in, a new unique session token is generated
- The session token is embedded in the JWT and validated on every API request
- When parent logs in from a new device, all previous sessions are invalidated
- Other devices with old session tokens will receive: `"Session expired. This account is logged in on another device."`

**Implementation:**

- Database: Added `session_token` column to `users` table (VARCHAR, nullable)
- File: `backend/models/models.py` - Added session_token field
- File: `backend/auth/security.py` - Added session token generation and validation
- File: `backend/auth/router.py` - Generate new session token on parent login
- Migration: `backend/migrations/add_session_token.py` - Database schema update

**How it works:**

1. Parent signs in → Server generates unique 64-character session token
2. Session token stored in database and embedded in JWT
3. Old session tokens in database are overwritten (invalidating old sessions)
4. Every API request validates: JWT session token matches database session token
5. If mismatch → User gets "Session expired" error and must re-authenticate

**Security Benefits:**

- Child cannot use parent's credentials on another device
- Parent has single point of control - one device at a time
- Automatic session invalidation - no manual logout needed from old device
- Real-time enforcement - takes effect immediately

## Testing the Fixes

### Test 1: Prevent Same Account for Multiple Roles

1. Sign in as parent with Google account A → Should succeed
2. Try to sign in as child with same Google account A → Should fail with error:
   ```
   "This Google account is already registered as parent. Please use a different account for child role."
   ```
3. Use different Google account B for child → Should succeed

### Test 2: Single Device Parent Login

1. Sign in as parent on Device 1 (emulator)
2. Note the parent account is working fine
3. Sign in as parent with same account on Device 2 (real phone)
4. Try to use any feature on Device 1 → Should fail with error:
   ```
   "Session expired. This account is logged in on another device."
   ```
5. Device 1 user must sign in again to regain access

## Impact on Existing Users

### For Existing Parent Accounts:

- ✅ No action needed - migration adds session_token column automatically
- ✅ First login after update will generate session token
- ✅ Subsequent logins will enforce single device access

### For Existing Child Accounts:

- ✅ No impact - child accounts can login on multiple devices
- ✅ Only parents are restricted to single device

### For New Users:

- ✅ All new accounts automatically have these security measures
- ✅ Role validation happens at account creation

## Database Changes

**Migration Required:** Yes ✅ (Already run)

**Migration Script:** `backend/migrations/add_session_token.py`

**Changes:**

```sql
ALTER TABLE users ADD COLUMN session_token VARCHAR
```

**Migration Status:** ✅ Completed successfully

## Code Changes Summary

1. **backend/models/models.py**
   - Added `session_token` field to User model

2. **backend/auth/security.py**
   - Added `create_session_token()` function
   - Updated `create_access_token()` to include session_token in JWT
   - Updated `get_current_user()` to validate session token for parents

3. **backend/auth/router.py**
   - Added role validation check during login
   - Generate and store session token for parent accounts
   - Pass session token when creating JWT for parents

4. **backend/migrations/**
   - Added `add_session_token.py` migration script
   - Added `README.md` with migration instructions

## Security Considerations

### What's Protected:

- ✅ Role separation - one Google account = one role
- ✅ Parent account single device access
- ✅ Automatic old session invalidation
- ✅ Real-time session validation

### What's NOT Affected:

- ❌ Child accounts can still login on multiple devices (by design)
- ❌ Individual accounts can login on multiple devices (by design)
- ❌ Existing JWT tokens for non-parent users remain valid

### Token Security:

- Session tokens are 64-character random hex strings
- Generated using cryptographically secure `os.urandom(32).hex()`
- Session tokens stored securely in database
- JWT tokens contain session token for validation
- No session token exposed to client directly

## Next Steps

1. ✅ Migration completed - database updated
2. ✅ Backend code updated with security measures
3. **TODO:** Test both scenarios:
   - Try logging in as parent then child with same account → Should fail
   - Try logging in as parent on two devices → Second device should invalidate first
4. **TODO:** Frontend error handling:
   - Show clear error message when role conflict occurs
   - Handle "Session expired" error and prompt re-login

## Need Help?

If you encounter issues:

1. Check backend logs for detailed error messages
2. Verify migration ran successfully: `python migrations/add_session_token.py`
3. Restart backend server after migration
4. Clear app data and retry if JWT caching issues occur
