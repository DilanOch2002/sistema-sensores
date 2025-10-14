import { useState, useEffect } from 'react'
import { createClient } from '@supabase/supabase-js'
import './App.css'

const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_KEY
)

function App() {
  const [sensors, setSensors] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSensors()
  }, [])

  const fetchSensors = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data, error } = await supabase
        .from('sensors')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(10)

      if (error) {
        console.error('Error de Supabase:', error)
        setError('Error: ' + error.message)
      } else {
        setSensors(data || [])
        console.log('Datos recibidos:', data)
      }
    } catch (err) {
      console.error('Error general:', err)
      setError('Error general: ' + err.message)
    }
    setLoading(false)
  }

  if (loading) return <div>Cargando sensores...</div>

  return (
    <div className="App">
      <h1>📊 Sistema de Sensores</h1>
      
      {error && (
        <div style={{ color: 'red', margin: '10px 0' }}>
          {error}
        </div>
      )}
      
      <p>Mostrando {sensors.length} sensores más recientes:</p>
      
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Temperatura</th>
            <th>Latitud</th>
            <th>Longitud</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {sensors.map(sensor => (
            <tr key={sensor.id}>
              <td>{sensor.id}</td>
              <td>{sensor.temperature}°C</td>
              <td>{sensor.latitude}</td>
              <td>{sensor.longitude}</td>
              <td>{new Date(sensor.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <button onClick={fetchSensors} style={{marginTop: '20px'}}>
        🔄 Actualizar
      </button>
    </div>
  )
}

export default App