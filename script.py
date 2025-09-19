# Create comprehensive database schemas for the Digital Krishi Officer system

import pandas as pd
import json

# Database Schema Design
schemas = {
    "farmers": {
        "description": "Farmer profile and authentication data",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "phone": "VARCHAR(15) UNIQUE NOT NULL",
            "name": "VARCHAR(255)",
            "location_district": "VARCHAR(100)",
            "location_panchayat": "VARCHAR(100)",
            "location_coordinates": "POINT",
            "primary_crops": "TEXT[]",
            "farm_size_acres": "DECIMAL(8,2)",
            "language_preference": "VARCHAR(10) DEFAULT 'ml'",
            "created_at": "TIMESTAMP DEFAULT NOW()",
            "last_active": "TIMESTAMP DEFAULT NOW()",
            "is_verified": "BOOLEAN DEFAULT FALSE"
        },
        "indexes": [
            "CREATE INDEX idx_farmers_location ON farmers USING GIST (location_coordinates)",
            "CREATE INDEX idx_farmers_district ON farmers (location_district)",
            "CREATE INDEX idx_farmers_phone ON farmers (phone)"
        ]
    },
    
    "queries": {
        "description": "Farmer queries and AI responses",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "farmer_id": "INTEGER REFERENCES farmers(id)",
            "query_text": "TEXT NOT NULL",
            "query_type": "VARCHAR(20) CHECK (query_type IN ('voice', 'text', 'image'))",
            "voice_file_path": "VARCHAR(500)",
            "image_file_path": "VARCHAR(500)",
            "detected_intent": "VARCHAR(100)",
            "detected_entities": "JSONB",
            "cv_detection_results": "JSONB",
            "cv_confidence": "DECIMAL(3,2)",
            "rag_context": "TEXT",
            "ai_response": "TEXT",
            "ai_confidence": "DECIMAL(3,2)",
            "response_language": "VARCHAR(10)",
            "safety_flags": "TEXT[]",
            "is_escalated": "BOOLEAN DEFAULT FALSE",
            "escalation_reason": "VARCHAR(200)",
            "created_at": "TIMESTAMP DEFAULT NOW()",
            "processed_at": "TIMESTAMP",
            "response_time_ms": "INTEGER"
        },
        "indexes": [
            "CREATE INDEX idx_queries_farmer ON queries (farmer_id)",
            "CREATE INDEX idx_queries_created ON queries (created_at)",
            "CREATE INDEX idx_queries_escalated ON queries (is_escalated, created_at)",
            "CREATE INDEX idx_queries_intent ON queries (detected_intent)"
        ]
    },
    
    "escalations": {
        "description": "Cases escalated to agricultural officers",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "query_id": "INTEGER REFERENCES queries(id)",
            "farmer_id": "INTEGER REFERENCES farmers(id)",
            "assigned_officer_id": "INTEGER REFERENCES officers(id)",
            "status": "VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'assigned', 'in_progress', 'resolved', 'closed'))",
            "priority": "VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent'))",
            "officer_response": "TEXT",
            "resolution_notes": "TEXT",
            "created_at": "TIMESTAMP DEFAULT NOW()",
            "assigned_at": "TIMESTAMP",
            "resolved_at": "TIMESTAMP"
        },
        "indexes": [
            "CREATE INDEX idx_escalations_status ON escalations (status, created_at)",
            "CREATE INDEX idx_escalations_officer ON escalations (assigned_officer_id, status)",
            "CREATE INDEX idx_escalations_priority ON escalations (priority, created_at)"
        ]
    },
    
    "officers": {
        "description": "Agricultural officers who handle escalations",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "employee_id": "VARCHAR(20) UNIQUE NOT NULL",
            "name": "VARCHAR(255) NOT NULL",
            "designation": "VARCHAR(100)",
            "department": "VARCHAR(100)",
            "phone": "VARCHAR(15)",
            "email": "VARCHAR(255)",
            "assigned_districts": "TEXT[]",
            "specializations": "TEXT[]",
            "is_active": "BOOLEAN DEFAULT TRUE",
            "created_at": "TIMESTAMP DEFAULT NOW()",
            "last_login": "TIMESTAMP"
        },
        "indexes": [
            "CREATE INDEX idx_officers_employee_id ON officers (employee_id)",
            "CREATE INDEX idx_officers_districts ON officers USING GIN (assigned_districts)",
            "CREATE INDEX idx_officers_active ON officers (is_active)"
        ]
    },
    
    "feedback": {
        "description": "User feedback on AI responses",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "query_id": "INTEGER REFERENCES queries(id)",
            "farmer_id": "INTEGER REFERENCES farmers(id)",
            "rating": "INTEGER CHECK (rating BETWEEN 1 AND 5)",
            "feedback_type": "VARCHAR(20) CHECK (feedback_type IN ('helpful', 'not_helpful', 'incorrect', 'incomplete'))",
            "comments": "TEXT",
            "created_at": "TIMESTAMP DEFAULT NOW()"
        },
        "indexes": [
            "CREATE INDEX idx_feedback_query ON feedback (query_id)",
            "CREATE INDEX idx_feedback_rating ON feedback (rating, created_at)"
        ]
    },
    
    "knowledge_base": {
        "description": "Kerala agriculture knowledge for RAG system",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "title": "VARCHAR(500) NOT NULL",
            "content": "TEXT NOT NULL",
            "content_type": "VARCHAR(50) CHECK (content_type IN ('crop_guide', 'disease_treatment', 'pest_control', 'government_scheme', 'weather_advisory', 'market_info'))",
            "crops": "TEXT[]",
            "diseases": "TEXT[]",
            "pests": "TEXT[]",
            "applicable_districts": "TEXT[]",
            "applicable_seasons": "TEXT[]",
            "source": "VARCHAR(200)",
            "source_url": "VARCHAR(500)",
            "language": "VARCHAR(10) DEFAULT 'en'",
            "last_updated": "TIMESTAMP DEFAULT NOW()",
            "is_verified": "BOOLEAN DEFAULT FALSE"
        },
        "indexes": [
            "CREATE INDEX idx_knowledge_content_type ON knowledge_base (content_type)",
            "CREATE INDEX idx_knowledge_crops ON knowledge_base USING GIN (crops)",
            "CREATE INDEX idx_knowledge_diseases ON knowledge_base USING GIN (diseases)",
            "CREATE INDEX idx_knowledge_districts ON knowledge_base USING GIN (applicable_districts)",
            "CREATE INDEX idx_knowledge_updated ON knowledge_base (last_updated)"
        ]
    },
    
    "audit_logs": {
        "description": "System audit trail for security and compliance",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "user_id": "INTEGER",
            "user_type": "VARCHAR(20) CHECK (user_type IN ('farmer', 'officer', 'admin'))",
            "action": "VARCHAR(100) NOT NULL",
            "resource_type": "VARCHAR(50)",
            "resource_id": "INTEGER",
            "ip_address": "INET",
            "user_agent": "TEXT",
            "metadata": "JSONB",
            "created_at": "TIMESTAMP DEFAULT NOW()"
        },
        "indexes": [
            "CREATE INDEX idx_audit_user ON audit_logs (user_id, user_type)",
            "CREATE INDEX idx_audit_created ON audit_logs (created_at)",
            "CREATE INDEX idx_audit_action ON audit_logs (action)"
        ]
    }
}

# Convert to DataFrame for better display
schema_df = []
for table, details in schemas.items():
    for column, definition in details["columns"].items():
        schema_df.append({
            "table": table,
            "column": column,
            "definition": definition,
            "description": details["description"]
        })

schema_df = pd.DataFrame(schema_df)

# Save to CSV
schema_df.to_csv("database_schema.csv", index=False)
print("Database schema saved to database_schema.csv")

# Create sample data for Kerala crops and diseases
kerala_agri_data = {
    "major_crops": [
        {"name": "Rice", "malayalam": "നെൽ", "seasons": ["Kharif", "Rabi"], "districts": ["Palakkad", "Thrissur", "Malappuram"]},
        {"name": "Coconut", "malayalam": "തെങ്ങ്", "seasons": ["Year-round"], "districts": ["All districts"]},
        {"name": "Rubber", "malayalam": "റബ്ബർ", "seasons": ["Year-round"], "districts": ["Kottayam", "Pathanamthitta", "Idukki"]},
        {"name": "Black Pepper", "malayalam": "കുരുമുളക്", "seasons": ["Post-monsoon"], "districts": ["Wayanad", "Idukki", "Kozhikode"]},
        {"name": "Cardamom", "malayalam": "ഏലം", "seasons": ["October-December"], "districts": ["Idukki", "Wayanad"]},
        {"name": "Banana", "malayalam": "വാഴ", "seasons": ["Year-round"], "districts": ["Thiruvananthapuram", "Thrissur", "Palakkad"]},
        {"name": "Arecanut", "malayalam": "അടയ്ക്ക", "seasons": ["Year-round"], "districts": ["Kasaragod", "Kannur", "Kozhikode"]}
    ],
    
    "common_diseases": [
        {"name": "Rice Blast", "malayalam": "നെൽ ബ്ലാസ്റ്റ്", "crops": ["Rice"], "symptoms": "Leaf spots, neck rot", "treatment": "Carbendazim spray"},
        {"name": "Coconut Root Wilt", "malayalam": "തെങ്ങിന്റെ വേരുചീയൽ", "crops": ["Coconut"], "symptoms": "Yellowing of leaves", "treatment": "Bordeaux mixture"},
        {"name": "Rubber Leaf Fall", "malayalam": "റബ്ബർ ഇല വീഴ്ച", "crops": ["Rubber"], "symptoms": "Premature leaf fall", "treatment": "Copper fungicide"},
        {"name": "Pepper Quick Wilt", "malayalam": "കുരുമുളക് വാട്ടം", "crops": ["Black Pepper"], "symptoms": "Sudden wilting", "treatment": "Trichoderma application"},
        {"name": "Banana Bunchy Top", "malayalam": "വാഴ ബഞ്ചി ടോപ്പ്", "crops": ["Banana"], "symptoms": "Stunted growth", "treatment": "Remove affected plants"}
    ],
    
    "safety_rules": {
        "banned_pesticides": [
            "Endosulfan", "Methyl Parathion", "Phorate", "Triazophos", "Alachlor", "Lannate"
        ],
        "restricted_pesticides": [
            {"name": "2,4-D", "restrictions": ["Not for rice after panicle initiation"]},
            {"name": "Monocrotophos", "restrictions": ["Banned for vegetables"]}
        ],
        "dosage_limits": {
            "Carbendazim": {"max_concentration": "0.1%", "max_applications": 2},
            "Mancozeb": {"max_concentration": "0.25%", "max_applications": 3},
            "Copper fungicides": {"max_concentration": "0.3%", "max_applications": 3}
        }
    }
}

# Save Kerala agriculture data
with open("kerala_agriculture_data.json", "w", encoding="utf-8") as f:
    json.dump(kerala_agri_data, f, ensure_ascii=False, indent=2)

print("Kerala agriculture data saved to kerala_agriculture_data.json")
print(f"\nDatabase schema created with {len(schemas)} tables")
print(f"Schema details saved with {len(schema_df)} total columns")