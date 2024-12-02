import React from 'react'
import './Footer.css'
import Instagram from '../../assets/instagram.png'
import LinkedIn from '../../assets/linkedin.png'
import Github from '../../assets/github.png'
import FitLogo from '../../Components/Hero/Header/VIFNXlogo.webp'

export const Footer = () => {
  return (
    <div className="Footer-container">
        <hr />
      <div className="footer">
           <div className="social-link">
              <img src={Github} alt="" />
              <img src={Instagram} alt="" />
              <img src={LinkedIn} alt="" />
            </div>
            <div className="Logo-f">
                <img src={FitLogo} alt="" />
            </div>
       </div>

         <div className="blur blur-f-1"></div>
         <div className="blur blur-f-2"></div>
    </div>
  )
}
