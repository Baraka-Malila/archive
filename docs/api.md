# Archives Web App API Backend Documentation

## Overview
This backend powers the Archives Web App, providing a robust API for managing users, courses, departments, assignments, resources, and submissions in an academic context. It is built with Django and Django REST Framework, supporting role-based access for students, lecturers, and class representatives.

## API Endpoints

### Authentication (Centralized in Custom App)
- `POST /api/auth/login/`: User login
- `POST /api/auth/logout/`: User logout
- `GET /api/auth/whoami/`: Get current user info
- `GET /api/auth/role/`: Get user role
- `GET /api/auth/csrf/`: Get CSRF token
- `GET /api/auth/check/`: Check authentication status
- `GET /api/auth/session/`: Get session information

### User Management
- `GET /api/users/`: List users (filtered by username)
- `GET /api/users/profile/`: Get user profile
- `PUT /api/users/update/`: Update user profile
- `DELETE /api/users/delete/`: Delete user account

### Student API
- `GET /api/student/student_dashboard/`: Student dashboard
- `PUT /api/student/update/`: Update student profile
- `DELETE /api/student/delete/`: Delete student account
- `GET /api/student/submissions/`: List student submissions
- `POST /api/student/submissions/`: Create submission
- `GET /api/student/submissions/<id>/`: Get submission details
- `GET /api/student/resources/`: List available resources
- `GET /api/student/resources/download/<id>/`: Download resource file

### Lecturer API
- `GET /api/lecture/lecture_dashboard/`: Lecturer dashboard
- `GET /api/lecture/retrieve_user/<username>/`: Get lecturer profile
- `PUT /api/lecture/update/`: Update lecturer profile
- `DELETE /api/lecture/delete/`: Delete lecturer account
- `GET /api/lecture/assignments/`: List assignments
- `POST /api/lecture/assignments/`: Create assignment
- `GET /api/lecture/assignments/<id>/`: Get assignment details
- `PUT /api/lecture/assignments/<id>/`: Update assignment
- `DELETE /api/lecture/assignments/<id>/`: Delete assignment
- `GET /api/lecture/submissions/`: List student submissions
- `PATCH /api/lecture/submissions/<id>/feedback/`: Provide submission feedback

### Resources API
- `GET /api/resources/`: List resources
- `POST /api/resources/`: Create resource (Lecturer/CR only)
- `GET /api/resources/<id>/`: Get resource details
- `PUT /api/resources/<id>/`: Update resource (Lecturer/CR only)
- `DELETE /api/resources/<id>/`: Delete resource (Lecturer/CR only)
- `GET /api/resources/download/<id>/`: Download resource file

## Authentication & Authorization

### Session Authentication
- All endpoints use Django's session authentication
- CSRF protection is enabled for all POST/PUT/DELETE requests
- Session cookies are HTTP-only and SameSite=Lax

### Role-Based Access
- Students: Can access student dashboard, submissions, and resources
- Lecturers: Can manage assignments, provide feedback, and manage resources
- Class Representatives: Can manage resources and view submissions

### Permissions
- `IsAuthenticated`: Required for all endpoints
- `IsLecturerOrClassRep`: Required for resource management
- Role-specific permissions are enforced at the view level

## Data Models

### User Model
- Custom user model with role-based access
- Fields: username, email, full_name, role, etc.
- Role-specific fields for students and lecturers

### Resource Model
- Fields: id, group_id, course_id, assignment, resource_type, resource_url, resource_file, etc.
- File handling for resource uploads
- Active/inactive status tracking

### Assignment Model
- Fields: id, group_id, course_id, title, description, due_date, version, etc.
- Created/updated tracking
- Maximum score configuration

### Submission Model
- Fields: id, assignment, student, submission_date, score, feedback, etc.
- Attempt tracking
- File checksum verification

## Frontend Integration

### Authentication Flow
1. Frontend should implement login/register forms
2. Store session token after successful authentication
3. Include session token in all subsequent requests
4. Handle role-based UI rendering based on user role

### API Integration
1. Use axios or fetch for API calls
2. Implement proper error handling
3. Handle file uploads using FormData
4. Implement proper loading states

### File Handling
1. Use proper content types for file uploads
2. Handle large file uploads with progress tracking
3. Implement proper file download handling
4. Validate file types and sizes on frontend

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Security Considerations
1. All endpoints require authentication except login/register
2. File uploads are validated for type and size
3. Role-based access control for sensitive operations
4. Session-based authentication with proper security measures
5. File downloads are protected and require authentication

## Limitations
1. File size limits for uploads
2. Supported file types restrictions
3. Maximum number of submissions per assignment
4. Role-based access restrictions
5. Session timeout after inactivity

## Frontend Team Guidelines
1. Implement proper error handling for all API calls
2. Use proper loading states for async operations
3. Implement proper form validation
4. Handle file uploads with progress tracking
5. Implement proper session management
6. Follow role-based UI rendering
7. Implement proper error messages for users
8. Handle API rate limiting
9. Implement proper file download handling
10. Follow security best practices

## API Response Formats and Error Handling

### Standard Response Format
All API responses follow this structure:
```json
{
    "data": {},           // Main response data
    "message": "",        // Success/error message
    "error": "",          // Error details if any
    "status": 200,        // HTTP status code
    "meta": {            // Optional metadata
        "pagination": {}, // For paginated responses
        "filters": {},    // Applied filters
        "sort": {}        // Applied sorting
    }
}
```

### Error Response Format
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {} // Additional error details
    },
    "status": 400
}
```

### Common Error Codes
1. **Authentication Errors (401)**:
   - `INVALID_CREDENTIALS`: Wrong username/password
   - `SESSION_EXPIRED`: Session timeout
   - `INVALID_TOKEN`: Invalid authentication token

2. **Authorization Errors (403)**:
   - `INSUFFICIENT_PERMISSIONS`: Role-based access denied
   - `RESOURCE_ACCESS_DENIED`: Resource access denied
   - `OPERATION_NOT_ALLOWED`: Action not allowed for role

3. **Validation Errors (400)**:
   - `INVALID_INPUT`: Invalid request data
   - `FILE_TOO_LARGE`: File size exceeds limit
   - `INVALID_FILE_TYPE`: Unsupported file type
   - `DUPLICATE_ENTRY`: Resource already exists

4. **Resource Errors (404)**:
   - `RESOURCE_NOT_FOUND`: Requested resource not found
   - `FILE_NOT_FOUND`: Requested file not found
   - `USER_NOT_FOUND`: User not found

5. **Server Errors (500)**:
   - `INTERNAL_ERROR`: Unexpected server error
   - `DATABASE_ERROR`: Database operation failed
   - `FILE_PROCESSING_ERROR`: File processing failed

### Rate Limiting
- Standard rate limit: 100 requests per minute
- File upload limit: 10 requests per minute
- Rate limit headers included in response:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1620000000
  ```

### Pagination
List endpoints support pagination with these parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

Response includes pagination metadata:
```json
{
    "meta": {
        "pagination": {
            "total": 100,
            "page": 1,
            "page_size": 10,
            "total_pages": 10
        }
    }
}
```

## API Capabilities and Limitations

### Resource Management
1. **File Upload Capabilities**:
   - Supports multiple file types
   - File size limits enforced
   - Automatic file type validation
   - Secure file storage with checksums
   - Progress tracking for large uploads

2. **Resource Organization**:
   - Hierarchical structure (Department > Course > Assignment)
   - Group-based resource sharing
   - Active/inactive status tracking
   - Version control for resources
   - Metadata management (type, description, upload info)

3. **Access Control**:
   - Role-based access (Student, Lecturer, Class Representative)
   - Course-level permissions
   - Group-level permissions
   - Resource-level visibility control

### Assignment System
1. **Assignment Management**:
   - Create, update, delete assignments
   - Set due dates and maximum scores
   - Version tracking
   - Active/inactive status
   - Course and group association

2. **Submission Handling**:
   - Multiple submission attempts
   - File upload support
   - Automatic attempt tracking
   - Checksum verification
   - Grading system integration

3. **Feedback System**:
   - Score assignment
   - Written feedback
   - Grading status tracking
   - Submission history

### User Management
1. **Role-Based Access**:
   - Student: View resources, submit assignments
   - Lecturer: Manage resources, create assignments, grade submissions
   - Class Representative: Limited resource management

2. **Profile Management**:
   - Basic info (name, email, username)
   - Role-specific fields
   - Department and course associations
   - Year of study (for students)
   - Title and department (for lecturers)

### API Limitations
1. **Rate Limiting**:
   - Per-user request limits
   - Concurrent request restrictions
   - File upload size limits
   - Session timeout after inactivity

2. **File Handling**:
   - Maximum file size: 10MB
   - Supported file types: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, ZIP, RAR
   - Maximum number of files per resource: 1
   - File name length limit: 255 characters

3. **Data Constraints**:
   - Maximum course code length: 5 characters
   - Maximum assignment title length: 200 characters
   - Maximum resource description length: 1000 characters
   - Maximum feedback length: 2000 characters

4. **Access Restrictions**:
   - Students cannot modify resources
   - Students cannot delete submissions
   - Lecturers cannot modify other lecturers' resources
   - Class representatives have limited resource management rights


### A. Student App

#### List resources:
http://127.0.0.1:8000/api/student/resources/
### Submit assignment:
http://127.0.0.1:8000/api/student/submissions/ (POST)
### View own submissions:
http://127.0.0.1:8000/api/student/submissions/

### B. Resources App
#### List resources:
http://127.0.0.1:8000/api/resources/resources/
#### Download resource:
http://127.0.0.1:8000/api/resources/resources/download/<id>/

### C. Lecture App

#### List assignments:
http://127.0.0.1:8000/api/lecture/assignments/
#### List submissions:
http://127.0.0.1:8000/api/lecture/submissions/
#### Give feedback:
http://127.0.0.1:8000/api/lecture/submissions/<id>/feedback/ (PATCH)

### D. Custom App

#### List users:
http://127.0.0.1:8000/api/custom/user/
#### Get own profile:
http://127.0.0.1:8000/api/custom/profile/
#### Get own role:
http://127.0.0.1:8000/api/custom/role/

