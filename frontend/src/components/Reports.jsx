import { useState, useEffect } from 'react'
import { useTranslation } from '../translations'
import { 
  FileText, 
  Download, 
  Calendar, 
  TrendingUp, 
  DollarSign, 
  Users,
  Building,
  Mail,
  Clock,
  BarChart3
} from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Reports = () => {
  const { t } = useTranslation()
  const [loading, setLoading] = useState(false)
  const [reportStats, setReportStats] = useState({
    totalReports: 0,
    lastGenerated: null,
    emailsSent: 0,
    scheduledReports: 0
  })

  useEffect(() => {
    fetchReportStats()
  }, [])

  const fetchReportStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/dashboard`)
      if (response.ok) {
        const data = await response.json()
        setReportStats({
          totalReports: data.total_reports || 0,
          lastGenerated: data.recent_generations?.[0]?.generated_at || null,
          emailsSent: data.total_emails_sent || 0,
          scheduledReports: data.scheduled_reports || 0
        })
      }
    } catch (error) {
      console.error('Error fetching report stats:', error)
    }
  }

  const generateReport = async (templateName) => {
    setLoading(true)
    try {
      const currentDate = new Date()
      const year = currentDate.getFullYear()
      const month = currentDate.getMonth() + 1
      const quarter = Math.floor((currentDate.getMonth()) / 3) + 1

      const response = await fetch(`${API_BASE_URL}/reports/quick-generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_name: templateName,
          year: year,
          month: month,
          quarter: quarter,
          generated_by: 'admin'
        })
      })

      if (response.ok) {
        const data = await response.json()
        alert(`${t('reports.generateReport')} ${t('common.success')}! ${t('common.file')}: ${data.generation.file_name}`)
        
        // Download the generated report
        if (data.download_url) {
          const downloadResponse = await fetch(`${API_BASE_URL}${data.download_url}`)
          if (downloadResponse.ok) {
            const blob = await downloadResponse.blob()
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.style.display = 'none'
            a.href = url
            a.download = data.generation.file_name || 'relatorio.pdf'
            document.body.appendChild(a)
            a.click()
            window.URL.revokeObjectURL(url)
            document.body.removeChild(a)
          }
        }
        
        // Refresh stats
        fetchReportStats()
      } else {
        const errorData = await response.json()
        alert(`${t('common.error')}: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Error generating report:', error)
      alert(t('common.error'))
    } finally {
      setLoading(false)
    }
  }

  const emailReport = async (templateName) => {
    setLoading(true)
    try {
      // First generate the report
      const currentDate = new Date()
      const year = currentDate.getFullYear()
      const month = currentDate.getMonth() + 1
      const quarter = Math.floor((currentDate.getMonth()) / 3) + 1

      const generateResponse = await fetch(`${API_BASE_URL}/reports/quick-generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          template_name: templateName,
          year: year,
          month: month,
          quarter: quarter,
          generated_by: 'admin'
        })
      })

      if (generateResponse.ok) {
        const generateData = await generateResponse.json()
        
        // Then send via email
        const emailResponse = await fetch(`${API_BASE_URL}/reports/send-email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            generation_id: generateData.generation.id,
            recipients: [] // Empty array means send to all residents
          })
        })

        if (emailResponse.ok) {
          const emailData = await emailResponse.json()
          alert(`${t('reports.sendByEmail')} ${t('common.success')} para ${emailData.sent_count} moradores!`)
        } else {
          const errorData = await emailResponse.json()
          alert(`${t('common.error')}: ${errorData.error}`)
        }
        
        // Refresh stats
        fetchReportStats()
      } else {
        const errorData = await generateResponse.json()
        alert(`${t('common.error')}: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Error emailing report:', error)
      alert(t('common.error'))
    } finally {
      setLoading(false)
    }
  }

  const reportTypes = [
    {
      id: 'financial_monthly',
      title: t('reports.financialMonthly'),
      description: t('reports.financialMonthlyDesc'),
      icon: DollarSign,
      color: 'bg-green-500',
      frequency: t('reports.monthly')
    },
    {
      id: 'transparency_monthly',
      title: t('reports.transparencyMonthly'),
      description: t('reports.transparencyMonthlyDesc'),
      icon: FileText,
      color: 'bg-blue-500',
      frequency: t('reports.monthly')
    },
    {
      id: 'annual_comparative',
      title: t('reports.annualComparative'),
      description: t('reports.annualComparativeDesc'),
      icon: TrendingUp,
      color: 'bg-purple-500',
      frequency: t('reports.annual')
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{t('reports.title')}</h1>
            <p className="text-gray-600 mt-1">
              {t('reports.subtitle')}
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-gray-500">{t('reports.lastGenerated')}</p>
              <p className="text-lg font-semibold text-gray-900">
                {reportStats.lastGenerated 
                  ? new Date(reportStats.lastGenerated).toLocaleDateString('pt-BR')
                  : t('reports.never')
                }
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">{t('reports.totalReports')}</p>
              <p className="text-2xl font-bold text-gray-900">{reportStats.totalReports}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100">
              <Mail className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">{t('reports.emailsSent')}</p>
              <p className="text-2xl font-bold text-gray-900">{reportStats.emailsSent}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-100">
              <Clock className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">{t('reports.scheduledReports')}</p>
              <p className="text-2xl font-bold text-gray-900">{reportStats.scheduledReports}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-orange-100">
              <Calendar className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">{t('reports.nextScheduled')}</p>
              <p className="text-lg font-bold text-gray-900">
                {new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('pt-BR')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Report Types */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {reportTypes.map((report) => {
          const IconComponent = report.icon
          return (
            <div key={report.id} className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4">
                  <div className={`p-3 rounded-lg ${report.color}`}>
                    <IconComponent className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">{report.title}</h3>
                    <p className="text-gray-600 mt-1 text-sm">{report.description}</p>
                    <div className="flex items-center mt-2">
                      <Calendar className="w-4 h-4 text-gray-400 mr-1" />
                      <span className="text-sm text-gray-500">{report.frequency}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
                <div className="flex space-x-3">
                  <button
                    onClick={() => generateReport(report.id)}
                    disabled={loading}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    {loading ? t('reports.generating') : t('reports.downloadPDF')}
                  </button>
                  
                  <button
                    onClick={() => emailReport(report.id)}
                    disabled={loading}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Mail className="w-4 h-4 mr-2" />
                    {loading ? t('reports.sending') : t('reports.sendByEmail')}
                  </button>
                </div>
                
                <span className="text-xs text-gray-400">
                  {t('reports.lastGenerated')}: Há 3 dias
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Scheduled Reports Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">{t('reports.scheduledReportsTitle')}</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-green-100">
                <Calendar className="w-4 h-4 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">{t('reports.financialMonthly')}</p>
                <p className="text-sm text-gray-500">{t('reports.everyFirstDay')}</p>
              </div>
            </div>
            <span className="px-3 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
              {t('reports.active')}
            </span>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-blue-100">
                <Calendar className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">{t('reports.transparencyMonthly')}</p>
                <p className="text-sm text-gray-500">{t('reports.everyMonth')}</p>
              </div>
            </div>
            <span className="px-3 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
              {t('reports.active')}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Reports

