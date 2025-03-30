import React, { useLayoutEffect } from "react";
import "./CVModels.css";
import { Tabs, Tab, Box } from "@mui/material";
import { Link, Outlet } from "react-router-dom";
import { useLocation } from "react-router-dom";

const CVTabs = () => {
  const location = useLocation();

  useLayoutEffect(() => {
    window.scroll({top: 0, left: 0, behavior: 'instant'});
  });

  return (
    <Box>
      <Tabs
        value={location.pathname}
        textColor="inherit"
        indicatorColor="secondary"
        sx={{
          "& .MuiTab-root": { color: "white", fontSize: "larger" },
          "& .Mui-selected": { color: "var(--orange)" },
          "& .MuiTabs-indicator": { backgroundColor: "var(--orange)" },
        }}
        centered
      >
        <Tab label="Dumbell" value="/exercise/dumbell" LinkComponent={Link} to="/exercise/dumbell" />
        <Tab label="Shoulder Press" value="/exercise/shld" LinkComponent={Link} to="/exercise/shld" />
        <Tab label="Push Up" value="/exercise/pushup" LinkComponent={Link} to="/exercise/pushup" />
        <Tab label="Squats" value="/exercise/squats" LinkComponent={Link} to="/exercise/squats"/>
      </Tabs>
      <Outlet />
    </Box>
  );
};

export default CVTabs;
