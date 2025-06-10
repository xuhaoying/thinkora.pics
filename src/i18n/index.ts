import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Translation resources
import en from './locales/en.json';
import zh from './locales/zh.json';
import es from './locales/es.json';
import fr from './locales/fr.json';
import de from './locales/de.json';
import ja from './locales/ja.json';
import ko from './locales/ko.json';
import pt from './locales/pt.json';
import ru from './locales/ru.json';
import ar from './locales/ar.json';

const resources = {
  en: { translation: en },
  zh: { translation: zh },
  es: { translation: es },
  fr: { translation: fr },
  de: { translation: de },
  ja: { translation: ja },
  ko: { translation: ko },
  pt: { translation: pt },
  ru: { translation: ru },
  ar: { translation: ar }
};

// Detect user's language
const getDefaultLanguage = (): string => {
  // Check localStorage first
  const savedLanguage = localStorage.getItem('language');
  if (savedLanguage && Object.keys(resources).includes(savedLanguage)) {
    return savedLanguage;
  }

  // Fallback to browser language
  const browserLanguage = navigator.language.split('-')[0];
  if (Object.keys(resources).includes(browserLanguage)) {
    return browserLanguage;
  }

  // Default to English
  return 'en';
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: getDefaultLanguage(),
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
    react: {
      useSuspense: false,
    }
  });

export default i18n;