"""LLM prompt templates for resume processing."""

# Language code to full name mapping
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "zh": "Chinese (Simplified)",
    "ja": "Japanese",
    "pt": "Brazilian Portuguese",
}


def get_language_name(code: str) -> str:
    """Get full language name from code."""
    return LANGUAGE_NAMES.get(code, "English")


# Schema with example values - used for prompts to show LLM expected format
RESUME_SCHEMA_EXAMPLE = """{
  "personalInfo": {
    "name": "John Doe",
    "title": "Software Engineer",
    "email": "john@example.com",
    "phone": "+1-555-0100",
    "location": "San Francisco, CA",
    "website": "https://johndoe.dev",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe"
  },
  "summary": "Experienced software engineer with 5+ years...",
  "workExperience": [
    {
      "id": 1,
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "years": "Jan 2020 - Present",
      "description": [
        "Led development of microservices architecture",
        "Improved system performance by 40%"
      ]
    }
  ],
  "education": [
    {
      "id": 1,
      "institution": "University of California",
      "degree": "B.S. Computer Science",
      "years": "2014 - 2018",
      "description": "Graduated with honors"
    }
  ],
  "personalProjects": [
    {
      "id": 1,
      "name": "Open Source Tool",
      "role": "Creator & Maintainer",
      "years": "Mar 2021 - Present",
      "description": [
        "Built CLI tool with 1000+ GitHub stars",
        "Used by 50+ companies worldwide"
      ]
    }
  ],
  "additional": {
    "technicalSkills": ["Python", "JavaScript", "AWS", "Docker"],
    "languages": ["English (Native)", "Spanish (Conversational)"],
    "certificationsTraining": ["AWS Solutions Architect"],
    "awards": ["Employee of the Year 2022"]
  },
  "customSections": {
    "publications": {
      "sectionType": "itemList",
      "items": [
        {
          "id": 1,
          "title": "Paper Title",
          "subtitle": "Journal Name",
          "years": "Jun 2023",
          "description": ["Brief description of the publication"]
        }
      ]
    },
    "volunteer_work": {
      "sectionType": "text",
      "text": "Description of volunteer activities..."
    }
  }
}"""

# Schema for improve prompts - excludes personalInfo (preserved from original)
IMPROVE_SCHEMA_EXAMPLE = """{
  "summary": "Experienced software engineer with 5+ years...",
  "workExperience": [
    {
      "id": 1,
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "years": "Jan 2020 - Present",
      "description": [
        "Led development of microservices architecture",
        "Improved system performance by 40%"
      ]
    }
  ],
  "education": [
    {
      "id": 1,
      "institution": "University of California",
      "degree": "B.S. Computer Science",
      "years": "2014 - 2018",
      "description": "Graduated with honors"
    }
  ],
  "personalProjects": [
    {
      "id": 1,
      "name": "Open Source Tool",
      "role": "Creator & Maintainer",
      "years": "Mar 2021 - Present",
      "description": [
        "Built CLI tool with 1000+ GitHub stars",
        "Used by 50+ companies worldwide"
      ]
    }
  ],
  "additional": {
    "technicalSkills": ["Python", "JavaScript", "AWS", "Docker"],
    "languages": ["English (Native)", "Spanish (Conversational)"],
    "certificationsTraining": ["AWS Solutions Architect"],
    "awards": ["Employee of the Year 2022"]
  },
  "customSections": {
    "publications": {
      "sectionType": "itemList",
      "items": [
        {
          "id": 1,
          "title": "Paper Title",
          "subtitle": "Journal Name",
          "years": "Jun 2023",
          "description": ["Brief description of the publication"]
        }
      ]
    },
    "volunteer_work": {
      "sectionType": "text",
      "text": "Description of volunteer activities..."
    }
  }
}"""

PARSE_RESUME_PROMPT = """Parse this resume into JSON. Output ONLY the JSON object, no other text.

Map content to standard sections when possible. For non-standard sections (like Publications, Volunteer Work, Research, Hobbies), add them to customSections with an appropriate type.

Example output format:
{schema}

Custom section types:
- "text": Single text block (e.g., objective, statement)
- "itemList": List of items with title, subtitle, years, description (e.g., publications, research)
- "stringList": Simple list of strings (e.g., hobbies, interests)

Rules:
- Use "" for missing text fields, [] for missing arrays, null for optional fields
- Number IDs starting from 1
- Format dates preserving the original precision. Keep months when present: "Jan 2020 - Dec 2023", "May 2021 - Present". Use "YYYY - YYYY" only when the source has no months.
- Use snake_case for custom section keys (e.g., "volunteer_work", "publications")
- Preserve the original section name as a descriptive key
- Normalize date separators: "2020-2021" -> "2020 - 2021", "Current"/"Ongoing" -> "Present". Do NOT discard months.
- For ambiguous dates like "3 years experience", infer approximate years from context or use "~YYYY"
- Flag overlapping dates (concurrent roles) by preserving both, don't merge

Resume to parse:
{resume_text}"""

EXTRACT_KEYWORDS_PROMPT = """Extract job requirements as JSON. Output ONLY a valid JSON object, no other text, no markdown.

Example format:
{{
  "company": "Acme Corp",
  "role": "Senior Backend Engineer",
  "required_skills": ["Python", "AWS", "PostgreSQL", "Docker", "Kubernetes"],
  "preferred_skills": ["Kafka", "Redis", "Terraform", "GraphQL"],
  "action_verbs": ["design", "build", "optimize", "scale", "architect", "lead", "mentor", "implement", "deploy", "monitor"],
  "experience_requirements": ["5+ years backend development", "3+ years cloud infrastructure"],
  "education_requirements": ["Bachelor's in CS or equivalent"],
  "key_responsibilities": ["Design scalable APIs", "Optimize database performance", "Lead code reviews", "Mentor junior engineers"],
  "keywords": ["microservices", "distributed systems", "CI/CD", "observability", "system design", "REST", "gRPC", "event-driven architecture"],
  "experience_years": 5,
  "seniority_level": "senior",
  "tech_stack_clusters": {{
    "languages": ["Python", "Go"],
    "cloud": ["AWS", "GCP"],
    "databases": ["PostgreSQL", "Redis"],
    "infrastructure": ["Docker", "Kubernetes", "Terraform"],
    "messaging": ["Kafka", "RabbitMQ"]
  }},
  "must_have_phrases": ["microservices architecture", "RESTful APIs", "distributed systems", "CI/CD pipelines", "system design"]
}}

Extract numeric years (e.g., "5+ years" -> 5) and infer seniority level.
Set "company" to the hiring company name and "role" to the job title exactly as written; use empty string if not stated.

CRITICAL FOR ATS MATCHING:
- Extract EXACT phrases from the JD, not paraphrases
- Include multi-word phrases: "microservices architecture", "RESTful APIs", "CI/CD pipelines"
- Capture ALL acronyms with their full forms: "AWS (Amazon Web Services)", "CI/CD (Continuous Integration/Continuous Deployment)"
- Group skills by category as shown in tech_stack_clusters
- Identify "must_have_phrases" — exact phrases that appear in JD requirements and MUST appear in resume for ATS

Job description:
{job_description}"""

CRITICAL_TRUTHFULNESS_RULES_TEMPLATE = """CRITICAL TRUTHFULNESS RULES - NEVER VIOLATE:
1. DO NOT invent numeric achievements (e.g., "increased by 30%") unless they exist in original
2. DO NOT add company names not in the original
3. DO NOT upgrade experience level (e.g., "Junior" -> "Senior")
4. DO NOT extend employment dates or change timelines. Copy date ranges exactly as they appear, including months.
5. {rule_7}
6. NEVER remove existing skills, certifications, languages, or awards. You may reorder by relevance, but every original item must remain.

Violation of these rules could cause serious problems for the candidate in job interviews.
"""


def _build_truthfulness_rules(rule_7: str) -> str:
    return CRITICAL_TRUTHFULNESS_RULES_TEMPLATE.format(rule_7=rule_7)


CRITICAL_TRUTHFULNESS_RULES = {
    "nudge": _build_truthfulness_rules(
        "DO NOT add new bullet points or content - only rephrase existing content"
    ),
    "keywords": _build_truthfulness_rules(
        "You may rephrase existing bullet points to include keywords, but do NOT add new bullet points"
    ),
    "full": _build_truthfulness_rules(
        "You may expand existing bullet points or add new ones that elaborate on existing work, but DO NOT invent entirely new responsibilities"
    ),
    "ats": _build_truthfulness_rules(
        "DO NOT add skills/tools/certifications the candidate has NEVER used. DO NOT invent metrics or achievements. Preserve ALL existing skills, certifications, languages, awards. Copy dates EXACTLY as they appear."
    ),
}

RESUME_WRITING_GUIDELINES = """Act as an expert human writer and editor. Your goal is to rewrite the text provided below so that it completely bypasses AI content detectors (like GPTZero, Winston AI, and Turnitin) by eliminating predictable patterns.

To achieve a 100% human score, you must strictly follow these structural and stylistic rules:

1. Maximize Perplexity and Burstiness: Humans naturally write with varying sentence lengths. Mix very short sentences (3–5 words) with medium and long, complex sentences. Never use the same sentence structure twice in a row.
2. Ban AI Buzzwords: Absolutely do not use common AI tells, fillers, or transition words. Ban these words entirely: delve, tapestry, robust, testament, foster, landscape, revolutionize, navigate, paradigm shift, furthermore, moreover, key takeaway, crucial, ultimately, in today's world, it is important to note, overall, in conclusion.
3. Lower the Vocabulary Predictability: AI selects the most statistically probable next word. Force yourself to use less predictable, more colorful, or casual synonyms that a human would naturally use in conversation.
4. Adopt a Grounded Voice: Write with calm, confident authority. Do not sound overly enthusiastic, cheerful, or marketing-heavy. Avoid exclamation points.
5. Introduce Imperfections and True Flow: Humans do not write in perfect, rigid blocks. Use natural, casual transitions (like "But here's the thing," "So," "Frankly"). You may occasionally use a fragment or a slightly informal phrasing to break mechanical perfection.
6. Format Cleanly: Do not use generic AI formatting like repetitive bullet points or identical paragraph lengths. Integrate ideas smoothly.

Output only the final text."""

IMPROVE_RESUME_PROMPT_NUDGE = """Lightly nudge this resume toward the job description. Output ONLY the JSON object, no other text.

{critical_truthfulness_rules}

IMPORTANT: Generate ALL text content (summary, descriptions, skills) in {output_language}.
Do NOT include personalInfo in your output - it will be preserved from the original resume.

Rules:
- Make minimal, conservative edits only where there is a clear existing match
- Do NOT change the candidate's role, industry, or seniority level
- Do NOT introduce new certifications not already present
- Preserve original bullet count and ordering within each section
- Keep proper nouns (names, company names, locations) unchanged
- For customSections: preserve exact structure, item count, titles, subtitles, and years. If an item's description is an empty array [] in the original, keep it empty []. Do NOT generate descriptions for items that had none.
- Copy the "years" field values EXACTLY as they appear in the original resume (including any month prefixes like "Jan 2020 - Present"). Do not shorten, reformat, or drop months.
- If the resume is non-technical, do NOT add technical jargon
- Do NOT use em dash ("—") anywhere in the writing/output, even if it exists, remove it

Job Description:
{job_description}

Keywords to emphasize (only if already supported by resume content):
{job_keywords}

Original Resume:
{original_resume}

Output in this JSON format:
{schema}"""

IMPROVE_RESUME_PROMPT_KEYWORDS = """Enhance this resume with relevant keywords from the job description. Output ONLY the JSON object, no other text.

{critical_truthfulness_rules}

IMPORTANT: Generate ALL text content (summary, descriptions, skills) in {output_language}.
Do NOT include personalInfo in your output - it will be preserved from the original resume.

Rules:
- Strengthen alignment by weaving in relevant keywords where evidence already exists
- You may rephrase bullet points to include keyword phrasing
- Do NOT introduce new certifications not in the resume
- Do NOT change role, industry, or seniority level
- For customSections: preserve exact structure, item count, titles, subtitles, and years. If an item's description is an empty array [] in the original, keep it empty []. Do NOT generate descriptions for items that had none.
- Copy the "years" field values EXACTLY as they appear in the original resume (including any month prefixes like "Jan 2020 - Present"). Do not shorten, reformat, or drop months.
- If resume is non-technical, keep language non-technical while still aligning keywords
- Do NOT use em dash ("—") anywhere in the writing/output, even if it exists, remove it

Job Description:
{job_description}

Keywords to emphasize:
{job_keywords}

Original Resume:
{original_resume}

Output in this JSON format:
{schema}"""

IMPROVE_RESUME_PROMPT_FULL = """Tailor this resume for the job. Output ONLY the JSON object, no other text.

{critical_truthfulness_rules}

IMPORTANT: Generate ALL text content (summary, descriptions, skills) in {output_language}.
Do NOT include personalInfo in your output - it will be preserved from the original resume.

Rules:
- Make targeted adjustments to bullet points to align with job description phrasing. Preserve the candidate's original details and voice - adjust wording, do not rewrite entirely.
- Preserve existing action verbs. Do not invent quantifiable achievements not in the original.
- Keep proper nouns (names, company names, locations) unchanged
- Translate job titles, descriptions, and skills to {output_language}
- For customSections: preserve exact structure, item count, titles, subtitles, and years. If an item's description is an empty array [] in the original, keep it empty []. Do NOT generate descriptions for items that had none.
- Improve custom section content the same way as standard sections
- Copy the "years" field values EXACTLY as they appear in the original resume (including any month prefixes like "Jan 2020 - Present"). Do not shorten, reformat, or drop months.
- Calculate and emphasize total relevant experience duration when it matches requirements
- Do NOT use em dash ("—") anywhere in the writing/output, even if it exists, remove it

Job Description:
{job_description}

Keywords to emphasize:
{job_keywords}

Original Resume:
{original_resume}

Output in this JSON format:
{schema}"""


IMPROVE_RESUME_PROMPT_ATS = """MAXIMIZE ATS MATCH: Tailor this resume to score highest on ATS scans for this job description. Output ONLY the JSON object, no other text.

CRITICAL ATS OPTIMIZATION RULES:
1. MATCH EXACT JD TERMS: Use the EXACT phrases, terminology, and acronyms from the job description (e.g., if JD says "ETL pipelines", use "ETL pipelines" not "data pipelines")
2. SKILL MIRRORING: Every skill mentioned in the JD's "required_skills" or "preferred_skills" MUST appear in the resume's technicalSkills section (reorder to prioritize JD skills first)
3. BULLET POINT OPTIMIZATION: Each bullet should contain 2-3 JD keywords naturally integrated
4. SECTION HEADER ALIGNMENT: Use JD section terminology (e.g., if JD says "DevOps", use "DevOps" not "Infrastructure")
5. ACRONYM FIRST: When JD uses acronyms (AWS, SQL, REST), mention full term FIRST then acronym in parentheses: "Amazon Web Services (AWS)"
6. VERB MATCHING: Use JD's action verbs (e.g., if JD says "spearhead", use "spearhead" not "lead")
7. SKILL CATEGORY ALIGNMENT: If JD groups skills (e.g., "Cloud Platforms: AWS, Azure, GCP"), mirror that grouping structure
8. EXPERIENCE LEVEL MATCH: If JD specifies "senior-level", "mid-level", "entry-level", reflect this in summary and experience descriptions
9. CERTIFICATION PLACEMENT: Move relevant certifications to top of certifications list if JD emphasizes them
10. MEASUREMENT LANGUAGE: If JD uses specific metrics (e.g., "scale to 1M users"), use similar metric language even if different numbers

TRUTHFULNESS (NON-NEGOTIABLE):
- DO NOT add certifications the candidate has NEVER used
- DO NOT add company names or products not in original resume
- Preserve ALL existing skills, certifications, languages, awards
- Copy dates EXACTLY as they appear (including months)

IMPORTANT: Generate ALL text content (summary, descriptions, skills) in {output_language}.

Job Description:
{job_description}

Extracted JD Keywords:
{job_keywords}

Original Resume:
{original_resume}

Output in this JSON format:
{schema}"""

IMPROVE_PROMPT_OPTIONS = [
    {
        "id": "nudge",
        "label": "Light nudge",
        "description": "Minimal edits to better align existing experience.",
    },
    {
        "id": "keywords",
        "label": "Keyword enhance",
        "description": "Blend in relevant keywords without changing role or scope.",
    },
    {
        "id": "full",
        "label": "Full tailor",
        "description": "Comprehensive tailoring using the job description.",
    },
    {
        "id": "ats",
        "label": "ATS-optimized",
        "description": "Maximize ATS scan score with exact JD terminology matching.",
    },
]

IMPROVE_RESUME_PROMPTS = {
    "nudge": IMPROVE_RESUME_PROMPT_NUDGE,
    "keywords": IMPROVE_RESUME_PROMPT_KEYWORDS,
    "full": IMPROVE_RESUME_PROMPT_FULL,
    "ats": IMPROVE_RESUME_PROMPT_ATS,
}

DEFAULT_IMPROVE_PROMPT_ID = "keywords"

# Backward-compatible alias
IMPROVE_RESUME_PROMPT = IMPROVE_RESUME_PROMPT_FULL

COVER_LETTER_PROMPT = """Write a brief cover letter for this job application.

IMPORTANT: Write in {output_language}.

Job Description:
{job_description}

Candidate Resume (JSON):
{resume_data}

Requirements:
- 100-150 words maximum
- 3-4 short paragraphs
- Opening: Reference ONE specific thing from the job description (product, tech stack, or problem they're solving) - not generic excitement about "the role"
- Middle: Pick 1-2 qualifications from resume that DIRECTLY match stated requirements, and reframe them in the job's language/terminology where the candidate's proven experience supports it (e.g., if the resume shows "built automated data pipelines" and the job says "ETL," describe that real work as ETL) - prioritize relevance over impressiveness
- Closing: Simple availability to discuss, no desperate enthusiasm
- If resume shows career transition, frame the pivot as intentional and relevant
- Extract company name from job description - do not use placeholders
- Do NOT invent information not in the resume
- Tone: Confident peer, not eager applicant
- Do NOT use em dash ("—") anywhere in the writing/output, even if it exists, remove it

Output plain text only. No JSON, no markdown formatting."""

OUTREACH_MESSAGE_PROMPT = """Generate a cold outreach message for LinkedIn or email about this job opportunity.

IMPORTANT: Write in {output_language}.

Job Description:
{job_description}

Candidate Resume (JSON):
{resume_data}

Guidelines:
- 70-100 words maximum (shorter than a cover letter)
- First sentence: Reference specific detail from job description (team, product, technical challenge) - never open with "I'm reaching out" or "I saw your posting"
- One sentence on strongest matching qualification with a concrete metric if available
- End with low-friction ask: "Worth a quick chat?" not "I'd love the opportunity to discuss"
- Tone: How you'd message a former colleague, not a stranger
- Do NOT include placeholder brackets
- Do NOT use phrases like "excited about" or "passionate about"
- Do NOT use em dash ("—") anywhere in the writing/output, even if it exists, remove it

Output plain text only. No JSON, no markdown formatting."""

GENERATE_TITLE_PROMPT = """Extract the job title and company name from this job description.

IMPORTANT: Write in {output_language}.

Job Description:
{job_description}

Rules:
- Format: "Role @ Company" (e.g., "Senior Frontend Engineer @ Stripe")
- If the company name is not found, return just the role (e.g., "Senior Frontend Engineer")
- Maximum 60 characters
- Use the most specific role title mentioned
- Do not add any other text, quotes, or formatting

Output the title only, nothing else."""

# Alias for backward compatibility
RESUME_SCHEMA = RESUME_SCHEMA_EXAMPLE

# Diff-based improvement: outputs targeted changes instead of full resume

DIFF_STRATEGY_INSTRUCTIONS = {
    "nudge": "Make minimal edits. Only rephrase where there is a clear match. Do not add new bullet points.",
    "keywords": "Weave in relevant keywords where evidence already exists. You may rephrase bullets but do not add new ones.",
    "full": "Make targeted adjustments. You may rephrase bullets, add verified JD skills, and add new bullets that elaborate on existing work, but do not invent new responsibilities.",
    "ats": "MAXIMIZE ATS SCORE: Use EXACT JD terminology. Mirror JD skill categories. Place JD-emphasized skills first. Use JD action verbs. Mention full terms then acronyms (e.g., 'Amazon Web Services (AWS)'). Every JD required skill MUST appear in technicalSkills. Do not invent new content.",
}

SKILL_TARGET_PLAN_PROMPT = """Build a concise skill target plan for tailoring this resume to the job. Focus on MAXIMUM ATS match.

Return ONLY a JSON object. Do not rewrite the resume.

RULES:
1. Prioritize JD required_skills first (these MUST appear for ATS pass)
2. Then JD preferred_skills (high value for ranking)
3. Include existing resume skills that match JD keywords/phrases exactly
4. Include JD tech_stack_clusters skills by category
5. Include must_have_phrases from JD
6. Do NOT include skills unrelated to the JD
7. Do NOT include certifications (handled separately)
8. Generate reasons in {output_language}

Existing resume skills:
{existing_skills}

JD keywords and skills:
{job_keywords}

Job Description:
{job_description}

Resume JSON:
{original_resume}

Output this exact JSON format:
{{
  "target_skills": [
    {{
      "skill": "exact skill/phrase from JD",
      "reason": "required by JD / preferred by JD / matches existing experience / appears in JD tech stack cluster",
      "source": "required|preferred|cluster|phrase|existing",
      "category": "languages|cloud|databases|infrastructure|messaging|frameworks|tools|other"
    }}
  ],
  "strategy_notes": "brief notes for the next editing pass: which JD categories to mirror, which phrases must appear in technicalSkills, which action verbs to adopt"
}}"""

SKILL_CLASSIFICATION_PROMPT = """Classify the technical skills into appropriate sub-categories for a professional resume.

Rules:
1. Every skill must end up in exactly one category - no drops, no duplicates.
2. Use conventional, resume-appropriate category names (e.g., Programming Languages, Cloud & DevOps, Databases, Frameworks, Tools, Testing).
3. Anything that doesn't cleanly fit goes into a catch-all "Additional Skills".
4. For small skill lists (<=4 skills), use a single category or keep flat.
5. Output ONLY valid JSON - no prose, no explanations.

Example output:
{{
  "categories": [
    {{"name": "Programming Languages", "skills": ["Python", "TypeScript", "JavaScript"]}},
    {{"name": "Cloud & DevOps", "skills": ["AWS", "Docker", "Kubernetes", "CI/CD"]}},
    {{"name": "Databases", "skills": ["PostgreSQL", "MongoDB", "Redis"]}}
  ]
}}

Skills to classify:
{skills_list}

Output JSON only:"""

DIFF_IMPROVE_PROMPT = """Given this resume and job description, output a JSON object with targeted changes to MAXIMIZE ATS MATCH SCORE.

RULES:
1. Only modify content; never change names, companies, dates, institutions, or degrees
2. Do not add new work entries, education entries, or project entries
3. {strategy_instruction}
4. Each change MUST include the original text (copied exactly) so it can be verified
5. For each change, explain WHY it helps match the job description
6. Generate all new text in {output_language}
7. Do not use em dash characters
8. Keep changes minimal and targeted; do not rewrite content that already aligns well
9. By DEFAULT, scan the summary and every work, project, and education description for content that already demonstrates a job-description keyword or skill, and reframe that text using the job description's EXACT terminology where it is not already phrased that way (per rule 9, leave content that already aligns well), while preserving the candidate's actual accomplishment. Do NOT add new work, metrics, or responsibilities; only restate existing content in the JD's EXACT language, and verify every reframe stays factually accurate.
10. Preserve original capitalization, especially for proper nouns, technical terms (e.g., REST, API, AWS), and acronyms. Do not change the casing of words that were capitalized in the original.

ATS OPTIMIZATION RULES (apply to ALL changes):
- EXACT PHRASE MATCHING: Use JD's exact multi-word phrases (e.g., "microservices architecture", "CI/CD pipelines", "RESTful APIs") -- not synonyms
- ACRONYM + FULL FORM: When JD uses acronyms, include BOTH: "Amazon Web Services (AWS)", "Continuous Integration/Continuous Deployment (CI/CD)"
- SKILL CATEGORY MIRRORING: Mirror JD's tech_stack_clusters structure in technicalSkills ordering
- ACTION VERB ADOPTION: Use JD's action_verbs verbatim in bullet points
- MUST-HAVE PHRASES: Every must_have_phrase from JD MUST appear in resume (summary, bullets, or skills)
- REQUIRED SKILLS COVERAGE: Every required_skill MUST appear in technicalSkills (reorder to top)
- KEYWORD DENSITY: Target 2-3 JD keywords per bullet point naturally integrated
- PRESERVE EXISTING SENIORITY: Do NOT add seniority terms (senior, lead, principal, junior, entry-level) unless they already exist in the original resume summary. Match the candidate's actual experience level.

PATHS you can target:
- "summary" -- the resume summary text
- "workExperience[i].description[j]" -- a specific bullet (i = entry index, j = bullet index)
- "workExperience[i].description" -- append a new bullet (action: "append")
- "personalProjects[i].description[j]" -- a specific project bullet
- "personalProjects[i].description" -- append a new project bullet (action: "append")
- "education[i].description" -- the education entry's description text (replace only; it is a single string, not a list)
- "additional.technicalSkills" -- reorder the skills list (action: "reorder") or add one verified skill (action: "add_skill")
- "additional.languages" -- reorder the languages list (action: "reorder")
- "additional.certificationsTraining" -- reorder the certifications list (action: "reorder")
- "additional.awards" -- reorder the awards list (action: "reorder")

Do NOT target: personalInfo, dates/years, company names, education degree/institution/years, customSections.

Keywords to emphasize (only if already supported by resume content):
{job_keywords}

Verified skill targets:
{skill_targets}

Job Description:
{job_description}

Original Resume:
{original_resume}

Output this exact JSON format, nothing else:
{{
  "changes": [
    {{
      "path": "workExperience[0].description[1]",
      "action": "replace",
      "original": "the exact original text at this path",
      "value": "the improved text with EXACT JD phrases, acronyms+full forms, action verbs",
      "reason": "why this change helps ATS match: exact phrase X, action verb Y, skill Z"
    }},
    {{
      "path": "summary",
      "action": "replace",
      "original": "the current summary text",
      "value": "the improved summary with JD must-have phrases, key skills",
      "reason": "why this change helps ATS match"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "reorder",
      "original": null,
      "value": ["JD required skill 1", "JD required skill 2", "JD preferred skill 1", "existing relevant skill", "..."],
      "reason": "reordered to prioritize ALL JD required skills first, then preferred, then existing -- mirrors JD tech_stack_clusters"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "add_skill",
      "original": null,
      "value": "verified JD required skill missing from the skills list",
      "reason": "added JD required skill for ATS coverage -- verified via skill target plan"
    }}
  ],
  "strategy_notes": "ATS strategy: which JD categories mirrored, which must-have phrases placed where, which action verbs adopted, technicalSkills ordering rationale"
}}"""

# ============================================
# DEDICATED ATS-MAXIMIZING DIFF PROMPT (for 'ats' strategy)
# ============================================

DIFF_IMPROVE_PROMPT_ATS = """Given this resume and job description, output a JSON object with MAXIMUM ATS-optimized changes. This prompt prioritizes ATS scan score above all else while maintaining truthfulness.

RULES:
1. Only modify content; never change names, companies, dates, institutions, or degrees
2. Do not add new work entries, education entries, or project entries
3. {strategy_instruction}
4. Each change MUST include the original text (copied exactly) so it can be verified
5. For each change, explain WHY it helps match the job description
6. Generate all new text in {output_language}
7. Do not use em dash characters
8. AGGRESSIVE ATS OPTIMIZATION -- this is the PRIMARY goal

ATS MAXIMIZATION RULES (MANDATORY):
- EXACT TERM MATCHING: Use JD's EXACT phrasing. If JD: "build CI/CD pipelines" -> resume: "build CI/CD pipelines" (not "create deployment pipelines")
- ACRONYM FIRST MENTION: "Amazon Web Services (AWS)", "Kubernetes (K8s)", "Continuous Integration/Continuous Deployment (CI/CD)"
- EVERY REQUIRED SKILL IN technicalSkills: All JD required_skills + preferred_skills MUST appear in technicalSkills, ordered by JD priority
- VERB MIRRORING: Mirror JD action verbs exactly -- "spearhead"->"spearhead", "architect"->"architect", "optimize"->"optimize"
- KEYWORD DENSITY: Each bullet MUST contain 2-3 JD keywords/phrases naturally
- SECTION HEADER ALIGNMENT: If JD mentions "DevOps Engineering", rename/rephrase to match
- METRIC STYLE MATCHING: If JD says "reduced latency by 40%", use "% improvement" language
- SKILL CATEGORY MIRRORING: If JD groups "Cloud: AWS, GCP, Azure", ensure technicalSkills reflects similar grouping
- NO FABRICATION: Only reframe existing content; never invent metrics, tools, or responsibilities

PATHS you can target (PRIORITY ORDER):
1. "summary" -- MUST include top 5 JD keywords
2. "additional.technicalSkills" -- reorder + add_skill for EVERY missing JD required/preferred skill
3. "workExperience[i].description[j]" -- reframe EVERY bullet to include JD terminology
4. "personalProjects[i].description[j]" -- same aggressive reframe
5. "education[i].description" -- add relevant coursework/keywords if applicable

Do NOT target: personalInfo, dates/years, company names, education degree/institution/years, customSections.

JD Required Skills (MUST appear in technicalSkills):
{job_keywords}

Verified skill targets (pre-approved for add_skill):
{skill_targets}

Job Description:
{job_description}

Original Resume:
{original_resume}

Output this exact JSON format, nothing else:
{{
  "changes": [
    {{
      "path": "summary",
      "action": "replace",
      "original": "the current summary text",
      "value": "ATS-optimized summary with top 5 JD keywords and exact JD phrasing",
      "reason": "summary is the highest-weight ATS field; must contain exact JD terminology"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "reorder",
      "original": null,
      "value": ["JD required skill 1", "JD required skill 2", "JD preferred skill 1", "existing relevant skill 1", "..."],
      "reason": "technicalSkills is primary ATS keyword field; ordered by JD priority"
    }},
    {{
      "path": "additional.technicalSkills",
      "action": "add_skill",
      "original": null,
      "value": "missing JD required skill",
      "reason": "every JD required skill must appear for ATS match"
    }},
    {{
      "path": "workExperience[0].description[0]",
      "action": "replace",
      "original": "original bullet text",
      "value": "reframed bullet with 2-3 exact JD keywords, JD verbs, acronym expansion",
      "reason": "each bullet must contain JD terminology for keyword density"
    }}
  ],
  "strategy_notes": "ATS-maximizing strategy: exact term matching, acronym expansion, skill mirroring, verb mirroring, keyword density 2-3 per bullet"
}}"""