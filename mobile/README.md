# Mobile App (Flutter) — Plan & API Usage

This folder documents how to build a Flutter app for Android/iOS that consumes the new lightweight API exposed by this repo.

## Architecture
- Client: Flutter app (Dart) calling the local API.
- Server: `api/server.js` (Express) reusing existing Valorant modules (auth, shop, inventory).
- Auth: Client sends `x-client-id` header (any unique string) to identify its account storage on the server. Login flows: username/password + optional 2FA, or Riot cookies.

## API Endpoints
All requests must include `x-client-id: <your-unique-id>` and optional `x-account: <1-based index>` if you manage multiple accounts under the same id.

- GET /health
- POST /auth/login { login, password }
- POST /auth/2fa { code }
- POST /auth/cookies { cookies }
- GET /users/me
- GET /shop/offers
- GET /shop/bundles
- GET /shop/nightmarket
- GET /wallet
- GET /inventory/loadout
- GET /inventory/skins

## Run the API
From the repo root:

1) Install deps: `npm install`
2) Start API: `node api/server.js` (listens on http://localhost:3001)

Optionally add a script in your IDE: `npm run start:api`

## Flutter: Minimal API client
Add `http` to `pubspec.yaml`:

```
dependencies:
  http: ^1.2.0
```

Create `lib/api_client.dart`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ValorantApiClient {
  final String baseUrl;
  final String clientId;
  final int? account; // 1-based index

  ValorantApiClient({
    this.baseUrl = 'http://localhost:3001',
    required this.clientId,
    this.account,
  });

  Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    'x-client-id': clientId,
    if (account != null) 'x-account': account.toString(),
  };

  Future<Map<String, dynamic>> login(String login, String password) async {
    final r = await http.post(Uri.parse('$baseUrl/auth/login'),
        headers: _headers,
        body: jsonEncode({'login': login, 'password': password}));
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> submit2FA(String code) async {
    final r = await http.post(Uri.parse('$baseUrl/auth/2fa'),
        headers: _headers, body: jsonEncode({'code': code}));
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> me() async {
    final r = await http.get(Uri.parse('$baseUrl/users/me'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> offers() async {
    final r = await http.get(Uri.parse('$baseUrl/shop/offers'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> bundles() async {
    final r = await http.get(Uri.parse('$baseUrl/shop/bundles'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> nightMarket() async {
    final r = await http.get(Uri.parse('$baseUrl/shop/nightmarket'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> wallet() async {
    final r = await http.get(Uri.parse('$baseUrl/wallet'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> loadout() async {
    final r = await http.get(Uri.parse('$baseUrl/inventory/loadout'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> skins() async {
    final r = await http.get(Uri.parse('$baseUrl/inventory/skins'), headers: _headers);
    return jsonDecode(r.body) as Map<String, dynamic>;
  }
}
```

## Flutter UI sketch
- After login, show tabs: Shop, Bundles, Night Market, Wallet, Loadout.
- Use the `ValorantApiClient` to populate screens and pull-to-refresh.

## Notes
- The API reuses existing rate-limit and maintenance handling from the bot.
- Credentials are stored server-side under `data/users/<x-client-id>.json` managed by the existing modules.
- For production, place the API behind HTTPS and implement a real auth layer (JWT or OAuth) instead of just `x-client-id`.

