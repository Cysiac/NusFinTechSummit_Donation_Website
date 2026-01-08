
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home'
import Layout from './layout';
import {useState} from 'react';
import CausePage from './CausePage';
import Page from './page'
function App() {
let causesList = [
{
    id:1,
    title: 'Feeding Communities',
    imgUrl: 'https://th.bing.com/th/id/OIP.8aKFGdMRinYFcoUbARV7zwHaMI?w=118&h=193&c=7&r=0&o=7&dpr=2&pid=1.7&rm=3',
    description : 'Basic necessities and nutrition for the underpriviledged in third world countries ',
    amount : 2000,
    amountFilled : 10,
    //include wallet key of person we donate to -> passed to donation page 


},
{
    id:2,
    title: 'Scholarships for underpriviledged chidren',
    imgUrl: 'https://th.bing.com/th/id/OIP.nssvrbL1GTBirYW8zTsO2wHaDy?w=349&h=178&c=7&r=0&o=7&dpr=2&pid=1.7&rm=3',
    description : 'School fees for children of lower income families that cannot afford to pay their full tution fee.',
    amount : 100000,
    amountFilled : 10
},
{
id:3,
    title: 'Urgent Homelessness Relief',
    imgUrl: 'https://th.bing.com/th/id/OIP.LmSO6fRCE3HuW1D_a4JAmwHaE8?w=253&h=180&c=7&r=0&o=7&dpr=2&pid=1.7&rm=3',
    description : 'Funds for homeless shelters to expand operations and increase their intake, providing shelter for thousands of the homeless',
    amount: 15000,
    amountFilled : 10
}
]
  return (
 
    <Router>
      <Routes>
        {/* Main routes */}
        <Route path="/" element={<Home causesList={causesList}/>} />
        <Route path="/causes" element={<CausePage />} />
        <Route path="/causes/:id" element={<CausePage />} />
        
        {/* Your Next.js converted pages */}
        <Route path="/layout-page" element={<Layout />} />
        <Route path="/special-page" element={<Page />} />
        
        {/* 404 route */}
        <Route path="*" element={
          <div style={{ padding: '20px' }}>
            <h1>404 - Page Not Found</h1>
            <a href="/">Go Home</a>
          </div>
        } />
      </Routes>
    </Router>
  );

 
}

export default App;
