import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import { LanguageProvider } from './contexts/LanguageContext'
import { useTranslation } from './translations'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'
import Residents from './components/Residents'
import Vendors from './components/Vendors'
import Payments from './components/Payments'
import Invoices from './components/Invoices'
import Bills from './components/Bills'
import Maintenance from './components/Maintenance'
import Events from './components/Events'
import Associates from './components/Associates'
import Violations from './components/Violations'
import Reports from './components/Reports'
import LanguageSwitcher from './components/LanguageSwitcher'
import './App.css'

const AppContent = () => {
  const { t } = useTranslation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="flex items-center justify-between px-6 py-4">
              <div className="flex items-center">
                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className="text-gray-500 hover:text-gray-600 lg:hidden"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
                <h1 className="text-2xl font-semibold text-gray-900 ml-4 lg:ml-0">
                  HOA Management System
                </h1>
              </div>
              <div className="flex items-center space-x-4">
                <LanguageSwitcher />
                <span className="text-sm text-gray-500">
                  {t('common.welcome')}, {t('common.admin')}
                </span>
              </div>
            </div>
          </header>

          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
            <div className="container mx-auto px-6 py-8">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/residents" element={<Residents />} />
                <Route path="/vendors" element={<Vendors />} />
                <Route path="/payments" element={<Payments />} />
                <Route path="/invoices" element={<Invoices />} />
                <Route path="/bills" element={<Bills />} />
                <Route path="/maintenance" element={<Maintenance />} />
                <Route path="/associates" element={<Associates />} />
                <Route path="/events" element={<Events />} />
                <Route path="/violations" element={<Violations />} />
                <Route path="/reports" element={<Reports />} />
              </Routes>
            </div>
          </main>

          {/* Footer */}
          <footer className="bg-white border-t border-gray-200 px-6 py-4">
            <div className="text-center text-sm text-gray-500">
              {t('footer.version')}
            </div>
          </footer>
        </div>
      </div>
    </Router>
  )
}

function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  )
}

export default App
