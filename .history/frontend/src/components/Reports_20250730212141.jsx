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

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://zmhqivcv83mv.manus.space'

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
      const response = await fetch(`${API_BASE_URL}/api/reports/dashboard`)
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

      const response = await fetch(`${API_BASE_URL}/api/reports/quick-generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          report_type: templateName,
          year: year,
          month: month,
          quarter: quarter,
          generated_by: 'admin'
        })
      })

      if (response.ok) {
        const data = await response.json()
        alert(`Relatório gerado com sucesso! Arquivo: ${data.filename}`)
        
        // Download the generated report
        if (data.download_url) {
          const downloadResponse = await fetch(`${API_BASE_URL}${data.download_url}`)
          if (downloadResponse.ok) {
            const blob = await downloadResponse.blob()
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.style.display = 'none'
            a.href = url
            a.download = data.filename || 'relatorio.json'
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
        alert(`Erro ao gerar relatório: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Error generating report:', error)
      alert('Erro ao gerar relatório')
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

      const generateResponse = await fetch(`${API_BASE_URL}/api/reports/quick-generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          report_type: templateName,
          year: year,
          month: month,
          quarter: quarter,
          generated_by: 'admin'
        })
      })

      if (generateResponse.ok) {
        const generateData = await generateResponse.json()
        
        // Then send via email
        const emailResponse = await fetch(`${API_BASE_URL}/api/reports/send-email`, {
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
          alert(`Relatório enviado por email para ${emailData.sent_count} moradores!`)
        } else {
          const errorData = await emailResponse.json()
          alert(`Erro ao enviar email: ${errorData.error}`)
        }
        
        // Refresh stats
        fetchReportStats()
      } else {
        const errorData = await generateResponse.json()
        alert(`Erro ao gerar relatório: ${errorData.error}`)
      }
    } catch (error) {
      console.error('Error emailing report:', error)
      alert('Erro ao enviar relatório por email')
    } finally {
      setLoading(false)
    }
  }

  const reportTypes = [
    {
      id: 'financial_monthly',
      title: 'Relatório Financeiro Mensal',
      description: 'Receitas vs Despesas com análise detalhada por categoria',
      icon: DollarSign,
      color: 'bg-green-500',
      frequency: 'Mensal'
    },
    {
      id: 'transparency_monthly',
      title: 'Prestação de Contas Mensal',
      description: 'Relatório de transparência com despesas por grupo (Pessoal, Utilidades, etc.)',
      icon: FileText,
      color: 'bg-blue-500',
      frequency: 'Mensal'
    },
    {
      id: 'annual_comparative',
      title: 'Relatório Comparativo Anual',
      description: 'Evolução financeira dos últimos 5 anos com análise de tendências',
      icon: TrendingUp,
      color: 'bg-purple-500',
      frequency: 'Anual'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Relatórios</h1>
            <p className="text-gray-600 mt-1">
              Gere e distribua relatórios de transparência para os moradores
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-gray-500">Último relatório gerado</p>
              <p className="text-lg font-semibold text-gray-900">
                {reportStats.lastGenerated 
                  ? new Date(reportStats.lastGenerated).toLocaleDateString('pt-BR')
                  : 'Nunca'
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
              <p className="text-sm font-medium text-gray-500">Total de Relatórios</p>
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
              <p className="text-sm font-medium text-gray-500">Emails Enviados</p>
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
              <p className="text-sm font-medium text-gray-500">Relatórios Agendados</p>
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
              <p className="text-sm font-medium text-gray-500">Próximo Agendado</p>
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
                    {loading ? 'Gerando...' : 'Gerar PDF'}
                  </button>
                  
                  <button
                    onClick={() => emailReport(report.id)}
                    disabled={loading}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Mail className="w-4 h-4 mr-2" />
                    {loading ? 'Enviando...' : 'Enviar por Email'}
                  </button>
                </div>
                
                <span className="text-xs text-gray-400">
                  Última geração: Há 3 dias
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Scheduled Reports Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Relatórios Agendados</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-green-100">
                <Calendar className="w-4 h-4 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Relatório Financeiro Mensal</p>
                <p className="text-sm text-gray-500">Todo dia 1º do mês às 09:00</p>
              </div>
            </div>
            <span className="px-3 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
              Ativo
            </span>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-blue-100">
                <Calendar className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Prestação de Contas Trimestral</p>
                <p className="text-sm text-gray-500">A cada 3 meses no dia 15 às 10:00</p>
              </div>
            </div>
            <span className="px-3 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
              Ativo
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Reports

