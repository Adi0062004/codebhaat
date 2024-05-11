import { useState } from 'react'
import Navbar from '../components/navbar'
import About from '../components/home_about'
import Features from '../components/home_features'



function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div>

     <Navbar/>
    <About/>
    </div>
    
    <Features/>
    </>
  )
}

export default App
