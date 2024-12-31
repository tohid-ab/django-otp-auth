# Django OTP Authentication

A Django-based authentication system that uses phone numbers and OTP (One-Time Password) for user verification. This project supports JWT (JSON Web Tokens) for secure authentication and authorization.

## Features

- **Phone Number Authentication**: Users can authenticate using their phone numbers.
- **OTP Verification**: A one-time password is sent to the user's phone for verification.
- **JWT Support**: Secure authentication using JSON Web Tokens, including access and refresh tokens.
- **Simple API**: Easy-to-use API endpoints for OTP creation, verification, and token refresh.

## API Endpoints

### 1. Create OTP
- **URL**: `/api/auth/otp/create/`
- **Method**: `POST`
- **Description**: Generates and sends an OTP to the provided phone number.
- **Request Body**:
  ```json
  {
    "receiver": "09000000000"
  }
  ```
- **Response**:
  ```json
  {
    "uuid": "69559251-5247-442b-9f6e-685da251fcf2"
  }
  ```
  
### 2. Verify OTP
- **URL**: `/api/auth/otp/verify/`
- **Method**: `POST`
- **Description**: Verifies the OTP and returns JWT tokens if successful.
- **Request Body**:
  ```json
  {
    "uuid": "e9a59251-5247-442b-9f6e-685da251fcf2",
    "receiver": "09000000000",
    "code": "76145"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
  
### 3. Refresh Token
- **URL**: `/api/auth/otp/refresh/`
- **Method**: `POST`
- **Description**: Refreshes the access token using the refresh token.
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
## Installation
1. Clone the repository:
```bash
  git clone https://github.com/tohid-ab/django-otp-auth.git
```
2. Navigate to the project directory:
```bash
  cd django-otp-auth
```

3. Install the required dependencies:
```bash
  pip install -r requirements.txt
```

4. Run migrations:
```bash
  python manage.py migrate
```

5 .Start the development server:
```bash
  python manage.py runserver
```
## Usage
1. Use the `/api/auth/otp/create/` endpoint to send an OTP to the user's phone number.
2. Verify the OTP using the `/api/auth/otp/verify/` endpoint to obtain JWT tokens.
3. Use the `/api/auth/otp/refresh/` endpoint to refresh the access token when it expires.
## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
## License
This project is licensed under the MIT License. See the **[LICENSE](https://github.com/tohid-ab/django-otp-auth/blob/main/LICENSE)** file for details.
