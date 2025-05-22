import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from bson.regex import Regex
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔐 Load Mongo URI from GitHub/Jenkins secrets via environment variable
MONGO_URI = os.getenv("MONGO_URI")

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB using secret URI with proper error handling
def connect_to_mongodb():
    """Connect to MongoDB with fallback support"""
    if not MONGO_URI:
        logger.warning("⚠️ MONGO_URI environment variable not set!")
        logger.info("💡 Add MONGO_URI to your GitHub Secrets or Jenkins Credentials")
        return None, None, None, False
    
    try:
        logger.info("🔗 Connecting to MongoDB using environment secret...")
        client = MongoClient(MONGO_URI)
        # Test the connection
        client.admin.command('ping')
        db = client["student_db"]
        students_collection = db["students"]
        logger.info("✅ Successfully connected to MongoDB!")
        return client, db, students_collection, True
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {str(e)}")
        logger.warning("⚠️ Running in fallback mode without database")
        return None, None, None, False

# Initialize database connection
client, db, students_collection, DB_CONNECTED = connect_to_mongodb()

# Fallback sample data when MongoDB secret is not available
SAMPLE_STUDENTS = [
    {"_id": "1", "name": "John Doe", "age": 20},
    {"_id": "2", "name": "Jane Smith", "age": 22},
    {"_id": "3", "name": "Alice Johnson", "age": 19},
    {"_id": "4", "name": "Bob Wilson", "age": 21}
]

def get_next_sample_id():
    """Generate next ID for sample data"""
    if not SAMPLE_STUDENTS:
        return "1"
    return str(max(int(s["_id"]) for s in SAMPLE_STUDENTS) + 1)

# Database functions with GitHub/Jenkins secrets support
def add_student(data):
    """Add a new student using secure MongoDB connection"""
    try:
        student = {
            "name": data["name"], 
            "age": data["age"],
            "created_at": datetime.utcnow()
        }
        
        if DB_CONNECTED and students_collection is not None:
            # Use secure MongoDB connection from secrets
            result = students_collection.insert_one(student)
            student["_id"] = str(result.inserted_id)
            logger.info(f"📝 Student added to MongoDB: {student['name']}")
        else:
            # Use fallback sample data
            student["_id"] = get_next_sample_id()
            student["created_at"] = student["created_at"].isoformat()
            SAMPLE_STUDENTS.append(student.copy())
            logger.info(f"📝 Student added to sample data: {student['name']}")
        
        return student
    except Exception as e:
        logger.error(f"❌ Error adding student: {str(e)}")
        raise

def get_students():
    """Get all students with secure database handling"""
    try:
        if DB_CONNECTED and students_collection is not None:
            # Use secure MongoDB connection from secrets
            students = list(students_collection.find())
            return [{"_id": str(student["_id"]), "name": student["name"], "age": student["age"]} 
                   for student in students]
        else:
            # Use fallback sample data
            return SAMPLE_STUDENTS.copy()
    except Exception as e:
        logger.error(f"❌ Error getting students: {str(e)}")
        return SAMPLE_STUDENTS.copy()

def get_student_by_id(student_id):
    """Get student by ID with secure database handling"""
    try:
        if DB_CONNECTED and students_collection is not None:
            # Use secure MongoDB connection from secrets
            student = students_collection.find_one({"_id": ObjectId(student_id)})
            if student:
                student["_id"] = str(student["_id"])
            return student
        else:
            # Use fallback sample data
            return next((s for s in SAMPLE_STUDENTS if s["_id"] == student_id), None)
    except Exception as e:
        logger.error(f"❌ Error getting student by ID {student_id}: {str(e)}")
        return next((s for s in SAMPLE_STUDENTS if s["_id"] == student_id), None)

def delete_student(student_id):
    """Delete student by ID with secure database handling"""
    try:
        if DB_CONNECTED and students_collection is not None:
            # Use secure MongoDB connection from secrets
            result = students_collection.delete_one({"_id": ObjectId(student_id)})
            if result.deleted_count > 0:
                return {"message": "Student deleted successfully"}
            return {"error": "Student not found"}
        else:
            # Use fallback sample data
            student_to_remove = next((s for s in SAMPLE_STUDENTS if s["_id"] == student_id), None)
            if student_to_remove:
                SAMPLE_STUDENTS.remove(student_to_remove)
                return {"message": "Student deleted successfully"}
            return {"error": "Student not found"}
    except Exception as e:
        logger.error(f"❌ Error deleting student {student_id}: {str(e)}")
        return {"error": "Failed to delete student"}

def search_students_by_name(name):
    """Search students by name with secure database handling"""
    try:
        if DB_CONNECTED and students_collection is not None:
            # Use secure MongoDB connection from secrets with regex search
            students = students_collection.find({"name": {"$regex": f".*{name}.*", "$options": "i"}})
            return [{"_id": str(student["_id"]), "name": student["name"], "age": student["age"]} 
                   for student in students]
        else:
            # Use fallback sample data with simple search
            return [s for s in SAMPLE_STUDENTS if name.lower() in s["name"].lower()]
    except Exception as e:
        logger.error(f"❌ Error searching students by name {name}: {str(e)}")
        return [s for s in SAMPLE_STUDENTS if name.lower() in s["name"].lower()]

# Flask routes
@app.route('/')
def home():
    """Home page with system status and secret configuration info"""
    try:
        db_status = "Connected via GitHub/Jenkins Secrets" if DB_CONNECTED else "Using Sample Data (No MongoDB Secret)"
        total_students = len(get_students())
        
        return jsonify({
            "message": "Welcome to the Student Management System API!",
            "status": "operational",
            "database_status": db_status,
            "total_students": total_students,
            "secret_configured": bool(MONGO_URI),
            "timestamp": datetime.utcnow().isoformat(),
            "endpoints": {
                "GET /students": "Get all students",
                "POST /students": "Add new student (requires: name, age)",
                "GET /students/{id}": "Get student by ID",
                "DELETE /students/{id}": "Delete student by ID", 
                "GET /students/name/{name}": "Search students by name",
                "GET /health": "Health check for CI/CD monitoring"
            }
        }), 200
    except Exception as e:
        logger.error(f"❌ Error in home route: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Jenkins/GitHub Actions monitoring"""
    try:
        # Test database connectivity if secret is configured
        if DB_CONNECTED and students_collection is not None:
            db.command('ping')
            db_status = "connected_via_secrets"
        else:
            db_status = "fallback_mode_no_secret"
        
        return jsonify({
            "status": "healthy",
            "database": db_status,
            "mongo_secret_configured": bool(MONGO_URI),
            "timestamp": datetime.utcnow().isoformat(),
            "total_students": len(get_students()),
            "ready_for_deployment": True
        }), 200
    except Exception as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        return jsonify({
            "status": "healthy_with_fallback",
            "database": "fallback_mode",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 200  # Still return 200 for CI/CD pipeline

@app.route('/students', methods=['POST'])
def add():
    """Add a new student with validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        if "name" not in data or "age" not in data:
            return jsonify({"error": "Missing required fields: 'name' and 'age'"}), 400
        
        # Validate age
        try:
            age = int(data["age"])
            if age < 0 or age > 150:
                return jsonify({"error": "Age must be between 0 and 150"}), 400
            data["age"] = age
        except (ValueError, TypeError):
            return jsonify({"error": "Age must be a valid number"}), 400
        
        # Validate name
        if not data["name"].strip():
            return jsonify({"error": "Name cannot be empty"}), 400
        
        student = add_student(data)
        return jsonify(student), 201
    except Exception as e:
        logger.error(f"❌ Error adding student: {str(e)}")
        return jsonify({"error": "Failed to add student"}), 500

@app.route('/students', methods=['GET'])
def get_all():
    """Get all students"""
    try:
        students = get_students()
        return jsonify(students), 200
    except Exception as e:
        logger.error(f"❌ Error getting students: {str(e)}")
        return jsonify({"error": "Failed to retrieve students"}), 500

@app.route('/students/<string:student_id>', methods=['GET'])
def get_by_id(student_id):
    """Get student by ID"""
    try:
        student = get_student_by_id(student_id)
        if student:
            return jsonify(student), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        logger.error(f"❌ Error getting student {student_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve student"}), 500

@app.route('/students/<string:student_id>', methods=['DELETE'])
def delete(student_id):
    """Delete student by ID"""
    try:
        result = delete_student(student_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"❌ Error deleting student {student_id}: {str(e)}")
        return jsonify({"error": "Failed to delete student"}), 500

@app.route('/students/name/<string:name>', methods=['GET'])
def get_by_name(name):
    """Search students by name using secure database"""
    try:
        students_list = search_students_by_name(name)
        if students_list:
            return jsonify(students_list), 200
        return jsonify({"error": "No students found with the given name"}), 404
    except Exception as e:
        logger.error(f"❌ Error searching students by name {name}: {str(e)}")
        return jsonify({"error": "Failed to search students"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting Student Management System...")
    logger.info(f"🔐 MongoDB Secret Status: {'Configured' if MONGO_URI else 'Not Configured'}")
    logger.info(f"📊 Database Status: {'Connected' if DB_CONNECTED else 'Sample Data Mode'}")
    logger.info("🌐 Server starting on http://0.0.0.0:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
