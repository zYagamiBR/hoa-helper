import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Users, Plus, Search, Edit, Trash2, Upload } from 'lucide-react';
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
