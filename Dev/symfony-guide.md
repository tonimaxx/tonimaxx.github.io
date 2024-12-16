# 🚀 Complete Symfony Development Guide

## 📋 Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Project Structure](#project-structure)
3. [Configuration](#configuration)
4. [Routing & Controllers](#routing--controllers)
5. [Doctrine ORM](#doctrine-orm)
6. [Twig Templates](#twig-templates)
7. [Forms](#forms)
8. [Security](#security)
9. [Services & DI](#services--dependency-injection)
10. [Console Commands](#console-commands)

## 🎯 Installation & Setup

### Requirements
- PHP >= 8.1
- Composer
- MySQL/PostgreSQL
- Symfony CLI (optional)

### Installation
```bash
# Install Symfony CLI
curl -sS https://get.symfony.com/cli/installer | bash

# Create new project
symfony new my-project --full

# Or using Composer directly
composer create-project symfony/website-skeleton my-project

# Start development server
symfony server:start

# Check requirements
symfony check:requirements
```

### Basic Configuration
```yaml
# .env
APP_ENV=dev
APP_SECRET=your-secret-here
DATABASE_URL="mysql://user:password@127.0.0.1:3306/database"
```

## 📁 Project Structure

### Directory Layout
```plaintext
my-project/
├── assets/           # Frontend assets
├── bin/             # Executable files
├── config/          # Configuration files
├── migrations/      # Database migrations
├── public/         # Web root directory
├── src/            # Application code
│   ├── Controller/
│   ├── Entity/
│   ├── Form/
│   ├── Repository/
│   └── Service/
├── templates/      # Twig templates
├── tests/         # Test files
└── translations/  # Translation files
```

## ⚙️ Configuration

### Services Configuration
```yaml
# config/services.yaml
services:
    _defaults:
        autowire: true
        autoconfigure: true
        public: false

    App\:
        resource: '../src/'
        exclude:
            - '../src/DependencyInjection/'
            - '../src/Entity/'
            - '../src/Kernel.php'

    App\Service\CustomService:
        arguments:
            $parameter: '%app.custom_parameter%'
```

### Parameters
```yaml
# config/services.yaml
parameters:
    app.custom_parameter: 'value'
    app.email_from: '%env(APP_EMAIL_FROM)%'
```

## 🛣️ Routing & Controllers

### Route Configuration
```yaml
# config/routes.yaml
homepage:
    path: /
    controller: App\Controller\HomeController::index

blog_show:
    path: /blog/{slug}
    controller: App\Controller\BlogController::show
    methods: GET
```

### Controller Example
```php
// src/Controller/BlogController.php
namespace App\Controller;

use App\Entity\Post;
use App\Form\PostType;
use App\Repository\PostRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class BlogController extends AbstractController
{
    #[Route('/blog', name: 'blog_index')]
    public function index(PostRepository $postRepository): Response
    {
        return $this->render('blog/index.html.twig', [
            'posts' => $postRepository->findAll(),
        ]);
    }

    #[Route('/blog/new', name: 'blog_new')]
    public function new(Request $request): Response
    {
        $post = new Post();
        $form = $this->createForm(PostType::class, $post);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $entityManager = $this->getDoctrine()->getManager();
            $entityManager->persist($post);
            $entityManager->flush();

            return $this->redirectToRoute('blog_show', [
                'id' => $post->getId()
            ]);
        }

        return $this->render('blog/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
```

## 🗄️ Doctrine ORM

### Entity Example
```php
// src/Entity/Post.php
namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity(repositoryClass: PostRepository::class)]
class Post
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private $id;

    #[ORM\Column(type: 'string', length: 255)]
    #[Assert\NotBlank]
    private $title;

    #[ORM\Column(type: 'text')]
    private $content;

    #[ORM\ManyToOne(targetEntity: User::class, inversedBy: 'posts')]
    #[ORM\JoinColumn(nullable: false)]
    private $author;

    // Getters and setters
}
```

### Repository Example
```php
// src/Repository/PostRepository.php
namespace App\Repository;

use App\Entity\Post;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class PostRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Post::class);
    }

    public function findPublishedPosts()
    {
        return $this->createQueryBuilder('p')
            ->andWhere('p.published = :published')
            ->setParameter('published', true)
            ->orderBy('p.createdAt', 'DESC')
            ->getQuery()
            ->getResult();
    }
}
```

## 🎨 Twig Templates

### Layout Template
```twig
{# templates/base.html.twig #}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{% block title %}Welcome!{% endblock %}</title>
        {% block stylesheets %}
            {{ encore_entry_link_tags('app') }}
        {% endblock %}
    </head>
    <body>
        {% block body %}{% endblock %}
        {% block javascripts %}
            {{ encore_entry_script_tags('app') }}
        {% endblock %}
    </body>
</html>
```

### Page Template
```twig
{# templates/blog/show.html.twig #}
{% extends 'base.html.twig' %}

{% block title %}{{ post.title }}{% endblock %}

{% block body %}
    <article class="post">
        <h1>{{ post.title }}</h1>
        
        <div class="metadata">
            Posted on {{ post.createdAt|date('Y-m-d') }}
            by {{ post.author.username }}
        </div>

        <div class="content">
            {{ post.content|raw }}
        </div>

        {% if is_granted('ROLE_ADMIN') %}
            <a href="{{ path('blog_edit', {id: post.id}) }}">Edit</a>
        {% endif %}
    </article>
{% endblock %}
```

## 📝 Forms

### Form Type
```php
// src/Form/PostType.php
namespace App\Form;

use App\Entity\Post;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class PostType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('title', TextType::class, [
                'label' => 'Post Title',
                'attr' => ['placeholder' => 'Enter title here']
            ])
            ->add('content', TextareaType::class, [
                'label' => 'Post Content',
                'attr' => ['rows' => 10]
            ]);
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            'data_class' => Post::class,
        ]);
    }
}
```

### Form Template
```twig
{# templates/blog/form.html.twig #}
{{ form_start(form) }}
    {{ form_row(form.title) }}
    {{ form_row(form.content) }}
    
    <button type="submit" class="btn">
        {{ button_label|default('Save') }}
    </button>
{{ form_end(form) }}
```

## 🔐 Security

### Security Configuration
```yaml
# config/packages/security.yaml
security:
    providers:
        app_user_provider:
            entity:
                class: App\Entity\User
                property: email

    password_hashers:
        App\Entity\User:
            algorithm: auto

    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        main:
            lazy: true
            provider: app_user_provider
            custom_authenticator: App\Security\LoginFormAuthenticator
            logout:
                path: app_logout

    access_control:
        - { path: ^/admin, roles: ROLE_ADMIN }
        - { path: ^/profile, roles: ROLE_USER }
```

### User Entity
```php
// src/Entity/User.php
namespace App\Entity;

use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;

class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    private $email;
    private $roles = [];
    private $password;

    public function getRoles(): array
    {
        $roles = $this->roles;
        $roles[] = 'ROLE_USER';

        return array_unique($roles);
    }

    // Other required methods...
}
```

## 🔧 Services & Dependency Injection

### Service Example
```php
// src/Service/FileUploader.php
namespace App\Service;

use Symfony\Component\HttpFoundation\File\Exception\FileException;
use Symfony\Component\HttpFoundation\File\UploadedFile;
use Symfony\Component\String\Slugger\SluggerInterface;

class FileUploader
{
    private $targetDirectory;
    private $slugger;

    public function __construct(
        string $targetDirectory,
        SluggerInterface $slugger
    ) {
        $this->targetDirectory = $targetDirectory;
        $this->slugger = $slugger;
    }

    public function upload(UploadedFile $file): string
    {
        $originalFilename = pathinfo($file->getClientOriginalName(), PATHINFO_FILENAME);
        $safeFilename = $this->slugger->slug($originalFilename);
        $fileName = $safeFilename.'-'.uniqid().'.'.$file->guessExtension();

        try {
            $file->move($this->targetDirectory, $fileName);
        } catch (FileException $e) {
            // Handle exception
        }

        return $fileName;
    }
}
```

## 🖥️ Console Commands

### Command Example
```php
// src/Command/CreateUserCommand.php
namespace App\Command;

use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

#[AsCommand(
    name: 'app:create-user',
    description: 'Creates a new user.',
)]
class CreateUserCommand extends Command
{
    public function __construct(
        private EntityManagerInterface $entityManager,
        private UserPasswordHasherInterface $passwordHasher
    ) {
        parent::__construct();
    }

    protected function configure(): void
    {
        $this
            ->addArgument('email', InputArgument::REQUIRED, 'The email of the user.')
            ->addArgument('password', InputArgument::REQUIRED, 'The password of the user.');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $user = new User();
        $user->setEmail($input->getArgument('email'));
        $user->setPassword(
            $this->passwordHasher->hashPassword(
                $user,
                $input->getArgument('password')
            )
        );

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        $output->writeln('User successfully generated!');

        return Command::SUCCESS;
    }
}
```

## 📝 Best Practices

1. **Code Organization**
   - Follow SOLID principles
   - Use services for business logic
   - Keep controllers thin
   - Use value objects when appropriate

2. **Performance**
   - Use Doctrine's lazy loading
   - Cache frequently accessed data
   - Use Doctrine's query builder
   - Implement proper indexes

3. **Security**
   - Validate all input
   - Use CSRF protection
   - Implement proper access control
   - Keep dependencies updated

4. **Testing**
   - Write unit tests
   - Use functional tests
   - Test edge cases
   - Mock external services

Remember to:
1. Follow Symfony conventions
2. Keep dependencies updated
3. Monitor application logs
4. Implement proper error handling
5. Document your code
6. Use version control
7. Back up your database regularly