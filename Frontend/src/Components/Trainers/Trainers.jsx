import React from 'react'
import { useState } from 'react';
import './Trainers.css'

import {TrainersData} from "../../data/TrainersData";
import leftArrow from '../../assets/leftArrow.png'
import rightArrow from '../../assets/rightArrow.png'

export const Trainers = () => {
        
    // Using use state hook of the react
         const [selected, setSelected] = useState(0);
         const tLength = TrainersData.length;
  return (
    <div className="Testimonials"> 

    <div className="left-t">
            <span>Personal Trainers</span>
            <span className='stroke-text'>Here's</span>
            <span>You can know about us :-
         </span>
         <span>
            {TrainersData[selected].review}
         </span>
         <span>
              <span style={{color: 'var(--orange)'} }>
                  {TrainersData[selected].name}
              </span>
             - {TrainersData[selected].status}
         </span>
    </div>
      < div className="right-t">
              <div></div>
              <div></div>
             <img src={TrainersData[selected].image} alt="" />

             <div className="arrows">
                  <img 
                  onClick={()=>{
                    selected === 0
                    ? setSelected(tLength-1)
                    : setSelected((prev) => prev - 1);
                  }}
                  src={leftArrow} alt="" />
                 
                 
                  <img
                   onClick={()=>{
                    selected ===tLength -1 
                    ? setSelected(0) 
                    : setSelected((prev) => prev + 1);
                  }}
                  src={rightArrow} alt="" />
             </div>
        </div>
</div>

  );
};

export default Trainers;
