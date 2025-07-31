import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Users, Plus, Search, Edit, Trash2, Upload, Download } from 'lucide-react';
import ImportExportModal from './ImportExportModal';

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Residents = () => {
  const [residents, setResidents] = useState([]);
  const [buildings, setBuildings] = useState([]);
  const [apartments, setApartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingResident, setEditingResident] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showImportExport, setShowImportExport] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    building: '',
    apartment: '',
    phone: ''
  });

  useEffect(() => {
    fetchResidents();
    fetchBuildings();
    fetchApartments();
  }, []);

  const fetchResidents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/users`);
      if (response.ok) {
        const data = await response.json();
        setResidents(data);
      }
    } catch (error) {
      console.error('Error fetching residents:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchBuildings = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/buildings`);
      if (response.ok) {
        const data = await response.json();
        setBuildings(data);
      }
    } catch (error) {
      console.error('Error fetching buildings:', error);
    }
  };

  const fetchApartments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/apartments`);
      if (response.ok) {
        const data = await response.json();
        setApartments(data);
      }
    } catch (error) {
      console.error('Error fetching apartments:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = editingResident 
        ? `${API_BASE_URL}/api/users/${editingResident.id}`
        : `${API_BASE_URL}/api/users`;
      
      const method = editingResident ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        fetchResidents();
        resetForm();
      } else {
        const error = await response.json();
        alert('Error saving resident: ' + (error.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error saving resident:', error);
      alert('Error saving resident');
    }
  };

  const handleEdit = (resident) => {
    setEditingResident(resident);
    setFormData({
      name: resident.name,
      email: resident.email,
      building: resident.building,
      apartment: resident.apartment,
      phone: resident.phone || ''
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this resident?')) {
      try {
        const response = await fetch(`${API_BASE_URL}/users/${id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchResidents();
        } else {
          alert('Error deleting resident');
        }
      } catch (error) {
        console.error('Error deleting resident:', error);
        alert('Error deleting resident');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      building: '',
      apartment: '',
      phone: ''
    });
    setEditingResident(null);
    setShowForm(false);
  };

  const filteredResidents = residents.filter(resident =>
    resident.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    resident.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (resident.building && resident.building.toString().includes(searchTerm)) ||
    (resident.apartment && resident.apartment.toString().includes(searchTerm))
  );

  const getBuildingDisplay = (building) => {
    return building ? `BL${building.toString().padStart(2, '0')}` : '';
  };

  const getApartmentDisplay = (apartment) => {
    return apartment ? `AP${apartment}` : '';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Residents</h1>
          <p className="text-gray-600">Manage HOA residents and their information</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowImportExport(true)}
            className="inline-flex items-center px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Upload className="w-4 h-4 mr-2" />
            Import/Export
          </button>
          <button
            onClick={() => setShowForm(true)}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Resident
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Users className="w-8 h-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Residents</p>
              <p className="text-2xl font-bold text-gray-900">{residents.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Users className="w-8 h-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Residents</p>
              <p className="text-2xl font-bold text-gray-900">{residents.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Users className="w-8 h-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Occupancy Rate</p>
              <p className="text-2xl font-bold text-gray-900">
                {((residents.length / 800) * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search residents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Residents Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Building
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Apartment
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Phone
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredResidents.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                    No residents found
                  </td>
                </tr>
              ) : (
                filteredResidents.map((resident) => (
                  <tr key={resident.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {resident.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {getBuildingDisplay(resident.building)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {getApartmentDisplay(resident.apartment)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{resident.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{resident.phone || '-'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleEdit(resident)}
                          className="text-blue-600 hover:text-blue-900 transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(resident.id)}
                          className="text-red-600 hover:text-red-900 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add/Edit Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
            <div className="flex items-center justify-between p-6 border-b">
              <h3 className="text-lg font-medium text-gray-900">
                {editingResident ? 'Edit Resident' : 'Add Resident'}
              </h3>
              <button
                onClick={resetForm}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Building *
                </label>
                <select
                  required
                  value={formData.building}
                  onChange={(e) => setFormData({...formData, building: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select a building...</option>
                  {Array.from({length: 50}, (_, i) => i + 1).map(num => (
                    <option key={num} value={num}>
                      BL{num.toString().padStart(2, '0')}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Apartment *
                </label>
                <select
                  required
                  value={formData.apartment}
                  onChange={(e) => setFormData({...formData, apartment: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select an apartment...</option>
                  {[101, 102, 103, 104, 201, 202, 203, 204, 301, 302, 303, 304, 401, 402, 403, 404].map(apt => (
                    <option key={apt} value={apt}>
                      AP{apt}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Phone
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  {editingResident ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Import/Export Modal */}
      <ImportExportModal
        isOpen={showImportExport}
        onClose={() => setShowImportExport(false)}
        entityName="residents"
        entityDisplayName="Residents"
        apiBaseUrl={API_BASE_URL}
      />
    </div>
  );
};

export default Residents;