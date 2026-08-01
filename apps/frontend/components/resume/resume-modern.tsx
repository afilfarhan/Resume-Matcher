import React from 'react';
import { Mail, Phone, MapPin, Globe, Linkedin, Github, ExternalLink } from 'lucide-react';
import type {
  ResumeData,
  SectionMeta,
  AdditionalSectionLabels,
} from '@/components/dashboard/resume-component';
import { getSortedSections } from '@/lib/utils/section-helpers';
import { formatDateRange } from '@/lib/utils';
import { SafeHtml } from './safe-html';
import baseStyles from './styles/_base.module.css';
import styles from './styles/modern.module.css';

interface ResumeModernProps {
  data: ResumeData;
  showContactIcons?: boolean;
  showHyperlinks?: boolean;
  personalInfoLayout?: 'single-line' | 'two-line' | 'stacked';
  additionalSectionLabels?: Partial<AdditionalSectionLabels>;
}

/**
 * Modern Resume Template
 *
 * Single-column layout with user-selectable accent colors.
 * Features colored section headers with underline and decorative name underline.
 * ATS-compatible: all visual elements are real DOM text nodes.
 *
 * Section order: Determined by sectionMeta ordering
 */
export const ResumeModern: React.FC<ResumeModernProps> = ({
  data,
  showContactIcons = false,
  showHyperlinks = false,
  personalInfoLayout = 'single-line',
  additionalSectionLabels,
}) => {
  const { personalInfo, summary, workExperience, education, personalProjects, additional } = data;

  // Get sorted visible sections
  const sortedSections = getSortedSections(data);

  // Icon mapping for contact types
  const contactIcons: Record<string, React.ReactNode> = {
    Email: <Mail size={12} />,
    Phone: <Phone size={12} />,
    Location: <MapPin size={12} />,
    Website: <Globe size={12} />,
    LinkedIn: <Linkedin size={12} />,
    GitHub: <Github size={12} />,
  };

  // Helper function to render contact details
  const renderContactDetail = (label: string, value?: string, hrefPrefix: string = '') => {
    if (!value) return null;

    let finalHrefPrefix = hrefPrefix;
    if (
      ['Website', 'LinkedIn', 'GitHub'].includes(label) &&
      !value.startsWith('http') &&
      !value.startsWith('//')
    ) {
      finalHrefPrefix = 'https://';
    }

    const href = finalHrefPrefix + value;
    const isLink =
      finalHrefPrefix.startsWith('http') ||
      value.startsWith('http') ||
      finalHrefPrefix.startsWith('mailto:') ||
      finalHrefPrefix.startsWith('tel:');

    let displayText = value;
    if (isLink && (label === 'LinkedIn' || label === 'GitHub' || label === 'Website')) {
      if (label === 'Website') {
        displayText = 'portfolio';
      } else if (label === 'GitHub') {
        displayText = 'github';
      } else {
        displayText = value.replace(/^https?:\/\//, '').replace(/^www\./, '');
      }
    }

    return (
      <span className="inline-flex items-center gap-1">
        {showContactIcons && contactIcons[label]}
        {isLink && showHyperlinks ? (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className={`${baseStyles['resume-link']} hover:underline`}
          >
            {displayText}
          </a>
        ) : (
          <span style={{ color: 'var(--resume-text-primary)' }}>{displayText}</span>
        )}
      </span>
    );
  };

  // Render contact info based on layout
  const renderContactInfo = () => {
    if (!personalInfo) return null;

    const contacts = [
      { key: 'email', render: () => renderContactDetail('Email', personalInfo.email, 'mailto:') },
      {
        key: 'phone',
        render: () =>
          personalInfo.phone && renderContactDetail('Phone', personalInfo.phone, 'tel:'),
      },
      {
        key: 'info',
        render: () =>
          personalInfo.info && (
            <span style={{ color: 'var(--resume-text-primary)' }}>{personalInfo.info}</span>
          ),
      },
      {
        key: 'location',
        render: () =>
          personalInfo.location && renderContactDetail('Location', personalInfo.location),
      },
      {
        key: 'website',
        render: () => personalInfo.website && renderContactDetail('Website', personalInfo.website),
      },
      {
        key: 'linkedin',
        render: () =>
          personalInfo.linkedin && renderContactDetail('LinkedIn', personalInfo.linkedin),
      },
      {
        key: 'github',
        render: () => personalInfo.github && renderContactDetail('GitHub', personalInfo.github),
      },
    ].filter((c) => c.render());

    // Separator for inline layouts
    const separator = <span className={baseStyles['text-muted']} aria-hidden="true"> | </span>;

    if (personalInfoLayout === 'stacked') {
      return (
        <div className={`flex flex-col items-center gap-1 ${baseStyles['resume-meta']}`}>
          {contacts.map((c, i) => (
            <span key={c.key} className="w-full text-center">
              {c.render()}
            </span>
          ))}
        </div>
      );
    }

    if (personalInfoLayout === 'two-line') {
      // Split into two lines: first line has email, phone, info; second line has location, website, linkedin, github
      const firstLine = contacts.filter((c) => ['email', 'phone', 'info'].includes(c.key));
      const secondLine = contacts.filter((c) =>
        ['location', 'website', 'linkedin', 'github'].includes(c.key)
      );

      return (
        <div className={`flex flex-col items-center gap-1 ${baseStyles['resume-meta']}`}>
          <div className={`flex flex-wrap justify-center gap-x-2 gap-y-1`}>
            {firstLine.map((c, i) => (
              <React.Fragment key={c.key}>
                {i > 0 && separator}
                {c.render()}
              </React.Fragment>
            ))}
          </div>
          {secondLine.length > 0 && (
            <div className={`flex flex-wrap justify-center gap-x-2 gap-y-1`}>
              {secondLine.map((c, i) => (
                <React.Fragment key={c.key}>
                  {i > 0 && separator}
                  {c.render()}
                </React.Fragment>
              ))}
            </div>
          )}
        </div>
      );
    }

    // single-line (default) - use pipe separators for better visual separation
    return (
      <div className={`flex flex-wrap justify-center gap-x-2 gap-y-1 ${baseStyles['resume-meta']}`}>
        {contacts.map((c, i) => (
          <React.Fragment key={c.key}>
            {i > 0 && separator}
            {c.render()}
          </React.Fragment>
        ))}
      </div>
    );
  };

  // Render a section based on its key
  const renderSection = (section: SectionMeta) => {
    switch (section.key) {
      case 'personalInfo':
        // Personal info is the header - handled separately
        return null;

      case 'summary':
        if (!summary) return null;
        return (
          <div key={section.id} className={baseStyles['resume-section']}>
            <h3 className={styles['section-title-accent']}>{section.displayName}</h3>
            <p className={styles['summary-text']}>{summary}</p>
          </div>
        );

      case 'workExperience':
        if (!workExperience || workExperience.length === 0) return null;
        return (
          <div key={section.id} className={baseStyles['resume-section']}>
            <h3 className={styles['section-title-accent']}>{section.displayName}</h3>
            <div className={baseStyles['resume-items']}>
              {workExperience.map((exp) => (
                <div key={exp.id} className={baseStyles['resume-item']}>
                  <div
                    className={`flex justify-between items-baseline ${baseStyles['resume-row-tight']}`}
                  >
                    <h4 className={baseStyles['resume-item-title']}>{exp.title}</h4>
                    <span className={`${baseStyles['resume-date']} ml-4`}>
                      {formatDateRange(exp.years)}
                    </span>
                  </div>
                  <div
                    className={`flex justify-between items-center ${baseStyles['resume-row']} ${baseStyles['resume-item-subtitle']}`}
                  >
                    <span>{exp.company}</span>
                    {exp.location && <span>{exp.location}</span>}
                  </div>
                  {exp.description && exp.description.length > 0 && (
                    <ul
                      className={`ml-4 ${baseStyles['resume-list']} ${baseStyles['resume-text-sm']}`}
                    >
                      {exp.description.map((desc, index) => (
                        <li key={index} className="flex">
                          <span className="mr-1.5 flex-shrink-0">•&nbsp;</span>
                          <span>
                            <SafeHtml html={desc} />
                          </span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </div>
        );

      case 'personalProjects':
        if (!personalProjects || personalProjects.length === 0) return null;
        return (
          <div key={section.id} className={baseStyles['resume-section']}>
            <h3 className={styles['section-title-accent']}>{section.displayName}</h3>
            <div className={baseStyles['resume-items']}>
              {personalProjects.map((project) => (
                <div key={project.id} className={baseStyles['resume-item']}>
                  <div
                    className={`flex justify-between items-baseline ${baseStyles['resume-row-tight']}`}
                  >
                    <div className="flex items-baseline gap-2">
                      <h4 className={baseStyles['resume-item-title']}>{project.name}</h4>
                      {(project.github || project.website) && (
                        <span className="flex gap-1.5">
                          {project.github && (
                            <a
                              href={
                                project.github.startsWith('http')
                                  ? project.github
                                  : `https://${project.github}`
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                              className={baseStyles['resume-link-pill']}
                            >
                              <Github size={10} />
                              {project.github
                                .replace(/^https?:\/\//, '')
                                .replace(/^www\./, '')
                                .replace(/\/$/, '')}
                            </a>
                          )}
                          {project.website && (
                            <a
                              href={
                                project.website.startsWith('http')
                                  ? project.website
                                  : `https://${project.website}`
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                              className={baseStyles['resume-link-pill']}
                            >
                              <ExternalLink size={10} />
                              {project.website
                                .replace(/^https?:\/\//, '')
                                .replace(/^www\./, '')
                                .replace(/\/$/, '')}
                            </a>
                          )}
                        </span>
                      )}
                    </div>
                    {project.years && (
                      <span className={`${baseStyles['resume-date']} ml-4`}>
                        {formatDateRange(project.years)}
                      </span>
                    )}
                  </div>
                  {project.role && (
                    <div
                      className={`${baseStyles['resume-row']} ${baseStyles['resume-item-subtitle']}`}
                    >
                      <span>{project.role}</span>
                    </div>
                  )}
                  {project.description && project.description.length > 0 && (
                    <ul
                      className={`ml-4 ${baseStyles['resume-list']} ${baseStyles['resume-text-sm']}`}
                    >
                      {project.description.map((desc, index) => (
                        <li key={index} className="flex">
                          <span className="mr-1.5 flex-shrink-0">•&nbsp;</span>
                          <span>
                            <SafeHtml html={desc} />
                          </span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </div>
        );

      case 'education':
        if (!education || education.length === 0) return null;
        return (
          <div key={section.id} className={baseStyles['resume-section']}>
            <h3 className={styles['section-title-accent']}>{section.displayName}</h3>
            <div className={baseStyles['resume-items']}>
              {education.map((edu) => (
                <div key={edu.id} className={baseStyles['resume-item']}>
                  <div
                    className={`flex justify-between items-baseline ${baseStyles['resume-row-tight']}`}
                  >
                    <h4 className={baseStyles['resume-item-title']}>{edu.institution}</h4>
                    <span className={`${baseStyles['resume-date']} ml-4`}>
                      {formatDateRange(edu.years)}
                    </span>
                  </div>
                  <div
                    className={`flex justify-between ${baseStyles['resume-item-subtitle']} ${baseStyles['resume-row-tight']}`}
                  >
                    <span>{edu.degree}</span>
                  </div>
                  {edu.description && (
                    <p className={baseStyles['resume-text-sm']}>{edu.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        );

      case 'additional':
        if (!additional) return null;
        return (
          <AdditionalSection
            key={section.id}
            additional={additional}
            displayName={section.displayName}
            labels={additionalSectionLabels}
          />
        );

      default:
        // Custom section - render using DynamicResumeSectionModern
        if (!section.isDefault) {
          return (
            <DynamicResumeSectionModern key={section.id} sectionMeta={section} resumeData={data} />
          );
        }
        return null;
    }
  };

  return (
    <div className={styles.container}>
      {/* Header Section - Centered Layout (always first) */}
      {personalInfo && (
        <header className={`text-center ${baseStyles['resume-header']}`}>
          {/* Name - Centered */}
          {personalInfo.name && (
            <h1 className={`${baseStyles['resume-name']} tracking-tight uppercase mb-1`}>
              {personalInfo.name}
            </h1>
          )}

          {/* Decorative accent underline under name */}
          <div className={styles['name-underline']} aria-hidden="true" />

          {/* Title - Centered, below name */}
          {personalInfo.title && (
            <h2
              className={`${baseStyles['resume-title']} ${baseStyles['resume-meta']} tracking-wide uppercase mt-3 mb-3`}
            >
              {personalInfo.title}
            </h2>
          )}

          {/* Contact - Own line, centered */}
          {renderContactInfo()}
        </header>
      )}

      {/* Render sections in order based on sectionMeta */}
      {sortedSections
        .filter((section) => section.key !== 'personalInfo')
        .map((section) => renderSection(section))}
    </div>
  );
};

/**
 * Additional info section (skills, languages, certifications, awards)
 */
const AdditionalSection: React.FC<{
  additional: ResumeData['additional'];
  displayName?: string;
  labels?: Partial<AdditionalSectionLabels>;
}> = ({ additional, displayName = 'Skills & Awards', labels }) => {
  console.log('[ResumeModern AdditionalSection] additional prop:', additional);

  if (!additional) {
    console.log('[ResumeModern AdditionalSection] additional is null/undefined, returning null');
    return null;
  }

  const {
    technicalSkills: rawTechnicalSkills = [],
    languages: rawLanguages = [],
    certificationsTraining: rawCertificationsTraining = [],
    awards: rawAwards = [],
    categorizedSkills,
  } = additional;

  // Drop blank/whitespace-only entries so empty lines (e.g. from editing in the
  // builder) never render in the resume or PDF (issue #763).

  // Support categorized skills (new) with fallback to flat list (legacy)
  const technicalSkills =
    categorizedSkills && categorizedSkills.length > 0
      ? [] // Will be rendered via categories
      : rawTechnicalSkills.filter(
          (item): item is string => typeof item === 'string' && item.trim() !== ''
        );
  const languages = rawLanguages.filter(
    (item): item is string => typeof item === 'string' && item.trim() !== ''
  );
  const certificationsTraining = rawCertificationsTraining.filter(
    (item): item is string => typeof item === 'string' && item.trim() !== ''
  );
  const awards = rawAwards.filter(
    (item): item is string => typeof item === 'string' && item.trim() !== ''
  );

  const mergedLabels: AdditionalSectionLabels = {
    technicalSkills: labels?.technicalSkills ?? 'Technical Skills:',
    languages: labels?.languages ?? 'Languages:',
    certifications: labels?.certifications ?? 'Certifications:',
    awards: labels?.awards ?? 'Awards:',
  };

  const hasContent =
    (categorizedSkills && categorizedSkills.length > 0) ||
    technicalSkills.length > 0 ||
    languages.length > 0 ||
    certificationsTraining.length > 0 ||
    awards.length > 0;

  console.log('[ResumeModern AdditionalSection] hasContent:', hasContent);
  console.log('[ResumeModern AdditionalSection] categorizedSkills:', categorizedSkills);
  console.log('[ResumeModern AdditionalSection] technicalSkills:', technicalSkills);
  console.log('[ResumeModern AdditionalSection] languages:', languages);
  console.log('[ResumeModern AdditionalSection] certificationsTraining:', certificationsTraining);
  console.log('[ResumeModern AdditionalSection] awards:', awards);

  if (!hasContent) {
    console.log('[ResumeModern AdditionalSection] no content, returning null');
    return null;
  }

  return (
    <div className={baseStyles['resume-section']}>
      <h3 className={styles['section-title-accent']}>{displayName}</h3>
      <div className={`${baseStyles['resume-stack']} ${baseStyles['resume-text-sm']}`}>
        {(technicalSkills.length > 0 || (categorizedSkills && categorizedSkills.length > 0)) && (
          <div>
            {categorizedSkills && categorizedSkills.length > 0 ? (
              <div className={baseStyles['resume-stack']}>
                {categorizedSkills.map((category, idx) => (
                  <div key={idx} className={baseStyles['resume-stack-tight']}>
                    <span className="font-bold">{category.name}:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {category.skills.map((skill, skillIdx) => (
                        <span key={skillIdx} className={baseStyles['resume-skill-pill']}>
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <>
                <span className="font-bold">{mergedLabels.technicalSkills}</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {technicalSkills.map((skill, index) => (
                    <span key={index} className={baseStyles['resume-skill-pill']}>
                      {skill}
                    </span>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
        {languages.length > 0 && (
          <div className={baseStyles['resume-stack-tight']}>
            <span className="font-bold">{mergedLabels.languages}</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {languages.map((lang, index) => (
                <span key={index} className={baseStyles['resume-skill-pill']}>
                  {lang}
                </span>
              ))}
            </div>
          </div>
        )}
        {certificationsTraining.length > 0 && (
          <div className="flex flex-col gap-1">
            <span className="font-bold">{mergedLabels.certifications}</span>
            <ul className={`ml-10 ${baseStyles['resume-list']} ${baseStyles['resume-text-sm']}`}>
              {certificationsTraining.map((cert, index) => (
                <li key={index} className="flex">
                  <span className="mr-1.5 flex-shrink-0">•&nbsp;</span>
                  <span>{cert}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        {awards.length > 0 && (
          <div className="flex flex-col gap-1">
            <span className="font-bold">{mergedLabels.awards}</span>
            <ul className={`ml-10 ${baseStyles['resume-list']} ${baseStyles['resume-text-sm']}`}>
              {awards.map((award, index) => (
                <li key={index} className="flex">
                  <span className="mr-1.5 flex-shrink-0">•&nbsp;</span>
                  <span>{award}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

/**
 * Dynamic section wrapper for Modern template
 * Uses accent-colored section titles
 */
const DynamicResumeSectionModern: React.FC<{
  sectionMeta: SectionMeta;
  resumeData: ResumeData;
}> = ({ sectionMeta, resumeData }) => {
  // Get the custom section data
  const customSection = resumeData.customSections?.[sectionMeta.key];

  if (!customSection) return null;

  // Check if section has content
  const hasContent = (() => {
    switch (sectionMeta.sectionType) {
      case 'text':
        return Boolean(customSection.text?.trim());
      case 'itemList':
        return Boolean(customSection.items?.length);
      case 'stringList':
        return Boolean(customSection.strings?.length);
      default:
        return false;
    }
  })();

  if (!hasContent) return null;

  return (
    <div className={baseStyles['resume-section']}>
      <h3 className={styles['section-title-accent']}>{sectionMeta.displayName}</h3>
      {renderDynamicContent(sectionMeta.sectionType, customSection)}
    </div>
  );
};

/**
 * Render dynamic section content based on type
 */
function renderDynamicContent(
  sectionType: SectionMeta['sectionType'],
  customSection: NonNullable<ResumeData['customSections']>[string]
) {
  switch (sectionType) {
    case 'text':
      if (!customSection.text?.trim()) return null;
      return <p className={`text-justify ${baseStyles['resume-text']}`}>{customSection.text}</p>;

    case 'itemList':
      if (!customSection.items?.length) return null;
      return (
        <div className={baseStyles['resume-items']}>
          {customSection.items.map((item) => (
            <div key={item.id} className={baseStyles['resume-item']}>
              <div
                className={`flex justify-between items-baseline ${baseStyles['resume-row-tight']}`}
              >
                <h4 className={baseStyles['resume-item-title']}>{item.title}</h4>
                {item.years && (
                  <span className={`${baseStyles['resume-meta-sm']} shrink-0 ml-4`}>
                    {formatDateRange(item.years)}
                  </span>
                )}
              </div>
              {(item.subtitle || item.location) && (
                <div
                  className={`flex justify-between items-center ${baseStyles['resume-row']} ${baseStyles['resume-meta']}`}
                >
                  {item.subtitle && <span>{item.subtitle}</span>}
                  {item.location && <span>{item.location}</span>}
                </div>
              )}
              {item.description && item.description.length > 0 && (
                <ul className={`ml-4 ${baseStyles['resume-list']} ${baseStyles['resume-text-sm']}`}>
                  {item.description.map((desc, index) => (
                    <li key={index} className="flex">
                      <span className="mr-1.5 flex-shrink-0">•&nbsp;</span>
                      <span>
                        <SafeHtml html={desc} />
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      );

    case 'stringList':
      if (!customSection.strings?.length) return null;
      return <div className={baseStyles['resume-text-sm']}>{customSection.strings.join(', ')}</div>;

    default:
      return null;
  }
}

export default ResumeModern;