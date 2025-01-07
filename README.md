# Trail Management Micro-Service

Description
A micro-service for managing hiking trail data, built with Flask and connected to a Microsoft SQL Server database. The service provides CRUD operations through a RESTful API.

Features
- Add new trails
- Retrieve all trails
- Update existing trails
- Delete trails and associated locations

Technologies Used
- Flask (Python)
- Microsoft SQL Server
- Docker
- PyODBC

Prerequisites
- Python 3.10 or higher
- Docker Desktop
- Microsoft SQL Server
- Postman (optional, for API testing)

Endpoints:
- Base Endpoint (GET): /  
- Create Trail (POST): /create-trail  
- Get Trails (GET): /get-trails  
- Update Trail (PUT): /update-trail/<TrailID>  
- Delete Trail (DELETE): /delete-trail/<TrailID>  

The application is accessible at http://127.0.0.1:5001 when running locally.
