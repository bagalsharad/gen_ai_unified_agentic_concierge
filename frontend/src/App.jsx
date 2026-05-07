import { useState } from 'react'
import { Send, UtensilsCrossed, Calendar, Users, MapPin, AlertCircle, CheckCircle2 } from 'lucide-react'
import './App.css'

function App() {
  const [intent, setIntent] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!intent.trim()) return

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: "demo_user",
          intent: intent
        })
      })

      if (!response.ok) {
        throw new Error('Failed to communicate with Concierge API')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const renderBookingResult = () => {
    if (!result || !result.response?.recommendations?.length) {
      return (
        <div className="glass-panel results-container animate-slide-up">
          <div className="status-badge error">
            <AlertCircle size={16} />
            <span>Booking Failed or No Safe Recommendations Found</span>
          </div>
          <p style={{ color: 'hsl(var(--text-muted))' }}>
            The concierge agents could not finalize a safe itinerary based on your preferences and the current inventory.
          </p>
        </div>
      )
    }

    const booking = result.response.recommendations[0]
    // The backend booking payload has restaurant_id, platform, party_size, reservation_date
    const dateStr = new Date(booking.reservation_date || booking.time || Date.now()).toLocaleString([], {
      weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    })

    return (
      <div className="glass-panel results-container animate-slide-up">
        <div className="status-badge success">
          <CheckCircle2 size={16} />
          <span>{result.status === 'confirmed' ? 'Reservation Confirmed' : 'Itinerary Proposed'}</span>
        </div>
        
        <div className="booking-card">
          <div className="restaurant-header">
            <span className="platform-tag">via {booking.platform || 'System'}</span>
            <h2>{booking.name || `Restaurant ID: ${booking.restaurant_id}`}</h2>
            {booking.match_reason && <p style={{ color: 'hsl(var(--text-muted))' }}>{booking.match_reason}</p>}
          </div>

          <div className="booking-details">
            <div className="detail-item">
              <Calendar size={24} />
              <div className="detail-text">
                <span>Date & Time</span>
                <strong>{dateStr}</strong>
              </div>
            </div>
            <div className="detail-item">
              <Users size={24} />
              <div className="detail-text">
                <span>Party Size</span>
                <strong>{booking.party_size || '2'} Guests</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      <header className="hero animate-slide-up">
        <h1>Global Dining Concierge</h1>
        <p>Your AI-powered hospitality expert. Discover and book premium dining experiences tailored perfectly to your tastes.</p>
      </header>

      <main className="chat-interface animate-slide-up" style={{ animationDelay: '0.1s' }}>
        <form onSubmit={handleSubmit} className="input-wrapper">
          <input
            type="text"
            className="chat-input"
            placeholder="e.g. I want a Michelin-level Japanese omakase dinner for 2 this Friday..."
            value={intent}
            onChange={(e) => setIntent(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="send-btn" disabled={!intent.trim() || isLoading}>
            <Send size={20} />
          </button>
        </form>

        {isLoading && (
          <div className="loading-indicator animate-slide-up">
            <div className="loader"></div>
            <p>Orchestrating agents across Resy & Tock...</p>
          </div>
        )}

        {error && (
          <div className="glass-panel results-container animate-slide-up" style={{ borderColor: 'hsl(0 70% 30%)' }}>
            <div className="status-badge error">
              <AlertCircle size={16} />
              <span>System Error</span>
            </div>
            <p>{error}</p>
          </div>
        )}

        {!isLoading && result && renderBookingResult()}
      </main>
    </div>
  )
}

export default App
