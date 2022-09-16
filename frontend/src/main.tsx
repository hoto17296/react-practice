import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Layout from './components/Layout'

const router = createBrowserRouter([
  {
    path: 'signin',
    element: <div>Sign in</div>,
  },
  {
    element: <Layout />,
    children: [
      {
        path: '',
        element: <div>Home</div>,
      },
      {
        path: 'users',
        children: [
          {
            path: '',
            element: <div>Users</div>,
          },
        ],
      },
      {
        path: '*',
        element: <div>Not Found</div>,
      },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
