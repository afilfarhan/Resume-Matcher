# Backend Architecture Deep Dive

## Module Organization

```
apps/backend/app/
├── main.py              # FastAPI app entry point, lifespan, routers
├── config.py            # Settings, env vars, API key management
├── config_cache.py      # TTL-cached config reads
├── crypto.py            # Fernet encrypt/decrypt for API keys
├── database.py          # Async SQLAlchemy/SQLite facade
├── db_engine.py         # Engine/session factories
├── models.py            # SQLAlchemy ORM models
├── llm.py               # LiteLLM wrapper, multi-provider support
├── pdf.py               # Headless Chromium PDF rendering
├── routers/             # HTTP endpoints
│   ├── __init__.py
│   ├── health.py        # Health checks
│   ├── config.py        # Config management
│   ├── resumes.py       # Resume CRUD + tailoring
│   ├── jobs.py          # Job description management
│   ├── applications.py  # Kanban tracker
│   ├── enrichment.py    # AI enrichment
│   └── resume_wizard.py # Resume wizard endpoints
├── services/            # Business logic
│   ├── __init__.py
│   ├── parser.py        # Document parsing, date restoration
│   ├── improver.py      # Resume tailoring with diffs
│   ├── refiner.py       # Keyword injection, AI phrase removal
│   ├── cover_letter.py  # Cover letter generation
│   └── resume_wizard.py # Resume wizard service
├── schemas/             # Pydantic models
│   ├── __init__.py
│   ├── models.py        # ResumeData, Job, Application schemas
│   ├── applications.py  # Tracker schemas
│   ├── refinement.py    # Refinement config
│   ├── enrichment.py    # Enrichment schemas
│   └── resume_wizard.py # Wizard schemas
├── prompts/             # LLM templates
│   ├── __init__.py
│   ├── templates.py     # Main prompt templates
│   ├── enrichment.py    # Enrichment prompts
│   ├── refinement.py    # Refinement prompts
│   └── resume_wizard.py # Wizard prompts
└── scripts/             # Utilities
    ├── __init__.py
    └── migrate_tinydb_to_sqlite.py
```

## Database Schema

### Tables

1. **resumes** - Master and tailored resumes
   - Fields: resume_id, content, content_type, filename, is_master, parent_id, processed_data, processing_status, cover_letter, outreach_message, title, original_markdown, created_at, updated_at
   - Unique constraint: is_master (only one master resume)

2. **jobs** - Job descriptions
   - Fields: job_id, content, resume_id, created_at, metadata_json
   - Dynamic fields stored in metadata_json: job_keywords, preview_hash, company, role

3. **improvements** - Tailoring history
   - Fields: request_id, original_resume_id, tailored_resume_id, job_id, improvements, created_at

4. **applications** - Kanban tracker cards
   - Fields: application_id, job_id, resume_id, master_resume_id, status, company, role, applied_at, notes, position, created_at, updated_at
   - Statuses: saved, applied, no_response, response, interview, accepted, rejected

5. **api_keys** - Encrypted API keys
   - Fields: provider, ciphertext, updated_at
   - Encrypted using Fernet in crypto.py

## API Endpoints

### Health & Status
- GET /api/v1/health - Liveness probe
- GET /api/v1/status - Full system status (LLM health + DB stats)

### Configuration
- GET/PUT /api/v1/config/llm-api-key - Get/update provider config
- GET/POST/DELETE /api/v1/config/api-keys - Provider key management
- POST /api/v1/config/llm-test - Test LLM connection
- GET/PUT /api/v1/config/features - Feature flags
- GET/PUT /api/v1/config/language - Content language
- GET/PUT /api/v1/config/prompts - Prompt options
- PUT /api/v1/config/feature-prompts - Custom prompts
- POST /api/v1/config/reset - Reset database

### Resumes
- POST /api/v1/resumes/upload - Upload PDF/DOCX
- GET /api/v1/resumes - List all resumes
- GET /api/v1/resumes/{id} - Get resume details
- PATCH /api/v1/resumes/{id} - Update resume
- DELETE /api/v1/resumes/{id} - Delete resume
- POST /api/v1/resumes/improve/preview - Generate tailored resume preview
- POST /api/v1/resumes/improve/confirm - Confirm and save tailored resume
- POST /api/v1/resumes/{id}/retry-processing - Retry failed processing
- GET /api/v1/resumes/{id}/pdf - Download resume PDF
- PATCH /api/v1/resumes/{id}/cover-letter - Update cover letter
- POST /api/v1/resumes/{id}/cover-letter/pdf - Download cover letter PDF
- PATCH /api/v1/resumes/{id}/outreach - Update outreach message
- PATCH /api/v1/resumes/{id}/title - Update resume title

### Jobs
- POST /api/v1/jobs/upload - Upload job descriptions (batch)
- GET /api/v1/jobs/{id} - Get job details

### Applications (Tracker)
- GET /api/v1/applications - List all applications (grouped by status)
- POST /api/v1/applications - Create application (manual add)
- PATCH /api/v1/applications/{id} - Update application
- PATCH /api/v1/applications/bulk - Bulk status update
- DELETE /api/v1/applications/{id} - Delete application
- DELETE /api/v1/applications/bulk - Bulk delete

### Enrichment
- POST /api/v1/enrichment/analyze/{id} - Analyze resume
- POST /api/v1/enrichment/enhance - Enhance resume
- POST /api/v1/enrichment/apply/{id} - Apply enhancements
- POST /api/v1/enrichment/regenerate - Regenerate enrichment
- POST /api/v1/enrichment/apply-regenerated/{id} - Apply regenerated enhancements

## LLM Integration

### Provider Support
- OpenAI (GPT-5, GPT-4o)
- Anthropic (Claude 3.7)
- Google Gemini (Gemini 3 Flash)
- OpenRouter (multiple models)
- DeepSeek (DeepSeek Chat)
- Ollama (local models)
- Groq
- NVIDIA NIM

### Key Functions
- get_llm_config() - Get current provider configuration
- get_model_name(config) - Convert to LiteLLM format
- get_router(config) - Get LiteLLM Router with retry policies
- check_llm_health() - Test provider connectivity
- complete() - Text completion
- complete_json() - JSON completion with retries

### Retry Policy
- AuthenticationError: 0 retries
- BadRequestError: 0 retries
- TimeoutError: 2 retries
- RateLimitError: 3 retries
- ContentPolicyViolation: 0 retries
- InternalServerError: 2 retries

## Data Models

### ResumeData (Pydantic)
- personalInfo: PersonalInfo
- summary: str
- workExperience: list[WorkExperience]
- education: list[Education]
- skills: list[str]
- additional: Additional
- personalProjects: list[PersonalProject]
- customSections: dict[str, CustomSection]
- sectionMeta: SectionMeta

### Application Status Flow
saved → applied → no_response → response → interview → accepted/rejected

## Security Features

1. API Keys: Encrypted with Fernet, stored in SQLite
2. Prompt Injection Prevention: Input sanitization in improver.py
3. Secret Redaction: Error messages scrubbed of API keys
4. Single Master Resume: Enforced via database constraint + asyncio.Lock
5. Access Control: CORS middleware with configurable origins
