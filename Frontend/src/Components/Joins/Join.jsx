import React, { useRef } from "react";
import "./Join.css";
import emailjs from "@emailjs/browser";
export const Join = () => {
  const form = useRef();

  const sendEmail = (e) => {
    e.preventDefault();

    emailjs
      .sendForm(
        "service_u2swhyn",
        "template_l7e8con",
        form.current,
        "GV_m50FUQCaH-3xVj"
      )
      .then(
        (result) => {
          console.log(result.text);
        },
        (error) => {
          console.log(error.text);
        }
      );
  };

  return (
    <div className="Join" id="join-us">
      <div className="left-j">
        <hr />
        <div>
          <span>
            I hated every minute of training, but I said, “Don't quit. Suffer
            now and live the rest of your life as a champion.“
          </span>
          <span className="stroke-text">– Muhammad Ali</span>
        </div>
      </div>
    </div>
  );
};
