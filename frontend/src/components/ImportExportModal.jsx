import React, { useState } from 'react';
import { X, Upload, Download, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { useTranslation } from '../translations';

const ImportExportModal = ({ 
  isOpen, 
  onClose, 
  entityName, 
  entityDisplayName,
  apiBaseUrl 
}) => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('import');
  const [importFile, setImportFile] = useState(null);
  const [importResults, setImportResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (!file.name.toLowerCase().endsWith('.csv')) {
        setError('Please select a CSV file');
        return;
      }
      setImportFile(file);
      setError('');
    }
  };

  const handleImport = async () => {
    if (!importFile) {
      setError('Please select a file to import');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', importFile);

      const response = await fetch(`${apiBaseUrl}/import-export/${entityName}/import`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      
      if (response.ok) {
        setImportResults(result);
        setImportFile(null);
        // Reset file input
        const fileInput = document.getElementById('import-file');
        if (fileInput) fileInput.value = '';
      } else {
        setError(result.error || 'Import failed');
      }
    } catch (err) {
      setError('Network error occurred during import');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${apiBaseUrl}/import-export/${entityName}/export`);
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${entityName}_export_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        const result = await response.json();
        setError(result.error || 'Export failed');
      }
    } catch (err) {
      setError('Network error occurred during export');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadTemplate = async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/import-export/${entityName}/template`);
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${entityName}_import_template.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        setError('Failed to download template');
      }
    } catch (err) {
      setError('Network error occurred');
    }
  };

  const resetModal = () => {
    setActiveTab('import');
    setImportFile(null);
    setImportResults(null);
    setError('');
    setIsLoading(false);
  };

  const handleClose = () => {
    resetModal();
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">
            {t('common.importExport')} {entityDisplayName}
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b">
          <button
            onClick={() => setActiveTab('import')}
            className={`flex-1 px-6 py-3 text-sm font-medium ${
              activeTab === 'import'
                ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <Upload className="w-4 h-4 inline-block mr-2" />
            Import Data
          </button>
          <button
            onClick={() => setActiveTab('export')}
            className={`flex-1 px-6 py-3 text-sm font-medium ${
              activeTab === 'export'
                ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <Download className="w-4 h-4 inline-block mr-2" />
            Export Data
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
              <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          )}

          {activeTab === 'import' && (
            <div className="space-y-6">
              {/* Template Download */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-medium text-blue-900 mb-2">
                  {t('common.step1')}: {t('common.downloadTemplate')}
                </h3>
                <p className="text-blue-700 text-sm mb-3">
                  Download the CSV template with the correct column headers for {entityDisplayName.toLowerCase()}.
                </p>
                <button
                  onClick={handleDownloadTemplate}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  {t('common.downloadTemplate')}
                </button>
              </div>

              {/* File Upload */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-2">
                  {t('common.step2')}: {t('common.uploadFile')}
                </h3>
                <p className="text-gray-600 text-sm mb-3">
                  Select your CSV file with {entityDisplayName.toLowerCase()} data to import.
                </p>
                
                <div className="space-y-3">
                  <input
                    id="import-file"
                    type="file"
                    accept=".csv"
                    onChange={handleFileSelect}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  />
                  
                  {importFile && (
                    <div className="text-sm text-gray-600">
                      Selected: {importFile.name} ({(importFile.size / 1024).toFixed(1)} KB)
                    </div>
                  )}
                </div>
              </div>

              {/* Import Button */}
              <div className="flex justify-end">
                <button
                  onClick={handleImport}
                  disabled={!importFile || isLoading}
                  className="inline-flex items-center px-6 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Importing...
                    </>
                  ) : (
                    <>
                      <Upload className="w-4 h-4 mr-2" />
                      Import Data
                    </>
                  )}
                </button>
              </div>

              {/* Import Results */}
              {importResults && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                    <h3 className="font-medium text-green-900">Import Completed</h3>
                  </div>
                  <p className="text-green-700 mb-2">
                    Successfully imported {importResults.imported_count} {entityDisplayName.toLowerCase()}.
                  </p>
                  
                  {importResults.errors && importResults.errors.length > 0 && (
                    <div className="mt-3">
                      <h4 className="font-medium text-orange-900 mb-2">Warnings:</h4>
                      <div className="bg-orange-50 border border-orange-200 rounded p-3 max-h-32 overflow-y-auto">
                        {importResults.errors.map((error, index) => (
                          <div key={index} className="text-sm text-orange-700">
                            {error}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'export' && (
            <div className="space-y-6">
              <div className="text-center">
                <Download className="w-16 h-16 text-blue-500 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Export {entityDisplayName}
                </h3>
                <p className="text-gray-600 mb-6">
                  Download all {entityDisplayName.toLowerCase()} data as a CSV file. This will include all current records with their complete information.
                </p>
                
                <button
                  onClick={handleExport}
                  disabled={isLoading}
                  className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Exporting...
                    </>
                  ) : (
                    <>
                      <Download className="w-5 h-5 mr-2" />
                      Export to CSV
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end px-6 py-4 border-t bg-gray-50">
          <button
            onClick={handleClose}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImportExportModal;

