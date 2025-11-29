
import React from 'react'
import { createRoot } from 'react-dom/client'
import Chat from './pages/Chat.jsx'

function App(){ return <Chat /> }

createRoot(document.getElementById('root')).render(<App />)
