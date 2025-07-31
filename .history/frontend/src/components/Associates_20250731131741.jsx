import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { UserCheck, Plus, Search, Edit, Trash2, Upload, Download } from 'lucide-react';
import ImportExportModal from './ImportExportModal';

const API_BASE_URL = import.meta.env.VITE_API_URL;

const Associates = () => {
  const [associates, setAssociates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingAssociate, setEditingAssociate] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showImportExport, setShowImportExport] = useState(false);
  const [activeTab, setActiveTab] = useState('personal');
  const [formData, setFormData] = useState({
    // Personal Information
    name: '',
    email: '',
    phone: '',
    mobile: '',
    address: '',
    birth_date: '',
    cpf: '',
    rg: '',
    nationality: '',
    marital_status: '',
    
    // Employment Details
    employee_id: '',
    department: '',
    work_area: '',
    position: '',
    hire_date: '',
    contract_type: '',
    work_schedule: '',
    status: 'Active',
    
    // Financial Information
    monthly_salary: '',
    payment_method: '',
    bank_name: '',
    bank_agency: '',
    bank_account: '',
    pix_key: '',
    
    // Emergency Contact
    emergency_name: '',
    emergency_relationship: '',
    emergency_phone: '',
    emergency_address: '',
    
    // Additional Information
    education_level: '',
    certifications: '',
    skills: '',
    languages: '',
    performance_rating: '',
    last_evaluation: '',
    notes: ''
  });

  useEffect(() => {
    fetchAssociates();
  }, []);

  const fetchAssociates = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/associates`);
      if (response.ok) {
        const data = await response.json();
        setAssociates(data);
      }
    } catch (error) {
      console.error('Error fetching associates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = editingAssociate 
        ? `${API_BASE_URL}/api/associates/${editingAssociate.id}`
        : `${API_BASE_URL}/api/associates`;
      
      const method = editingAssociate ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        fetchAssociates();
        resetForm();
      } else {
        const error = await response.json();
        alert('Error saving associate: ' + (error.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error saving associate:', error);
      alert('Error saving associate');
    }
  };

  const handleEdit = (associate) => {
    setEditingAssociate(associate);
    setFormData({
      name: associate.name || '',
      email: associate.email || '',
      phone: associate.phone || '',
      mobile: associate.mobile || '',
      address: associate.address || '',
      birth_date: associate.birth_date || '',
      cpf: associate.cpf || '',
      rg: associate.rg || '',
      nationality: associate.nationality || '',
      marital_status: associate.marital_status || '',
      employee_id: associate.employee_id || '',
      department: associate.department || '',
      work_area: associate.work_area || '',
      position: associate.position || '',
      hire_date: associate.hire_date || '',
      contract_type: associate.contract_type || '',
      work_schedule: associate.work_schedule || '',
      status: associate.status || 'Active',
      monthly_salary: associate.monthly_salary || '',
      payment_method: associate.payment_method || '',
      bank_name: associate.bank_name || '',
      bank_agency: associate.bank_agency || '',
      bank_account: associate.bank_account || '',
      pix_key: associate.pix_key || '',
      emergency_name: associate.emergency_name || '',
      emergency_relationship: associate.emergency_relationship || '',
      emergency_phone: associate.emergency_phone || '',
      emergency_address: associate.emergency_address || '',
      education_level: associate.education_level || '',
      certifications: associate.certifications || '',
      skills: associate.skills || '',
      languages: associate.languages || '',
      performance_rating: associate.performance_rating || '',
      last_evaluation: associate.last_evaluation || '',
      notes: associate.notes || ''
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this associate?')) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/associates/${id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchAssociates();
        } else {
          alert('Error deleting associate');
        }
      } catch (error) {
        console.error('Error deleting associate:', error);
        alert('Error deleting associate');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '', email: '', phone: '', mobile: '', address: '', birth_date: '',
      cpf: '', rg: '', nationality: '', marital_status: '', employee_id: '',
      department: '', work_area: '', position: '', hire_date: '', contract_type: '',
      work_schedule: '', status: 'Active', monthly_salary: '', payment_method: '',
      bank_name: '', bank_agency: '', bank_account: '', pix_key: '', emergency_name: '',
      emergency_relationship: '', emergency_phone: '', emergency_address: '',
      education_level: '', certifications: '', skills: '', languages: '',
      performance_rating: '', last_evaluation: '', notes: ''
    });
    setEditingAssociate(null);
    setShowForm(false);
    setActiveTab('personal');
  };

  const filteredAssociates = associates.filter(associate =>
    associate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (associate.department && associate.department.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (associate.position && associate.position.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const formatSalary = (salary) => {
    if (!salary) return '-';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(salary);
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
          <h1 className="text-2xl font-bold text-gray-900">Associates</h1>
          <p className="text-gray-600">Manage HOA employees and associates</p>
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
            Add Associate
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <UserCheck className="w-8 h-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Associates</p>
              <p className="text-2xl font-bold text-gray-900">{associates.length}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <UserCheck className="w-8 h-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active</p>
              <p className="text-2xl font-bold text-gray-900">
                {associates.filter(a => a.status === 'Active').length}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <UserCheck className="w-8 h-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Departments</p>
              <p className="text-2xl font-bold text-gray-900">
                {new Set(associates.map(a => a.department).filter(Boolean)).size}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <UserCheck className="w-8 h-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Monthly Payroll</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatSalary(associates.reduce((sum, a) => sum + (parseFloat(a.monthly_salary) || 0), 0))}
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
              placeholder="Search associates..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Associates Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Department
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Position
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Salary
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredAssociates.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                    No associates found
                  </td>
                </tr>
              ) : (
                filteredAssociates.map((associate) => (
                  <tr key={associate.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {associate.name}
                      </div>
                      <div className="text-sm text-gray-500">{associate.email}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{associate.department || '-'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{associate.position || '-'}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{formatSalary(associate.monthly_salary)}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        associate.status === 'Active' 
                          ? 'bg-green-100 text-green-800'
                          : associate.status === 'Inactive'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {associate.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleEdit(associate)}
                          className="text-blue-600 hover:text-blue-900 transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(associate.id)}
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

      {/* Import/Export Modal */}
      <ImportExportModal
        isOpen={showImportExport}
        onClose={() => setShowImportExport(false)}
        entityName="associates"
        entityDisplayName="Associates"
        apiBaseUrl={API_BASE_URL}
      />
    </div>
  );
};

export default Associates;

