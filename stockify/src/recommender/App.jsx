import { useState } from 'react'
import Navbar from '../components/navbar'
import StockInput from '../components/stock_input'




function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Navbar/>

     <StockInput/>
    
    
   
    </>
  )
}

export default App
