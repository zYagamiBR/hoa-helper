import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Plus, Search, AlertTriangle, CheckCircle, Clock, XCircle, Edit, Trash2, X } from 'lucide-react'
import { useTranslation } from '../translations'

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Violations = () => {
  const { t } = useTranslation()
  const [violations, setViolations] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showEditForm, setShowEditForm] = useState(false)
  const [editingViolation, setEditingViolation] = useState(null)
  const [formData, setFormData] = useState({
    violation_type: '',
    description: '',
    location: '',
    severity: 'medium',
    status: 'open',
    fine_amount: '',
    fine_paid: false,
    notes: ''
  })

  useEffect(() => {
    fetchViolations()
  }, [])

  const fetchViolations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/violations`)
      if (response.ok) {
        const data = await response.json()
        setViolations(data)
      } else {
        console.error('Failed to fetch violations')
      }
    } catch (error) {
      console.error('Error fetching violations:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (violation) => {
    setEditingViolation(violation)
    setFormData({
      violation_type: violation.violation_type || '',
      description: violation.description || '',
      location: violation.location || '',
      severity: violation.severity || 'medium',
      status: violation.status || 'open',
      fine_amount: violation.fine_amount || '',
      fine_paid: violation.fine_paid || false,
      notes: violation.notes || ''
    })
    setShowEditForm(true)
  }

  const handleDelete = async (violationId) => {
    if (window.confirm(t('violations.confirmDelete'))) {
      try {
        const response = await fetch(`${API_BASE_URL}/violations/${violationId}`, {
          method: 'DELETE'
        })
        if (response.ok) {
          setViolations(violations.filter(violation => violation.id !== violationId))
        } else {
          alert('Erro ao excluir violação')
        }
      } catch (error) {
        console.error('Error deleting violation:', error)
        alert('Erro ao excluir violação')
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE_URL}/violations/${editingViolation.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      
      if (response.ok) {
        const updatedViolation = await response.json()
        setViolations(violations.map(violation => 
          violation.id === editingViolation.id ? updatedViolation : violation
        ))
        setShowEditForm(false)
        setEditingViolation(null)
        resetForm()
      } else {
        alert('Erro ao atualizar violação')
      }
    } catch (error) {
      console.error('Error updating violation:', error)
      alert('Erro ao atualizar violação')
    }
  }

  const resetForm = () => {
    setFormData({
      violation_type: '',
      description: '',
      location: '',
      severity: 'medium',
      status: 'open',
      fine_amount: '',
      fine_paid: false,
      notes: ''
    })
  }

  const filteredViolations = violations.filter(violation =>
    violation.violation_type?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    violation.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    violation.resident_name?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const openViolations = violations.filter(v => v.status === 'open' || v.status === 'pending')
  const resolvedViolations = violations.filter(v => v.status === 'resolved' || v.status === 'closed')
  const totalFines = violations.reduce((sum, v) => sum + (parseFloat(v.fine_amount) || 0), 0)

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'low': return 'bg-yellow-100 text-yellow-800'
      case 'medium': return 'bg-orange-100 text-orange-800'
      case 'high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSeverityText = (severity) => {
    switch (severity) {
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
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case 'resolved':
      case 'closed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'in_progress':
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <XCircle className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'open': return 'Aberta'
      case 'pending': return 'Pendente'
      case 'resolved': return 'Resolvida'
      case 'closed': return 'Fechada'
      case 'in_progress': return 'Em Andamento'
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
          <div className="text-lg text-gray-600">Carregando violações...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('violations.title')}</h2>
          <p className="text-gray-600">{t('violations.subtitle')}</p>
        </div>
        <Button className="bg-green-600 hover:bg-green-700">
          <Plus className="h-4 w-4 mr-2" />
          Reportar Violação
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('violations.totalViolations')}</p>
              <p className="text-2xl font-bold text-gray-900">{violations.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <XCircle className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('violations.openViolations')}</p>
              <p className="text-2xl font-bold text-gray-900">{openViolations.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('violations.resolvedViolations')}</p>
              <p className="text-2xl font-bold text-gray-900">{resolvedViolations.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <span className="text-purple-600 font-bold text-lg">R$</span>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total em Multas</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalFines)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Buscar violações..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Violations Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Morador
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo de Violação
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descrição
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Gravidade
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Multa
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredViolations.length === 0 ? (
                <tr>
                  <td colSpan="8" className="px-6 py-4 text-center text-gray-500">
                    Nenhuma violação encontrada
                  </td>
                </tr>
              ) : (
                filteredViolations.map((violation) => (
                  <tr key={violation.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {violation.resident_name || 'N/A'}
                        </div>
                        <div className="text-sm text-gray-500">
                          Prédio {violation.resident_building}, Apt {violation.resident_apartment}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {violation.violation_type || 'N/A'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 max-w-xs">
                      <div className="truncate" title={violation.description}>
                        {violation.description || 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSeverityColor(violation.severity)}`}>
                        {getSeverityText(violation.severity)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {getStatusIcon(violation.status)}
                        <span className="ml-2 text-sm text-gray-900">
                          {getStatusText(violation.status)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {violation.fine_amount ? formatCurrency(violation.fine_amount) : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(violation.reported_date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-blue-600 border-blue-600 hover:bg-blue-50"
                          onClick={() => handleEdit(violation)}
                        >
                          <Edit className="h-3 w-3 mr-1" />
                          Editar
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="text-red-600 border-red-600 hover:bg-red-50"
                          onClick={() => handleDelete(violation.id)}
                        >
                          <Trash2 className="h-3 w-3 mr-1" />
                          Excluir
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
      {showEditForm && editingViolation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Editar Violação</h3>
              <Button variant="ghost" size="sm" onClick={() => setShowEditForm(false)}>
                <X className="w-4 h-4" />
              </Button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tipo de Violação *
                </label>
                <input
                  type="text"
                  required
                  value={formData.violation_type}
                  onChange={(e) => setFormData({ ...formData, violation_type: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descrição *
                </label>
                <textarea
                  required
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Local
                </label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gravidade
                  </label>
                  <select
                    value={formData.severity}
                    onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="low">Baixa</option>
                    <option value="medium">Média</option>
                    <option value="high">Alta</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="open">Aberta</option>
                    <option value="pending">Pendente</option>
                    <option value="in_progress">Em Andamento</option>
                    <option value="resolved">Resolvida</option>
                    <option value="closed">Fechada</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Valor da Multa (R$)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.fine_amount}
                    onChange={(e) => setFormData({ ...formData, fine_amount: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
                
                <div className="flex items-center pt-6">
                  <input
                    type="checkbox"
                    id="fine_paid"
                    checked={formData.fine_paid}
                    onChange={(e) => setFormData({ ...formData, fine_paid: e.target.checked })}
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                  <label htmlFor="fine_paid" className="ml-2 block text-sm text-gray-900">
                    Multa paga
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Observações
                </label>
                <textarea
                  rows={2}
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              
              <div className="flex space-x-3 pt-4">
                <Button type="submit" className="flex-1 bg-green-600 hover:bg-green-700">
                  Salvar Alterações
                </Button>
                <Button type="button" variant="outline" onClick={() => setShowEditForm(false)}>
                  Cancelar
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Violations

