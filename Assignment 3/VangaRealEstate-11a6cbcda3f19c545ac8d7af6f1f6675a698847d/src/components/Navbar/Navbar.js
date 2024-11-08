import React from "react"; 
import { Link } from "react-router-dom";
import Logo from "../Logo/Logo"; 
import './Navbar.css'

function Navbar() {

  return (
    <nav className="nav">
        <div className="nav-container nav-container-left">
            <Link to="/home">
              <Logo />
            </Link>
        </div>
        <div className="nav-container nav-container-right">
            <Link to="/home">Home</Link>
            <Link to="/about">About</Link>
            <Link to="/search">Search</Link>
        </div>
    </nav>
  )
}
export default Navbar