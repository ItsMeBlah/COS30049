import React from "react"; 
import { Link } from "react-router-dom";
import Logo from "../Logo/Logo"; 
import './Footer.css'

function Footer() {

  return (
    <footer className="footer">
        <div className="footer-container footer-container-top">
            <Link className="footer-title" to="/home">
                <Logo />
            </Link>
        </div>
        <div className="footer-container footer-container-middle">
            <Link to="/home">Home</Link>
            <Link to="/about">About</Link>
            <Link to="/prediction">Prediction</Link>
        </div>
        <div className="footer-container footer-container-bottom">
          <p className="footer-subtitle">© Vanga Realestate</p>
        </div>
    </footer>
  )
}

export default Footer