# Create a vertically-oriented, improved system architecture diagram using Mermaid
diagram_code = """
flowchart TD
    %% Mobile App Layer - Top Layer
    subgraph Mobile["📱 MOBILE APP LAYER - Flutter"]
        direction TB
        subgraph MobileFeatures["User Interface Features"]
            direction LR
            MA1["OTP Login System"]
            MA2["Voice Recording<br/>Malayalam ASR Input"]
            MA3["Text Input Interface"]
        end
        subgraph MobileActions["User Actions"]
            direction LR
            MA4["Image Capture<br/>with Guidance Overlay"]
            MA5["TTS Answer Display"]
            MA6["Escalation Button"]
            MA7["Query History View"]
        end
    end

    %% API Gateway - Second Layer
    subgraph API["🔗 BACKEND API GATEWAY - FastAPI"]
        direction TB
        LB["Load Balancer & Authentication"]
        subgraph APIEndpoints["REST API Endpoints"]
            direction LR
            API1["/query<br/>Main Query Handler"]
            API2["/asr<br/>Speech to Text"]
            API3["/cv<br/>Computer Vision"]
            API4["/rag<br/>Knowledge Retrieval"]
            API5["/llm<br/>Answer Generation"]
            API6["/escalate<br/>Officer Escalation"]
            API7["/feedback<br/>User Feedback"]
        end
    end

    %% AI/ML Services - Third Layer
    subgraph AIML["🤖 AI/ML PROCESSING PIPELINE"]
        direction TB
        subgraph InputProcessing["Input Processing Services"]
            direction LR
            ASR["Malayalam ASR<br/>Whisper Fine-tuned Model"]
            NLU["Natural Language Understanding<br/>Intent & Entity Extraction"]
            CV["Computer Vision<br/>YOLOv8 Crop Disease Detection"]
        end
        subgraph KnowledgeGen["Knowledge & Generation"]
            direction LR
            RAG["RAG System<br/>Vector Knowledge Retrieval"]
            LLM["Large Language Model<br/>Llama 2 / Mistral"]
            SAFETY["Safety Rules Engine<br/>Content Validation"]
        end
    end

    %% Data Storage - Fourth Layer
    subgraph DATA["💾 DATA STORAGE LAYER"]
        direction LR
        PG["PostgreSQL Database<br/>Farmer Profiles<br/>Query Records<br/>Case Management"]
        S3["Amazon S3 Storage<br/>Voice Files<br/>Image Assets<br/>Media Content"]
        MILVUS["Milvus Vector Database<br/>Kerala Agriculture<br/>Knowledge Embeddings"]
        REDIS["Redis Cache<br/>Session Management<br/>Quick Access Data"]
    end

    %% Officer Dashboard - Fifth Layer
    subgraph DASH["👨‍💼 OFFICER DASHBOARD - React Web App"]
        direction LR
        DASH1["Authentication<br/>Login System"]
        DASH2["Escalation Queue<br/>Case Management"]
        DASH3["Response Tools<br/>Template Library"]
        DASH4["Analytics Dashboard<br/>Performance Reports"]
    end

    %% Infrastructure - Bottom Layer
    subgraph INFRA["☁️ INFRASTRUCTURE LAYER - Kubernetes"]
        direction LR
        K8S["Kubernetes Orchestration<br/>Container Management"]
        MODEL["Model Serving Platform<br/>Triton Inference Server<br/>TorchServe"]
        MON["Monitoring Stack<br/>Prometheus & Grafana"]
        CICD["CI/CD Pipeline<br/>Automated Deployment"]
    end

    %% Primary Data Flow - Vertical Flow
    Mobile ==> LB
    LB ==> API1
    
    %% API to Services Flow
    API1 --> ASR
    API1 --> NLU
    API2 --> ASR
    API3 --> CV
    API4 --> RAG
    API5 --> LLM
    API6 --> DASH2
    API7 --> PG
    
    %% AI/ML Pipeline Flow
    ASR --> NLU
    NLU --> RAG
    RAG --> LLM
    LLM --> SAFETY
    
    %% Data Connections
    ASR --> S3
    CV --> S3
    CV --> PG
    RAG --> MILVUS
    SAFETY --> PG
    LB --> REDIS
    
    %% Officer Dashboard Connections
    DASH2 --> PG
    DASH3 --> API5
    DASH4 --> PG
    
    %% Infrastructure Support
    InputProcessing --> MODEL
    KnowledgeGen --> MODEL
    APIEndpoints --> K8S
    DASH --> K8S
    MON --> K8S
    CICD --> K8S
    
    %% Styling for better visual separation
    classDef mobileLayer fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    classDef apiLayer fill:#FFF3E0,stroke:#F57C00,stroke-width:3px
    classDef aimlLayer fill:#E8F5E8,stroke:#388E3C,stroke-width:3px
    classDef dataLayer fill:#FFF8E1,stroke:#FBC02D,stroke-width:3px
    classDef dashLayer fill:#F3E5F5,stroke:#7B1FA2,stroke-width:3px
    classDef infraLayer fill:#FAFAFA,stroke:#616161,stroke-width:3px
    
    class Mobile,MobileFeatures,MobileActions,MA1,MA2,MA3,MA4,MA5,MA6,MA7 mobileLayer
    class API,LB,APIEndpoints,API1,API2,API3,API4,API5,API6,API7 apiLayer
    class AIML,InputProcessing,KnowledgeGen,ASR,NLU,CV,RAG,LLM,SAFETY aimlLayer
    class DATA,PG,S3,MILVUS,REDIS dataLayer
    class DASH,DASH1,DASH2,DASH3,DASH4 dashLayer
    class INFRA,K8S,MODEL,MON,CICD infraLayer
"""

# Create the diagram with optimal dimensions for vertical layout
create_mermaid_diagram(diagram_code, 'architecture_diagram.png', 'architecture_diagram.svg', width=1600, height=1800)

print("Final improved system architecture diagram created!")
print("Key improvements implemented:")
print("✓ Vertical layered layout for better flow readability")
print("✓ All components from instructions explicitly labeled")
print("✓ Clearer subgroupings within each layer")
print("✓ Better visual separation with distinct colors per layer")
print("✓ Reduced arrow overlapping with logical flow paths")
print("✓ Larger text labels for improved readability")
print("✓ Proper aspect ratio to minimize whitespace")
print("Files saved: architecture_diagram.png and architecture_diagram.svg")