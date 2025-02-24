import React from "react";
import "./CVModels.css";
import { Tabs, Tab, Box } from "@mui/material";
import { Link, Outlet } from "react-router-dom";

const CVTabs = () => {
  const [value, setValue] = React.useState(1);

  const handleChange = (e, newValue) => {
    setValue(newValue);
  };

  return (
    <Box>
      <Tabs
        value={value}
        onChange={handleChange}
        textColor="inherit"
        indicatorColor="secondary"
        sx={{
          "& .MuiTab-root": { color: "white", fontSize: "larger" },
          "& .Mui-selected": { color: "#ff9800" },
          "& .MuiTabs-indicator": { backgroundColor: "#ff9800" },
        }}
        centered
      >
        <Tab label="Dumbell" value="0" LinkComponent={Link} to="/train/dumbell" />
        <Tab label="Shoulder Press" value="1" LinkComponent={Link} to="/train/shld" />
        <Tab label="Push Up" value="2" LinkComponent={Link} />
        <Tab label="Squats" value="3" LinkComponent={Link} />
      </Tabs>
      <Outlet />
    </Box>
  );
};

export default CVTabs;
