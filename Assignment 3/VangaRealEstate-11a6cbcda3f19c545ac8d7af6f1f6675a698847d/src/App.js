import React from 'react'; 
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './components/Navbar/Navbar.js';
import Home from './pages/Home/Home';
import About from './pages/About/About';
import Search from './pages/Search/Search';
import Prediction from './pages/Prediction/Prediction';
import Footer from './components/Footer/Footer';
import ErrorPage from './pages/Prediction/Error';
import './App.css';

function App() {
  return (
    <BrowserRouter>
    <Navbar />
    <main>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/search" element={<Search />} />
        <Route path="/predict" element={<Prediction />} />
        <Route path="/error" element={<ErrorPage />} /> 
      </Routes>
    </main>
    <Footer />
    </BrowserRouter>
  )
}

export default App; 