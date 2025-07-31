import { useState } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { Button } from '@/components/ui/button'
import { Globe, ChevronDown } from 'lucide-react'

const LanguageSwitcher = () => {
  const { language, changeLanguage } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'pt-br', name: 'Português (BR)', flag: '🇧🇷' }
  ]

  const currentLanguage = languages.find(lang => lang.code === language)

  const handleLanguageChange = (langCode) => {
    changeLanguage(langCode)
    setIsOpen(false)
  }

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 min-w-[140px]"
      >
        <Globe className="w-4 h-4" />
        <span className="flex items-center gap-1">
          <span>{currentLanguage?.flag}</span>
          <span className="hidden sm:inline">{currentLanguage?.name}</span>
        </span>
        <ChevronDown className="w-4 h-4" />
      </Button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown */}
          <div className="absolute right-0 top-full mt-1 z-20 bg-white border border-gray-200 rounded-md shadow-lg min-w-[160px]">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code)}
                className={`w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-2 ${
                  language === lang.code ? 'bg-blue-50 text-blue-600' : 'text-gray-700'
                }`}
              >
                <span>{lang.flag}</span>
                <span>{lang.name}</span>
                {language === lang.code && (
                  <span className="ml-auto text-blue-600">✓</span>
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export default LanguageSwitcher

