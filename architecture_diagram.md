# Website Scraper - Architecture Diagram

## System Overview

This is a **Streamlit-based Web Application** that combines **web scraping**, **vector database storage**, and **AI-powered chat functionality** to create an intelligent website content analyzer and Q&A system.

## Architecture Diagram

```mermaid
graph TB
    %% User Interface Layer
    subgraph "🎨 User Interface Layer"
        UI[Streamlit Web App]
        UI --> WS[Website Scraper Page]
        UI --> CD[Chat with Data Page]
        UI --> HOME[Home Page]
    end

    %% Core Application Layer
    subgraph "⚙️ Core Application Layer"
        SM[scrape_module.py]
        PDL[pineconeDataLoad.py]
        CM[chat_module.py]
    end

    %% External Services Layer
    subgraph "🌐 External Services"
        WEB[Target Websites]
        OPENAI[OpenAI API]
        PINECONE[Pinecone Vector DB]
    end

    %% Data Flow
    subgraph "📊 Data Processing Pipeline"
        SCRAPED[scraped_data.json]
        CLEANED[cleaned_file.json]
        VECTORS[Vector Embeddings]
    end

    %% Connections
    WS --> SM
    CD --> CM
    SM --> WEB
    SM --> SCRAPED
    PDL --> SCRAPED
    PDL --> CLEANED
    PDL --> OPENAI
    PDL --> PINECONE
    PDL --> VECTORS
    CM --> OPENAI
    CM --> PINECONE
    CM --> VECTORS

    %% Styling
    classDef uiLayer fill:#e1f5fe
    classDef coreLayer fill:#f3e5f5
    classDef externalLayer fill:#fff3e0
    classDef dataLayer fill:#e8f5e8

    class UI,WS,CD,HOME uiLayer
    class SM,PDL,CM coreLayer
    class WEB,OPENAI,PINECONE externalLayer
    class SCRAPED,CLEANED,VECTORS dataLayer
```

## Detailed Component Architecture

```mermaid
graph LR
    %% User Interface Components
    subgraph "🎨 Streamlit UI Components"
        direction TB
        HOME_PAGE[app.py - Home Page]
        SCRAPER_PAGE[1_Website_Scraper.py]
        CHAT_PAGE[2_Chat_With_Data.py]
    end

    %% Core Modules
    subgraph "⚙️ Core Modules"
        direction TB
        SCRAPE_MOD[scrape_module.py<br/>- Async web scraping<br/>- Playwright browser automation<br/>- BeautifulSoup parsing]
        PINECONE_MOD[pineconeDataLoad.py<br/>- Text cleaning & chunking<br/>- OpenAI embeddings<br/>- Pinecone vector storage]
        CHAT_MOD[chat_module.py<br/>- Query embedding<br/>- Vector similarity search<br/>- GPT-4 response generation]
    end

    %% Data Storage
    subgraph "💾 Data Storage"
        direction TB
        JSON_RAW[scraped_data.json<br/>Raw scraped content]
        JSON_CLEAN[cleaned_file.json<br/>Processed content]
        VECTOR_DB[Pinecone Index<br/>Vector embeddings]
    end

    %% External APIs
    subgraph "🔌 External APIs"
        direction TB
        OPENAI_API[OpenAI API<br/>- text-embedding-ada-002<br/>- gpt-4]
        PINECONE_API[Pinecone API<br/>Vector database]
    end

    %% Data Flow
    HOME_PAGE --> SCRAPER_PAGE
    HOME_PAGE --> CHAT_PAGE
    SCRAPER_PAGE --> SCRAPE_MOD
    CHAT_PAGE --> CHAT_MOD
    SCRAPE_MOD --> JSON_RAW
    PINECONE_MOD --> JSON_RAW
    PINECONE_MOD --> JSON_CLEAN
    PINECONE_MOD --> VECTOR_DB
    CHAT_MOD --> VECTOR_DB
    PINECONE_MOD --> OPENAI_API
    CHAT_MOD --> OPENAI_API
    PINECONE_MOD --> PINECONE_API
    CHAT_MOD --> PINECONE_API

    %% Styling
    classDef uiComp fill:#e3f2fd
    classDef coreComp fill:#f1f8e9
    classDef dataComp fill:#fff8e1
    classDef apiComp fill:#fce4ec

    class HOME_PAGE,SCRAPER_PAGE,CHAT_PAGE uiComp
    class SCRAPE_MOD,PINECONE_MOD,CHAT_MOD coreComp
    class JSON_RAW,JSON_CLEAN,VECTOR_DB dataComp
    class OPENAI_API,PINECONE_API apiComp
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant Scraper
    participant Playwright
    participant Website
    participant PineconeLoader
    participant OpenAI
    participant Pinecone
    participant ChatModule

    %% Scraping Flow
    User->>Streamlit: Enter URL & Start Scraping
    Streamlit->>Scraper: scrape_to_json(url, max_pages)
    Scraper->>Playwright: Launch browser
    loop For each page
        Playwright->>Website: Navigate to page
        Website-->>Playwright: Return HTML content
        Playwright->>Scraper: Extract text content
        Scraper->>Streamlit: Save to scraped_data.json
    end

    %% Vector Storage Flow
    Streamlit->>PineconeLoader: uploadFileOnPonecone()
    PineconeLoader->>PineconeLoader: Clean & chunk text
    PineconeLoader->>OpenAI: Generate embeddings
    OpenAI-->>PineconeLoader: Return vectors
    PineconeLoader->>Pinecone: Upsert vectors
    Pinecone-->>PineconeLoader: Confirm storage

    %% Chat Flow
    User->>Streamlit: Ask question
    Streamlit->>ChatModule: Process query
    ChatModule->>OpenAI: Embed query
    OpenAI-->>ChatModule: Query vector
    ChatModule->>Pinecone: Search similar vectors
    Pinecone-->>ChatModule: Relevant context
    ChatModule->>OpenAI: Generate response with context
    OpenAI-->>ChatModule: AI response
    ChatModule->>Streamlit: Display answer
    Streamlit->>User: Show response
```

## Technology Stack

### Frontend

- **Streamlit** - Web application framework
- **HTML/CSS** - Custom styling and layout

### Backend Processing

- **Python 3.12** - Core programming language
- **Asyncio** - Asynchronous web scraping
- **Playwright** - Browser automation
- **BeautifulSoup4** - HTML parsing

### AI & Machine Learning

- **OpenAI API** - Text embeddings (text-embedding-ada-002)
- **OpenAI GPT-4** - Natural language generation
- **Pinecone** - Vector database for similarity search

### Data Storage

- **JSON Files** - Local data storage
- **Pinecone Vector Database** - Cloud vector storage

### Development Tools

- **python-dotenv** - Environment variable management
- **tqdm** - Progress bars
- **textwrap** - Text processing

## Key Features

### 1. **Intelligent Web Scraping**

- Async crawling with Playwright
- Anti-detection measures
- Configurable page limits
- Automatic popup handling

### 2. **Vector Database Integration**

- Text chunking and cleaning
- OpenAI embeddings generation
- Pinecone vector storage
- Batch processing for efficiency

### 3. **AI-Powered Chat Interface**

- Semantic search capabilities
- Context-aware responses
- Chat history management
- Professional formatting

### 4. **User-Friendly Interface**

- Multi-page Streamlit app
- Real-time progress indicators
- Data preview functionality
- Download capabilities

## Environment Variables Required

```bash
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
```

## Performance Characteristics

- **Scalability**: Handles up to 500 pages per scraping session
- **Efficiency**: Batch processing for vector operations
- **Reliability**: Retry mechanisms for API calls
- **User Experience**: Real-time progress updates and error handling
