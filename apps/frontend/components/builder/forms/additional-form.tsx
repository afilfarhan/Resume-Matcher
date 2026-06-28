'use client';

import React from 'react';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { AdditionalInfo, SkillCategory } from '@/components/dashboard/resume-component';
import { useTranslations } from '@/lib/i18n';

interface AdditionalFormProps {
  data: AdditionalInfo;
  onChange: (data: AdditionalInfo) => void;
}

export const AdditionalForm: React.FC<AdditionalFormProps> = ({ data, onChange }) => {
  const { t } = useTranslations();
  
  // Debug logging to track categorizedSkills in AdditionalForm
  React.useEffect(() => {
    console.log('[ADDITIONAL_FORM] Received data:', {
      hasCategorizedSkills: (data.categorizedSkills?.length ?? 0) > 0,
      categorizedSkillsCount: data.categorizedSkills?.length ?? 0,
      technicalSkills: data.technicalSkills,
      categorizedSkills: data.categorizedSkills,
    });
  }, [data]);

  // Helper to handle array conversions (text -> string[])
  const handleArrayChange = (field: keyof AdditionalInfo, value: string) => {
    // Split by newlines only. Blank/whitespace lines are preserved while editing
    // so pressing Enter creates a new line (issue #763); consumers filter empty
    // entries at render time, and the backend drops them on save.
    const items = value.split('\n');
    const newData: AdditionalInfo = { ...data, [field]: items };
    onChange(newData);
  };

  // Handle categorized skills changes
  const handleCategoryChange = (categoryIndex: number, field: 'name' | 'skills', value: string | string[]) => {
    const newData = { ...data };
    if (!newData.categorizedSkills) {
      newData.categorizedSkills = [];
    }
    newData.categorizedSkills[categoryIndex] = {
      ...newData.categorizedSkills[categoryIndex],
      [field]: value,
    };
    onChange(newData);
  };

  // Add a new category
  const addCategory = () => {
    const newData = { ...data };
    if (!newData.categorizedSkills) {
      newData.categorizedSkills = [];
    }
    newData.categorizedSkills.push({ name: '', skills: [] });
    onChange(newData);
  };

  // Remove a category
  const removeCategory = (categoryIndex: number) => {
    const newData = { ...data };
    if (newData.categorizedSkills) {
      newData.categorizedSkills.splice(categoryIndex, 1);
      onChange(newData);
    }
  };

  // Convert skills array to newline-separated string for textarea
  const formatSkillsArray = (skills?: string[]) => {
    return skills?.join('\n') || '';
  };

  const formatArray = (arr?: string[]) => {
    return arr?.join('\n') || '';
  };

  // Check if we have categorized skills to display
  const hasCategorizedSkills = data.categorizedSkills && data.categorizedSkills.length > 0;

  // Explicitly allow Enter key to create newlines (prevent form submission interference)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      // Allow default behavior (newline insertion)
      e.stopPropagation();
    }
  };

  return (
    <div className="space-y-6">
      <p className="font-mono text-xs uppercase tracking-wider text-blue-700">
        {t('builder.additionalForm.instructions')}
      </p>

      {/* Technical Skills - always editable */}
      <div className="space-y-2">
        <Label
          htmlFor="technicalSkills"
          className="font-mono text-xs uppercase tracking-wider text-steel-grey"
        >
          {t('resume.additional.technicalSkills')}
        </Label>
        {hasCategorizedSkills ? (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="text-xs text-ink-soft italic">
                {t('builder.additionalForm.categorizedSkillsNotice')}
              </div>
              <button
                type="button"
                onClick={addCategory}
                className="text-xs font-mono text-primary hover:underline"
              >
                + {t('builder.additionalForm.addCategory')}
              </button>
            </div>
            {data.categorizedSkills?.map((category, idx) => (
              <div key={idx} className="border border-black p-3 rounded-none shadow-sm relative">
                <button
                  type="button"
                  onClick={() => removeCategory(idx)}
                  className="absolute top-2 right-2 text-xs text-destructive hover:underline"
                >
                  ×
                </button>
                <div className="mb-2">
                  <input
                    type="text"
                    value={category.name}
                    onChange={(e) => handleCategoryChange(idx, 'name', e.target.value)}
                    placeholder={t('builder.additionalForm.placeholders.categoryName')}
                    className="w-full border border-black rounded-none p-1 text-sm font-bold"
                  />
                </div>
                <Textarea
                  value={formatSkillsArray(category.skills)}
                  onChange={(e) => handleCategoryChange(idx, 'skills', e.target.value.split('\n'))}
                  onKeyDown={handleKeyDown}
                  placeholder={t('builder.additionalForm.placeholders.skills')}
                  className="min-h-[80px] text-black rounded-none border-black bg-white focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-700"
                />
              </div>
            ))}
          </div>
        ) : (
          <Textarea
            id="technicalSkills"
            value={formatArray(data.technicalSkills)}
            onChange={(e) => handleArrayChange('technicalSkills', e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t('builder.additionalForm.placeholders.technicalSkills')}
            className="min-h-[120px] text-black rounded-none border-black bg-white focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-700"
          />
        )}
      </div>

      {/* Languages */}
      <div className="space-y-2">
        <Label
          htmlFor="languages"
          className="font-mono text-xs uppercase tracking-wider text-steel-grey"
        >
          {t('resume.sections.languages')}
        </Label>
        <Textarea
          id="languages"
          value={formatArray(data.languages)}
          onChange={(e) => handleArrayChange('languages', e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t('builder.additionalForm.placeholders.languages')}
          className="min-h-[120px] text-black rounded-none border-black bg-white focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-700"
        />
      </div>

      {/* Certifications */}
      <div className="space-y-2">
        <Label
          htmlFor="certifications"
          className="font-mono text-xs uppercase tracking-wider text-steel-grey"
        >
          {t('resume.sections.certifications')}
        </Label>
        <Textarea
          id="certifications"
          value={formatArray(data.certificationsTraining)}
          onChange={(e) => handleArrayChange('certificationsTraining', e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t('builder.additionalForm.placeholders.certifications')}
          className="min-h-[120px] text-black rounded-none border-black bg-white focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-700"
        />
      </div>

      {/* Awards */}
      <div className="space-y-2">
        <Label
          htmlFor="awards"
          className="font-mono text-xs uppercase tracking-wider text-steel-grey"
        >
          {t('resume.sections.awards')}
        </Label>
        <Textarea
          id="awards"
          value={formatArray(data.awards)}
          onChange={(e) => handleArrayChange('awards', e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={t('builder.additionalForm.placeholders.awards')}
          className="min-h-[120px] text-black rounded-none border-black bg-white focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-700"
        />
      </div>
    </div>
  );
};
