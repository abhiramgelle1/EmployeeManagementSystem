# Employee Management System

An enterprise-grade Employee Management System designed to streamline workforce operations through efficient employee data handling, department organization, and secure authentication. This project demonstrates clean architecture, scalable backend design, and professional software engineering practices.

## Overview

The Employee Management System (EMS) is a full-stack application that enables organizations to manage their employees, departments, and roles efficiently.  
It includes secure role-based authentication, CRUD operations for all modules, and API-first design principles suitable for enterprise-level deployments.

## Features

- Employee CRUD Operations – Add, update, delete, and view employee records  
- Department Management – Assign and manage employees by department  
- Authentication & Authorization – Secure login using JWT and role-based access  
- Dashboard Interface – Display employee statistics and summaries  
- Scalable Architecture – Designed for extensibility and large data handling  
- Database Integration – Supports relational databases like MySQL/PostgreSQL  
- Audit & Validation – Automatic tracking of created/updated records  

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | React / Angular / Flutter (based on implementation) |
| Backend | Spring Boot (Java 17+), Spring Security, REST APIs |
| Database | MySQL / PostgreSQL |
| Tools | Maven, Docker, Postman, Swagger UI |
| Authentication | JWT (JSON Web Tokens) |

## Project Structure

```
EmployeeManagementSystem/
│
├── src/
│   ├── main/
│   │   ├── java/com/ems/
│   │   │   ├── controller/      # REST controllers
│   │   │   ├── service/         # Business logic
│   │   │   ├── repository/      # JPA repositories
│   │   │   ├── model/           # Entity classes
│   │   │   ├── config/          # Security, CORS, etc.
│   │   │   └── dto/             # Data Transfer Objects
│   │   └── resources/
│   │       ├── application.yml  # Configuration file
│   │       └── db/migration/    # Database migrations (Flyway)
│   └── test/                    # Unit and integration tests
│
├── Dockerfile
├── docker-compose.yml
├── pom.xml
└── README.md
```

## Setup Instructions

### Clone Repository
```bash
git clone https://github.com/abhiramgelle1/EmployeeManagementSystem.git
cd EmployeeManagementSystem
```

### Configure Environment
Edit `src/main/resources/application.yml` to match your database credentials:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/ems
    username: postgres
    password: admin
  jpa:
    hibernate:
      ddl-auto: update
```

### Build and Run
```bash
mvn clean install
mvn spring-boot:run
```

### Access Application
- Swagger UI: http://localhost:8080/swagger-ui.html
- API Docs: http://localhost:8080/v3/api-docs

## API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | /api/v1/auth/login | Login with credentials |
| GET | /api/v1/employees | Retrieve all employees |
| GET | /api/v1/employees/{id} | Get specific employee details |
| POST | /api/v1/employees | Add a new employee |
| PUT | /api/v1/employees/{id} | Update employee details |
| DELETE | /api/v1/employees/{id} | Delete an employee |
| GET | /api/v1/departments | List all departments |
| POST | /api/v1/departments | Create a new department |

## Testing

Run unit and integration tests using:
```bash
mvn test
```

## Run with Docker

To run the full application stack using Docker:

```bash
docker-compose up --build
```

This will start:
- PostgreSQL container  
- Employee Management System container

## Example Requests

**Create Employee**
```bash
curl -X POST http://localhost:8080/api/v1/employees -H "Content-Type: application/json" -d '{
  "firstName": "Abhiram",
  "lastName": "Gelle",
  "email": "abhiram@company.com",
  "departmentId": 1
}'
```

**Login**
```bash
curl -X POST http://localhost:8080/api/v1/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}'
```

## Future Enhancements

- Attendance & Leave management  
- Payroll integration  
- Notifications & activity logs  
- Multi-tenant architecture for enterprise use  

## Author

**Abhiram Gelle**  
Full Stack Developer | Software Engineer  
Email: abhiramgelle738@gmail.com  
GitHub: https://github.com/abhiramgelle1
