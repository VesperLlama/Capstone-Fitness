import "./App.css";
import { Footer } from "./Components/Footer/Footer";
import Header from "./Components/Hero/Header/Header";
import Hero from "./Components/Hero/Hero";
import { Join } from "./Components/Joins/Join";
import { Plans } from "./Components/Plans/Plans";
import Programs from "./Components/Programs/Programs";
import Reasons from "./Components/Reasons/Reasons";
import { Testimonials } from "./Components/Testimonials/Testimonials";
import { Trainers } from "./Components/Trainers/Trainers";
import CVTabs from "./Components/CV/CVModels";
import { Routes, Route } from "react-router-dom";
import Dumbell from "./Components/CV/Dumbell";
import ShldPress from "./Components/CV/Shld_Press";

function App() {
  return (
    <>
      <div className="App">
        <Header />
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Hero />
                <Programs />
                <Reasons />
                <Plans />
                <Testimonials />
                <Trainers />
                <Join />
              </>
            }
          />
          <Route path="/exercise/*" element={<CVTabs />} >
            <Route path="dumbell" element={<Dumbell />} />
            <Route path="shld" element={<ShldPress />} />
          </Route>
        </Routes>

        <Footer />
      </div>
    </>
  );
}

export default App;
