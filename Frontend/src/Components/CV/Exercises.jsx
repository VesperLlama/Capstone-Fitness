import React, { useRef, useEffect, useState } from "react";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import noCamera from "../../assets/noCamera.png";
import { Button } from "@mui/material";

function Exercises({ exercise }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const hasStopped = useRef(false);
  const [processedImage, setProcessedImage] = useState(noCamera);
  const [count, setCount] = useState(0);
  const [calories, setCalories] = useState(0);
  const [weight, setWeight] = useState(0);
  const [totalSeconds, setTotalSeconds] = useState(0);
  const [weightError, setWeightError] = useState(false);
  const [timeError, setTimeError] = useState(false);
  const [inputTime, setInputTime] = useState("05:00");
  const [timeLeft, setTimeLeft] = useState(300);
  const [isActive, setIsActive] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [MET, setMET] = useState(5);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(`${process.env.REACT_APP_WS_URL}cv/${exercise}`);

    ws.current.onopen = () => {
      console.log("WebSocket connection established.");
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProcessedImage(data.image);
      setCount((prevCount) => prevCount + data.count);
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.current.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  useEffect(() => {
    switch (exercise) {
      case "dumbell":
        setMET(5);
        break;
      case "shldpress":
        setMET(5);
        break;
      case "pushup":
        setMET(8);
        break;
      case "squats":
        setMET(5);
        break;
      default:
        break;
    }
  }, []);

  // Initialize the webcam feed
  useEffect(() => {
    const video = videoRef.current;

    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          video.srcObject = stream;
        })
        .catch((err) => {
          console.error("Error accessing webcam: ", err);
        });
    }
  }, []);

  // Capture and send frames periodically
  useEffect(() => {
    const interval = setInterval(captureFrame, 100);
    return () => clearInterval(interval);
  }, []);

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to image data (base64 format)
    canvas.toBlob((blob) => {
      sendFrameToServer(blob);
    }, "image/jpeg");
  };

  const sendFrameToServer = async (imageBlob) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64String = reader.result.split(",")[1];
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(base64String);
      }
    };
    reader.readAsDataURL(imageBlob);
  };

  // Timer

  const handleInputChange = (e) => {
    setInputTime(e.target.value);
  };

  const validateFields = () => {
    let validated = true;
    if (weight < 20) {
      setWeightError("Invalid Weight");
      validated = false;
    } else setWeightError(false);
    if (totalSeconds <= 0) {
      setTimeError("Time not set");
      validated = false;
    } else setTimeError(false);
    return validated;
  };

  const startTimer = () => {
    const [minutes, seconds] = inputTime.split(":").map(Number);
    setTotalSeconds(minutes * 60 + seconds);

    if (!validateFields()) return;
    else {
      setTimeLeft(totalSeconds);
      setIsActive(true);
      setIsPaused(false);
    }
  };

  const togglePauseResume = () => {
    if (isActive) {
      setIsActive(false);
      setIsPaused(true);
    } else {
      setIsActive(true);
      setIsPaused(false);
    }
  };

  useEffect(() => {
    let timer;
    if (isActive && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
    } else if (timeLeft === 0 && !hasStopped.current) {
      hasStopped.current = true;
      setIsActive(false);
      stop();
    }
    return () => clearInterval(timer);
  }, [isActive, timeLeft]);

  useEffect(() => {
    if (timeLeft >= 0) {
      const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0");
      const seconds = String(timeLeft % 60).padStart(2, "0");
      setInputTime(`${minutes}:${seconds}`);
    }
  }, [timeLeft]);

  // Calories calculation
  useEffect(() => {
    setCalories(MET * weight * ((totalSeconds - timeLeft) / 3600).toFixed(2));
  }, [count]);

  const reset = () => {
    setInputTime("00:00");
    setCount(0);
    setCalories(0);
    setIsActive(false);
    setTimeLeft(0);
  };

  const stop = async () => {
    const email = localStorage.getItem("loggedInEmail");

    if (email === null) return;

    const data = JSON.stringify({
      email: email,
      count: parseInt(Math.ceil(count)),
      calories: calories,
      exercise: exercise,
      date: new Date().toISOString(),
      weight: weight,
    });

    await fetch(`${process.env.REACT_APP_API_URL}addData`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: data,
    }).then(async (res) => {
      const result = await res.json();
      console.log(result.message);
    });
  };

  return (
    <Container maxWidth="lg" className="videoContainer">
      <div>
        <video
          ref={videoRef}
          style={{ display: "none" }}
          autoPlay
          muted
          width="640"
          height="480"
        ></video>
        <canvas ref={canvasRef} style={{ display: "none" }}></canvas>

        {processedImage && (
          <img
            style={{
              alignItems: "center",
              justifyContent: "center",
              width: "640px",
              height: "480px",
            }}
            src={processedImage}
            alt="Camera Feed"
          />
        )}
      </div>
      <div className="data">
        <div>
          <TextField
            error={weightError}
            label="Enter your weight"
            id="outlined-start-adornment"
            sx={{ m: 1, width: "25ch" }}
            slotProps={{
              input: {
                endAdornment: (
                  <InputAdornment position="start">kg</InputAdornment>
                ),
              },
            }}
            onChange={(e) => setWeight(e.target.value)}
            helperText={weightError}
          />
        </div>
        <div className="countC">
          <div>
            <h4>Count</h4>
            <p style={{ textAlign: "center" }}>{count}</p>
          </div>
          <div>
            <h4>Calories</h4>
            <p style={{ textAlign: "center" }}>
              {calories} <span style={{ fontSize: "small" }}>cal</span>
            </p>
          </div>
        </div>
        <div className="time">
          <h4>Time</h4>
          <TextField
            error={timeError}
            helperText={timeError}
            id="outlined-basic"
            label="Time (MM:SS)"
            value={inputTime}
            variant="outlined"
            onChange={handleInputChange}
            placeholder="MM:SS"
            sx={{ width: 0.4 }}
          />
        </div>
        <div className="buttons">
          <Button
            variant="contained"
            onClick={startTimer}
            disabled={isActive || isPaused}
          >
            Start
          </Button>
          <Button
            variant="outlined"
            onClick={togglePauseResume}
            disabled={timeLeft === 0}
          >
            {!isPaused ? "Pause" : "Resume"}
          </Button>
          <Button variant="outlined" color="error" onClick={reset}>
            Reset
          </Button>
        </div>
      </div>
    </Container>
  );
}

export default Exercises;
