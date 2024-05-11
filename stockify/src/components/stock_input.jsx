import React from 'react'



export default function StockInput() {


    const IncomeRange=["less than 10k","10-50k","50k-3lac","3-10lac","10-50lac","above 50lac"]
    const sectors=["technology","health","entertainment"]
    const targets=["5-10k","10-25k","25k-1lac","1-5lac","more than 5 lac"]
    const investment=["upto 1k","1-5k","5-25k","25k-1lac","1lac-5lac","more than 5 lac"]

  return (
    <>
    <form className='bg-red-950 text-amber-600 p-5 grid justify-center ' 
    >
        <h1 className='text-4xl font-bold pb-10'>Stock Recommender</h1>
        <label >Age</label>
        <input type="number" /><br />
        <label>Income</label>
        <select>
        {IncomeRange.map(item=>(
            <option value={item}>{item}</option>
        ))}
        </select><br />
        <label >Sector</label>
        <select>
        {sectors.map(item=>(
            <option value={item}>{item}</option>
        ))} 
        </select><br />
        <label >Target Income</label>
        <select >
        {targets.map(item=>(
            <option value={item}>{item}</option>
        ))}
        </select><br />
        <label >Time of Investment</label>
        <input type="number"  /><br />
        <label >Investment</label>
        <select >
        {investment.map(item=>(
            <option value={item}>{item}</option>
        ))}
        </select><br />
        <button className='text-red-950 bg-amber-600 w-1/3 hover' type='submit'>submit</button>
    </form>
   
    </>
  );
}


