import { StrictMode } from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { createTheme, ThemeProvider } from '@mui/material/styles'
import TopLevelErrorBoundary from './components/TopLevelErrorBoundary'
import DashboardLayout from './components/DashboardLayout'
import SigninPage from './pages/Signin'

const theme = createTheme()

const router = createBrowserRouter([
  {
    path: 'signin',
    element: <SigninPage />,
  },
  {
    element: <DashboardLayout sitename="WebApp" />,
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
  <StrictMode>
    <TopLevelErrorBoundary>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </TopLevelErrorBoundary>
  </StrictMode>
)
