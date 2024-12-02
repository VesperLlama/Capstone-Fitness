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
import VideoStream from "./Components/CV/Dumbell";
import { Routes, Route, useLocation } from "react-router-dom";

function App() {
  const location = useLocation();
  const isDumbellPage = location.pathname === "/dumbell";
  const isHomePage = location.pathname === "/";

  return (
    <div className="App">
      <Header />

      <Routes>
        {isDumbellPage && <Route path="/dumbell" element={<VideoStream />} />}
        {isHomePage && (
          <>
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
          </>
        )}
      </Routes>

      <Footer />
    </div>
  );
}

export default App;
