# Frontend Architecture Deep Dive

## Directory Structure

apps/frontend/
├── app/
│   ├── (default)/           # Main app routes
│   │   ├── page.tsx         # Landing (/)
│   │   ├── layout.tsx       # Root layout
│   │   ├── dashboard/       # /dashboard - Resume list
│   │   ├── builder/         # /builder - Resume editor
│   │   ├── tailor/          # /tailor - Job description input
│   │   ├── settings/        # /settings - LLM config
│   │   └── resumes/[id]/    # /resumes/[id] - Single resume view
│   └── print/               # Print routes for PDF
│       ├── resumes/[id]/page.tsx
│       └── cover-letter/[id]/page.tsx
├── components/
│   ├── ui/                  # Primitives (Button, Input, Dialog, etc.)
│   ├── builder/             # Resume builder components
│   ├── dashboard/           # Dashboard components
│   ├── tailor/              # Tailor page components
│   ├── tracker/             # Application tracker
│   ├── enrichment/          # AI enrichment wizard
│   ├── resume/              # Resume templates
│   ├── preview/             # Paginated preview
│   ├── home/                # Landing page
│   └── common/              # Shared components
├── lib/
│   ├── api/                 # Backend client
│   ├── i18n/                # Translation engine
│   ├── context/             # React contexts
│   ├── utils/               # Utility functions
│   ├── types/               # TypeScript types
│   ├── config/              # Config constants
│   └── constants/           # Constants
├── hooks/                   # Custom hooks
├── i18n/                    # i18n configuration
├── messages/                # Translation files
├── tests/                   # Vitest tests
├── public/                  # Static assets
├── next.config.ts           # Next.js config
├── vitest.config.ts         # Vitest config
├── vitest.setup.ts          # Test setup
├── tsconfig.json            # TypeScript config
└── package.json

## Pages

### Landing (/)
- Hero section with feature highlights
- Swiss design system

### Dashboard (/dashboard)
- Master resume card + tailored resume tiles
- States: loading | pending | processing | ready | failed
- Auto-refreshes on window focus
- localStorage: master_resume_id

### Builder (/builder)
- Left: Editor Panel (forms + formatting controls)
- Right: WYSIWYG PaginatedPreview
- Tabs: Resume | Cover Letter | Outreach
- Auto-saves to localStorage

### Tailor (/tailor)
- Job description textarea
- Calls: POST /jobs/upload -> POST /resumes/improve
- Redirects to /resumes/[new_id]

### Settings (/settings)
- Provider selection (6 providers)
- API key input
- System status (cached, 30-min refresh)

### Print Routes (/print/resumes/[id], /print/cover-letter/[id])
- Headless Chrome renders these for PDF
- Query params: template, pageSize, margins, spacing

## UI Components

### Button Variants
- default (blue #1D4ED8)
- destructive (red)
- success (green)
- warning (orange)
- outline
- secondary

### Styling
- rounded-none (square corners)
- Hard shadows (shadow-sw-xs through shadow-sw-xl)
- font-mono for labels
- 1px black borders (border border-black)

## Context Providers

### StatusCacheProvider
- Caches system status, 30-min auto-refresh
- Optimistic counter updates on user actions

### LanguageProvider
- Content generation language (en, es, zh, ja, pt)
- UI language (separate setting)

## API Client (lib/api/)

### client.ts Exports
- API_URL, API_BASE
- apiFetch, apiPost, apiPatch, apiPut, apiDelete
- getUploadUrl()

### resume.ts
- uploadJobDescriptions, improveResume, fetchResume, fetchResumeList
- updateResume, downloadResumePdf, deleteResume

### config.ts
- fetchLlmConfig, updateLlmConfig, testLlmConnection, fetchSystemStatus
- fetchFeatureFlags, updateFeatureFlags
- fetchContentLanguage, updateContentLanguage
- fetchPromptOptions, updateDefaultPrompt
- updateFeaturePrompts, resetDatabase

### tracker.ts
- listApplications, createApplication, updateApplication
- bulkUpdateStatus, deleteApplication, bulkDeleteApplications

### enrichment.ts
- analyzeResume, enhanceResume, applyEnhancements
- regenerateEnrichment, applyRegenerated

## localStorage Keys

| Key | Purpose |
|-----|---------|
| master_resume_id | Master resume UUID |
| resume_builder_draft | Auto-saved form data |
| resume_builder_settings | Template preferences |
| contentLanguage | Content generation language |
| uiLanguage | UI display language |

## i18n System

### Two Settings
- UI Language: Interface text (client-only, localStorage)
- Content Language: LLM output language (persisted to backend)

### Supported Locales
- en (English - source)
- es (Spanish)
- zh (Chinese)
- ja (Japanese)
- pt (Portuguese - pt-BR.json)

### Engine
- No external i18n lib
- Static imports in messages.ts
- Dot-notation lookup (t(a.b.c))
- Locale parity guard (build breaks if structure differs)

## Key Patterns

1. Backend Access: Always via lib/api/* (never raw fetch)
2. 240s Timeout: Matches backend (NEXT_PUBLIC_REQUEST_TIMEOUT_MS)
3. Print Pages: Server components (no use client)
4. Enter Key: Add e.stopPropagation() in textarea forms
5. HTML Sanitization: Use sanitizeHtml() before dangerouslySetInnerHTML
