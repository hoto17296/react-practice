export default async function fetchJSON<T>(
  input: string, // Request or URL object is not supported
  data?: any,
  init?: RequestInit
): Promise<T> {
  if (input.substring(0, 1) === '/') {
    input = import.meta.env.VITE_API_BASE + input
  }
  init ||= {} as RequestInit
  if (data) {
    init.method ||= 'POST'
    init.headers ||= { 'Content-Type': 'application/json' }
    init.body ||= JSON.stringify(data)
  }
  const response = await fetch(input, init)
  if (!response.ok) throw response
  return (await response.json()) as T
}
