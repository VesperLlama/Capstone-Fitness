import React, { useRef, useEffect, useState } from 'react';
import './Dumbell.css'

const VideoStream = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [processedImage, setProcessedImage] = useState(null);

  // Initialize the webcam feed
  useEffect(() => {
    const video = videoRef.current;

    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          video.srcObject = stream;
        })
        .catch(err => {
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
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to image data (base64 format)
    canvas.toBlob(blob => {
      sendFrameToServer(blob);
    }, 'image/jpeg');
  };

  const sendFrameToServer = async (imageBlob) => {
    const formData = new FormData();
    formData.append('file', imageBlob, 'frame.jpg');
    
    const response = await fetch('http://localhost:8000/api/dumbell', {
      method: 'POST',
      body: formData,
    });
    
    if (response.ok) {
      const data = await response.json();
      setProcessedImage(data.image);  // Set the processed image received from the backend
    } else {
      console.error("Error processing frame:", response.statusText);
    }
  };

  return (
    <div>
      <video ref={videoRef} style={{ display: 'none' }} autoPlay muted width="640" height="480"></video>
      <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>

      {/* Display the processed image */}
      {processedImage && <img style={{ alignItems: 'center', justifyContent: 'center' }} src={processedImage} alt="Processed frame" />}

    </div>
  );
};

export default VideoStream;
