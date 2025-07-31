# HOA Management System - Setup Instructions

## Prerequisites
- Python 3.11+ 
- Node.js 20+
- npm or yarn

## Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   cd src
   python main.py
   ```
   
   The backend will run on `http://localhost:5002`

## Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Start the frontend development server**
   ```bash
   npm run dev
   ```
   
   The frontend will run on `http://localhost:5173`

## Accessing the Application

1. **Open your browser** and navigate to `http://localhost:5173`
2. **Language switching**: Click the language button in the top-right corner
3. **Navigation**: Use the sidebar menu to access different modules

## New Features

### Enhanced Filtering
- **Payments**: Use the "Filtrar" button to filter by method, status, and type
- **Maintenance**: Use the "Filtrar" button to filter by priority, status, and category
- **Search**: Use the search boxes to find specific records

### Bilingual Support
- **Language Toggle**: Switch between English and Portuguese using the flag button
- **Complete Translation**: All UI elements are fully translated

### Monthly Reports
- **Financial Reports**: Now generated monthly instead of quarterly
- **Transparency Reports**: Now generated monthly instead of quarterly  
- **Annual Reports**: Comparative reports remain annual as requested

## Troubleshooting

### Backend Issues
- Ensure Python 3.11+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the backend is running on port 5002

### Frontend Issues
- Ensure Node.js 20+ is installed
- Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install --legacy-peer-deps`
- Check that the frontend is running on port 5173

### Database Issues
- The application uses the existing database configuration
- Ensure database connectivity is working properly

## Development Notes

### Adding New Filters
To add filters to other modules, follow the pattern used in `Payments.jsx` and `Maintenance.jsx`:

1. Add filter state variables
2. Create filter dropdown components
3. Implement filter logic in the data fetching function
4. Add appropriate translations to both language files

### Adding New Translations
1. Add new keys to `frontend/src/translations/en.js`
2. Add corresponding translations to `frontend/src/translations/pt-br.js`
3. Use the `t()` function in components to access translations

### Report Customization
- Report templates are in `backend/src/services/simple_report_generator.py`
- Monthly reports use the `transparency_monthly` template
- Annual reports use the existing annual template

## Support
The application is now fully functional with all requested enhancements implemented. All modules have been tested and verified to work correctly with the new filtering and translation features.

