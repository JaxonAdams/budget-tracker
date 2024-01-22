import { useEffect } from 'react'
import './App.css'

function App() {
  useEffect(() => {
    document.title = "Budget Tracker";
  });

  return (
    <>
      <main>
        <h1>Hello, world!</h1>
      </main>
    </>
  )
}

export default App
