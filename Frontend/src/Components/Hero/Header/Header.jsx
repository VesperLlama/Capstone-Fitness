import React, { useState } from "react";
import "./Header.css";
import Logo from "./VIFNXlogo.webp";
import Bars from "../../../assets/bars.png";
import { Link } from "react-scroll";
import { Link as LinkRoute } from "react-router-dom";
import Modal from "@mui/material/Modal";
import SignIn from "../../Account/SignIn";
import SignUp from "../../Account/SignUp";

const Header = () => {
  const mobile = window.innerWidth <= 768 ? true : false;
  const [menuOpened, setMenuOpened] = useState(false);
  const [modal, setModal] = useState(false);
  const [isSignIn, setIsSignIn] = useState(true);
  const handleOpen = () => setModal(true);
  const handleClose = () => setModal(false);
  const switchToSignUp = () => setIsSignIn(false);
  const switchToSignIn = () => setIsSignIn(true);

  return (
    <div className="header">
      <Modal open={modal} onClose={handleClose}>
        <div onClick={(e) => e.stopPropagation()}>
          {isSignIn ? <SignIn switchToSignUp={switchToSignUp} /> : <SignUp switchToSignIn={switchToSignIn} />}
        </div>
      </Modal>
      <img src={Logo} alt="" className="logo" />
      {menuOpened === false && mobile === true ? (
        <div
          style={{
            backgroundColor: "var(--appColor)",
            padding: "0.5rem",
            borderRadius: "5px",
          }}
          onClick={() => setMenuOpened(true)}
        >
          <img
            src={Bars}
            alt=""
            style={{ width: "1.5rem", height: "1.5rem" }}
          />
        </div>
      ) : (
        <ul className="header-menu">
          <li>
            <Link
              onClick={() => setMenuOpened(false)}
              to="home"
              span={true}
              smooth={true}
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              onClick={() => setMenuOpened(false)}
              to="programs"
              span={true}
              smooth={true}
            >
              Programs
            </Link>
          </li>

          <li>
            <Link
              onClick={() => setMenuOpened(false)}
              to="reasons"
              span={true}
              smooth={true}
            >
              Why us
            </Link>
          </li>
          <li>
            <Link
              onClick={() => setMenuOpened(false)}
              to="PLANs"
              span={true}
              smooth={true}
            >
              Plans
            </Link>
          </li>
          <li>
            <Link
              onClick={() => setMenuOpened(false)}
              to="Testimonials"
              span={true}
              smooth={true}
            >
              Clients
            </Link>
          </li>
          <li>
            <LinkRoute className="LinkRoute" to="/Exercise">
              Exercise
            </LinkRoute>
          </li>
          <li>
            <Link onClick={handleOpen}>Sign In</Link>
          </li>
        </ul>
      )}
    </div>
  );
};

export default Header;
