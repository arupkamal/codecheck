# TypeScript Coding Conventions

## File Organization

### File Naming
- Use `kebab-case` for file names: `user-service.ts`, `auth-middleware.ts`
- Test files should end with `.spec.ts` or `.test.ts`
- One class/component per file
- Filename should match the class/component name: `UserService.ts` for class `UserService`

### Directory Structure
```
src/
├── config/         # Configuration files
├── controllers/    # Request handlers
├── models/         # Data models
├── services/       # Business logic
├── middlewares/    # Express middlewares
├── utils/          # Utility functions
├── types/          # Type definitions
└── tests/          # Test files
```

## Code Style

### Naming Conventions
- Use `PascalCase` for class names, interfaces, and type aliases
  ```typescript
  class UserService {}
  interface UserData {}
  type ApiResponse<T> = {}
  ```
- Use `camelCase` for variables, functions, and methods
  ```typescript
  const userData: UserData;
  function getUserById(id: string): Promise<User>;
  ```
- Use `UPPER_SNAKE_CASE` for constants
  ```typescript
  const MAX_RETRY_ATTEMPTS = 3;
  const API_BASE_URL = 'https://api.example.com';
  ```
- Prefix interfaces with 'I' only when there's a class implementing it
  ```typescript
  interface IRepository<T> {}
  class MongoRepository<T> implements IRepository<T> {}
  ```
- Prefix private properties with underscore
  ```typescript
  class UserService {
    private _userRepository: IUserRepository;
  }
  ```

### Type Annotations
- Always define return types for functions/methods
  ```typescript
  // Good
  function createUser(data: UserInput): Promise<User> {}
  
  // Avoid
  function createUser(data: UserInput) {}
  ```
- Use type inference for simple variable declarations
  ```typescript
  // Good
  const name = 'John'; // inferred as string
  
  // Unnecessary
  const name: string = 'John';
  ```
- Use explicit types for complex objects and arrays
  ```typescript
  const config: ServerConfig = {
    port: 3000,
    host: 'localhost'
  };
  ```

### Async Code
- Always use `async/await` over `.then()`
- Handle errors with try/catch
  ```typescript
  async function fetchUser(id: string): Promise<User> {
    try {
      const user = await userRepository.findById(id);
      return user;
    } catch (error) {
      logger.error('Failed to fetch user', { id, error });
      throw new ApplicationError('UserNotFound');
    }
  }
  ```

### Error Handling
- Create custom error classes
  ```typescript
  class ApplicationError extends Error {
    constructor(
      public code: string,
      public status: number = 500,
      public details?: unknown
    ) {
      super(code);
      this.name = 'ApplicationError';
    }
  }
  ```
- Use error codes instead of messages for error identification
- Log errors with context

### Comments and Documentation
- Use JSDoc for public APIs and complex functions
  ```typescript
  /**
   * Creates a new user in the system
   * @param data - User creation data
   * @throws {ValidationError} When data is invalid
   * @returns Newly created user
   */
  async function createUser(data: UserInput): Promise<User>
  ```
- Write comments for complex business logic
- Keep comments up to date with code changes

## Best Practices

### Dependency Injection
- Use dependency injection for better testability
  ```typescript
  class UserService {
    constructor(private userRepository: IUserRepository) {}
  }
  ```

### Immutability
- Use `readonly` for properties that shouldn't change
- Use `const` over `let` when possible
- Use immutable data structures
  ```typescript
  interface UserState {
    readonly id: string;
    readonly email: string;
  }
  ```

### Testing
- Write unit tests for business logic
- Use integration tests for API endpoints
- Follow AAA pattern (Arrange, Act, Assert)
- Use meaningful test descriptions
  ```typescript
  describe('UserService', () => {
    it('should throw UserNotFound when user does not exist', async () => {
      // test implementation
    });
  });
  ```

### Code Organization
- Keep functions small and focused
- Follow Single Responsibility Principle
- Use pure functions when possible
- Avoid any use of `any` type
- Use enums for fixed sets of values
  ```typescript
  enum UserRole {
    ADMIN = 'admin',
    USER = 'user',
    GUEST = 'guest'
  }
  ```

## Tools and Configuration

### ESLint Configuration
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:prettier/recommended"
  ],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

### Prettier Configuration
```json
{
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2,
  "semi": true
}
```

### tsconfig.json Recommendations
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.spec.ts"]
}
```

## Version Control

### Git Practices
- Use meaningful commit messages following conventional commits
  ```
  feat: add user authentication
  fix: correct email validation
  docs: update API documentation
  ```
- Create feature branches from develop
- Use pull requests for code reviews
- Keep commits atomic and focused

### Pull Request Guidelines
- Include description of changes
- Link related issues
- Add tests for new features
- Update documentation when needed
- Request review from at least one team member

## Continuous Integration
- Run tests before merging
- Check code coverage
- Perform linting
- Run security checks
- Build documentation

These conventions should be reviewed and adjusted based on team feedback and project requirements. Regular updates to maintain relevance are recommended.
