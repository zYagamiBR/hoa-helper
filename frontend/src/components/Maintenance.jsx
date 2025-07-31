import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Plus, Search, Edit, Trash2, X, Clock, CheckCircle, AlertCircle, Wrench, Filter } from 'lucide-react'
import { useTranslation } from '../translations'

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Maintenance = () => {
  const { t } = useTranslation()
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filters, setFilters] = useState({
    priority: '',
    status: '',
    category: ''
  })
  const [showFilters, setShowFilters] = useState(false)
  const [showEditForm, setShowEditForm] = useState(false)
  const [editingRequest, setEditingRequest] = useState(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    location: '',
    priority: 'medium',
    status: 'open',
    category: '',
    estimated_cost: '',
    actual_cost: ''
  })

  useEffect(() => {
    fetchRequests()
  }, [])

  const fetchRequests = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/maintenance`)
      if (response.ok) {
        const data = await response.json()
        setRequests(data)
      } else {
        console.error('Failed to fetch maintenance requests')
      }
    } catch (error) {
      console.error('Error fetching maintenance requests:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredRequests = requests.filter(request => {
    const matchesSearch = request.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         request.location?.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesPriority = !filters.priority || request.priority === filters.priority
    const matchesStatus = !filters.status || request.status === filters.status
    const matchesCategory = !filters.category || request.category === filters.category
    
    return matchesSearch && matchesPriority && matchesStatus && matchesCategory
  })

  const clearFilters = () => {
    setFilters({ priority: '', status: '', category: '' })
    setSearchTerm('')
  }

  const handleEdit = (request) => {
    setEditingRequest(request)
    setFormData({
      title: request.title || '',
      description: request.description || '',
      location: request.location || '',
      priority: request.priority || 'medium',
      status: request.status || 'open',
      category: request.category || '',
      estimated_cost: request.estimated_cost || '',
      actual_cost: request.actual_cost || ''
    })
    setShowEditForm(true)
  }

  const handleDelete = async (requestId) => {
    if (window.confirm(t('maintenance.confirmDelete'))) {
      try {
        const response = await fetch(`${API_BASE_URL}/maintenance/${requestId}`, {
          method: 'DELETE'
        })
        if (response.ok) {
          setRequests(requests.filter(request => request.id !== requestId))
        } else {
          alert(t('common.error'))
        }
      } catch (error) {
        console.error('Error deleting maintenance request:', error)
        alert(t('common.error'))
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE_URL}/maintenance/${editingRequest.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      
      if (response.ok) {
        const updatedRequest = await response.json()
        setRequests(requests.map(request => 
          request.id === editingRequest.id ? updatedRequest : request
        ))
        setShowEditForm(false)
        setEditingRequest(null)
        resetForm()
      } else {
        alert(t('common.error'))
      }
    } catch (error) {
      console.error('Error updating maintenance request:', error)
      alert(t('common.error'))
    }
  }

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      location: '',
      priority: 'medium',
      status: 'open',
      category: '',
      estimated_cost: '',
      actual_cost: ''
    })
  }

  const openRequests = requests.filter(r => r.status === 'open' || r.status === 'pending')
  const inProgressRequests = requests.filter(r => r.status === 'in_progress')
  const completedRequests = requests.filter(r => r.status === 'completed')

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityText = (priority) => {
    switch (priority) {
      case 'low': return 'Baixa'
      case 'medium': return 'Média'
      case 'high': return 'Alta'
      default: return 'N/A'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'open':
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      case 'in_progress':
        return <Clock className="h-4 w-4 text-yellow-500" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'open': return 'Aberta'
      case 'pending': return 'Pendente'
      case 'in_progress': return 'Em Andamento'
      case 'completed': return 'Concluída'
      default: return 'N/A'
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(amount)
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
          <h2 className="text-3xl font-bold text-gray-900">{t('maintenance.title')}</h2>
          <p className="text-gray-600">{t('maintenance.subtitle')}</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Plus className="h-4 w-4 mr-2" />
          {t('maintenance.newRequest')}
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Wrench className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('maintenance.allRequests')}</p>
              <p className="text-2xl font-bold text-gray-900">{requests.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <AlertCircle className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Abertas</p>
              <p className="text-2xl font-bold text-gray-900">{openRequests.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Clock className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Em Andamento</p>
              <p className="text-2xl font-bold text-gray-900">{inProgressRequests.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Concluídas</p>
              <p className="text-2xl font-bold text-gray-900">{completedRequests.length}</p>
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
                placeholder={t('maintenance.searchPlaceholder')}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
            {(filters.priority || filters.status || filters.category || searchTerm) && (
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
                  {t('maintenance.priority')}
                </label>
                <select
                  value={filters.priority}
                  onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Todas as Prioridades</option>
                  <option value="low">Baixa</option>
                  <option value="medium">Média</option>
                  <option value="high">Alta</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('maintenance.status')}
                </label>
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Todos os Status</option>
                  <option value="open">Aberta</option>
                  <option value="pending">Pendente</option>
                  <option value="in_progress">Em Andamento</option>
                  <option value="completed">Concluída</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('maintenance.category')}
                </label>
                <select
                  value={filters.category}
                  onChange={(e) => setFilters({ ...filters, category: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Todas as Categorias</option>
                  <option value="electrical">Elétrica</option>
                  <option value="plumbing">Hidráulica</option>
                  <option value="cleaning">Limpeza</option>
                  <option value="security">Segurança</option>
                  <option value="general">Geral</option>
                </select>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Results Summary */}
      {filteredRequests.length !== requests.length && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-blue-800">
            {t('filters.showingResults').replace('{count}', filteredRequests.length)} de {requests.length}
          </p>
        </div>
      )}

      {/* Maintenance Requests Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('maintenance.title_field')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('maintenance.description')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Local
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('maintenance.priority')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('maintenance.status')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('maintenance.category')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {t('maintenance.requestDate')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredRequests.length === 0 ? (
                <tr>
                  <td colSpan="8" className="px-6 py-4 text-center text-gray-500">
                    {searchTerm || filters.priority || filters.status || filters.category 
                      ? t('filters.noResults') 
                      : t('maintenance.noRequests')
                    }
                  </td>
                </tr>
              ) : (
                filteredRequests.map((request) => (
                  <tr key={request.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {request.title || 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 max-w-xs">
                      <div className="truncate" title={request.description}>
                        {request.description || 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {request.location || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(request.priority)}`}>
                        {getPriorityText(request.priority)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getStatusIcon(request.status)}
                        <span className="ml-2 text-sm text-gray-900">
                          {getStatusText(request.status)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {request.category || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(request.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-blue-600 border-blue-600 hover:bg-blue-50"
                          onClick={() => handleEdit(request)}
                        >
                          <Edit className="h-3 w-3 mr-1" />
                          {t('common.edit')}
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-red-600 border-red-600 hover:bg-red-50"
                          onClick={() => handleDelete(request.id)}
                        >
                          <Trash2 className="h-3 w-3 mr-1" />
                          {t('common.delete')}
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Edit Form Modal */}
      {showEditForm && editingRequest && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Editar Solicitação de Manutenção</h3>
              <Button variant="ghost" size="sm" onClick={() => setShowEditForm(false)}>
                <X className="w-4 h-4" />
              </Button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('maintenance.title_field')} *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('maintenance.description')} *
                </label>
                <textarea
                  required
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('maintenance.priority')}
                  </label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="low">Baixa</option>
                    <option value="medium">Média</option>
                    <option value="high">Alta</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('maintenance.status')}
                  </label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="open">Aberta</option>
                    <option value="pending">Pendente</option>
                    <option value="in_progress">Em Andamento</option>
                    <option value="completed">Concluída</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => setShowEditForm(false)}
                >
                  {t('common.cancel')}
                </Button>
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                  {t('common.save')}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Maintenance

