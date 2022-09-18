import { Component, ReactNode } from 'react'
import { Alert } from '@mui/material'

export default class TopLevelErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode }) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(_error: any) {
    return { hasError: true }
  }

  componentDidMount() {
    window.addEventListener('unhandledrejection', this.onUnhandledRejection)
  }

  componentWillUnmount() {
    window.removeEventListener('unhandledrejection', this.onUnhandledRejection)
  }

  onUnhandledRejection = (event: PromiseRejectionEvent) => {
    event.promise.catch((error) => {
      this.setState(TopLevelErrorBoundary.getDerivedStateFromError(error))
    })
  }

  componentDidCatch(error: any, errorInfo: any) {
    console.error(error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '1em' }}>
          <Alert severity="error">
            Sorry, an unexpected error has occurred.
            <a href="#" onClick={() => location.reload()}>
              Reload
            </a>
          </Alert>
        </div>
      )
    }
    return this.props.children
  }
}
