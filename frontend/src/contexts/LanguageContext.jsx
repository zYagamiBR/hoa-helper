import { createContext, useContext, useState, useEffect } from 'react'

const LanguageContext = createContext()

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    // Get saved language from localStorage or default to English
    return localStorage.getItem('hoa-language') || 'en'
  })

  const changeLanguage = (newLanguage) => {
    setLanguage(newLanguage)
    localStorage.setItem('hoa-language', newLanguage)
  }

  useEffect(() => {
    // Save language preference
    localStorage.setItem('hoa-language', language)
  }, [language])

  const value = {
    language,
    changeLanguage,
    isPortuguese: language === 'pt-br',
    isEnglish: language === 'en'
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}

