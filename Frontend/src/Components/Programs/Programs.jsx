import React from 'react'
import './Programs.css'
import {programsData} from '../../data/programsData';
import RightArrow from '../../assets/rightArrow.png'
import { useNavigate } from 'react-router-dom';

const Programs = () => {
    const navigate = useNavigate();
  return (
    <div className="Programs" id="programs">
        {/* Header */}
        <div className="programs-header">
            <span className='stroke-text'>Explore our</span>
            <span>Fit AI</span>
            <span className='stroke-text'>Models</span>
        </div>

        <div className="program-categories">
            {programsData.map((program) => (
                <div className="category" onClick={() => navigate(`exercise/${program.url}`)}>
                    {program.image}
                    <span>{program.heading}</span>
                    <span>{program.details}</span>
                    <div className="join-now"><span>Join Now</span><img src={RightArrow} alt='' /></div>
                </div>
            ))}
        </div>
    </div>
  )
}

export default Programs