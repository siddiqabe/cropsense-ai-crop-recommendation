# backend/init_db.py
from app import app, db
from models import User, SoilType, Crop, CropDetails, History, Recommendation, Feedback

def init_database():
    with app.app_context():
        # Drop all tables (careful! This deletes all data)
        print("⚠️ Dropping all existing tables...")
        db.drop_all()
        
        # Create all tables
        print("📊 Creating new tables...")
        db.create_all()
        
        print("\n✅ Database initialized successfully!")
        print("📋 Tables created:")
        print("   ✅ users")
        print("   ✅ soil_type")
        print("   ✅ crop")
        print("   ✅ crop_details")
        print("   ✅ history")
        print("   ✅ recommendation")
        print("   ✅ feedback")

if __name__ == '__main__':
    print("🚀 Starting Database Initialization...")
    init_database()
    print("\n✨ Done! You can now run 'python app.py'")