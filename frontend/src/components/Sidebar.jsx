import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from '../translations'
import { 
  Home, 
  Users, 
  Building, 
  CreditCard, 
  FileText, 
  Receipt,
  Wrench,
  UserCheck,
  Calendar, 
  AlertTriangle,
  BarChart3,
  X 
} from 'lucide-react'

const Sidebar = ({ isOpen, setIsOpen }) => {
  const location = useLocation()
  const { t } = useTranslation()

  const navigation = [
    { name: t('nav.dashboard'), href: '/', icon: Home },
    { name: t('nav.residents'), href: '/residents', icon: Users },
    { name: t('nav.vendors'), href: '/vendors', icon: Building },
    { name: t('nav.payments'), href: '/payments', icon: CreditCard },
    { name: t('nav.invoices'), href: '/invoices', icon: FileText },
    { name: t('nav.bills'), href: '/bills', icon: Receipt },
    { name: t('nav.maintenance'), href: '/maintenance', icon: Wrench },
    { name: t('nav.associates'), href: '/associates', icon: UserCheck },
    { name: t('nav.events'), href: '/events', icon: Calendar },
    { name: t('nav.violations'), href: '/violations', icon: AlertTriangle },
    { name: t('nav.reports'), href: '/reports', icon: BarChart3 },
  ]

  return (
    <>
      {/* Mobile sidebar overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        >
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75"></div>
        </div>
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">HOA Portal</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden text-gray-500 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <nav className="mt-6">
          <div className="px-3">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`
                    group flex items-center px-3 py-2 text-sm font-medium rounded-md mb-1 transition-colors duration-200
                    ${isActive 
                      ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700' 
                      : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                    }
                  `}
                >
                  <item.icon className={`
                    mr-3 h-5 w-5 transition-colors duration-200
                    ${isActive ? 'text-blue-700' : 'text-gray-500 group-hover:text-gray-700'}
                  `} />
                  {item.name}
                </Link>
              )
            })}
          </div>
        </nav>

        <div className="absolute bottom-0 w-full p-4 border-t border-gray-200">
          <div className="text-xs text-gray-500 text-center">
            {t('footer.version')}
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar

