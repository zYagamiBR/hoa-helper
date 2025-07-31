import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Plus, Search, DollarSign, TrendingUp, Calendar, Filter, X } from 'lucide-react'
import { useTranslation } from '../translations'

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Payments = () => {
  const { t } = useTranslation()
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filters, setFilters] = useState({
    method: '',
    status: '',
    type: ''
  })
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    fetchPayments()
  }, [])

  const fetchPayments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/payments`)
      if (response.ok) {
        const data = await response.json()
        setPayments(data)
      } else {
        console.error('Failed to fetch payments')
      }
    } catch (error) {
      console.error('Error fetching payments:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredPayments = payments.filter(payment => {
    const matchesSearch = payment.resident_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         payment.payment_type?.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesMethod = !filters.method || payment.payment_method === filters.method
    const matchesStatus = !filters.status || payment.status === filters.status
    const matchesType = !filters.type || payment.payment_type === filters.type
    
    return matchesSearch && matchesMethod && matchesStatus && matchesType
  })

  const clearFilters = () => {
    setFilters({ method: '', status: '', type: '' })
    setSearchTerm('')
  }

  const totalAmount = payments.reduce((sum, payment) => sum + parseFloat(payment.amount || 0), 0)
  const thisMonthPayments = payments.filter(payment => {
    const paymentDate = new Date(payment.payment_date)
    const now = new Date()
    return paymentDate.getMonth() === now.getMonth() && paymentDate.getFullYear() === now.getFullYear()
  })

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(amount)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  const getStatusBadge = (status) => {
    const statusMap = {
      completed: { class: 'bg-green-100 text-green-800', text: t('payments.completed') },
      pending: { class: 'bg-yellow-100 text-yellow-800', text: t('payments.pending') },
      cancelled: { class: 'bg-red-100 text-red-800', text: t('payments.cancelled') }
    }
    const statusInfo = statusMap[status] || { class: 'bg-gray-100 text-gray-800', text: status }
    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${statusInfo.class}`}>
        {statusInfo.text}
      </span>
    )
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg text-gray-600">{t('common.loading')}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('payments.title')}</h2>
          <p className="text-gray-600">{t('payments.subtitle')}</p>
        </div>
        <Button className="bg-purple-600 hover:bg-purple-700">
          <Plus className="h-4 w-4 mr-2" />
          {t('payments.addPayment')}
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('payments.totalCollected')}</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalAmount)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('payments.paymentsThisMonth')}</p>
              <p className="text-2xl font-bold text-gray-900">{thisMonthPayments.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Calendar className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('payments.totalPayments')}</p>
              <p className="text-2xl font-bold text-gray-900">{payments.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="flex flex-col space-y-4">
          <div className="flex items-center space-x-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                placeholder={t('payments.searchPlaceholder')}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <Button
              variant="outline"
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-2"
            >
              <Filter className="h-4 w-4" />
              <span>{t('filters.filter')}</span>
            </Button>
            {(filters.method || filters.status || filters.type || searchTerm) && (
              <Button
                variant="outline"
                onClick={clearFilters}
                className="flex items-center space-x-2"
              >
                <X className="h-4 w-4" />
                <span>{t('filters.clearFilters')}</span>
              </Button>
            )}
          </div>

          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('payments.filterByMethod')}
                </label>
                <select
                  value={filters.method}
                  onChange={(e) => setFilters({ ...filters, method: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">{t('payments.allMethods')}</option>
                  <option value="cash">{t('payments.cash')}</option>
                  <option value="credit_card">{t('payments.creditCard')}</option>
                  <option value="debit_card">{t('payments.debitCard')}</option>
                  <option value="bank_transfer">{t('payments.bankTransfer')}</option>
                  <option value="pix">{t('payments.pix')}</option>
                  <option value="check">{t('payments.check')}</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('payments.filterByStatus')}
                </label>
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">{t('payments.allStatuses')}</option>
                  <option value="completed">{t('payments.completed')}</option>
                  <option value="pending">{t('payments.pending')}</option>
                  <option value="cancelled">{t('payments.cancelled')}</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('payments.filterByType')}
                </label>
                <select
                  value={filters.type}
                  onChange={(e) => setFilters({ ...filters, type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="">{t('payments.allTypes')}</option>
                  <option value="monthly_fee">Taxa Mensal</option>
                  <option value="maintenance">Manutenção</option>
                  <option value="fine">Multa</option>
                  <option value="special_assessment">Taxa Especial</option>
                </select>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Results Summary */}
      {filteredPayments.length !== payments.length && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-blue-800">
            {t('filters.showingResults').replace('{count}', filteredPayments.length)} de {payments.length}
          </p>
        </div>
      )}

      {/* Payments Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('payments.resident')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('payments.type')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('payments.amount')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('payments.method')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('payments.date')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('payments.status')}
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredPayments.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center text-gray-500">
                    {searchTerm || filters.method || filters.status || filters.type 
                      ? t('filters.noResults') 
                      : t('payments.noPayments')
                    }
                  </td>
                </tr>
              ) : (
                filteredPayments.map((payment) => (
                  <tr key={payment.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {payment.resident_name || 'N/A'}
                        </div>
                        <div className="text-sm text-gray-500">
                          Prédio {payment.resident_building}, Apt {payment.resident_apartment}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {payment.payment_type || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {formatCurrency(payment.amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {payment.payment_method || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(payment.payment_date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(payment.status)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Payments

