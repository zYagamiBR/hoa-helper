import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Users, 
  Building, 
  DollarSign, 
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Calendar,
  Wrench,
  FileText,
  PiggyBank
} from 'lucide-react'

const API_BASE_URL = 'https://xlhyimc3nd7n.manus.space/api'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalResidents: 0,
    totalVendors: 0,
    monthlyRevenue: 0,
    openViolations: 0,
    pendingMaintenance: 0,
    upcomingEvents: 0,
    unpaidInvoices: 0,
    collectionRate: 0
  })
  const [loading, setLoading] = useState(true)
  const [recentMaintenance, setRecentMaintenance] = useState([])
  const [upcomingEvents, setUpcomingEvents] = useState([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      console.log('Dashboard: Starting to fetch data...')
      
      // Initialize with default values in case of API failures
      let residents = []
      let vendors = []
      let payments = []
      let invoices = []
      let maintenance = []
      let events = []
      let violations = []
      let associates = []
      let bills = []
      
      // Fetch all data sequentially with better error handling
      try {
        console.log('Dashboard: Fetching residents...')
        const residentsRes = await fetch(`${API_BASE_URL}/users`)
        if (residentsRes.ok) {
          residents = await residentsRes.json()
          console.log('Dashboard: Residents fetched:', residents.length)
        } else {
          console.error('Dashboard: Failed to fetch residents:', residentsRes.status)
        }
      } catch (error) {
        console.error('Dashboard: Error fetching residents:', error)
      }

      try {
        console.log('Dashboard: Fetching vendors...')
        const vendorsRes = await fetch(`${API_BASE_URL}/vendors`)
        if (vendorsRes.ok) {
          vendors = await vendorsRes.json()
          console.log('Dashboard: Vendors fetched:', vendors.length)
        } else {
          console.error('Dashboard: Failed to fetch vendors:', vendorsRes.status)
        }
      } catch (error) {
        console.error('Dashboard: Error fetching vendors:', error)
      }

      try {
        const paymentsRes = await fetch(`${API_BASE_URL}/payments`)
        if (paymentsRes.ok) {
          payments = await paymentsRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching payments:', error)
      }

      try {
        const invoicesRes = await fetch(`${API_BASE_URL}/invoices`)
        if (invoicesRes.ok) {
          invoices = await invoicesRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching invoices:', error)
      }

      try {
        const maintenanceRes = await fetch(`${API_BASE_URL}/maintenance`)
        if (maintenanceRes.ok) {
          maintenance = await maintenanceRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching maintenance:', error)
      }

      try {
        const eventsRes = await fetch(`${API_BASE_URL}/events`)
        if (eventsRes.ok) {
          events = await eventsRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching events:', error)
      }

      try {
        const violationsRes = await fetch(`${API_BASE_URL}/violations`)
        if (violationsRes.ok) {
          violations = await violationsRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching violations:', error)
      }

      try {
        const associatesRes = await fetch(`${API_BASE_URL}/associates`)
        if (associatesRes.ok) {
          associates = await associatesRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching associates:', error)
      }

      try {
        const billsRes = await fetch(`${API_BASE_URL}/bills`)
        if (billsRes.ok) {
          bills = await billsRes.json()
        }
      } catch (error) {
        console.error('Dashboard: Error fetching bills:', error)
      }

      // Calculate real metrics
      const totalResidents = residents.length
      const totalVendors = vendors.length
      
      // Calculate total revenue from ALL payments + violation fines
      const totalPayments = payments.reduce((sum, payment) => sum + (parseFloat(payment.amount) || 0), 0)
      const totalFines = violations.reduce((sum, violation) => sum + (parseFloat(violation.fine_amount) || 0), 0)
      const monthlyRevenue = totalPayments + totalFines

      // Calculate monthly costs (employees + maintenance + invoices + bills)
      const employeeCosts = associates.reduce((sum, associate) => sum + (parseFloat(associate.salary) || 1500), 0) // Default R$1500 if no salary
      const maintenanceCosts = maintenance.reduce((sum, req) => sum + (parseFloat(req.actual_cost) || parseFloat(req.estimated_cost) || 0), 0)
      const invoiceCosts = invoices.reduce((sum, invoice) => sum + (parseFloat(invoice.amount) || 0), 0)
      const billsCosts = bills.filter(bill => bill.status === 'active').reduce((sum, bill) => {
        // Calculate monthly equivalent based on frequency
        const amount = parseFloat(bill.amount) || 0
        switch(bill.frequency) {
          case 'monthly': return sum + amount
          case 'quarterly': return sum + (amount / 3)
          case 'semi-annual': return sum + (amount / 6)
          case 'yearly': return sum + (amount / 12)
          default: return sum + amount
        }
      }, 0)
      const monthlyCosts = employeeCosts + maintenanceCosts + invoiceCosts + billsCosts

      // Calculate profit (revenue - costs)
      const monthlyProfit = monthlyRevenue - monthlyCosts

      // Calculate savings (accumulated profits - for now same as profit)
      const totalSavings = monthlyProfit > 0 ? monthlyProfit : 0

      // Count pending maintenance (open or in progress)
      const pendingMaintenance = maintenance.filter(req => 
        req.status === 'open' || req.status === 'in_progress' || req.status === 'Open' || req.status === 'In Progress'
      ).length

      // Count open violations
      const openViolations = violations.filter(violation => 
        violation.status === 'open' || violation.status === 'pending' || violation.status === 'Open' || violation.status === 'Pending'
      ).length

      // Count upcoming events (future events)
      const now = new Date()
      const upcomingEventsCount = events.filter(event => {
        const eventDate = new Date(event.event_date || event.date)
        return eventDate > now
      }).length

      // Count unpaid invoices
      const unpaidInvoices = invoices.filter(invoice => 
        invoice.status === 'pending' || invoice.status === 'overdue' || invoice.status === 'Pending' || invoice.status === 'Overdue'
      ).length

      // Calculate collection rate (paid invoices / total invoices)
      const paidInvoices = invoices.filter(invoice => 
        invoice.status === 'paid' || invoice.status === 'Paid'
      ).length
      const collectionRate = invoices.length > 0 ? ((paidInvoices / invoices.length) * 100) : 100

      console.log('Dashboard: Calculated stats:', {
        totalResidents,
        totalVendors,
        monthlyRevenue,
        openViolations,
        pendingMaintenance,
        upcomingEventsCount,
        unpaidInvoices,
        collectionRate
      })

      setStats({
        totalResidents,
        totalVendors,
        monthlyRevenue,
        monthlyCosts,
        monthlyProfit,
        totalSavings,
        openViolations,
        pendingMaintenance,
        upcomingEvents: upcomingEventsCount,
        unpaidInvoices,
        collectionRate: Math.round(collectionRate * 10) / 10 // Round to 1 decimal
      })

      // Set recent maintenance (last 3)
      const sortedMaintenance = maintenance
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 3)
      setRecentMaintenance(sortedMaintenance)

      // Set upcoming events (next 3)
      const sortedEvents = events
        .filter(event => new Date(event.event_date || event.date) > now)
        .sort((a, b) => new Date(a.event_date || a.date) - new Date(b.event_date || b.date))
        .slice(0, 3)
      setUpcomingEvents(sortedEvents)

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: 'Monthly Revenue',
      value: `R$ ${stats.monthlyRevenue?.toLocaleString('pt-BR', {minimumFractionDigits: 2}) || '0,00'}`,
      icon: DollarSign,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-100'
    },
    {
      title: 'Monthly Costs',
      value: `R$ ${stats.monthlyCosts?.toLocaleString('pt-BR', {minimumFractionDigits: 2}) || '0,00'}`,
      icon: TrendingDown,
      color: 'text-red-600',
      bgColor: 'bg-red-100'
    },
    {
      title: 'Profit',
      value: `R$ ${stats.monthlyProfit?.toLocaleString('pt-BR', {minimumFractionDigits: 2}) || '0,00'}`,
      icon: TrendingUp,
      color: stats.monthlyProfit >= 0 ? 'text-green-600' : 'text-red-600',
      bgColor: stats.monthlyProfit >= 0 ? 'bg-green-100' : 'bg-red-100'
    },
    {
      title: 'Savings',
      value: `R$ ${stats.totalSavings?.toLocaleString('pt-BR', {minimumFractionDigits: 2}) || '0,00'}`,
      icon: PiggyBank,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    }
  ]

  const operationalCards = [
    {
      title: 'Total Residents',
      value: stats.totalResidents,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Active Vendors',
      value: stats.totalVendors,
      icon: Building,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Collection Rate',
      value: `${stats.collectionRate}%`,
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      title: 'Upcoming Events',
      value: stats.upcomingEvents,
      icon: Calendar,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100'
    }
  ]

  const alertCards = [
    {
      title: 'Pending Maintenance',
      value: stats.pendingMaintenance,
      icon: Wrench,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    },
    {
      title: 'Open Violations',
      value: stats.openViolations,
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-100'
    },
    {
      title: 'Unpaid Invoices',
      value: stats.unpaidInvoices,
      icon: FileText,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100'
    },
    {
      title: 'Upcoming Events',
      value: stats.upcomingEvents,
      icon: Calendar,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100'
    }
  ]

  const formatDate = (dateString) => {
    if (!dateString) return 'No Data'
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString()
  }

  const formatEventDate = (dateString) => {
    if (!dateString) return 'No Data'
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = date - now
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Tomorrow'
    if (diffDays < 7) return `In ${diffDays} days`
    return date.toLocaleDateString()
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-600 mt-2">Overview of your HOA management system</p>
      </div>

      {/* Key Metrics */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((stat, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
                  </div>
                  <div className={`p-3 rounded-full ${stat.bgColor}`}>
                    <stat.icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Alerts & Actions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Alerts & Actions Required</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {alertCards.map((alert, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-200 border-l-4 border-l-gray-300">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{alert.title}</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">{alert.value}</p>
                  </div>
                  <div className={`p-3 rounded-full ${alert.bgColor}`}>
                    <alert.icon className={`w-6 h-6 ${alert.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Maintenance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentMaintenance.length > 0 ? recentMaintenance.map((request, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">
                      {request.resident_name ? `${request.resident_name} - Unit ${request.resident_unit}` : `Unit ${request.resident_unit || 'Unknown'}`}
                    </p>
                    <p className="text-sm text-gray-600">{request.title || request.description}</p>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      request.priority === 'High' ? 'bg-red-100 text-red-800' :
                      request.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {request.priority || 'Medium'}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">{formatDate(request.created_at)}</p>
                  </div>
                </div>
              )) : (
                <p className="text-gray-500 text-center py-4">No recent maintenance requests</p>
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Upcoming Events</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {upcomingEvents.length > 0 ? upcomingEvents.map((event, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{event.title || event.name}</p>
                    <p className="text-sm text-gray-600">{event.location || 'Location TBD'}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{formatEventDate(event.event_date || event.date)}</p>
                  </div>
                </div>
              )) : (
                <p className="text-gray-500 text-center py-4">No upcoming events</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

