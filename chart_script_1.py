# Create a detailed AI/ML pipeline flow diagram for Digital Krishi Officer system
diagram_code = """
flowchart TD
    %% Input Processing Stage
    A[Voice Input] --> B[Malayalam ASR<br/>Whisper Model]
    C[Text Input] --> D[NLU Pipeline<br/>Intent Recognition]
    E[Image Input] --> F[YOLOv8<br/>Disease/Pest Detection]
    
    B --> G[Normalized Text]
    D --> H[Intent + Entities<br/>Extracted]
    F --> I[Disease Detection<br/>+ Confidence Score]
    
    %% Consolidation
    G --> J[Query Processing]
    H --> J
    I --> J
    
    %% Knowledge Retrieval RAG Stage
    J --> K[Query Embedding<br/>Vector Generation]
    K --> L[Vector Search<br/>Milvus Database]
    L --> M[(Kerala Agriculture<br/>Knowledge Base)]
    
    M --> N[Crop Database]
    M --> O[Disease Knowledge]
    M --> P[Treatment Guidelines]
    M --> Q[Government Schemes]
    
    N --> R[Top-K Documents<br/>Retrieved]
    O --> R
    P --> R
    Q --> R
    
    R --> S[Context Assembly<br/>Relevant Information]
    
    %% Answer Generation Stage
    S --> T[LLM Processing<br/>Query + Context + Location + Season]
    
    %% Safety Validation Stage
    T --> U[Safety Rules Engine]
    U --> V{Safety Validation}
    V -->|Pesticide Rules Check| W{Safe Dosage?}
    V -->|Banned Chemicals Check| X{Approved Chemical?}
    
    W -->|Yes| Y[Continue Processing]
    W -->|No| Z[Block Response]
    X -->|Yes| Y
    X -->|No| Z
    
    Y --> AA[Confidence Scoring]
    Z --> BB[Auto-escalate<br/>to Officer]
    
    %% Decision Logic Stage
    AA --> CC{Confidence Level}
    CC -->|High >0.8| DD[Direct Answer<br/>Generated]
    CC -->|Medium 0.5-0.8| EE[Answer with<br/>Disclaimer]
    CC -->|Low <0.5| FF[Auto-escalate<br/>to Officer]
    
    %% Malayalam Translation
    DD --> GG[Malayalam Translation<br/>Output Generation]
    EE --> GG
    
    %% Response Delivery Stage
    GG --> HH[Response Delivery<br/>Multi-modal Output]
    
    HH --> II[Text Display<br/>UI Interface]
    HH --> JJ[TTS Audio<br/>Malayalam Voice]
    HH --> KK[Source Citations<br/>Knowledge Provenance]
    HH --> LL[Confidence Indicator<br/>UI Display]
    
    %% Officer Escalation Path
    BB --> MM[Officer Review<br/>Manual Processing]
    FF --> MM
    MM --> NN[Manual Response<br/>Expert Answer]
    NN --> HH
    
    %% Feedback Loop
    II --> OO[User Feedback<br/>Collection]
    OO --> PP[Model Retraining<br/>Continuous Learning]
    PP --> K
    
    MM --> QQ[Officer Corrections<br/>Knowledge Update]
    QQ --> PP
    
    %% Styling for different node types
    classDef inputNode fill:#B3E5EC,stroke:#1FB8CD,stroke-width:2px
    classDef processNode fill:#A5D6A7,stroke:#2E8B57,stroke-width:2px
    classDef decisionNode fill:#FFEB8A,stroke:#D2BA4C,stroke-width:2px
    classDef dataNode fill:#FFCDD2,stroke:#DB4545,stroke-width:2px
    classDef safetyNode fill:#9FA8B0,stroke:#5D878F,stroke-width:2px
    classDef escalationNode fill:#FFB3BA,stroke:#B4413C,stroke-width:2px
    
    class A,C,E inputNode
    class B,D,F,G,H,I,J,K,L,S,T,AA,GG,HH,II,JJ,KK,LL,PP processNode
    class V,W,X,CC decisionNode
    class M,N,O,P,Q dataNode
    class U,Y,Z safetyNode
    class BB,FF,MM,NN,OO,QQ escalationNode
"""

# Create the mermaid diagram
png_path, svg_path = create_mermaid_diagram(
    diagram_code, 
    png_filepath='krishi_pipeline.png',
    svg_filepath='krishi_pipeline.svg',
    width=1400,
    height=1000
)

print(f"Digital Krishi Officer AI/ML Pipeline diagram saved as:")
print(f"PNG: {png_path}")
print(f"SVG: {svg_path}")