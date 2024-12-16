# 🚀 Complete Laravel Development Guide

## 📋 Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Project Structure](#project-structure)
3. [Routing & Controllers](#routing--controllers)
4. [Database & Migrations](#database--migrations)
5. [Models & Eloquent](#models--eloquent)
6. [Views & Blade](#views--blade)
7. [Authentication & Authorization](#authentication--authorization)
8. [APIs & Resources](#apis--resources)
9. [Testing](#testing)
10. [Deployment](#deployment)

## 🎯 Installation & Setup

### Requirements
- PHP >= 8.1
- Composer
- MySQL/PostgreSQL
- Node.js & NPM

### Installation
```bash
# Install Laravel installer
composer global require laravel/installer

# Create new project
laravel new project-name
# OR
composer create-project laravel/laravel project-name

# Navigate to project
cd project-name

# Install dependencies
composer install
npm install

# Generate application key
php artisan key:generate

# Start development server
php artisan serve
```

### Configuration
```bash
# Create .env file
cp .env.example .env

# Basic .env configuration
APP_NAME=Laravel
APP_ENV=local
APP_KEY=base64:your-key
APP_DEBUG=true
APP_URL=http://localhost

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

## 📁 Project Structure

### Key Directories
```plaintext
project/
├── app/
│   ├── Console/         # Artisan commands
│   ├── Http/           # Controllers, Middleware
│   ├── Models/         # Eloquent models
│   ├── Providers/      # Service providers
│   └── Services/       # Business logic
├── config/             # Configuration files
├── database/
│   ├── factories/      # Model factories
│   ├── migrations/     # Database migrations
│   └── seeders/       # Database seeders
├── public/            # Web root
├── resources/
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript
│   └── views/        # Blade templates
├── routes/           # Route definitions
└── tests/           # Test files
```

## 🛣️ Routing & Controllers

### Basic Routing
```php
// routes/web.php
Route::get('/', function () {
    return view('welcome');
});

Route::get('/posts', [PostController::class, 'index']);
Route::post('/posts', [PostController::class, 'store']);
Route::get('/posts/{post}', [PostController::class, 'show']);
Route::put('/posts/{post}', [PostController::class, 'update']);
Route::delete('/posts/{post}', [PostController::class, 'destroy']);

// Resource route
Route::resource('posts', PostController::class);

// API routes
Route::prefix('api')->group(function () {
    Route::apiResource('posts', PostApiController::class);
});
```

### Controller Example
```php
// app/Http/Controllers/PostController.php
namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::paginate(10);
        return view('posts.index', compact('posts'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        $post = Post::create($validated);
        return redirect()->route('posts.show', $post);
    }

    public function show(Post $post)
    {
        return view('posts.show', compact('post'));
    }
}
```

## 🗄️ Database & Migrations

### Migration Example
```php
// database/migrations/create_posts_table.php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('title');
            $table->text('content');
            $table->string('slug')->unique();
            $table->boolean('is_published')->default(false);
            $table->timestamp('published_at')->nullable();
            $table->timestamps();
            $table->softDeletes();
        });
    }

    public function down()
    {
        Schema::dropIfExists('posts');
    }
};
```

### Database Commands
```bash
# Run migrations
php artisan migrate

# Rollback migrations
php artisan migrate:rollback

# Refresh migrations
php artisan migrate:refresh

# Fresh migrations with seeders
php artisan migrate:fresh --seed

# Create migration
php artisan make:migration create_posts_table

# Create model with migration
php artisan make:model Post -m
```

## 📦 Models & Eloquent

### Model Example
```php
// app/Models/Post.php
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'title',
        'content',
        'slug',
        'is_published',
        'published_at'
    ];

    protected $casts = [
        'is_published' => 'boolean',
        'published_at' => 'datetime',
    ];

    // Relationships
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function comments()
    {
        return $this->hasMany(Comment::class);
    }

    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }

    // Scopes
    public function scopePublished($query)
    {
        return $query->where('is_published', true);
    }

    // Accessors & Mutators
    public function getTitleAttribute($value)
    {
        return ucfirst($value);
    }

    public function setSlugAttribute($value)
    {
        $this->attributes['slug'] = Str::slug($value);
    }
}
```

## 🎨 Views & Blade

### Layout Template
```php
// resources/views/layouts/app.blade.php
<!DOCTYPE html>
<html>
<head>
    <title>@yield('title', config('app.name'))</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <nav>
        @include('layouts.navigation')
    </nav>

    <main>
        @yield('content')
    </main>

    @stack('scripts')
</body>
</html>
```

### View Example
```php
// resources/views/posts/show.blade.php
@extends('layouts.app')

@section('title', $post->title)

@section('content')
    <article class="post">
        <h1>{{ $post->title }}</h1>
        
        <div class="content">
            {!! $post->content !!}
        </div>

        @if($post->comments_count)
            <div class="comments">
                @foreach($post->comments as $comment)
                    @include('comments.single', ['comment' => $comment])
                @endforeach
            </div>
        @endif
    </article>
@endsection

@push('scripts')
    <script>
        // Additional scripts
    </script>
@endpush
```

## 🔐 Authentication & Authorization

### Authentication Setup
```bash
# Install Laravel Breeze
composer require laravel/breeze --dev
php artisan breeze:install

# Install Laravel Sanctum (for APIs)
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

### Authorization Policy
```php
// app/Policies/PostPolicy.php
namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    public function view(User $user, Post $post)
    {
        return true;
    }

    public function create(User $user)
    {
        return true;
    }

    public function update(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }
}
```

## 🌐 APIs & Resources

### API Controller
```php
// app/Http/Controllers/Api/PostController.php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\PostResource;
use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::published()->paginate(10);
        return PostResource::collection($posts);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        $post = $request->user()->posts()->create($validated);
        return new PostResource($post);
    }
}
```

### API Resource
```php
// app/Http/Resources/PostResource.php
namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'content' => $this->content,
            'created_at' => $this->created_at,
            'author' => new UserResource($this->whenLoaded('user')),
            'comments_count' => $this->comments_count,
        ];
    }
}
```

## 🧪 Testing

### Feature Test
```php
// tests/Feature/PostTest.php
namespace Tests\Feature;

use App\Models\Post;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_view_posts()
    {
        $post = Post::factory()->create();

        $response = $this->get('/posts');

        $response->assertStatus(200)
                ->assertSee($post->title);
    }

    public function test_authenticated_user_can_create_post()
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
                        ->post('/posts', [
                            'title' => 'Test Post',
                            'content' => 'Test Content',
                        ]);

        $response->assertRedirect();
        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
        ]);
    }
}
```

## 🚀 Deployment

### Production Checklist
```bash
# Optimize application
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Compile assets
npm run build

# Update dependencies
composer install --optimize-autoloader --no-dev

# Run migrations
php artisan migrate --force
```

### Server Configuration
```nginx
# nginx configuration
server {
    listen 80;
    server_name example.com;
    root /var/www/html/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

## 💡 Best Practices

1. **Code Organization**
   - Use service classes for business logic
   - Implement repositories for data access
   - Use form requests for validation
   - Keep controllers thin

2. **Performance**
   - Cache frequently accessed data
   - Eager load relationships
   - Use database indexes
   - Implement queue for long-running tasks

3. **Security**
   - Validate all input
   - Use CSRF protection
   - Implement rate limiting
   - Keep dependencies updated

4. **Testing**
   - Write feature tests
   - Use factories for test data
   - Test edge cases
   - Maintain test coverage

Remember to:
1. Follow Laravel conventions
2. Keep dependencies updated
3. Monitor application logs
4. Implement proper error handling
5. Document your code
6. Use version control
7. Backup your database regularly