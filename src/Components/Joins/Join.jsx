import React, { useRef } from 'react'
import './Join.css'
import emailjs from  '@emailjs/browser'
export const Join = () => {
    const form = useRef()

    const sendEmail = (e) => {
        e.preventDefault();
    
        emailjs.sendForm('service_u2swhyn', 'template_l7e8con', form.current, 'GV_m50FUQCaH-3xVj')
          .then((result) => {
              console.log(result.text);
          }, (error) => {
              console.log(error.text);
          });
      };

  return (
    <div className="Join" id="join-us">
         <div className="left-j">
            <hr />
            <div>
                <span>READY FOR A</span>
                <span class='stroke-text'> CHANGE?</span>
            </div>
         </div>

         <div className="right-j">

            <form ref={form}  className="email-container" onSubmit={(e)=>sendEmail(e)}>
                <input type="email" name="user_email" placeholder="Enter your Email address" />  
                <button type='submit' className="btn btn-j">Join Now</button>
            </form>  
         </div>
    </div>
  )
}
