import React from 'react'
import './Plans.css'
import { plansData } from '../../data/plansData';
export const Plans = () => {
  return (
      <div className="plans-container">
        <div className="programs-header" style={{gap: '2rem'}}>
            <span className='stroke-text'>Transform Your Life :</span>
            <span>Choose</span>
            <span className='stroke-text'>Our Diet Plan</span>
        </div>

           {/* Plans card */}
           <div className="plans" id="PLANs">
               {plansData.map((plan, i)=>(
                <div className="plan">
                    {plansData.icon}
                    <span>{plan.name}</span>
                    <span>$ {plan.price}</span>


                    <div className="features">
                        {plan.features.map((features, i)=> (
                           <div className="features">
                                {/* <img src={} alt="" /> */}
                                <span key={i}>{features}</span>
                           </div> 
                        ))}
                    </div>

                    <div>
                        <span>See more benefits  </span>
                    </div>
                        <button className="btn">Best of Luck</button>
                </div>


               ))}
           </div>
      </div>
  );
};


export default Plans;