import './App.css';
import { Footer } from './Components/Footer/Footer';
import Hero from './Components/Hero/Hero'
import { Join } from './Components/Joins/Join';
import { Plans } from './Components/Plans/Plans';
import Programs from './Components/Programs/Programs';
import Reasons from './Components/Reasons/Reasons';
import { Testimonials } from './Components/Testimonials/Testimonials';
import { Trainers } from './Components/Trainers/Trainers';
function App() {
  return (
    <div className="App">
       <Hero/>
       <Programs/>
       <Reasons/>
       <Plans/>
       <Testimonials/>
       <Trainers/>
       <Join/>
       <Footer/>
    </div>
  );
}

export default App;
