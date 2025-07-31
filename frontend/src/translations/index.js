import { en } from './en'
import { ptBr } from './pt-br'
import { useLanguage } from '../contexts/LanguageContext'

export const translations = {
  en,
  'pt-br': ptBr
}

export const useTranslation = () => {
  const { language } = useLanguage()
  
  const t = (key, params = {}) => {
    const keys = key.split('.')
    let value = translations[language]
    
    for (const k of keys) {
      if (value && typeof value === 'object') {
        value = value[k]
      } else {
        // Fallback to English if key not found
        value = translations.en
        for (const k of keys) {
          if (value && typeof value === 'object') {
            value = value[k]
          } else {
            return key // Return key if not found in any language
          }
        }
        break
      }
    }
    
    if (typeof value === 'string') {
      // Replace parameters in the string
      return value.replace(/\{(\w+)\}/g, (match, param) => {
        return params[param] !== undefined ? params[param] : match
      })
    }
    
    return key // Return key if value is not a string
  }
  
  return { t }
}

