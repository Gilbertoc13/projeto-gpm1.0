import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

import Home from './routes/Home.jsx'
import Login from './routes/Login.jsx'
import Search from './routes/Search.jsx'
import Error from './routes/Error.jsx'

import { createBrowserRouter, RouterProvider } from 'react-router-dom'

const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login/>,
  },
  {
  path: '/',
  element: <App/>,
  errorElement: <Error/>,
  children: [
    {
      path: '/',
      element: <Home/>
    },
    {
      path: '/search',
      element: <Search/>
    }
  ]
  } 
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
