# 🚀 Creating a Codename API Endpoint in Laravel

## 1. Project Setup

First, create a new Laravel project if you haven't already:

```bash
laravel new codename-api
cd codename-api
```

## 2. Create JSON Data Storage

Create a new directory and file for your JSON data:

```bash
mkdir -p storage/app/json
```

Save your JSON file as `storage/app/json/codename.json`

## 3. Create Service Class

Create a service to handle the JSON data operations:

```php
// app/Services/CodenameService.php
<?php

namespace App\Services;

use Illuminate\Support\Facades\Storage;

class CodenameService
{
    private $jsonData;

    public function __construct()
    {
        $this->jsonData = json_decode(
            Storage::get('json/codename.json'),
            true
        );
    }

    public function getAllThemes(): array
    {
        return array_keys($this->jsonData['themes']);
    }

    public function getThemeData(string $theme): ?array
    {
        return $this->jsonData['themes'][$theme] ?? null;
    }

    public function getRandomCodename(string $theme): ?string
    {
        $themeData = $this->getThemeData($theme);
        if (!$themeData || empty($themeData['data'])) {
            return null;
        }

        return $themeData['data'][array_rand($themeData['data'])];
    }

    public function validateTheme(string $theme): bool
    {
        return isset($this->jsonData['themes'][$theme]);
    }
}
```

## 4. Create Controller

Create an API controller to handle the requests:

```php
// app/Http/Controllers/Api/CodenameController.php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\CodenameService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class CodenameController extends Controller
{
    private $codenameService;

    public function __construct(CodenameService $codenameService)
    {
        $this->codenameService = $codenameService;
    }

    public function themes(): JsonResponse
    {
        return response()->json([
            'status' => 'success',
            'data' => $this->codenameService->getAllThemes()
        ]);
    }

    public function getTheme(string $theme): JsonResponse
    {
        if (!$this->codenameService->validateTheme($theme)) {
            return response()->json([
                'status' => 'error',
                'message' => 'Theme not found'
            ], 404);
        }

        return response()->json([
            'status' => 'success',
            'data' => $this->codenameService->getThemeData($theme)
        ]);
    }

    public function getRandomCodename(string $theme): JsonResponse
    {
        if (!$this->codenameService->validateTheme($theme)) {
            return response()->json([
                'status' => 'error',
                'message' => 'Theme not found'
            ], 404);
        }

        $codename = $this->codenameService->getRandomCodename($theme);
        
        if ($codename === null) {
            return response()->json([
                'status' => 'error',
                'message' => 'No codenames available for this theme'
            ], 404);
        }

        return response()->json([
            'status' => 'success',
            'data' => [
                'theme' => $theme,
                'codename' => $codename
            ]
        ]);
    }

    public function searchCodenames(Request $request): JsonResponse
    {
        $theme = $request->input('theme');
        $query = $request->input('query');

        if (!$theme || !$this->codenameService->validateTheme($theme)) {
            return response()->json([
                'status' => 'error',
                'message' => 'Invalid or missing theme'
            ], 400);
        }

        $themeData = $this->codenameService->getThemeData($theme);
        $filteredCodenames = array_filter(
            $themeData['data'],
            fn($codename) => stripos($codename, $query) !== false
        );

        return response()->json([
            'status' => 'success',
            'data' => array_values($filteredCodenames)
        ]);
    }
}
```

## 5. Define Routes

Add the routes in your API routes file:

```php
// routes/api.php
use App\Http\Controllers\Api\CodenameController;

Route::prefix('codenames')->group(function () {
    Route::get('themes', [CodenameController::class, 'themes']);
    Route::get('theme/{theme}', [CodenameController::class, 'getTheme']);
    Route::get('random/{theme}', [CodenameController::class, 'getRandomCodename']);
    Route::get('search', [CodenameController::class, 'searchCodenames']);
});
```

## 6. Add Service Provider (Optional)

If you want to bind the service to the container:

```php
// app/Providers/AppServiceProvider.php
<?php

namespace App\Providers;

use App\Services\CodenameService;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function register()
    {
        $this->app->singleton(CodenameService::class, function ($app) {
            return new CodenameService();
        });
    }
}
```

## 7. API Usage Examples

### List All Themes
```bash
curl http://localhost:8000/api/codenames/themes
```

Response:
```json
{
    "status": "success",
    "data": [
        "space-objects",
        "norse-mythology",
        "classic-literature",
        // ... more themes
    ]
}
```

### Get Theme Data
```bash
curl http://localhost:8000/api/codenames/theme/space-objects
```

Response:
```json
{
    "status": "success",
    "data": {
        "description": "Names of celestial objects, stars, and planets.",
        "data": [
            "Andromeda",
            "Betelgeuse",
            // ... more codenames
        ]
    }
}
```

### Get Random Codename
```bash
curl http://localhost:8000/api/codenames/random/space-objects
```

Response:
```json
{
    "status": "success",
    "data": {
        "theme": "space-objects",
        "codename": "Jupiter"
    }
}
```

### Search Codenames
```bash
curl "http://localhost:8000/api/codenames/search?theme=space-objects&query=ar"
```

Response:
```json
{
    "status": "success",
    "data": [
        "Mars",
        "Quasar",
        // ... matching codenames
    ]
}
```

## 8. Error Handling

The API includes error handling for common scenarios:

- Invalid theme
- Empty theme data
- Search without required parameters
- File reading errors

Example error response:
```json
{
    "status": "error",
    "message": "Theme not found"
}
```

## 9. Testing

Create tests for your endpoints:

```php
// tests/Feature/CodenameApiTest.php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class CodenameApiTest extends TestCase
{
    public function test_can_get_themes()
    {
        $response = $this->get('/api/codenames/themes');
        $response->assertStatus(200)
                ->assertJsonStructure([
                    'status',
                    'data'
                ]);
    }

    public function test_can_get_random_codename()
    {
        $response = $this->get('/api/codenames/random/space-objects');
        $response->assertStatus(200)
                ->assertJsonStructure([
                    'status',
                    'data' => [
                        'theme',
                        'codename'
                    ]
                ]);
    }

    public function test_returns_error_for_invalid_theme()
    {
        $response = $this->get('/api/codenames/random/invalid-theme');
        $response->assertStatus(404)
                ->assertJson([
                    'status' => 'error',
                    'message' => 'Theme not found'
                ]);
    }
}
```

## 🔍 Best Practices

1. **Cache Implementation**
Consider adding cache for frequently accessed data:

```php
use Illuminate\Support\Facades\Cache;

public function getAllThemes(): array
{
    return Cache::remember('codename.themes', 3600, function () {
        return array_keys($this->jsonData['themes']);
    });
}
```

2. **Rate Limiting**
Add rate limiting to your routes:

```php
Route::middleware('throttle:60,1')->group(function () {
    // Your routes here
});
```

3. **Validation**
Add request validation:

```php
// app/Http/Requests/SearchCodenameRequest.php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class SearchCodenameRequest extends FormRequest
{
    public function rules()
    {
        return [
            'theme' => 'required|string',
            'query' => 'required|string|min:2'
        ];
    }
}
```

Remember to:
1. Keep your JSON file in version control
2. Implement proper logging
3. Add appropriate documentation
4. Consider implementing caching for better performance
5. Add proper validation for all inputs
6. Include comprehensive error handling
7. Write thorough tests