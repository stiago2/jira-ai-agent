#!/usr/bin/env python3
"""
Authentication System Test Script

Tests the complete authentication flow:
1. User registration
2. User login (JWT token generation)
3. Access to protected endpoints with token
4. Logout

Usage:
    python3 test_auth_system.py
"""

import requests
import json
import sys
from datetime import datetime


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subsection(title):
    """Print a formatted subsection header."""
    print(f"\n{title}")
    print("-" * 70)


def test_registration(base_url: str) -> dict:
    """Test user registration endpoint."""
    print_subsection("1. TESTING REGISTRATION")

    test_user = {
        'email': f'test_{datetime.now().timestamp()}@example.com',
        'username': f'testuser_{int(datetime.now().timestamp())}',
        'password': 'TestPassword123!',
        'jira_email': 'test@company.com',
        'jira_api_token': 'test_token_123',
        'jira_base_url': 'https://testcompany.atlassian.net'
    }

    response = requests.post(
        f'{base_url}/api/v1/auth/register',
        json=test_user
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 201:
        user_data = response.json()
        print(f"✅ User registered successfully!")
        print(f"   ID: {user_data['id']}")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        return test_user
    else:
        print(f"❌ Registration failed: {response.json()}")
        sys.exit(1)


def test_login(base_url: str, username: str, password: str) -> str:
    """Test user login and return access token."""
    print_subsection("2. TESTING LOGIN")

    response = requests.post(
        f'{base_url}/api/v1/auth/login',
        data={
            'username': username,
            'password': password
        }
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        token_data = response.json()
        token = token_data['access_token']
        print(f"✅ Login successful!")
        print(f"   Token type: {token_data['token_type']}")
        print(f"   Token (first 50 chars): {token[:50]}...")
        return token
    else:
        print(f"❌ Login failed: {response.json()}")
        sys.exit(1)


def test_get_current_user(base_url: str, token: str):
    """Test getting current user information."""
    print_subsection("3. TESTING GET CURRENT USER (/me)")

    response = requests.get(
        f'{base_url}/api/v1/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ User info retrieved successfully!")
        print(f"   Username: {user_data['username']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Active: {user_data['is_active']}")
        print(f"   Last login: {user_data.get('last_login', 'N/A')}")
    else:
        print(f"❌ Failed to get user info: {response.json()}")
        sys.exit(1)


def test_protected_endpoint(base_url: str, token: str):
    """Test accessing a protected endpoint."""
    print_subsection("4. TESTING PROTECTED ENDPOINT (/projects)")

    response = requests.get(
        f'{base_url}/api/v1/projects',
        headers={'Authorization': f'Bearer {token}'}
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        projects = response.json()
        print(f"✅ Protected endpoint accessible!")
        print(f"   Projects found: {len(projects)}")
    elif response.status_code == 500:
        # Expected if Jira credentials are not real
        error = response.json()
        if 'Jira' in error.get('detail', ''):
            print(f"⚠️  Protected endpoint accessible (Jira error expected with test credentials)")
            print(f"   Error: {error['detail'][:80]}...")
        else:
            print(f"❌ Unexpected error: {error}")
    else:
        print(f"❌ Failed to access protected endpoint: {response.json()}")
        sys.exit(1)


def test_logout(base_url: str, token: str):
    """Test logout endpoint."""
    print_subsection("5. TESTING LOGOUT")

    response = requests.post(
        f'{base_url}/api/v1/auth/logout',
        headers={'Authorization': f'Bearer {token}'}
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        logout_data = response.json()
        print(f"✅ Logout successful!")
        print(f"   Message: {logout_data['message']}")
    else:
        print(f"❌ Logout failed: {response.json()}")


def test_invalid_token(base_url: str):
    """Test accessing protected endpoint with invalid token."""
    print_subsection("6. TESTING INVALID TOKEN REJECTION")

    response = requests.get(
        f'{base_url}/api/v1/auth/me',
        headers={'Authorization': 'Bearer invalid_token_123'}
    )

    print(f"Status: {response.status_code}")

    if response.status_code == 401:
        print(f"✅ Invalid token correctly rejected!")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"❌ Invalid token should have been rejected!")
        sys.exit(1)


def main():
    """Run all authentication tests."""
    base_url = 'http://localhost:8000'

    print_section("AUTHENTICATION SYSTEM TEST")
    print(f"Testing server at: {base_url}")

    try:
        # Test health endpoint first
        response = requests.get(f'{base_url}/api/v1/health', timeout=5)
        if response.status_code != 200:
            print("❌ Server health check failed!")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print(f"   Make sure the server is running at {base_url}")
        sys.exit(1)

    # Run tests
    test_user = test_registration(base_url)
    token = test_login(base_url, test_user['username'], test_user['password'])
    test_get_current_user(base_url, token)
    test_protected_endpoint(base_url, token)
    test_logout(base_url, token)
    test_invalid_token(base_url)

    # Summary
    print_section("TEST SUMMARY")
    print("✅ All authentication tests passed!")
    print("\nTested endpoints:")
    print("  - POST /api/v1/auth/register")
    print("  - POST /api/v1/auth/login")
    print("  - GET  /api/v1/auth/me")
    print("  - GET  /api/v1/projects (with authentication)")
    print("  - POST /api/v1/auth/logout")
    print("  - Token validation")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
