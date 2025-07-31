export const en = {
  // Navigation
  nav: {
    dashboard: 'Dashboard',
    residents: 'Residents',
    vendors: 'Vendors',
    payments: 'Payments',
    invoices: 'Invoices',
    bills: 'Bills',
    maintenance: 'Maintenance',
    associates: 'Associates',
    events: 'Events',
    violations: 'Violations',
    reports: 'Reports'
  },

  // Common
  common: {
    welcome: 'Welcome',
    admin: 'Administrator',
    create: 'Create',
    update: 'Update',
    cancel: 'Cancel',
    save: 'Save',
    edit: 'Edit',
    delete: 'Delete',
    search: 'Search',
    filter: 'Filter',
    loading: 'Loading...',
    noData: 'No data available',
    error: 'An error occurred',
    success: 'Operation completed successfully',
    file: 'File',
    importExport: 'Import/Export',
    actions: 'Actions'
  },

  // Dashboard
  dashboard: {
    title: 'Dashboard',
    overview: 'Overview',
    totalResidents: 'Total Residents',
    activeVendors: 'Active Vendors',
    monthlyRevenue: 'Monthly Revenue',
    monthlyCosts: 'Monthly Costs',
    profit: 'Profit',
    savings: 'Savings',
    collectionRate: 'Collection Rate',
    pendingMaintenance: 'Pending Maintenance',
    upcomingEvents: 'Upcoming Events',
    recentViolations: 'Recent Violations',
    overduePayments: 'Overdue Payments',
    alertsActions: 'Alerts & Actions Required',
    viewAll: 'View All',
    noAlerts: 'No alerts at this time'
  },

  // Residents
  residents: {
    title: 'Residents',
    subtitle: 'Manage building residents',
    addResident: 'Add Resident',
    newResident: 'New Resident',
    editResident: 'Edit Resident',
    allResidents: 'All Residents',
    activeResidents: 'Active Residents',
    occupancyRate: 'Occupancy Rate',
    searchPlaceholder: 'Search residents...',
    name: 'Name',
    email: 'Email',
    building: 'Building',
    apartment: 'Apartment',
    unit: 'Unit',
    phone: 'Phone',
    selectBuilding: 'Select a building...',
    selectApartment: 'Select an apartment...',
    noResidents: 'No residents found',
    confirmDelete: 'Are you sure you want to delete this resident?'
  },

  // Vendors
  vendors: {
    title: 'Vendors',
    subtitle: 'Manage service providers',
    addVendor: 'Add Vendor',
    newVendor: 'New Vendor',
    editVendor: 'Edit Vendor',
    allVendors: 'All Vendors',
    totalVendors: 'Total Vendors',
    searchPlaceholder: 'Search vendors...',
    name: 'Company Name',
    email: 'Email',
    phone: 'Phone',
    services: 'Services',
    noVendors: 'No vendors found',
    confirmDelete: 'Are you sure you want to delete this vendor?'
  },

  // Maintenance
  maintenance: {
    title: 'Maintenance',
    subtitle: 'Track maintenance requests',
    newRequest: 'New Request',
    allRequests: 'All Requests',
    searchPlaceholder: 'Search maintenance requests...',
    title_field: 'Title',
    description: 'Description',
    category: 'Category',
    priority: 'Priority',
    status: 'Status',
    resident: 'Resident',
    requestDate: 'Request Date',
    noRequests: 'No maintenance requests found',
    confirmDelete: 'Are you sure you want to delete this maintenance request?',
    // Filters
    filterByPriority: 'Filter by Priority',
    filterByStatus: 'Filter by Status',
    filterByCategory: 'Filter by Category',
    allPriorities: 'All Priorities',
    allStatuses: 'All Statuses',
    allCategories: 'All Categories',
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    open: 'Open',
    pending: 'Pending',
    inProgress: 'In Progress',
    completed: 'Completed',
    electrical: 'Electrical',
    plumbing: 'Plumbing',
    cleaning: 'Cleaning',
    security: 'Security',
    general: 'General'
  },

  // Violations
  violations: {
    title: 'Violations',
    subtitle: 'Track HOA rule violations',
    newViolation: 'New Violation',
    allViolations: 'All Violations',
    searchPlaceholder: 'Search violations...',
    resident: 'Resident',
    description: 'Description',
    violationType: 'Violation Type',
    reportedDate: 'Reported Date',
    noViolations: 'No violations found'
  },

  // Associates
  associates: {
    title: 'Associates Management',
    subtitle: 'Manage HOA employees and associates',
    addAssociate: 'Add Associate',
    newAssociate: 'New Associate',
    editAssociate: 'Edit Associate',
    allAssociates: 'All Associates',
    totalAssociates: 'Total Associates',
    activeEmployees: 'Active Employees',
    searchPlaceholder: 'Search associates...',
    noAssociates: 'No associates registered yet.',
    noAssociatesFound: 'No associates found matching your search.',
    confirmDelete: 'Are you sure you want to delete this associate?',
    
    // Tabs
    tabs: {
      personal: 'Personal',
      employment: 'Employment',
      financial: 'Financial',
      emergency: 'Emergency',
      additional: 'Additional'
    },
    
    // Personal Information
    name: 'Full Name',
    email: 'Email',
    phone: 'Phone',
    mobile: 'Mobile',
    address: 'Address',
    city: 'City',
    state: 'State',
    zipCode: 'ZIP Code',
    birthDate: 'Birth Date',
    cpf: 'CPF',
    rg: 'RG',
    nationality: 'Nationality',
    maritalStatus: 'Marital Status',
    selectMaritalStatus: 'Select marital status...',
    
    // Employment Information
    employeeId: 'Employee ID',
    department: 'Department',
    workArea: 'Work Area',
    position: 'Position',
    hireDate: 'Hire Date',
    contractType: 'Contract Type',
    workSchedule: 'Work Schedule',
    status: 'Status',
    selectDepartment: 'Select department...',
    selectWorkArea: 'Select work area...',
    selectContractType: 'Select contract type...',
    
    // Financial Information
    monthlySalary: 'Monthly Salary',
    paymentMethod: 'Payment Method',
    bankName: 'Bank Name',
    bankAgency: 'Bank Agency',
    bankAccount: 'Bank Account',
    pixKey: 'PIX Key',
    selectPaymentMethod: 'Select payment method...',
    
    // Emergency Contact
    emergencyContactName: 'Emergency Contact Name',
    emergencyContactRelationship: 'Relationship',
    emergencyContactPhone: 'Emergency Contact Phone',
    emergencyContactAddress: 'Emergency Contact Address',
    
    // Additional Information
    educationLevel: 'Education Level',
    certifications: 'Certifications',
    skills: 'Skills',
    languages: 'Languages',
    notes: 'Notes',
    performanceRating: 'Performance Rating',
    lastEvaluationDate: 'Last Evaluation Date',
    selectEducationLevel: 'Select education level...',
    selectPerformanceRating: 'Select performance rating...',
    skillsPlaceholder: 'List relevant skills and competencies...',
    certificationsPlaceholder: 'List certifications, licenses, and qualifications...',
    notesPlaceholder: 'Additional notes and observations...'
  },

  // Footer
  footer: {
    version: 'HOA Management System v1.0'
  },

  // Payments
  payments: {
    title: 'Payments',
    subtitle: 'Manage resident payments',
    addPayment: 'Add Payment',
    newPayment: 'New Payment',
    editPayment: 'Edit Payment',
    allPayments: 'All Payments',
    totalCollected: 'Total Collected',
    paymentsThisMonth: 'Payments This Month',
    totalPayments: 'Total Payments',
    searchPlaceholder: 'Search payments...',
    resident: 'Resident',
    type: 'Type',
    amount: 'Amount',
    method: 'Method',
    date: 'Date',
    status: 'Status',
    completed: 'Completed',
    pending: 'Pending',
    cancelled: 'Cancelled',
    noPayments: 'No payments found',
    confirmDelete: 'Are you sure you want to delete this payment?',
    // Filters
    filterByMethod: 'Filter by Method',
    filterByStatus: 'Filter by Status',
    filterByType: 'Filter by Type',
    allMethods: 'All Methods',
    allStatuses: 'All Statuses',
    allTypes: 'All Types',
    cash: 'Cash',
    creditCard: 'Credit Card',
    debitCard: 'Debit Card',
    bankTransfer: 'Bank Transfer',
    pix: 'PIX',
    check: 'Check'
  },

  // Invoices
  invoices: {
    title: 'Invoices',
    subtitle: 'Manage monthly invoices',
    addInvoice: 'Add Invoice',
    newInvoice: 'New Invoice',
    editInvoice: 'Edit Invoice',
    allInvoices: 'All Invoices',
    searchPlaceholder: 'Search invoices...',
    invoiceNumber: 'Invoice Number',
    resident: 'Resident',
    amount: 'Amount',
    dueDate: 'Due Date',
    status: 'Status',
    paid: 'Paid',
    overdue: 'Overdue',
    noInvoices: 'No invoices found',
    confirmDelete: 'Are you sure you want to delete this invoice?',
    // Filters
    filterByStatus: 'Filter by Status',
    filterByMonth: 'Filter by Month',
    allStatuses: 'All Statuses',
    allMonths: 'All Months'
  },

  // Bills
  bills: {
    title: 'Bills',
    subtitle: 'Manage recurring bills',
    addBill: 'Add Bill',
    newBill: 'New Bill',
    editBill: 'Edit Bill',
    allBills: 'All Bills',
    searchPlaceholder: 'Search bills...',
    name: 'Bill Name',
    category: 'Category',
    amount: 'Amount',
    dueDate: 'Due Date',
    frequency: 'Frequency',
    status: 'Status',
    active: 'Active',
    inactive: 'Inactive',
    noBills: 'No bills found',
    confirmDelete: 'Are you sure you want to delete this bill?',
    // Filters
    filterByCategory: 'Filter by Category',
    filterByStatus: 'Filter by Status',
    filterByFrequency: 'Filter by Frequency',
    allCategories: 'All Categories',
    allStatuses: 'All Statuses',
    allFrequencies: 'All Frequencies',
    monthly: 'Monthly',
    quarterly: 'Quarterly',
    annually: 'Annually'
  },

  // Events
  events: {
    title: 'Events',
    subtitle: 'Manage community events',
    addEvent: 'Add Event',
    newEvent: 'New Event',
    editEvent: 'Edit Event',
    allEvents: 'All Events',
    upcomingEvents: 'Upcoming Events',
    pastEvents: 'Past Events',
    searchPlaceholder: 'Search events...',
    name: 'Event Name',
    description: 'Description',
    date: 'Date',
    time: 'Time',
    location: 'Location',
    capacity: 'Capacity',
    status: 'Status',
    approved: 'Approved',
    pendingApproval: 'Pending Approval',
    rejected: 'Rejected',
    cancelled: 'Cancelled',
    noEvents: 'No events found',
    confirmDelete: 'Are you sure you want to delete this event?',
    // Filters
    filterByStatus: 'Filter by Status',
    filterByDate: 'Filter by Date',
    filterByLocation: 'Filter by Location',
    allStatuses: 'All Statuses',
    allDates: 'All Dates',
    allLocations: 'All Locations',
    future: 'Future',
    past: 'Past',
    today: 'Today'
  },

  // Reports
  reports: {
    title: 'Reports',
    subtitle: 'Generate and distribute transparency reports',
    generateReport: 'Generate Report',
    sendByEmail: 'Send by Email',
    downloadPDF: 'Download PDF',
    lastGenerated: 'Last Generated',
    never: 'Never',
    totalReports: 'Total Reports',
    emailsSent: 'Emails Sent',
    scheduledReports: 'Scheduled Reports',
    nextScheduled: 'Next Scheduled',
    generating: 'Generating...',
    sending: 'Sending...',
    // Report Types
    financialMonthly: 'Monthly Financial Report',
    transparencyMonthly: 'Monthly Transparency Report',
    annualComparative: 'Annual Comparative Report',
    financialMonthlyDesc: 'Revenue vs Expenses with detailed analysis by category',
    transparencyMonthlyDesc: 'Transparency report with expenses by group (Personnel, Utilities, etc.)',
    annualComparativeDesc: 'Financial evolution of the last 5 years with trend analysis',
    monthly: 'Monthly',
    annual: 'Annual',
    // Scheduled Reports
    scheduledReportsTitle: 'Scheduled Reports',
    active: 'Active',
    inactive: 'Inactive',
    everyFirstDay: 'Every 1st of the month at 09:00',
    everyQuarter: 'Every 3 months on the 15th at 10:00'
  },

  // Filters (Common)
  filters: {
    search: 'Search',
    filter: 'Filter',
    clearFilters: 'Clear Filters',
    applyFilters: 'Apply Filters',
    noResults: 'No results found',
    showingResults: 'Showing {count} results',
    // Date filters
    dateRange: 'Date Range',
    from: 'From',
    to: 'To',
    today: 'Today',
    yesterday: 'Yesterday',
    lastWeek: 'Last Week',
    lastMonth: 'Last Month',
    lastYear: 'Last Year',
    custom: 'Custom',
    // Status filters
    current: 'Current',
    past: 'Past',
    active: 'Active',
    inactive: 'Inactive',
    pending: 'Pending',
    approved: 'Approved',
    rejected: 'Rejected'
  }
}

