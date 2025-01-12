# TypeScript Naming Conventions Guide

## File Names

### Source Files
- Use `kebab-case` for all file names
- Files should have a `.ts` extension
- One class/interface/component per file
- Name should reflect the primary export
```typescript
// user-service.ts
export class UserService { }

// authentication-types.ts
export type AuthenticationResponse = { }

// date-utils.ts
export function formatDate() { }
```

### Test Files
- Add `.test.ts` or `.spec.ts` suffix
- Match the name of the file being tested
```
user-service.ts → user-service.test.ts
date-utils.ts → date-utils.spec.ts
```

### Barrel Files
- Use `index.ts` for barrel files (re-exporting)
- Place in feature/module directories
```typescript
// src/components/index.ts
export * from './user-card';
export * from './user-profile';
```

## Classes

### Class Names
- Use `PascalCase`
- Use nouns or noun phrases
- Be descriptive and unambiguous
```typescript
class UserRepository { }
class PaymentProcessor { }
class EmailService { }
```

### Abstract Classes
- Prefix with "Abstract" or "Base"
- Use `PascalCase`
```typescript
abstract class AbstractRepository<T> { }
abstract class BaseController { }
```

### Class Members

#### Properties
- Use `camelCase`
- Private members prefixed with underscore
```typescript
class User {
  public firstName: string;
  private _password: string;
  protected _lastLoginDate: Date;
}
```

#### Methods
- Use `camelCase`
- Use verbs or verb phrases
```typescript
class UserService {
  async fetchUserById(id: string): Promise<User> { }
  private _validateUserData(data: UserInput): boolean { }
}
```

## Interfaces

### Interface Names
- Use `PascalCase`
- Use nouns or noun phrases
- Add 'I' prefix only when implementing with a class
```typescript
// Without 'I' prefix (common interfaces)
interface UserData { }
interface ApiResponse { }

// With 'I' prefix (when paired with implementation)
interface IRepository<T> { }
class MongoRepository<T> implements IRepository<T> { }
```

### Interface Members
- Use `camelCase`
- Be descriptive and clear
```typescript
interface UserProfile {
  firstName: string;
  lastName: string;
  dateOfBirth: Date;
  getFullName(): string;
}
```

## Types

### Type Aliases
- Use `PascalCase`
- Be descriptive of the type's purpose
```typescript
type UserId = string;
type ApiResponse<T> = {
  data: T;
  status: number;
};
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
```

### Generics
- Use `PascalCase`
- Single capital letter for simple cases
- Descriptive names for complex cases
```typescript
// Simple generic
function identity<T>(arg: T): T { }

// Complex generic
interface Repository<TEntity extends BaseEntity> { }
```

## Variables

### Constants
- Use `UPPER_SNAKE_CASE`
- Group related constants in const enums
```typescript
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';

const enum HttpStatus {
  OK = 200,
  NOT_FOUND = 404,
  INTERNAL_ERROR = 500
}
```

### Variables
- Use `camelCase`
- Be descriptive and clear
```typescript
let currentUser: User;
const userList: User[] = [];
let isLoading = false;
```

## Functions

### Function Names
- Use `camelCase`
- Use verb or verb phrases
- Be descriptive of the action
```typescript
function getUserById(id: string): Promise<User> { }
function validateEmail(email: string): boolean { }
function formatCurrency(amount: number, currency: string): string { }
```

### Parameters
- Use `camelCase`
- Be descriptive but concise
```typescript
function updateUser(userId: string, userData: UserUpdateData): Promise<User> { }
```

## Enums

### Enum Names
- Use `PascalCase`
- Use singular form
```typescript
enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  GUEST = 'guest'
}

enum LogLevel {
  ERROR = 'error',
  WARN = 'warn',
  INFO = 'info',
  DEBUG = 'debug'
}
```

## Namespaces
- Use `PascalCase`
- Use nouns or noun phrases
```typescript
namespace Validation {
  export interface StringValidator { }
}
```

## Imports and Exports

### Named Exports
- Match the name of the exported item
```typescript
export class UserService { }
export interface ApiResponse { }
export type UserId = string;
```

### Default Exports
- Match the file name (minus extension)
```typescript
// user-service.ts
export default class UserService { }
```

## Error Classes
- End with 'Error'
- Use `PascalCase`
```typescript
class ValidationError extends Error { }
class DatabaseConnectionError extends Error { }
class AuthenticationError extends Error { }
```

## Event Names
- Use `camelCase`
- Be descriptive of the event
```typescript
const onUserLogin = () => { };
const handleSubmit = () => { };
const emitUserUpdate = () => { };
```

## Best Practices

### General Guidelines
1. Be consistent throughout the project
2. Use meaningful and pronounceable names
3. Avoid abbreviations unless widely known
4. Use the same vocabularies for the same types of variables
5. Avoid using similar names with different meanings
6. Add meaningful context through naming

### Naming Length
- Shorter names for smaller scopes
- Longer, more descriptive names for larger scopes
```typescript
// Short scope
array.map(item => item.id);

// Larger scope
function calculateMonthlyRevenue(transactions: Transaction[]): number { }
```

### Boolean Variables
- Prefix with question words or be adjectives
```typescript
let isValid = false;
let hasPermission = true;
let shouldRedirect = false;
```

These conventions should be documented in your project's README or contributing guidelines and enforced through ESLint rules where possible.
