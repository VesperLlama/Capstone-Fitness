import React from "react";
import "./Reasons.css";
import image2 from "./pse2.jpg";
import image3 from "../../assets/image3.png";
import image4 from "../../assets/image4.png";
import tick from "../../assets/tick.png";
const Reasons = () => {
  return (
    <div className="Reasons" id="reasons">
      <div className="left-r">
        <span></span>
        <img src={image2} alt="" />
        <img src={image3} alt="" />
        <img src={image4} alt="" />
      </div>

      <div className="right-r">
        <span> ----Value----</span>

        <div>
          <span className="stroke-text">How </span>
          <span>it adds Value to our Society ?</span>
        </div>

        <div className="details-r">
          <div>
            <img src={tick} alt=""></img>
            <span>WE TRAIN YOUR MIND AND BODY</span>
          </div>
          <div>
            <img src={tick} alt="" />
            <span>
              FitFusion Hub brings a transformative approach to fitness and
              wellness by integrating advanced FIT AI models. Our platform
              provides personalized training experiences that adapt to
              individual needs, helping users achieve their fitness goals more
              effectively. The AI models offer real-time corrections and
              feedback, ensuring proper form and reducing the risk of injury.
              This innovation not only enhances personal health and well-being
              but also promotes a more active and mindful society. By making
              advanced fitness solutions accessible.
            </span>
          </div>
          <div>
            <img src={tick} alt="" />
            <span>RELIABLE PARTNERS</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reasons;
