import type { FC } from 'react'
import { Outlet } from 'react-router-dom'

interface LayoutProps {}

const Layout: FC<LayoutProps> = () => {
  return (
    <div>
      <h1>WebApp</h1>
      <Outlet />
    </div>
  )
}

export default Layout
