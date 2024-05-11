import { useState } from 'react'
import Navbar from '../components/navbar'
import predictInput from '../components/predict_input'




function App() {
  const [count, setCount] = useState(0)

  return (
    <>
     <Navbar/>
        
        <predictInput/>
    
    </>
  )
}

export default App
