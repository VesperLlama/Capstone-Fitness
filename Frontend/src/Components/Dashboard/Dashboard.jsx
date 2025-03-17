import React, { useState, useMemo, useEffect } from "react";
import {
  Container,
  Grid2,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  TextField,
} from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { LocalizationProvider, DatePicker } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";

const Dashboard = () => {
  const [exerciseData, setExerciseData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(dayjs());

  useEffect(() => {
    const email = localStorage.getItem("loggedInEmail");

    fetch("http://localhost:8000/getData/" + email, {
      method: "GET",
    }).then(async (res) => {
      if (res.ok) {
        const data = await res.json();
        console.log(data);
        setExerciseData(JSON.parse(data));
      }
    });
  }, []);

  const isSameDay = (date1, date2) => {
    return date1.isSame(date2, "day");
  };

  const overallTotals = useMemo(() => {
    return exerciseData.reduce(
      (totals, record) => {
        totals.count += record.count;
        totals.calories += record.calories;
        return totals;
      },
      { count: 0, calories: 0 }
    );
  }, [exerciseData]);

  const filteredData = useMemo(() => {
    return exerciseData.filter((record) => {
      console.log(record.date.$date);
      const recordDate = dayjs(record.date.$date);
      return isSameDay(recordDate, selectedDate);
    });
  }, [exerciseData, selectedDate]);

  const darkTheme = createTheme({
    palette: {
      mode: "dark",
    },
  });

  const exercises = {
    "dumbell": "Dumbell Curls",
    "shldpress": "Shoulder Press",
    "pushup": "Push Ups",
    "squats": "Squats",
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <Container sx={{ marginTop: 4 }}>
        <Grid2 container spacing={4} direction="column">
          <Grid2 item xs={12}>
            <Card elevation={3}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Overall Exercise Totals
                </Typography>
                <Typography variant="body1">
                  Total Exercise Count: {overallTotals.count}
                </Typography>
                <Typography variant="body1">
                  Total Calories Burnt: {overallTotals.calories}
                </Typography>
              </CardContent>
            </Card>
          </Grid2>

          <Grid2 item xs={12} sm={6}>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label="Select Date"
                value={selectedDate}
                onChange={(newValue) => {
                  if (newValue) {
                    setSelectedDate(newValue);
                  }
                }}
                sx={[(theme) => theme.applyStyles("dark")]}
                renderInput={(params) => <TextField fullWidth {...params} />}
              />
            </LocalizationProvider>
          </Grid2>

          <Grid2 item xs={12}>
            <Card elevation={3}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Data for {selectedDate.format("MMMM D, YYYY")}
                </Typography>
                {filteredData.length > 0 ? (
                  <List>
                    {filteredData.map((record, index) => (
                      <ListItem key={index} divider>
                        <ListItemText
                          primary={`${exercises[record.exercise]}`}
                          secondary={
                            <Typography
                              component="span"
                              variant="body2"
                              color="textSecondary"
                            >
                              {`Count: ${record.count}`}
                              <br />
                              {`Calories Burnt: ${record.calories} on ${dayjs(
                                record.date
                              ).format("h:mm A")}`}
                              <br />
                              {`Weight: ${record.weight} kg`}
                            </Typography>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography variant="body2">
                    No exercise data for this date.
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid2>
        </Grid2>
      </Container>
    </ThemeProvider>
  );
};

export default Dashboard;
