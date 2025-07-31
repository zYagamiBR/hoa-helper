import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Plus, Search, Calendar, Users, MapPin, Clock, Edit, Trash2, X } from 'lucide-react'
import { useTranslation } from '../translations'

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Events = () => {
  const { t } = useTranslation()
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showEditForm, setShowEditForm] = useState(false)
  const [editingEvent, setEditingEvent] = useState(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    location: '',
    event_date: '',
    end_date: '',
    max_attendees: '',
    cost_per_person: '',
    event_type: '',
    status: 'scheduled'
  })

  useEffect(() => {
    fetchEvents()
  }, [])

  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/events`)
      if (response.ok) {
        const data = await response.json()
        setEvents(data)
      } else {
        console.error('Failed to fetch events')
      }
    } catch (error) {
      console.error('Error fetching events:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (event) => {
    setEditingEvent(event)
    setFormData({
      title: event.title || '',
      description: event.description || '',
      location: event.location || '',
      event_date: event.event_date ? new Date(event.event_date).toISOString().slice(0, 16) : '',
      end_date: event.end_date ? new Date(event.end_date).toISOString().slice(0, 16) : '',
      max_attendees: event.max_attendees || '',
      cost_per_person: event.cost_per_person || '',
      event_type: event.event_type || '',
      status: event.status || 'scheduled'
    })
    setShowEditForm(true)
  }

  const handleDelete = async (eventId) => {
    if (window.confirm(t('events.confirmDelete'))) {
      try {
        const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
          method: 'DELETE'
        })
        if (response.ok) {
          setEvents(events.filter(event => event.id !== eventId))
        } else {
          alert('Erro ao excluir evento')
        }
      } catch (error) {
        console.error('Error deleting event:', error)
        alert('Erro ao excluir evento')
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE_URL}/events/${editingEvent.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      
      if (response.ok) {
        const updatedEvent = await response.json()
        setEvents(events.map(event => 
          event.id === editingEvent.id ? updatedEvent : event
        ))
        setShowEditForm(false)
        setEditingEvent(null)
        resetForm()
      } else {
        alert('Erro ao atualizar evento')
      }
    } catch (error) {
      console.error('Error updating event:', error)
      alert('Erro ao atualizar evento')
    }
  }

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      location: '',
      event_date: '',
      end_date: '',
      max_attendees: '',
      cost_per_person: '',
      event_type: '',
      status: 'scheduled'
    })
  }

  const filteredEvents = events.filter(event =>
    event.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    event.event_type?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const upcomingEvents = events.filter(event => {
    const eventDate = new Date(event.event_date)
    const now = new Date()
    return eventDate > now
  })

  const totalRSVPs = events.reduce((sum, event) => sum + (event.rsvp_count || 0), 0)

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
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
          <div className="text-lg text-gray-600">Carregando eventos...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('events.title')}</h2>
          <p className="text-gray-600">{t('events.subtitle')}</p>
        </div>
        <Button className="bg-orange-600 hover:bg-orange-700">
          <Plus className="h-4 w-4 mr-2" />
          Criar Evento
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Calendar className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('events.totalEvents')}</p>
              <p className="text-2xl font-bold text-gray-900">{events.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Clock className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{t('events.upcomingEvents')}</p>
              <p className="text-2xl font-bold text-gray-900">{upcomingEvents.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Users className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total de Confirmações</p>
              <p className="text-2xl font-bold text-gray-900">{totalRSVPs}</p>
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
            placeholder="Buscar eventos..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEvents.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Nenhum evento encontrado</p>
          </div>
        ) : (
          filteredEvents.map((event) => (
            <div key={event.id} className="bg-white rounded-lg shadow-sm border overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                    {event.title}
                  </h3>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    event.status === 'scheduled' 
                      ? 'bg-green-100 text-green-800'
                      : event.status === 'cancelled'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {event.status === 'scheduled' ? 'Agendado' : 
                     event.status === 'cancelled' ? 'Cancelado' : 'Concluído'}
                  </span>
                </div>

                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                  {event.description || 'Sem descrição disponível'}
                </p>

                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 mr-2" />
                    {formatDate(event.event_date)}
                  </div>
                  
                  {event.location && (
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-2" />
                      {event.location}
                    </div>
                  )}

                  <div className="flex items-center">
                    <Users className="h-4 w-4 mr-2" />
                    {event.rsvp_count || 0} confirmações
                    {event.max_attendees && ` / ${event.max_attendees} vagas`}
                  </div>

                  {event.cost_per_person > 0 && (
                    <div className="flex items-center">
                      <span className="text-green-600 font-medium">
                        {formatCurrency(event.cost_per_person)} por pessoa
                      </span>
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      Tipo: {event.event_type || 'Geral'}
                    </span>
                    <div className="flex space-x-2">
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="text-blue-600 border-blue-600 hover:bg-blue-50"
                        onClick={() => handleEdit(event)}
                      >
                        <Edit className="h-3 w-3 mr-1" />
                        Editar
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline" 
                        className="text-red-600 border-red-600 hover:bg-red-50"
                        onClick={() => handleDelete(event.id)}
                      >
                        <Trash2 className="h-3 w-3 mr-1" />
                        Excluir
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Edit Form Modal */}
      {showEditForm && editingEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Editar Evento</h3>
              <Button variant="ghost" size="sm" onClick={() => setShowEditForm(false)}>
                <X className="w-4 h-4" />
              </Button>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Título *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descrição
                </label>
                <textarea
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Data do Evento *
                  </label>
                  <input
                    type="datetime-local"
                    required
                    value={formData.event_date}
                    onChange={(e) => setFormData({ ...formData, event_date: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Data de Término
                  </label>
                  <input
                    type="datetime-local"
                    value={formData.end_date}
                    onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Local
                </label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tipo de Evento
                  </label>
                  <select
                    value={formData.event_type}
                    onChange={(e) => setFormData({ ...formData, event_type: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  >
                    <option value="">Selecionar</option>
                    <option value="meeting">Reunião</option>
                    <option value="social">Social</option>
                    <option value="maintenance">Manutenção</option>
                    <option value="emergency">Emergência</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Máximo de Participantes
                  </label>
                  <input
                    type="number"
                    value={formData.max_attendees}
                    onChange={(e) => setFormData({ ...formData, max_attendees: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Custo por Pessoa (R$)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.cost_per_person}
                    onChange={(e) => setFormData({ ...formData, cost_per_person: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                >
                  <option value="scheduled">Agendado</option>
                  <option value="completed">Concluído</option>
                  <option value="cancelled">Cancelado</option>
                </select>
              </div>
              
              <div className="flex space-x-3 pt-4">
                <Button type="submit" className="flex-1 bg-orange-600 hover:bg-orange-700">
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

export default Events

