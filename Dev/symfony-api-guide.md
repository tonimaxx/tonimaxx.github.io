# 🚀 Creating Simple API Endpoints in Symfony

## 📋 Step-by-Step Guide

### 1. Project Setup
```bash
# Create new Symfony project
symfony new api-project --full

# Start development server
symfony serve -d

# Install required packages
composer require symfony/orm-pack
composer require symfony/maker-bundle --dev
composer require symfony/serializer-pack
```

### 2. Configure Database
```yaml
# .env
DATABASE_URL="mysql://root:password@127.0.0.1:3306/symfony_api?serverVersion=8.0"
```

### 3. Create Entity
```php
// src/Entity/Product.php
namespace App\Entity;

use App\Repository\ProductRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Serializer\Annotation\Groups;

#[ORM\Entity(repositoryClass: ProductRepository::class)]
class Product
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    #[Groups(['product:read'])]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    #[Groups(['product:read', 'product:write'])]
    private ?string $name = null;

    #[ORM\Column]
    #[Groups(['product:read', 'product:write'])]
    private ?float $price = null;

    #[ORM\Column(length: 1000, nullable: true)]
    #[Groups(['product:read', 'product:write'])]
    private ?string $description = null;

    // Getters and Setters
    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;
        return $this;
    }

    public function getPrice(): ?float
    {
        return $this->price;
    }

    public function setPrice(float $price): self
    {
        $this->price = $price;
        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(?string $description): self
    {
        $this->description = $description;
        return $this;
    }
}
```

### 4. Create Migration
```bash
# Generate migration
php bin/console make:migration

# Run migration
php bin/console doctrine:migrations:migrate
```

### 5. Create API Controller
```php
// src/Controller/Api/ProductController.php
namespace App\Controller\Api;

use App\Entity\Product;
use App\Repository\ProductRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Serializer\SerializerInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

#[Route('/api/products', name: 'api_products_')]
class ProductController extends AbstractController
{
    public function __construct(
        private EntityManagerInterface $entityManager,
        private ProductRepository $productRepository,
        private SerializerInterface $serializer,
        private ValidatorInterface $validator
    ) {}

    #[Route('', name: 'index', methods: ['GET'])]
    public function index(): JsonResponse
    {
        $products = $this->productRepository->findAll();
        
        return $this->json([
            'data' => $products
        ], Response::HTTP_OK, [], ['groups' => ['product:read']]);
    }

    #[Route('/{id}', name: 'show', methods: ['GET'])]
    public function show(Product $product): JsonResponse
    {
        return $this->json([
            'data' => $product
        ], Response::HTTP_OK, [], ['groups' => ['product:read']]);
    }

    #[Route('', name: 'create', methods: ['POST'])]
    public function create(Request $request): JsonResponse
    {
        try {
            $product = $this->serializer->deserialize(
                $request->getContent(),
                Product::class,
                'json',
                ['groups' => ['product:write']]
            );

            $errors = $this->validator->validate($product);
            if (count($errors) > 0) {
                return $this->json([
                    'errors' => (string) $errors
                ], Response::HTTP_BAD_REQUEST);
            }

            $this->entityManager->persist($product);
            $this->entityManager->flush();

            return $this->json([
                'data' => $product
            ], Response::HTTP_CREATED, [], ['groups' => ['product:read']]);
        } catch (\Exception $e) {
            return $this->json([
                'error' => $e->getMessage()
            ], Response::HTTP_BAD_REQUEST);
        }
    }

    #[Route('/{id}', name: 'update', methods: ['PUT'])]
    public function update(Request $request, Product $product): JsonResponse
    {
        try {
            $this->serializer->deserialize(
                $request->getContent(),
                Product::class,
                'json',
                [
                    'object_to_populate' => $product,
                    'groups' => ['product:write']
                ]
            );

            $errors = $this->validator->validate($product);
            if (count($errors) > 0) {
                return $this->json([
                    'errors' => (string) $errors
                ], Response::HTTP_BAD_REQUEST);
            }

            $this->entityManager->flush();

            return $this->json([
                'data' => $product
            ], Response::HTTP_OK, [], ['groups' => ['product:read']]);
        } catch (\Exception $e) {
            return $this->json([
                'error' => $e->getMessage()
            ], Response::HTTP_BAD_REQUEST);
        }
    }

    #[Route('/{id}', name: 'delete', methods: ['DELETE'])]
    public function delete(Product $product): JsonResponse
    {
        try {
            $this->entityManager->remove($product);
            $this->entityManager->flush();

            return $this->json(null, Response::HTTP_NO_CONTENT);
        } catch (\Exception $e) {
            return $this->json([
                'error' => $e->getMessage()
            ], Response::HTTP_BAD_REQUEST);
        }
    }
}
```

### 6. Add Validation
```php
// src/Entity/Product.php
use Symfony\Component\Validator\Constraints as Assert;

class Product
{
    #[Assert\NotBlank]
    #[Assert\Length(min: 3, max: 255)]
    private ?string $name = null;

    #[Assert\NotBlank]
    #[Assert\Positive]
    private ?float $price = null;

    #[Assert\Length(max: 1000)]
    private ?string $description = null;
}
```

### 7. Testing the API

#### Get All Products
```bash
curl -X GET http://localhost:8000/api/products
```

#### Get Single Product
```bash
curl -X GET http://localhost:8000/api/products/1
```

#### Create Product
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "price": 29.99,
    "description": "Product description"
  }'
```

#### Update Product
```bash
curl -X PUT http://localhost:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product",
    "price": 39.99,
    "description": "Updated description"
  }'
```

#### Delete Product
```bash
curl -X DELETE http://localhost:8000/api/products/1
```

### 8. Add API Documentation (Optional)
```bash
# Install API Platform
composer require api-platform/api-pack

# Configure API Platform
```yaml
# config/packages/api_platform.yaml
api_platform:
    title: 'Products API'
    version: '1.0.0'
    formats:
        json: ['application/json']
    docs_formats:
        jsonld: ['application/ld+json']
        jsonopenapi: ['application/vnd.openapi+json']
        html: ['text/html']
```

### 9. Error Handling
```php
// src/EventListener/ExceptionListener.php
namespace App\EventListener;

use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Event\ExceptionEvent;
use Symfony\Component\HttpKernel\Exception\HttpExceptionInterface;

class ExceptionListener
{
    public function onKernelException(ExceptionEvent $event): void
    {
        $exception = $event->getThrowable();
        $message = [
            'message' => $exception->getMessage(),
            'code' => Response::HTTP_INTERNAL_SERVER_ERROR
        ];

        if ($exception instanceof HttpExceptionInterface) {
            $message['code'] = $exception->getStatusCode();
        }

        $response = new JsonResponse($message, $message['code']);
        $event->setResponse($response);
    }
}
```

### 10. Configure CORS (if needed)
```yaml
# config/packages/nelmio_cors.yaml
nelmio_cors:
    defaults:
        origin_regex: true
        allow_origin: ['%env(CORS_ALLOW_ORIGIN)%']
        allow_methods: ['GET', 'OPTIONS', 'POST', 'PUT', 'PATCH', 'DELETE']
        allow_headers: ['Content-Type', 'Authorization']
        expose_headers: ['Link']
        max_age: 3600
```

## 📝 Best Practices

1. **Response Format**
   - Use consistent response formats
   - Include proper HTTP status codes
   - Handle errors gracefully
   - Add pagination for large collections

2. **Security**
   - Validate all input
   - Implement authentication if needed
   - Use HTTPS in production
   - Add rate limiting

3. **Performance**
   - Use pagination
   - Implement caching
   - Optimize database queries
   - Use appropriate indexes

4. **Documentation**
   - Document your API
   - Include example requests/responses
   - Add validation rules
   - Specify required headers

Remember to:
1. Keep endpoints RESTful
2. Version your API
3. Implement proper error handling
4. Add appropriate security measures
5. Monitor API usage
6. Cache responses when possible
7. Validate all input data